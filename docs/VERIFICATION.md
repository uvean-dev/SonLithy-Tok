# Verification log

Records what has been run in a target environment, with the exact command and result.
Verification is not a design approval; see docs/decisions.md for decisions.

## 2026-10-29: environment install and lint (Codespaces)

- Environment: GitHub Codespaces, Linux x86_64, Python 3.11.18 (uv-managed venv at .venv)
- Commit: 4406860 (origin/main at time of run)
- Command: uv pip install --only-binary :all: "tokenizers==0.23.3"
  Result: installed; tokenizers.__version__ == 0.23.3
- Command: uv pip install -e ".[dev]"
  Result: installed sonlithy-tok-v1 0.1.0 (editable)
- Command: ruff check .
  Result: All checks passed!
- Command: ruff format --check .
  Result: 24 files already formatted
- Command: pytest
  Result: 2 passed (tests/unit/test_config.py, tests/unit/test_package.py)
- Not run: any test of Split, ByteLevel, BPE training, encoding or decoding.
  Status: Split behaviour on tokenizers==0.23.3 is Not tested.
