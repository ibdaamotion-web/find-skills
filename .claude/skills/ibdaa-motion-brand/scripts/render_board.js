#!/usr/bin/env node
// Render an Ibdaa Motion project board (1080x1350, Facebook 4:5) to PNG.
// Usage: node render_board.js <board.json> [out.png]
// Image paths in the JSON may be relative to the JSON file, absolute, or http(s) URLs.
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

(async () => {
  const [jsonPath, outArg] = process.argv.slice(2);
  if (!jsonPath) { console.error('Usage: node render_board.js <board.json> [out.png]'); process.exit(1); }
  const data = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
  const base = path.dirname(path.resolve(jsonPath));
  data.images = (data.images || []).map(src =>
    /^(https?:|data:|file:)/.test(src) ? src : pathToFileURL(path.resolve(base, src)).href);

  const out = outArg || path.join(base, path.basename(jsonPath, '.json') + '.png');
  const template = path.join(__dirname, '..', 'templates', 'project-board.html');

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 2 });
  await page.goto(pathToFileURL(template).href, { waitUntil: 'networkidle' });
  await page.evaluate(d => window.fillBoard(d), data);
  await page.evaluate(async () => {
    await document.fonts.ready;
    await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })));
  });
  await page.screenshot({ path: out, clip: { x: 0, y: 0, width: 1080, height: 1350 } });
  await browser.close();
  console.log('Board saved:', out);
})();
