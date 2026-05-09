# Hacker News "Show HN" — copy-paste ready

> Posting checklist at the bottom. Read it first. The reply templates
> for the predictable top comments live in
> [`hn-comment-templates.md`](./hn-comment-templates.md).
>
> **Synthesis note (Bo):** this file is unchanged from Lara R3 in tone
> and substance. HN actively penalises marketing-rewrites. The only
> edit is the title field — we lead with `git diff` because it's the
> single most differentiating verb we own. Henrik's punchier
> Twitter-direction lives in `twitter-thread.md`, not here.

---

## Title (≤ 80 chars, plain, no hype)

```
Show HN: skill-everything – memory you can `git diff` for AI coding agents
```

Alternative if the above is taken:

```
Show HN: Git-versioned memory for AI coding agents (no DB, no embeddings)
```

We do not use:

- "Battle-tested"
- "AI engineers from BMW and Google"
- "First skill system with X" (`dspy`, `promptfoo`, and `langgraph` have lockfile-equivalents)
- "84% fewer tokens"

If we say any of the above on HN, we lose the front page.

---

## URL field

```
https://github.com/sordi-ai/skill-everything
```

---

## First comment (post within 5 minutes of submission)

```
Hi HN — author here.

skill-everything is a side project. Two engineers, weekends, ~6 weeks.
Day jobs are AI engineering at large companies (BMW and Google), but
this is independent work — see DISCLAIMER.md, not endorsed by either
employer.

The pitch in one paragraph: an agent makes a mistake. Instead of
forgetting, it writes a YAML entry into references/errors/error-log.md,
derives an action directive, and opens a PR labelled needs-rule-review.
A maintainer reviews it. CI lints it against a JSON-Schema and a
verb allow-list. After merge, the rule loads automatically next session.

The thing we keep going back to: cross-tool. The same Markdown that
Cursor reads via .cursorrules, Claude Code reads via CLAUDE.md, and
Gemini CLI reads via GEMINI.md. One source-of-truth (references/_index.yml)
generates all four loaders. CI fails on drift. If you've ever rewritten
the same conventions for three different agents, you'll recognise the
pain.

What's actually new (small, but real): a structured error schema with
JSON-Schema validation, a `learn(errors): ERR-YYYY-NNN` PR convention
that makes self-extension visible in `git log`, per-skill manifest
frontmatter (id, version, tokens_target, triggers), and an honest
adversarial test suite at tests/test_validate_rules_adversarial.py
that documents every bypass we know about.

What's not new: agent memory in Markdown. AGENTS.md, aider conventions,
Cursor Rules, Continue.dev all sit in the same neighbourhood. We sit
on top of those formats — `CLAUDE.md`, `GEMINI.md`, `.cursorrules` are
generated from references/_index.yml.

Honest about what's not solved:
- Token savings vs. cached monolithic prompts are roughly break-even.
  The 20-34% number in the README is for uncached comparisons.
- The validator catches 12/20 prompt-injection bypasses we've thought
  of. The remaining 8 (homoglyphs, indirection, natural-language
  nudges) rely on human PR review. SECURITY.md spells this out.
- We don't claim a Re-Mistake-Rate yet. The eval skeleton at
  tests/eval/ documents the methodology contract (n≥30 per cell,
  multiple models, prompt hash pinned) and we'll publish numbers
  when Phase 2 produces them. No vibe checks.

Happy to answer questions. Most likely critiques and our honest
answers are in the repo already (linked from README → SECURITY.md).
```

---

## Posting checklist

| When | What | Notes |
|---|---|---|
| **T-7 days** | Final READ-THROUGH of README and DISCLAIMER as a hostile reader | Sven's HN-comment simulation in `concept/04-review-sven.md` is your dress rehearsal |
| **T-2 days** | Test all repo links from a logged-out browser | GitHub auth caches surprise people |
| **T-2 days** | Confirm the 30-second `git clone` flow on a fresh machine | This is the first thing curious commenters try |
| **T-1 day** | Make sure CI is fully green on `main` | A red badge in the readme is fatal |
| **T-1 day** | Pre-load comment templates in `hn-comment-templates.md` into a draft window | You will not have time to compose them live |
| **T-1 day** | Verify `git shortlog -sne` shows engineer #2 — or rephrase README to "solo project, looking for co-maintainers" | Comment-template #5 antedates the audit; do not rely on it as Plan A |
| **Post** | Tuesday–Thursday, 14:00–16:00 UTC (8–10 AM Eastern) | Avoid Mondays and weekends |
| **0–15 min** | Submit + post the first comment within 5 minutes | Comment ordering rewards early authors |
| **15 min – 4 h** | Reply to **every** top-level comment, even hostile ones | Take the bait politely; concede the ones we already know about |
| **4 – 24 h** | Don't argue with bad-faith comments. Flag once and move on | HN's downvote economy handles them |
| **24 h** | Post a follow-up to the discussion thread with anything you learned | Often becomes its own small attention spike |
| **48 h** | Open issues for every legitimate critique that surfaced | This becomes the next sprint |

## Suggested posting times

- Tue / Wed / Thu, 14:00–16:00 UTC.
- Avoid: Mon morning (catch-up flood), Fri afternoon (everyone's checked out), weekends (low signal).

## Time budget for launch day

Block **6 hours** continuous after submission. That's not flexibility — that's the floor.

- 0–2 h: heavy comment reply load.
- 2–4 h: secondary commenters and questions arrive from US wake-up.
- 4–6 h: discussion winds down, but a single late comment can re-spike it.

## What we do NOT do

- We do not edit the title or URL after posting (HN penalises this).
- We do not delete comments (even hostile ones, even our own typos — reply with a correction).
- We do not call in friends to upvote; HN penalises this aggressively.
- We do not respond to "you should have used X" comments by defending. We say "yes, here's the trade-off we picked, and here's the issue tracking the alternative".
