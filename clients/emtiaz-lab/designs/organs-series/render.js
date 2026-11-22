// Render the 3 posts to PNG: node render.js [outDir]
// Fails (exit 1) if any text overlaps other text or leaves the canvas margins.
const { chromium } = require('playwright');
const path = require('path');

// Runs in the page: boxes of every rendered text line, then pairwise overlap + bounds check.
function checkText(margin) {
  const W = document.documentElement.clientWidth, H = document.documentElement.clientHeight;
  const boxes = [];
  const walker = document.createTreeWalker(document.getElementById('post'), NodeFilter.SHOW_TEXT);
  for (let n; (n = walker.nextNode());) {
    if (!n.textContent.trim()) continue;
    const r = document.createRange(); r.selectNodeContents(n);
    for (const b of r.getClientRects()) {
      if (b.width < 1 || b.height < 1) continue;
      boxes.push({ text: n.textContent.trim().slice(0, 30), x: b.left, y: b.top, r: b.right, b: b.bottom, el: n.parentElement });
    }
  }
  const problems = [];
  for (const a of boxes) {
    if (a.x < margin || a.y < margin || a.r > W - margin || a.b > H - margin)
      problems.push(`outside margin: "${a.text}"`);
  }
  // Lines of the same text node wrap with natural line-height; compare different nodes only.
  const pad = 2;
  for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
    const a = boxes[i], b = boxes[j];
    if (a.el === b.el) continue;
    const ox = Math.min(a.r, b.r) - Math.max(a.x, b.x), oy = Math.min(a.b, b.b) - Math.max(a.y, b.y);
    // glyph boxes include line-height leading, so require a real ink-sized overlap
    if (ox > pad && oy > Math.min(a.b - a.y, b.b - b.y) * 0.35)
      problems.push(`overlap: "${a.text}" × "${b.text}"`);
  }
  return [...new Set(problems)];
}

(async () => {
  const out = process.argv[2] || path.join(__dirname, 'export');
  require('fs').mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  let failed = false;
  for (const d of ['liver', 'kidney', 'hpylori']) {
    await page.goto('file://' + path.join(__dirname, (process.env.POST || 'post.html')) + '?d=' + d);
    await page.waitForSelector('body[data-ready="1"]');
    await page.waitForTimeout(400);
    const problems = await page.evaluate(checkText, 40);
    await page.locator('#post').screenshot({ path: path.join(out, `emtiaz-${d}.png`) });
    if (problems.length) { failed = true; console.log(`✗ ${d}\n  ` + problems.join('\n  ')); }
    else console.log(`✓ ${d}: no text collisions`);
  }
  await browser.close();
  process.exit(failed ? 1 : 0);
})();
