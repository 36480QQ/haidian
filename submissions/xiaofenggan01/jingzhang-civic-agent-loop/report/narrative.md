# 机器可读治理制品（京张·转辙）

本方案把 agent-readable city 落成三件配套制品，使四环协作成为可审计、可回滚、可证伪的状态机，而非隐喻。母题采用转辙器的完整工程动作——**转辙（路由）→ 锁闭（防错）→ 验通（验证）**：门闸 G0-G6 即这三个动作的状态机展开。

## Civic Agent Receipt Schema

```json
{
  "$schema": "http://json-schema.org/draft-2020-12/schema",
  "$id": "civic-agent-receipt.schema.json",
  "title": "Civic Agent Receipt (京张·转辙)",
  "description": "每次城市智能体干预/场景运行的机器可读收据。把 agent-readable city 从宣言落成 per-run 凭证：每次干预都有证据、人工责任、最差组、申诉通道、处置结果。环会自转，门闸可回滚。",
  "type": "object",
  "required": [
    "receipt_id",
    "scenario_id",
    "gate",
    "disposition",
    "human_responsibility",
    "evidence_refs",
    "appeal",
    "run_status"
  ],
  "properties": {
    "receipt_id": {
      "type": "string",
      "description": "唯一收据 ID"
    },
    "version": {
      "type": "string"
    },
    "scenario_id": {
      "type": "string",
      "description": "对应 proposal 场景卡 01-12"
    },
    "gate": {
      "enum": [
        "G0",
        "G1",
        "G2",
        "G3",
        "G4",
        "G5",
        "G6"
      ],
      "description": "当前所处门闸"
    },
    "evidence_refs": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "[data:]/[metric:]/[source:]/[standard:] 引用清单"
    },
    "human_responsibility": {
      "type": "string",
      "description": "人工责任主体（写角色，不指派真实政府部门）"
    },
    "worst_group": {
      "type": "string",
      "description": "受影响最大的群体（最差组优先原则）"
    },
    "appeal": {
      "type": "string",
      "description": "申诉/投诉/删除通道"
    },
    "deadline": {
      "type": [
        "string",
        "null"
      ]
    },
    "disposition": {
      "enum": [
        "pending",
        "pass",
        "fail",
        "rollback",
        "exit"
      ],
      "description": "处置结果"
    },
    "performance_results": {
      "type": [
        "object",
        "null"
      ],
      "description": "性能指标；null 表示未运行，不冒充已测试"
    },
    "run_status": {
      "enum": [
        "sandbox_only",
        "not_run",
        "controlled_test",
        "public_pilot",
        "retired"
      ]
    },
    "rollback_path": {
      "type": "string",
      "description": "回滚到哪个上游门闸/环"
    },
    "generated_at": {
      "type": "string"
    }
  },
  "additionalProperties": true
}
```

## G0-G6 门闸状态机

```json
{
  "schema_version": "0.1.0",
  "name": "京张·转辙 七道门闸状态机 (G0-G6)",
  "description": "把四环协作落成 7 道可复核门闸，每道有进入条件、可复核状态、未通过处理、人签。环会自转——任何一道未过都回流上游环，而非顺序终止。",
  "four_step_protocol": {
    "apply": "G3 申请",
    "verify": "G4 验证",
    "open": "G5 开放",
    "retire": "G6 退役"
  },
  "gates": [
    {
      "gate_id": "G0",
      "name": "资料就绪",
      "ring": "资料环",
      "entry_condition": "公开资料 + 来源登记 + provisional 披露完成",
      "reviewable_state": "证据链可追溯",
      "on_fail": "回资料环补料",
      "human_signoff": "资料委员会"
    },
    {
      "gate_id": "G1",
      "name": "推演生成",
      "ring": "推演环",
      "entry_condition": "多方案生成 + 指标 EPSG:4548 复算",
      "reviewable_state": "方案可比、指标自洽",
      "on_fail": "重设参数重推",
      "human_signoff": "规划师"
    },
    {
      "gate_id": "G2",
      "name": "反馈接入",
      "ring": "反馈环",
      "entry_condition": "公众/传感反馈接入并脱敏",
      "reviewable_state": "反馈已分类、可复核",
      "on_fail": "关停 + 线下征集",
      "human_signoff": "社区代表"
    },
    {
      "gate_id": "G3",
      "name": "人工复核(申请)",
      "ring": "复核环",
      "entry_condition": "合规 + 隐私 + 伦理审查通过",
      "reviewable_state": "复核签字、receipt=ready",
      "on_fail": "红牌暂停",
      "human_signoff": "专家 + 角色"
    },
    {
      "gate_id": "G4",
      "name": "受控测试(验证)",
      "ring": "验证",
      "entry_condition": "受控测试场闭合合格、可证伪三问过关",
      "reviewable_state": "性能指标达标、非 null",
      "on_fail": "退回 G1",
      "human_signoff": "测试负责人"
    },
    {
      "gate_id": "G5",
      "name": "公开试点(开放)",
      "ring": "开放",
      "entry_condition": "边界 + 低速 + 可监管 + 申诉通道就绪",
      "reviewable_state": "运行 receipt 公开可查",
      "on_fail": "收缩或退出",
      "human_signoff": "运营 + 治理者"
    },
    {
      "gate_id": "G6",
      "name": "退役/迭代(退役)",
      "ring": "迭代",
      "entry_condition": "到期或失败触发或更优方案取代",
      "reviewable_state": "退出空间处置完成",
      "on_fail": "公众触发复议",
      "human_signoff": "议事会"
    }
  ],
  "three_falsifiability_questions": [
    "能否被证伪（什么证据能推翻）？",
    "退出后空间如何处置？",
    "公众能否独立触发暂停/复议？"
  ],
  "switch_lock_verify_mapping": {
    "switch": "G0-G2 转辙：资料/推演/反馈三环把方案、数据、反馈路由到对应的处理股道——转辙器母题的原始动作",
    "lock": "G3 锁闭：人工复核上锁。转辙器在铁路里转辙后必须锁闭，防止列车走上错误股道；同理，未经复核锁闭的智能体干预不得进入公开空间",
    "verify": "G4 验通：受控测试验通。道岔验通才许列车通过；同理，先在受控测试场验证可通过，验不通退回 G1 重新转辙",
    "open_retire": "G5-G6 开放与退役：验通后开放试点；到期、失败触发或更优方案取代即退役"
  },
  "provisional_use_zone": {
    "name": "留白验证区（临时用途机制）",
    "mechanism": "AI 场景用地作为按生命周期管理的临时用途（申请→验证→开放→退役），退出后按用途兼容清单处置，不改变法定用地性质",
    "planning_note": "可直接被控规采用的制度接口：临时用途不需调整法定图则，由 G5 开放授权与 G6 退出处置闭环管理；G6 退役后空间按兼容清单回到原用途或进入下一轮申请"
  },
  "note": "门闸可回滚（任何一道未过都回流上游环），这是'环会自转'的状态机落地，区别于顺序闸门。"
}
```

## 示例收据（example-receipt）

```json
{
  "receipt_id": "RCPT-EXAMPLE-001",
  "version": "0.1.0",
  "scenario_id": "02-用地合规自动复核",
  "gate": "G3",
  "evidence_refs": [
    "[data:geometry/land_use.geojson#LU-090]",
    "[standard:MOHURD-CONTROL-DETAILED-PLANNING]",
    "[metric:land_use_area_0802_sqm]"
  ],
  "human_responsibility": "规划师终审（角色，不指派真实政府部门）",
  "worst_group": "用地红线内现状产权人",
  "appeal": "公示期异议 + 规划师窗口 + 线下纸质",
  "deadline": null,
  "disposition": "pending",
  "performance_results": null,
  "run_status": "sandbox_only",
  "rollback_path": "G3→G0 回资料环复核证据",
  "note": "示例收据，标 sandbox_only / not_run / performance_results=null —— 不冒充已运行。真实运行须先在 G4 受控测试场取得闭合合格、三问过关，方可进 G5 公开试点。",
  "generated_at": "2026-08-09"
}
```

注：示例收据标 sandbox_only / not_run / performance_results=null，不冒充已运行。真实运行须先在 G4 受控测试场取得闭合合格、三问过关。
