"""Future text and Unicode normalization responsibilities.

Normalization should remain conservative until experiments justify any additional
transformations. No normalization implementation or policy beyond that constraint is
currently provided.
"""


def check_input(text: str) -> str:
    """Return ``text`` unchanged if it can be encoded as UTF-8.

    Implements D-010 (option 1): inputs that cannot be encoded as UTF-8, such as
    strings with unpaired surrogates, raise an explicit error. Nothing is replaced
    and no normalization is applied.
    """
    if not isinstance(text, str):
        raise TypeError(f"expected str, got {type(text).__name__}")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError(
            "input cannot be encoded as UTF-8 (unpaired surrogate or similar)"
        ) from exc
    return text
