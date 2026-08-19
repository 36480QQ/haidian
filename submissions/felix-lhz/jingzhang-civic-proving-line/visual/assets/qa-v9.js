const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ROOT = path.resolve(__dirname, '..', '..');
const read = (file) => JSON.parse(fs.readFileSync(file, 'utf8'));
const fail = (message) => { throw new Error(message); };
const hash = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const allowed = new Set(['ready_documented','pending_survey','pending_permit','pending_quote','not_built','not_field_run']);

const answers = read(path.join(__dirname,'two-answers.json'));
const atlas = read(path.join(__dirname,'spatial-atlas.json'));
const ready = read(path.join(__dirname,'e2-readiness.json'));
if (answers.schema_version !== '1.7.0' || atlas.schema_version !== '1.7.0' || ready.schema_version !== '1.7.0') fail('schema 1.7.0 required');
if (answers.scenarios.length !== 12) fail('12 scenarios required');
if (atlas.landmarks.length !== 3) fail('3 landmarks required');
if (ready.permit_checklist.length !== 8 || ready.bill_of_components.length !== 16 || ready.forms.length !== 5 || ready.procurement_packages.length !== 4) fail('E2 readiness counts mismatch');
if (ready.prototype_readiness !== 'ready_documented' || ready.field_status !== 'not_field_run') fail('E2 status semantics mismatch');
if (!ready.permitted_states.every((x)=>allowed.has(x))) fail('unsupported readiness status');

const ids = new Set();
for (const name of ['roads.geojson','public_space.geojson','buildings.geojson','constraints.geojson','green_space.geojson','key_areas.geojson','land_use.geojson','phasing.geojson','site_boundary.geojson']) {
  const file = path.join(ROOT,'geometry',name);
  const data = read(file);
  for (const feature of data.features || []) ids.add(String(feature.id || feature.properties?.id || ''));
}
const missingGeometry = [];
for (const scene of answers.scenarios) {
  for (const key of ['prototype_readiness','readiness_gate','survey_dependency','permit_checklist','bill_of_components','quantity_formula','procurement_package_ref','baseline_form_ref','trial_form_ref','incident_form_ref','recovery_drill_ref','receipt_template_ref','e2_status']) if (!(key in scene)) fail(`${scene.id} missing ${key}`);
  if (!allowed.has(scene.prototype_readiness) || !allowed.has(scene.e2_status)) fail(`${scene.id} invalid readiness state`);
  if (scene.evidence_status !== 'not_field_run') fail(`${scene.id} must remain not_field_run`);
  for (const ref of scene.geometry_refs || []) if (/^V[57]-/.test(ref) && !ids.has(ref)) missingGeometry.push(`${scene.id}:${ref}`);
}
if (missingGeometry.length) fail(`unresolved geometry refs: ${missingGeometry.slice(0,8).join(', ')}`);
const s7 = answers.scenarios.find((x)=>x.code==='S7');
if (!s7 || s7.e2_status !== 'ready_documented' || s7.prototype_readiness !== 'ready_documented') fail('S7 E2 dossier must be ready_documented');
if (s7.bill_of_components.length !== 16 || s7.permit_checklist.length !== 8 || s7.procurement_package_ref.length !== 4) fail('S7 E2 references incomplete');

const canonical = ['site-overview','land-use-structure','key-areas','mobility-bluegreen','metrics-evidence'];
for (const lang of ['zh','en']) {
  const suffix = lang==='en'?'.en.png':'.png';
  const files = canonical.map((name)=>path.join(ROOT,'assets','figures',`${name}${suffix}`));
  files.forEach((file)=>{ if(!fs.existsSync(file) || fs.statSync(file).size < 20000) fail(`missing or undersized ${file}`); });
  const hashes = files.map(hash);
  if (new Set(hashes).size !== files.length) fail(`duplicate canonical figure in ${lang}`);
}
for (const name of ['t2','s2','s7']) for (const ext of ['webp','jpg']) {
  const file = path.join(ROOT,'assets','figures',ext==='jpg'?`concept-${name}-v9-print.jpg`:`concept-${name}-v9.webp`);
  if (!fs.existsSync(file) || fs.statSync(file).size < 50000) fail(`missing concept asset ${file}`);
}

for (const name of ['a0-boards.pdf','a0-boards.en.pdf','a3-booklet.pdf','a3-booklet.en.pdf']) {
  const file = path.join(ROOT,'drawings',name);
  if (!fs.existsSync(file)) fail(`missing PDF ${name}`);
  if (fs.statSync(file).size >= 6*1024*1024) fail(`${name} exceeds 6 MiB`);
}
for (const file of [path.join(ROOT,'visual','index.html'),path.join(ROOT,'visual','index.en.html'),path.join(ROOT,'report','proposal.html'),path.join(ROOT,'report','proposal.en.html')]) {
  const text = fs.readFileSync(file,'utf8');
  if (/<(?:script|img|link|iframe)[^>]+(?:src|href)=["']https?:\/\//i.test(text)) fail(`runtime remote request in ${file}`);
  if (!text.includes('V9') || !text.includes('E2')) fail(`V9/E2 first-screen evidence missing in ${file}`);
}

function size(dir) { return fs.readdirSync(dir,{withFileTypes:true}).reduce((sum,item)=>sum+(item.isDirectory()?size(path.join(dir,item.name)):fs.statSync(path.join(dir,item.name)).size),0); }
const packageBytes = size(ROOT);
if (packageBytes >= 38*1024*1024) fail(`package exceeds 38 MiB: ${packageBytes}`);

console.log(JSON.stringify({ ok:true, schema:'1.7.0', scenarios:12, landmarks:3, geometry_ids:ids.size, e2:{components:16,permits:8,forms:5,packages:4}, canonical_figures:10, pdf_under_6_mib:true, package_mib:Number((packageBytes/1024/1024).toFixed(2)) },null,2));
