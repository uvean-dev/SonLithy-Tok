"""Pilot BPE tests: determinism, merges, round trip, save/load, invalid input.

These tests check the training path on a synthetic corpus. They do not check the
SonLithy 3.5 vocabulary.
"""

import pytest
from tokenizers import Tokenizer

from sonlithy_tok.bpe_pilot import PILOT_VOCAB_SIZE, synthetic_corpus, train_pilot_tokenizer
from sonlithy_tok.encoding import decode, encode

CASES = [
    "",
    "a",
    "\u00e9",
    "e\u0301",
    "Hello,   world!",
    "\u0928\u092e\u0938\u094d\u0924\u0947 \u0926\u0941\u0928\u093f\u092f\u093e",
    "\u0915\u094d\u200d\u0937\u093f \u092e\u0947\u0902",
    "\u4f60\u597d\u4e16\u754c\uff0c\u4e16\u754c\uff01",
    "Hello\r\nworld\n",
    "line\u2028separator",
    "tab\there",
    "trailing   ",
    "   leading",
    "\U0001f600 emoji",
    "def f(x):\n    return {'a': x + 12345}\n",
]


@pytest.fixture(scope="module")
def pilot():
    return train_pilot_tokenizer(synthetic_corpus())


def test_training_is_deterministic():
    first = train_pilot_tokenizer(synthetic_corpus()).to_str()
    second = train_pilot_tokenizer(synthetic_corpus()).to_str()
    assert first == second


def test_vocabulary_is_within_bounds_and_has_merges(pilot):
    assert 256 < pilot.get_vocab_size() <= PILOT_VOCAB_SIZE
    assert max(len(token) for token in pilot.get_vocab()) > 1


@pytest.mark.parametrize("text", CASES)
def test_round_trip_after_training(pilot, text):
    assert decode(pilot, encode(pilot, text)) == text


def test_merges_compress_repeated_english(pilot):
    text = "the quick brown fox jumps over the lazy dog " * 5
    assert len(encode(pilot, text)) < len(text.encode("utf-8"))


def test_save_and_load_gives_same_encoding(pilot, tmp_path):
    path = tmp_path / "pilot.json"
    pilot.save(str(path))
    loaded = Tokenizer.from_file(str(path))
    for text in CASES:
        assert encode(loaded, text) == encode(pilot, text)


def test_invalid_input_is_rejected_after_training(pilot):
    with pytest.raises(ValueError):
        encode(pilot, "a\ud800b")
