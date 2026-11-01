"""Corpus manifest rules (D-009).

A record describes a document by its hash and metadata. It never stores the text.
These rules are checked before any corpus is used for tokenizer training.
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterable
from dataclasses import dataclass

from sonlithy_tok.normalization import check_input

LANGUAGES = frozenset(
    {
        "en",
        "zh-Hans",
        "zh-Hant",
        "hi",
        "hi-Latn",
        "es",
        "ru",
        "pt",
        "de",
        "code",
        "structured",
        "tech_doc",
        "unknown",
    }
)
CATEGORIES = frozenset({"natural", "code", "structured", "tech_doc"})
SPLITS = frozenset({"train", "validation", "test", "excluded"})
_UNUSABLE_LICENCES = frozenset({"", "unknown", "none", "unlicensed"})


class ManifestError(ValueError):
    """Raised when a manifest violates a D-009 rule."""


@dataclass(frozen=True)
class DocRecord:
    doc_id: str
    source: str
    license: str
    language: str
    category: str
    utf8_bytes: int
    sha256: str
    split: str


def make_record(
    *,
    doc_id: str,
    source: str,
    license: str,
    language: str,
    category: str,
    text: str,
    split: str,
) -> DocRecord:
    """Build a record. The text is checked (D-010) and hashed, then discarded."""
    data = check_input(text).encode("utf-8")
    return DocRecord(
        doc_id=doc_id,
        source=source,
        license=license,
        language=language,
        category=category,
        utf8_bytes=len(data),
        sha256=hashlib.sha256(data).hexdigest(),
        split=split,
    )


def validate_records(
    records: Iterable[DocRecord], flores_sha256: frozenset[str] = frozenset()
) -> None:
    """Raise ManifestError on the first violated rule."""
    seen_ids: set[str] = set()
    seen_hashes: set[str] = set()
    for r in records:
        if r.license.strip().lower() in _UNUSABLE_LICENCES:
            raise ManifestError(f"{r.doc_id}: licence missing (rule 1)")
        if r.language not in LANGUAGES:
            raise ManifestError(f"{r.doc_id}: unknown language code {r.language!r}")
        if r.category not in CATEGORIES:
            raise ManifestError(f"{r.doc_id}: unknown category {r.category!r}")
        if r.split not in SPLITS:
            raise ManifestError(f"{r.doc_id}: unknown split {r.split!r}")
        if r.language == "unknown" and r.split != "excluded":
            raise ManifestError(f"{r.doc_id}: low-confidence language must be excluded (rule 8)")
        if r.doc_id in seen_ids:
            raise ManifestError(f"{r.doc_id}: duplicate doc_id")
        if r.sha256 in seen_hashes:
            raise ManifestError(f"{r.doc_id}: duplicate content (rule 5)")
        if r.sha256 in flores_sha256 and r.split != "excluded":
            raise ManifestError(f"{r.doc_id}: matches FLORES-200 devtest (rule 7)")
        seen_ids.add(r.doc_id)
        seen_hashes.add(r.sha256)


def bytes_by_language(records: Iterable[DocRecord], split: str = "train") -> dict[str, int]:
    """Sum UTF-8 bytes per language for one split (used for the measurement in rule 3)."""
    totals: dict[str, int] = {}
    for r in records:
        if r.split == split:
            totals[r.language] = totals.get(r.language, 0) + r.utf8_bytes
    return totals
