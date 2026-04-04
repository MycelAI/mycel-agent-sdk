# Docker: gateway + Python SDK

Two images, used **together** via Compose or **separately** as needed.

## Combined (gateway + demo client)

From the **repository root**:

```bash
docker compose up --build
```

- **gateway** listens on `localhost:8080` (override host port with `MYCEL_GATEWAY_PORT=9000`).
- **sdk** runs `examples/model_providers/gateway_chatcompletions.py` against `http://gateway:8080/v1`.

## Rust gateway only

```bash
docker build -t mycel-gateway -f gateway/Dockerfile gateway
docker run --rm -p 8080:8080 mycel-gateway
```

## Python SDK only

Build the library image (no gateway):

```bash
docker build -t mycel-agent-sdk -f docker/sdk/Dockerfile .
```

Run your code or the bundled example against **any** OpenAI-compatible base URL:

```bash
docker run --rm \
  -e OPENAI_BASE_URL=http://host.docker.internal:8080/v1 \
  -e GATEWAY_API_KEY=gateway-internal-key \
  mycel-agent-sdk
```

Replace `host.docker.internal` with your gateway hostname or IP. On Linux, use the host bridge IP or `--network host` if appropriate.

**Compose** without starting the bundled gateway service:

```bash
docker compose run --rm --no-deps \
  -e OPENAI_BASE_URL=http://your.remote.gateway:8080/v1 \
  sdk
```

## Notes

- The PyPI distribution name is `mycel-agent-sdk`; `import agents` is unchanged.
- The gateway image is a **stub** (no real LLM). Swap the image for your production gateway or extend `gateway/`.
