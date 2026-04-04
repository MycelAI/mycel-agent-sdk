//! `mycel-gateway` binary entrypoint.

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    mycel_gateway::run_from_env().await
}
