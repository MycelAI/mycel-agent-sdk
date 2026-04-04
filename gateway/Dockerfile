# Standalone image for `mycel-gateway` (OpenAI Chat Completions + SSE stub).
#
# Build (from this directory):
#   docker build -t mycel-gateway .
# Run:
#   docker run --rm -p 8080:8080 mycel-gateway
#
# Compose: see ../docker-compose.yml

FROM rust:1.85-bookworm AS builder
WORKDIR /build
COPY Cargo.toml ./
COPY src ./src
RUN cargo build --release

FROM debian:bookworm-slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates wget \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /build/target/release/mycel-gateway /usr/local/bin/mycel-gateway
ENV MYCEL_GATEWAY_BIND=0.0.0.0:8080
EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/mycel-gateway"]
