"""Tests for the encoding wrapper: round trip, D-010 check, special-token spelling."""

import pytest

pytest.importorskip("tokenizers")

from sonlithy_tok.encoding import build_byte_level_tokenizer, decode, encode


class _ForbiddenTokenizer:
    def encode(self, *args, **kwargs):
        raise AssertionError("library must not be called for invalid input")


@pytest.mark.parametrize(
    "text",
    ["", "a", "\u00e9", "e\u0301", "\u4f60\u597d", "\U0001f600", "\r\n", "  pad  "],
)
def test_round_trip_through_wrapper(text):
    tokenizer = build_byte_level_tokenizer()
    assert decode(tokenizer, encode(tokenizer, text)) == text


def test_one_id_per_utf8_byte_through_wrapper():
    tokenizer = build_byte_level_tokenizer()
    assert len(encode(tokenizer, "\u00e9")) == 2


def test_invalid_input_is_rejected_before_library_is_called():
    with pytest.raises(ValueError):
        encode(_ForbiddenTokenizer(), "a\ud800b")


def test_special_token_spelling_is_ordinary_text():
    # No special tokens are registered, so the spelling is plain bytes.
    # The full special-token contract remains open (D-005).
    tokenizer = build_byte_level_tokenizer()
    text = "<|im_start|>"
    ids = encode(tokenizer, text)
    assert decode(tokenizer, ids) == text
    assert len(ids) == len(text.encode("utf-8"))
