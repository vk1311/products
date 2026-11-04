#!/usr/bin/env node
// Prints an HTML file to PDF with headless Chromium (via Playwright).
// Usage: node print-pdf.js input.html output.pdf
// Set CHROME_PATH to use a specific Chrome/Chromium binary.
const path = require('path');
const { pathToFileURL } = require('url');

let chromium;
try {
  ({ chromium } = require('playwright'));
} catch (e) {
  console.error('Playwright is not installed. Run:  npm install playwright  (in the ebooks folder)');
  process.exit(1);
}

(async () => {
  const [input, output] = process.argv.slice(2);
  if (!input || !output) {
    console.error('Usage: node print-pdf.js input.html output.pdf');
    process.exit(1);
  }
  const launchOpts = process.env.CHROME_PATH
    ? { executablePath: process.env.CHROME_PATH, args: ['--no-sandbox'] }
    : {};
  const browser = await chromium.launch(launchOpts);
  const page = await browser.newPage();
  await page.goto(pathToFileURL(path.resolve(input)).href, { waitUntil: 'networkidle' });
  await page.emulateMedia({ media: 'print' });
  await page.pdf({
    path: output,
    preferCSSPageSize: true,
    printBackground: true,
    tagged: true,
    outline: true,
  });
  await browser.close();
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
