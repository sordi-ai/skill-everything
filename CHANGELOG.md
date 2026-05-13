# Changelog

All notable changes to **skill-everything** are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [Unreleased] — 2026-05-13

### Added — 13 new sub-skills

| Sub-skill | Directory |
|-----------|-----------|
| Test-Driven Development | `skills/tdd/` |
| Debugging | `skills/debugging/` |
| Security Review Depth | `skills/security-review/` |
| Docker / Containers | `skills/docker/` |
| Bash / POSIX Scripting | `skills/shell-scripting/` |
| Database Schema Design | `skills/db-schema/` |
| GitHub CLI (`gh`) | `skills/github-cli/` |
| Branch Finishing | `skills/branch-finishing/` |
| FastAPI | `skills/fastapi/` |
| LangChain / Agent Frameworks | `skills/langchain/` |
| Diagrams (draw.io / Mermaid) | `skills/drawio/` |
| Brainstorming | `skills/brainstorming/` |
| Implementation Plan | `skills/implementation-plan/` |

### Extended — 3 fold-ins to existing sub-skills

| Sub-skill | Topic added | New rules |
|-----------|-------------|----------:|
| Python (`skills/python/`) | Testing + Packaging | 19–23, 26–28 |
| React (`skills/react/`) | Responsive Design | 18–22 |
| Code Quality (`skills/code-quality/`) | Error Handling | 12–15 |

### Changed

- Error log — 16 new ERR entries added (ERR-2026-014 through ERR-2026-029).
- `skills/_index.yml` — 13 new entries registered.
- Loader files regenerated (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `SKILL.md`, `.cursorrules`, per-skill `.cursor/rules/*.mdc`).
- `README.md` — skill table refreshed.

### Infrastructure

- 13 new eval tasks (`tests/eval/tasks/06-*.yml` through `18-*.yml`).
- Total sub-skill count: **10 → 23**.
- Tests: **38 → 55**, all passing.

---

## [Post-0.75.0] — 2026-05-11

### Added

- `feat: v0.85 SVG sync + P2.12 eval framework MVP` (29717ba) — SVG sync and initial eval framework.
- `feat: v1.0 eval build-out — real providers + judge + calibration + compare` (21006af) — full eval pipeline with real providers, judge, calibration, and comparison tooling.
- `feat: skills/svg-check sub-skill — Playwright bbox check for SVGs` (25983e3) — new `svg-check` sub-skill using Playwright for bounding-box validation.

### Fixed

- `fix: frontpage audit fixes + Bo architecture folder-strip upgrade` (7968afd).
- `fix: trust-cleanup — voice softening + ruff format + WHAT'S INSIDE fix` (43aa6d3).
- `fix: architecture.svg meta.version chip 1.0.0 -> 0.75.0` (d82e392).
- `fix: second senior-review pass — diagram count + CODEOWNERS + magic-tone` (797b96e).
- `fix: escape <name> placeholder + remove -- in comment for GitHub SVG render` (b1dfd70).
- `fix: architecture.svg pixel-perfect review — 4-designer synthesis` (e9d90bb).
- `fix: GEMINI CLI box text overflow + pixel-perfect overflow checker` (22aef9a).
- `fix: extend viewBox 500->520 so bottom-row tagline clears folder strip` (88cf1d9).
- `fix: memory-to-go.svg — GEMINI loader + runtime box overflows` (ea8f070).

---

## [0.75.0] — 2026-05-10

> Tagged release: `v0.75.0` — Foundation (preview)

### Added

- 9 sub-skills: `code-quality`, `python`, `typescript`, `react`, `git-conventions`, `review-deployment`, `domain-template`, `error-log`, `self-extension-workflow`.
- MUST/SHOULD/AVOID rule classification across all dev sub-skills (`feat: MUST/SHOULD/AVOID rule classification in dev sub-skills`, 88b8a2b).
- Single source of truth (`skills/_index.yml`) generating 5 loaders + per-skill `.cursor/rules/*.mdc` files (`feat: error-entry evidence schema + Cursor MDC + AGENTS.md`, e418f18).
- JSON-Schema validators for rule files.
- CI gates: `lint-rules`, `auto-approve-rule-pr`, `loaders-and-table-no-drift`, per-skill token budgets.
- Adversarial test suite — 15/20 bypass attempts caught.
- Multi-runtime support: Claude Code, OpenCode, Cursor, Gemini CLI.
- Per-tool token reality docs + Anthropic-Skill folder migration (`feat: per-tool token reality docs + Anthropic-Skill folder migration`, bafcc61).
- 38 tests passing.

### Fixed

- `fix: validator scope + OpenCode compat docs` (e419dfc).
- `fix: senior-review consistency patch (P0 + small P1/P2)` (d614879).
- `fix: token-budget hard check + Gemini line + SECURITY language (Patch 3)` (1bd3277).

### Changed

- Project version set to `v0.75.0` preview (`chore: downgrade project version to v0.75.0 preview`, 4d5279c).

---

## [Pre-0.75.0 patches] — 2026-05-10

> Commits on `main` before the `v0.75.0` tag, same day.

- `feat: skill-everything v0.75 — self-learning skills for AI agents` (3d32c30) — initial framework commit establishing the project.
