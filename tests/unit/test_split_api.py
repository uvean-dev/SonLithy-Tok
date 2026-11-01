"""Probe of the tokenizers Split API on the pinned version (0.23.3).

These tests use a deliberately simple regex. They check how the library
behaves. They do not test the SonLithy-Tok regex candidate, which is not yet
decided (see D-001 in docs/decisions.md). The semantics of invert=True are
not tested here and remain Not tested.
"""

import pytest

SIMPLE = r"\s+|\S+"


def _split(text):
    pytest.importorskip("tokenizers")
    from tokenizers import Regex
    from tokenizers.pre_tokenizers import Split

    splitter = Split(Regex(SIMPLE), behavior="isolated", invert=False)
    return splitter.pre_tokenize_str(text)


def test_tokenizers_version_is_pinned():
    tokenizers = pytest.importorskip("tokenizers")
    assert tokenizers.__version__ == "0.23.3"


def test_split_pieces_join_back_to_input():
    text = "Hello, world!"
    pieces = [piece for piece, _ in _split(text)]
    assert pieces == ["Hello,", " ", "world!"]
    assert "".join(pieces) == text


def test_split_offsets_are_contiguous_and_cover_input():
    text = "Hello, world!"
    cursor = 0
    for _, (start, end) in _split(text):
        assert start == cursor
        assert end > start
        cursor = end
    assert cursor == len(text)


def test_split_offsets_index_characters_for_non_ascii():
    text = "привет мир"
    for piece, (start, end) in _split(text):
        assert text[start:end] == piece


def test_split_offsets_index_code_points_for_emoji():
    text = "a\U0001f600 b"
    for piece, (start, end) in _split(text):
        assert text[start:end] == piece


def test_split_two_spaces_form_one_piece():
    text = "a\x20\x20b"
    pieces = [piece for piece, _ in _split(text)]
    assert pieces == ["a", "\x20\x20", "b"]


def test_split_empty_input_returns_list():
    # D-004 is not decided: this only checks that the call returns a list.
    assert isinstance(_split(""), list)


def test_split_matches_documented_example():
    # Example from the Split docstring (tokenizers 0.23.3, behavior="isolated").
    # The invert flag is not used here; its effect remains Not tested.
    from tokenizers import Regex
    from tokenizers.pre_tokenizers import Split

    pytest.importorskip("tokenizers")
    splitter = Split(Regex(r"\s+"), behavior="isolated")
    assert splitter.pre_tokenize_str("hello   world") == [
        ("hello", (0, 5)),
        ("   ", (5, 8)),
        ("world", (8, 13)),
    ]
