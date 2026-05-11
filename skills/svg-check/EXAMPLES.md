# SVG Check — Examples

Real before/after fixes with script output. Use these as templates when fixing similar bugs.

---

## Example 1 — own-container overflow (architecture.svg, GEMINI CLI loader)

**Bug.** The GEMINI CLI box was 200 px wide. The mono-tag text `@skills/<name>/SKILL.md  ·  /memory show` measured ~241 px. Overflow right +40.1 px.

**Script output (before fix):**

```
OVERFLOW: FOUND 1 text overflowing own container:

  [right +40.1px] "@skills/<name>/SKILL.md  ·  /memory show"
     in translate(670 322)
```

**Fix.** Move `/memory show` to the mono-dim line below; mono-tag now matches the CLAUDE CODE pattern.

```diff
- <text class="mono-tag" x="10" y="48">@skills/&lt;name&gt;/SKILL.md  ·  /memory show</text>
- <text class="mono-dim" x="10" y="62">imports + reload command</text>
+ <text class="mono-tag" x="10" y="48">@skills/&lt;name&gt;/SKILL.md</text>
+ <text class="mono-dim" x="10" y="62">imports  ·  /memory show</text>
```

**Script output (after fix):**

```
OVERFLOW: CLEAN — 0 text overflows past their containing rect
FOREIGN-RECT INTERSECT: CLEAN — 0 text-vs-foreign-rect intersections
```

---

## Example 2 — foreign-rect intersection (architecture.svg, tagline)

**Bug.** Tagline at `y=494` had ascenders reaching `y=485`. Folder-strip chip border at `y=487`. The 2 px difference made the tagline text visually touch the chip border (anti-aliased fringe overlapped).

**Script output (before fix):**

```
FOREIGN-RECT INTERSECT: FOUND 1 text-touches-non-parent-rect:

  "edit the index, regenerate, commit  ·  drift fails CI" (top 485)
    intrudes into rect.chip (425..487) — overlap 280.0px × 2.0px
```

**Fix.** Extend the SVG viewBox height by 20 px and move the bottom row down by 16 px. Other elements stay put.

```diff
- <svg viewBox="0 0 1280 500" ...>
+ <svg viewBox="0 0 1280 520" ...>

- <rect class="frame" ... width="1279" height="499" .../>
+ <rect class="frame" ... width="1279" height="519" .../>

- <text class="tagline"  x="1256" y="494" ...>edit the index, regenerate, commit ...</text>
- <text class="mono-dim" x="24"   y="494" >skill-everything  /  docs/architecture.svg</text>
+ <text class="tagline"  x="1256" y="510" ...>edit the index, regenerate, commit ...</text>
+ <text class="mono-dim" x="24"   y="510" >skill-everything  /  docs/architecture.svg</text>
```

**Script output (after fix):**

```
OVERFLOW: CLEAN — 0 text overflows past their containing rect
FOREIGN-RECT INTERSECT: CLEAN — 0 text-vs-foreign-rect intersections
```

---

## Example 3 — Copy-Paste bug (memory-to-go.svg, same GEMINI line)

**Bug.** The exact same `@skills/<name>/SKILL.md  ·  /memory show` pattern existed in a second SVG and overflowed the same way (+42.6 px). Eyeball reviews of one SVG never look at the others — the script run across the whole folder catches it.

**Lesson.** After fixing a bug in one SVG, run the script across **every** SVG in the folder, not just the one you touched.

```bash
for svg in docs/*.svg; do
  out=$(node skills/svg-check/overflow-check.js "$svg" 2>&1)
  if echo "$out" | grep -q "FOUND"; then
    echo "FAIL: $svg"
    echo "$out" | grep -E "FOUND|  \[|  \""
  fi
done
```

---

## Anti-pattern — what NOT to do

**Don't widen the tolerance to make red go away.** The default tolerance is 2 px because anti-aliased text rendering needs at least 2 px of clearance to read as separated. Bumping tolerance to 10 px will hide real bugs.

**Don't suppress the check by editing the script.** If the script reports something that is genuinely a false-positive (e.g. a free-floating annotation that the check still flags), document the false-positive class and add a structural filter (size, position, class-name). Do not silently delete the assertion.

**Don't declare done from eyeballing**. Two separate review-sprints — one with four parallel design agents at 4× zoom, one with three sequential iteration cycles — both missed real overflows that the script caught in five seconds. The script is the judge.
