const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ROOT = path.resolve(__dirname, '..', '..');
const manifestFile = path.join(ROOT,'manifest.json');
const manifest = JSON.parse(fs.readFileSync(manifestFile,'utf8'));
const entries = [
  ['assets/figures/concept-t2-v9.webp','asset',true,'neutral'],
  ['assets/figures/concept-s2-v9.webp','asset',true,'neutral'],
  ['assets/figures/concept-s7-v9.webp','asset',true,'neutral'],
  ['assets/figures/concept-t2-v9-print.jpg','asset',false,'neutral'],
  ['assets/figures/concept-s2-v9-print.jpg','asset',false,'neutral'],
  ['assets/figures/concept-s7-v9-print.jpg','asset',false,'neutral'],
  ['visual/assets/e2-readiness.json','evidence_data',true,'neutral'],
  ['visual/assets/upgrade-v9-data.js','verification_script',false,'neutral'],
  ['visual/assets/build-v9.js','verification_script',false,'neutral'],
  ['visual/assets/embed-v9-html.js','verification_script',false,'neutral'],
  ['visual/assets/refresh-v9-evidence.js','verification_script',false,'neutral'],
  ['visual/assets/qa-v9.js','verification_script',false,'neutral'],
  ['visual/assets/register-v9-manifest.js','verification_script',false,'neutral'],
  ['visual/assets/two-answers-v9.css','asset',true,'neutral'],
];
for (const [filePath,role,required,language] of entries) {
  let item = manifest.files.find((x)=>x.path===filePath);
  if (!item) { item={path:filePath}; manifest.files.push(item); }
  Object.assign(item,{role,required,language});
  // File records must stay within the published manifest schema. Image origin,
  // rights and evidence limitations live in sources.json instead.
  delete item.source_type;
  delete item.geometry_role;
  delete item.status;
  delete item.rights_note;
}
manifest.files.sort((a,b)=>a.path.localeCompare(b.path));
for (const item of manifest.files) {
  if (item.path === 'manifest.json') { delete item.sha256; continue; }
  const target = path.join(ROOT,item.path);
  if (!fs.existsSync(target)) throw new Error(`manifest file missing: ${item.path}`);
  item.sha256 = crypto.createHash('sha256').update(fs.readFileSync(target)).digest('hex');
}
manifest.site_package_version = '0.4.0';
manifest.generated_at = '2026-08-18T12:30:00Z';
fs.writeFileSync(manifestFile,`${JSON.stringify(manifest,null,2)}\n`);

const sourcesFile = path.join(ROOT,'sources.json');
const sources = JSON.parse(fs.readFileSync(sourcesFile,'utf8'));
sources.sources = sources.sources.filter((x)=>x.id!=='V9-CONCEPT-EXPERIENCE');
sources.sources.push({
  id:'V9-CONCEPT-EXPERIENCE',
  publisher:'Participant / OpenAI built-in ImageGen workflow',
  date:'2026-08-18',
  source_type:'agent_generated_media',
  url:null,
  retrieved_at:'2026-08-18',
  license:'Participant-created concept media for this submission; use governed by submission rights and platform terms.',
  usage:'Three geometry-matched experiential views for T2 Verification Ring, S2 Translation Gate and S7 Receipt Porch.',
  files:['assets/figures/concept-t2-v9.webp','assets/figures/concept-s2-v9.webp','assets/figures/concept-s7-v9.webp'],
  method:'Built-in ImageGen with the corresponding local concept plan used as spatial reference; local vector labels are added separately.',
  limitations:'Concept-generated image, not a photograph, site survey, verified existing condition, dimensional proof, performance record or institutional commitment.',
});
fs.writeFileSync(sourcesFile,`${JSON.stringify(sources,null,2)}\n`);

// sources.json is updated above, so refresh all hashes once more before the
// manifest is frozen. This keeps the manifest deterministic and prevents the
// source registry from carrying the hash of its pre-V9 state.
for (const item of manifest.files) {
  if (item.path === 'manifest.json') { delete item.sha256; continue; }
  const target = path.join(ROOT,item.path);
  if (!fs.existsSync(target)) throw new Error(`manifest file missing: ${item.path}`);
  item.sha256 = crypto.createHash('sha256').update(fs.readFileSync(target)).digest('hex');
}
fs.writeFileSync(manifestFile,`${JSON.stringify(manifest,null,2)}\n`);
console.log(JSON.stringify({registered:entries.length,manifest_files:manifest.files.length,source:'V9-CONCEPT-EXPERIENCE'},null,2));
