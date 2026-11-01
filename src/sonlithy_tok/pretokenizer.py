"""Future text pre-tokenization responsibilities.

This module will define boundaries passed to the byte-level BPE stages. The exact
Split grammar and its tokenizer-engine compatibility are unresolved; no splitting
implementation is provided.
"""

# CANDIDATE, NOT VERIFIED. Copied from the earlier project handoff without edits.
# Not tested on tokenizers==0.23.3. See D-001 and docs/TOKENIZATION.md.
SPLIT_REGEX_V7_CANDIDATE = (
    r"(?:"
    # Han: up to eight Han characters per fragment.
    r" ?(?:\p{Han}\p{M}*){1,8}"
    # Devanagari: letters, marks, and ZWJ/ZWNJ-linked sequences.
    r"| ?(?:(?=\p{Devanagari})\p{L}\p{M}*"
    r"(?:[\x{200C}\x{200D}]\p{M}*\p{L}\p{M}*)*)+"
    # Latin-script letter sequences.
    r"| ?(?:(?=\p{Latin})\p{L}\p{M}*)+"
    # Cyrillic-script letter sequences.
    r"| ?(?:(?=\p{Cyrillic})\p{L}\p{M}*)+"
    # Numeric groups of one to three numeric characters.
    r"| ?\p{N}{1,3}"
    # Punctuation/symbol groups of up to eight characters.
    r"| ?[\p{P}\p{S}]{1,8}"
    # Keep CRLF as one newline sequence; also cover other line separators.
    r"|\r\n"
    r"|[\r\n\x{2028}\x{2029}]"
    # Trailing runs of spaces/tabs (including at end of input).
    r"|[ \t]+(?!\S)"
    r"|[ \t]+"
    # General Unicode-letter fallback, with optional joiner-linked sequences.
    r"| ?(?:\p{L}\p{M}*"
    r"(?:[\x{200C}\x{200D}]\p{M}*\p{L}\p{M}*)*)+"
    # Fallback for any remaining character.
    r"|[\s\S]"
    r")"
)
