# Hacker News "Show HN" Post

Copy-paste ready for https://news.ycombinator.com/submit

---

## Title

Show HN: Skill-Everythink – Git-versioned memory for AI coding agents (plain Markdown, zero infra)

---

## URL

https://github.com/sordi-ai/skill-everything

---

## Text (paste into the text field if no URL, or as first comment)

I got tired of watching Claude/GPT make the same mistakes I'd already corrected. Every session starts fresh — the agent has no memory of what it learned yesterday.

Fine-tuning is expensive and frozen. RAG needs infrastructure. Cursor Rules only work in Cursor. mem0/MemGPT are powerful but opaque.

So I built Skill-Everythink: a memory system for AI coding agents made entirely of plain Markdown files, versioned with Git.

**How it works:**

- Agent makes a mistake → analyzes root cause → writes a rule ("Never X without Y") → commits it to a Markdown file
- Next session, the rule is loaded automatically
- Every mistake makes the system permanently better

**What makes it different:**

- Plain Markdown — no database, no embeddings, no infrastructure
- Git-versioned — every lesson is a commit you can diff, blame, revert, or cherry-pick
- Agent-agnostic — works with Claude Code, Gemini CLI, OpenCode, Cursor
- Transparent — you can read exactly what your agent knows and why
- Self-extending — the agent grows its own skill system

**Ships with 8 starter skills** (code quality, git conventions, Python/TypeScript/React best practices, deployment checklists, error memory) — all from real projects.

The whole thing is ~50 Markdown files. No build step. No runtime dependencies. `git clone` and you're done.

MIT licensed. Would love feedback from the HN community on the approach.

---

## Suggested posting times (HN best engagement)

- Tuesday–Thursday, 8-10 AM EST (1-3 PM UTC)
- Avoid weekends and Monday mornings
- Respond to every comment in the first 2 hours

## First comment to post immediately after submission

Hey HN, author here. The core insight is embarrassingly simple: LLMs have no persistent memory across sessions. Every workaround (fine-tuning, RAG, vector DBs) adds complexity.

Markdown files in a Git repo are the simplest possible "memory" — and they're already the format every coding agent can read (CLAUDE.md, GEMINI.md, .cursorrules).

The interesting part is the self-extension: the agent doesn't just consume rules, it writes new ones when it makes mistakes. The human reviews the PR. The agent wrote it.

Happy to answer any questions about the architecture or trade-offs.
