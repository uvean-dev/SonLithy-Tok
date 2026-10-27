# Evaluation

Evaluation tooling and results do not exist yet. Future evaluations should be
repeatable and report the tokenizer configuration, corpus sources and splits, tool
versions, and measurement environment.

## Quality and coverage

Assess round-trip preservation, byte coverage, tokenization behavior on representative
text, and language coverage across the intended languages and scripts. Include
Unicode, whitespace, punctuation, code, and domain-relevant examples. A fixed
evaluation split must remain isolated from training and tuning.

## Efficiency

Compare candidate vocabulary sizes (32768, 50048, and 65536) using measured token
counts or compression ratios, model vocabulary constraints, and encoding/decoding
throughput. Include warm-up and repeated measurements and record the hardware and
software environment.

These are proposed evaluation dimensions, not completed tests or benchmark results.
No quality threshold has been selected yet.