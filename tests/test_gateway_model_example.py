"""Contract smoke tests for the gateway + OpenAI Chat Completions client pattern."""

from __future__ import annotations

from openai import AsyncOpenAI

from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel


def test_openai_chatcompletions_model_accepts_custom_base_url() -> None:
    client = AsyncOpenAI(base_url="http://127.0.0.1:8080/v1", api_key="test-key")
    model = OpenAIChatCompletionsModel(model="routed-model-id", openai_client=client)
    assert model.model == "routed-model-id"
    assert str(client.base_url).rstrip("/").endswith("/v1")
