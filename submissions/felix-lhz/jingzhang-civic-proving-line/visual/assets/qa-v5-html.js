const path = require('path');
const os = require('os');
const fs = require('fs');
const cp = require('child_process');
const { chromium } = require('playwright');

(async () => {
  const root = path.resolve(__dirname, '..');
  const pkg = path.resolve(root, '..');
  const out = path.join(os.tmpdir(), 'jingzhang-v6-review-evidence');
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ headless: true, executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe' });
  const report = { ok: true, pages: [], external_requests: [], console_errors: [], evidence_pack: [] };
  const pages = [
    ['index.html', 1440, 1600, 'visual-zh'],
    ['index.en.html', 1440, 1600, 'visual-en'],
    ['index.html', 390, 844, 'visual-mobile'],
  ];
  for (const [file, width, height, name] of pages) {
    const page = await browser.newPage({ viewport: { width, height }, reducedMotion: 'reduce' });
    page.on('request', (request) => { if (!/^(file|data):/.test(request.url())) report.external_requests.push(request.url()); });
    page.on('console', (message) => { if (message.type() === 'error') report.console_errors.push(message.text()); });
    page.on('pageerror', (error) => report.console_errors.push(error.message));
    await page.goto(`file:///${path.join(root, file).replace(/\\/g, '/')}`, { waitUntil: 'load' });
    const firstLook = await page.locator('.first-look.v6').isVisible();
    const stateInit = await page.evaluate(() => document.body.dataset.v6Init || 'missing');
    const geometryCount = await page.locator('.v5-object').count();
    const version = await page.locator('#scenario-data').evaluate((node) => JSON.parse(node.textContent).schema_version);
    const screenshot = path.join(out, `${name}-first.png`);
    await page.screenshot({ path: screenshot, fullPage: false });
    await page.locator('[data-state-view="RETIRE"]').click();
    const stateHash = await page.evaluate(() => location.hash);
    const stateBody = await page.evaluate(() => document.body.dataset.v6State || 'missing');
    const stateRestored = stateHash.includes('state=retire') && stateBody === 'retire';
    await page.locator('[data-mode="baseline"]').click();
    await page.locator('[data-scenario="SCN-010"]').last().click();
    const hashRestored = (await page.evaluate(() => location.hash)).includes('SCN-010');
    await page.keyboard.press('Tab');
    const interaction = path.join(out, `${name}-interaction.png`);
    await page.screenshot({ path: interaction, fullPage: false });
    report.pages.push({ name, firstLook, stateInit, geometryCount, version, hashRestored, stateRestored, stateHash, stateBody, screenshot, interaction });
    if (name !== 'visual-mobile') report.evidence_pack.push(screenshot);
    if (!firstLook || geometryCount < 50 || version !== '1.4.0' || !hashRestored || !stateRestored) report.ok = false;
    await page.close();
  }
  for (const [file, name] of [['proposal.html', 'proposal-zh'], ['proposal.en.html', 'proposal-en']]) {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1600 }, reducedMotion: 'reduce' });
    page.on('request', (request) => { if (!/^(file|data):/.test(request.url())) report.external_requests.push(request.url()); });
    page.on('console', (message) => { if (message.type() === 'error') report.console_errors.push(message.text()); });
    await page.goto(`file:///${path.join(pkg, 'report', file).replace(/\\/g, '/')}`, { waitUntil: 'load' });
    const screenshot = path.join(out, `${name}-first.png`);
    await page.screenshot({ path: screenshot, fullPage: false });
    report.evidence_pack.push(screenshot);
    await page.close();
  }
  await browser.close();

  const figureNames = ['site-overview', 'land-use-structure', 'key-areas', 'mobility-bluegreen', 'metrics-evidence'];
  for (const name of figureNames) for (const suffix of ['', '.en']) report.evidence_pack.push(path.join(pkg, 'assets', 'figures', `${name}${suffix}.png`));
  const ppm = 'C:/Users/11759/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe';
  for (const pdf of ['a0-boards.pdf', 'a0-boards.en.pdf', 'a3-booklet.pdf', 'a3-booklet.en.pdf']) {
    const target = path.join(out, path.basename(pdf, '.pdf'));
    const run = cp.spawnSync(ppm, ['-png', '-f', '1', '-singlefile', '-r', '90', path.join(pkg, 'drawings', pdf), target], { encoding: 'utf8' });
    if (run.status !== 0) { report.ok = false; report.console_errors.push(run.stderr); }
    report.evidence_pack.push(`${target}.png`);
  }
  if (report.external_requests.length || report.console_errors.length || report.evidence_pack.length !== 18) report.ok = false;
  const index = path.join(out, 'evidence-index.json');
  fs.writeFileSync(index, JSON.stringify(report, null, 2));
  console.log(JSON.stringify({ ...report, evidence_index: index }, null, 2));
  process.exit(report.ok ? 0 : 1);
})().catch((error) => { console.error(error); process.exit(1); });
