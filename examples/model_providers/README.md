# Model provider examples

This directory shows how to route models through **OpenAI-compatible HTTP endpoints** (including a
local gateway) and optional **any-llm** adapter flows.

## Any-LLM (OpenRouter)

```bash
export OPENROUTER_API_KEY="..."
```

```bash
uv run examples/model_providers/any_llm_provider.py
uv run examples/model_providers/any_llm_auto.py
uv run examples/model_providers/any_llm_provider.py --model openrouter/openai/gpt-5.4-mini
```

## OpenAI-compatible gateway

Point `OPENAI_BASE_URL` at your gateway’s `/v1` root (for example `http://127.0.0.1:8080/v1`):

```bash
export OPENAI_BASE_URL="http://127.0.0.1:8080/v1"
export GATEWAY_API_KEY="your-internal-key"
export GATEWAY_MODEL="your-logical-model-name"
uv run examples/model_providers/gateway_chatcompletions.py
```

See [Gateway model provider](../../docs/gateway_model_provider.md) for details.
