# Tokenizer Specification

## Purpose

The SonLithy 3.5 Tokenizer is intended to be a byte-level BPE tokenizer for the
SonLithy 3.5 language model. This repository stage establishes structure and records
design intent; it does not implement or train a tokenizer.

## Current draft configuration

- The intended algorithm family is byte-level BPE.
- The proposed component order is `Split -> ByteLevel(use_regex=false) -> BPE`.
- `add_prefix_space` is currently set to `false`.
- The byte-level alphabet must come from `ByteLevel.alphabet()`.
- Unicode handling remains conservative until experiments justify transformations.
- Up to 128 special and service IDs may be reserved within, not beyond, the total
  vocabulary size.

These are draft configuration values from [tokenizer.yaml](../configs/tokenizer.yaml),
not Approved decisions or validated behavior. The YAML marks the overall configuration
as `draft`; its internal status labels do not by themselves establish approval. The
component order and vocabulary size remain candidates, not validated outcomes.

The repository contains no complete regex v7, regex compatibility test, or separate
test harness. No compatibility with Hugging Face Tokenizers is claimed. The
`tokenizers` package is not declared as a project dependency, so compatibility with
version `0.23.3` has not been tested.

## Additional v7 items not verified in repository sources

The task context reports corpus proportions of 70%, 18%, 4.5%, and 7.5%; a
seven-language composition and per-language weights; a budget of 6 billion processed
token positions; `tokenizers==0.23.3`; and policy questions for regex/script handling.
Those details were not found in the checked-in project materials, and their v7 source
was not available for verification. The language names and individual weights are
also not specified in the task context. Treat these items as unverified, not as
repository-confirmed proposals or final requirements. See [decisions.md](decisions.md)
for their decision status and the evidence checked.

The candidate vocabulary sizes 32,768, 50,048, and 65,536 are present in the draft
configuration and evaluation document. They are hypotheses for comparison, not a
selected size or measured results.

## Open questions

- What exact `Split` grammar and regex-engine compatibility should be used?
- Where will the full regex v7 be canonically stored, and how will it be tested?
- How should the regex handle strict script separation, combining marks, ZWJ, ZWNJ,
  and adjacent mixed-script text?
- What values should be used for `min_frequency`, alphabet restrictions, and stopping
  criteria?
- Which vocabulary size best balances quality, efficiency, and model constraints?
- Which special tokens and service IDs are needed, and how should they be assigned?
- How should literal special-token spellings be distinguished from reserved control
  IDs and trusted explicit insertion?
- What is the expected `Split` result for empty input?
- What are the definition, observation unit, and aggregation method for tokenization
  parity metrics, including P90? Is the reported `tokens per word` denominator
  `whitespace_units`?
- What artifact schema and compatibility guarantees should serialization provide?

The task context reports that strict script separation (option B) was selected by the
developer; its boundary cases and final regex rules remain unresolved. No training,
benchmark, regex-compatibility, or tokenizer-correctness result is claimed at this
stage. Decision statuses and evidence are tracked in [decisions.md](decisions.md).
