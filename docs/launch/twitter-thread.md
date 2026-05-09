# Twitter / X launch thread

8 tweets, all under 280 chars. Honest tone. Henrik's pain-hook spine
("same mistake tomorrow"); Lara's substance ratio preserved (Tweet 4
+ Tweet 6 honest about the math and the bypass-rate).

> **Synthesis note (Bo):** Twitter rewards punchy hooks more than HN
> does. Tweets 1, 2, 4, and 8 were refreshed to Henrik's harder hooks.
> Tweets 3, 5, 6, 7 stay on Lara's substance line — they carry the
> token-math, the threat model, and the side-project honesty.
> The launch tweet is posted within 30 min of the HN submission so the
> two amplify each other. Tweet 8 CTA tied back to Tweet 1's pain
> framing per Lara's R4 review.

---

## Tweet 1 (Hook — concrete pain)

```
Your AI agent makes the same mistake tomorrow it made today.

We built a memory layer where every fix is a Git commit, every rule is
plain Markdown, and the same memory works in Cursor, Claude Code,
Gemini CLI, and OpenCode.

Side project. Two engineers. ~6 weeks dogfooding. MIT.

🧵👇 github.com/sordi-ai/skill-everything
```

---

## Tweet 2 (The actual loop, with click-hook ending)

```
The loop:

1. Agent makes a mistake
2. Writes a YAML entry → derives a rule (`Always X`, `Never Y`)
3. Opens a PR labelled `needs-rule-review`
4. CI lints. Human merges.
5. Next session, the rule auto-loads.

The repo IS the loop. Open the error log — every entry is a real one.
```

---

## Tweet 3 (Why Markdown + Git, not vector DB)

```
Why not a vector store?

Because we want every rule to be:
- `cat`-able by a human
- `git diff`-able in a PR
- revertable when wrong
- portable across Cursor, Claude Code, Gemini CLI, OpenCode

A vector index is the right answer for >1k rules. Not for
team conventions.
```

---

## Tweet 4 (Marginal-cost framing — token math, no hype)

```
Token math, no hype:

Monolithic prompts grow with your skill library — every user, every
message pays for skills they don't use.

skill-everything stays flat. Add the 50th skill, pay the same per
message as the 1st.

20–34% cheaper uncached. ~break-even cached. README has the table.
```

---

## Tweet 5 (Self-extension as supply-chain problem)

```
Self-extending memory is a supply-chain problem disguised as a
magic feature.

So we treat it like one:
- JSON-Schema validation on every PR
- Verb allow-list for `new_rule`
- CODEOWNERS gating on references/errors/
- Adversarial test suite docs every bypass we know

Trust boundary = human PR review.
```

---

## Tweet 6 (Honest about gaps)

```
Honest about what we don't have yet:

- No published Re-Mistake-Rate. The eval skeleton documents the
  methodology contract (n≥30, multi-model, prompt hash pinned).
  Numbers come when Phase 2 produces them.
- 12/20 documented prompt-injection bypasses caught by the
  validator. The other 8 rely on human review.
```

---

## Tweet 7 (Who built this)

```
Side project. Two engineers. Day jobs are AI engineering at
large companies — this is independent open source, not endorsed
by any employer. DISCLAIMER.md spells it out.

We built it because we ran into agent-memory at scale and wanted
something we could git-blame.
```

---

## Tweet 8 (CTA — bound back to Tweet 1 pain)

```
MIT-licensed. `git clone` is the entire setup.

Star it if you've ever rewritten your conventions for three different agents.

github.com/sordi-ai/skill-everything
```

---

## Hashtags / mentions (Tweet 1 or 8 tail)

`#AI #LLM #DevTools #OpenSource`

Don't tag company accounts of employers (BMW, Google) — DISCLAIMER policy.
Don't tag Anthropic / Cursor / Google AI accounts in the launch tweet —
they'll see it organically; tagging looks needy.

---

## Posting time

Same window as HN: Tue/Wed/Thu, 14:00–16:00 UTC. Post the thread within
30 minutes of the HN submission so the two amplify each other.

---

## Three independent hook-tweets for follow-up days

Use these on the days after launch — independent of the thread, each
one is self-contained and points to the repo. Pick one per day, not all
three at once.

### Hook A — Asymmetry (cross-tool pain)

```
Your `.cursorrules` is dead the moment you open Claude Code.

Built a thing where the same Markdown lives in Cursor, Claude
Code, Gemini CLI, and OpenCode — generated from one source,
drift-checked in CI.

github.com/sordi-ai/skill-everything · MIT
```

### Hook B — Marginal cost (the bet, in 4 lines)

```
Hot take: monolithic system prompts charge every user for every skill,
every message — even the ones they don't use.

Add a 50th skill to your repo, every message pays.

We tried something different. Per-skill router, 3k-token cap, CI-enforced.

🔗 github.com/sordi-ai/skill-everything
```

### Hook C — `git log --grep` (a command they can paste)

```
`git log --grep="learn("`

That's how I know when my agent learned something this week.
Every mistake → YAML entry → action directive → PR → human merge.

The repo IS the loop. Plain Markdown. MIT.

github.com/sordi-ai/skill-everything
```
