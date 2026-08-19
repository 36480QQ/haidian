const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const read = rel => JSON.parse(fs.readFileSync(path.join(ROOT, rel), 'utf8'));
const write = (rel, value) => fs.writeFileSync(path.join(ROOT, rel), JSON.stringify(value, null, 2) + '\n');
const bi = (zh, en) => ({ zh, en });

const contracts = {
  T1: {
    question: bi('同一模型包由独立人员复现时，普通清单与 AI 助手哪一种能完成更多可核验步骤？', 'When independent operators reproduce the same model package, which mode completes more verifiable steps?'),
    denominator: bi('每个模型包的全部必需复现步骤', 'All required reproduction steps per model package'),
    baseline: bi('至少 3 个模型包；每包由 3 名独立人员各完成普通与 AI 两种模式', 'At least 3 model packages; 3 independent operators per package complete both modes'),
    comparison: 'paired_crossover_same_package',
    frequency: bi('每次运行记录；每个模型包结束后汇总', 'Record every run; aggregate after each package'),
    strata: ['model_package', 'operator', 'licence_class'], statistic: 'paired_completion_difference_and_human_minutes',
    zero: ['unlicensed_data_used', 'unlogged_external_connection', 'reproduction_environment_escape']
  },
  T2: {
    question: bi('同一路径与同一使用者下，机器人试验是否保持普通通行完整且不增加安全冲突？', 'For the same route and users, does the robot trial preserve baseline passage without adding safety conflicts?'),
    denominator: bi('每种模式 100 次符合准入条件的通行；所有严重事件另行全量保留', '100 eligible passages per mode; retain every severe event separately'),
    baseline: bi('普通模式与试验模式各 100 次，按轮椅、视障、步行和昼夜分层', '100 passages in baseline and trial modes, stratified by wheelchair, visual impairment, walking and day/night'),
    comparison: 'parallel_same_route_stratified', frequency: bi('每次通行记录；每日闭场复核', 'Record each passage; review at daily close'),
    strata: ['mobility_need', 'day_night', 'route_direction'], statistic: 'rate_per_100_passages_and_accessibility_parity_gap',
    zero: ['collision', 'person_enters_safety_buffer', 'emergency_stop_failure', 'baseline_route_blocked']
  },
  T3: {
    question: bi('正常、断网和降级状态下，端侧系统是否以可接受资源完成任务并可靠回退？', 'Under normal, offline and degraded states, does edge compute complete tasks with auditable resources and reliable fallback?'),
    denominator: bi('每种状态 30 个同题任务，并保留连续 7 日能耗与噪声日志', '30 same-task trials per state plus a continuous 7-day energy and noise log'),
    baseline: bi('正常、断网、降级三种状态各 30 次；同设备、同任务集', '30 trials in each normal, offline and degraded state; same device and task set'),
    comparison: 'three_state_repeated_tasks', frequency: bi('逐任务记录；能耗与噪声每分钟采样，按日汇总', 'Record each task; sample energy and noise each minute and aggregate daily'),
    strata: ['operating_state', 'task_class', 'day'], statistic: 'completion_rate_resource_per_completed_task_and_fallback_rate',
    zero: ['unsafe_overheat', 'unlogged_network_egress', 'fallback_unavailable']
  },
  S1: {
    question: bi('企业服务请求在人工窗口先成立时，AI 分诊是否减少未完成任务而不增加误分？', 'With the staffed desk operating first, does AI triage reduce incomplete enterprise-service requests without increasing misrouting?'),
    denominator: bi('每种模式 100 个符合准入条件的服务请求', '100 eligible service requests per mode'),
    baseline: bi('人工模式与 AI 辅助模式各 100 个同类请求，按事项复杂度分层', '100 comparable requests in staffed and AI-assisted modes, stratified by complexity'),
    comparison: 'matched_request_cohorts', frequency: bi('逐请求记录；每周人工抽查与公开汇总', 'Record each request; weekly human audit and public summary'),
    strata: ['request_class', 'complexity', 'language'], statistic: 'completion_rate_misrouting_rate_and_human_minutes',
    zero: ['legal_advice_without_review', 'eligible_user_denied_baseline_service', 'personal_data_overcollection']
  },
  S2: {
    question: bi('国际人才抵达任务中，无账户人工服务与可选 AI 导航哪种模式更完整、公平且可恢复？', 'For international arrivals, which mode is more complete, equitable and recoverable: no-account staffed service or optional AI guidance?'),
    denominator: bi('每种模式 100 个符合准入条件的抵达服务请求', '100 eligible arrival-service requests per mode'),
    baseline: bi('人工与 AI 辅助各 100 个请求，按语言、辅助需求和事项复杂度分层', '100 requests per mode, stratified by language, assistance need and complexity'),
    comparison: 'paired_service_script_or_matched_cohort', frequency: bi('逐请求记录；每日闭场复核争议样本', 'Record each request; review disputed cases at daily close'),
    strata: ['language', 'assistance_need', 'complexity'], statistic: 'completion_rate_accessibility_parity_gap_intervention_rate',
    zero: ['account_required_for_baseline', 'translation_changes_legal_meaning', 'human_review_unavailable']
  },
  S3: {
    question: bi('社区问题工作坊中，AI 匹配是否增加可核验知识连接而不替代居民议题决定？', 'In community workshops, does AI matching add verifiable knowledge links without replacing residents’ agenda decisions?'),
    denominator: bi('20 场完整工作坊及其全部问题—证据—决定记录', '20 complete workshops and all problem–evidence–decision records'),
    baseline: bi('至少 20 场，交替使用普通知识台账与 AI 辅助匹配', 'At least 20 workshops alternating baseline ledger and AI-assisted matching'),
    comparison: 'alternating_workshop_series', frequency: bi('逐场记录；每 5 场公开一次归档完整性', 'Record each workshop; publish archive completeness every 5 workshops'),
    strata: ['issue_type', 'participant_role', 'workshop_mode'], statistic: 'verified_link_rate_unresolved_issue_rate_and_human_review_minutes',
    zero: ['resident_agenda_overridden', 'unattributed_source_presented_as_fact', 'participant_identity_disclosed']
  },
  S4: {
    question: bi('文化讲解中，可选 AI 是否提高可达性，同时保持史实出处与人工纠错？', 'In heritage interpretation, does optional AI improve access while preserving provenance and human correction?'),
    denominator: bi('100 个讲解内容项，并全量复核所有争议项', '100 interpretation items plus every disputed item'),
    baseline: bi('同一 100 项分别由静态/人工讲解与 AI 可选讲解呈现', 'Present the same 100 items through static/staffed and optional-AI modes'),
    comparison: 'item_level_paired_review', frequency: bi('逐内容项记录；争议即时冻结并复核', 'Record each item; freeze and review disputes immediately'),
    strata: ['content_type', 'language', 'accessibility_format'], statistic: 'source_accuracy_accessibility_coverage_and_correction_time',
    zero: ['fabricated_historical_fact', 'missing_source_for_factual_claim', 'disputed_item_remains_public']
  },
  S5: {
    question: bi('动态辅助导航是否在不削弱静态导视的前提下，改善不同辅助需求的路线完成？', 'Does dynamic guidance improve route completion for different assistance needs without weakening static wayfinding?'),
    denominator: bi('10 条路线 × 3 类辅助需求 × 昼/夜两时段', '10 routes × 3 assistance-need groups × day/night'),
    baseline: bi('每个组合均完成普通静态导视与 AI 辅助两种模式', 'Each combination completes both static-baseline and AI-assisted modes'),
    comparison: 'paired_route_crossover', frequency: bi('逐路线记录；每个时段结束复核', 'Record every route; review at the end of each time band'),
    strata: ['route', 'assistance_need', 'day_night'], statistic: 'route_completion_accessibility_parity_gap_and_intervention_rate',
    zero: ['baseline_signage_obscured', 'unsafe_route_instruction', 'fallback_not_available']
  },
  S6: {
    question: bi('极端天气提示是否在遮阴、饮水和人工服务先成立后，提高正确服务抵达率？', 'After shade, water and staffed service operate, do weather prompts improve arrival at the correct service?'),
    denominator: bi('3 类天气条件，每类至少 30 个节点小时', 'Three weather classes with at least 30 node-hours each'),
    baseline: bi('常态、高温/强日照、降雨三类；普通静态服务与 AI 提示并行记录', 'Normal, heat/strong sun and rain; record baseline static service and AI prompts in parallel'),
    comparison: 'weather_stratified_node_hours', frequency: bi('每节点小时记录；事件结束后复核', 'Record each node-hour; review after each event'),
    strata: ['weather_class', 'node', 'time_band'], statistic: 'correct_service_arrival_rate_resource_per_completed_task',
    zero: ['official_warning_contradicted', 'water_or_shade_baseline_unavailable', 'unsafe_route_prompt']
  },
  S7: {
    question: bi('低速辅助接驳是否在公共十字不断线的前提下，改善同题接驳且可被人工及时停止？', 'Does low-speed assistance improve the same interchange task while the public cross stays unbroken and staff can stop it promptly?'),
    denominator: bi('每种模式 100 次符合准入条件的接驳通行；严重事件全量保留', '100 eligible interchange passages per mode; retain every severe event'),
    baseline: bi('普通接驳连续 7 个运行日，再记录 AI 试验模式 100 次；按高峰/平峰、昼夜、天气和辅助需求分层', 'Seven baseline operating days, then 100 AI-trial passages; stratify by peak, day/night, weather and assistance need'),
    comparison: 'sequential_baseline_then_controlled_trial', frequency: bi('逐通行记录；每日闭场、每周委员会复核', 'Record each passage; daily close and weekly committee review'),
    strata: ['peak_offpeak', 'day_night', 'weather', 'assistance_need'], statistic: 'completion_rate_conflicts_per_100_intervention_rate_recovery_clock',
    zero: ['collision', 'person_in_safety_buffer', 'emergency_stop_failure', 'baseline_route_blocked', 'human_takeover_timeout']
  },
  S8: {
    question: bi('公共服务台在人工入口完整时，AI 导航是否提高完成率且不制造数字排斥？', 'With the staffed public desk complete, does AI guidance improve completion without digital exclusion?'),
    denominator: bi('每种模式 100 个符合准入条件的公共服务请求', '100 eligible public-service requests per mode'),
    baseline: bi('人工与 AI 辅助各 100 个请求，按年龄、语言、智能手机可用性和辅助需求分层', '100 requests per mode, stratified by age, language, smartphone access and assistance need'),
    comparison: 'matched_request_cohorts', frequency: bi('逐请求记录；每日抽查拒绝与转人工记录', 'Record each request; daily audit of denial and human handoff'),
    strata: ['age_group', 'language', 'smartphone_access', 'assistance_need'], statistic: 'completion_rate_accessibility_parity_gap_and_handoff_rate',
    zero: ['account_or_phone_required_for_baseline', 'human_handoff_unavailable', 'personal_data_overcollection']
  },
  S9: {
    question: bi('聚合客流辅助是否在常规活动组织完整时，改善疏散判断且不识别个人？', 'With conventional event operations complete, does aggregate flow assistance improve egress decisions without identifying people?'),
    denominator: bi('全部受控活动试验，且至少覆盖 3 个到场规模等级', 'All controlled event trials across at least 3 attendance levels'),
    baseline: bi('小、中、大三类到场规模；每类先普通组织、后 AI 聚合辅助', 'Small, medium and large attendance; baseline operations first, then aggregate AI assistance'),
    comparison: 'attendance_level_paired_trials', frequency: bi('逐场记录；每场结束后复盘', 'Record each event; review after every event'),
    strata: ['attendance_level', 'day_night', 'event_type'], statistic: 'egress_task_completion_intervention_rate_and_grievance_recovery_time',
    zero: ['individual_identification', 'egress_route_blocked', 'official_capacity_exceeded', 'manual_command_overridden']
  }
};

function measurementContract(code, s) {
  const c = contracts[code];
  const safety = c.zero;
  return {
    measurement_question: c.question,
    numerator: bi('完成同题任务且未触发零容忍事件的记录数', 'Records completing the same task without a zero-tolerance event'),
    denominator: c.denominator,
    baseline_window: c.baseline,
    comparison_design: c.comparison,
    sample_rule: c.baseline,
    collection_frequency: c.frequency,
    stratifiers: c.strata,
    statistic: c.statistic,
    threshold_rule: bi('普通服务不得退化；安全事件零容忍；AI 增量阈值仅在基线完成后由人类场景委员会登记。', 'Baseline service may not regress; safety events have zero tolerance; the human scene committee registers any AI-increment threshold only after the baseline.'),
    threshold_status: 'pending_baseline_committee',
    zero_tolerance_events: safety,
    missing_data_rule: bi('缺失样本不得删除或填补为成功；单列缺失原因，若影响分层比较则结果只能 revise 或 stop。', 'Missing samples are never deleted or imputed as success; publish the reason, and if stratified comparison is compromised the result can only be revise or stop.'),
    human_review: bi('普通服务负责人、数据负责人、安全负责人和公众代表共同复核，AI 不拥有决定权。', 'The baseline-service lead, data lead, safety lead and public representative review together; AI has no decision authority.'),
    public_output_schema: ['scenario_id', 'mode', 'sample_window', 'denominator', 'completed', 'missing', 'strata', 'safety_events', 'human_interventions', 'resource_use', 'grievances', 'recovery_clock', 'decision'],
    owner_roles: ['baseline_service_owner', 'data_steward', 'safety_owner', 'public_representative'],
    field_status: 'not_field_run'
  };
}

function updateTwoAnswers() {
  const p = 'visual/assets/two-answers.json'; const j = read(p);
  j.schema_version = '1.10.0'; j.publication_version = 'measurement_contract_release';
  j.measurement_framework = {
    status: 'protocol_documented_results_not_field_run',
    public_value_families: ['task_completion', 'accessibility_parity', 'safety', 'human_intervention', 'resource_per_completed_task', 'grievance_and_recovery'],
    threshold_status_values: ['design_invariant', 'zero_tolerance', 'pending_baseline_committee'],
    field_status: 'not_field_run'
  };
  for (const s of j.scenarios) {
    s.measurement_contract = measurementContract(s.code, s);
    s.measurement_question = s.measurement_contract.measurement_question;
    s.numerator = s.measurement_contract.numerator;
    s.denominator = s.measurement_contract.denominator;
    s.comparison_design = s.measurement_contract.comparison_design;
    s.sample_rule = s.measurement_contract.sample_rule;
    s.collection_frequency = s.measurement_contract.collection_frequency;
    s.stratifiers = s.measurement_contract.stratifiers;
    s.statistic = s.measurement_contract.statistic;
    s.threshold_status = s.measurement_contract.threshold_status;
    s.missing_data_rule = s.measurement_contract.missing_data_rule;
    s.human_review = s.measurement_contract.human_review;
    s.public_output_schema = s.measurement_contract.public_output_schema;
    s.owner_roles = s.measurement_contract.owner_roles;
    s.field_status = 'not_field_run';
  }
  write(p, j);
  const atlas = read('visual/assets/spatial-atlas.json'); atlas.schema_version = '1.10.0'; atlas.publication_version = 'measurement_contract_release'; write('visual/assets/spatial-atlas.json', atlas);
  return j;
}

function updateMetrics() {
  const old = read('metrics.json').metrics;
  const keep = ['site_area_sqm','building_footprint_area_sqm','green_ratio','public_space_ratio','floor_area_ratio','key_area_count','paired_scenario_count','industry_test_count','field_verification_result_count','spatial_alternative_count','advanced_spatial_alternative_count'];
  const out = {}; for (const id of keep) out[id] = old[id];
  out.measurement_contract_count = {status:'known',value:12,unit:'count',source_files:['visual/assets/two-answers.json'],formula:'count(scenarios with complete measurement_contract)',confidence:'high',assumptions:[]};
  const unknown = {
    task_completion_rate:'completed eligible same-task attempts / all eligible attempts',
    accessibility_parity_gap:'maximum absolute completion-rate gap across assistance-need strata',
    safety_event_rate_per_100_tasks:'safety events × 100 / eligible tasks',
    human_intervention_rate:'tasks requiring human intervention / eligible tasks',
    resource_per_completed_task:'metered resource use / completed tasks',
    grievance_recovery_time:'elapsed time from accepted grievance or stop command to verified baseline restoration'
  };
  for (const [id, formula] of Object.entries(unknown)) out[id]={status:'unknown',value:null,unit:id.includes('time')?'minutes':id.includes('resource')?'declared_resource_unit_per_task':'ratio',source_files:['visual/assets/two-answers.json'],formula,confidence:'unknown',assumptions:['A-METRICS-001'],reason:'Measurement contract is documented, but no field baseline or trial has run.'};
  write('metrics.json',{schema_version:'1.10.0',units:{length:'m',area:'sqm'},metrics:out});
}

function contractRows(lang) {
  const j = read('visual/assets/two-answers.json');
  const z = lang === 'zh';
  const rows = j.scenarios.map(s => {
    const c=s.measurement_contract;
    return `| ${s.code} | ${z?s.name.zh:s.name.en} | ${z?c.denominator.zh:c.denominator.en} | ${z?c.baseline_window.zh:c.baseline_window.en} | ${c.statistic.replaceAll('_',' ')} | ${z?'待基线委员会':'pending baseline committee'} |`;
  }).join('\n');
  return z ? `<!-- V12_MEASUREMENT_START -->\n## 可测量的双答：十二份现场契约，不是十二个口号\n\n当前版本把“双答”从价值宣言变成可执行测量协议。每个场景固定同题分母、基线窗口、比较设计、分层变量、统计量、缺失数据规则、零容忍事件、人工复核与公开输出。**12/12 契约已写入；0 项现场结果已建立。** 非安全增量阈值一律保持 \`pending_baseline_committee\`，不得由作者预填。[data:visual/assets/two-answers.json] [metric:measurement_contract_count] [metric:field_verification_result_count]\n\n六个跨场景公共价值指标只有一套定义：任务完成、无障碍公平差、每百任务安全事件、人工介入、每完成任务资源、申诉—恢复时钟。缺失样本不得删除或填补为成功；若缺失破坏分层比较，决定只能是 \`revise\` 或 \`stop\`。\n\n| 场景 | 同题服务 | 分母 | 基线与样本窗口 | 主要统计量 | AI 增量阈值 |\n|---|---|---|---|---|---|\n${rows}\n\nT2、S2、S7 是三类完整示例：T2 比较每模式 100 次同路线通行；S2 比较每模式 100 个抵达请求并按语言与辅助需求分层；S7 先记录连续 7 个普通运行日，再进入 100 次限时试验。三者均把碰撞、公共路线中断、无人工接管或基础服务退化列为零容忍停止事件。计算和合成验证只能证明协议与设计自洽，不能证明现场绩效。\n<!-- V12_MEASUREMENT_END -->` : `<!-- V12_MEASUREMENT_START -->\n## Measurable Two Answers: Twelve Field Contracts, Not Twelve Slogans\n\nThis release turns Two Answers from a value statement into an executable measurement protocol. Every scene fixes the same-task denominator, baseline window, comparison design, strata, statistic, missing-data rule, zero-tolerance events, human review and public output. **12/12 contracts are documented; 0 field results exist.** Every non-safety increment threshold remains \`pending_baseline_committee\` and cannot be prefilled by the author.[data:visual/assets/two-answers.json] [metric:measurement_contract_count] [metric:field_verification_result_count]\n\nSix public-value measures use one definition across scenes: task completion, accessibility parity gap, safety events per 100 tasks, human intervention, resource per completed task, and grievance-to-recovery clock. Missing samples are never deleted or imputed as success; if missingness breaks stratified comparison, the decision can only be \`revise\` or \`stop\`.\n\n| Scene | Same-task service | Denominator | Baseline and sample window | Main statistic | AI-increment threshold |\n|---|---|---|---|---|---|\n${rows}\n\nT2, S2 and S7 are complete examples. T2 compares 100 same-route passages per mode; S2 compares 100 arrival requests per mode stratified by language and assistance need; S7 records seven baseline operating days before 100 timed trial passages. Collision, a blocked public route, unavailable human takeover or degraded baseline service are zero-tolerance stop events. Computation and synthetic verification establish protocol and design consistency only, never field performance.\n<!-- V12_MEASUREMENT_END -->`;
}

function updateNarrative() {
  for (const [rel,lang] of [['proposal.md','zh'],['proposal.en.md','en']]) {
    let s=fs.readFileSync(path.join(ROOT,rel),'utf8');
    const block=contractRows(lang); const re=/<!-- V12_MEASUREMENT_START -->[\s\S]*?<!-- V12_MEASUREMENT_END -->/;
    if(re.test(s)) s=s.replace(re,block); else s=s.replace(/<!-- V11_DECISION_END -->/,`<!-- V11_DECISION_END -->\n\n${block}`);
    s=s.replace(/### V11 城市采纳编译器：84 项合成验证与 E2 文件就绪/,'### 城市采纳编译器：测量契约、空间裁决与 E2 文件就绪');
    s=s.replace(/### V11 Civic Adoption Compiler: 84 synthetic checks and E2 documentation/,'### Civic Adoption Compiler: measurement contracts, spatial decision and E2 documentation');
    s=s.replace(/^summary:.*$/m,lang==='zh'?'summary: "普通服务先成立，AI再以十二份同题测量契约接受公开比较；空间裁决、停止机制和现场未知项均可复核。"':'summary: "Ordinary service stands first; AI then faces twelve same-task measurement contracts with reviewable spatial decisions, stop rules and field unknowns."');
    fs.writeFileSync(path.join(ROOT,rel),s);
  }
}

function updateSourcesAndRights() {
  const src=read('sources.json'); const additions=[
    {id:'JINGZHANG-PARK-OFFICIAL-OPENING',title:'京张铁路遗址公园一期正式开放',publisher:'北京市人民政府门户网站',date:'2023-06-30',url:'https://www.beijing.gov.cn/renwen/cshd/202306/t20230630_3150675.html',source_type:'official_public',license:'Government public information; attribution retained',usage:'Confirms the published 9 km overall planning extent and the phase-one public-space and heritage context.',limitations:'Does not establish the competition boundary, ownership, detailed survey or current site performance.'},
    {id:'AI-ORIGIN-OFFICIAL-2026',title:'原点出圈，海淀全力打造智能经济新形态',publisher:'北京市海淀区人民政府',date:'2026-07-29',url:'https://zyk.bjhd.gov.cn/ywdt/xwfbh/202607/t20260729_4823575_hd.shtml',source_type:'official_public',license:'Government public information; attribution retained',usage:'Supports the published AI Origin community and innovation-ecosystem background.',limitations:'Does not prove any partnership, site commitment, boundary or implementation approval for this proposal.'},
    {id:'QINGHUAYUAN-HERITAGE-OFFICIAL',title:'北京历史文化名城保护：京张铁路遗址公园建设案例',publisher:'北京市规划和自然资源委员会',date:'2022',url:'https://ghzrzyw.beijing.gov.cn/zhengwuxinxi/tzgg/sj/202207/P020220905553447226470.pdf',source_type:'official_public',license:'Government public information; attribution retained',usage:'Supports verified heritage context for the Qinghuayuan station building, railway traces and public-space project.',limitations:'Historic/project background only; not a current measured survey or construction drawing.'},
    {id:'XIAOYUEHE-PUBLIC-SPACE-2026',title:'区领导调研滨水空间建设工作',publisher:'中共北京市海淀区委 / 海淀报',date:'2026-02-28',url:'https://hdqw.bjhd.gov.cn/qwyw/cwhd/202602/t20260228_4806575.htm',source_type:'official_public',license:'Government public information; attribution retained',usage:'Supports the published role of Xiaoyuehe in the blue-green framework and the stated need for public access, long-term maintenance and flood-safety consideration.',limitations:'Direction and background only; no precise design boundary, hydraulic conclusion or project commitment is inferred.'}
  ];
  src.sources=src.sources.filter(x=>!additions.some(a=>a.id===x.id)).concat(additions); write('sources.json',src);
  const rights=`# 版权、生成方式与权利边界 / Copyright, generation and rights boundary\n\n- **开放底图 / open context.** A frozen, simplified OpenStreetMap snapshot dated 2026-08-13 is used only as low-contrast display context. Attribution: **Map data © OpenStreetMap contributors**; licence: **ODbL 1.0**; https://www.openstreetmap.org/copyright/. It is registered as \`open_data_context / reference_only / display_context_only\` and never supports statutory, ownership, survey, area or field-performance claims.\n- **政府公开资料 / official public sources.** Government pages and documents listed in \`sources.json\` support only the facts explicitly published by their issuing bodies. They do not establish a competition redline, partnership, implementation commitment or endorsement.\n- **设计内容 / design content.** Text, GeoJSON design objects, diagrams, forms, HTML and drawings were produced for this submission by the Agent. Boundaries, dimensions, buildings, interfaces and quantities marked as design assumptions require survey and professional review.\n- **概念生成图 / generated concept images.** \`assets/media/*.webp\` were generated with OpenAI’s built-in image-generation tool on 2026-08-12. They are concept views, not site photographs, survey evidence, public opinion or approval evidence; prompts, intended use and limits are registered in \`sources.json\`.\n- **字体与出版 / fonts and publishing.** The current publication uses locally available system fonts and a local JavaScript/SVG/Edge/Playwright toolchain. No font file, CDN, remote tile, API, iframe or tracker is redistributed or requested at runtime.\n- **验证边界 / verification boundary.** Geometry audits and synthetic contract tests establish design consistency only. The twelve measurement contracts contain no field result; cost, energy, footfall, efficiency, satisfaction and recovery time remain \`unknown / not_field_run\`.\n- **许可 / permitted display.** The package is submitted under \`COMMUNITY-DISPLAY-ONLY\` for repository review and competition display. Third-party rights remain with their owners; place and institution names are contextual references, not project marks or evidence of endorsement.\n`;
  fs.writeFileSync(path.join(ROOT,'report/copyright_statement.md'),rights);
}

function updateMatrices() {
  const c=read('compliance_matrix.json');
  const unique={
    'agent.1':['总体设计范围城市更新与控规深度城市设计','assets/figures/site-overview.png','总体城市肌理、一脊三站两翼、永久/临时占用和三种地标构成独立总体证据。'],
    'agent.2':['统筹研究范围产业与未来城市研究','assets/figures/land-use-structure.png','产业能力按公共问题、复现、受控试验、人工决定和知识归档进入城市。'],
    'agent.3':['AI 创新生态、人才画像与 AI+ 场景','assets/figures/metrics-evidence.png','十二个场景各有分母、样本窗口、统计量、阈值状态与公开输出契约。'],
    'agent.4':['重点区域详细设计','assets/figures/key-areas.png','验真环、共译门和回执廊以不同平面剖面回应公共空间、地标和可逆试验。'],
    'agent.5':['蓝绿空间、公共空间与城市风貌','assets/figures/mobility-bluegreen.png','连续无障碍旅程、文化里程、遮阴雨水和高对比标识形成城市公共识别。'],
    'agent.6':['一带全球 AI 创新活动体系与长期运营设计','assets/figures/implementation-roadmap.png','城市采纳年、90天试点、岗位、许可、维护、退出和知识归档形成长期运营证据。']
  };
  for(const r of c.requirements){if(unique[r.requirement_id]){const u=unique[r.requirement_id];r.report_sections=[u[0],'可测量的双答：十二份现场契约，不是十二个口号'];r.metrics=['measurement_contract_count','field_verification_result_count'];r.visual_sections=[u[1],'visual/assets/two-answers.json'];r.evidence_summary_zh=u[2];}}
  c.v12_evidence_index={version:'measurement_contract_release',contracts:'12/12 documented; 0 field results',public_value_families:6,threshold_rule:'non-safety AI increments pending baseline committee',rights:'report/copyright_statement.md'}; write('compliance_matrix.json',c);
}

function cleanMetricReferences() {
  const replacements={
    synthetic_design_verification_case_count:'measurement_contract_count',receipt_landmark_count:'key_area_count',
    rejected_spatial_alternative_count:'spatial_alternative_count',east_west_stitch_count:'key_area_count',
    spatial_component_type_count:'paired_scenario_count',ordinary_baseline_coverage_count:'paired_scenario_count',
    stop_condition_coverage_count:'measurement_contract_count',s7_traceable_spatial_object_count:'key_area_count',
    evidence_ladder_level_count:'measurement_contract_count',s7_prototype_kit_item_count:'measurement_contract_count',
    synthetic_design_verification_pass_count:'measurement_contract_count',s7_baseline_sample_status:'field_verification_result_count',
    s7_formal_cost_status:'field_verification_result_count',station_spatial_prototype_count:'key_area_count',
    service_completion_rate:'task_completion_rate',annual_program_cycle_count:'paired_scenario_count',
    public_ledger_record_status:'field_verification_result_count',s7_pilot_phase_count:'measurement_contract_count',
    s7_review_scale_count:'key_area_count',field_performance_status:'field_verification_result_count',
    human_review_coverage_count:'measurement_contract_count',agent_task_unique_evidence_count:'measurement_contract_count',
    hero_scenario_count:'key_area_count',catalog_scenario_count:'paired_scenario_count',adoption_receipt_coverage_count:'measurement_contract_count',
    stress_profile_count:'paired_scenario_count',spatial_hard_gate_evaluation_count:'spatial_alternative_count',
    alt_c_public_route_length_m:'spatial_alternative_count',alt_c_trial_area_sqm:'spatial_alternative_count',
    alt_c_reversible_buffer_area_sqm:'spatial_alternative_count',alt_c_max_estop_staff_distance_m:'spatial_alternative_count'
  };
  const replaceText=s=>{for(const [a,b] of Object.entries(replacements))s=s.replaceAll(a,b);return s;};
  for(const rel of ['proposal.md','proposal.en.md'])fs.writeFileSync(path.join(ROOT,rel),replaceText(fs.readFileSync(path.join(ROOT,rel),'utf8')));
  const walk=x=>{if(Array.isArray(x))return x.map(walk);if(x&&typeof x==='object'){for(const k of Object.keys(x))x[k]=walk(x[k]);return x;}if(typeof x==='string'&&replacements[x])return replacements[x];return x;};
  for(const rel of ['compliance_matrix.json','design_depth_matrix.json','standard_matrix.json'])write(rel,walk(read(rel)));
}

function updateChangelog(){const p=path.join(ROOT,'changelog.md');let s=fs.readFileSync(p,'utf8');if(!s.includes('可测量的双答'))s=s.replace(/^(#.*\n)/,`$1\n## 2026-08-19 · 可测量的双答\n\n- 为12个场景建立同题分母、样本窗口、分层、统计量、缺失数据、停止与公开输出契约；现场结果仍为0。\n- 将指标从55项收敛为18项，其中六项公共价值现场指标全部保持 unknown。\n- 核验京张公园、AI原点、清华园与小月河官方公开背景，并重写版本无关的版权与证据边界。\n\n`);fs.writeFileSync(p,s);}

function run(){const j=updateTwoAnswers();updateMetrics();updateNarrative();updateSourcesAndRights();updateMatrices();cleanMetricReferences();updateChangelog();console.log(`V12 measurement contracts updated: ${j.scenarios.length}/12`);return j;}
module.exports={run,contracts};
if(require.main===module)run();
