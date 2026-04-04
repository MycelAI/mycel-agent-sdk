# Optional Rust accelerator (`mycel_accelerator`)

The **HTTP gateway** for Chat Completions lives in **`../gateway/`** (separate binary). This directory
holds an experimental [PyO3](https://github.com/PyO3/pyo3) extension stub used by the Mycel fork for
future file/shell performance work.

The Python package **does not** depend on this crate. To experiment locally:

```bash
cd rust/mycel_accelerator
pip install maturin
maturin develop --release
```

Then from Python: `import mycel_accelerator; assert mycel_accelerator.echo_u64(7) == 7`.
