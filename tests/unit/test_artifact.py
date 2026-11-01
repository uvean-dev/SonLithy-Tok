"""Artifact format v1 (D-018): save/load, integrity checks, committed pilot fixture."""

import json
from pathlib import Path

import pytest

from sonlithy_tok.artifact import ArtifactError, load_artifact, save_artifact
from sonlithy_tok.bpe_pilot import synthetic_corpus, train_pilot_tokenizer
from sonlithy_tok.encoding import decode, encode

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "pilot_v1"
SAMPLES = [
    "",
    "a",
    "\u00e9",
    "Hello,   world!",
    "\u4f60\u597d\u4e16\u754c",
    "\U0001f600 emoji",
    "def f(x):\n    return x\n",
]


@pytest.fixture(scope="module")
def pilot():
    return train_pilot_tokenizer(synthetic_corpus())


def _meta(path):
    return json.loads((path / "meta.json").read_text(encoding="utf-8"))


def _write_meta(path, meta):
    (path / "meta.json").write_text(json.dumps(meta), encoding="utf-8")


def test_save_then_load_gives_same_encoding(pilot, tmp_path):
    save_artifact(pilot, tmp_path, pipeline="probe")
    loaded, meta = load_artifact(tmp_path)
    for text in SAMPLES:
        assert encode(loaded, text) == encode(pilot, text)
    assert meta["vocab_size"] == pilot.get_vocab_size()


def test_meta_has_required_fields(pilot, tmp_path):
    save_artifact(pilot, tmp_path, pipeline="probe")
    meta = _meta(tmp_path)
    for key in ("schema_version", "tokenizers_version", "sha256", "vocab_size", "pipeline"):
        assert key in meta
    assert meta["schema_version"] == 1


def test_extra_metadata_is_kept(pilot, tmp_path):
    save_artifact(pilot, tmp_path, pipeline="probe", extra={"seed": 20261029})
    assert _meta(tmp_path)["seed"] == 20261029


def test_reserved_extra_key_is_rejected(pilot, tmp_path):
    with pytest.raises(ArtifactError, match="reserved"):
        save_artifact(pilot, tmp_path, pipeline="probe", extra={"sha256": "x"})


def test_tampered_tokenizer_is_rejected(pilot, tmp_path):
    save_artifact(pilot, tmp_path, pipeline="probe")
    path = tmp_path / "tokenizer.json"
    path.write_text(path.read_text(encoding="utf-8") + " ", encoding="utf-8")
    with pytest.raises(ArtifactError, match="sha256"):
        load_artifact(tmp_path)


def test_unsupported_schema_is_rejected(pilot, tmp_path):
    save_artifact(pilot, tmp_path, pipeline="probe")
    meta = _meta(tmp_path)
    meta["schema_version"] = 2
    _write_meta(tmp_path, meta)
    with pytest.raises(ArtifactError, match="schema_version"):
        load_artifact(tmp_path)


def test_tokenizers_version_mismatch_is_rejected(pilot, tmp_path):
    save_artifact(pilot, tmp_path, pipeline="probe")
    meta = _meta(tmp_path)
    meta["tokenizers_version"] = "0.0.0"
    _write_meta(tmp_path, meta)
    with pytest.raises(ArtifactError, match="tokenizers version"):
        load_artifact(tmp_path)


def test_missing_files_are_rejected(tmp_path):
    with pytest.raises(ArtifactError, match="missing"):
        load_artifact(tmp_path)


def test_committed_fixture_loads_and_round_trips():
    tokenizer, meta = load_artifact(FIXTURE)
    assert meta["vocab_size"] == tokenizer.get_vocab_size()
    for text in SAMPLES:
        assert decode(tokenizer, encode(tokenizer, text)) == text
