const fs=require('fs');
const path=require('path');
const crypto=require('crypto');
const {run:runAudit}=require('./spatial-audit-v11');
const ROOT=path.resolve(__dirname,'..','..');
const fail=m=>{throw new Error(m)};
const read=rel=>JSON.parse(fs.readFileSync(path.join(ROOT,rel),'utf8'));
const sha=rel=>crypto.createHash('sha256').update(fs.readFileSync(path.join(ROOT,rel))).digest('hex');
const decision=runAudit();
if(decision.schema_version!=='1.9.0')fail('spatial-decision schema is not 1.9.0');
const counts=decision.alternatives.reduce((m,a)=>(m[a.decision]=(m[a.decision]||0)+1,m),{});
if(counts.reject_design!==1||counts.revise_design!==1||counts.advance_design!==1)fail(`decision diversity failed ${JSON.stringify(counts)}`);
if(decision.summary.input_hash!=='3c4c466bf8dc2b03b14ff69dd77b5c6d86c1fd93cb68665296b95bbd3098c38c')fail('spatial input hash drifted');

const ids=new Set();
for(const rel of ['geometry/roads.geojson','geometry/public_space.geojson','geometry/constraints.geojson'])for(const f of read(rel).features)ids.add(f.id||f.properties?.id);
for(const a of decision.alternatives)for(const ref of a.geometry_refs){const id=ref.split('#')[1];if(!ids.has(id))fail(`unresolved geometry ref ${ref}`)}
const answers=read('visual/assets/two-answers.json');
if(answers.schema_version!=='1.11.0')fail('two-answers schema is not 1.11.0');
if(!Array.isArray(answers.scenarios)||answers.scenarios.length!==12)fail('scenario count is not 12');
const allowedThreshold=new Set(['design_invariant','zero_tolerance','pending_baseline_committee']);
for(const scene of answers.scenarios){
  if(!scene.measurement_contract)fail(`missing measurement contract ${scene.code}`);
  if(!allowedThreshold.has(scene.threshold_status))fail(`invalid threshold status ${scene.code}`);
  if(scene.field_status!=='not_field_run'||scene.measurement_contract.field_status!=='not_field_run')fail(`field status drift ${scene.code}`);
  for(const key of ['measurement_question','numerator','denominator','baseline_window','comparison_design','sample_rule','collection_frequency','stratifiers','statistic','threshold_rule','threshold_status','zero_tolerance_events','missing_data_rule','human_review','public_output_schema','owner_roles','field_status'])if(scene.measurement_contract[key]===undefined)fail(`incomplete contract ${scene.code}.${key}`);
}
const metrics=read('metrics.json').metrics;
for(const id of ['east_west_stitch_count','spatial_component_type_count','receipt_landmark_count','s7_prototype_kit_item_count','s7_pilot_phase_count','measurement_contract_count','field_verification_result_count','spatial_hard_gate_evaluation_count','rejected_spatial_alternative_count','revised_spatial_alternative_count','advanced_spatial_alternative_count'])if(!metrics[id])fail(`missing restored metric ${id}`);
for(const id of ['task_completion_rate','accessibility_parity_gap','safety_event_rate_per_100_tasks','human_intervention_rate','resource_per_completed_task','grievance_recovery_time'])if(metrics[id]?.status!=='unknown'||metrics[id]?.value!==null)fail(`field metric is not unknown ${id}`);
require('./semantic-qa-v13');

const core=['site-overview','land-use-structure','key-areas','mobility-bluegreen','metrics-evidence'];
for(const lang of ['','.en'])for(const name of core)if(!fs.existsSync(path.join(ROOT,`assets/figures/${name}${lang}.png`)))fail(`missing core figure ${name}${lang}`);
for(const lang of ['','.en']){
  const hashes=core.map(name=>sha(`assets/figures/${name}${lang}.png`));
  if(new Set(hashes).size!==hashes.length)fail(`duplicate core figure content ${lang||'zh'}`);
}

for(const rel of ['visual/index.html','visual/index.en.html']){
  const html=fs.readFileSync(path.join(ROOT,rel),'utf8');
  if(/<(iframe|form)\b/i.test(html)||/\b(fetch|XMLHttpRequest)\s*\(/.test(html))fail(`${rel} contains forbidden runtime`);
  if(/(?:src|href)=["']https?:\/\//i.test(html))fail(`${rel} contains remote dependency`);
  if((html.match(/<link\b[^>]*stylesheet/g)||[]).length!==1||(html.match(/<script\b[^>]*src=/g)||[]).length!==1)fail(`${rel} does not use exactly one local CSS and JS`);
  for(const token of ['data-alt="ALT-A"','data-alt="ALT-B"','data-alt="ALT-C"','data-mode="baseline"','data-mode="ai"','data-mode="compare"','NOT FIELD-RUN','decision-data','alternative-data','cutaway-proof','ALT-A REJECT','ALT-C ADVANCE'])if(!html.includes(token))fail(`${rel} missing ${token}`);
}
const css=fs.readFileSync(path.join(ROOT,'visual/assets/v11.css'),'utf8');
const js=fs.readFileSync(path.join(ROOT,'visual/assets/v11.js'),'utf8');
if(!css.includes('prefers-reduced-motion')||!css.includes(':focus-visible'))fail('accessibility CSS incomplete');
if(!js.includes('location.hash')||!js.includes('hashchange')||!js.includes('ArrowRight'))fail('hash/keyboard interaction incomplete');

const manifest=read('manifest.json');
for(const item of manifest.files)if(!fs.existsSync(path.join(ROOT,item.path)))fail(`manifest points to missing file ${item.path}`);
function size(dir){return fs.readdirSync(dir,{withFileTypes:true}).reduce((s,e)=>s+(e.isDirectory()?size(path.join(dir,e.name)):fs.statSync(path.join(dir,e.name)).size),0)}
const bytes=size(ROOT);if(bytes>=38*1024*1024)fail(`package too large ${(bytes/1048576).toFixed(2)} MiB`);
if(!fs.existsSync(path.join(ROOT,'assets/media/dazhongsi-alt-c-v13.webp')))fail('missing V13 ALT-C concept view');
console.log(JSON.stringify({ok:true,schema:'1.11.0',measurement_contracts:12,field_results:0,metrics:Object.keys(metrics).length,decision_counts:counts,input_hash:decision.summary.input_hash,scenarios:12,core_figures:10,html:'static-offline-pass',browser_runtime:'user_review_required_file_url_policy',package_mib:Number((bytes/1048576).toFixed(2))},null,2));
