<div align="center">

<sub>🧠 SELF-LEARNING · ⚡ TOKEN-EFFICIENT · 🚀 MULTI-AGENT</sub>

# skill-everything

### Never make the same mistake twice.

### The self-learning memory layer for AI agents — beyond fine-tuning.

**Self-extending skills in plain Markdown. Save tokens. Enhance quality. Ship smarter agents — across Claude Code, Cursor, Gemini CLI, and OpenCode.**

[![GitHub stars](https://img.shields.io/github/stars/sordi-ai/skill-everything?style=for-the-badge&logo=github&color=gold)](https://github.com/sordi-ai/skill-everything/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](./LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/sordi-ai/skill-everything?style=for-the-badge&color=green)](https://github.com/sordi-ai/skill-everything/commits/main)
[![Commit Activity](https://img.shields.io/github/commit-activity/m/sordi-ai/skill-everything?style=for-the-badge&color=brightgreen)](https://github.com/sordi-ai/skill-everything/commits/main)

[![Self-Learning](https://img.shields.io/badge/AI_Memory-Self--Learning-gold?style=for-the-badge&logo=brain)](./docs/how-it-works.svg)
[![Beyond Fine-Tuning](https://img.shields.io/badge/Beyond-Fine--Tuning-purple?style=for-the-badge&logo=anthropic)](./docs/architecture.svg)
[![Token Efficient](https://img.shields.io/badge/Tokens-20--34%25_Lower-1f7a4a?style=for-the-badge&logo=lightning)](./docs/token-math.svg)
[![Quality Compounds](https://img.shields.io/badge/Quality-Compounds-ff6b35?style=for-the-badge&logo=trendingup)](./references/errors/error-log.md)

[![CI](https://img.shields.io/github/actions/workflow/status/sordi-ai/skill-everything/ci.yml?style=for-the-badge&label=CI&logo=githubactions&logoColor=white)](./.github/workflows/ci.yml)
[![Schemas](https://img.shields.io/badge/Schemas-JSON_Validated-blue?style=for-the-badge&logo=json)](./schemas/skill-manifest.json)
[![PR Reviewed](https://img.shields.io/badge/Updates-PR_Reviewed-darkblue?style=for-the-badge&logo=git)](./CONTRIBUTING.md)
[![Per-Skill Cap](https://img.shields.io/badge/Per--Skill_Cap-3K_Tokens-1f7a4a?style=for-the-badge)](./schemas/skill-manifest.json)

[![Claude Code](https://img.shields.io/badge/Works_With-Claude_Code-CC785C?style=for-the-badge&logo=anthropic&logoColor=white)](./CLAUDE.md)
[![Cursor](https://img.shields.io/badge/Works_With-Cursor-000000?style=for-the-badge&logo=cursor&logoColor=white)](./.cursorrules)
[![Gemini CLI](https://img.shields.io/badge/Works_With-Gemini_CLI-4285F4?style=for-the-badge&logo=google&logoColor=white)](./GEMINI.md)
[![OpenCode](https://img.shields.io/badge/Works_With-OpenCode-9333EA?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](./AGENTS.md)

🚀 **One source of truth · Four agent runtimes · Zero re-authoring**
♻️ **Errors become commits · Commits become skills · Skills make agents smarter**

</div>

---

## THE PITCH IN 30 SECONDS
*One paragraph. One terminal command. The repo is the loop.*

Your agent makes a mistake. Most setups forget. **This one commits.**

It writes a YAML entry into `references/errors/error-log.md`, derives a one-line action directive, and opens a PR labelled `needs-rule-review` titled `learn(errors): ERR-2026-014`. **You review the PR.** CI lints it against a JSON-Schema and a verb allow-list. After merge, the rule loads automatically — in Claude Code, in Cursor, in Gemini CLI, in OpenCode. **Same Markdown. Four tools. Zero re-authoring.**

```bash
git clone https://github.com/sordi-ai/skill-everything.git
```

That is the entire setup. **Star this repo if you want your agent's memory to be `cat`-able, `git diff`-able, and reviewable like code.**

> [!NOTE]
> **This sits on top of `CLAUDE.md`, not instead of it.** Skill-everything generates the rule files Claude Code, Cursor, Gemini CLI, and OpenCode already read — Anthropic's native Skills covers a different layer (packaging and distribution). We work alongside it, not against it.

---

## WHY THIS MATTERS
*Six structural arguments. Each survives an HN audit. Each is verifiable in 30 seconds with `cat` or `grep`.*

- **Cross-tool agent memory by construction.** Switch from Cursor to Claude Code and `.cursorrules` is dead. Skill-everything is the *same Markdown* in Claude Code, Cursor, Gemini CLI, and OpenCode — generated from one [`references/_index.yml`](./references/_index.yml), drift-checked in CI on every PR.
- **`cat`-able memory beats black-box memory.** Every rule is a file. `git diff` it, `git blame` it, `git revert` it, screenshot it, share it. **No vector store. No API key. No SaaS dashboard.** Your agent's brain lives in `references/`.
- **`learn(errors):` is the commit-type of the loop.** A correction becomes `learn(errors): ERR-2026-014` — error log entry and derived rule in one PR, signed by a human. **`git log --grep="learn("` is your agent's growth trail.**
- **Add the 10th, 50th, 200th skill — your per-message bill stays flat.** Per-skill 3k-token cap, CI-enforced by [`tools/validate_rules.py`](./tools/validate_rules.py). The router loads only what is relevant for the task.
- **PR-reviewed agent learning.** The agent never pushes to `main`. Every rule that goes live has been seen by a human. `git revert` is the rollback. **Notion wikis decay. Git history doesn't.**
- **Built on the formats your tools already read.** `CLAUDE.md`, `GEMINI.md`, `.cursorrules` are *generated* from `references/_index.yml`. **We sit on top of the ecosystem, not next to it.**

---

## HOW IT WORKS
*Six steps from mistake to merged rule. Three lanes — agent, CI, human. One substrate — git.*

<picture>
  <source media="(max-width: 600px)" srcset="./docs/how-it-works-mobile.svg">
  <img src="./docs/how-it-works.svg" alt="The self-extension loop — six steps from agent trigger to merged rule, with three serial CI gates">
</picture>

*Trigger → Analyse → Formulate → PR → Lint → Merge. The agent runs steps 1–4 automatically. CI runs step 5. **You** run step 6. The same loop captures errors, deployment gotchas, naming conventions — anything worth remembering, in the format every modern agent reads.*

> [!NOTE]
> **CI GATE · lint-rules + auto-approve-rule-pr** — both gates enforce the trust boundary before any rule reaches `main`. Skill-everything **treats prompt-injection as a supply-chain problem**, not a magic feature. Threat model in [SECURITY.md](./SECURITY.md).

---

## ARCHITECTURE
*One register. Four loaders. Identical sub-skill set. CI fails on drift.*

`references/_index.yml` is the master register. **One file.** Every sub-skill is declared once with its `id`, `tokens_target`, `triggers`, and load order. From it, [`tools/render_loaders.py`](./tools/render_loaders.py) regenerates **four** loader files: `SKILL.md` (OpenCode), `CLAUDE.md` (Claude Code), `GEMINI.md` (Gemini CLI), and `.cursorrules` (Cursor). **Edit the index, regenerate, done.**

A CI no-drift job runs `git diff --exit-code` against the regenerated loaders on every PR. **Hand-edit a loader and CI fails.** The fix is to edit `_index.yml` and regenerate — no more "Cursor team forgot to update Claude config" tickets.

![Architecture — _index.yml as master, render_loaders.py as generator, four loaders rendering the same sub-skill directory](./docs/architecture.svg)

*One source of truth. Four loaders. Zero drift.*

> [!NOTE]
> **CI GATE · loaders-no-drift** — `git diff --exit-code` against regenerated `SKILL.md`, `CLAUDE.md`, `GEMINI.md`, `.cursorrules`. The drift test is the no-marketing-fudging test.

---

## SELF-EXTENSION
*Your agent's mistakes — versioned. From error to rule in one PR. Memory you can `git diff`.*

The agent doesn't just *use* the skill — it **grows the skill**. Trigger → search → analyse → formulate → PR → human merge. Six steps. **From error to rule in one PR.** Every rule that goes live has been seen by a human.

`learn(errors):` is a commit-type that *triggers* the `lint-rules` CI, the `auto-approve-rule-pr` workflow, and the CODEOWNERS gate — branding and plumbing in one prefix.

```text
$ git log --grep="learn("
learn(errors): ERR-2026-001 — never disable strict checks for convenience
learn(errors): ERR-2026-007 — grep before claiming a rename complete
learn(errors): ERR-2026-012 — order migrations before backend deploys
```

The full procedure with troubleshooting lives in [`references/errors/self-extension-workflow.md`](./references/errors/self-extension-workflow.md). The CI lint validates the proposed rule against [`schemas/error-entry.json`](./schemas/error-entry.json) plus a [verb allow-list and forbidden-pattern set](./tools/validate_rules.py).

> [!WARNING]
> **HUMAN GATE · CODEOWNERS approval** — the validator is best-effort, not airtight. Human PR review is the primary trust boundary. See [SECURITY.md](./SECURITY.md) and the [adversarial test suite](./tests/test_validate_rules_adversarial.py) — **we publish every bypass we know about.**

---

## TOKEN MATH
*Add a skill. Pay nothing. Per-message input cost stays flat as the library grows.*

![Token-math chart — monolithic prompts grow with skill count, skill-everything stays flat](./docs/token-math.svg)

**The architectural promise:** monolithic prompts pay every skill on every message. Skill-everything pays only what the router opens for the task at hand.

| Setup | Input/msg | Cost / 1k msgs |
|---|---:|---:|
| Monolithic `.cursorrules`, no caching | 10,000 | $75.00 |
| Monolithic + Anthropic prompt caching | 10,000 (~1k effective) | $48.00 |
| `skill-everything`, single sub-skill | 1,600 | $50.00 |
| `skill-everything`, 2–3 sub-skills | 3,300 | $55.00 |
| `skill-everything` **with caching** | 1,600 (~800 effective) | **$47.00** |

*Math: Sonnet-class pricing $3 / 1M input, $15 / 1M output, ~3,000 output tokens / message.*

**The honest take:**

- **20–34 % cheaper** than uncached monolithic prompts.
- **Roughly break-even** with cached monolithic prompts at today's 9-skill scale.
- The **architectural win** is structural: at 30, 90, 200 skills — caching helps both, but only one of the two architectures keeps your per-message input cost flat. **That's the bet. We don't claim 84%.**

<details>
<summary><strong>Per-skill token budgets — real tiktoken counts, CI-validated</strong></summary>

<br>

<!-- token-table:start -->

| Sub-skill | Path | Tokens (tiktoken cl100k) |
|---|---|---:|
| `code-quality` | `references/development/code-quality.md` | ~1,000 |
| `python` | `references/development/python.md` | ~2,000 |
| `typescript` | `references/development/typescript.md` | ~2,300 |
| `react` | `references/development/react.md` | ~2,400 |
| `git-conventions` | `references/git/conventions.md` | ~650 |
| `review-deployment` | `references/process/review-deployment.md` | ~800 |
| `domain-template` | `references/domain/template.md` | ~850 |
| `error-log` | `references/errors/error-log.md` | ~1,200 |
| `self-extension-workflow` | `references/errors/self-extension-workflow.md` | ~1,100 |
| **Total if all loaded** | — | **~12,300** |
| **Typical (router + 1–2 skills)** | depends on task | **~1,800–3,500** |

<!-- token-table:end -->

*Numbers auto-updated by `python tools/render_readme_table.py`. CI fails on drift. **No marketing fudging possible.***

</details>

---

## CONCRETE EXAMPLES
*Three real mistakes. Three Git commits. None hypothetical.*

The first three entries committed during dogfooding — see [`references/errors/error-log.md`](./references/errors/error-log.md):

| ID | Mistake | Derived rule |
|---|---|---|
| `ERR-2026-001` | TS `strictNullChecks` disabled to make a demo green | Never disable strict checks for convenience |
| `ERR-2026-007` | Refactor missed 4 imports after rename | After any rename, run a project-wide grep before claiming done |
| `ERR-2026-012` | Migration ran after backend deploy, broke prod | Always order migrations before backend deploy in domain runbooks |

*Each entry links a real commit SHA. `ERR-2026-007`'s `count` jumped from 1 to 2 on the second occurrence — **repeat-prevention captured in YAML, reviewed by a human, merged into `main`**.*

[**Browse the public error log →**](./references/errors/error-log.md) — every mistake we have made and learned from, in plain Markdown.

---

## QUICK START
*Three steps. Five minutes. Your agent reads the same Markdown in all four tools.*

```bash
git clone https://github.com/sordi-ai/skill-everything.git
```

<details open>
<summary><strong>Claude Code</strong> — auto-discovers <code>CLAUDE.md</code></summary>

<br>

Add the repository as a submodule into your project, or clone it next to your project. Claude Code reads `CLAUDE.md` automatically. Or reference sub-skills directly:

```markdown
@references/development/code-quality.md
@references/errors/error-log.md
```

</details>

<details>
<summary><strong>Gemini CLI</strong> — auto-discovers <code>GEMINI.md</code></summary>

<br>

Same as above. Use `/memory show` to verify the loaded context. Use `/memory refresh` after edits.

</details>

<details>
<summary><strong>Cursor</strong> — paste <code>SKILL.md</code> into Settings → Rules for AI</summary>

<br>

Cursor does not auto-discover `CLAUDE.md` / `GEMINI.md` files. Either paste `SKILL.md` content directly into **Settings → Rules for AI**, or maintain a `.cursorrules` file with `@file:./skill-everything/SKILL.md` if your Cursor build supports it.

</details>

<details>
<summary><strong>OpenCode</strong> — via <code>opencode.json</code></summary>

<br>

```json
{
  "skills": ["./skill-everything/SKILL.md"]
}
```

The `skill_resource` tool lets the agent load individual sub-skills on demand without bloating the context window.

</details>

---

## HONEST COMPARISON
*Fair, not flattering. We don't win every column — that's deliberate.*

<div style="overflow-x:auto">

| Capability | **`skill-everything`** | AGENTS.md | Cursor Rules | mem0 / MemGPT |
|---|:---:|:---:|:---:|:---:|
| Plain Markdown, no DB | ✓ | ✓ | ✓ | ✗ |
| Git-versioned out of the box | ✓ | ✓ | ✓ | ✗ |
| **Cross-tool portable (one source, four loaders)** | **✓** | ◐ | Cursor-only | ✓ |
| **Per-skill 3k-token cap, CI-enforced** | **✓** | ✗ | ✗ | n/a |
| **Schema-validated rule entries** | **✓** | ✗ | ✗ | ✗ |
| Versioned skill-manifest frontmatter | ✓ | ✗ | ✗ | ✗ |
| Embedding-based recall | ✗ | ✗ | ✗ | ✓ |
| Scales to 1,000+ rules | ✗ | ✗ | ✗ | ✓ |
| Setup cost | `git clone` | none | none | API key + SaaS |

</div>

*We win on cross-tool portability, the token-cap router, and machine-validated rule entries. **mem0 wins on embeddings and 1k-rule scale** — if that's your problem, use mem0. AGENTS.md and Cursor Rules are siblings — we sit on top of them and add the missing review and validation layers. **At 9 sub-skills today, we are not pretending to scale to 1k.***

---

## WHAT'S INSIDE
*The directory tree. Mono identifiers, comment column.*

```text
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

## CREATE YOUR OWN SKILL
*Copy the template, fill the frontmatter, open a PR. CI takes care of the rest.*

```bash
cp references/_templates/sub-skill.template.md references/my-area/my-skill.md
# Add frontmatter (id, version, tokens_target, triggers), fill in rules, open a PR.
```

Each sub-skill has a [skill-manifest frontmatter block](./schemas/skill-manifest.json) declaring its `id`, `version`, `tokens_target`, `triggers`, and load order. CI validates the frontmatter on every PR. **Keep each skill under 3,000 tokens.** Split rather than bloat. Rules are action directives, not descriptions.

---

## ROADMAP
*We're shipping, not pitching. Star the repo to track Phase 2 → 3 → 4.*

| Phase | When | What |
|---|---|---|
| **`phase-1` — Foundation** | this repo, today | `lint-rules` CI · schema validator · XSS hardening · honest token table · single-source-of-truth loader sync · CODEOWNERS + branch protection. **You're looking at it.** |
| **`phase-2` — Eval that earns the claim** | weeks 3–6 | 30 days of real errors logged · eval-framework MVP for re-mistake rate · methodology contract published (n≥30, multi-model, prompt hash pinned). **No vibe-check numbers ship before this lands.** |
| **`phase-3` — Soft launch** | weeks 7–10 | Targeted Show HN posts (eval-tool + skill-repo) · Twitter thread with the real numbers · first community PRs landing — `learn(errors):` going wild on a public commit graph. |
| **`phase-4` — Community + ecosystem** | weeks 11–24 | Big launch · first external sub-skills (Go, Rust, Java) merged · sub-skill PR template institutionalised. The skill library starts looking like a public dataset. |

*Vision (not on a 2026 roadmap): a skill-marketplace with trust layer (signing + reputation), sandboxing, versioning, license management. That's a 6–12 month team-effort, **not something a side project ships next year**. We say it out loud so you know what we're not promising.*

---

## FAQ
*The eight questions we expect on Show HN. Honest answers, no hedging.*

<details>
<summary><strong>Does this work with my agent?</strong></summary>

<br>

If your agent reads Markdown, **yes**. **One repo, four loaders, zero re-authoring.** Confirmed: Claude Code, Cursor, Gemini CLI, OpenCode. Probable: aider, Continue.dev, any tool that auto-discovers `CLAUDE.md` / `GEMINI.md` / `.cursorrules`. **File an issue if not** — cross-tool support is what this project is for.

</details>

<details>
<summary><strong>How large can a skill get?</strong></summary>

<br>

**Hard cap: 3,000 tokens. CI fails the PR if you bloat.** Enforced via `tokens_target` in the frontmatter and `tools/validate_rules.py`. When it grows beyond that, split it. **Two precise modules beat one bloated one** — and your router loads them on demand.

</details>

<details>
<summary><strong>Can the agent really extend itself?</strong></summary>

<br>

**Yes — but only via PR, and the human always reviews.** The workflow in [`references/errors/self-extension-workflow.md`](./references/errors/self-extension-workflow.md) describes exactly how the agent formulates entries, classifies them, and opens a PR labelled `needs-rule-review`. CI lints it. A maintainer reviews and merges. **The agent never pushes to `main`.** That's the supply-chain discipline.

</details>

<details>
<summary><strong>What is the difference from <code>.cursorrules</code> or <code>AGENTS.md</code>?</strong></summary>

<br>

**We sit on top of them, not next to them.** `.cursorrules`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` are static rule files. Skill-everything adds: structured error schema (JSON-Schema), versioned skill manifest, `learn(errors)` PR workflow, CI validator, per-skill token budget. **One source of truth in `references/_index.yml`. Four loaders. Zero drift.**

</details>

<details>
<summary><strong>Do I need a database?</strong></summary>

<br>

**No.** Plain Markdown. Plain Git. That is it. **No vector DB, no embeddings, no running processes, no API key, no SaaS.** `git clone` is the entire setup.

</details>

<details>
<summary><strong>What if a rule turns out to be wrong?</strong></summary>

<br>

**`git revert`. Done.** Every change is versioned. Every rule has a commit SHA. **That's the entire point of the architecture.**

</details>

<details>
<summary><strong>Is this safe to run? The agent writes its own rules.</strong></summary>

<br>

That's the threat model spelled out in [SECURITY.md](./SECURITY.md). **We treat prompt-injection as a supply-chain problem, not a magic feature.** The CI validator catches obvious bad patterns (URLs, shell binaries, credential paths, base64 blobs, `<script>` tags). **It does not catch homoglyphs, indirection, or natural-language nudges** — see the [adversarial test suite](./tests/test_validate_rules_adversarial.py) where every known bypass is documented (current scoreline: **12 of 20 caught**, the other 8 are public). Human PR review is the primary trust boundary. Don't enable auto-merge on `references/errors/`. Use [`.github/CODEOWNERS`](./.github/CODEOWNERS) to require maintainer review on rule changes. **Defence-in-depth, not silver bullet.**

</details>

<details>
<summary><strong>How does this save tokens?</strong></summary>

<br>

See the [Token math](#token-math) section. Headline: **20–34% cheaper than uncached monolithic prompts; roughly break-even with cached at today's scale.** The architectural win is **flat per-message input cost as your skill library grows**. **We don't claim 84%.**

</details>

---

<div align="center">

<sub>MIT · plain Markdown · plain Git · reviewed in PRs</sub>

`LICENSE` · [Disclaimer](./DISCLAIMER.md) · [Contributing](./CONTRIBUTING.md) · [Security](./SECURITY.md) · [Browse the public error log →](./references/errors/error-log.md) · [Issue](https://github.com/sordi-ai/skill-everything/issues)

*Side project. Two engineers. Built on weekends. Dogfooded daily — the [error log](./references/errors/error-log.md) is public. [Not endorsed by any employer.](./DISCLAIMER.md)*

</div>
