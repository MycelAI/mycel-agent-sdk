//! Optional native accelerator bindings (stub).
//!
//! Build locally with `maturin develop` from this directory after installing Rust and maturin.
//! The Python SDK does not require this module at runtime.

use pyo3::prelude::*;

#[pyfunction]
fn echo_u64(x: u64) -> u64 {
    x
}

#[pymodule]
fn mycel_accelerator(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(echo_u64, m)?)?;
    Ok(())
}
