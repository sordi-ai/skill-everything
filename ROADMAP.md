# Roadmap

> **`v0.85` is the current release.** 23 sub-skills shipped, eval framework wired. `v1.0` ships when the eval measurement run earns the claim. New features land in `main` via PR — every change is a commit, every commit is reviewed, every release is auditable.

## Versions

| Version | Status | What |
|---|:---:|---|
| **`v0.85` — Skill expansion** | 🟢 **CURRENT** | 13 new sub-skills (tdd, debugging, security-review, docker, shell-scripting, db-schema, github-cli, branch-finishing, fastapi, langchain, drawio, brainstorming, implementation-plan) · 3 fold-ins to existing skills (python, react, code-quality) · 16 new ERR entries (ERR-2026-014 through ERR-2026-029) · 13 new eval tasks · skill count 10 → 23 · tests 38 → 55 · SVG-check sub-skill with Playwright bbox validation · eval framework MVP + v1.0 eval build-out with real providers. |
| **`v0.75` — Foundation** | ✅ **SHIPPED** | `lint-rules` CI · JSON-Schema validator · XSS hardening · single-source-of-truth loader sync · `learn(errors):` PR convention · CODEOWNERS + branch protection · 9 sub-skills shipped · 13 production diagrams (skills/ paths synced) · adversarial test suite (15/20 caught) · per-skill token budget hard-checked · MUST/SHOULD/AVOID rule classification · **eval framework wired with real providers (Anthropic + OpenAI + Ollama SDK shim, retry-on-transient, tier-3 judge + 20-row calibration corpus, `compare_eval.py` ±10pp baseline gate)**. |
| **`v1.0` — Eval that earns the claim** | 🟡 In development | Curated `tests/eval/results/baseline.jsonl` populated under the methodology contract (n ≥ 100 per cell, 5 dated-SKU models, T ∈ {0.0, 0.7}) · macro-Re-Mistake-Rate ≤ 0.40 with bootstrap 95 % CI upper ≤ 0.55 · per-model floor satisfied · tier-3 judge calibration ≥ 0.90 · published per-cell numbers. Provider integration is shipped; the ~$500 measurement run earns the stable tag, not the framework. |
| **`v1.1` — Community ecosystem** | 🔵 Planned | First external sub-skills merged (Go, Rust, Java, Swift) · sub-skill PR template institutionalised · public skill catalogue with usage stats · `learn(errors):` going wild on a public commit graph. |
| **`v2.0` — Marketplace + trust layer** | ⚪ Vision | Signed skills with reputation graph · sandboxed execution · semantic versioning · license management · cross-repo skill imports. |

## How features land

1. **Open a PR against this file (`ROADMAP.md`)** with the proposed feature, target version, and a one-paragraph motivation.
2. **CI runs** the validation pipeline (lint + schema + drift checks).
3. **Maintainer review** — a feature is accepted when the rationale is concrete and the implementation path is reviewable.
4. **The accepted feature lands in `main`** as a follow-up PR. The README's `## VERSIONS` table is regenerated from this file.

## How `v0.75` was shipped

`v0.75` is the result of a tight pre-launch sprint that produced the foundation: validators, the `learn(errors):` self-extension loop, the cross-tool loader generator, and the 13 production diagrams in [`docs/`](./docs/). Every commit is in the public history; every architectural decision lives in the relevant `skills/` sub-skill. There is nothing hidden — `git clone` is the entire setup and the entire story. The `v1.0` stable target is held back deliberately until the eval framework provides measured re-mistake numbers — claim and measurement ship together or not at all.

## Known follow-ups

- **Architecture diagram holistic upgrade (`v0.85+`).** The path-string sync for `docs/architecture.svg` has shipped. A follow-up design pass proposes replacing the flat "SUB-SKILL DIRECTORY" chip with a horizontal strip of nine mini-folder glyphs (one per skill under `skills/<name>/SKILL.md`) — making the Anthropic-Skill folder pattern visible rather than asserted. The upgrade ships when the iteration loop produces a clean light + dark rendering at the maintainer pixel-review bar.

## What's not on the 2026 roadmap

A full skill marketplace with signing, reputation, sandboxing, and license management is a multi-quarter team effort. We've sketched it as `v2.0` so you know we know it's the destination — we are not promising it for this calendar year.
