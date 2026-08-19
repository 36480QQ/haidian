const fs = require('fs');
const path = require('path');
const os = require('os');
const sharp = require('sharp');
const { chromium } = require('playwright');
const base = require('./build-v6');
const previous = require('./build-v9');

const ROOT = path.resolve(__dirname, '..', '..');
const FIG = path.join(ROOT, 'assets', 'figures');
const DRAW = path.join(ROOT, 'drawings');
const RESULTS = JSON.parse(fs.readFileSync(path.join(__dirname, 'v10-tabletop-results.json'), 'utf8'));
const C = { ink:'#14251f', paper:'#f3efe5', white:'#fff', graphite:'#66736e', green:'#176b55', green2:'#dcebe4', amber:'#d98a12', amber2:'#f7e2b7', blue:'#126d9b', blue2:'#d8ebf4', red:'#a7463e', red2:'#f3d7d2', dark:'#0c2119', line:'#bcc6bf', water:'#9bcfdb', yellow:'#f1c55b' };
const q = (lang, zh, en) => lang === 'zh' ? zh : en;
const esc = (value) => String(value ?? '').replace(/[&<>\"]/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c]));
const css = () => `text{font-family:'Segoe UI','Microsoft YaHei',Arial,sans-serif;fill:${C.ink}}.title{font-size:40px;font-weight:900}.h{font-size:24px;font-weight:850}.b{font-size:17px;font-weight:750}.s{font-size:13px;fill:${C.graphite}}.xs{font-size:10px;fill:${C.graphite}}.card{fill:white;stroke:#d5ddd7;stroke-width:2}.dim{fill:none;stroke:${C.graphite};stroke-width:2;stroke-dasharray:7 6}`;
const defs = () => `<defs><marker id="arr10" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="${C.ink}"/></marker><pattern id="dataGap10" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line y2="12" stroke="#b3bdb6" stroke-width="2"/></pattern></defs>`;
const svg = (w, h, body, bg=C.paper) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}"><style>${css()}</style>${defs()}<rect width="${w}" height="${h}" fill="${bg}"/>${body}</svg>`;
const nest = (source, x, y, w, h) => source.replace('<svg xmlns="http://www.w3.org/2000/svg"', '<svg').replace('<svg ', `<svg x="${x}" y="${y}" width="${w}" height="${h}" `);
const dataUri = (file) => `data:image/${path.extname(file).toLowerCase()==='.jpg'?'jpeg':path.extname(file).slice(1)};base64,${fs.readFileSync(file).toString('base64')}`;
const raster = (name, x, y, w, h, fit='xMidYMid meet') => `<image href="${dataUri(path.join(FIG, name))}" x="${x}" y="${y}" width="${w}" height="${h}" preserveAspectRatio="${fit}"/>`;
const v10 = (source) => source
  .replaceAll('V9 · VERIFIABLE CIVIC PROTOTYPE', 'V10 · CIVIC ADOPTION COMPILER')
  .replaceAll('V9 · Verifiable Civic Prototype', 'V10 · Civic Adoption Compiler')
  .replaceAll('V9 · 可验证的城市样机', 'V10 · 城市采纳编译器')
  .replaceAll('E2 DOCUMENTED · NOT BUILT · NOT FIELD-RUN', 'T0 SYNTHETIC VERIFIED · E2 DOCUMENTED · NOT FIELD-RUN')
  .replaceAll('VERIFIABLE CIVIC PROTOTYPE', 'CIVIC ADOPTION COMPILER')
  .replaceAll('可验证的城市样机', '城市采纳编译器');

function landmark(kind, x, y, scale=1) {
  if (kind === 'ring') return `<g transform="translate(${x} ${y}) scale(${scale})"><ellipse rx="92" ry="68" fill="white" stroke="${C.green}" stroke-width="18"/><ellipse rx="54" ry="34" fill="${C.amber2}" stroke="${C.amber}" stroke-width="5"/><path d="M-128 0H-92M92 0H128" stroke="${C.green}" stroke-width="14"/><circle cx="0" cy="0" r="11" fill="${C.blue}"/></g>`;
  if (kind === 'gate') return `<g transform="translate(${x} ${y}) scale(${scale})"><path d="M-92 72V-72H92V72M-30 72V-10H30V72" fill="none" stroke="${C.amber}" stroke-width="18"/><path d="M-120 -42H120M-120 0H120M-120 42H120" stroke="${C.green}" stroke-width="11"/><rect x="52" y="-60" width="32" height="120" fill="${C.blue2}" stroke="${C.blue}" stroke-width="4"/></g>`;
  return `<g transform="translate(${x} ${y}) scale(${scale})"><path d="M-110 0H110M0-110V110" stroke="${C.green}" stroke-width="18"/><rect x="30" y="30" width="76" height="76" fill="${C.amber2}" stroke="${C.amber}" stroke-width="5" stroke-dasharray="10 7"/><rect x="-106" y="30" width="70" height="76" fill="${C.blue2}" stroke="${C.blue}" stroke-width="5"/></g>`;
}

function siteOverview(lang='zh') {
  const z = lang === 'zh';
  const overall = v10(base.overall(lang));
  return svg(1800,1100, `<text x="48" y="58" class="title">${z?'总体城市设计｜公共基线连接三座回执地标':'OVERALL URBAN DESIGN · PUBLIC BASELINE LINKS THREE RECEIPT LANDMARKS'}</text><text x="48" y="91" class="b">${z?'只表达城市肌理、一脊三站两翼与六条缝合；S7 详图留给重点区图':'City fabric, spine, stations, wings and stitches only; S7 detail belongs to the key-area figure'}</text><clipPath id="siteCrop"><rect x="35" y="120" width="1190" height="900" rx="22"/></clipPath><g clip-path="url(#siteCrop)">${nest(overall,20,105,1920,925)}</g><rect x="35" y="120" width="1190" height="900" rx="22" fill="none" stroke="${C.line}" stroke-width="2"/><g transform="translate(1260 120)"><rect width="500" height="900" rx="22" fill="white"/><text x="26" y="48" class="h">${z?'三种空间原型':'THREE SPATIAL ARCHETYPES'}</text>${landmark('ring',92,165,.55)}${landmark('gate',250,165,.55)}${landmark('porch',410,165,.55)}<text x="92" y="265" text-anchor="middle" class="b">${z?'验真环':'RING'}</text><text x="250" y="265" text-anchor="middle" class="b">${z?'共译门':'GATE'}</text><text x="410" y="265" text-anchor="middle" class="b">${z?'回执廊':'PORCH'}</text><path d="M26 300H474" stroke="${C.line}"/><text x="26" y="350" class="h">${z?'城市采纳编译器':'CIVIC ADOPTION COMPILER'}</text>${[[C.green,z?'完整公共路线':'COMPLETE PUBLIC ROUTE'],[C.red,z?'可触发停止':'TRIGGERABLE STOP'],[C.blue,z?'可复核回执':'REVIEWABLE RECEIPT']].map((r,i)=>`<g transform="translate(28 ${390+i*92})"><circle cx="26" cy="26" r="24" fill="${r[0]}"/><text x="26" y="33" text-anchor="middle" style="font-size:14px;font-weight:900;fill:white">0${i+1}</text><text x="72" y="33" class="b">${r[1]}</text></g>`).join('')}<rect x="26" y="700" width="448" height="155" rx="14" fill="${C.dark}"/><text x="50" y="750" style="font-size:27px;font-weight:900;fill:white">12 × 7 = 84 / 84 PASS</text><text x="50" y="795" style="font-size:16px;font-weight:800;fill:${C.amber2}">T0 SYNTHETIC CONTRACT VERIFIED</text><text x="50" y="830" style="font-size:15px;font-weight:800;fill:${C.blue2}">FIELD PERFORMANCE · UNKNOWN</text></g><text x="48" y="1080" class="xs">Map data © OpenStreetMap contributors · ODbL · 2026-08-13 · ${z?'临时边界与概念布局待官方底图复核':'provisional boundary and concept layout pending official base'}</text>`);
}

function landUseStructure(lang='zh') {
  const z = lang === 'zh';
  const stations = [
    { x:115, w:430, c:C.green, pale:C.green2, code:'T2', title:z?'众智园｜研发验证首层':'ZHONGZHIYUAN · VALIDATION GROUND FLOOR', type:z?'环形庭院 + 完整旁路':'ring court + complete bypass' },
    { x:610, w:430, c:C.amber, pale:C.amber2, code:'S2', title:z?'AI 原点｜公共服务首层':'AI ORIGIN · CIVIC-SERVICE GROUND FLOOR', type:z?'穿行大厅 + 复核后台':'porous hall + review back office' },
    { x:1105, w:580, c:C.blue, pale:C.blue2, code:'S7', title:z?'大钟寺｜交通前场':'DAZHONGSI · INTERCHANGE FORECOURT', type:z?'公共十字 + 单侧试验湾':'public cross + one-side trial bay' },
  ];
  return svg(1800,1100, `<text x="48" y="58" class="title">${z?'首层功能与永久 / 临时占用剖带':'GROUND-FLOOR USE + PERMANENT / TEMPORARY OCCUPATION BAND'}</text><text x="48" y="92" class="b">${z?'用地判断从“色块”转为可进入的首层、公共界面和限时占用':'Land-use judgement shifts from coloured parcels to enterable ground floors, public edges and timed occupation'}</text><g transform="translate(0 120)">${stations.map((s,i)=>`<g transform="translate(${s.x} 0)"><rect width="${s.w}" height="540" rx="20" fill="white" stroke="${s.c}" stroke-width="5"/><rect y="350" width="${s.w}" height="190" fill="${s.pale}"/><text x="24" y="45" class="h">${s.code} · ${s.title}</text><text x="24" y="78" class="b">${s.type}</text><path d="M25 320H${s.w-25}" stroke="${s.c}" stroke-width="12"/>${i===0?`<path d="M80 220A120 90 0 1 0 320 220A120 90 0 1 0 80 220" fill="none" stroke="${C.green}" stroke-width="24"/><ellipse cx="200" cy="220" rx="70" ry="42" fill="${C.amber2}" stroke="${C.amber}" stroke-width="5"/>`:i===1?`<path d="M70 300V130H360V300M150 300V185H280V300" fill="none" stroke="${C.amber}" stroke-width="22"/><path d="M35 165H395M35 220H395M35 275H395" stroke="${C.green}" stroke-width="10"/>`:`<path d="M70 230H510M290 90V330" stroke="${C.green}" stroke-width="25"/><rect x="330" y="250" width="145" height="85" fill="${C.amber2}" stroke="${C.amber}" stroke-width="6" stroke-dasharray="12 8"/><rect x="105" y="250" width="145" height="85" fill="${C.blue2}" stroke="${C.blue}" stroke-width="6"/>`}<text x="24" y="395" class="b">${z?'永久：路径、人工、蓝绿':'PERMANENT · route, staff, blue-green'}</text><text x="24" y="438" class="b" style="fill:${C.amber}">${z?'临时：可拆 AI 插件':'TEMPORARY · removable AI plug-in'}</text><text x="24" y="481" class="b" style="fill:${C.blue}">${z?'公开：状态、申诉、回执':'PUBLIC · state, appeal, receipt'}</text></g>`).join('')}</g><g transform="translate(90 720)"><rect width="1620" height="255" rx="20" fill="${C.dark}"/><text x="30" y="52" style="font-size:27px;font-weight:900;fill:white">${z?'更新顺序：公共路径 → 首层界面 → 可拆插件 → 现场回执':'RENEWAL ORDER · PUBLIC ROUTE → GROUND EDGE → REMOVABLE PLUG-IN → FIELD RECEIPT'}</text>${[[C.green,z?'永久公共基线':'PERMANENT BASELINE',z?'全天独立运行':'independent all day'],[C.blue,z?'公共证据界面':'PUBLIC EVIDENCE',z?'人工决定与申诉':'human decision + appeal'],[C.amber,z?'限时试验占用':'TIMED TRIAL',z?'许可齐全才开启':'permits complete before opening'],[C.red,z?'失败退出':'FAILURE EXIT',z?'恢复普通用途':'restore ordinary use']].map((r,i)=>`<g transform="translate(${30+i*390} 95)"><rect width="355" height="120" rx="13" fill="white"/><rect width="12" height="120" rx="6" fill="${r[0]}"/><text x="32" y="42" class="h">${r[1]}</text><text x="32" y="78" class="b">${r[2]}</text></g>`).join('')}</g><text x="90" y="1055" class="xs">${z?'概念首层与占用关系；不是法定用地、现状建筑或工程审批结论。':'Concept ground-floor and occupation relationships; not statutory land use, existing buildings or approval.'}</text>`);
}

function s7Node(lang='zh') {
  const z = lang === 'zh';
  return svg(1400,760, `<text x="38" y="50" class="title">S7 · 1:50 ${z?'装配节点':'ASSEMBLY NODE'}</text><text x="38" y="82" class="b">${z?'坡道 / 盲道 + 可拆隔离 + 证据牌 + 临电接口 + 雨水边界':'ramp / tactile + removable barrier + evidence plate + temporary power + rain edge'}</text><g transform="translate(55 120)"><rect width="1290" height="500" rx="18" fill="white"/><rect x="60" y="85" width="610" height="280" fill="${C.green2}"/><path d="M60 225H670" stroke="${C.green}" stroke-width="36"/><path d="M80 225H650" stroke="${C.yellow}" stroke-width="9" stroke-dasharray="16 10"/><path d="M150 365L250 300H510L610 365" fill="${C.paper}" stroke="${C.ink}" stroke-width="4"/><text x="335" y="405" text-anchor="middle" class="b">${z?'1:12 原型坡道 · 0.4m 触觉带':'1:12 prototype ramp · 0.4m tactile band'}</text><rect x="710" y="85" width="230" height="280" fill="${C.amber2}" stroke="${C.amber}" stroke-width="5" stroke-dasharray="12 8"/><path d="M700 80V370M950 80V370" stroke="${C.red}" stroke-width="7"/><circle cx="725" cy="115" r="18" fill="${C.red}"/><text x="825" y="220" text-anchor="middle" class="h">${z?'可逆试验边界':'REVERSIBLE TRIAL EDGE'}</text><rect x="995" y="100" width="120" height="250" rx="10" fill="${C.blue2}" stroke="${C.blue}" stroke-width="5"/><text x="1055" y="190" text-anchor="middle" class="b">E01</text><text x="1055" y="225" text-anchor="middle" class="s">${z?'证据牌':'EVIDENCE'}</text><rect x="1155" y="225" width="90" height="125" fill="${C.graphite}"/><text x="1200" y="280" text-anchor="middle" style="font-size:14px;font-weight:900;fill:white">POWER</text><path d="M950 390H1250V465H950Z" fill="${C.blue2}" stroke="${C.blue}" stroke-width="4"/><path d="M970 430c40-45 80 45 120 0s80 45 120 0" fill="none" stroke="${C.water}" stroke-width="10"/><text x="1100" y="495" text-anchor="middle" class="b">${z?'雨水花园边界':'RAIN-GARDEN EDGE'}</text>${[[60,670,'4.0m '+(z?'连续公共路线':'CONTINUOUS PUBLIC ROUTE')],[710,940,'1.5m '+(z?'建议缓冲':'PROPOSED BUFFER')],[995,1115,z?'证据界面':'EVIDENCE EDGE']].map(([a,b,t],i)=>`<path d="M${a} ${35+i*18}H${b}" class="dim"/><text x="${(a+b)/2}" y="${28+i*18}" text-anchor="middle" class="s">${t}</text>`).join('')}</g><g transform="translate(55 645)">${[[C.green,'B01',z?'公共路线先成立':'baseline first'],[C.amber,'A01',z?'插件保持单侧':'plug-in on one side'],[C.blue,'E01',z?'决定公开可见':'decision publicly visible'],[C.red,'E02',z?'急停不占通路':'E-stop outside route']].map((r,i)=>`<g transform="translate(${i*320} 0)"><circle cx="15" cy="15" r="13" fill="${r[0]}"/><text x="38" y="21" class="b">${r[1]} · ${r[2]}</text></g>`).join('')}</g><text x="55" y="735" class="xs">${z?'所有尺寸为可复核原型假设，待测绘、无障碍、消防、市政与设备专业复核。':'All dimensions are reviewable prototype assumptions pending survey and professional accessibility, fire, utility and equipment review.'}</text>`);
}

function keyAreas(lang='zh') {
  const z = lang === 'zh';
  const suffix = lang === 'en' ? '.en.png' : '.png';
  return svg(1800,1100, `<text x="48" y="58" class="title">${z?'三座地标同尺度对照｜环、门、廊不用标题也能辨认':'THREE LANDMARKS AT A COMPARABLE SCALE · RING, GATE AND PORCH READ WITHOUT TITLES'}</text><g transform="translate(35 100)">${[
    {x:0,c:C.green,pale:C.green2,code:'T2',name:z?'众智园·验真环':'ZHONGZHIYUAN · VERIFICATION RING',plan:`hero-t2-detail${suffix}`,sec:`hero-t2-section${suffix}`},
    {x:570,c:C.amber,pale:C.amber2,code:'S2',name:z?'AI 原点·共译门':'AI ORIGIN · TRANSLATION GATE',plan:`hero-s2-detail${suffix}`,sec:`hero-s2-section${suffix}`},
  ].map((s)=>`<g transform="translate(${s.x} 0)"><rect width="540" height="650" rx="20" fill="white" stroke="${s.c}" stroke-width="5"/><text x="22" y="42" class="h">${s.code} · ${s.name}</text>${raster(s.plan,18,60,504,390)}${raster(s.sec,18,465,504,150)}<rect x="18" y="620" width="504" height="10" fill="${s.c}"/></g>`).join('')}<g transform="translate(1140 0)"><rect width="590" height="650" rx="20" fill="white" stroke="${C.blue}" stroke-width="5"/><text x="22" y="42" class="h">S7 · ${z?'大钟寺·回执廊':'DAZHONGSI · RECEIPT PORCH'}</text>${nest(v10(base.s7Plan(lang,true,true)),15,55,560,400)}${nest(v10(base.s7Section(lang)),15,470,560,145)}<rect x="18" y="620" width="554" height="10" fill="${C.blue}"/></g></g><g transform="translate(35 785)"><rect width="1730" height="245" rx="20" fill="white"/>${nest(s7Node(lang),10,10,1160,225)}<g transform="translate(1200 20)"><text x="0" y="32" class="h">${z?'同一编译规则，不同空间原型':'ONE COMPILER, DIFFERENT SPATIAL TYPES'}</text>${[[C.green,'T2',z?'旁路围合内环':'bypass encloses inner ring'],[C.amber,'S2',z?'三路穿过服务门':'three routes cross service gate'],[C.blue,'S7',z?'公共十字邻接试验湾':'public cross beside trial bay']].map((r,i)=>`<g transform="translate(0 ${60+i*54})"><circle cx="16" cy="16" r="14" fill="${r[0]}"/><text x="42" y="22" class="b">${r[1]} · ${r[2]}</text></g>`).join('')}</g></g><text x="48" y="1080" class="xs">${z?'比例均为原型建议；现状、界面与许可待正式资料和专业团队复核。':'All scales are prototype proposals; existing conditions, interfaces and permits await formal data and professional review.'}</text>`);
}

function mobilityBluegreen(lang='zh') {
  const z = lang === 'zh';
  const suffix = lang === 'en' ? '.en.png' : '.png';
  const steps = [z?'抵达公共路径':'ARRIVE ON PUBLIC ROUTE',z?'触觉 / 坡道连续':'TACTILE + RAMP CONTINUITY',z?'常规接驳与候车':'CONVENTIONAL INTERCHANGE',z?'主动选择试验':'OPT IN TO TRIAL',z?'失败即人工回退':'FAIL TO STAFFED FALLBACK',z?'恢复公共空间':'RESTORE PUBLIC SPACE'];
  return svg(1800,1100, `<text x="48" y="58" class="title">${z?'连续旅程与三道剖面｜无障碍、蓝绿、消防和失败回退':'CONTINUOUS JOURNEY + THREE SECTIONS · ACCESS, BLUE-GREEN, FIRE AND FALLBACK'}</text><g transform="translate(55 120)"><path d="M75 95H1590" stroke="${C.green}" stroke-width="18"/><path d="M75 95H1590" stroke="${C.yellow}" stroke-width="5" stroke-dasharray="13 9"/>${steps.map((s,i)=>`<g transform="translate(${70+i*305} 0)"><circle cx="0" cy="95" r="34" fill="${i===4?C.red:i===3?C.amber:C.green}" stroke="white" stroke-width="6"/><text x="0" y="103" text-anchor="middle" style="font-size:16px;font-weight:900;fill:white">0${i+1}</text><foreignObject x="-82" y="135" width="165" height="58"><div xmlns="http://www.w3.org/1999/xhtml" style="font:800 15px/1.25 'Segoe UI','Microsoft YaHei',Arial;text-align:center;color:${C.ink}">${s}</div></foreignObject></g>`).join('')}</g><g transform="translate(35 355)">${[
    {x:0,c:C.green,title:'T2 · '+(z?'旁路—缓冲—测试环':'BYPASS—BUFFER—TEST RING'),img:`hero-t2-section${suffix}`},
    {x:570,c:C.amber,title:'S2 · '+(z?'穿行—人工台—插件墙':'PASSAGE—STAFF—PLUG-IN WALL'),img:`hero-s2-section${suffix}`},
  ].map((s)=>`<g transform="translate(${s.x} 0)"><rect width="540" height="470" rx="20" fill="white" stroke="${s.c}" stroke-width="5"/><text x="20" y="42" class="h">${s.title}</text>${raster(s.img,15,60,510,330)}<text x="20" y="430" class="b">${z?'普通路线在试验关闭时仍完整':'baseline remains complete with trial closed'}</text></g>`).join('')}<g transform="translate(1140 0)"><rect width="625" height="470" rx="20" fill="white" stroke="${C.blue}" stroke-width="5"/><text x="20" y="42" class="h">S7 · ${z?'公共路径—缓冲—试验湾':'PUBLIC ROUTE—BUFFER—TRIAL BAY'}</text>${nest(v10(base.s7Section(lang)),15,60,595,330)}<text x="20" y="430" class="b">${z?'消防、疏散与人工接管均不穿过试验湾':'fire, egress and takeover never cross the trial bay'}</text></g></g><g transform="translate(55 875)"><rect width="1690" height="120" rx="16" fill="${C.dark}"/><text x="28" y="43" style="font-size:25px;font-weight:900;fill:white">${z?'失败回退：停止设备 → 关闭边界 → 人工完成同题任务 → 两条路线开放 → 记录与申诉':'FAILURE FALLBACK · STOP DEVICE → CLOSE EDGE → STAFF COMPLETE TASK → ROUTES OPEN → LOG + APPEAL'}</text><text x="28" y="82" style="font-size:17px;font-weight:800;fill:${C.amber2}">${z?'恢复时长仍为现场未知；桌面演练只验证恢复出口存在。':'Recovery duration remains field unknown; tabletop cases verify only that a recovery exit exists.'}</text></g>`);
}

function stateMachine(lang='zh') {
  const z = lang === 'zh';
  const states = [['OPEN',C.green],['TRIAL',C.amber],['PAUSE',C.red],['RETIRE',C.blue]];
  return svg(1500,520, `<text x="35" y="50" class="title">${z?'允许状态机｜非法跃迁阻断出版':'ALLOWED STATE MACHINE · ILLEGAL JUMPS BLOCK PUBLICATION'}</text>${states.map((s,i)=>`<g transform="translate(${80+i*350} 155)"><rect width="245" height="105" rx="20" fill="${s[1]}"/><text x="122" y="63" text-anchor="middle" style="font-size:29px;font-weight:900;fill:white">${s[0]}</text></g>`).join('')}<path d="M325 207H430M675 207H780M1025 207H1130" stroke="${C.ink}" stroke-width="6" marker-end="url(#arr10)"/><path d="M900 280C900 410 200 410 200 285" fill="none" stroke="${C.green}" stroke-width="5" marker-end="url(#arr10)"/><path d="M1250 280C1250 450 550 450 550 285" fill="none" stroke="${C.blue}" stroke-width="5" marker-end="url(#arr10)"/><text x="360" y="195" class="s">${z?'许可 + 岗位 + 基线':'permits + roles + baseline'}</text><text x="710" y="195" class="s">${z?'停止事件':'stop event'}</text><text x="1060" y="195" class="s">${z?'退役决定':'retire decision'}</text><text x="540" y="385" class="b">PAUSE → OPEN</text><text x="1010" y="438" class="b">RETIRE → OPEN</text>`);
}

function metricsEvidence(lang='zh') {
  const z = lang === 'zh';
  const types = ['BASE','PERMIT','ROLE','REGRESS','ZERO','RECOVER','RETIRE'];
  return svg(1800,1100, `<text x="48" y="58" class="title">${z?'城市采纳编译器｜84 项合成演练、许可门与现场未知':'CIVIC ADOPTION COMPILER · 84 SYNTHETIC CASES, PERMIT GATES + FIELD UNKNOWNS'}</text>${nest(stateMachine(lang),35,90,1120,385)}<g transform="translate(35 490)"><rect width="1120" height="515" rx="20" fill="white"/><text x="24" y="42" class="h">12 × 7 = 84 · ${z?'确定性设计契约矩阵':'DETERMINISTIC DESIGN-CONTRACT MATRIX'}</text>${types.map((t,i)=>`<text x="${265+i*105}" y="80" text-anchor="middle" class="xs">${t}</text>`).join('')}${Array.from({length:12},(_,r)=>`<g transform="translate(0 ${105+r*31})"><text x="24" y="21" class="b">SCN-${String(r+1).padStart(3,'0')}</text>${types.map((_,c)=>`<rect x="${225+c*105}" width="80" height="24" rx="5" fill="${C.green2}" stroke="${C.green}"/><text x="${265+c*105}" y="17" text-anchor="middle" style="font-size:11px;font-weight:900;fill:${C.green}">PASS</text>`).join('')}</g>`).join('')}<rect x="24" y="485" width="1072" height="18" fill="${C.green}"/><text x="560" y="500" text-anchor="middle" style="font-size:12px;font-weight:900;fill:white">84 / 84 PASS · INPUT HASHED · RULE VERSIONED · FIELD RESULT COUNT = 0</text></g><g transform="translate(1190 95)"><rect width="575" height="910" rx="22" fill="white" stroke="${C.blue}" stroke-width="5"/><text x="26" y="48" class="h">${z?'合成回执实例':'SYNTHETIC RECEIPT EXAMPLE'}</text><text x="26" y="78" class="s">SCN-010-T05 · ZERO-TOLERANCE EVENT</text>${[[z?'初态':'INITIAL','TRIAL'],[z?'注入事件':'EVENT','zero_tolerance_event_detected'],[z?'预期 / 实际':'EXPECTED / OBSERVED','PAUSE / PAUSE'],[z?'责任触发':'ACCOUNTABLE TRIGGER',z?'安全负责人立即停止':'safety lead stops immediately'],[z?'恢复出口':'RECOVERY EXIT',z?'人工同题 + 公共路线恢复':'staffed task + route restoration']].map((r,i)=>`<g transform="translate(26 ${115+i*110})"><text class="s">${r[0]}</text><foreignObject y="16" width="520" height="75"><div xmlns="http://www.w3.org/1999/xhtml" style="font:800 17px/1.3 'Segoe UI','Microsoft YaHei',Arial;color:${C.ink}">${r[1]}</div></foreignObject></g>`).join('')}<g transform="translate(26 685)">${[[C.green,z?'已知设计':'KNOWN DESIGN',z?'几何、数量、文档':'geometry, quantity, documents'],[C.amber,z?'合成验证':'SYNTHETIC',z?'规则自洽，不是绩效':'rule consistency, not performance'],[C.red,z?'现场未知':'FIELD UNKNOWN',z?'安全、效率、满意度、成本':'safety, efficiency, acceptance, cost']].map((r,i)=>`<g transform="translate(0 ${i*66})"><rect width="520" height="54" rx="9" fill="${i===0?C.green2:i===1?C.amber2:C.red2}"/><rect width="10" height="54" rx="5" fill="${r[0]}"/><text x="28" y="23" class="b">${r[1]}</text><text x="250" y="23" class="s">${r[2]}</text></g>`).join('')}</g></g><text x="48" y="1080" class="xs">${z?'synthetic_design_verification：只验证方案状态、准入、停止、恢复和退役规则；不证明现场安全、交通效率、公众接受度或批准。':'synthetic_design_verification verifies only design-state, admission, stop, recovery and retirement rules; not field safety, transport efficiency, public acceptance or approval.'}</text>`);
}

function jurySummary(lang='zh') {
  const z = lang === 'zh';
  return svg(1800,950, `<g transform="translate(10 5)">${nest(keyAreas(lang),0,0,1160,705)}${nest(s7Node(lang),1185,0,585,315)}<rect x="1185" y="335" width="585" height="235" rx="20" fill="${C.dark}"/><text x="1220" y="395" style="font-size:31px;font-weight:900;fill:white">12 × 7 = 84 / 84 PASS</text><text x="1220" y="445" style="font-size:18px;font-weight:800;fill:${C.green2}">T0 SYNTHETIC CONTRACT VERIFIED</text><text x="1220" y="485" style="font-size:18px;font-weight:800;fill:${C.blue2}">E2 DOCUMENTED PROTOTYPE READY</text><text x="1220" y="525" style="font-size:18px;font-weight:800;fill:${C.amber2}">FIELD PERFORMANCE UNKNOWN</text><g transform="translate(1185 595)">${['ADOPT','REVISE','STOP'].map((t,i)=>`<rect x="${i*200}" width="185" height="110" rx="15" fill="${i===0?C.green2:i===1?C.amber2:C.red2}"/><text x="${92+i*200}" y="66" text-anchor="middle" style="font-size:24px;font-weight:900">${t}</text>`).join('')}</g>${nest(stateMachine(lang),0,720,1160,205)}<rect x="1185" y="730" width="585" height="195" rx="18" fill="white" stroke="${C.blue}" stroke-width="4"/><text x="1215" y="775" class="h">${z?'第一页的三个审查结论':'THREE PAGE-ONE CONCLUSIONS'}</text><text x="1215" y="825" class="b">01 · ${z?'环、门、廊各有空间原型':'ring, gate and porch are spatial types'}</text><text x="1215" y="865" class="b">02 · ${z?'非法跃迁阻断出版':'illegal transition blocks publication'}</text><text x="1215" y="905" class="b">03 · ${z?'现场未知不伪装为已知':'field unknown never masquerades as known'}</text></g>`);
}

function page(n, lang, title, sub, body, cls='') {
  return `<section class="page ${cls}"><header><b>${String(n).padStart(2,'0')} / 16</b><span>JING-ZHANG TWO ANSWERS · V10 · CIVIC ADOPTION COMPILER</span></header><h1>${esc(title)}</h1><p class="sub">${esc(sub)}</p>${body}<footer>${q(lang,'已知设计 / 合成验证 / 现场未知 · 临时边界概念建议','Known design / synthetic verification / field unknown · provisional concept')}<i>${n}</i></footer></section>`;
}

function a3(lang='zh') {
  const z = lang === 'zh';
  const sections = previous.a3(lang).match(/<section class="page[\s\S]*?<\/section>/g).map(v10);
  sections[0] = page(1, lang, z?'京张双答｜城市采纳编译器':'JING-ZHANG TWO ANSWERS · CIVIC ADOPTION COMPILER', z?'空间、停止与回执在第一页同时可审查；84 项为合成验证，现场绩效未知。':'Space, stop and receipt are reviewable on page one; 84 cases are synthetic and field performance is unknown.', `<div style="height:220mm;background:${C.paper};overflow:hidden">${jurySummary(lang)}</div>`, 'coverpage');
  sections[11] = page(12, lang, z?'S7 1:50 节点、分层装配与四态':'S7 1:50 NODE, LAYERED ASSEMBLY + FOUR STATES', z?'永久基线、可拆插件和证据界面在装配与退役时仍可区分。':'Permanent baseline, removable plug-in and evidence interface remain distinct through assembly and retirement.', `<div style="height:205mm;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:4mm"><div style="background:white;overflow:hidden">${v10(base.s7Assembly(lang))}</div><div style="background:white;overflow:hidden">${s7Node(lang)}</div><div style="grid-column:1/3;background:white;overflow:hidden">${stateMachine(lang)}</div></div>`);
  sections[15] = page(16, lang, z?'验证结果、风险、来源与深化门槛':'VERIFICATION, RISK, SOURCES + NEXT GATES', z?'规则可以先被编译；现实绩效必须由测绘、许可、搭建和现场运行证明。':'Rules can compile first; survey, permits, assembly and field operation must prove real performance.', `<div style="height:210mm;background:white;overflow:hidden">${metricsEvidence(lang)}</div>`);
  return sections.join('');
}

function board(lang, index, title, body, footer) {
  return `<section class="board">${svg(1684,1191, `<text x="52" y="54" class="h">0${index} / V10 · CIVIC ADOPTION COMPILER</text><text x="52" y="118" style="font-size:${lang==='zh'?48:38}px;font-weight:900">${esc(title)}</text>${body}<path d="M52 1138H1632" stroke="${C.line}" stroke-width="2"/><text x="52" y="1170" class="b">${esc(footer)}</text><text x="1632" y="1170" text-anchor="end" class="s">T0 SYNTHETIC VERIFIED · E2 DOCUMENTED · NOT FIELD-RUN</text>`)}</section>`;
}

function a0(lang='zh') {
  const z = lang === 'zh';
  return [
    board(lang,1,z?'总体城市设计：一条公共基线，三座回执地标':'OVERALL URBAN DESIGN · ONE PUBLIC BASELINE, THREE RECEIPT LANDMARKS',`${nest(siteOverview(lang),30,135,1180,920)}${nest(landUseStructure(lang),1230,150,405,545)}<rect x="1230" y="720" width="405" height="315" rx="20" fill="${C.dark}"/><text x="1260" y="775" style="font-size:27px;font-weight:900;fill:white">${z?'城市采纳编译器':'CIVIC ADOPTION COMPILER'}</text><text x="1260" y="830" style="font-size:18px;font-weight:800;fill:${C.green2}">01 · ${z?'完整公共路线':'COMPLETE PUBLIC ROUTE'}</text><text x="1260" y="880" style="font-size:18px;font-weight:800;fill:${C.amber2}">02 · ${z?'可触发停止':'TRIGGERABLE STOP'}</text><text x="1260" y="930" style="font-size:18px;font-weight:800;fill:${C.blue2}">03 · ${z?'可复核回执':'REVIEWABLE RECEIPT'}</text><text x="1260" y="995" style="font-size:16px;font-weight:800;fill:white">84 SYNTHETIC · FIELD UNKNOWN</text>`,z?'一脊三站两翼 · 环 / 门 / 廊 · 临时边界概念建议':'one spine, three stations, two wings · ring / gate / porch · provisional concept'),
    board(lang,2,z?'三座空间原型：S7 四级尺度加 1:50 装配节点':'THREE SPATIAL TYPES · S7 FOUR SCALES PLUS 1:50 ASSEMBLY NODE',`${nest(keyAreas(lang),30,135,1130,930)}${nest(s7Node(lang),1185,145,450,300)}${nest(v10(base.s7Assembly(lang)),1185,470,450,335)}${nest(stateMachine(lang),1185,830,450,210)}`,z?'T2 验真环 · S2 共译门 · S7 回执廊 · 尺寸待测绘和专业复核':'T2 ring · S2 gate · S7 porch · dimensions pending survey and professional review'),
    board(lang,3,z?'城市采纳编译器：规则先编译，现场再证明':'CIVIC ADOPTION COMPILER · RULES COMPILE FIRST, FIELD PROVES LATER',`${nest(metricsEvidence(lang),30,135,1160,920)}${nest(v10(base.operation(lang)),1215,145,420,300)}<rect x="1215" y="470" width="420" height="565" rx="20" fill="${C.dark}"/><text x="1245" y="525" style="font-size:26px;font-weight:900;fill:white">${z?'九十天进入门':'90-DAY ENTRY GATES'}</text>${[[C.green,'00–30',z?'只搭普通基线':'baseline only'],[C.blue,'31–45',z?'建立现场基线':'field baseline'],[C.amber,'46–75',z?'许可后受控试验':'permitted trial'],[C.red,'76–90',z?'停止、撤场、回执':'stop, retire, receipt']].map((r,i)=>`<g transform="translate(1245 ${560+i*92})"><circle cx="25" cy="25" r="23" fill="${r[0]}"/><text x="62" y="20" style="font-size:18px;font-weight:900;fill:white">${r[1]}</text><text x="62" y="48" style="font-size:15px;font-weight:800;fill:${i===0?C.green2:i===1?C.blue2:i===2?C.amber2:C.red2}">${r[2]}</text></g>`).join('')}<text x="1245" y="965" style="font-size:17px;font-weight:900;fill:white">ADOPT · REVISE · STOP</text><text x="1245" y="1005" style="font-size:14px;font-weight:800;fill:${C.amber2}">${z?'任一失败门返回普通答案':'any failed gate returns to baseline'}</text>`,z?'84 / 84 合成设计验证通过 · 现场安全、效率、公众接受度与成本仍未知':'84 / 84 synthetic design checks pass · field safety, efficiency, acceptance and cost remain unknown'),
  ].join('');
}

function pdfCss(a0=false) {
  return `${previous.pdfCss(a0)}.page.coverpage{background:${C.paper};color:${C.ink}}.page.coverpage header,.page.coverpage h1,.page.coverpage .sub,.page.coverpage footer{color:${C.ink}}.page>div svg{width:100%;height:100%;display:block}`;
}

async function png(source, name, width, height) {
  await sharp(Buffer.from(source), { density:180 }).resize(width,height).png({ compressionLevel:9, palette:true, quality:96 }).toFile(path.join(FIG,name));
}
function replace(tmp, final) {
  const old = `${final}.prior`;
  if (fs.existsSync(old)) fs.rmSync(old,{force:true});
  if (fs.existsSync(final)) fs.renameSync(final,old);
  fs.renameSync(tmp,final);
  if (fs.existsSync(old)) fs.rmSync(old,{force:true});
}
async function exportPdf(pageInstance, lang) {
  const suffix = lang === 'en' ? '.en' : '';
  let tmp = path.join(os.tmpdir(),`jz-v10-a3${suffix}-${Date.now()}.pdf`);
  await pageInstance.setContent(`<html lang="${lang}"><meta charset="utf-8"><style>${pdfCss(false)}</style><body>${a3(lang)}</body></html>`,{waitUntil:'load'});
  await pageInstance.pdf({path:tmp,printBackground:true,preferCSSPageSize:true,tagged:true,outline:true});
  replace(tmp,path.join(DRAW,`a3-booklet${suffix}.pdf`));
  tmp = path.join(os.tmpdir(),`jz-v10-a0${suffix}-${Date.now()}.pdf`);
  await pageInstance.setContent(`<html lang="${lang}"><meta charset="utf-8"><style>${pdfCss(true)}</style><body>${a0(lang)}</body></html>`,{waitUntil:'load'});
  await pageInstance.pdf({path:tmp,printBackground:true,preferCSSPageSize:true,tagged:true,outline:true});
  replace(tmp,path.join(DRAW,`a0-boards${suffix}.pdf`));
}

async function build() {
  if (RESULTS.summary.test_case_count !== 84 || RESULTS.summary.pass_count !== 84 || RESULTS.summary.fail_count !== 0) throw new Error('V10 tabletop gate failed');
  for (const lang of ['zh','en']) {
    const suffix = lang === 'en' ? '.en.png' : '.png';
    await png(siteOverview(lang),`site-overview${suffix}`,2700,1650);
    await png(landUseStructure(lang),`land-use-structure${suffix}`,2700,1650);
    await png(keyAreas(lang),`key-areas${suffix}`,2700,1650);
    await png(mobilityBluegreen(lang),`mobility-bluegreen${suffix}`,2700,1650);
    await png(metricsEvidence(lang),`metrics-evidence${suffix}`,2700,1650);
    await png(s7Node(lang),`s7-node-050${suffix}`,2100,1140);
  }
  const browser = await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
  const pageInstance = await browser.newPage();
  for (const lang of ['zh','en']) await exportPdf(pageInstance,lang);
  await browser.close();
  console.log('V10 five core figures, 1:50 node and four vector PDFs generated');
}

module.exports = { build, siteOverview, landUseStructure, keyAreas, mobilityBluegreen, metricsEvidence, s7Node, stateMachine, jurySummary, a3, a0, pdfCss };
if (require.main === module) build().catch((error)=>{ console.error(error); process.exit(1); });
