# Changelog

## [1.3.0] - 2026-09-30

### Added
- Three explicit stages: local generation, mandatory validation gate, and separately authorized platform upload with a per-resource completion list.
- Deterministic bundle validator with a saved Markdown report and a build-script hook.
- Local batch output under the project folder; generated teaching materials are ignored by Git.
- Official help links and stop conditions for Kahoot and Wayground upload operations.

### Changed
- A platform-ready batch must pass both deterministic file/consistency checks and question-by-question source and assessment review before upload.
- Updated Canonical schema requirements to retain verifiable source claims and adapter support status.

## [1.2.0] - 2026-09-30

### Added
- Natural Science AI Content Factory project identity.
- Factory-mode workflow for whole-book / whole-site batch production.
- “Inventory first, produce second” batch manifest workflow.
- Canonical question bank as the single source of truth.
- Kahoot × Wayground dual-platform output architecture.
- Teacher notes, QA summary, and batch index as standard deliverables.

### Changed
- Renamed the skill to `natural-science-ai-content-factory`.
- Upgraded project positioning from dual-platform assessment engine to AI content factory.
