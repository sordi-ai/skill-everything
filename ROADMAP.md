# Roadmap

> **`v1.0` is stable and released.** New features land in `main` via PR — every change is a commit, every commit is reviewed, every release is auditable.

## Versions

| Version | Status | What |
|---|:---:|---|
| **`v1.0` — Foundation** | 🟢 **STABLE** | `lint-rules` CI · JSON-Schema validator · XSS hardening · single-source-of-truth loader sync · `learn(errors):` PR convention · CODEOWNERS + branch protection · 9 sub-skills shipped · 5 production diagrams · adversarial test suite. |
| **`v1.1` — Eval that earns the claim** | 🟡 In development | Eval-framework MVP for re-mistake rate · methodology contract (n ≥ 30, multi-model, prompt hash pinned) · 30 days of real errors logged from production usage · published benchmark numbers. |
| **`v1.2` — Community ecosystem** | 🔵 Planned | First external sub-skills merged (Go, Rust, Java, Swift) · sub-skill PR template institutionalised · public skill catalogue with usage stats · `learn(errors):` going wild on a public commit graph. |
| **`v2.0` — Marketplace + trust layer** | ⚪ Vision | Signed skills with reputation graph · sandboxed execution · semantic versioning · license management · cross-repo skill imports. |

## How features land

1. **Open a PR against this file (`ROADMAP.md`)** with the proposed feature, target version, and a one-paragraph motivation.
2. **CI runs** the validation pipeline (lint + schema + drift checks).
3. **Maintainer review** — a feature is accepted when the rationale is concrete and the implementation path is reviewable.
4. **The accepted feature lands in `main`** as a follow-up PR. The README's `## VERSIONS` table is regenerated from this file.

## How `v1.0` was shipped

`v1.0` is the result of a tight pre-launch sprint that produced the foundation: validators, the `learn(errors):` self-extension loop, the cross-tool loader generator, and the five production diagrams in [`docs/`](./docs/). Every commit is in the public history; every architectural decision lives in the relevant `references/` sub-skill. There is nothing hidden — `git clone` is the entire setup and the entire story.

## What's not on the 2026 roadmap

A full skill marketplace with signing, reputation, sandboxing, and license management is a multi-quarter team effort. We've sketched it as `v2.0` so you know we know it's the destination — we are not promising it for this calendar year.
