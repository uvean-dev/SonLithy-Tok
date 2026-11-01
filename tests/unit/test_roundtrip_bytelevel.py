"""Round-trip tests for the library pipeline Split -> ByteLevel, without merges.

The vocabulary is the 256-symbol ByteLevel alphabet with no BPE merge rules, so
each UTF-8 byte is exactly one token. These tests check the byte-level layer and
decoding. They do not test BPE training, which does not exist yet.
"""

import pytest

pytest.importorskip("tokenizers")

SIMPLE_SPLIT = r"\s+|\S+"

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


def build_byte_tokenizer(split_pattern=SIMPLE_SPLIT):
    from tokenizers import Regex, Tokenizer, decoders, models, pre_tokenizers

    alphabet = sorted(set(pre_tokenizers.ByteLevel.alphabet()))
    vocab = {symbol: index for index, symbol in enumerate(alphabet)}
    tokenizer = Tokenizer(models.BPE(vocab=vocab, merges=[]))
    tokenizer.pre_tokenizer = pre_tokenizers.Sequence(
        [
            pre_tokenizers.Split(Regex(split_pattern), behavior="isolated", invert=False),
            pre_tokenizers.ByteLevel(add_prefix_space=False, use_regex=False),
        ]
    )
    tokenizer.decoder = decoders.ByteLevel()
    return tokenizer


@pytest.mark.parametrize("text", CASES)
def test_round_trip_is_exact(text):
    tokenizer = build_byte_tokenizer()
    ids = tokenizer.encode(text, add_special_tokens=False).ids
    assert tokenizer.decode(ids) == text


@pytest.mark.parametrize("text", CASES)
def test_one_token_per_utf8_byte(text):
    tokenizer = build_byte_tokenizer()
    ids = tokenizer.encode(text, add_special_tokens=False).ids
    assert len(ids) == len(text.encode("utf-8"))


def test_empty_string_gives_no_ids():
    tokenizer = build_byte_tokenizer()
    assert tokenizer.encode("", add_special_tokens=False).ids == []


def test_composed_and_decomposed_forms_are_distinct():
    # Unicode normalization is not applied (D-010, option A). The two forms
    # must stay distinct and each must round-trip unchanged.
    tokenizer = build_byte_tokenizer()
    composed = tokenizer.encode("\u00e9", add_special_tokens=False).ids
    decomposed = tokenizer.encode("e\u0301", add_special_tokens=False).ids
    assert composed != decomposed
    assert tokenizer.decode(composed) == "\u00e9"
    assert tokenizer.decode(decomposed) == "e\u0301"
