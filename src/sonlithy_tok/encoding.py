"""Thin wrapper over the tokenizers pipeline with the D-010 input check.

Pipeline: Split(\\s+|\\S+) -> ByteLevel(no merges). The split pattern is a probe
pattern, not the regex candidate (D-001). There are no BPE merges yet.

Special tokens are not handled here. add_special_tokens is always False, and the
special-token contract remains open (D-005).
"""

from tokenizers import Regex, Tokenizer, decoders, models, pre_tokenizers

from sonlithy_tok.normalization import check_input

PROBE_SPLIT = r"\s+|\S+"


def build_byte_level_tokenizer() -> Tokenizer:
    """Return a tokenizer whose vocabulary is the 256 ByteLevel symbols."""
    alphabet = sorted(set(pre_tokenizers.ByteLevel.alphabet()))
    vocab = {symbol: index for index, symbol in enumerate(alphabet)}
    tokenizer = Tokenizer(models.BPE(vocab=vocab, merges=[]))
    tokenizer.pre_tokenizer = pre_tokenizers.Sequence(
        [
            pre_tokenizers.Split(Regex(PROBE_SPLIT), behavior="isolated", invert=False),
            pre_tokenizers.ByteLevel(add_prefix_space=False, use_regex=False),
        ]
    )
    tokenizer.decoder = decoders.ByteLevel()
    return tokenizer


def encode(tokenizer: Tokenizer, text: str) -> list[int]:
    """Encode text after the D-010 check; invalid input never reaches the library."""
    checked = check_input(text)
    return tokenizer.encode(checked, add_special_tokens=False).ids


def decode(tokenizer: Tokenizer, ids: list[int]) -> str:
    """Decode token IDs produced by encode."""
    return tokenizer.decode(ids)
