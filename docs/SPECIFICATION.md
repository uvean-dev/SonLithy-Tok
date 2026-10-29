# Tokenizer Specification

## Purpose

SonLithy-Tok is the byte-level BPE tokenizer for the SonLithy 3.5 language model.
This repository stage establishes structure and records design intent; it does not
implement or train a tokenizer.

## Current draft configuration

- The intended algorithm family is byte-level BPE. This is the chosen algorithm.
- The proposed component order is `Split -> ByteLevel(use_regex=false) -> BPE`.
  Runtime tests: Not tested.
- `add_prefix_space` is currently set to `false`.
- The byte-level alphabet must come from `ByteLevel.alphabet()`.
- Unicode handling remains conservative until experiments justify transformations.
  The normalization policy is not yet defined (see Open questions).
- Up to 128 special and service IDs may be reserved within, not beyond, the total
  vocabulary size. The limit is a constraint; the list of IDs is open.
- Candidate vocabulary sizes are 32,768, 50,048, and 65,536. They are candidates for
  comparison, not a selected size.

These are draft configuration values from [tokenizer.yaml](../configs/tokenizer.yaml).
They are not Approved decisions or validated behavior. The YAML marks the overall
configuration as `draft`; its internal status labels do not by themselves establish
approval.

The repository contains no complete regex v7 and no compatibility test with Hugging
Face Tokenizers. The `tokenizers` package is not declared as a project dependency.
Compatibility with version 0.23.3 is Not tested.

The regex candidate and its description are in [TOKENIZATION.md](TOKENIZATION.md).
Its status is Not tested.

## Values not yet verified against the canonical configuration

The following values are not yet verified against the repository's canonical
configuration. See D-011 in [decisions.md](decisions.md). They are recorded as
unverified project targets, not as approved requirements:

- Corpus proportions 70% / 18% / 4.5% / 7.5%, and per-language weights for seven
  languages.
- The 6-billion-token-position budget. It applies to main model training, not to the
  tokenizer corpus (see D-009).
- `tokenizers==0.23.3` as the target version.

## Open questions

- What exact `Split` grammar and regex-engine compatibility should be used?
- Where should the regex v7 be stored once an executable module exists? (See D-001.)
- How should the regex handle strict script separation, combining marks, ZWJ, ZWNJ,
  and adjacent mixed-script text? The developer selected strict separation (D-003);
  boundary cases remain open.
- What exactly does the "conservative" Unicode policy mean, and how does it affect
  round-trip reversibility?
- What values should be used for `min_frequency`, alphabet restrictions, and stopping
  criteria?
- Which vocabulary size best balances quality, efficiency, and model constraints?
- Which special tokens and service IDs are needed, and how should they be assigned?
- How should literal special-token spellings be distinguished from reserved control
  IDs and trusted explicit insertion?
- What is the expected `Split` result for empty input?
- What is the definition, observation unit, and aggregation method for tokenization
  parity metrics, including P90? Is the `tokens per word` denominator
  `whitespace_units`?
- What is the tokenizer corpus budget and sampling policy? (See D-009.)
- What artifact schema and compatibility guarantees should serialization provide?

No training, benchmark, regex-compatibility, or tokenizer-correctness result is
claimed at this stage. Decision statuses and evidence are tracked in
[decisions.md](decisions.md).
