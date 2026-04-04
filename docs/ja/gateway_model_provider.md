# OpenAI 互換ゲートウェイ（Chat Completions） {#openai-compatible-gateway-chat-completions}

すべてのモデルトラフィックを、[OpenAI Chat Completions API](https://platform.openai.com/docs/api-reference/chat)（SSE ストリーミングを含む）を実装した**別 HTTP サービス**経由にルーティングできます。Python SDK は引き続き [`OpenAIChatCompletionsModel`][agents.models.openai_chatcompletions.OpenAIChatCompletionsModel] と既存の chat-completions コンバーターを使います。`base_url`（および任意で `api_key`）だけをゲートウェイに向けます。

## このリポジトリ内 {#in-this-repository}

Mycel フォークはリポジトリルートの `gateway/` に **Rust 製ゲートウェイスタブ**（バイナリ `mycel-gateway`）を含みます。**`POST /v1/chat/completions`** の **JSON** と **SSE**（`stream: true`）の両方を実装し、`gateway/` で Rust の**契約テスト**（`cargo test`）を通し、CI でビルドされます。Python wheel には**同梱されません**。SDK は `pip`/`uv` でインストールし、ゲートウェイは別プロセスまたはコンテナとして実行・展開してください。`gateway/README.md` に、ゲートウェイを Python パッケージに「埋め込まない」理由があります。

## 最小セットアップ {#minimal-setup}

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

ゲートウェイは次を満たす必要があります。

- OpenAI と同じ JSON ボディの `POST /v1/chat/completions` を受け付ける。
- 非ストリーミングでは Chat Completions JSON、ストリーミングでは OpenAI クライアント互換の SSE を返す。
- 論理モデル名を上流 API にマッピングする。

## 例 {#examples}

- [`examples/model_providers/gateway_chatcompletions.py`](https://github.com/MycelAI/mycel-agent-sdk/tree/main/examples/model_providers/gateway_chatcompletions.py)

## 関連 {#related}

- 名前空間付きモデル ID をゲートウェイに渡す場合は、[`MultiProvider`][agents.MultiProvider] で `unknown_prefix_mode="model_id"`。
- 組み込みコーディングツール：[`CODING_TOOLKIT`][agents.CODING_TOOLKIT] と [`PermissionMode`][agents.PermissionMode]。
