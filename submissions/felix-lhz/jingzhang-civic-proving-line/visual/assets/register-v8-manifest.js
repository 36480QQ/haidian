const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const root = path.resolve(__dirname, '..', '..');
const manifestFile = path.join(root, 'manifest.json');
const manifest = JSON.parse(fs.readFileSync(manifestFile, 'utf8'));
const entries = [
  ['visual/assets/build-v8.js','verification_script',false,'neutral'],
  ['visual/assets/upgrade-v8-data.js','verification_script',false,'neutral'],
  ['visual/assets/embed-v8-html.js','verification_script',false,'neutral'],
  ['visual/assets/qa-v8.js','verification_script',false,'neutral'],
  ['visual/assets/register-v8-manifest.js','verification_script',false,'neutral'],
  ['visual/assets/two-answers-v8.css','asset',true,'neutral'],
];
for (const [filePath,role,required,language] of entries) {
  let item = manifest.files.find(x => x.path === filePath);
  if (!item) { item = {path:filePath}; manifest.files.push(item); }
  Object.assign(item,{role,required,language});
}
manifest.files.sort((a,b) => a.path.localeCompare(b.path));
for (const item of manifest.files) {
  if (item.path === 'manifest.json') { delete item.sha256; continue; }
  const target = path.join(root,item.path);
  if (fs.existsSync(target)) item.sha256 = crypto.createHash('sha256').update(fs.readFileSync(target)).digest('hex');
}
manifest.generated_at = '2026-08-18T10:00:00Z';
fs.writeFileSync(manifestFile, `${JSON.stringify(manifest,null,2)}\n`);
console.log(`registered ${entries.length} V8 build and runtime files`);
