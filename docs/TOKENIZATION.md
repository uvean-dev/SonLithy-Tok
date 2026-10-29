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

## Regex v7 candidate (D-001)

This file is the working location for the regex v7 candidate, the expected split
outputs, and the intended behavior. D-001 remains Open. This placement is not an
approved normative decision.

**Status: Not tested.** The full regex text is not yet recorded in this repository.
Its source must be confirmed before it is added. Verification statuses use these
labels:

- Not tested: no run against the target engine.
- Preflight passed: run in a different runtime; name the runtime and version.
- Runtime tests passed: run against the pinned `tokenizers` version; record the
  command and output.

No compatibility with `tokenizers==0.23.3` is claimed.

Expected split examples are not listed in this document yet. When added, each input
must be written as an explicit Python literal in test code, with spaces escaped where
the count matters (for example `"Hello\x20\x20world"` for two spaces), and checked with
`repr`. Markdown tables are not used as the source of test inputs.
