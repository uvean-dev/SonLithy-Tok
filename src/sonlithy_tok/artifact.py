"""Artifact format v1 (D-018): tokenizer.json plus meta.json with integrity checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import tokenizers
from tokenizers import Tokenizer

SCHEMA_VERSION = 1
TOKENIZER_FILE = "tokenizer.json"
META_FILE = "meta.json"
REQUIRED_META = ("schema_version", "tokenizers_version", "sha256", "vocab_size", "pipeline")
_RESERVED = frozenset(REQUIRED_META)


class ArtifactError(ValueError):
    """Raised when an artifact is missing, malformed, or fails an integrity check."""


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_artifact(
    tokenizer: Tokenizer,
    directory,
    *,
    pipeline: str,
    extra: dict | None = None,
) -> dict:
    """Write tokenizer.json and meta.json into directory and return the metadata."""
    extra = extra or {}
    clash = _RESERVED.intersection(extra)
    if clash:
        raise ArtifactError(f"extra metadata may not reuse reserved keys: {sorted(clash)}")
    target = Path(directory)
    target.mkdir(parents=True, exist_ok=True)
    tokenizer_path = target / TOKENIZER_FILE
    tokenizer.save(str(tokenizer_path))
    meta = {
        "schema_version": SCHEMA_VERSION,
        "tokenizers_version": tokenizers.__version__,
        "sha256": _sha256(tokenizer_path),
        "vocab_size": tokenizer.get_vocab_size(),
        "pipeline": pipeline,
        **extra,
    }
    (target / META_FILE).write_text(
        json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return meta


def load_artifact(directory) -> tuple[Tokenizer, dict]:
    """Load and verify an artifact. Any mismatch raises ArtifactError."""
    target = Path(directory)
    tokenizer_path = target / TOKENIZER_FILE
    meta_path = target / META_FILE
    if not tokenizer_path.is_file() or not meta_path.is_file():
        raise ArtifactError(f"missing {TOKENIZER_FILE} or {META_FILE} in {target}")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    missing = [key for key in REQUIRED_META if key not in meta]
    if missing:
        raise ArtifactError(f"meta.json lacks required keys: {missing}")
    if meta["schema_version"] != SCHEMA_VERSION:
        raise ArtifactError(f"unsupported schema_version {meta['schema_version']!r}")
    if _sha256(tokenizer_path) != meta["sha256"]:
        raise ArtifactError("sha256 mismatch: tokenizer.json changed since it was saved")
    if meta["tokenizers_version"] != tokenizers.__version__:
        raise ArtifactError(
            f"tokenizers version mismatch: artifact {meta['tokenizers_version']}, "
            f"installed {tokenizers.__version__}; re-verify before use"
        )
    tokenizer = Tokenizer.from_file(str(tokenizer_path))
    if tokenizer.get_vocab_size() != meta["vocab_size"]:
        raise ArtifactError("vocab_size in meta.json does not match tokenizer.json")
    return tokenizer, meta
