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

## D-001. Canonical regex v7

**Status: Open**

The repository does not contain the full `SPLIT_REGEX_V7`, a regex v7 section, or a
test harness for it. No duplicate copies were found. There is therefore no basis for
choosing a canonical storage location or comparing versions. Do not reconstruct or
edit the regex until the source and ownership are established.

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

**Status: Not recorded**

No empty-input Split test was found. The documentation does not specify the expected
result for an empty string. No contract is inferred.

## D-005. Special-token safety

**Status: Open**

`docs/TOKENIZATION.md` states the design requirement that literal user text matching
a special-token spelling must not silently become a control token, and that an API
should distinguish ordinary text from explicitly authorized special-token input.
The distinction and mechanics are not implemented or specified sufficiently to be a
contract. Decide and verify separately:

- Literal text whose characters match a special-token spelling.
- A genuine reserved control ID.
- Explicit insertion of a control token by a trusted serializer.

Required future tests should cover alternative spellings, adjacent characters,
repetitions, and occurrences inside ordinary text. No mechanism is implemented by
this register.

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

## D-008. Unidentified file `0000000`

**Status: Open**

`git status --short` showed `?? 0000000` during this review. Its contents were not
opened or inspected, and it is not treated as a project artifact. Do not modify,
rename, delete, or further inspect it without the developer's permission.
