//! OpenAI Chat Completions-compatible HTTP surface (JSON and SSE streaming stub).

use axum::{
    body::Body,
    http::{header, StatusCode},
    response::{IntoResponse, Response},
    routing::{get, post},
    Json, Router,
};
use bytes::Bytes;
use serde_json::{json, Value};
use tower_http::trace::TraceLayer;

async fn health() -> &'static str {
    "ok"
}

fn stub_chat_completion_json(model: &str) -> Value {
    json!({
        "id": "chatcmpl-mycel-stub",
        "object": "chat.completion",
        "created": 0_i64,
        "model": model,
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": format!(
                    "mycel-gateway stub: model={model}. Implement provider calls and streaming here."
                )
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
    })
}

fn stub_stream_chunk_events(model: &str) -> Vec<Value> {
    let id = "chatcmpl-mycel-stub-stream";
    vec![
        json!({
            "id": id,
            "object": "chat.completion.chunk",
            "created": 0_i64,
            "model": model,
            "choices": [{
                "index": 0,
                "delta": {"role": "assistant"},
                "finish_reason": Value::Null
            }]
        }),
        json!({
            "id": id,
            "object": "chat.completion.chunk",
            "created": 0_i64,
            "model": model,
            "choices": [{
                "index": 0,
                "delta": {"content": format!("mycel-gateway stub (stream); model={model}. ")},
                "finish_reason": Value::Null
            }]
        }),
        json!({
            "id": id,
            "object": "chat.completion.chunk",
            "created": 0_i64,
            "model": model,
            "choices": [{
                "index": 0,
                "delta": Value::Object(Default::default()),
                "finish_reason": "stop"
            }]
        }),
    ]
}

fn sse_response_for_model(model: &str) -> Response {
    let events = stub_stream_chunk_events(model);
    let stream = async_stream::stream! {
        for event in events {
            let line = format!(
                "data: {}\n\n",
                serde_json::to_string(&event).expect("json serialize")
            );
            yield Ok::<_, std::io::Error>(Bytes::from(line));
        }
        yield Ok(Bytes::from("data: [DONE]\n\n"));
    };
    let body = Body::from_stream(stream);
    Response::builder()
        .status(StatusCode::OK)
        .header(header::CONTENT_TYPE, "text/event-stream; charset=utf-8")
        .header(header::CACHE_CONTROL, "no-cache")
        .body(body)
        .expect("valid response")
}

/// Core router (no global tracing layer). Unit and integration tests use this entry point.
pub fn router() -> Router {
    Router::new()
        .route("/health", get(health))
        .route("/v1/chat/completions", post(chat_completions))
}

pub async fn run_from_env() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "mycel_gateway=info,tower_http=info".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    let app = router().layer(TraceLayer::new_for_http());
    let host = std::env::var("MYCEL_GATEWAY_BIND").unwrap_or_else(|_| "0.0.0.0:8080".to_string());
    let listener = tokio::net::TcpListener::bind(&host).await?;
    tracing::info!("mycel-gateway listening on http://{}", host);
    axum::serve(listener, app).await?;
    Ok(())
}

async fn chat_completions(Json(body): Json<Value>) -> Result<Response, StatusCode> {
    let model = body
        .get("model")
        .and_then(|m| m.as_str())
        .unwrap_or("unknown");
    let stream = body.get("stream").and_then(|v| v.as_bool()).unwrap_or(false);
    if stream {
        Ok(sse_response_for_model(model))
    } else {
        Ok(Json(stub_chat_completion_json(model)).into_response())
    }
}
