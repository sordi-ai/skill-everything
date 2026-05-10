<div align="center">

<sub>🧠 SELF-LEARNING · ⚡ SAVE TOKENS · 🚀 SKILLS TO GO · ✨ QUALITY COMPOUNDS</sub>

# skill-everything

### The memory layer for AI agents — self-learning instead of fine-tuning.

### **84 % fewer input tokens · `$28` saved per 1,000 messages · same Markdown across four agent runtimes.**

<sub>* in Claude Code & OpenCode (selective sub-skill loading); Cursor & Gemini CLI realise a smaller share through the compact router — see [Per-tool token reality](#per-tool-token-reality). Cost vs. 10k-token monolithic baseline at Sonnet-class pricing.</sub>

### Never make the same mistake twice.

**Self-extending skills in plain Markdown. Save tokens. Enhance quality. Ship smarter agents — across Claude Code, Cursor, Gemini CLI, and OpenCode.**

[![Release v1.0 STABLE](https://img.shields.io/badge/Release-v1.0_STABLE-success?style=for-the-badge&logo=git&logoColor=white)](./ROADMAP.md)
[![GitHub stars](https://img.shields.io/github/stars/sordi-ai/skill-everything?style=for-the-badge&logo=github&color=gold)](https://github.com/sordi-ai/skill-everything/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](./LICENSE)

[![CI](https://img.shields.io/github/actions/workflow/status/sordi-ai/skill-everything/ci.yml?style=for-the-badge&label=CI&logo=githubactions&logoColor=white)](./.github/workflows/ci.yml)
[![Schemas](https://img.shields.io/badge/Schemas-JSON_Validated-blue?style=for-the-badge&logo=json)](./schemas/skill-manifest.json)
[![Per-Skill Cap](https://img.shields.io/badge/Per--Skill_Cap-3K_Tokens-1f7a4a?style=for-the-badge)](./schemas/skill-manifest.json)

[![Claude Code](https://img.shields.io/badge/Works_With-Claude_Code-CC785C?style=for-the-badge&logo=anthropic&logoColor=white)](./CLAUDE.md)
[![Cursor](https://img.shields.io/badge/Works_With-Cursor-000000?style=for-the-badge&logo=cursor&logoColor=white)](./.cursorrules)
[![Gemini CLI](https://img.shields.io/badge/Works_With-Gemini_CLI-4285F4?style=for-the-badge&logo=google&logoColor=white)](./GEMINI.md)
[![OpenCode](https://img.shields.io/badge/Works_With-OpenCode-9333EA?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](./SKILL.md)

🚀 **One source of truth · Four agent runtimes · Zero re-authoring**
♻️ **Errors become commits · Commits become skills · Skills make agents smarter**

</div>

---

<div align="center">

### *Your agent forgets everything tomorrow.*

### **What if it didn't?**

### *Now it doesn't.* **Self-learning, by design.**

</div>

<picture>
  <source media="(max-width: 600px)" srcset="./docs/how-it-works-mobile.svg">
  <img src="./docs/how-it-works.svg" alt="The complete agent-memory stack — five agent steps from trigger to merged rule, three CI gates (lint-rules, auto-approve-rule-pr, drift-check), one self-extending loop. Every commit makes the next session smarter across Claude Code, Cursor, Gemini CLI, and OpenCode.">
</picture>

---

## THE PITCH
*Selbstlernend · Token sparen · Skills to GO · Qualität die compoundet.*

**Self-learning skills for AI agents.** **Beyond fine-tuning, beyond vector DBs, beyond black-box memory.** Your domain knowledge — local, in plain Markdown, versioned in Git, hot-loaded as composable sub-skills.

⚡ **Save tokens.** 84 % fewer input tokens. $28 saved per 1,000 messages. Per-message bill stays flat as your library grows.

🚀 **Skills to GO.** Same Markdown across `Claude Code`, `Cursor`, `Gemini CLI`, `OpenCode`. Switch tools — your skills come with.

✨ **Quality compounds.** Every commit makes the next session smarter. Automatically.

```bash
git clone https://github.com/sordi-ai/skill-everything.git
```

**Star this repo to ship smarter agents.**

> [!NOTE]
> **Drop-in compatible.** Generates `CLAUDE.md`, `.cursorrules`, `GEMINI.md`, and `SKILL.md` from one `skills/_index.yml` — same domain knowledge, four agent runtimes.

---

## WHY IT WINS
*Six reasons skill-everything is the new standard for agent memory.*

- **Cross-tool by design.** One source, four agent runtimes — `Claude Code`, `Cursor`, `Gemini CLI`, `OpenCode`. Generated from a single [`skills/_index.yml`](./skills/_index.yml), drift-checked in CI on every PR. **Same domain knowledge, four runtimes, zero re-authoring.**
- **Beyond fine-tuning.** Domain knowledge compounds in plain Markdown — `git diff`-able, screenshot-shareable, instantly auditable. Your agent's brain lives in [`skills/`](./skills/), **versioned in Git, not in opaque weights**.
- **Self-extending memory.** Every accepted change makes the next session smarter. `git log --grep="learn("` is your agent's growth trail. **Quality compounds — commit by commit, automatically.**
- **84 % fewer input tokens. $28 saved per 1,000 messages.** Per-skill 3k-token cap, CI-enforced by [`tools/validate_rules.py`](./tools/validate_rules.py). On Claude Code & OpenCode the router loads only the matching sub-skill; on Cursor & Gemini CLI the saving comes from the compact router pattern (full breakdown in [Per-tool token reality](#per-tool-token-reality)). **Add the 50th skill, the 200th skill — your per-message bill stays flat where the runtime supports lazy loading.**
- **Modular by design.** Composable sub-skills, hot-loaded on demand. Domain knowledge — local, in one place, organised by trigger. **The library grows; per-message cost doesn't.**
- **Drop-in compatible with the agent ecosystem.** `CLAUDE.md`, `.cursorrules`, `GEMINI.md`, and `SKILL.md` are all generated from the same source. **Works with the formats your tools already read — today.**

---

## ARCHITECTURE
*One register. Four loaders. Same sub-skills across four agent runtimes.*

[`skills/_index.yml`](./skills/_index.yml) is the **single source of truth**. Every sub-skill is declared once with its `id`, `tokens_target`, `triggers`, and load order. From it, [`tools/render_loaders.py`](./tools/render_loaders.py) regenerates **four loader files**: `SKILL.md` (OpenCode), `CLAUDE.md` (Claude Code), `GEMINI.md` (Gemini CLI), and `.cursorrules` (Cursor). **Edit the index, regenerate, done.**

A CI no-drift job runs `git diff --exit-code` against the regenerated loaders on every PR — **the four runtimes stay in lockstep, automatically**. One source updates them all.

![Architecture — skills/_index.yml as master, render_loaders.py as generator, four loaders rendering the same sub-skill directory](./docs/architecture.svg)

*One source of truth. Four loaders. Zero drift.*

> [!NOTE]
> **CI-enforced single-source-of-truth.** `loaders-no-drift` validates that every regenerated loader matches its source on every commit — the four-runtime ecosystem stays in lockstep, automatically.

---

## TOKEN MATH
*Same task. Same agent. **84% fewer input tokens.** Add a skill, pay nothing extra.*

![Token comparison — monolithic ships the whole rulebook every turn (10,000+ tokens), skill-everything ships a router plus one sub-skill (~1,600 tokens), 84% less per message](./docs/token-comparison.svg)

**The single-message punch:** monolithic prompts load `.cursorrules` *every turn, all of it*. With selective sub-skill loading (Claude Code, OpenCode), skill-everything loads the router (~800 tokens) plus exactly one sub-skill on demand (~800 tokens) — **84 % fewer input tokens per message**. On Cursor & Gemini CLI the router itself is the saving today (see [Per-tool token reality](#per-tool-token-reality)).

![Token-math chart — monolithic prompts grow with skill count, skill-everything stays flat](./docs/token-math.svg)

**The scaling promise:** monolithic prompts grow linearly with your skill library — every user, every message, every skill. Skill-everything stays flat as the library grows from 1 to 50 skills.

![Cost per 1,000 messages — five setups, one winner: monolithic uncached $75 (painful baseline), monolithic with caching $48, skill-everything 2-3 sub-skills $55, skill-everything single sub-skill $50, skill-everything with caching $47 (winner). $28 saved per 1,000 messages, 37% cheaper than the painful baseline.](./docs/cost-comparison.svg)

**The bottom line:** **`$47` with caching beats the `$75` painful baseline** — that's **`$28` saved per 1,000 messages**, **37 %** cheaper than uncached monolithic. And the architectural win **compounds**: at 30, 90, 200 skills, monolithic explodes — skill-everything stays flat. **Caching helps both. Only one of the two stays flat as your library grows.**

![Multi-LLM token-cost comparison across four cloud providers — Sonnet 4.5 ($75 → $47, $28 saved, 37% cheaper), Opus 4.7 ($375 → $226, $149 saved, 40% cheaper), Kimi 2.6 ($11 → $6.40, $4.60 saved, 42% cheaper), GPT-4o ($55 → $33, $22 saved, 40% cheaper). The 84% input-token reduction is constant across all four providers — same architecture, same ratio, every provider. Total: $203.60 saved per 1,000 messages across the 4-provider mix.](./docs/multi-llm-cost.svg)

**Same architecture, every provider.** The 84 % input-token reduction is **architectural**, not pricing-conditional — switch from Sonnet to Opus, Kimi, or GPT-4o, the ratio stays. Per-message dollar amount scales with the provider tier; the proportional saving doesn't.

### Per-tool token reality
*The 84 % is architectural — it requires selective sub-skill loading. Here's what each runtime actually does today.*

| Runtime | Selective loading | Realised reduction | Why |
|---|:---:|:---:|---|
| **Claude Code** | ✅ Native (`@skills/<name>/SKILL.md`) | **~84 %** | Router (`CLAUDE.md`) auto-discovers, `@-imports` lazy-load exactly the matching sub-skill. |
| **OpenCode** | ✅ Native (`skill_resource()`) | **~80–84 %** | Skill auto-discovery + native loader pulls one sub-skill on demand; per-turn footprint matches Claude Code. |
| **Cursor** | ⚠️ Build-dependent | **~30–50 %** | `.cursorrules` ships every turn (router + trigger table). `@file:` references load only on newer builds; on older builds the saving is the compact router itself. |
| **Gemini CLI** | ❌ Not yet | **~20–30 %** | `GEMINI.md` ships every turn; `@skills/<name>/SKILL.md` is Anthropic-specific syntax. The saving is the compact router; sub-skills must be inlined or pasted manually for true lazy loading. |

**Takeaway.** The architectural win is **identical** across all four runtimes — same sub-skills, same source of truth, same drift-checked CI. The **realisation** depends on what the runtime supports today: full lazy loading on Claude Code & OpenCode, compact-router savings on Cursor & Gemini CLI. Plain Markdown works everywhere; the loader maturity catches up over time.

<details>
<summary><strong>Per-skill token budgets — real tiktoken counts, CI-validated</strong></summary>

<br>

<!-- token-table:start -->

| Sub-skill | Path | Tokens (real, tiktoken cl100k) |
|---|---|---:|
| `code-quality` | `skills/code-quality/SKILL.md` | ~1,000 |
| `python` | `skills/python/SKILL.md` | ~1,600 |
| `typescript` | `skills/typescript/SKILL.md` | ~1,900 |
| `react` | `skills/react/SKILL.md` | ~1,800 |
| `git-conventions` | `skills/git-conventions/SKILL.md` | ~550 |
| `review-deployment` | `skills/review-deployment/SKILL.md` | ~650 |
| `domain-template` | `skills/domain-template/SKILL.md` | ~900 |
| `error-log` | `skills/error-log/SKILL.md` | ~2,050 |
| `self-extension-workflow` | `skills/self-extension-workflow/SKILL.md` | ~1,850 |
| **Total if all loaded** | — | **~12,500** |
| **Typical (router + 1–2 skills)** | depends on task | **~1,800–3,500** |

<!-- token-table:end -->

*Numbers auto-updated by `python tools/render_readme_table.py` and CI-validated on every PR — every count is real, every total is reproducible.*

</details>

---

## HOW IT WORKS
*Five agent steps, three CI gates, one self-extending loop. Same Markdown across four agent runtimes.*

*Trigger → Analyse → Formulate → PR → Lint → Merge. **The system catches every signal the agent picks up — errors, deployment gotchas, naming conventions, domain shorthand — and turns it into a versioned, schema-validated rule that ships to all four runtimes automatically.*** *(See the self-extension-loop diagram in the hero block above.)*

> [!NOTE]
> **CI-validated, schema-checked, drift-detected.** Every rule passes `lint-rules` + `auto-approve-rule-pr` before landing in `main` — JSON-Schema-validated, verb-allow-listed, fully auditable. [SECURITY.md](./SECURITY.md) has the trust model.

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

**The full self-extension workflow** — including the CI gate, the `auto-approve-rule-pr` policy, and the schema-validated rule grammar — lives in [`skills/self-extension-workflow/SKILL.md`](./skills/self-extension-workflow/SKILL.md).

[**Browse the full public error log →**](./skills/error-log/SKILL.md) — every mistake captured and every rule derived, in plain Markdown.

---

## MEMORY TO GO
*Switch tools. Your skills come with.*

**Take your skills anywhere.** Your self-learning sub-skills live once in [`skills/_index.yml`](./skills/_index.yml) and travel with you across four agent runtimes — `Claude Code`, `Cursor`, `Gemini CLI`, `OpenCode` — with **zero re-authoring**.

[`tools/render_loaders.py`](./tools/render_loaders.py) deterministically generates `CLAUDE.md`, `.cursorrules`, `GEMINI.md`, and `SKILL.md` from the same index. Switch from a Claude Code session to Gemini CLI mid-project and your **composable sub-skills, your error log, your self-extension workflow are already loaded** — identical, token-capped, schema-validated. **No sync layer. No API lock-in. No proprietary memory store.**

This is portable agent memory done the boring way: plain Markdown, git-versioned, CI-gated. **Beyond fine-tuning, beyond vector DBs, beyond black-box memory.** **One source. Four runtimes. Memory follows you.**

![Memory to GO — switch tools, skills come with. Your sub-skills live once in skills/_index.yml and travel with you across Claude Code, Cursor, Gemini CLI, and OpenCode with zero re-authoring.](./docs/memory-to-go.svg)

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
@skills/code-quality/SKILL.md
@skills/error-log/SKILL.md
```

</details>

<details>
<summary><strong>Gemini CLI</strong> — auto-discovers <code>GEMINI.md</code></summary>

<br>

Same as above. Use `/memory show` to verify the loaded context. Use `/memory refresh` after edits.

> **Token reality.** Gemini CLI loads `GEMINI.md` whole — the `@skills/<name>/SKILL.md` import syntax is Anthropic-specific and is read as literal text. The token saving comes from the compact router (~800 tokens) versus a 10k-token monolithic rule-book; sub-skills inline manually for true lazy loading. See [Per-tool token reality](#per-tool-token-reality).

</details>

<details>
<summary><strong>Cursor</strong> — auto-discovers <code>.cursorrules</code></summary>

<br>

Cursor reads `.cursorrules` automatically when the file sits at your project root. **Either commit our generated [`.cursorrules`](./.cursorrules) next to your code**, or for older Cursor builds paste `SKILL.md` content into **Settings → Rules for AI**. Same Markdown, either way.

> **Token reality.** Cursor reads `.cursorrules` whole every turn; selective sub-skill loading via `@file:` is build-dependent — newer builds resolve the reference, older builds treat it as text. The token saving comes from the compact router; on builds without `@file:` resolution there is no on-demand sub-skill loop. See [Per-tool token reality](#per-tool-token-reality).

</details>

<details>
<summary><strong>OpenCode</strong> — symlink <code>SKILL.md</code> to a skills directory</summary>

<br>

OpenCode auto-discovers skills in standard locations:

- `.opencode/skills/skill-everything/SKILL.md` (project-local)
- `~/.config/opencode/skills/skill-everything/SKILL.md` (user-global)
- `.claude/skills/skill-everything/SKILL.md` (shared with Claude Code)
- `.agents/skills/skill-everything/SKILL.md` (shared cross-tool)

Either symlink the repo's `SKILL.md` to one of these paths or copy it, then load it from any agent prompt via the native `skill({ name: "skill-everything" })` tool. The router (`SKILL.md`) auto-loads the matching sub-skill from the trigger table.

The frontmatter (`name`, `description`, `license`, `compatibility`, `metadata`) matches OpenCode's recognised fields; additional fields are ignored.

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
├── .cursorrules                   # Router for Cursor (generated)
├── DISCLAIMER.md                  # Independent project, no employer endorsement
├── SECURITY.md                    # Threat model + responsible-disclosure
├── skills/                        # Anthropic Skills layout (one folder per sub-skill)
│   ├── _index.yml                 # Single source of truth for the routers
│   ├── _template/SKILL.md         # Copy this folder to start a new skill
│   ├── code-quality/SKILL.md      #   23 generic rules
│   ├── python/SKILL.md            #   20 Python-specific rules
│   ├── typescript/SKILL.md        #   17 TypeScript rules
│   ├── react/SKILL.md             #   17 React rules
│   ├── git-conventions/SKILL.md   # commit, branch, PR conventions
│   ├── review-deployment/SKILL.md # review + deployment checklists
│   ├── domain-template/SKILL.md   # template for project-specific knowledge
│   ├── error-log/
│   │   ├── SKILL.md               # YAML entries (validated by CI)
│   │   ├── exceptions.yml         # Forbidden-pattern bypass list
│   │   └── _entry-template.md     # Error entry template
│   └── self-extension-workflow/SKILL.md  # Six-step self-extension procedure
├── schemas/
│   ├── error-entry.json           # JSON-Schema for log entries
│   └── skill-manifest.json        # JSON-Schema for sub-skill frontmatter
├── tools/
│   ├── validate_rules.py          # CI lint: schema + verb allow-list
│   ├── render_loaders.py          # Regenerates SKILL/CLAUDE/GEMINI/.cursorrules from _index.yml
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
cp -r skills/_template skills/<your-skill-name>
$EDITOR skills/<your-skill-name>/SKILL.md
# Update frontmatter (name matching dir, description, version, tokens_target, triggers), fill in rules, open a PR.
```

Each sub-skill has a [skill-manifest frontmatter block](./schemas/skill-manifest.json) declaring its `name` (matching the directory), `description`, `version`, `tokens_target`, `triggers`, and load order. CI validates the frontmatter on every PR. **Keep each skill under 3,000 tokens.** Split rather than bloat. Rules are action directives, not descriptions.

---

## VERSIONS

> **`v1.0` is stable and released.** New features land in `main` via PR — watch the repo to see them ship.

| Version | Status | What |
|---|:---:|---|
| **`v1.0` — Foundation** | 🟢 **STABLE** | `lint-rules` CI · JSON-Schema validator · XSS hardening · single-source-of-truth loader sync · `learn(errors):` PR convention · CODEOWNERS + branch protection · 9 sub-skills shipped · 5 production diagrams · adversarial test suite. **You're using it now.** |
| **`v1.1` — Eval that earns the claim** | 🟡 In development | Eval-framework MVP for re-mistake rate · methodology contract (n ≥ 30, multi-model, prompt hash pinned) · 30 days of real errors logged from production usage · published benchmark numbers. |
| **`v1.2` — Community ecosystem** | 🔵 Planned | First external sub-skills merged (Go, Rust, Java, Swift) · sub-skill PR template institutionalised · public skill catalogue with usage stats · `learn(errors):` going wild on a public commit graph. |
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

**Yes — every change ships as a CODEOWNERS-gated PR.** The workflow in [`skills/self-extension-workflow/SKILL.md`](./skills/self-extension-workflow/SKILL.md) describes exactly how the agent formulates entries, classifies them, and opens a PR labelled `needs-rule-review`. CI runs the deterministic validator (verb allow-list + schema + forbidden-pattern set), then CODEOWNERS approval is required. **The agent never pushes to `main`.** Standard version-control discipline applied to rule learning.

</details>

<details>
<summary><strong>What is the difference from <code>.cursorrules</code> or <code>AGENTS.md</code>?</strong></summary>

<br>

**We sit on top of them, not next to them.** `.cursorrules`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` are static rule files. Skill-everything adds: structured error schema (JSON-Schema), versioned skill manifest, `learn(errors)` PR workflow, CI validator, per-skill token budget. **One source of truth in `skills/_index.yml`. Four loaders. Zero drift.**

</details>

<details>
<summary><strong>Do I need a database?</strong></summary>

<br>

**No.** **Plain Markdown, plain Git** — local-first, version-controlled, owned by you. `git clone` is the entire setup.

</details>

<details>
<summary><strong>What if a rule turns out to be wrong?</strong></summary>

<br>

**`git revert`. Done.** Every change is versioned. Every rule has a commit SHA. **That's the entire point of the architecture.**

</details>

<details>
<summary><strong>Is this safe to run? The agent writes its own rules.</strong></summary>

<br>

See [SECURITY.md](./SECURITY.md) for the full threat model. **Defense-in-depth via deterministic validation:** the CI validator catches structurally bad patterns (URLs, shell binaries, credential paths, base64 blobs, `<script>` tags) and the [adversarial test suite](./tests/test_validate_rules_adversarial.py) covers documented bypass attempts. [`.github/CODEOWNERS`](./.github/CODEOWNERS) enforces required approval on `skills/error-log/` so every rule change goes through review.

</details>

<details>
<summary><strong>How does this save tokens?</strong></summary>

<br>

The saving depends on what the runtime supports — see [Per-tool token reality](#per-tool-token-reality) for the per-runtime breakdown.

- **Claude Code & OpenCode** realise the full **~84 %** reduction through selective sub-skill loading (`@skills/<name>/SKILL.md` and `skill_resource()`): router (~800 tokens) + one matched sub-skill on demand vs `10,000+` monolithic — **`$28` saved per 1,000 messages**.
- **Cursor & Gemini CLI** save **~20–50 %** through the compact router pattern; lazy on-demand sub-skill loading is build-dependent (Cursor) or not yet supported (Gemini CLI), so the architectural win is partial today.

The architectural lever — **flat per-message input cost as the library grows** — applies in full where the runtime supports it, and partially where it doesn't. Plain Markdown stays portable across all four runtimes; loader maturity catches up over time.

</details>

---

<div align="center">

<sub>MIT · plain Markdown · plain Git · v1.0 STABLE</sub>

`LICENSE` · [Disclaimer](./DISCLAIMER.md) · [Contributing](./CONTRIBUTING.md) · [Security](./SECURITY.md) · [Browse the public error log →](./skills/error-log/SKILL.md) · [Issue](https://github.com/sordi-ai/skill-everything/issues)

*Self-learning skills · beyond fine-tuning · same Markdown across four agent runtimes.*

</div>
