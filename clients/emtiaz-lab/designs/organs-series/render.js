// Render the 3 posts to PNG: node render.js [outDir]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const out = process.argv[2] || path.join(__dirname, 'export');
  require('fs').mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  for (const d of ['liver', 'kidney', 'hpylori']) {
    await page.goto('file://' + path.join(__dirname, 'post.html') + '?d=' + d);
    await page.waitForSelector('body[data-ready="1"]');
    await page.waitForTimeout(400);
    await page.locator('#post').screenshot({ path: path.join(out, `emtiaz-${d}.png`) });
    console.log('rendered', d);
  }
  await browser.close();
})();
