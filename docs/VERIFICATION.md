# Verification log

Records what has been run in a target environment, with the exact command and result.
Verification is not a design approval; see docs/decisions.md for decisions.

## 2026-10-29: environment install and lint (Codespaces)

- Environment: GitHub Codespaces, Linux x86_64, Python 3.11.18 (uv-managed venv at .venv)
- Commit: 4406860 (origin/main at time of run)
- Command: uv pip install --only-binary :all: "tokenizers==0.23.3"
  Result: installed; tokenizers.__version__ == 0.23.3
- Command: uv pip install -e ".[dev]"
  Result: installed sonlithy-tok-v1 0.1.0 (editable)
- Command: ruff check .
  Result: All checks passed!
- Command: ruff format --check .
  Result: 24 files already formatted
- Command: pytest
  Result: 2 passed (tests/unit/test_config.py, tests/unit/test_package.py)
- Not run: any test of Split, ByteLevel, BPE training, encoding or decoding.
  Status: Split behaviour on tokenizers==0.23.3 is Not tested.

## 2026-10-29: Split API probe (Codespaces, Python 3.11.18, tokenizers 0.23.3)

- Command: pre_tokenize_str on "Hello, world!" with patterns \s+ and \s+|\S+,
  invert=False and invert=True.
  Result: identical output in all four cases:
  [('Hello,', (0, 6)), (' ', (6, 7)), ('world!', (7, 13))].
- Command: pre_tokenize_str on "a😀 b" with \s+|\S+, invert=False.
  Result: [('a😀', (0, 2)), (' ', (2, 3)), ('b', (3, 4))]; slices text[start:end]
  equal the pieces. For this input, offsets are Python code-point indices.
- Documentation: Split.__doc__ says invert means "Whether to invert the pattern".
  It does not define the effect with behavior="isolated".
  Status: invert semantics Not tested. No test asserts them.
- Scope: not tested are combining marks, ZWJ/ZWNJ, multi-code-point emoji,
  and the SonLithy-Tok regex candidate (D-001, Open).

- Command: ruff format tests/unit/test_split_api.py; ruff format --check; ruff check
  Result: ruff format reported "1 file left unchanged" (no edit in this run); ruff format --check: 1 file already formatted; ruff check: All checks passed!
- Command: pytest tests/unit/test_split_api.py -v (after ruff format)
  Result: 8 passed (tokenizers 0.23.3, Python 3.11.18). Covers version pin, offsets,
  code points for BMP and one non-BMP emoji, two-space piece, documented example.
  Not covered: invert semantics, empty-input contract (D-004), regex candidate (D-001).
  CI note: tokenizers is not declared in dev dependencies, so these tests are
  skipped in GitHub Actions; this has not been run in CI.

## 2026-10-29: regex candidate compile probe and local test run (Python 3.11.18, tokenizers 0.23.3)

- Command: Split(Regex(SPLIT_REGEX_V7_CANDIDATE), behavior="isolated").pre_tokenize_str("Hello, world!")
  Result: [('Hello', (0, 5)), (',', (5, 6)), (' world', (6, 12)), ('!', (12, 13))]
  Scope: the candidate compiles and matches the handoff expectation for this one input.
  This is not a verification of the regex. Other handoff examples are Not tested.
- Command: pytest -v (local, after pyproject change)
  Result: 10 passed (2 existing tests, 8 Split probe tests).
  This is a local result. CI status is not recorded here until observed.

## 2026-10-29: byte-level round-trip tests (Python 3.11.18, tokenizers 0.23.3)

- Command: ruff check tests/unit/test_roundtrip_bytelevel.py; ruff format (1 file reformatted)
  Result: All checks passed!; 1 file already formatted.
- Command: pytest tests/unit/test_roundtrip_bytelevel.py -v (local)
  Result: 32 passed. Covers exact round trip and one token per UTF-8 byte for 16 strings,
  empty input, and distinct composed and decomposed forms of U+00E9.
  Pipeline: Split(\s+|\S+) -> ByteLevel(add_prefix_space=False, use_regex=False),
  vocabulary = 256 ByteLevel symbols, no merges.
  Not tested: BPE training, invalid input (D-010 option 1), the regex candidate
  (D-001), CI result for this commit (not yet observed).

## 2026-10-29: lone-surrogate probe and input check

- Command: Tokenizer(Split -> ByteLevel).encode("a\ud800b")
  Result: TypeError "TextInputSequence must be str". Input is rejected, not replaced.
  The message is misleading and version-dependent, so the project check_input raises
  its own ValueError before the library is called.
- Command: Tokenizer(Split -> ByteLevel).encode("a\u00e9b")
  Result: 4 ids (one per UTF-8 byte); decode returns 'aéb'.
- Command: pytest -v (local, after check_input was added)
  Result: 42 passed (local). CI not observed for this commit.

## 2026-10-29: encoding wrapper with D-010 check

- Command: pytest -v (local, after encoding.py was added)
  Result: all tests passed; includes round trip through the wrapper for 8 strings,
  one id per UTF-8 byte, rejection of a lone surrogate before the library is called,
  and the special-token spelling as ordinary text.
  Not tested: BPE training, special-token contract (D-005), regex candidate (D-001),
  CI result for this commit (not yet observed).

## 2026-10-29: tokenizers as runtime dependency; D-005 approved

- Command: uv pip install --python /tmp/rt/bin/python . ; import sonlithy_tok.encoding
  Result: runtime import ok in a clean Python 3.11 environment without dev extras.
- Command: pytest -q; ruff check .; ruff format --check .
  Result: recorded in the terminal output of this step (fill in the numbers after running).
