# Changelog

## [1.4.0] - 2026-10-01

### Added
- Traceable Markdown build reports with curriculum-code mapping, per-question sources, verification/revision status, storage paths, file hashes, and upload state.
- A deterministic report generator and guidance to keep generated teaching materials under the Git-ignored outputs/ directory.
- Wordwall manual activity-design plans generated from the same Canonical question bank and source/QA gate as Kahoot and Wayground.
- Wordwall activity suggestions for matching, group sorting, quizzes, random wheels, and other learning-goal-aligned formats, with item/answer keys, Canonical IDs, sources, and teacher setup steps.
- Separate Kahoot, Wayground, and Wordwall output folders, plus a deterministic Wordwall plan builder and validator coverage.

## [1.3.1] - 2026-09-30

### Added
- Camera-ready Traditional Chinese video script documenting the skill's real design, validation, testing, and release process.

## [1.3.0] - 2026-09-30

### Added
- Three explicit stages: local generation, mandatory validation gate, and separately authorized platform upload with a per-resource completion list.
- Deterministic bundle validator with a saved Markdown report and a build-script hook.
- Local batch output under the project folder; generated teaching materials are ignored by Git.
- Official help links and stop conditions for Kahoot and Wayground upload operations.

### Changed
- A platform-ready batch must pass both deterministic file/consistency checks and question-by-question source and assessment review before upload.
- Updated Canonical schema requirements to retain verifiable source claims and adapter support status.
- Wordwall remains a manual design deliverable unless current official feature and import specifications are verified; no direct-import or publication claim is made.
- All three platform outputs retain the same Canonical IDs, answers, learning objectives, and per-question evidence.

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
