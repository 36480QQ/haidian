const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const pkg = path.resolve(__dirname, '..', '..');
const assets = path.join(pkg, 'visual', 'assets');
const figures = path.join(pkg, 'assets', 'figures');
const atlas = JSON.parse(fs.readFileSync(path.join(assets, 'spatial-atlas.json'), 'utf8'));
const answers = JSON.parse(fs.readFileSync(path.join(assets, 'two-answers.json'), 'utf8'));
const zh = fs.readFileSync(path.join(pkg, 'visual', 'index.html'), 'utf8');
const en = fs.readFileSync(path.join(pkg, 'visual', 'index.en.html'), 'utf8');
const reportZh = fs.readFileSync(path.join(pkg, 'report', 'proposal.html'), 'utf8');
const reportEn = fs.readFileSync(path.join(pkg, 'report', 'proposal.en.html'), 'utf8');
const errors = [];
const assert = (condition, message) => { if (!condition) errors.push(message); };

assert(atlas.schema_version === '1.6.0' && answers.schema_version === '1.6.0', 'schema must be 1.6.0');
assert(atlas.landmarks?.length === 3, 'three landmarks required');
assert(new Set(atlas.landmarks?.map(x => x.spatial_archetype)).size === 3, 'landmark archetypes must be distinct');
assert(answers.annual_program?.length === 4, 'four seasonal programmes required');
assert(answers.pilot_protocol?.phases?.length === 5, 'five 90-day pilot phases required');
assert(answers.scenarios?.length === 12, 'twelve stable scenarios required');

const scenarioIds = new Set(answers.scenarios.map(x => x.id));
const componentIds = new Set((atlas.components || []).map(x => x.id));
for (const landmark of atlas.landmarks || []) {
  for (const id of landmark.scene_refs || []) assert(scenarioIds.has(id), `missing scene ref ${id}`);
  for (const id of [...(landmark.public_baseline_refs || []), ...(landmark.ai_plugin_refs || []), ...(landmark.evidence_interface_refs || [])]) assert(componentIds.has(id), `missing component ref ${id}`);
}

const geometryIds = new Set(['roads.geojson','public_space.geojson','buildings.geojson','constraints.geojson']
  .flatMap(name => JSON.parse(fs.readFileSync(path.join(pkg, 'geometry', name), 'utf8')).features)
  .map(x => String(x.id || x.properties?.id || '')));
const activeRefs = [...new Set(JSON.stringify([atlas, answers]).match(/V\d+-D-[A-Z0-9-]+/g) || [])];
for (const id of activeRefs) assert(geometryIds.has(id), `unresolved design geometry ${id}`);
assert(!activeRefs.some(id => id.startsWith('V5-D-')), 'active V5-D references are forbidden');

for (const [name, html] of [['visual zh',zh],['visual en',en]]) {
  assert(html.includes('v8-first-look'), `${name} lacks V8 first screen`);
  assert((html.match(/class="v8-landmark"/g) || []).length === 3, `${name} lacks three landmark cards`);
  assert(['OPEN','TRIAL','PAUSE','RETIRE'].every(x => html.includes(`data-state-view="${x}"`)), `${name} lacks four state controls`);
  assert(html.includes('two-answers-v8.css'), `${name} lacks V8 stylesheet`);
  const remoteRuntime = [...html.matchAll(/(?:src|href)="(https?:\/\/[^\"]+)"/g)].map(x => x[1]);
  assert(remoteRuntime.length === 0, `${name} contains remote runtime dependencies: ${remoteRuntime.join(', ')}`);
}
assert(reportZh.includes('V8_EXEC_START') && reportEn.includes('V8_EXEC_START'), 'reports lack V8 executive entry');
assert((reportZh.match(/Agent [1-6]/g) || []).length >= 6 && (reportEn.match(/Agent [1-6]/g) || []).length >= 6, 'reports lack six-task index');

const canonical = ['site-overview','land-use-structure','key-areas','mobility-bluegreen','metrics-evidence','culture-brand','ecosystem-synergy','implementation-roadmap'];
for (const suffix of ['', '.en']) {
  const hashes = canonical.map(name => ({name, hash: crypto.createHash('sha256').update(fs.readFileSync(path.join(figures, `${name}${suffix}.png`))).digest('hex')}));
  const groups = new Map();
  for (const item of hashes) groups.set(item.hash, [...(groups.get(item.hash) || []), item.name]);
  for (const names of groups.values()) assert(names.length === 1, `duplicate ${suffix || 'zh'} figures: ${names.join(', ')}`);
}

const result = {
  ok: errors.length === 0,
  schema: atlas.schema_version,
  landmarks: atlas.landmarks?.length,
  annual_programmes: answers.annual_program?.length,
  pilot_phases: answers.pilot_protocol?.phases?.length,
  scenarios: answers.scenarios?.length,
  active_geometry_refs: activeRefs.length,
  design_geometry_objects: [...geometryIds].filter(x => x.startsWith('V7-D-')).length,
  errors,
};
console.log(JSON.stringify(result, null, 2));
process.exit(result.ok ? 0 : 1);
