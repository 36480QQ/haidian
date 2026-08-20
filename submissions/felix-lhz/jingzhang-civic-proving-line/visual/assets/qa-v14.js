const fs=require('fs');
const path=require('path');
const crypto=require('crypto');
const ROOT=path.resolve(__dirname,'..','..');
const read=rel=>fs.readFileSync(path.join(ROOT,rel));
const text=rel=>read(rel).toString('utf8');
const json=rel=>JSON.parse(text(rel));
const sha=rel=>crypto.createHash('sha256').update(read(rel)).digest('hex');
const ok=(condition,message)=>{if(!condition)throw new Error(message);};

const model=json('visual/assets/v14-spatial-model.json');
ok(model.field_status==='not_field_run','V14 model must remain not_field_run');
ok(model.landmarks.length===3,'V14 must contain three distinct landmarks');
ok(model.s7.public_routes.length===2,'S7 must contain two public routes');
ok(model.s7.public_routes.every(route=>route.clear_width_m>=4),'S7 public routes must preserve 4 m clear width');
ok(model.s7.trial_bay.assembly_state==='reversible','S7 trial bay must remain reversible');
ok(model.s7.fire_route.independent_of_trial,'Fire route must remain independent');
ok(model.s7.retirement_route.independent_of_public_cross,'Retirement route must remain independent');
ok(model.current_gate.decision==='no_go','Current gate must remain no-go');
ok(model.current_gate.closed_permit_count===0&&model.current_gate.required_permit_count===8,'Permit gate must truthfully remain 0/8');
ok(model.current_gate.baseline_days_recorded===0&&model.current_gate.required_baseline_days===7,'Baseline must truthfully remain 0/7');

const scenes=json('visual/assets/two-answers.json').scenarios;
ok(scenes.length===12,'All twelve scenarios must remain present');
ok(scenes.every(scene=>scene.field_status==='not_field_run'),'Every scenario must remain not_field_run');
ok(scenes.every(scene=>scene.ordinary_answer&&scene.ai_answer&&scene.human_responsibility&&scene.stop_conditions),'Every scenario needs paired answers, human responsibility and stop conditions');

const decision=json('visual/assets/spatial-decision.json');
const decisions=decision.alternatives.map(item=>item.decision);
ok(decisions.filter(x=>x==='reject_design').length>=1,'At least one spatial alternative must be rejected');
ok(decisions.filter(x=>x==='revise_design').length>=1,'At least one spatial alternative must require revision');
ok(decisions.filter(x=>x==='advance_design').length===1,'Exactly one spatial alternative may advance');

for(const rel of ['visual/index.html','visual/index.en.html']){
  const html=text(rel);
  ok(!/<(?:iframe|script|link)[^>]+(?:src|href)=["']https?:/i.test(html),`${rel} must not load remote runtime resources`);
  ok((html.match(/<article class="scene/g)||[]).length===12,`${rel} must expose twelve scene cards`);
  for(const state of ['OPEN','TRIAL','PAUSE','RETIRE'])ok(html.includes(`data-state="${state}"`),`${rel} missing ${state} control`);
  for(const alt of ['ALT-A','ALT-B','ALT-C'])ok(html.includes(`data-alt="${alt}"`),`${rel} missing ${alt} control`);
  ok(html.includes('URLSearchParams(location.hash.slice(1))'),`${rel} must restore state from URL hash`);
  ok(html.includes('prefers-reduced-motion'),`${rel} must respect reduced motion`);
  ok(html.includes('NOT FIELD-RUN'),`${rel} must disclose field status`);
}

const core=['site-overview','land-use-structure','key-areas','mobility-bluegreen','metrics-evidence'];
for(const language of ['', '.en']){
  const hashes=core.map(name=>sha(`assets/figures/${name}${language}.png`));
  ok(new Set(hashes).size===hashes.length,`Core ${language||'zh'} figures must not be exact duplicates`);
}

const sources=json('sources.json').sources;
for(const id of ['GENERATED-VERIFICATION-RING-V14','GENERATED-TRANSLATION-GATE-V14','GENERATED-RECEIPT-PORCH-V14']){
  const source=sources.find(item=>item.id===id);
  ok(source&&source.source_type==='ai_generated_visual',`Missing generated-image source record ${id}`);
  ok(fs.existsSync(path.join(ROOT,source.path)),`Missing generated-image asset for ${id}`);
}

const manifest=json('manifest.json');
const listed=new Set(manifest.files.map(item=>item.path));
for(const rel of ['visual/assets/v14-spatial-model.json','visual/assets/content-v14.js','visual/assets/build-v14.js','visual/assets/build-v14-html.js','visual/assets/qa-v14.js'])ok(listed.has(rel),`Manifest missing ${rel}`);

console.log(JSON.stringify({ok:true,landmarks:3,scenarios:12,current_gate:'G0_no_go',permits:'0/8',baseline:'0/7',core_figures_unique:true,offline_visual:true},null,2));
