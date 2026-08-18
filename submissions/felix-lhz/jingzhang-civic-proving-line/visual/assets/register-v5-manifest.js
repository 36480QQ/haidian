const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const root = path.resolve(__dirname, '..', '..');
const file = path.join(root, 'manifest.json');
const manifest = JSON.parse(fs.readFileSync(file, 'utf8'));
const entries = [
  { path: 'visual/assets/build-v5.js', role: 'verification_script', required: false, language: 'neutral' },
  { path: 'visual/assets/build-v6.js', role: 'verification_script', required: false, language: 'neutral' },
  { path: 'visual/assets/embed-v5-html.js', role: 'verification_script', required: false, language: 'neutral' },
  { path: 'visual/assets/enrich-v6-data.js', role: 'verification_script', required: false, language: 'neutral' },
  { path: 'visual/assets/qa-v5-html.js', role: 'verification_script', required: false, language: 'neutral' },
  { path: 'visual/assets/register-v5-manifest.js', role: 'verification_script', required: false, language: 'neutral' },
  { path: 'visual/assets/refresh-v6-evidence.js', role: 'verification_script', required: false, language: 'neutral' },
  { path: 'visual/assets/two-answers-v5.css', role: 'asset', required: true, language: 'neutral' },
  { path: 'visual/assets/two-answers-v5.js', role: 'asset', required: true, language: 'neutral' },
  { path: 'assets/figures/hero-s7-assembly.png', role: 'proposal_figure', required: true, language: 'zh' },
  { path: 'assets/figures/hero-s7-assembly.en.png', role: 'proposal_figure', required: true, language: 'en', translation_of: 'assets/figures/hero-s7-assembly.png' },
];

manifest.files = manifest.files.filter((item) => item.path !== 'visual/assets/enrich-v5-data.js');

for (const entry of entries) {
  const target = manifest.files.find((item) => item.path === entry.path) || entry;
  Object.assign(target, entry);
  target.sha256 ||= 'pending';
  if (!manifest.files.includes(target)) manifest.files.push(target);
}
manifest.files.sort((a, b) => a.path.localeCompare(b.path));
for (const entry of manifest.files) {
  if (entry.path === 'manifest.json') { delete entry.sha256; continue; }
  const source = path.join(root, entry.path);
  if (fs.existsSync(source)) entry.sha256 = crypto.createHash('sha256').update(fs.readFileSync(source)).digest('hex');
}
manifest.generated_at = '2026-08-18T08:00:00Z';
fs.writeFileSync(file, `${JSON.stringify(manifest, null, 2)}\n`);
console.log(`registered ${entries.length} V7 build files and removed the obsolete V5 generator`);
