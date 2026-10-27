"""Validation of the checked-in draft tokenizer configuration."""

from pathlib import Path

import yaml

CONFIG_PATH = Path(__file__).parents[2] / "configs" / "tokenizer.yaml"


def test_draft_tokenizer_configuration_records_constraints() -> None:
    with CONFIG_PATH.open(encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file)

    assert config["status"] == "draft"
    assert config["decisions"]["algorithm"]["value"] == "byte-level BPE"
    assert config["decisions"]["reserved_ids"]["maximum"] == 128
    assert config["decisions"]["reserved_ids"]["included_in_vocabulary_size"] is True
    assert config["hypotheses"]["vocabulary_size_candidates"] == [32768, 50048, 65536]
    assert config["open_questions"]["min_frequency"] == "TBD"
