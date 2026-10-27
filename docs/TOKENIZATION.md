# Tokenization

## Intended data path

The current proposal is to pass input through `Split`, then `ByteLevel` with
`use_regex=false`, and finally BPE. The exact `Split` grammar is intentionally
unselected. Its behavior and compatibility with the chosen tokenizer engine must be
tested before it is treated as a specification.

`ByteLevel.alphabet()` is the source of the byte-level alphabet. `add_prefix_space` is
currently `false`. Neither this document nor the draft configuration claims that an
implementation exists.

## Text preservation and safe input

Normalization should preserve input distinctions unless documented experiments
justify changing them. The implementation must define how Unicode is handled and
test that decoding reconstructs the intended original text, including whitespace,
combining characters, and malformed or unusual input where supported.

User-provided text that literally contains the spelling of a special token must not
silently become a control token. A future safe-encoding API must distinguish ordinary
text from explicitly authorized special-token input. The behavior and API are not yet
implemented.

## Status

All tokenization stages described here are design intent. No final split pattern,
engine compatibility, or round-trip behavior has been verified.