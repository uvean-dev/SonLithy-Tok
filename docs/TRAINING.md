# Training

The trainer is not implemented. This document outlines requirements for a future
training workflow without selecting unresolved training parameters.

## Corpus preparation

- Record each source, version or snapshot, license, provenance, and permitted use.
- Review whether each source may be processed and redistributed; public availability
  alone is not permission for every use.
- Audit duplicates and near-duplicates before splitting data.
- Keep evaluation data isolated from training data and prevent source-level leakage
  where applicable.
- Do not commit corpora, downloaded archives, or derived large datasets.

## Training process

A future run should capture its complete configuration, tool and library versions,
input source manifest, preprocessing choices, random seeds where applicable, and
output artifact checksums. Vocabulary size candidates are recorded in the draft
configuration, but no candidate is selected by measurement.

`min_frequency`, alphabet restrictions, and stopping criteria remain `TBD`. Do not
start training with undocumented defaults or present a run as reproducible without
its inputs and configuration.

## Artifacts

The artifact format, schema version, compatibility checks, and special-token ID
allocation are open design items. Store generated artifacts outside Git unless a
separate review explicitly approves a small distributable artifact.