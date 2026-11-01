# Decision Register

## Statuses

- **Approved**: The developer has made a final decision and it is recorded here.
- **Chosen by developer, awaiting recording**: The developer selected an option, but
  recording is not complete.
- **Open**: A decision is required.
- **Not recorded**: A necessary rule is absent or insufficiently defined in the
  documentation checked for this register.
- **Proposed, awaiting developer confirmation**: An option has been proposed but
  the developer has not approved it.

Values appearing in configuration, tests, or other documentation are not Approved
solely because they appear there. Repository findings below refer to files inspected
for this register. Details explicitly attributed to the task context were not
independently verified against source material when that material was not present.

## D-001. Canonical regex v7 storage location

**Status: Approved (developer selected option B)**

Approval covers only the storage location. `SPLIT_REGEX_V7_CANDIDATE` in
`src/sonlithy_tok/pretokenizer.py` is copied without edits from the earlier project
handoff. Its source document is not verified, and its correctness is not verified.
Tests import the constant from the module; documentation links to it instead of
keeping a second copy. The text changes only after a test shows a defect or the
original source is found.

**Verification:** compiles on tokenizers 0.23.3 and matches the expected split for one
input ("Hello, world!"). Other expectations are Not tested.

## D-002. Specification synchronization

**Status: Not recorded**

The checked-in specification does not document all items named in the task registry.
The repository does not confirm the following details:

- Corpus category proportions of 70%, 18%, 4.5%, and 7.5%.
- The seven-language corpus composition or the weight assigned to each language.
- A training budget of 6 billion processed token positions.
- A target dependency version of `tokenizers==0.23.3`.
- A canonical regex/harness relationship or a policy for scripts in the regex.

The task context lists those figures as v7 material, but the corresponding v7 source
was not found in the repository. Treat them as unverified task-context information,
not repository-confirmed proposals or approved requirements. The seven language names
and their individual weights are not specified in the task context either.

The candidate vocabulary sizes 32,768, 50,048, and 65,536 do appear in
`configs/tokenizer.yaml` and `docs/EVALUATION.md`; both present them as candidates,
not a selected size or measured outcome. The `pyproject.toml` does not declare
`tokenizers` as a dependency or pin version 0.23.3. The current specification's
existing algorithm and pipeline intent remains a draft, not a validated result.

## D-003. Strict script separation in regex

**Status: Chosen by developer, awaiting recording**

The task context states that the developer selected option B: strict separation of
scripts in the regex. A letter group for one script must not silently consume letters
from another script. This is the selected direction, not an Approved final regex
rule.

Separate decisions are still needed for combining marks, ZWJ, ZWNJ, and strings that
mix scripts without spaces. This repository contains no v7 regex from which to infer
those boundary rules.

## D-004. Split behavior on empty input

**Status: Approved (developer selected option A: empty list)**

Contract: empty input produces an empty list of pieces. Offsets are only defined for
non-empty pieces, so no piece is emitted for an empty string.

Probe on tokenizers 0.23.3 (probe regex, not the candidate):
`Split(Regex(r'\s+|\S+'), behavior='isolated').pre_tokenize_str('') == []`.
Test: `test_split_empty_input_returns_empty_list`.

**Verification:** tested once locally on the probe regex. The contract must be
re-tested on the regex actually used by the pipeline once it is verified (see D-001).

## D-005. Special-token safety

**Status: Approved (principle); reserved-ID allocation Open**

Approved:
- Ordinary text that contains a special-token spelling (for example `<|im_start|>`) is
  encoded as ordinary bytes. It never becomes a control token.
- The encoding wrapper (`src/sonlithy_tok/encoding.py`) calls the library with
  `add_special_tokens=False` and registers no special tokens.
- Control IDs are inserted only by trusted code (a future serializer), never from
  user text.

Open:
- The list of reserved special and service IDs (at most 128, inside the 65,536
  vocabulary; D-012).
- The API of the trusted serializer.

**Verification:** tested on the byte-level pipeline only. `test_special_token_spelling_is_ordinary_text`
checks that the spelling round-trips as ordinary bytes. Trusted insertion is Not tested.

## D-006. TPW terminology

**Status: Not recorded**

The task context reports that v7 calls the metric `tokens per word`, while its
denominator is `whitespace_units`: the number of non-empty parts returned by
`text.split()`. That formula is not present in the repository files checked here,
so the reported definition could not be independently verified. The proposed metric
name is **tokens per whitespace unit**. Do not change the formula or adopt the new
name until the source definition is available and the terminology is confirmed.

## D-007. 90th-percentile aggregation

**Status: Not recorded**

The checked-in documentation does not define a tokenization-parity metric or a
90th-percentile calculation. The task context identifies unresolved questions:
whether P90 is calculated per language or over a pooled sample, how results are
aggregated, and what constitutes one observation. No aggregation method is selected.

## D-008. Unidentified local file `0000000`

**Status: Resolved**

The file was a local, untracked saved output of `git log --stat` for commit
3e99d58 (project skeleton). It contained no secrets or personal data, and its
content is reproducible from Git history. The file was removed from the working
copy. No tracked project file was affected.

## D-009. Tokenizer corpus budget and sampling

**Status: Open**

Not yet decided:

- Total corpus volume used for tokenizer training.
- Sampling unit, sampling rules, and random seed.
- Per-language and per-category minimums.
- Deduplication and near-duplicate rules.
- Exclusion rules for FLORES-200 `devtest` from tokenizer training.

The 6-billion-token-position budget in the unverified-values list (D-011) belongs to
main model training. It must not be used as the tokenizer corpus budget.

## D-010. Unicode normalization and invalid input

**Status: Approved (option A: no normalization; option 1: explicit error for invalid input)**

Contract: `decode(encode(s)) == s` for every Python `str` that can be encoded as UTF-8.
The tokenizer applies no Unicode normalization (NFC, NFKC, NFD, NFKD), no whitespace
trimming, no line-ending conversion, and no space collapsing.

Inputs that cannot be encoded as UTF-8, such as strings containing unpaired surrogates
(for example "\ud800"), are rejected with an explicit error. They are never replaced
with U+FFFD or any other character.

Normalization, if it is ever needed, belongs to corpus preparation (D-009) and must be
recorded in the corpus manifest.

The YAML field `unicode_normalization: conservative` is not changed by this record.

**Verification:** Not tested. Round-trip and invalid-input tests are not yet written.

## D-011. Unverified project values

**Status: Open** (labelling rule proposed; not yet approved)

Values not verified against the repository's canonical configuration are recorded in
documentation as unverified targets, not as approved requirements. Current entries:

- Corpus proportions 70% / 18% / 4.5% / 7.5%. Unit of measure (cleaned UTF-8 bytes
  before tokenization) and source still need to be confirmed.
- Per-language weights for the seven languages. Source and basis not confirmed.
- 6-billion-token-position budget. Applies to main model training, not to the
  tokenizer corpus (see D-009).
- `tokenizers==0.23.3` as the target version. Not verified by a runtime run.

Origin: earlier project discussion, recorded in the handoff document. This is not
independent technical evidence. Each entry needs a source and a status before it can
become a requirement.

## D-012. Vocabulary size for SonLithy-Base-v1 (SonLithy 3.5)

**Status: Working target; final choice pending comparison (see D-015)**

The current target configuration uses a total vocabulary of 65,536 tokens. This value
includes the byte-level alphabet and the reserved special and service IDs.

This is a working target, not a proven optimum. The candidates 32,768 and 50,048 remain
experimental alternatives. The final choice will follow the comparison in D-015.

**Verification:** Not tested. No tokenizer has been trained or evaluated.

## D-013. SonLithy-Base-v1 model configuration

**Status: Approved by developer (confirmed in chat); implementation not tested**

- Architecture name: SonLithy-Base-v1 (model SonLithy 3.5).
- 24 Transformer layers, d_model 768, 12 attention heads, head_dim 64, d_ff 3072.
- Context length 2048 tokens.
- Parameter count 220,442,112 for vocabulary 65,536, with weight tying and without a
  learned positional-embedding table.

Parameter arithmetic was checked by hand: embeddings 50,331,648 + 24 layers
(7,087,872 each) + final LayerNorm 1,536.

Developer confirmation was given in conversation. This is not evidence that the
implementation matches the specification.

**Verification:** Not tested. Model code does not yet exist.

## D-014. Weight tying and positional encoding

**Status: Approved by developer (confirmed in chat)**

- Weight tying: enabled. The output projection shares weights with the input embedding.
- Positional encoding: RoPE, with no learned positional-embedding table.

These choices are the basis of the parameter count in D-013. Confirmation was given in
conversation; no test result is implied.

**Verification:** Not tested.

## D-015. Vocabulary comparison design

**Status: Chosen by developer, awaiting recording of open items**

Main experiment:

- One architecture (as in D-013) for all candidates.
- Three vocabularies: 32,768, 50,048, 65,536.
- Same fixed corpus and document order for all candidates.
- Same budget of original UTF-8 bytes.
- Tokens, FLOPs and quality are measured outcomes; the corpus is not rebuilt per candidate.
- Total parameter counts differ by candidate because of the embedding matrix:
  195,276,288 / 208,547,328 / 220,442,112.

Control experiment: compare candidates at an equal FLOPs budget.

Open items before running:

- Tokenizer-training corpus size, sampling and seed (see D-009).
- Training budget for the proxy experiments (the 6-billion-token figure is unverified;
  see D-011).
- Success criteria and statistical rules.
- Metric definitions, including the status of the earlier tokens-per-word and P90 proposals.

Interpretation note: differences between candidates combine tokenizer effects and the
effect of embedding and output-layer size. The report must state this.

**Verification:** Not tested. No experiment has been run.

## D-016. License

**Status: Chosen by developer (confirmed in chat)**

The project is licensed under the Apache License, Version 2.0, as stated in the
LICENSE file. This is a project licence decision only. Licences of corpus data
sources remain an open question (see D-009 and D-011).

**Verification:** Not applicable (licence choice, not implementation).

## D-017. tokenizers as a runtime dependency

**Status: Approved (developer confirmed in chat)**

`tokenizers==0.23.3` is a runtime dependency of the package, because `encoding.py` imports
it. It is no longer only a development extra. Verified: install without extras and import
of `sonlithy_tok.encoding` on Python 3.11 (see docs/VERIFICATION.md).

**Verification:** installed and imported in a clean environment; CI result not yet observed.
