<div align="center">

<sub>🧠 SELF-LEARNING · ⚡ TOKEN-EFFICIENT · 🚀 MULTI-AGENT</sub>

# skill-everything

### Never make the same mistake twice.

### The self-learning memory layer for AI agents — beyond fine-tuning.

**Self-extending skills in plain Markdown. Save tokens. Enhance quality. Ship smarter agents — across Claude Code, Cursor, Gemini CLI, and OpenCode.**

[![Release v1.0 STABLE](https://img.shields.io/badge/Release-v1.0_STABLE-success?style=for-the-badge&logo=git&logoColor=white)](./ROADMAP.md)
[![GitHub stars](https://img.shields.io/github/stars/sordi-ai/skill-everything?style=for-the-badge&logo=github&color=gold)](https://github.com/sordi-ai/skill-everything/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](./LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/sordi-ai/skill-everything?style=for-the-badge&color=green)](https://github.com/sordi-ai/skill-everything/commits/main)
[![Commit Activity](https://img.shields.io/github/commit-activity/m/sordi-ai/skill-everything?style=for-the-badge&color=brightgreen)](https://github.com/sordi-ai/skill-everything/commits/main)

[![Self-Learning](https://img.shields.io/badge/AI_Memory-Self--Learning-gold?style=for-the-badge)](./docs/how-it-works.svg)
[![Beyond Fine-Tuning](https://img.shields.io/badge/Beyond-Fine--Tuning-purple?style=for-the-badge&logo=anthropic)](./docs/architecture.svg)
[![Token Efficient](https://img.shields.io/badge/Tokens-84%25_Fewer-1f7a4a?style=for-the-badge&logo=lightning)](./docs/token-comparison.svg)
[![Quality Compounds](https://img.shields.io/badge/Quality-Compounds-ff6b35?style=for-the-badge)](./references/errors/error-log.md)

[![CI](https://img.shields.io/github/actions/workflow/status/sordi-ai/skill-everything/ci.yml?style=for-the-badge&label=CI&logo=githubactions&logoColor=white)](./.github/workflows/ci.yml)
[![Schemas](https://img.shields.io/badge/Schemas-JSON_Validated-blue?style=for-the-badge&logo=json)](./schemas/skill-manifest.json)
[![PR Reviewed](https://img.shields.io/badge/Updates-PR_Reviewed-darkblue?style=for-the-badge&logo=git)](./CONTRIBUTING.md)
[![Per-Skill Cap](https://img.shields.io/badge/Per--Skill_Cap-3K_Tokens-1f7a4a?style=for-the-badge)](./schemas/skill-manifest.json)

[![Claude Code](https://img.shields.io/badge/Works_With-Claude_Code-CC785C?style=for-the-badge&logo=anthropic&logoColor=white)](./CLAUDE.md)
[![Cursor](https://img.shields.io/badge/Works_With-Cursor-000000?style=for-the-badge&logo=cursor&logoColor=white)](#quick-start)
[![Gemini CLI](https://img.shields.io/badge/Works_With-Gemini_CLI-4285F4?style=for-the-badge&logo=google&logoColor=white)](./GEMINI.md)
[![OpenCode](https://img.shields.io/badge/Works_With-OpenCode-9333EA?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](./SKILL.md)

🚀 **One source of truth · Four agent runtimes · Zero re-authoring**
♻️ **Errors become commits · Commits become skills · Skills make agents smarter**

</div>

---

<div align="center">

### *Fine-tuning is frozen.*
### *RAG is blind.*
### *Your agent forgets everything tomorrow.*

### **What if it didn't?**

</div>

---

## THE PITCH IN 30 SECONDS
*Self-learning skills. One paragraph. One terminal command.*

**Self-learning skills — beyond fine-tuning.** Your domain knowledge, local, in one place, organised as composable sub-skills in plain Markdown, versioned in Git. The router loads only the matching sub-skill: ~800 tokens for the router, ~800 tokens for the sub-skill — **84 % fewer input tokens per message, $28 saved per 1,000 messages**. Add the 50th skill, the 200th skill — your per-message bill stays flat.

The same memory ships across **Claude Code, Cursor, Gemini CLI, and OpenCode** — generated from a single source of truth. **Same Markdown. Four agent runtimes. Zero re-authoring.** Self-extending and modular — your agent's domain knowledge compounds in `git`, not in opaque weights.

```bash
git clone https://github.com/sordi-ai/skill-everything.git
```

That is the entire setup. **Star this repo to ship smarter agents — beyond fine-tuning, beyond vector DBs, beyond black-box memory.**

> [!NOTE]
> **Built on top of the formats your tools already read.** Skill-everything generates `CLAUDE.md`, `.cursorrules`, `GEMINI.md`, and `AGENTS.md` from one `references/_index.yml` — same domain knowledge, four agent runtimes.

---

## WHY IT WINS
*Six reasons skill-everything is the new standard for agent memory.*

- **Cross-tool by design.** One source, four agent runtimes — `Claude Code`, `Cursor`, `Gemini CLI`, `OpenCode`. Generated from a single [`references/_index.yml`](./references/_index.yml), drift-checked in CI on every PR. **Same domain knowledge, four runtimes, zero re-authoring.**
- **Beyond fine-tuning.** Domain knowledge compounds in plain Markdown — `git diff`-able, screenshot-shareable, instantly auditable. Your agent's brain lives in [`references/`](./references/), **versioned in Git, not in opaque weights**.
- **Self-extending memory.** Every accepted change makes the next session smarter. `git log --grep="learn("` is your agent's growth trail. **Quality compounds — commit by commit, automatically.**
- **84 % fewer input tokens. $28 saved per 1,000 messages.** Per-skill 3k-token cap, CI-enforced by [`tools/validate_rules.py`](./tools/validate_rules.py). The router loads only the matching sub-skill. **Add the 50th skill, the 200th skill — your per-message bill stays flat.**
- **Modular by design.** Composable sub-skills, hot-loaded on demand. Domain knowledge — local, in one place, organised by trigger. **The library grows; per-message cost doesn't.**
- **Drop-in compatible with the agent ecosystem.** `CLAUDE.md`, `.cursorrules`, `GEMINI.md`, and `AGENTS.md` are all generated from the same source. **Works with the formats your tools already read — today.**

---

## HOW IT WORKS
*Six steps. One self-extending loop. Same Markdown across four agent runtimes.*

<picture>
  <source media="(max-width: 600px)" srcset="./docs/how-it-works-mobile.svg">
  <img src="./docs/how-it-works.svg" alt="The self-extension loop — six steps from agent trigger to merged rule, with three serial CI gates">
</picture>

*Trigger → Analyse → Formulate → PR → Lint → Merge. **The system catches every signal the agent picks up — errors, deployment gotchas, naming conventions, domain shorthand — and turns it into a versioned, schema-validated rule that ships to all four runtimes automatically.***

> [!NOTE]
> **CI-validated, schema-checked, drift-detected.** Every rule passes `lint-rules` + `auto-approve-rule-pr` before landing in `main` — JSON-Schema-validated, verb-allow-listed, fully auditable. [SECURITY.md](./SECURITY.md) has the trust model.

---

## ARCHITECTURE
*One register. Four loaders. Same sub-skills across four agent runtimes.*

[`references/_index.yml`](./references/_index.yml) is the **single source of truth**. Every sub-skill is declared once with its `id`, `tokens_target`, `triggers`, and load order. From it, [`tools/render_loaders.py`](./tools/render_loaders.py) regenerates **four loader files**: `SKILL.md` (OpenCode), `CLAUDE.md` (Claude Code), `GEMINI.md` (Gemini CLI), and `.cursorrules` (Cursor). **Edit the index, regenerate, done.**

A CI no-drift job runs `git diff --exit-code` against the regenerated loaders on every PR — **the four runtimes stay in lockstep, automatically**. One source updates them all.

![Architecture — _index.yml as master, render_loaders.py as generator, four loaders rendering the same sub-skill directory](./docs/architecture.svg)

*One source of truth. Four loaders. Zero drift.*

> [!NOTE]
> **CI-enforced single-source-of-truth.** `loaders-no-drift` validates that every regenerated loader matches its source on every commit — the four-runtime ecosystem stays in lockstep, automatically.

---

## SELF-EXTENSION
*Self-learning skills — every commit makes the next session smarter.*

The agent doesn't just *use* the skill set — it **grows it**. Trigger → search → analyse → formulate → PR. **The system catches repeats automatically. Quality compounds, commit by commit.**

![Real error log entries — ERR-2026-001 (TypeScript strictNullChecks disabled, derived rule: never disable strict checks for convenience), ERR-2026-007 (refactor missed 4 imports after rename, REPEAT CAUGHT · COUNT 1 → 2, auto-merged into existing entry as self-extension trust proof, derived rule: after any rename run a project-wide grep), ERR-2026-012 (migration ran after backend deploy and broke prod, derived rule: always order migrations before backend deploy in domain runbooks). Each entry links a real commit SHA. The system catches repeats — quality compounds, automatically.](./docs/error-log.svg)

`learn(errors):` is a commit-type that triggers `lint-rules` CI and validates every proposed rule against [`schemas/error-entry.json`](./schemas/error-entry.json) — a JSON-Schema with verb allow-list and pattern guards.

```text
$ git log --grep="learn("
learn(errors): ERR-2026-001 — never disable strict checks for convenience
learn(errors): ERR-2026-007 — grep before claiming a rename complete  (count 1 → 2)
learn(errors): ERR-2026-012 — order migrations before backend deploys
```

**The full self-extension workflow** — including the CI gate, the `auto-approve-rule-pr` policy, and the schema-validated rule grammar — lives in [`references/errors/self-extension-workflow.md`](./references/errors/self-extension-workflow.md).

[**Browse the full public error log →**](./references/errors/error-log.md) — every mistake captured and every rule derived, in plain Markdown.

---

## MEMORY TO GO
*Switch tools. Your skills come with.*

**Take your skills anywhere.** Your self-learning sub-skills live once in [`references/_index.yml`](./references/_index.yml) and travel with you across four agent runtimes — `Claude Code`, `Cursor`, `Gemini CLI`, `OpenCode` — with **zero re-authoring**.

[`tools/render_loaders.py`](./tools/render_loaders.py) deterministically generates `CLAUDE.md`, `.cursorrules`, `GEMINI.md`, and `SKILL.md` from the same index. Switch from a Claude Code session to Gemini CLI mid-project and your **composable sub-skills, your error log, your self-extension workflow are already loaded** — identical, token-capped, schema-validated. **No sync layer. No API lock-in. No proprietary memory store.**

This is portable agent memory done the boring way: plain Markdown, git-versioned, CI-gated. **Beyond fine-tuning, beyond vector DBs, beyond black-box memory.** **One source. Four runtimes. Memory follows you.**

![Memory to GO — switch tools, skills come with. Your sub-skills live once in references/_index.yml and travel with you across Claude Code, Cursor, Gemini CLI, and OpenCode with zero re-authoring.](./docs/memory-to-go.svg)

---

## TOKEN MATH
*Same task. Same agent. **84% fewer input tokens.** Add a skill, pay nothing extra.*

![Token comparison — monolithic ships the whole rulebook every turn (10,000+ tokens), skill-everything ships a router plus one sub-skill (~1,600 tokens), 84% less per message](./docs/token-comparison.svg)

**The single-message punch:** monolithic prompts load `.cursorrules` *every turn, all of it*. Skill-everything loads the router (`SKILL.md`, ~800 tokens) plus exactly one sub-skill on demand (~800 tokens). Same task, same agent, **84 % fewer input tokens per message**.

![Token-math chart — monolithic prompts grow with skill count, skill-everything stays flat](./docs/token-math.svg)

**The scaling promise:** monolithic prompts grow linearly with your skill library — every user, every message, every skill. Skill-everything stays flat as the library grows from 1 to 50 skills.

![Cost per 1,000 messages — five setups, one winner: monolithic uncached $75 (painful baseline), monolithic with caching $48, skill-everything 2-3 sub-skills $55, skill-everything single sub-skill $50, skill-everything with caching $47 (winner). $28 saved per 1,000 messages, 37% cheaper than the painful baseline.](./docs/cost-comparison.svg)

**The bottom line:** **`$47` with caching beats the `$75` painful baseline** — that's **`$28` saved per 1,000 messages**, **37 %** cheaper than uncached monolithic. And the architectural win **compounds**: at 30, 90, 200 skills, monolithic explodes — skill-everything stays flat. **Caching helps both. Only one of the two stays flat as your library grows.**

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

*Numbers auto-updated by `python tools/render_readme_table.py` and CI-validated on every PR — every count is real, every total is reproducible.*

</details>

---

## SELF-HOSTED & SMALLER MODELS
*The smaller your model, the bigger the win.*

Skill-everything's router pattern is **custom-made for self-hosted and quantized models** — `Ollama`, `llama.cpp`, `vLLM`, `LM Studio`, `MLX`, and every local runtime in between. When the context window is **8k** and there's no Anthropic prompt-caching layer, **token efficiency stops being a nice-to-have and becomes the difference between shipping and not**.

- **8k context fits.** A 10,000-token monolithic `.cursorrules` doesn't even load on a Llama 3 8B. Skill-everything's ~1,600-token footprint runs comfortably on **8k, 16k, or 32k** windows — with room left for the actual conversation, tool calls, and reasoning.
- **No caching tax.** Cloud monolithic prompts lean on Anthropic prompt-caching to stay competitive. **Local models have no caching layer** — every token is paid in compute time and VRAM pressure. Skill-everything's flat per-message footprint translates directly into **faster inference, lower thermal pressure, fewer OOMs**.
- **Sharper needle-in-haystack.** Smaller models lose accuracy fast as context grows. Loading exactly the matched sub-skill puts the **relevant rule on top, where the model can actually use it** — the difference between a hallucinated convention and a clean call.
- **Self-hosted by design.** Plain Markdown, no SaaS, no API key, no vector DB. Drops into any local runtime — **your domain knowledge stays on your hardware, your agents stay private**.

![Self-hosted & smaller models — context-window comparison shows monolithic 10,000+ tokens overflowing the 8k Llama 3 8B window, while skill-everything's ~1,600-token footprint fits comfortably with ~6,400 tokens of headroom for conversation, tool calls, and reasoning. Plus four facts (8k fits, no caching tax, sharper needle, self-hosted) and a fan-out from skill-everything to five local runtimes: Ollama, llama.cpp, vLLM, LM Studio, MLX. The smaller your model, the bigger the win.](./docs/self-hosted-models.svg)

**Built for every model. Best on the small ones.**

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

## CAPABILITY MATRIX

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/comparison.svg">
  <img alt="Capability matrix: skill-everything carries 9 of 9 capabilities (plain Markdown no database · git-versioned · cross-tool portable · per-skill 3k-token cap CI-enforced · schema-validated rule entries · versioned skill-manifest frontmatter · self-extending via PR · skill-router auto-loads on trigger · audit trail in git history) plus a one-command `git clone` setup. AGENTS.md carries 3 of 9; Cursor Rules 2 of 9; mem0 / MemGPT 1 of 9 and requires API key, SaaS, vector DB and embeddings to install." src="docs/comparison.svg" width="100%">
</picture>

<sub>Capabilities sourced from each project's documentation as of 2026-05. <code>✓</code> supported&nbsp;·&nbsp;<code>◐</code> partial&nbsp;·&nbsp;<code>✗</code> missing&nbsp;·&nbsp;<code>n/a</code> not applicable. AGENTS.md and Cursor Rules are siblings — skill-everything sits on top of them and adds the review and validation layers. mem0 / MemGPT solves a different problem (long-running embedded recall); if that's your problem, use mem0.</sub>

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

## VERSIONS

> **`v1.0` is stable and released.** New features land in `main` via PR — watch the repo to see them ship.

| Version | Status | What |
|---|:---:|---|
| **`v1.0` — Foundation** | 🟢 **STABLE** | `lint-rules` CI · JSON-Schema validator · XSS hardening · single-source-of-truth loader sync · `learn(errors):` PR convention · CODEOWNERS + branch protection · 9 sub-skills shipped · 5 production diagrams · adversarial test suite. **You're using it now.** |
| **`v1.1` — Eval that earns the claim** | 🟡 In development | Eval-framework MVP for re-mistake rate · methodology contract (n ≥ 30, multi-model, prompt hash pinned) · 30 days of real errors logged from production usage · published benchmark numbers. |
| **`v1.2` — Community ecosystem** | 🔵 Planned | First external sub-skills merged (Go, Rust, Java, TypeScript) · sub-skill PR template institutionalised · public skill catalogue with usage stats · `learn(errors):` going wild on a public commit graph. |
| **`v2.0` — Marketplace + trust layer** | ⚪ Vision | Signed skills with reputation graph · sandboxed execution · semantic versioning · license management · cross-repo skill imports. The skill library becomes a public dataset others ship on top of. |

*Feature requests and roadmap updates land as PRs against [`ROADMAP.md`](./ROADMAP.md) in `main` — same loop as the rest of the repo: every change is a commit, every commit is reviewed, every release is auditable.*

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

See the [Token math](#token-math) section. **Same task, same agent: 84% fewer input tokens** (`10,000+` monolithic vs `~1,600` skill-everything per message). At cost level: **`$28` saved per 1,000 messages, 37% cheaper than the painful baseline**. The architectural win is **flat per-message input cost as your skill library grows** — caching helps both, but only one stays flat.

</details>

---

<div align="center">

<sub>MIT · plain Markdown · plain Git · v1.0 STABLE</sub>

`LICENSE` · [Disclaimer](./DISCLAIMER.md) · [Contributing](./CONTRIBUTING.md) · [Security](./SECURITY.md) · [Browse the public error log →](./references/errors/error-log.md) · [Issue](https://github.com/sordi-ai/skill-everything/issues)

*Self-learning skills · beyond fine-tuning · same Markdown across four agent runtimes.*

</div>
