<div align="center">

# 🧠 Skill-Everythink

### Agents that never make the same mistake twice.

**A Git-versioned memory system for AI coding agents — plain Markdown, zero infrastructure.**

<br>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/sordi-ai/skill-everything?style=social)](https://github.com/sordi-ai/skill-everything)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)

</div>

---

## 🤔 The Problem

Fine-tuning is expensive, slow, and produces a frozen model that stops learning the moment training ends. RAG solves the knowledge problem but demands vector infrastructure, embeddings, and ongoing maintenance. Cursor Rules are static, unversioned, and locked to a single tool. Systems like mem0 or MemGPT are powerful but opaque — you never know what was stored, why, or how it shapes behavior.

The core problem is the same everywhere: **no agent learns from its mistakes.** The same error happens tomorrow — in a different project, with a different user, on a different machine.

---

## ✅ The Solution

Skill-Everythink is a Git-versioned memory system built entirely from plain Markdown files:

- **Plain Markdown** — no database, no framework, no lock-in
- **Git-versioned** — every change is traceable, revertable, and reviewable
- **Error memory** — mistakes are analyzed, turned into rules, and stored permanently
- **Domain knowledge** — company processes, conventions, and partner quirks flow in structurally
- **Agent-agnostic** — works with OpenCode, Claude Code, Gemini CLI, Cursor, and any LLM-based agent
- **Modular** — sub-skills are independent, composable, and individually loadable
- **Zero setup** — `git clone` and you're done, no infrastructure required
- **Transparent** — anyone can read exactly what the agent knows and why

---

## 🚀 Quick Start

**Step 1 — Clone the repository**

```bash
git clone https://github.com/sordi-ai/skill-everything.git
```

**Step 2 — Load the skill into your agent**

<details>
<summary><strong>OpenCode</strong> — via <code>opencode.json</code> or skill path</summary>

```json
{
  "skills": ["./skill-everythink/SKILL.md"]
}
```

The `skill_resource` tool lets the agent load individual sub-skills on demand without bloating the context window.

</details>

<details>
<summary><strong>Claude Code</strong> — via <code>CLAUDE.md</code> and <code>@file</code> imports</summary>

Add to your project's `CLAUDE.md`:

```markdown
@file ./skill-everythink/SKILL.md
```

Or reference sub-skills directly in your prompts:

```markdown
@references/errors/error-log.md
@references/development/code-quality.md
```

</details>

<details>
<summary><strong>Gemini CLI</strong> — via <code>GEMINI.md</code> and <code>@file</code> imports</summary>

Copy or symlink the provided `GEMINI.md` into your project root:

```bash
cp skill-everythink/GEMINI.md ./GEMINI.md
```

Or import sub-skills directly using `@file.md` syntax:

```markdown
@references/development/code-quality.md
@references/errors/error-log.md
```

Use `/memory show` to verify loaded context, `/memory refresh` after edits.

</details>

<details>
<summary><strong>Cursor</strong> — via <code>.cursorrules</code> or Settings › Rules</summary>

```
@file:./skill-everythink/SKILL.md
```

Or paste the contents of `SKILL.md` directly into **Settings › Rules for AI**.

</details>

**Step 3 — Done.**

Your agent now has memory. It knows your conventions, remembers past mistakes, and expands its knowledge with every session.

---

## ⚙️ How It Works

### The Learning Loop

```
Agent makes a mistake
        ↓
Mistake is analyzed  (cause · context · impact)
        ↓
Rule is formulated   ("Never do X without checking Y first")
        ↓
Skill is updated     (references/errors/ or the matching sub-module)
        ↓
Agent never makes that mistake again — in any project
```

### Not Just Errors

The same loop applies to any kind of knowledge:

- **New insights** — better patterns, more efficient approaches
- **Processes** — deployment steps, review checklists, onboarding flows
- **Conventions** — naming schemes, commit style, architecture decisions
- **Partner knowledge** — API quirks, external systems, integration pitfalls

Every time the agent learns something important, it lands in the skill — structured, versioned, immediately available.

---

## 📊 How It Compares

| Feature | Fine-Tuning | RAG | Cursor Rules | mem0 / MemGPT | **Skill-Everythink** |
|---|:---:|:---:|:---:|:---:|:---:|
| Learns from mistakes | ✗ | ✗ | ✗ | ✓ | **✓** |
| Git-versioned | ✗ | ✗ | optional | ✗ | **✓** |
| Agent-agnostic | ✗ | partial | ✗ | partial | **✓** |
| Zero setup | ✗ | ✗ | ✓ | ✗ | **✓** |
| Domain knowledge | limited | ✓ | limited | ✓ | **✓** |
| Modular | ✗ | partial | ✗ | ✗ | **✓** |
| Transparent | ✗ | partial | ✓ | ✗ | **✓** |
| Cost | High (GPU) | Medium (infra) | Low | Medium (API) | **Minimal** |

---

## 📁 Project Structure

```
skill-everythink/
├── SKILL.md                    # Router — entry point (OpenCode)
├── CLAUDE.md                   # Claude Code integration entry point
├── GEMINI.md                   # Gemini CLI integration entry point
├── references/
│   ├── development/            # Code quality rules (15 rules)
│   ├── git/                    # Commit conventions (15 rules)
│   ├── domain/                 # Company knowledge template
│   ├── process/                # Review & deployment checklists
│   ├── errors/                 # Error log + self-extension workflow
│   └── _templates/             # Templates for new skills
├── docs/                       # Explanations & presentations
├── CONTRIBUTING.md             # How to contribute
└── LICENSE                     # MIT
```

`SKILL.md` is the central entry point. It is always loaded and decides which sub-skills are relevant for the current task. Sub-skills in `references/` are standalone modules — they can be loaded individually, in combination, or all at once.

---

## 📦 Starter Skills

Five production-ready sub-skills ship out of the box:

| Sub-Skill | What It Contains |
|---|---|
| `references/development/` | 15 rules for clean, maintainable code — from naming to error handling |
| `references/git/` | 15 rules for consistent commit messages, branch strategies, and PR hygiene |
| `references/domain/` | Template for company-specific knowledge: systems, processes, contacts |
| `references/process/` | Checklists for code review, deployment, and incident response |
| `references/errors/` | Structured error log with cause analysis, rule formulation, and prevention |

---

## 🔄 Self-Extension

The agent can extend its own skill — without human intervention. Here's the workflow:

1. **Trigger** — The agent detects a mistake, a new insight, or a missing rule
2. **Analysis** — Cause, context, and impact are captured in a structured format
3. **Formulation** — A clear, action-oriented rule is written (precise, not vague)
4. **Classification** — The rule is assigned to the right sub-skill (`errors/`, `development/`, etc.)
5. **Entry** — The agent writes the entry into the appropriate Markdown file
6. **Commit** — The change is committed via Git — with context, date, and rationale

The result: a skill that improves with every session — traceable, revertable, reviewable.

---

## 🛠️ Creating Your Own Skill

**Step 1 — Copy the template**

```bash
cp references/_templates/skill-template.md references/my-area/SKILL.md
```

**Step 2 — Fill in the template**

Add context, rules, and examples. Keep each sub-skill under 3,000 tokens — split rather than bloat.

**Step 3 — Open a PR**

```bash
git checkout -b feat/my-skill
git add references/my-area/
git commit -m "feat(skills): add my-area skill"
git push origin feat/my-skill
```

Then open a Pull Request on GitHub. Details and review criteria in [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## 🗺️ Roadmap

| Version | Status | What's included |
|---|---|---|
| **v1.0** | ✅ current | Core system · 5 starter skills · Claude Code support · OpenCode + Cursor integration |
| **v1.1** | planned | CLI tool (`npx skill-everythink init`) for fast project setup |
| **v1.2** | planned | Consolidation loop (auto-merge similar rules) · GitHub Actions linter |
| **v2.0** | planned | Skill Marketplace — discover, rate, and embed community skills |

---

## ❓ FAQ

<details>
<summary><strong>Does this work with my agent?</strong></summary>

Yes. Skill-Everythink is fully agent-agnostic. As long as your agent can load Markdown files as context — whether as a system prompt, file reference, or skill configuration — it works. Tested with OpenCode, Claude Code, Cursor, Claude Projects, GPT-4, and local models via Ollama.

</details>

<details>
<summary><strong>How large can a skill get?</strong></summary>

Maximum 3,000 tokens per sub-skill. That's the threshold where context overhead and attention loss become noticeable. When an area grows, split it into two focused sub-skills — two precise modules beat one bloated one.

</details>

<details>
<summary><strong>Can the agent really extend the skill itself?</strong></summary>

Yes. The self-extension workflow in `references/errors/` describes exactly how the agent formulates new entries, classifies them, and commits them. The human reviews the PR — the agent writes it.

</details>

<details>
<summary><strong>What's the difference from <code>.cursorrules</code>?</strong></summary>

Cursor Rules are static, unversioned, and only work in Cursor. Skill-Everythink is modular, Git-versioned, agent-agnostic, and has an active error memory. A skill grows with you — a `.cursorrules` file doesn't.

</details>

<details>
<summary><strong>Do I need a database?</strong></summary>

No. Everything is plain Markdown, stored on the filesystem, versioned with Git. No vector database, no embedding service, no running process. `git clone` is the only setup step.

</details>

<details>
<summary><strong>Can I use this in an existing project?</strong></summary>

Yes. Clone the repository next to your project or add it as a Git submodule. The skill path is registered once in your agent configuration — after that, everything runs automatically.

</details>

<details>
<summary><strong>What if a skill entry is wrong?</strong></summary>

`git revert`. Every change is versioned and can be undone in seconds. That's one of the core advantages over opaque memory systems.

</details>

---

## 🤝 Contributing

Contributions are welcome — new starter skills, improvements to existing rules, or tooling. Please read [CONTRIBUTING.md](./CONTRIBUTING.md) first.

---

## 📄 License

MIT — free to use, modify, and distribute, including commercially. See [LICENSE](./LICENSE).
