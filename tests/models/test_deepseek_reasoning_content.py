from typing import Any

from agents.models.chatcmpl_converter import Converter


def test_deepseek_reasoning_content_with_openai_chatcompletions_path():
    """Verify reasoning_content works when using OpenAI Chat Completions-shaped history."""
    input_items: list[Any] = [
        {"role": "user", "content": "What's the weather in Paris?"},
        {
            "id": "__fake_id__",
            "summary": [{"text": "I need to check the weather in Paris.", "type": "summary_text"}],
            "type": "reasoning",
            "content": None,
            "encrypted_content": None,
            "status": None,
            "provider_data": {"model": "deepseek-reasoner", "response_id": "chatcmpl-test"},
        },
        {
            "arguments": '{"city": "Paris"}',
            "call_id": "call_weather_456",
            "name": "get_weather",
            "type": "function_call",
            "id": "__fake_id__",
            "status": None,
            "provider_data": {"model": "deepseek-reasoner"},
        },
        {
            "type": "function_call_output",
            "call_id": "call_weather_456",
            "output": "The weather in Paris is cloudy and 15°C.",
        },
    ]

    messages = Converter.items_to_messages(
        input_items,
        model="deepseek-reasoner",
    )

    assistant_with_tools = None
    for msg in messages:
        if isinstance(msg, dict) and msg.get("role") == "assistant" and msg.get("tool_calls"):
            assistant_with_tools = msg
            break

    assert assistant_with_tools is not None
    assert "reasoning_content" in assistant_with_tools
    assert assistant_with_tools["reasoning_content"] == "I need to check the weather in Paris."  # type: ignore[typeddict-item]


def test_reasoning_content_from_other_provider_not_attached_to_deepseek():
    """Verify reasoning_content from non-DeepSeek providers is NOT attached to DeepSeek messages."""
    input_items: list[Any] = [
        {"role": "user", "content": "What's the weather in Paris?"},
        {
            "id": "__fake_id__",
            "summary": [{"text": "Claude's reasoning about the weather.", "type": "summary_text"}],
            "type": "reasoning",
            "content": None,
            "encrypted_content": None,
            "status": None,
            "provider_data": {"model": "claude-sonnet-4-20250514", "response_id": "chatcmpl-test"},
        },
        {
            "arguments": '{"city": "Paris"}',
            "call_id": "call_weather_789",
            "name": "get_weather",
            "type": "function_call",
            "id": "__fake_id__",
            "status": None,
            "provider_data": {"model": "claude-sonnet-4-20250514"},
        },
        {
            "type": "function_call_output",
            "call_id": "call_weather_789",
            "output": "The weather in Paris is cloudy.",
        },
    ]

    messages = Converter.items_to_messages(
        input_items,
        model="deepseek-reasoner",
    )

    assistant_with_tools = None
    for msg in messages:
        if isinstance(msg, dict) and msg.get("role") == "assistant" and msg.get("tool_calls"):
            assistant_with_tools = msg
            break

    assert assistant_with_tools is not None
    assert "reasoning_content" not in assistant_with_tools


def test_reasoning_content_without_provider_data_attached_for_backward_compat():
    """Reasoning items without provider_data still attach reasoning_content for DeepSeek."""
    input_items: list[Any] = [
        {"role": "user", "content": "What's the weather in Tokyo?"},
        {
            "id": "__fake_id__",
            "summary": [{"text": "Reasoning without provider info.", "type": "summary_text"}],
            "type": "reasoning",
            "content": None,
            "encrypted_content": None,
            "status": None,
        },
        {
            "arguments": '{"city": "Tokyo"}',
            "call_id": "call_weather_101",
            "name": "get_weather",
            "type": "function_call",
            "id": "__fake_id__",
            "status": None,
        },
        {
            "type": "function_call_output",
            "call_id": "call_weather_101",
            "output": "The weather in Tokyo is sunny.",
        },
    ]

    messages = Converter.items_to_messages(
        input_items,
        model="deepseek-reasoner",
    )

    assistant_with_tools = None
    for msg in messages:
        if isinstance(msg, dict) and msg.get("role") == "assistant" and msg.get("tool_calls"):
            assistant_with_tools = msg
            break

    assert assistant_with_tools is not None
    assert "reasoning_content" in assistant_with_tools
    assert assistant_with_tools["reasoning_content"] == "Reasoning without provider info."  # type: ignore[typeddict-item]
