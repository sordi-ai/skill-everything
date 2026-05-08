# Twitter / X launch thread

8 tweets, all under 280 chars. Honest tone. Lara's recommended Tagline B
("inherits the fix") is the spine.

---

## Tweet 1 (Hook)

```
Every mistake your AI coding agent makes — same one again tomorrow.

We built something to fix that. Plain Markdown, plain Git, dogfooded
for ~6 weeks. Independent open source.

Show HN today. 🧵👇

github.com/sordi-ai/skill-everything
```

---

## Tweet 2 (The actual loop)

```
The loop:

1. Agent makes a mistake
2. Writes a YAML entry → derives an action directive
3. Opens a PR labelled `needs-rule-review`
4. Human reviews + merges
5. Next session, the fix is loaded automatically

The repo IS the loop.
```

---

## Tweet 3 (Why Markdown + Git, not vector DB)

```
Why not a vector store?

Because we want every rule to be:
- `cat`-able by a human
- `git diff`-able in a PR
- revertable when wrong
- portable across Cursor, Claude Code, Gemini CLI

A vector index is the right answer for >1k rules. Not for
team conventions.
```

---

## Tweet 4 (The honest token math)

```
Token math, no hype:

- vs. uncached monolithic prompts: 20–34% cheaper
- vs. cached monolithic prompts: ~break-even

We don't claim 84% savings. The README has the full table.
The headline win is review + portability, not the cents.
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

## Tweet 8 (CTA)

```
MIT licensed. Plain Markdown. `git clone` is the entire setup.

If you've been hand-pasting conventions into your agent, this
might save you an evening.

Issues > stars. Honest critique > 🚀.

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
