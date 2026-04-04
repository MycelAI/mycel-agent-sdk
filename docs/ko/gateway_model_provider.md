# OpenAI 호환 게이트웨이(Chat Completions) {#openai-compatible-gateway-chat-completions}

[OpenAI Chat Completions API](https://platform.openai.com/docs/api-reference/chat)(SSE 스트리밍 포함)를 구현한 **별도 HTTP 서비스**를 통해 모든 모델 트래픽을 라우팅할 수 있습니다. Python SDK는 계속 [`OpenAIChatCompletionsModel`][agents.models.openai_chatcompletions.OpenAIChatCompletionsModel]과 기존 chat-completions 변환 스택을 사용하며, `base_url`(필요 시 `api_key`)만 게이트웨이를 가리키면 됩니다.

## 이 리포지토리에서 {#in-this-repository}

Mycel 포크는 리포지토리 루트 `gateway/`에 **Rust 게이트웨이 스텁**(바이너리 `mycel-gateway`)을 둡니다. **`POST /v1/chat/completions`**를 **JSON** 및 **SSE**(`stream: true`) 모두 구현하고, `gateway/`에서 Rust **계약 테스트**(`cargo test`)를 통과하며 CI에서 빌드됩니다. Python wheel에는 **포함되지 않습니다**. SDK는 `pip`/`uv`로 설치하고 게이트웨이는 별도 프로세스나 컨테이너로 실행·배포하세요. `gateway/README.md`에 게이트웨이를 Python 패키지에 “포함하지 않는” 이유가 있습니다.

## 최소 설정 {#minimal-setup}

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

게이트웨이는 다음을 만족해야 합니다.

- OpenAI와 동일한 JSON 본문의 `POST /v1/chat/completions`를 받음.
- 비스트리밍 시 Chat Completions JSON, 스트리밍 시 OpenAI 클라이언트 호환 SSE 청크를 반환.
- 논리 모델 이름을 업스트림 API에 매핑.

## 예시 {#examples}

- [`examples/model_providers/gateway_chatcompletions.py`](https://github.com/MycelAI/mycel-agent-sdk/tree/main/examples/model_providers/gateway_chatcompletions.py)

## 관련 {#related}

- 네임스페이스 모델 ID를 게이트웨이로 넘기려면 [`MultiProvider`][agents.MultiProvider]에 `unknown_prefix_mode="model_id"`.
- 내장 코딩 도구: [`CODING_TOOLKIT`][agents.CODING_TOOLKIT] 및 [`PermissionMode`][agents.PermissionMode].
