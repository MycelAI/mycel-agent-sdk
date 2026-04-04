# Python image with the Mycel Agent SDK from this repository.
#
# Build (from repository root):
#   docker build -t mycel-agent-sdk -f docker/sdk/Dockerfile .
#
# Run against a gateway you already host:
#   docker run --rm -e OPENAI_BASE_URL=http://host.docker.internal:8080/v1 mycel-agent-sdk
#
# Compose (both services): see docker-compose.yml at repo root.

FROM python:3.12-slim-bookworm

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md uv.lock ./
COPY src ./src
COPY examples ./examples

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

ENV OPENAI_BASE_URL=http://gateway:8080/v1
ENV GATEWAY_API_KEY=gateway-internal-key
ENV GATEWAY_MODEL=gpt-4o-mini

# Demo against OPENAI_BASE_URL; override CMD for your app.
CMD ["python", "examples/model_providers/gateway_chatcompletions.py"]
