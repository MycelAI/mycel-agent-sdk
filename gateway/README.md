# `mycel-gateway` (in-monorepo)

Rust **HTTP sidecar** implementing the [OpenAI Chat Completions](https://platform.openai.com/docs/api-reference/chat) JSON shape (non-streaming stub). Implementation **source code is Mycel-original** (API-compatible wire format only; not derived from the OpenAI Agents SDK Python tree). Same repo **MIT** license; see the repository root `LICENSE` and `NOTICE`. The Python SDK stays a normal `openai` client; it does **not** bundle or import this binary.

## Why not “embedded” in the Python wheel?

- The gateway is a **server** (listening socket, async runtime, provider HTTP clients). The SDK is a **library** that calls `POST /v1/chat/completions` over HTTP.
- Shipping the gateway *inside* the same PyPI package would mean either spawning a subprocess, binding ports from import time, or re-implementing routing in-process—none of which match how `AsyncOpenAI` is meant to work.
- **Monorepo** = one git repo, **two artifacts**: `pip install mycel-agent-sdk` (Python) and `mycel-gateway` binary or Docker image (Rust).

## Docker (standalone image)

```bash
docker build -t mycel-gateway .
docker run --rm -p 8080:8080 mycel-gateway
```

(Build context must be this `gateway/` directory.)

## Run locally

```bash
cd gateway
cargo run --release
```

Defaults to `0.0.0.0:8080`. Override with `MYCEL_GATEWAY_BIND=127.0.0.1:9000`.

- `GET /health` → `ok`
- `POST /v1/chat/completions` with JSON body:
  - `"stream": false` or omitted → non-streaming `chat.completion` JSON
  - `"stream": true` → `text/event-stream` SSE chunks (`chat.completion.chunk` + `data: [DONE]`)

Contract tests: `cargo test --manifest-path gateway/Cargo.toml`.

## Next steps (product)

- Replace stub responses with real provider calls and usage metrics.
- Per-model routing, retries, provider SDKs, secrets from env.
- Container image build and publish (e.g. GHCR) from CI.
