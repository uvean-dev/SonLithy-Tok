# sonlithy-tok-v1
SonLithy 3.5 Tokenizer: a byte-level BPE tokenizer project for the SonLithy 3.5 model

## Project status

This repository currently contains the tokenizer project scaffold. The tokenizer,
training pipeline, and evaluation tools are not implemented. Design choices that
still need experiments are marked as drafts or open questions in `configs/` and
`docs/`.

## Development setup

Python 3.10 or newer is required. Install the package and development tools with:

```shell
python -m pip install -e ".[dev]"
```

Install the local hooks with `pre-commit install`. Run the checks directly with
`ruff check .`, `ruff format --check .`, and `pytest`.

See `docs/SPECIFICATION.md` for current decisions and unresolved design questions.
