// Pixel-perfect SVG overflow checker.
//
// Loads an SVG inline in headless Chromium so getBBox() works, then runs
// two check classes:
//
//   1. OVERFLOW (own-container): per <g> that wraps container <rect>s
//      (.node, .chip, .gate, .gate-fill), reports every child <text>
//      whose bbox extends past the matching rect. Picks the rect whose
//      vertical range contains the text's y. Skips text that is not
//      contained by any rect (free-floating annotations).
//
//   2. FOREIGN-RECT INTERSECT: for every <text>, checks whether its
//      viewport bbox (getBoundingClientRect) intersects any <rect> that
//      is NOT an ancestor of the text. Catches "tagline touches folder
//      strip border" class of bugs.
//
// Both classes filter false-positives: rects smaller than 40x18 are
// treated as swatches/markers, not containers. Tolerance: 2 px.
//
// Exit code: 0 if both checks CLEAN, 1 if any issue found.
// Usage: node overflow-check.js path/to/file.svg

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const svgPath = process.argv[2];
const TOL = 2;

if (!svgPath) {
  console.error('usage: node overflow-check.js <path/to/file.svg>');
  process.exit(2);
}

(async () => {
  const svgText = fs.readFileSync(path.resolve(svgPath), 'utf-8');
  const browser = await chromium.launch();
  const ctx = await browser.newContext({
    viewport: { width: 1400, height: 900 },
    deviceScaleFactor: 1,
  });
  const page = await ctx.newPage();
  await page.setContent(
    `<!DOCTYPE html><html><head><style>body{margin:0;padding:0}</style></head><body>${svgText}</body></html>`
  );
  await page.waitForLoadState('networkidle');

  // CHECK 1 — text overflows OWN container rect
  const issues = await page.evaluate((TOL) => {
    const results = [];
    for (const g of document.querySelectorAll('g')) {
      const allRects = g.querySelectorAll(
        ':scope > rect.node, :scope > rect.chip, :scope > rect.gate, :scope > rect.gate-fill'
      );
      const containers = Array.from(allRects).filter((r) => {
        const w = parseFloat(r.getAttribute('width'));
        const h = parseFloat(r.getAttribute('height'));
        return w >= 40 && h >= 18;
      });
      if (containers.length === 0) continue;
      for (const t of g.querySelectorAll(':scope > text')) {
        const tX = parseFloat(t.getAttribute('x') || 0);
        const tY = parseFloat(t.getAttribute('y') || 0);
        let rect = null;
        for (const r of containers) {
          const rXc = parseFloat(r.getAttribute('x') || 0);
          const rYc = parseFloat(r.getAttribute('y') || 0);
          const rWc = parseFloat(r.getAttribute('width'));
          const rHc = parseFloat(r.getAttribute('height'));
          if (
            tY >= rYc - 2 && tY <= rYc + rHc + 2 &&
            tX >= rXc - 5 && tX <= rXc + rWc + 5
          ) {
            rect = r;
            break;
          }
        }
        if (!rect) continue;
        const rWidth = parseFloat(rect.getAttribute('width'));
        const rHeight = parseFloat(rect.getAttribute('height'));
        const rX = parseFloat(rect.getAttribute('x') || 0);
        const rY = parseFloat(rect.getAttribute('y') || 0);
        const bbox = t.getBBox();
        const issue = {
          text: t.textContent.trim().slice(0, 60),
          overflowRight: bbox.x + bbox.width - (rX + rWidth),
          overflowLeft: rX - bbox.x,
          overflowBottom: bbox.y + bbox.height - (rY + rHeight),
          overflowTop: rY - bbox.y,
          parent_g: g.getAttribute('transform') || '(no-transform)',
        };
        if (
          issue.overflowRight > TOL ||
          issue.overflowLeft > TOL ||
          issue.overflowBottom > TOL ||
          issue.overflowTop > TOL
        ) {
          results.push(issue);
        }
      }
    }
    return results;
  }, TOL);

  // CHECK 2 — text bbox intersects a NON-PARENT rect
  const intersections = await page.evaluate((TOL) => {
    const results = [];
    const isAncestorOf = (rect, text) => {
      let p = text.parentNode;
      while (p && p.nodeType === 1) {
        if (p === rect.parentNode) return true;
        p = p.parentNode;
      }
      return false;
    };
    const intersect = (a, b) =>
      !(
        a.right <= b.left + TOL ||
        a.left >= b.right - TOL ||
        a.bottom <= b.top + TOL ||
        a.top >= b.bottom - TOL
      );
    for (const t of document.querySelectorAll('text')) {
      const tBox = t.getBoundingClientRect();
      if (tBox.width === 0 || tBox.height === 0) continue;
      for (const r of document.querySelectorAll('rect')) {
        if (isAncestorOf(r, t)) continue;
        const rBox = r.getBoundingClientRect();
        if (rBox.width < 40 || rBox.height < 18) continue;
        if (intersect(tBox, rBox)) {
          results.push({
            text: t.textContent.trim().slice(0, 60),
            text_y: tBox.top.toFixed(0),
            rect_y: rBox.top.toFixed(0) + '..' + rBox.bottom.toFixed(0),
            rect_class: r.getAttribute('class') || '(no-class)',
            overlapX: (
              Math.min(tBox.right, rBox.right) - Math.max(tBox.left, rBox.left)
            ).toFixed(1),
            overlapY: (
              Math.min(tBox.bottom, rBox.bottom) - Math.max(tBox.top, rBox.top)
            ).toFixed(1),
          });
        }
      }
    }
    return results;
  }, TOL);

  let exit = 0;
  if (issues.length === 0) {
    console.log('OVERFLOW: CLEAN — 0 text overflows past their containing rect');
  } else {
    exit = 1;
    console.log(
      `OVERFLOW: FOUND ${issues.length} text overflowing own container:\n`
    );
    for (const i of issues) {
      const d = [];
      if (i.overflowRight > TOL) d.push(`right +${i.overflowRight.toFixed(1)}px`);
      if (i.overflowLeft > TOL) d.push(`left +${i.overflowLeft.toFixed(1)}px`);
      if (i.overflowBottom > TOL) d.push(`bottom +${i.overflowBottom.toFixed(1)}px`);
      if (i.overflowTop > TOL) d.push(`top +${i.overflowTop.toFixed(1)}px`);
      console.log(`  [${d.join(', ')}] "${i.text}"\n     in ${i.parent_g}`);
    }
  }

  if (intersections.length === 0) {
    console.log(
      '\nFOREIGN-RECT INTERSECT: CLEAN — 0 text-vs-foreign-rect intersections'
    );
  } else {
    exit = 1;
    console.log(
      `\nFOREIGN-RECT INTERSECT: FOUND ${intersections.length} text-touches-non-parent-rect:\n`
    );
    for (const i of intersections) {
      console.log(
        `  "${i.text}" (top ${i.text_y}) intrudes into rect.${i.rect_class} (${i.rect_y}) — overlap ${i.overlapX}px × ${i.overlapY}px`
      );
    }
  }

  await browser.close();
  if (exit !== 0) process.exit(exit);
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
