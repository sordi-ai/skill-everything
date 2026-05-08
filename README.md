<div align="center">

# 🧠 Skill-Every<i>think</i>

### Every mistake your agent makes becomes a Git commit.<br>Every commit means the next session inherits the fix.

**Plain Markdown. Plain Git. No vector DB. No black box.**

<br>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)
[![GitHub Stars](https://img.shields.io/github/stars/sordi-ai/skill-everything?style=social)](https://github.com/sordi-ai/skill-everything)

[![Works with Claude Code](https://img.shields.io/badge/Works%20with-Claude%20Code-orange?logo=anthropic&logoColor=white)](https://docs.anthropic.com/en/docs/claude-code)
[![Works with Cursor](https://img.shields.io/badge/Works%20with-Cursor-000?logo=cursor&logoColor=white)](https://cursor.sh)
[![Works with Gemini CLI](https://img.shields.io/badge/Works%20with-Gemini%20CLI-4285F4?logo=google&logoColor=white)](https://github.com/google-gemini/gemini-cli)
[![Works with OpenCode](https://img.shields.io/badge/Works%20with-OpenCode-blue)](https://github.com/nicepkg/opencode)

<br>

*Side project. Two engineers. Built on weekends.*<br>
*Dogfooded daily — the [error log](./references/errors/error-log.md) is public. [Not endorsed by any employer.](./DISCLAIMER.md)*

</div>

---

## 30-second pitch

An agent makes a mistake. Instead of forgetting, it writes a YAML entry into `references/errors/error-log.md`, derives an action directive from it, and commits both as `learn(errors): ERR-2026-014`. **You review the PR.** Next session, the rule loads automatically. The repo *is* that loop.

```bash
git clone https://github.com/sordi-ai/skill-everything.git
```

That's the entire setup.

---

## Why this matters

- **Conventions don't survive across tools.** Switch from Cursor to Claude Code and `.cursorrules` is dead. Skill-everything is the same Markdown in Claude Code, Cursor, Gemini CLI, and OpenCode.
- **Agent memory is usually opaque. This one is `cat`-able.** Every rule is a file. Read it, diff it, blame it, revert it, share it. No vector store, no API key.
- **Mistakes deserve a commit, not a chat message.** A correction becomes `learn(errors): ERR-2026-014` — the error log entry and the derived rule land in one PR.
- **Per-skill token budgets, not 10k system prompts.** Each sub-skill stays under 3k tokens. The router loads only what's relevant.
- **Convention drift is a code-review problem.** Skills are reviewed in PRs. Rollback is `git revert`. No Notion wiki that decays.
- **Built on the formats your tools already read.** `CLAUDE.md`, `GEMINI.md`, `.cursorrules` — we sit *on top* of them, not next to them.

---

## ⚙️ How it works

<p align="center">
  <img src="./docs/how-it-works.svg" alt="How it works — the self-extension loop" width="100%"/>
</p>

> **Not just errors.** The same loop captures new insights, better patterns, deployment gotchas, naming conventions, API quirks — anything worth remembering. Every lesson is a Git commit you can `diff`, `blame`, `revert`, or `cherry-pick` into another project.

---

## 💰 Token math (the part nobody else shows)

We don't claim "84% savings" anymore. The honest comparison is more interesting:

| Setup | Input tokens / message | Cache-friendly? | Cost / 1k messages | vs. uncached monolith |
|---|---:|:---:|---:|---:|
| Monolithic `.cursorrules`, no caching | 10,000 | — | $75.00 | baseline |
| Monolithic + Anthropic prompt caching | 10,000 (~1k effective) | ✓ ideal | $48.00 | **−36%** |
| Skill-everything, single sub-skill | 1,600 | partial | $50.00 | **−33%** |
| Skill-everything, 2–3 sub-skills | 3,300 | partial | $55.00 | **−27%** |
| Skill-everything **with caching** | 1,600 (~800 effective) | partial | **$47.00** | **−1%** vs. cached monolith |

> Math: Sonnet-class pricing $3 / 1M input, $15 / 1M output, ~3,000 output tokens / message.

**The honest take:**

- **20–34% cheaper** than uncached monolithic prompts.
- **Roughly break-even** with cached monolithic prompts. The bar for monolithic prompts gets *much* tougher when caching is on.
- The win is *modular*: you only load what's relevant. The cost of *adding* a skill stays small.

<details>
<summary><strong>Per-skill token budgets (real tiktoken counts)</strong></summary>

<br>

<!-- token-table:start -->

| Sub-skill | Tokens (real, tiktoken cl100k) | Path |
|---|---:|---|
| Code Quality | ~1,000 | `references/development/code-quality.md` |
| Python | ~2,000 | `references/development/python.md` |
| TypeScript | ~2,300 | `references/development/typescript.md` |
| React | ~2,400 | `references/development/react.md` |
| Git Conventions | ~650 | `references/git/conventions.md` |
| Review & Deployment | ~800 | `references/process/review-deployment.md` |
| Domain Knowledge (template) | ~850 | `references/domain/template.md` |
| Error Log (grows with entries) | ~1,200 | `references/errors/error-log.md` |
| Self-Extension Workflow | ~1,100 | `references/errors/self-extension-workflow.md` |
| **Total if all loaded** | **~12,300** | — |
| **Typical (router + 1–2 skills)** | **~1,800–3,500** | depends on task |

<!-- token-table:end -->

> Numbers are auto-updated by `python tools/render_readme_table.py`. CI fails on drift.

</details>

---

## 🔄 Self-extension: the agent teaches itself

This is where it gets interesting. The agent doesn't just *use* the skill — it *grows* the skill:

1. **Trigger** — a test fails, the user corrects you, your first approach was wrong.
2. **Search** — check if a similar error already exists (no duplicates).
3. **Analyse** — root cause, false assumption, impact.
4. **Formulate** — action directive: *"Always X before Y"* or *"Never Z without W"*.
5. **Open a PR** labelled `needs-rule-review`. Never push to `main`.
6. **Human reviews + merges.**

> Every mistake makes the system permanently better. The improvement is a Git commit you can review, revert, or share.

The CI lint validates the proposed rule against [`schemas/error-entry.json`](./schemas/error-entry.json) plus a [verb allow-list and forbidden-pattern set](./tools/validate_rules.py). The validator is **best-effort, not airtight** — see [SECURITY.md](./SECURITY.md) for the threat model and the [adversarial test suite](./tests/test_validate_rules_adversarial.py) for the documented bypasses.

---

## 🎯 Concrete examples (real, from the public error log)

The first three entries committed during dogfooding — see [`references/errors/error-log.md`](./references/errors/error-log.md):

- **`ERR-2026-001` — TS strict-null disabled for convenience.** Agent disabled `strictNullChecks` to make a demo green. Local pass, CI failure. Rule: *"Never disable strict checks for convenience."*
- **`ERR-2026-007` — Rename without import sweep.** Refactor missed 4 imports. Rule: *"After any rename, run a project-wide grep before claiming done."* `count` jumped from 1 to 2 on the second occurrence — that's repeat prevention in action.
- **`ERR-2026-012` — Wrong deployment order.** A migration had to run before the backend deploy; the agent picked the wrong sequence. Domain knowledge moved to `references/domain/`, not global code-quality.

Each entry links a real commit SHA. None of these are hypothetical.

---

## 🚀 Quick start

```bash
git clone https://github.com/sordi-ai/skill-everything.git
```

<details>
<summary><strong>Claude Code</strong> — auto-discovers <code>CLAUDE.md</code></summary>

Add the repository as a submodule into your project, or clone it next to your project. Claude Code reads `CLAUDE.md` automatically. Or reference sub-skills directly:

```markdown
@references/development/code-quality.md
@references/errors/error-log.md
```

</details>

<details>
<summary><strong>Gemini CLI</strong> — auto-discovers <code>GEMINI.md</code></summary>

Same as above. Use `/memory show` to verify the loaded context. Use `/memory refresh` after edits.

</details>

<details>
<summary><strong>Cursor</strong> — paste <code>SKILL.md</code> into Settings → Rules for AI</summary>

Cursor doesn't auto-discover `CLAUDE.md`/`GEMINI.md` files. Either paste `SKILL.md` content directly into **Settings → Rules for AI**, or maintain a `.cursorrules` file with `@file:./skill-everything/SKILL.md` if your Cursor build supports it.

</details>

<details>
<summary><strong>OpenCode</strong> — via <code>opencode.json</code></summary>

```json
{
  "skills": ["./skill-everything/SKILL.md"]
}
```

The `skill_resource` tool lets the agent load individual sub-skills on demand without bloating the context window.

</details>

---

## 📊 Honest comparison

How does this compare to the things it's actually competing with? We've seen too many tables where the new tool wins every column. This one doesn't:

| Capability | Skill-everything | AGENTS.md | aider conv. | Cursor Rules | mem0 / MemGPT | LangGraph |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Plain Markdown, no DB | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Git-versioned out of the box | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Cross-tool portable | ✓ | partial | aider-only | Cursor-only | ✓ | ✓ |
| Structured error schema (JSON-Schema validated) | ✓ | ✗ | ✗ | ✗ | ✗ | partial |
| `learn(errors): …` PR workflow | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Per-skill token-budget router | ✓ | ✗ | ✗ | ✗ | n/a | n/a |
| Skill-manifest frontmatter (versioned) | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Embedding-based recall | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ |
| Scales to 1,000+ rules | partial | partial | partial | partial | ✓ | ✓ |
| Setup cost | `git clone` | none | none | none | API key + SaaS | code + infra |

**Honest reading:** we win on Markdown + Git + structured workflow. mem0 and LangGraph win on embeddings and large-scale retrieval. AGENTS.md and Cursor Rules are siblings — we sit on top of them and add the missing review and validation layers.

---

## 📁 What's inside

```
skill-everything/
├── SKILL.md                       # Router for OpenCode (generated)
├── CLAUDE.md                      # Router for Claude Code (generated)
├── GEMINI.md                      # Router for Gemini CLI (generated)
├── DISCLAIMER.md                  # Independent project, no employer endorsement
├── SECURITY.md                    # Threat model + responsible-disclosure
├── references/
│   ├── _index.yml                 # Single source of truth for the routers
│   ├── development/               # Language sub-skills
│   │   ├── code-quality.md        #   23 generic rules
│   │   ├── python.md              #   20 Python-specific rules
│   │   ├── typescript.md          #   17 TypeScript rules
│   │   └── react.md               #   17 React rules
│   ├── git/conventions.md
│   ├── process/review-deployment.md
│   ├── domain/template.md
│   ├── errors/
│   │   ├── error-log.md           # YAML entries (validated by CI)
│   │   ├── exceptions.yml         # Forbidden-pattern bypass list
│   │   └── self-extension-workflow.md
│   └── _templates/
├── schemas/
│   ├── error-entry.json           # JSON-Schema for log entries
│   └── skill-manifest.json        # JSON-Schema for sub-skill frontmatter
├── tools/
│   ├── generate-dashboard.py      # Updates docs/dashboard.html
│   ├── validate_rules.py          # CI lint: schema + verb allow-list
│   ├── render_loaders.py          # Regenerates SKILL/CLAUDE/GEMINI from _index.yml
│   ├── render_readme_table.py     # Regenerates the token table above
│   └── templates/                 # Jinja2 templates for the routers
├── tests/                         # pytest suite + adversarial bypass tests
├── .github/
│   ├── CODEOWNERS
│   ├── ISSUE_TEMPLATE/
│   └── workflows/
│       ├── ci.yml                 # ruff + pyright + pytest + secret-scan
│       ├── lint-rules.yml         # validate_rules.py
│       └── auto-approve-rule-pr.yml
├── CONTRIBUTING.md
└── LICENSE
```

---

## 🛠️ Create your own skill

```bash
cp references/_templates/sub-skill.template.md references/my-area/my-skill.md
# Add frontmatter (id, version, tokens_target, triggers), fill in rules, open a PR.
```

Each sub-skill has a [skill-manifest frontmatter block](./schemas/skill-manifest.json) declaring its `id`, `version`, `tokens_target`, `triggers`, and load order. CI validates the frontmatter on every PR. Keep each skill under **3,000 tokens**. Split rather than bloat. Rules are action directives, not descriptions.

---

## 🗺️ Roadmap

| Phase | When | What |
|---|---|---|
| **Phase 1** | weeks 1–2 | Pre-launch repair: lint-rules CI, schema validator, XSS hardening, honest token table, single-source-of-truth loader sync, CODEOWNERS + branch protection. **You're looking at it.** |
| **Phase 2** | weeks 3–6 | Self-use validation: 30 days of real errors logged from a side project, eval framework MVP for re-mistake rate, baseline methodology documented (n, model, temperature, prompt hash). |
| **Phase 3** | weeks 7–10 | Soft launch: small Show HN posts (Eval-Tool + Skill-Repo), Twitter thread with the real numbers, first community PRs landing. |
| **Phase 4** | weeks 11–24 | Big launch + community: Show HN proper, first external sub-skills (Go, Rust, Java) merged, sub-skill PR template institutionalised. |

> **Vision (not on a 2026 roadmap):** a skill marketplace with trust layer (signing + reputation), sandboxing (skills are executable instructions — prompt-injection risk), versioning, and licence management. That's a 6–12 month team-effort, not something a side project ships next year.

---

## ❓ FAQ

<details>
<summary><strong>Does this work with my agent?</strong></summary>

If your agent reads Markdown, yes. We've confirmed it with Claude Code, Cursor, Gemini CLI, and OpenCode. Other agents that read Markdown context files (aider, Continue.dev) should work too — file an issue if not.

</details>

<details>
<summary><strong>How large can a skill get?</strong></summary>

Hard cap: 3,000 tokens (`tokens_target` in the frontmatter is enforced via CI lint). When it grows beyond that, split it. Two precise modules beat one bloated one.

</details>

<details>
<summary><strong>Can the agent really extend itself?</strong></summary>

Yes — but only via PR. The workflow in [`references/errors/self-extension-workflow.md`](./references/errors/self-extension-workflow.md) describes exactly how the agent formulates entries, classifies them, and opens a PR labelled `needs-rule-review`. CI lints the rule. A human reviews and merges. The agent never pushes to `main`.

</details>

<details>
<summary><strong>What's the difference from <code>.cursorrules</code> or <code>AGENTS.md</code>?</strong></summary>

`.cursorrules` and `AGENTS.md` are static rule files. They don't have a structured error schema, a versioned manifest, a `learn()` PR workflow, or a CI validator. We sit on top of these formats — the file your tool reads (`CLAUDE.md`, `GEMINI.md`, `.cursorrules`) is generated from `references/_index.yml`.

</details>

<details>
<summary><strong>Do I need a database?</strong></summary>

No. Plain Markdown. Git. That's it. No vector DB, no embeddings, no running processes. `git clone` is the entire setup.

</details>

<details>
<summary><strong>What if a rule turns out to be wrong?</strong></summary>

`git revert`. Every change is versioned. That's the whole point.

</details>

<details>
<summary><strong>Is this safe to run? The agent writes its own rules.</strong></summary>

That's the threat model spelled out in [SECURITY.md](./SECURITY.md). The CI validator catches obvious bad patterns (URLs, shell binaries, credential paths, base64 blobs, `<script>` tags). It does **not** catch homoglyphs, indirection, or natural-language nudges — see the [adversarial test suite](./tests/test_validate_rules_adversarial.py). Human PR review is the primary trust boundary. Don't enable auto-merge on `references/errors/`. Use the [`.github/CODEOWNERS`](./.github/CODEOWNERS) file to require maintainer review on rule changes.

</details>

<details>
<summary><strong>How does this save tokens?</strong></summary>

See the [Token math](#-token-math-the-part-nobody-else-shows) section above. Headline: 20–34% cheaper than an uncached monolithic prompt; roughly break-even with a cached one. We don't claim 84%.

</details>

---

<div align="center">

### Built because we got tired of watching agents make the same mistakes we already taught them not to make.

**[⭐ Star this repo](https://github.com/sordi-ai/skill-everything)** if you think agents should learn from the work you've already done with them.

<br>

MIT License · [Contributing](./CONTRIBUTING.md) · [Security](./SECURITY.md) · [Disclaimer](./DISCLAIMER.md) · [Report a bug](https://github.com/sordi-ai/skill-everything/issues)

</div>
