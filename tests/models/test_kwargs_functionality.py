import pytest
from openai.types.chat.chat_completion import ChatCompletion, Choice
from openai.types.chat.chat_completion_message import ChatCompletionMessage
from openai.types.completion_usage import CompletionUsage

from agents.model_settings import ModelSettings
from agents.models.interface import ModelTracing
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel


@pytest.mark.allow_call_model_methods
@pytest.mark.asyncio
async def test_openai_chatcompletions_kwargs_forwarded(monkeypatch):
    """ModelSettings.extra_args are forwarded to the OpenAI chat completions API."""
    captured: dict[str, object] = {}

    class MockChatCompletions:
        async def create(self, **kwargs):
            captured.update(kwargs)
            msg = ChatCompletionMessage(role="assistant", content="test response")
            choice = Choice(index=0, message=msg, finish_reason="stop")
            return ChatCompletion(
                id="test-id",
                created=0,
                model="gpt-4",
                object="chat.completion",
                choices=[choice],
                usage=CompletionUsage(completion_tokens=5, prompt_tokens=10, total_tokens=15),
            )

    class MockChat:
        def __init__(self):
            self.completions = MockChatCompletions()

    class MockClient:
        def __init__(self):
            self.chat = MockChat()
            self.base_url = "https://api.openai.com/v1"

    settings = ModelSettings(
        temperature=0.7,
        extra_args={
            "seed": 123,
            "logit_bias": {456: 10},
            "stop": ["STOP", "END"],
            "user": "test-user",
        },
    )

    mock_client = MockClient()
    model = OpenAIChatCompletionsModel(model="gpt-4", openai_client=mock_client)  # type: ignore

    await model.get_response(
        system_instructions="Test system",
        input="test input",
        model_settings=settings,
        tools=[],
        output_schema=None,
        handoffs=[],
        tracing=ModelTracing.DISABLED,
        previous_response_id=None,
    )

    assert captured["seed"] == 123
    assert captured["logit_bias"] == {456: 10}
    assert captured["stop"] == ["STOP", "END"]
    assert captured["user"] == "test-user"
    assert captured["temperature"] == 0.7
