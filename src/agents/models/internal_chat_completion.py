"""OpenAI Chat Completions message subclasses for provider-specific fields.

Used by the chat completions converter and tests. Does not depend on LiteLLM.
"""

from __future__ import annotations

from typing import Any

from openai.types.chat.chat_completion_message import ChatCompletionMessage
from openai.types.chat.chat_completion_message_function_tool_call import (
    ChatCompletionMessageFunctionToolCall,
)


class InternalChatCompletionMessage(ChatCompletionMessage):
    """Carries reasoning_content and thinking_blocks without changing the base schema."""

    reasoning_content: str
    thinking_blocks: list[dict[str, Any]] | None = None


class InternalToolCall(ChatCompletionMessageFunctionToolCall):
    """Carries provider-specific metadata (e.g. Gemini thought signatures)."""

    extra_content: dict[str, Any] | None = None
