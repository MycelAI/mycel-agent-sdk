# OpenAI-compatible gateway (Chat Completions)

You can route all model traffic through a **separate HTTP service** that implements the [OpenAI Chat Completions API](https://platform.openai.com/docs/api-reference/chat) (including streaming with SSE). The Python SDK keeps using [`OpenAIChatCompletionsModel`][agents.models.openai_chatcompletions.OpenAIChatCompletionsModel] and the existing chat-completions converter stack; only the `base_url` (and optionally `api_key`) point at your gateway.

## In this repository

The Mycel fork includes a **Rust gateway stub** at the repository root in `gateway/` (binary `mycel-gateway`). It implements **`POST /v1/chat/completions`** for both **JSON** and **SSE** (`stream: true`), passes Rust **contract tests** (`cargo test` in `gateway/`), and is built in CI. It is **not** shipped inside the Python wheel: install the SDK with `pip`/`uv`, run or deploy the gateway as its own process or container. The `gateway/README.md` file explains why the gateway is not “embedded” in the Python package.

## Minimal setup

```python
import os

from agents import Agent, OpenAIChatCompletionsModel, Runner
from openai import AsyncOpenAI

gateway = AsyncOpenAI(
    base_url=os.environ.get("OPENAI_BASE_URL", "http://127.0.0.1:8080/v1"),
    api_key=os.environ.get("GATEWAY_API_KEY", "gateway-internal-key"),
)

agent = Agent(
    name="GatewayAgent",
    instructions="You are a helpful assistant.",
    model=OpenAIChatCompletionsModel(
        model="claude-sonnet-4-20250514",  # routed by the gateway
        openai_client=gateway,
    ),
)

async def main():
    result = await Runner.run(agent, "Hello!")
    print(result.final_output)
```

The gateway should:

- Accept `POST /v1/chat/completions` with the same JSON body shape as OpenAI.
- Return Chat Completions JSON (non-streaming) or SSE chunks (streaming) compatible with OpenAI clients.
- Map your logical model names (for example provider-specific strings) to upstream APIs.

## Examples

- [`examples/model_providers/gateway_chatcompletions.py`](https://github.com/MycelAI/mycel-agent-sdk/tree/main/examples/model_providers/gateway_chatcompletions.py)

## Related

- [`MultiProvider`][agents.MultiProvider] with `unknown_prefix_mode="model_id"` if you pass through namespaced model IDs to the gateway.
- Built-in coding tools: [`CODING_TOOLKIT`][agents.CODING_TOOLKIT] and [`PermissionMode`][agents.PermissionMode].
