"""Smoke tests for functionality that currently exists."""

import sonlithy_tok


def test_package_import_exposes_development_version() -> None:
    assert sonlithy_tok.__version__ == "0.1.0"
