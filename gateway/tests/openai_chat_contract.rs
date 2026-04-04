//! Contract tests: non-stream JSON and SSE (`text/event-stream`) for Chat Completions.

use axum::{body::Body, http::Request, http::StatusCode};
use http_body_util::BodyExt;
use serde_json::json;
use tower::ServiceExt;

#[tokio::test]
async fn health_returns_ok() {
    let mut app = mycel_gateway::router();
    let response = app
        .oneshot(Request::get("/health").body(Body::empty()).unwrap())
        .await
        .unwrap();
    assert_eq!(response.status(), StatusCode::OK);
}

#[tokio::test]
async fn chat_completions_json_when_not_streaming() {
    let mut app = mycel_gateway::router();
    let body = json!({ "model": "claude-test" });
    let response = app
        .oneshot(
            Request::builder()
                .method("POST")
                .uri("/v1/chat/completions")
                .header("content-type", "application/json")
                .body(Body::from(body.to_string()))
                .unwrap(),
        )
        .await
        .unwrap();
    assert_eq!(response.status(), StatusCode::OK);
    let bytes = response.into_body().collect().await.unwrap().to_bytes();
    let v: serde_json::Value = serde_json::from_slice(&bytes).unwrap();
    assert_eq!(v["object"], "chat.completion");
    assert!(v["choices"][0]["message"]["content"]
        .as_str()
        .unwrap()
        .contains("mycel-gateway stub"));
}

#[tokio::test]
async fn chat_completions_sse_when_stream_true() {
    let mut app = mycel_gateway::router();
    let body = json!({ "model": "kimi-test", "stream": true });
    let response = app
        .oneshot(
            Request::builder()
                .method("POST")
                .uri("/v1/chat/completions")
                .header("content-type", "application/json")
                .body(Body::from(body.to_string()))
                .unwrap(),
        )
        .await
        .unwrap();
    assert_eq!(response.status(), StatusCode::OK);
    let ct = response
        .headers()
        .get(axum::http::header::CONTENT_TYPE)
        .unwrap()
        .to_str()
        .unwrap();
    assert!(
        ct.contains("text/event-stream"),
        "expected text/event-stream, got {ct}"
    );
    let bytes = response.into_body().collect().await.unwrap().to_bytes();
    let text = String::from_utf8(bytes.to_vec()).unwrap();
    assert!(text.contains("data: "), "body: {text}");
    assert!(text.contains("chat.completion.chunk"), "body: {text}");
    assert!(text.contains("data: [DONE]"), "body: {text}");
}
