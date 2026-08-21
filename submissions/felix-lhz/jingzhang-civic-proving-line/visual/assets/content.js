const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const readJson = rel => JSON.parse(fs.readFileSync(path.join(ROOT, rel), 'utf8'));
const writeJson = (rel, value) => fs.writeFileSync(path.join(ROOT, rel), JSON.stringify(value, null, 2) + '\n');
const readText = rel => fs.readFileSync(path.join(ROOT, rel), 'utf8');
const writeText = (rel, value) => fs.writeFileSync(path.join(ROOT, rel), value.replace(/\r\n/g, '\n'));

const zhIntro = `

> **可建造的公共十字 / BUILDABLE CIVIC CROSS。** 把“不牺牲公共路径”建成一段可进入、可维护、可关闭、可恢复的城市空间：公共十字和人工服务先独立成立，AI 只进入一侧可逆试验湾，所有决定留在可见的回执廊。[data:visual/assets/prototype-model.json] [data:visual/assets/spatial-decision.json]

同一建筑—地面系统包含五个可定位部分：全天公共十字、单侧试验湾、有人值守的回执廊、蓝绿边界和独立维护后场。统一模型同时生成 1:5000 城市联系、1:2000 总平面、1:500 场地与建筑平面、两道 1:200 剖面、1:50 门廊节点和三项 1:20 原型详图。尺寸均为待测绘、结构、消防、基础和耐久复核的设计假设。[data:visual/assets/prototype-model.json] [depth:three_key_area_detailed_design]

材料家族采用螺栓连接镀锌钢框架、穿孔金属遮阳屏、干式预制压重基础、透水预制铺装和可更换证据面板。永久公共层先建；可拆 AI 插件在许可齐全后装配；试验停止时设备沿独立后勤线撤出，门廊继续作为人工公共服务。[metric:architectural_prototype_count] [metric:material_system_count] [metric:architectural_detail_count]

ALT-A 因切断公共十字被 **REJECT**，ALT-B 因监督、消防与撤场碎片化被 **REVISE**，ALT-C 单侧可逆湾进入建筑深化。空间裁决只回答“为什么选择”；十二份测量契约回答“建成后如何验证”。两者均不冒充现场结果。[metric:rejected_spatial_alternative_count] [metric:revised_spatial_alternative_count] [metric:advanced_spatial_alternative_count]

**当前实施决定仍是 G0 NO-GO。** 精确测绘、权属、八类许可、四个独立岗位和连续 7 日普通服务基线尚未完成；当前关闭许可 0/8、基线 0/7 日，AI 试验不得开始。[data:visual/assets/e2-readiness.json] [metric:current_trial_open_gate_count] [metric:pending_trial_permit_count]

![总体城市设计与三座建筑地标](assets/figures/site-overview.png)

`;

const enIntro = `

> **BUILDABLE CIVIC CROSS.** Turn “do not sacrifice the public route” into an enterable, maintainable, closable and recoverable civic space. The public cross and staffed service stand alone; AI enters one reversible bay; every decision remains visible in the Receipt Porch.[data:visual/assets/prototype-model.json] [data:visual/assets/spatial-decision.json]

One architectural-ground system contains five locatable parts: the all-day public cross, one-sided trial bay, staffed Receipt Porch, blue-green edge and independent back-of-house. A single model generates 1:5000 context, 1:2000 plan, 1:500 architectural-ground plan, two 1:200 sections, a 1:50 porch node and three 1:20 prototype details. Every dimension is a design assumption pending survey, structural, fire, foundation and durability review.[data:visual/assets/prototype-model.json] [depth:three_key_area_detailed_design]

The material family uses bolted galvanized steel frames, perforated-metal sun screens, dry precast ballast, permeable precast paving and replaceable evidence panels. The permanent public layer is built first; removable AI plug-ins assemble only after permits close; after a stop, equipment leaves on an independent service route while the porch remains staffed public service.[metric:architectural_prototype_count] [metric:material_system_count] [metric:architectural_detail_count]

ALT-A is **REJECTED** for severing the public cross; ALT-B is **REVISED** because supervision, fire and removal access fragment; ALT-C advances into architectural development. The spatial decision answers “why this option”; twelve measurement contracts answer “how to verify it after construction”. Neither is field evidence.[metric:rejected_spatial_alternative_count] [metric:revised_spatial_alternative_count] [metric:advanced_spatial_alternative_count]

**The present implementation decision remains G0 NO-GO.** Precise survey, title, eight permits, four independent duty posts and seven consecutive ordinary-service days are incomplete; 0/8 permits and 0/7 days are closed, so AI trial may not begin.[data:visual/assets/e2-readiness.json] [metric:current_trial_open_gate_count] [metric:pending_trial_permit_count]

![Overall urban design and three architectural landmarks](assets/figures/site-overview.en.png)

`;

const zhArchitecture = `## 重点区域详细设计

### 建筑家族：环、门、廊

三座地标共享 **MAT-01–05** 干式材料家族和“公共基线 / AI 插件 / 证据界面”语法，却采用不可混淆的平面和剖面。[data:visual/assets/prototype-model.json]

- **众智园·验真环（T2）**：全天公共旁路围绕受控测试庭；观察廊、安全台、失败公示和东侧设备退出口在 1:500 平面与 1:200 剖面中对位。关闭测试庭后，公共外环和观察廊继续运行。
- **AI 原点·共译门（S2）**：三条无账户穿行线穿过人工双语台、等候界面和复核后台；可关闭插件墙由后勤带维护。夜间关闭插件后，静态导视和人工窗口仍成立。
- **大钟寺·回执廊（S7）**：公共十字、单侧试验湾、有人值守门廊、蓝绿边界与维护后场组成完整建筑—地面系统；公共路线、消防和撤场互不占用。

### 大钟寺旗舰样板：五级尺度

**1:5000 / 1:2000** 只判断轨道、公园、道路和四象限方向性接口；公开快照在大钟寺仅含一个建筑要素，缺测处统一标为“适配界面 / 待调查带”，不补画虚构建筑。[data:visual/assets/context-open-map.json] [source:OPENSTREETMAP-CONTEXT-20260813]

**1:500 平面**直接绘出路缘、四处坡道、两条触觉路线、透水铺装、树池、雨水花园、候车与遮阴、回执廊、双急停、控制亭、设备接口、消防线和独立撤场线。门廊后侧 2.4 米维护带连接控制、存储、维护和废弃物空间。[data:visual/assets/prototype-model.json]

**1:200 两道剖面**分别穿过公共路径—缓冲—试验湾和回执廊—公共十字—蓝绿边界，验证净高、遮阴、视线、雨水边缘和人机分离的相对关系；它们不是施工图。[metric:architectural_section_count]

**1:50 / 1:20 节点**记录三类可逆连接：螺栓钢框架与压重基础、触觉路线外侧的可拆隔离、可更换证据牌与临电接口、齐平透水路缘与雨水花园溢流。结构尺寸、防火等级、抗风、排水能力和耐久年限均待专业计算。[metric:architectural_detail_count]

### 装配、维护与四态

- **OPEN**：普通接驳、公共十字、遮阴候车和人工门廊独立运行。
- **TRIAL**：八类许可、四岗位和七日普通基线齐全后，仅开启单侧试验湾。
- **PAUSE**：双急停切断设备，安全负责人接管，公众路线保持不变。
- **RETIRE**：拆除插件和隔离，铺装抬起复位，设备沿东侧撤场，证据面板保留复盘。

90 天实施依次对应测绘核验、永久公共层、基线记录、限时插件和撤场复核；任何阶段的许可、岗位或普通服务失败都阻止进入下一阶段。数量可复算，单价与总价保持 **pending_market_quote**。[data:visual/assets/e2-readiness.json]
`;

const enArchitecture = `## Detailed Design of Key Areas

### Architectural family: Ring, Gate and Porch

The three landmarks share the dry-assembly **MAT-01–05** family and the grammar “public baseline / AI plug-in / evidence interface”, yet remain unmistakable in plan and section.[data:visual/assets/prototype-model.json]

- **Zhongzhiyuan Verification Ring (T2):** an all-day bypass surrounds the controlled test court. Observation arcade, safety desk, failure display and east equipment exit align across the 1:500 plan and 1:200 section. Closing the court leaves the public ring working.
- **AI Origin Translation Gate (S2):** three account-free passages cross the staffed bilingual desk, waiting edge and review backstage; a rear service strip maintains the closable plug-in wall. Static guidance and staffed service survive the night closure.
- **Dazhongsi Receipt Porch (S7):** the public cross, one-sided bay, staffed porch, blue-green edge and back-of-house form one architectural-ground system. Public, fire and removal routes do not occupy one another.

### Dazhongsi flagship: five scales

**1:5000 / 1:2000** establish directional relations among rail, park, roads and four quadrants only. The public crop contains one building feature at Dazhongsi; missing fabric is labelled “adaptation interface / survey-pending band”, never invented.[data:visual/assets/context-open-map.json] [source:OPENSTREETMAP-CONTEXT-20260813]

The **1:500 plan** draws kerbs, four ramps, two tactile routes, permeable paving, tree pits, rain gardens, waiting and shade, Receipt Porch, dual E-stops, control booth, equipment interfaces, fire route and independent removal line. A 2.4 m rear maintenance strip connects control, storage, maintenance and waste.[data:visual/assets/prototype-model.json]

Two **1:200 sections** cut public route—buffer—trial bay and Receipt Porch—public cross—blue-green edge, checking relative clear height, shade, sightline, drainage edge and human-machine separation. They are not construction drawings.[metric:architectural_section_count]

The **1:50 / 1:20 details** record reversible connections: bolted frame on ballast, removable boundary outside the tactile route, replaceable evidence rail and temporary power, and a flush permeable kerb with rain-garden overflow. Structural sizes, fire rating, wind, drainage capacity and durability await professional calculation.[metric:architectural_detail_count]

### Assembly, maintenance and four states

- **OPEN**: ordinary feeder, public cross, shaded waiting and staffed porch work independently.
- **TRIAL**: after eight permits, four posts and seven baseline days close, only the one-sided bay opens.
- **PAUSE**: dual E-stops isolate equipment; the safety lead takes over; the public route does not move.
- **RETIRE**: plug-ins and boundary leave, lifted paving is relaid, equipment exits east and evidence panels remain for review.

The 90-day sequence maps survey, permanent public layer, baseline record, timed plug-in and removal review to drawn components. Any failed permit, post or ordinary service blocks the next stage. Quantities are reproducible; prices remain **pending_market_quote**.[data:visual/assets/e2-readiness.json]
`;

function replaceIntro(text, intro) {
  const marker = '<!-- V11_DECISION_START -->';
  const idx = text.indexOf(marker);
  if (idx < 0) throw new Error('Decision marker missing');
  const h1 = text.match(/^# .+$/m);
  if (!h1) throw new Error('H1 missing');
  const headEnd = h1.index + h1[0].length;
  return text.slice(0, headEnd + 1) + intro + text.slice(idx);
}

function replaceSection(text, start, end, replacement) {
  const a = text.indexOf(start);
  const b = text.indexOf(end, a + start.length);
  if (a < 0 || b < 0) throw new Error(`Section boundary missing: ${start} / ${end}`);
  return text.slice(0, a) + replacement.trim() + '\n\n' + text.slice(b);
}

function updateProposal(rel, lang) {
  let text = readText(rel);
  text = text.replace(/^summary: ".*"$/m, lang === 'zh'
    ? 'summary: "把不牺牲公共路径建成可进入、可维护、可关闭、可恢复的公共十字；当前实施门仍为G0 NO-GO。"'
    : 'summary: "Build the unbroken public route as an enterable, maintainable, closable and recoverable civic cross; the current implementation gate remains G0 NO-GO."');
  text = replaceIntro(text, lang === 'zh' ? zhIntro : enIntro);
  text = replaceSection(text,
    lang === 'zh' ? '## 重点区域详细设计' : '## Detailed Design of Key Areas',
    lang === 'zh' ? '## AI 创新生态、人才画像与 AI+ 场景' : '## AI Innovation Ecosystem, Personas, and AI+ Scenarios',
    lang === 'zh' ? zhArchitecture : enArchitecture);
  text = text.replaceAll('visual/assets/v14-spatial-model.json', 'visual/assets/prototype-model.json');
  text = text.replaceAll('V14 不虚构', 'V15 不虚构').replaceAll('V14 therefore', 'V15 therefore');
  writeText(rel, text);
}

function updateReadiness() {
  const data = readJson('visual/assets/e2-readiness.json');
  data.schema_version = '1.12.0';
  data.dataset_id = 'jingzhang-v15-buildable-civic-cross-g0';
  data.title = {zh:'V15 可建造公共十字 G0 准入门',en:'V15 Buildable Civic Cross G0 Gate'};
  data.prototype_readiness = 'design_documented_trial_not_admitted';
  data.field_status = 'not_field_run';
  data.readiness_gate = {...(data.readiness_gate||{}), gate_id:'G0-S7-PRETRIAL', decision:'no_go', closed_permit_count:0, required_permit_count:8, recorded_baseline_days:0, required_baseline_days:7, contracted_independent_role_count:0, required_independent_role_count:4};
  writeJson('visual/assets/e2-readiness.json', data);
}

function updateMetrics() {
  const data = readJson('metrics.json');
  data.metrics.architectural_prototype_count = {status:'known',value:3,unit:'count',source_files:['visual/assets/prototype-model.json'],formula:'count(architectural_prototypes)',confidence:'high',assumptions:[]};
  data.metrics.material_system_count = {status:'known',value:5,unit:'count',source_files:['visual/assets/prototype-model.json'],formula:'count(material_palette)',confidence:'high',assumptions:[]};
  data.metrics.architectural_section_count = {status:'known',value:4,unit:'count',source_files:['visual/assets/prototype-model.json'],formula:'count(section_refs across three prototypes)',confidence:'high',assumptions:[]};
  data.metrics.architectural_detail_count = {status:'known',value:5,unit:'count',source_files:['visual/assets/prototype-model.json'],formula:'count(detail_refs across three prototypes)',confidence:'high',assumptions:[]};
  data.metrics.current_trial_open_gate_count = {status:'known',value:0,unit:'count',source_files:['visual/assets/e2-readiness.json'],formula:'count(readiness gates permitting TRIAL)',confidence:'high',assumptions:[]};
  data.metrics.pending_trial_permit_count = {status:'known',value:8,unit:'count',source_files:['visual/assets/e2-readiness.json'],formula:'count(pending permit gates)',confidence:'high',assumptions:[]};
  writeJson('metrics.json', data);
}

function updateStructuredData() {
  const model = readJson('visual/assets/prototype-model.json');
  const atlas = readJson('visual/assets/spatial-atlas.json');
  atlas.schema_version = '1.12.0';
  delete atlas.v14_spatial_model_ref;
  atlas.prototype_model_ref = 'visual/assets/prototype-model.json';
  atlas.architectural_prototypes = model.architectural_prototypes;
  atlas.current_implementation_gate = 'G0_no_go_pending_survey_and_permits';
  writeJson('visual/assets/spatial-atlas.json', atlas);
  const scenes = readJson('visual/assets/two-answers.json');
  scenes.schema_version = '1.12.0';
  delete scenes.v14_spatial_model_ref;
  scenes.prototype_model_ref = 'visual/assets/prototype-model.json';
  scenes.current_implementation_gate = 'G0_no_go_pending_survey_and_permits';
  for (const scene of scenes.scenarios) {
    scene.field_status = 'not_field_run';
    scene.architectural_prototype_ref = scene.id === 'SCN-002' ? 'LMK-01' : scene.id === 'SCN-005' ? 'LMK-02' : scene.id === 'SCN-010' ? 'LMK-03' : scene.architectural_prototype_ref || null;
  }
  writeJson('visual/assets/two-answers.json', scenes);
}

function updateChangelog() {
  let text = readText('changelog.md');
  if (!text.includes('## V15 - 可建造的公共十字')) text = text.replace(/^(# .*\n)/, `$1
## V15 - 可建造的公共十字

- 将 ALT-C 深化为公共十字、单侧试验湾、回执廊、蓝绿边界和维护后场组成的建筑—地面系统。
- 三座地标补齐 1:500 平面、1:200 剖面、装配和关闭状态，形成环、门、廊建筑家族。
- 新增 1:50 与 1:20 可逆节点及五类材料系统；结构、消防、基础、耐久和报价继续待专业复核。
- 五张核心图、A0/A3和交互展由统一 V15 模型生成；当前准入仍为 G0 NO-GO，现场绩效未知。

`);
  writeText('changelog.md', text);
}

function updateRights() {
  const data = readJson('sources.json');
  const generated = [
    {
      id:'GENERATED-VERIFICATION-RING-V15',path:'assets/media/verification-ring-v15.webp',companion_path:'assets/media/verification-ring-v15.jpg',
      usage:'T2 architectural experience communication only; not a photograph, survey, field result or approval evidence.',
      limitations:'Follows the V15 outer public bypass, controlled inner court, observation arcade and separate equipment exit; all dimensions and context require survey and professional review.',
      prompt_summary:'Photorealistic concept view of an oval verification ring with an all-day accessible outer bypass, controlled robot court, shaded observation arcade, staffed safety threshold, failure display and separate equipment exit; bolted galvanized steel and perforated screens; no text or logos.'
    },
    {
      id:'GENERATED-TRANSLATION-GATE-V15',path:'assets/media/translation-gate-v15.webp',companion_path:'assets/media/translation-gate-v15.jpg',
      usage:'S2 architectural experience communication only; not a photograph, survey, field result or approval evidence.',
      limitations:'Follows the V15 three account-free passages, staffed bilingual desk, review backstage, closable plug-in wall and rear service strip; all dimensions and context require survey and professional review.',
      prompt_summary:'Photorealistic concept view of a porous translation hall with three account-free passages, staffed bilingual desk, accessible waiting, human review backstage, closable amber plug-in wall and independent rear service strip; no text or logos.'
    },
    {
      id:'GENERATED-RECEIPT-PORCH-V15',path:'assets/media/receipt-porch-v15.webp',companion_path:'assets/media/receipt-porch-v15.jpg',
      usage:'S7 architectural experience communication only; not a photograph, survey, field result or approval evidence.',
      limitations:'Follows the V15 public cross, one-sided reversible trial bay, staffed Receipt Porch, blue-green edge and back-of-house; all dimensions and context require survey and professional review.',
      prompt_summary:'Photorealistic elevated concept view of a buildable civic cross with continuous accessible paths, one-sided trial bay, staffed Receipt Porch, rain gardens, shade, dual E-stops and separate back-of-house/removal access; no text or logos.'
    }
  ].map(x=>({publisher:'OpenAI built-in image generation',date:'2026-08-21',source_type:'ai_generated_visual',license:'Competition display only; subject to platform and competition terms',...x}));
  data.sources = data.sources.filter(x=>!generated.some(y=>y.id===x.id)&&!/-V14$/.test(x.id));
  data.sources.push(...generated);
  writeJson('sources.json', data);
  const rel='report/copyright_statement.md';
  let text=readText(rel).replace(/\n- \*\*V14 project-bound experience views\.\*\*[\s\S]*?(?=\n- \*\*|\n##|$)/,'');
  const block=`

## V15 concept-generated architectural experience images

- assets/media/verification-ring-v15.webp / .jpg
- assets/media/translation-gate-v15.webp / .jpg
- assets/media/receipt-porch-v15.webp / .jpg

Generated with OpenAI built-in image generation on 2026-08-21. They communicate the Ring, Gate and Porch architectural prototypes only and are not site photographs, surveys, field evidence, consultation records or approvals. Text, dimensions, IDs and evidence status are added by local vector layers; professional judgement relies on the plans, sections, structured data and cited public sources.
`;
  if(!text.includes('## V15 concept-generated architectural experience images')) text+=block;
  writeText(rel,text);
}

function run() {
  updateReadiness();
  updateMetrics();
  updateStructuredData();
  updateProposal('proposal.md', 'zh');
  updateProposal('proposal.en.md', 'en');
  updateChangelog();
  updateRights();
  console.log('V15 architecture, structured evidence and G0 NO-GO content written');
}

module.exports = {run};
if (require.main === module) run();
