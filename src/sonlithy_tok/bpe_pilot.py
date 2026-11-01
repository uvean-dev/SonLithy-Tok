"""Pilot BPE training on a synthetic corpus (development only).

Purpose: exercise the training path, determinism, and save/load. These values are
not the SonLithy 3.5 configuration. The vocabulary size 65,536 (D-012) is still
under comparison (D-015), and the real corpus is blocked by D-009.
"""

from tokenizers import Regex, Tokenizer, decoders, models, pre_tokenizers, trainers

from sonlithy_tok.encoding import PROBE_SPLIT

PILOT_VOCAB_SIZE = 512
PILOT_MIN_FREQUENCY = 2

_BASE_LINES = (
    "The quick brown fox jumps over the lazy dog.",
    "我们今天去公园散步，天气很好。",
    "आज मौसम अच्छा है और हम पार्क में जा रहे हैं।",
    "Сегодня хорошая погода, и мы идём в парк.",
    "def add(a, b):\n    return a + b  # 12345\n",
    '{"name": "sonlithy", "size": 220442112}',
    "Emoji test: \U0001f600 \U0001f680 done",
)


def synthetic_corpus(repetitions: int = 40) -> list[str]:
    """Return a deterministic corpus: base lines with a numeric suffix."""
    total = repetitions * len(_BASE_LINES)
    return [f"{_BASE_LINES[i % len(_BASE_LINES)]} {i}" for i in range(total)]


def _new_pipeline_tokenizer() -> Tokenizer:
    tokenizer = Tokenizer(models.BPE())
    tokenizer.pre_tokenizer = pre_tokenizers.Sequence(
        [
            pre_tokenizers.Split(Regex(PROBE_SPLIT), behavior="isolated", invert=False),
            pre_tokenizers.ByteLevel(add_prefix_space=False, use_regex=False),
        ]
    )
    tokenizer.decoder = decoders.ByteLevel()
    return tokenizer


def train_pilot_tokenizer(corpus: list[str]) -> Tokenizer:
    """Train a byte-level BPE tokenizer with the pilot settings. No special tokens."""
    tokenizer = _new_pipeline_tokenizer()
    trainer = trainers.BpeTrainer(
        vocab_size=PILOT_VOCAB_SIZE,
        min_frequency=PILOT_MIN_FREQUENCY,
        initial_alphabet=pre_tokenizers.ByteLevel.alphabet(),
        show_progress=False,
    )
    tokenizer.train_from_iterator(corpus, trainer=trainer)
    return tokenizer
