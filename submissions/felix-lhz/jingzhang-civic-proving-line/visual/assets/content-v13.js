const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const read = rel => JSON.parse(fs.readFileSync(path.join(ROOT, rel), 'utf8'));
const write = (rel, value) => fs.writeFileSync(path.join(ROOT, rel), JSON.stringify(value, null, 2) + '\n');

const restoredMetrics = {
  east_west_stitch_count:[6,'count','geometry/roads.geojson','count(features where function=conceptual_east_west_stitch)','A-SPATIAL-ATLAS-001'],
  spatial_component_type_count:[9,'count','visual/assets/spatial-atlas.json','count(component_catalog)','A-SPATIAL-ATLAS-001'],
  receipt_landmark_count:[3,'count','visual/assets/spatial-atlas.json','count(landmarks)','A-V8-LANDMARKS'],
  hero_operating_state_count:[4,'count','visual/assets/spatial-atlas.json','count(OPEN, TRIAL, PAUSE, RETIRE)',null],
  evidence_ladder_level_count:[5,'count','visual/assets/two-answers.json','count(E0..E4 evidence levels)',null],
  s7_review_scale_count:[5,'count','visual/assets/spatial-atlas.json','count(1:5000, 1:2000, 1:500, 1:200, 1:50/assembly)','A-SPATIAL-ATLAS-001'],
  ordinary_baseline_coverage_count:[12,'count','visual/assets/two-answers.json','count(scenarios with non-empty ordinary_answer)',null],
  human_review_coverage_count:[12,'count','visual/assets/two-answers.json','count(scenarios with non-empty human_responsibility)',null],
  stop_condition_coverage_count:[12,'count','visual/assets/two-answers.json','count(scenarios with non-empty stop_conditions)',null],
  s7_prototype_kit_item_count:[16,'count','visual/assets/e2-readiness.json','count(bill_of_components)','ASM-V9-E2'],
  e2_permit_gate_count:[8,'count','visual/assets/e2-readiness.json','count(permit_checklist)','ASM-V9-E2'],
  e2_printable_form_count:[5,'count','visual/assets/e2-readiness.json','count(forms where printable=true)','ASM-V9-E2'],
  e2_procurement_package_count:[4,'count','visual/assets/e2-readiness.json','count(procurement_packages)','ASM-V9-E2'],
  s7_pilot_phase_count:[5,'count','visual/assets/two-answers.json','count(pilot_protocol.phases)','A-V8-OPERATIONS'],
  synthetic_design_verification_case_count:[84,'count','visual/assets/tabletop-results.json','count(12 scenarios × 7 deterministic design-contract cases)','ASM-V10-SYNTHETIC'],
  spatial_hard_gate_evaluation_count:[21,'count','visual/assets/spatial-decision.json','3 alternatives × 7 geometry hard gates','ASM-V11-PROTOTYPE-DIMENSIONS'],
  rejected_spatial_alternative_count:[1,'count','visual/assets/spatial-decision.json','count(decision=reject_design)','ASM-V11-PROTOTYPE-DIMENSIONS'],
  revised_spatial_alternative_count:[1,'count','visual/assets/spatial-decision.json','count(decision=revise_design)','ASM-V11-PROTOTYPE-DIMENSIONS'],
  advanced_spatial_alternative_count:[1,'count','visual/assets/spatial-decision.json','count(decision=advance_design)','ASM-V11-PROTOTYPE-DIMENSIONS'],
  alt_c_public_route_length_m:[372,'m','visual/assets/spatial-decision.json','sum(length(ALT-C OPEN public routes) in local metre projection)','ASM-V11-PROTOTYPE-DIMENSIONS'],
  alt_c_trial_area_sqm:[2496,'sqm','visual/assets/spatial-decision.json','polygon_area(ALT-C trial boundary in local metre projection)','ASM-V11-PROTOTYPE-DIMENSIONS'],
  alt_c_reversible_buffer_area_sqm:[3840,'sqm','visual/assets/spatial-decision.json','polygon_area(ALT-C reversible buffer in local metre projection)','ASM-V11-PROTOTYPE-DIMENSIONS'],
  alt_c_max_estop_staff_distance_m:[24.331,'m','visual/assets/spatial-decision.json','max(min(distance(E-stop, human post)))','ASM-V11-PROTOTYPE-DIMENSIONS']
};

function updateSchemasAndMetrics(){
  for(const rel of ['visual/assets/two-answers.json','visual/assets/spatial-atlas.json']){
    const data=read(rel); data.schema_version='1.11.0'; data.publication_version='spatial_decision_table_release'; write(rel,data);
  }
  const doc=read('metrics.json');
  for(const [id,[value,unit,source,formula,assumption]] of Object.entries(restoredMetrics)){
    doc.metrics[id]={status:'known',value,unit,source_files:[source],formula,confidence:'high',assumptions:assumption?[assumption]:[]};
  }
  doc.schema_version='1.11.0'; write('metrics.json',doc);
}

function replaceOnce(text, before, after, label){
  if(text.includes(before)) return text.replace(before,after);
  if(text.includes(after)) return text;
  throw new Error(`V13 narrative anchor missing: ${label}`);
}

function updateNarrative(){
  const files=[['proposal.md','zh'],['proposal.en.md','en']];
  for(const [rel,lang] of files){
    let s=fs.readFileSync(path.join(ROOT,rel),'utf8');
    if(lang==='zh'){
      s=s.replace(/^summary:.*$/m,'summary: "三个方案接受同一把尺子；牺牲公共路径的方案被公开否决，入选方案再接受十二份测量契约。"');
      s=replaceOnce(s,'S7 以 1:5000、1:2000、1:500、1:200、1:50 节点和装配轴测承担实施样板；12 个场景各运行 7 类确定性桌面用例，形成 84 项可复跑的合成设计契约验证，不增加场景数量。[metric:measurement_contract_count] [metric:key_area_count]','S7 以五级审查尺度承担实施样板；12 个场景各运行 7 类确定性桌面用例，形成 84 项可复跑验证。五级尺度与 84 项验证分别引用其可复算指标，不用场景数替代空间深度。[metric:s7_review_scale_count] [metric:synthetic_design_verification_case_count]','opening metrics zh');
      s=replaceOnce(s,'[metric:rejected_spatial_alternative_count] [metric:advanced_spatial_alternative_count] [data:geometry/public_space.geojson#V11-ALT-C-TRIAL-1]','[metric:rejected_spatial_alternative_count] [metric:revised_spatial_alternative_count] [metric:advanced_spatial_alternative_count] [metric:alt_c_public_route_length_m] [metric:alt_c_trial_area_sqm] [metric:alt_c_reversible_buffer_area_sqm] [metric:alt_c_max_estop_staff_distance_m] [data:geometry/public_space.geojson#V11-ALT-C-TRIAL-1]','decision metrics zh');
      s=s.replace('[data:geometry/roads.geojson#STITCH-01] [metric:key_area_count]','[data:geometry/roads.geojson#STITCH-01] [metric:east_west_stitch_count]');
      s=s.replace('[data:visual/assets/spatial-atlas.json] [metric:paired_scenario_count]','[data:visual/assets/spatial-atlas.json] [metric:spatial_component_type_count]');
      s=s.replace('[data:visual/assets/spatial-atlas.json] [metric:measurement_contract_count]\n\n“编译器”','[data:visual/assets/spatial-atlas.json] [metric:s7_review_scale_count] [metric:s7_prototype_kit_item_count] [metric:e2_permit_gate_count] [metric:e2_printable_form_count] [metric:e2_procurement_package_count]\n\n“编译器”');
      s=s.replace('[data:visual/assets/tabletop-results.json] [metric:measurement_contract_count]','[data:visual/assets/tabletop-results.json] [metric:synthetic_design_verification_case_count]');
      s=s.replace('任一阶段的失败门触发暂停或返回前一阶段。[data:visual/assets/two-answers.json] [metric:measurement_contract_count]','任一阶段的失败门触发暂停或返回前一阶段。[data:visual/assets/two-answers.json] [metric:s7_pilot_phase_count]');
      s=s.replace('证据按 `E0 public source → E1 concept design → E2 documented prototype ready → E3 controlled trial pending → E4 civic adoption pending` 五级推进。','证据按 `E0 public source → E1 concept design → E2 documented prototype ready → E3 controlled trial pending → E4 civic adoption pending` 五级推进。[metric:evidence_ladder_level_count]');
    }else{
      s=s.replace(/^summary:.*$/m,'summary: "Three alternatives face one ruler: a design that sacrifices the public route is publicly rejected, and the selected design then faces twelve measurement contracts."');
      s=replaceOnce(s,'Three unmistakable receipt landmarks—Zhongzhiyuan Verification Ring, AI Origin Translation Gate and Dazhongsi Receipt Porch—remain the spatial prototypes. S7 adds a 1:50 construction node to its 1:5000, 1:2000, 1:500, 1:200 and assembly views. Twelve scenarios each run seven deterministic tabletop cases, producing 84 rerunnable synthetic design-contract checks without adding scenes.[data:visual/assets/two-answers.json] [data:visual/assets/spatial-atlas.json] [metric:measurement_contract_count]','Three unmistakable receipt landmarks—Zhongzhiyuan Verification Ring, AI Origin Translation Gate and Dazhongsi Receipt Porch—remain the spatial prototypes. S7 carries five review scales; 12 scenes each run seven deterministic tabletop cases, producing 84 rerunnable checks. Scale and verification cite their own recomputable metrics rather than generic scene counts.[data:visual/assets/two-answers.json] [data:visual/assets/spatial-atlas.json] [metric:s7_review_scale_count] [metric:synthetic_design_verification_case_count]','opening metrics en');
      s=replaceOnce(s,'[metric:rejected_spatial_alternative_count] [metric:advanced_spatial_alternative_count] [data:geometry/public_space.geojson#V11-ALT-C-TRIAL-1]','[metric:rejected_spatial_alternative_count] [metric:revised_spatial_alternative_count] [metric:advanced_spatial_alternative_count] [metric:alt_c_public_route_length_m] [metric:alt_c_trial_area_sqm] [metric:alt_c_reversible_buffer_area_sqm] [metric:alt_c_max_estop_staff_distance_m] [data:geometry/public_space.geojson#V11-ALT-C-TRIAL-1]','decision metrics en');
      s=s.replace('[data:geometry/roads.geojson#STITCH-01] [metric:key_area_count]','[data:geometry/roads.geojson#STITCH-01] [metric:east_west_stitch_count]');
      s=s.replace('[data:visual/assets/spatial-atlas.json] [metric:paired_scenario_count]','[data:visual/assets/spatial-atlas.json] [metric:spatial_component_type_count]');
      s=s.replace('[data:visual/assets/spatial-atlas.json] [metric:measurement_contract_count]\n\nThe compiler','[data:visual/assets/spatial-atlas.json] [metric:s7_review_scale_count] [metric:s7_prototype_kit_item_count] [metric:e2_permit_gate_count] [metric:e2_printable_form_count] [metric:e2_procurement_package_count]\n\nThe compiler');
      s=s.replace('[data:visual/assets/tabletop-results.json] [metric:measurement_contract_count]','[data:visual/assets/tabletop-results.json] [metric:synthetic_design_verification_case_count]');
      s=s.replace('Any failed gate pauses or returns the pilot.[data:visual/assets/two-answers.json] [metric:measurement_contract_count]','Any failed gate pauses or returns the pilot.[data:visual/assets/two-answers.json] [metric:s7_pilot_phase_count]');
      s=s.replace('Evidence progresses through `E0 public source → E1 concept design → E2 documented prototype ready → E3 controlled trial pending → E4 civic adoption pending`.','Evidence progresses through `E0 public source → E1 concept design → E2 documented prototype ready → E3 controlled trial pending → E4 civic adoption pending`.[metric:evidence_ladder_level_count]');
    }
    s=s.replace(/## 可测量的双答：十二份现场契约，不是十二个口号/,'## 入选之后再测量：十二份现场契约');
    s=s.replace(/## Measurable Two Answers: Twelve Field Contracts, Not Twelve Slogans/,'## Measure after selection: twelve field contracts');
    // Normalize generated citations so repeated builds are byte-stable and a
    // paragraph never cites the same metric more than once.
    s=s.replace(/(?:\s*\[metric:east_west_stitch_count\])+(?=\s*每座)/,' ');
    s=s.replace(/links(?:\[metric:east_west_stitch_count\])+(?= between)/,'links');
    s=s.replace(/(?:\s*\[metric:spatial_component_type_count\])+(?=\s*每项)/,' ');
    s=s.replace(/exhibit\.(?:\[metric:spatial_component_type_count\])+(?= Each)/,'exhibit.');
    s=s.replace(/(?:\[metric:evidence_ladder_level_count\])+\s*(?=S7)/,'[metric:evidence_ladder_level_count] ');
    s=s.replace(/固定空间地址：\s*(?=每座)/,'固定空间地址：');
    s=s.replace(/交互展；\s*(?=每项)/,'交互展；');
    s=s.replace(/退役资产去向。\[data:visual\/assets\/spatial-atlas\.json\](?! \[metric:spatial_component_type_count\])/,'退役资产去向。[data:visual/assets/spatial-atlas.json] [metric:spatial_component_type_count]');
    s=s.replace(/retirement destination\.\[data:visual\/assets\/spatial-atlas\.json\](?! \[metric:spatial_component_type_count\])/,'retirement destination.[data:visual/assets/spatial-atlas.json] [metric:spatial_component_type_count]');
    s=s.split(/(\n\n+)/).map(part=>{
      if(/^\n+$/.test(part))return part;
      const seen=new Set();
      return part.replace(/\[metric:([a-z0-9_]+)\]/g,(all,id)=>seen.has(id)?'':(seen.add(id),all));
    }).join('');
    fs.writeFileSync(path.join(ROOT,rel),s);
  }
}

function updateMatrices(){
  const matrix=read('compliance_matrix.json');
  const map={
    'agent.1':['east_west_stitch_count','receipt_landmark_count'],
    'agent.2':['receipt_landmark_count','measurement_contract_count'],
    'agent.3':['measurement_contract_count','synthetic_design_verification_case_count'],
    'agent.4':['spatial_hard_gate_evaluation_count','advanced_spatial_alternative_count'],
    'agent.5':['east_west_stitch_count','spatial_component_type_count'],
    'agent.6':['s7_pilot_phase_count','e2_permit_gate_count']
  };
  for(const row of matrix.requirements||[]) if(map[row.requirement_id]) row.metrics=map[row.requirement_id];
  delete matrix.v12_evidence_index;
  matrix.v13_evidence_index={version:'spatial_decision_table_release',primary_judgement:'ALT-A reject / ALT-B revise / ALT-C advance',secondary_evidence:'12/12 measurement contracts; 0 field results',semantic_metric_assertions:'visual/assets/semantic-qa-v13.js'};
  write('compliance_matrix.json',matrix);
}

function updateSourcesAndRights(){
  const sources=read('sources.json');
  const entry={
    id:'GENERATED-DAZHONGSI-ALT-C-V13',publisher:'OpenAI built-in image generation',date:'2026-08-20',
    path:'assets/media/dazhongsi-alt-c-v13.webp',source_type:'ai_generated_visual',
    license:'Competition display only; subject to platform and competition terms',
    usage:'ALT-C concept communication only; not a photograph, survey, consultation record, field result or approval evidence.',
    limitations:'The experience view follows the public cross, southeast one-side trial bay, southwest staffed receipt porch and eastward removal route, but all dimensions and existing context require survey and professional review.',
    prompt_summary:'Elevated architectural cutaway of an unobstructed cross-shaped step-free public route, southeast removable amber low-speed trial bay, southwest staffed blue receipt porch, dual E-stops, tactile guidance, rain gardens and an eastward equipment-removal route; no text or logos; concept rendering only.'
  };
  sources.sources=(sources.sources||[]).filter(x=>x.id!==entry.id).concat(entry); write('sources.json',sources);
  const rightsPath=path.join(ROOT,'report/copyright_statement.md');
  let rights=fs.readFileSync(rightsPath,'utf8');
  rights=rights.replace(/`assets\/media\/\*\.webp` were generated with OpenAI’s built-in image-generation tool on 2026-08-12\./,'`assets/media/*.webp` were generated with OpenAI’s built-in image-generation tool on 2026-08-12 and 2026-08-20.');
  if(!rights.includes('dazhongsi-alt-c-v13.webp')) rights += '\n- **V13 ALT-C experience view.** `assets/media/dazhongsi-alt-c-v13.webp` follows the selected design geometry as a generated concept view. It is not field evidence; vector plan, section and geometry audit remain authoritative for scale and selection.\n';
  fs.writeFileSync(rightsPath,rights);
}

function updateChangelog(){
  const p=path.join(ROOT,'changelog.md'); let s=fs.readFileSync(p,'utf8');
  if(!s.includes('V13 空间裁决台')) s=s.replace(/^(#.*\n)/,`$1\n## 2026-08-20 · V13 空间裁决台\n\n- 恢复 ALT-A 淘汰、ALT-B 修改、ALT-C 推进为空间主叙事；12份测量契约降为入选后的二级证据。\n- 恢复六缝合、九组件、三地标、五尺度、构件、许可、表单、试点与几何审计的精确指标，删除语义错配。\n- 重构五张核心图、四份正式PDF和双语HTML首屏；现场结果继续为0，未声称测绘、许可、采购或运行。\n\n`);
  fs.writeFileSync(p,s);
}

function run(){updateSchemasAndMetrics();updateNarrative();updateMatrices();updateSourcesAndRights();updateChangelog();console.log('V13 spatial-decision evidence and semantic metrics restored');}
module.exports={run,restoredMetrics};
if(require.main===module)run();
