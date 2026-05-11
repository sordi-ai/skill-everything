# Roadmap

> **`v0.75` is the current preview release.** Foundation work is done; `v1.0` ships only when the eval framework earns the claim. New features land in `main` via PR — every change is a commit, every commit is reviewed, every release is auditable.

## Versions

| Version | Status | What |
|---|:---:|---|
| **`v0.75` — Foundation** | 🟡 **PREVIEW** | `lint-rules` CI · JSON-Schema validator · XSS hardening · single-source-of-truth loader sync · `learn(errors):` PR convention · CODEOWNERS + branch protection · 9 sub-skills shipped · 7 production diagrams (skills/ paths synced) · adversarial test suite (15/20 caught) · per-skill token budget hard-checked · MUST/SHOULD/AVOID rule classification · **eval framework MVP wired (dry-run end-to-end, schema-validated, CI-gated, n=50/100 methodology contract published)**. |
| **`v1.0` — Eval that earns the claim** | 🟡 In development | Real-provider integration (Anthropic + OpenAI + Ollama) for the eval harness · `tests/eval/results/baseline.jsonl` populated under the methodology contract (n ≥ 100, 5 dated-SKU models, T ∈ {0.0, 0.7}) · macro-Re-Mistake-Rate ≤ 0.40 with bootstrap 95 % CI upper ≤ 0.55 · published per-cell numbers in the README. The first stable release ships only after the claim is measured, not before. |
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

- **Architecture diagram holistic upgrade (`v0.85+`).** Bo (senior diagrammatic designer) proposed a folder-strip visualisation at the bottom of `docs/architecture.svg` to make "composable sub-skills" visible rather than asserted (a row of nine mini-folder glyphs corresponding to the nine skills under `skills/<name>/SKILL.md`). Anya's minimal-diff string-only update has shipped; Bo's holistic upgrade needs its own Playwright iteration loop with maintainer pixel review before merging.

## What's not on the 2026 roadmap

A full skill marketplace with signing, reputation, sandboxing, and license management is a multi-quarter team effort. We've sketched it as `v2.0` so you know we know it's the destination — we are not promising it for this calendar year.
