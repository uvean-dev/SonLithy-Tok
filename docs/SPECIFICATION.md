# Tokenizer Specification

## Purpose

The SonLithy 3.5 Tokenizer is intended to be a byte-level BPE tokenizer for the
SonLithy 3.5 language model. This repository stage establishes structure and records
design intent; it does not implement or train a tokenizer.

## Current decisions

- The intended algorithm family is byte-level BPE.
- The proposed component order is `Split -> ByteLevel(use_regex=False) -> BPE`.
- `add_prefix_space` is currently set to `false`.
- The byte-level alphabet must come from `ByteLevel.alphabet()`.
- Unicode handling remains conservative until experiments justify transformations.
- Up to 128 special and service IDs may be reserved within, not beyond, the total
  vocabulary size.

These decisions and their status are recorded in [tokenizer.yaml](../configs/tokenizer.yaml).
The component order and vocabulary size remain candidates, not validated outcomes.

## Open questions

- What exact `Split` grammar and regex-engine compatibility should be used?
- What values should be used for `min_frequency`, alphabet restrictions, and stopping
  criteria?
- Which vocabulary size best balances quality, efficiency, and model constraints?
- Which special tokens and service IDs are needed, and how should they be assigned?
- What artifact schema and compatibility guarantees should serialization provide?

No training, benchmark, or tokenizer correctness result is claimed at this stage.