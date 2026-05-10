# Roadmap

> **`v0.75` is the current preview release.** Foundation work is done; `v1.0` ships only when the eval framework earns the claim. New features land in `main` via PR — every change is a commit, every commit is reviewed, every release is auditable.

## Versions

| Version | Status | What |
|---|:---:|---|
| **`v0.75` — Foundation** | 🟡 **PREVIEW** | `lint-rules` CI · JSON-Schema validator · XSS hardening · single-source-of-truth loader sync · `learn(errors):` PR convention · CODEOWNERS + branch protection · 9 sub-skills shipped · 5 production diagrams · adversarial test suite (15/20 caught) · per-skill token budget hard-checked · MUST/SHOULD/AVOID rule classification. |
| **`v1.0` — Eval that earns the claim** | 🟡 In development | Eval-framework MVP for re-mistake rate · methodology contract (n ≥ 30, multi-model, prompt hash pinned) · 30 days of real errors logged from production usage · published benchmark numbers. The first stable release ships only after the claim is measured, not before. |
| **`v1.1` — Community ecosystem** | 🔵 Planned | First external sub-skills merged (Go, Rust, Java, Swift) · sub-skill PR template institutionalised · public skill catalogue with usage stats · `learn(errors):` going wild on a public commit graph. |
| **`v2.0` — Marketplace + trust layer** | ⚪ Vision | Signed skills with reputation graph · sandboxed execution · semantic versioning · license management · cross-repo skill imports. |

## How features land

1. **Open a PR against this file (`ROADMAP.md`)** with the proposed feature, target version, and a one-paragraph motivation.
2. **CI runs** the validation pipeline (lint + schema + drift checks).
3. **Maintainer review** — a feature is accepted when the rationale is concrete and the implementation path is reviewable.
4. **The accepted feature lands in `main`** as a follow-up PR. The README's `## VERSIONS` table is regenerated from this file.

## How `v0.75` was shipped

`v0.75` is the result of a tight pre-launch sprint that produced the foundation: validators, the `learn(errors):` self-extension loop, the cross-tool loader generator, and the five production diagrams in [`docs/`](./docs/). Every commit is in the public history; every architectural decision lives in the relevant `skills/` sub-skill. There is nothing hidden — `git clone` is the entire setup and the entire story. The `v1.0` stable target is held back deliberately until the eval framework provides measured re-mistake numbers — claim and measurement ship together or not at all.

## Known follow-ups

- **Diagram sync to `skills/` paths.** The seven production SVGs in [`docs/`](./docs/) (`architecture`, `memory-to-go`, `comparison`, `error-log`, `pr-flow`, `how-it-works`, `how-it-works-mobile`) still display the legacy `references/...` path layout that `v0.75` shipped with. The code, schemas, loaders, validator, CI, and CODEOWNERS were migrated to the Anthropic Skills folder standard (`skills/<name>/SKILL.md`); the SVGs lag behind because they require pixel-perfect Bo-design-system iteration with Playwright. Tracked as a `v0.85` design sprint.

## What's not on the 2026 roadmap

A full skill marketplace with signing, reputation, sandboxing, and license management is a multi-quarter team effort. We've sketched it as `v2.0` so you know we know it's the destination — we are not promising it for this calendar year.
