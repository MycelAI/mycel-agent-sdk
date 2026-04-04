"""Normalize chat completion message lists for strict tool-call ordering.

Some providers require each assistant tool_calls block to be immediately followed by
the matching tool result messages. Shared by chat-completions model adapters.
"""

from __future__ import annotations

from typing import Any, cast

from openai.types.chat import ChatCompletionMessageParam


def fix_tool_message_ordering(
    messages: list[ChatCompletionMessageParam],
) -> list[ChatCompletionMessageParam]:
    """Reorder tool results so each tool_use is immediately followed by its tool result."""
    if not messages:
        return messages

    tool_call_messages: dict[str, tuple[int, ChatCompletionMessageParam]] = {}
    tool_result_messages: dict[str, tuple[int, ChatCompletionMessageParam]] = {}
    paired_tool_result_indices: set[int] = set()
    fixed_messages: list[ChatCompletionMessageParam] = []
    used_indices: set[int] = set()

    for index, message in enumerate(messages):
        if not isinstance(message, dict):
            continue
        message_dict = cast(dict[str, Any], message)

        if message_dict.get("role") == "assistant" and message_dict.get("tool_calls"):
            tool_calls = message_dict.get("tool_calls", [])
            if isinstance(tool_calls, list):
                for tool_call in tool_calls:
                    if isinstance(tool_call, dict) and tool_call.get("id"):
                        single_tool_msg = message_dict.copy()
                        single_tool_msg["tool_calls"] = [tool_call]
                        tool_call_messages[str(tool_call["id"])] = (
                            index,
                            cast(ChatCompletionMessageParam, single_tool_msg),
                        )
        elif message_dict.get("role") == "tool" and message_dict.get("tool_call_id"):
            tool_result_messages[str(message_dict["tool_call_id"])] = (
                index,
                cast(ChatCompletionMessageParam, message_dict),
            )

    for tool_id in tool_call_messages:
        if tool_id in tool_result_messages:
            paired_tool_result_indices.add(tool_result_messages[tool_id][0])

    for index, original_message in enumerate(messages):
        if index in used_indices:
            continue

        if not isinstance(original_message, dict):
            fixed_messages.append(original_message)
            used_indices.add(index)
            continue

        role = original_message.get("role")
        if role == "assistant" and original_message.get("tool_calls"):
            tool_calls = original_message.get("tool_calls", [])
            if isinstance(tool_calls, list):
                for tool_call in tool_calls:
                    if not isinstance(tool_call, dict):
                        continue
                    tool_id_value = tool_call.get("id")
                    if not isinstance(tool_id_value, str):
                        continue
                    tool_id = tool_id_value
                    if tool_id in tool_call_messages and tool_id in tool_result_messages:
                        _, tool_call_message = tool_call_messages[tool_id]
                        tool_result_index, tool_result_message = tool_result_messages[tool_id]
                        fixed_messages.append(tool_call_message)
                        fixed_messages.append(tool_result_message)
                        used_indices.add(tool_call_messages[tool_id][0])
                        used_indices.add(tool_result_index)
                    elif tool_id in tool_call_messages:
                        _, tool_call_message = tool_call_messages[tool_id]
                        fixed_messages.append(tool_call_message)
                        used_indices.add(tool_call_messages[tool_id][0])
            used_indices.add(index)
        elif role == "tool":
            if index not in paired_tool_result_indices:
                fixed_messages.append(original_message)
            used_indices.add(index)
        else:
            fixed_messages.append(original_message)
            used_indices.add(index)

    return fixed_messages
