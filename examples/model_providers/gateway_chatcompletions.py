"""Use OpenAIChatCompletionsModel against an OpenAI-compatible HTTP gateway.

Set OPENAI_BASE_URL to your gateway (e.g. http://127.0.0.1:8080/v1) and GATEWAY_API_KEY if required.

    uv run examples/model_providers/gateway_chatcompletions.py
"""

from __future__ import annotations

import asyncio
import os

from openai import AsyncOpenAI

from agents import Agent, OpenAIChatCompletionsModel, Runner


async def main() -> None:
    base_url = os.environ.get("OPENAI_BASE_URL", "http://127.0.0.1:8080/v1")
    api_key = os.environ.get("GATEWAY_API_KEY", "gateway-internal-key")
    model_name = os.environ.get("GATEWAY_MODEL", "gpt-4o-mini")

    client = AsyncOpenAI(base_url=base_url, api_key=api_key)
    agent = Agent(
        name="GatewayAssistant",
        instructions="You are a concise assistant.",
        model=OpenAIChatCompletionsModel(model=model_name, openai_client=client),
    )
    result = await Runner.run(agent, "Say hello in one short sentence.")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
