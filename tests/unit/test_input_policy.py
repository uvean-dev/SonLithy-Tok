"""Input policy from D-010: unchanged text passes, unencodable text raises."""

import pytest

from sonlithy_tok.normalization import check_input


@pytest.mark.parametrize(
    "text",
    ["", "a", "\u00e9", "e\u0301", "  spaces\t", "\r\nline\n", "\u2028", "\U0001f600"],
)
def test_valid_text_is_returned_unchanged(text):
    assert check_input(text) is text


def test_lone_surrogate_raises_value_error():
    with pytest.raises(ValueError, match="UTF-8"):
        check_input("a\ud800b")


def test_trailing_lone_surrogate_raises_value_error():
    with pytest.raises(ValueError):
        check_input("\udfff")


def test_non_string_raises_type_error():
    with pytest.raises(TypeError):
        check_input(b"bytes")  # type: ignore[arg-type]
