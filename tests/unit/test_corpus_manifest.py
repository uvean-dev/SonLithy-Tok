"""Corpus manifest rules (D-009) on synthetic records. No real corpus is used."""

import pytest

from sonlithy_tok.corpus_manifest import (
    ManifestError,
    bytes_by_language,
    make_record,
    validate_records,
)


def _rec(doc_id="d1", text="hello world", **overrides):
    fields = dict(
        doc_id=doc_id,
        source="synthetic",
        license="CC0-1.0",
        language="en",
        category="natural",
        text=text,
        split="train",
    )
    fields.update(overrides)
    return make_record(**fields)


def test_valid_records_pass():
    validate_records([_rec("a", "one"), _rec("b", "two")])


def test_record_stores_hash_and_byte_count_not_text():
    r = _rec(text="\u00e9")
    assert r.utf8_bytes == 2
    assert len(r.sha256) == 64
    assert "\u00e9" not in repr(r)


@pytest.mark.parametrize("licence", ["", "  ", "unknown", "None"])
def test_missing_licence_is_rejected(licence):
    with pytest.raises(ManifestError, match="licence"):
        validate_records([_rec(license=licence)])


def test_duplicate_content_is_rejected():
    with pytest.raises(ManifestError, match="duplicate content"):
        validate_records([_rec("a", "same"), _rec("b", "same")])


def test_duplicate_doc_id_is_rejected():
    with pytest.raises(ManifestError, match="duplicate doc_id"):
        validate_records([_rec("a", "one"), _rec("a", "two")])


def test_flores_match_in_training_is_rejected():
    r = _rec("a", "held out")
    with pytest.raises(ManifestError, match="FLORES"):
        validate_records([r], flores_sha256=frozenset({r.sha256}))


def test_flores_match_marked_excluded_is_allowed():
    r = _rec("a", "held out", split="excluded")
    validate_records([r], flores_sha256=frozenset({r.sha256}))


def test_low_confidence_language_must_be_excluded():
    with pytest.raises(ManifestError, match="low-confidence"):
        validate_records([_rec(language="unknown", split="train")])


def test_unknown_language_code_is_rejected():
    with pytest.raises(ManifestError, match="language"):
        validate_records([_rec(language="xx")])


def test_lone_surrogate_text_is_rejected_at_record_creation():
    with pytest.raises(ValueError):
        _rec(text="a\ud800b")


def test_bytes_by_language_counts_only_requested_split():
    records = [
        _rec("a", "\u00e9", language="en", split="train"),
        _rec("b", "abc", language="en", split="validation"),
        _rec("c", "\u4f60", language="zh-Hans", split="train"),
    ]
    assert bytes_by_language(records, split="train") == {"en": 2, "zh-Hans": 3}
