# OpenAI 兼容网关（Chat Completions） {#openai-compatible-gateway-chat-completions}

你可以通过单独的 HTTP 服务路由所有模型流量，该服务实现 [OpenAI Chat Completions API](https://platform.openai.com/docs/api-reference/chat)（含 SSE 流式）。Python SDK 仍使用 [`OpenAIChatCompletionsModel`][agents.models.openai_chatcompletions.OpenAIChatCompletionsModel] 与现有 chat-completions 转换栈；仅需将 `base_url`（以及可选的 `api_key`）指向你的网关。

## 本仓库内 {#in-this-repository}

Mycel 分支在仓库根目录 `gateway/` 提供 **Rust 网关桩**（二进制 `mycel-gateway`）。它实现 **`POST /v1/chat/completions`** 的 **JSON** 与 **SSE**（`stream: true`）两种路径，在 `gateway/` 下通过 Rust **契约测试**（`cargo test`），并在 CI 中构建。它**不会**打入 Python wheel：请用 `pip`/`uv` 安装 SDK，并将网关作为独立进程或容器运行或部署。`gateway/README.md` 说明了网关为何不“嵌入” Python 包。

## 最小示例 {#minimal-setup}

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

网关应：

- 接受与 OpenAI 相同 JSON 请求体的 `POST /v1/chat/completions`。
- 返回与 OpenAI 客户端兼容的非流式 Chat Completions JSON 或流式 SSE。
- 将逻辑模型名映射到上游 API。

## 示例 {#examples}

- [`examples/model_providers/gateway_chatcompletions.py`](https://github.com/MycelAI/mycel-agent-sdk/tree/main/examples/model_providers/gateway_chatcompletions.py)

## 相关 {#related}

- 若将带命名空间的模型 ID 直接传给网关，可配合 [`MultiProvider`][agents.MultiProvider] 使用 `unknown_prefix_mode="model_id"`。
- 内置编码工具：[`CODING_TOOLKIT`][agents.CODING_TOOLKIT] 与 [`PermissionMode`][agents.PermissionMode]。
