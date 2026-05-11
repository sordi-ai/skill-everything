# svg-check

Pixel-perfect Playwright bbox check for SVG diagrams. Catches text-overflow and foreign-rect-intersection bugs that eyeball review misses.

## Quick start

```bash
cd skills/svg-check
bash setup.sh                     # one-time: installs Playwright + Chromium
node overflow-check.js ../../docs/diagram.svg
```

Exit 0 means both check classes pass. Exit 1 means a bug was found — fix the SVG and re-run.

## Two check classes

- **OVERFLOW**: text bbox extends past its containing rect
- **FOREIGN-RECT INTERSECT**: text bbox intersects a non-ancestor rect

Both with 2 px tolerance.

## Files

- [`SKILL.md`](./SKILL.md) — when to apply, acceptance criteria, fix patterns
- [`overflow-check.js`](./overflow-check.js) — the script
- [`setup.sh`](./setup.sh) — one-time install
- [`EXAMPLES.md`](./EXAMPLES.md) — real before/after fixes

## Why

LLM eyeball review at 4× zoom missed two real overflows in `architecture.svg` on 2026-05-11 — first a 40 px text overflow in a four-designer parallel review, then a 2 px foreign-rect intersection in a three-cycle iteration. The script catches both in 5 seconds.

The acceptance test is the script. Not the agent's "looks good".
