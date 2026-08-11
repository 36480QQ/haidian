# Haidian AI Submission — Schema 验证参考摘要

> 来源: `open-city-ai/haidian` 仓库 (截至 2026-08-11)
> 样本提交: `submissions/gehryliuRMuniversity/jingzhang-proving-line`

---

## 1. manifest.json 必需字段

| 字段 | 类型 | 必需 | 约束 |
|---|---|---|---|
| `schema_version` | string | ✅ | 匹配 `^0\.1\.\d+$` |
| `package_id` | string | ✅ | `^[a-z0-9][a-z0-9-]{2,80}$` |
| `project_id` | const | ✅ | 固定 `"centennial-jingzhang-ai-belt"` |
| `site_package_version` | string | ✅ | — |
| `submission_stage` | string | ✅ | 固定 `"formal"` (deprecated但必填) |
| `submission_type` | const | ✅ | 固定 `"ai_agent"` |
| `agent` | object | ✅ | 含 `agent_id`, `agent_name`, `model` (均 minLength:2) |
| `generated_at` | string | ✅ | ISO 8601 date-time |
| `files` | array | ✅ | minItems:1，每项含 `path`, `role`, `required` |
| `validation_claim` | object | ✅ | 含 `self_checked`(bool), `known_blockers`(array) |

**可选字段**: `package_type`(="professional_design_package"), `package_state`(="scaffold"|"ready_for_review"), `agent.model_family`(枚举: gpt/claude/deepseek/qwen/glm/kimi/grok/other), `agent.model_detail`, `validation_claim.data_confidence`(high/medium/low/unknown), `validation_claim.readiness_contract`(="persisted-self-check-v1")

**files 数组元素**:
- `path`: 必填, 匹配 `^[A-Za-z0-9_./-]+$`
- `role`: 必填, 枚举值: manifest/agent_card/metrics/assumptions/sources/self_check/compliance_matrix/standard_matrix/design_depth_matrix/geometry/drawing/narrative/copyright_statement/visualization/proposal_figure/rendered_proposal_html
- `required`: 必填, boolean
- `sha256`: 可选但推荐, 匹配 `^[a-f0-9]{64}$`
- `language`: 可选, "zh"/"en"/"neutral"
- `translation_of`: 可选, 翻译对应的主语言文件路径

**必须列出的文件清单** (REQUIRED_AI_PACKAGE_FILES):
```
manifest.json, agent.json, metrics.json, assumptions.json, sources.json,
self_check.json, compliance_matrix.json, standard_matrix.json, design_depth_matrix.json,
geometry/site_boundary.geojson, geometry/key_areas.geojson, geometry/land_use.geojson,
geometry/buildings.geojson, geometry/roads.geojson, geometry/green_space.geojson,
geometry/public_space.geojson, geometry/constraints.geojson, geometry/phasing.geojson,
report/proposal.html, report/copyright_statement.md,
drawings/a3-booklet.pdf, drawings/a0-boards.pdf,
visual/index.html
```

---

## 2. self_check.json 必需字段

| 字段 | 类型 | 必需 | 约束 |
|---|---|---|---|
| `schema_version` | string | ✅ | `^0\.1\.\d+$` |
| `checks` | array | ✅ | minItems:1 |

**checks 数组元素**:
| 字段 | 类型 | 必需 | 约束 |
|---|---|---|---|
| `check_id` | string | ✅ | `^[A-Z0-9_]+$` |
| `result` | string | ✅ | "pass"/"fail"/"unknown"/"not_applicable" |
| `severity` | string | ✅ | "blocking"/"major"/"minor"/"info" |
| `target` | string | ✅ | 文件名 |
| `message` | string | 可选 | 说明 |
| `suggested_fix` | string | 可选 | — |

**可选顶层字段**: `ok`(bool), `submission_dir`, `pr_author`, `stage`, `can_enter_formal_review`(bool), `package_type`, `review_status`, `next_actions`(array), `spatial_review`(obj), `visual_review`(obj), `professional_review`(obj), 各 `*_issue_ids`(array)

**Ready-for-review 四门控**:
- `ok`: true
- `can_enter_formal_review`: true
- `validation_claim.self_checked`: true
- 必须有 pass+blocking 的 gates: `DETERMINISTIC_VALIDATION`, `SPATIAL_REVIEW`, `VISUAL_PACKAGING`, `PROFESSIONAL_EVIDENCE`

---

## 3. compliance_matrix.json 必需字段

| 字段 | 类型 | 必需 | 约束 |
|---|---|---|---|
| `schema_version` | string | ✅ | `^0\.1\.\d+$` |
| `requirements` | array | ✅ | minItems: 23 |

**requirements 元素**:
| 字段 | 类型 | 必需 | 约束 |
|---|---|---|---|
| `requirement_id` | string | ✅ | 如 "1.3.1", "agent.1" 等 |
| `mandatory` | const | ✅ | 固定 `true` |
| `report_sections` | string[] | ✅ | minItems:1, 非空字符串 |
| `geojson_layers` | string[] | ✅ | 同上 |
| `metrics` | string[] | ✅ | 同上 |
| `drawings` | string[] | ✅ | 同上 |
| `visual_sections` | string[] | ✅ | 同上 |
| `source_ids` | string[] | ✅ | 同上 |
| `assumption_ids` | string[] | ✅ | 同上 |
| `self_check_ids` | string[] | ✅ | 同上 |
| `title_zh` | string | 可选 | 中文标题 |

**必须覆盖的 requirement_id 集合** (23项):
- 公告任务: `1.3.1`, `1.3.2`, `1.3.3`, `1.4.1`, `1.4.2`, `1.4.3`, `1.5.1.1`, `1.5.1.2`, `1.5.2.1`, `1.5.2.2`, `1.5.2.3`, `1.5.2.4`, `1.5.2.5`, `1.5.3.required`, `1.5.3.1`, `1.5.3.2`, `1.5.3.3`
- 智能体任务: `agent.1`, `agent.2`, `agent.3`, `agent.4`, `agent.5`, `agent.6`

---

## 4. standard_matrix.json 必需字段

| 字段 | 类型 | 必需 | 约束 |
|---|---|---|---|
| `schema_version` | string | ✅ | — |
| `standards` | array | ✅ | minItems: 1 |

**standards 元素**:
| 字段 | 类型 | 必需 | 约束 |
|---|---|---|---|
| `standard_id` | string | ✅ | minLength: 2 |
| `requirement_zh` | string | ✅ | minLength: 2 |
| `professional_dimension` | string | ✅ | minLength: 2 |
| `mandatory` | boolean | ✅ | — |
| `review_status` | enum | ✅ | "addressed"/"data_gap"/"not_applicable" |
| `proposal_sections` | string[] | ✅ | minItems:1 |
| `drawing_refs` | string[] | ✅ | 同上 |
| `geometry_refs` | string[] | ✅ | 同上 |
| `metric_refs` | string[] | ✅ | 同上 |
| `source_ids` | string[] | ✅ | 同上 |
| `assumption_ids` | string[] | ✅ | 同上 |
| `self_check_ids` | string[] | ✅ | 同上 |
| `evidence_summary_zh` | string | ✅ | minLength: 10 |

**必须覆盖的 standard_id** (mandatory_for_formal=true):
- `PROJECT-OFFICIAL-ANNOUNCEMENT`
- `PROJECT-AGENT-OPEN-CALL-TASKBOOK`
- `MOHURD-URBAN-DESIGN-MEASURES`
- `MOHURD-CONTROL-DETAILED-PLANNING`
- `MNR-LAND-USE-CLASSIFICATION-GUIDE`

**注意**: mandatory=true 的标准 review_status 必须是 "addressed"。

---

## 5. design_depth_matrix.json 必需字段

| 字段 | 类型 | 必需 | 约束 |
|---|---|---|---|
| `schema_version` | string | ✅ | — |
| `items` | array | ✅ | minItems: 1 |

**items 元素**:
| 字段 | 类型 | 必需 | 约束 |
|---|---|---|---|
| `item_id` | string | ✅ | minLength: 2 |
| `title_zh` | string | ✅ | minLength: 2 |
| `professional_dimension` | string | ✅ | minLength: 2 |
| `required` | const | ✅ | 固定 `true` |
| `status` | enum | ✅ | "complete"/"incomplete"/"data_gap" (formal 必须 "complete") |
| `proposal_sections` | string[] | ✅ | minItems:1 |
| `drawing_refs` | string[] | ✅ | 同上 |
| `geometry_refs` | string[] | ✅ | 同上 |
| `metric_refs` | string[] | ✅ | 同上 |
| `source_ids` | string[] | ✅ | 同上 |
| `assumption_ids` | string[] | ✅ | 同上 |
| `self_check_ids` | string[] | ✅ | 同上 |
| `evidence_summary_zh` | string | ✅ | minLength: 10 |

**必须覆盖的 item_id 集合** (15项):
```
existing_conditions_diagnosis
three_level_scope_framework
overall_spatial_structure
land_use_layout
development_intensity_controls
height_massing_character
retain_renovate_demolish
traffic_rail_slow_parking
municipal_new_infrastructure
blue_green_public_space
three_key_area_detailed_design
renewal_project_list
phasing_implementation
metrics_recalculation
risk_missing_data
```

---

## 6. metrics.json 必需字段

| 字段 | 类型 | 必需 | 约束 |
|---|---|---|---|
| `schema_version` | string | ✅ | `^0\.1\.\d+$` |
| `units` | object | ✅ | `{length: "m", area: "sqm"}` |
| `metrics` | object | ✅ | minProperties: 1, key 自定义 |

**每个 metric 对象**:
| 字段 | 类型 | 必需 | 约束 |
|---|---|---|---|
| `status` | enum | ✅ | "known"/"unknown"/"not_applicable" |
| `value` | number\|null | ✅ | known 时必须为数字; unknown 时必须为 null |
| `unit` | enum | ✅ | "sqm"/"m"/"ratio"/"count"/"index"/"none" |
| `source_files` | string[] | ✅ | — |
| `formula` | string | ✅ | — |
| `confidence` | enum | ✅ | "high"/"medium"/"low"/"unknown" |
| `assumptions` | string[] | ✅ | — |
| `reason` | string | ⚠️ | 仅 status="unknown" 时必需 |

**特殊规则**: unit="ratio" 时 value 须在 0-1 之间。

---

## 7. proposal.md frontmatter 必需字段

| 字段 | 类型 | 必需 | 约束 |
|---|---|---|---|
| `title` | string | ✅ | — |
| `author_github` | string | ✅ | 必须与 PR 作者和目录名匹配 |
| `language` | string | ✅ | "zh" 或 "en" |
| `license` | string | ✅ | "COMMUNITY-DISPLAY-ONLY"/"CC-BY-4.0"/"CC-BY-SA-4.0" |
| `summary` | string | ✅ | — |

**可选 frontmatter 字段**:
- `translation_file`: 翻译文件路径
- `tracks`: 数组, max 3 个, 须在 tracks.json 注册
- `scenarios`: 数组, max 8 个, 须在 scenarios/ 注册
- `iteration`/`version`: 格式 `v?\d+(\.\d+){0,2}([-+][A-Za-z0-9.-]+)?`
- `proposal_format_version`: "1" 或 "2"
- `bilingual_contract_version`: "1" (需同时设 proposal_format_version="2")

**proposal.md 必需章节** (13 个 `## ` 标题):
1. 设计依据与资料清单
2. 三层范围工作框架
3. 统筹研究范围产业与未来城市研究
4. 总体设计范围城市更新与控规深度城市设计
5. 重点区域详细设计
6. AI 创新生态、人才画像与 AI+ 场景
7. 用地、建筑规模与拆改留方案
8. 交通、轨道、市政与公共服务设施
9. 蓝绿空间、公共空间与城市风貌
10. 更新项目清单、实施政策与分期计划
11. 指标体系、面积复算与合规矩阵
12. 风险、版权与合规说明
13. 参考资料

**正文规则**:
- 每个必需章节至少包含一个机读证据引用 `[source:...]`, `[standard:...]`, `[depth:...]`, `[data:...]`, `[metric:...]`
- 每个章节至少 280 个非空白字符
- 正文总计至少 5000 个非空白字符
- 必须嵌入 5 张必需图片: `site-overview.png`, `land-use-structure.png`, `key-areas.png`, `mobility-bluegreen.png`, `metrics-evidence.png`
- 禁止模板占位符: "your-github-login", "方案标题", "用 200-400 字说明", "请用 3-5 句话"
- 禁止硬风险模式 (身份证号、手机号、伪造官方批准)
- 每段最多 8 个证据标记, 连续最多 3 个

---

## 8. GeoJSON FeatureCollection 必需属性

**顶层**:
- `type`: "FeatureCollection"
- `features`: array

**每个 Feature**:
- `type`: "Feature"
- `id`: string (minLength: 2, 唯一)
- `properties.id`: string (minLength: 2)
- `properties.layer`: string (须在 layers.json 注册的 code 中)
- `properties.source_type`: string (须在 source_types 枚举中)
- `properties.confidence`: string (须在 confidence_levels 枚举中)
- `properties.geometry_role`: string (须在 geometry_roles 枚举中)
- `geometry.type`: "Point"/"LineString"/"MultiLineString"/"Polygon"/"MultiPolygon"
- `geometry.coordinates`: 合法坐标 (lon: -180~180, lat: -90~90)
- Polygon 环必须闭合 (首尾相同, 至少 4 个点)

**可选属性**: `area_sqm_declared`(number|null), `building_type`(须在 building_types.json 中), `land_use_code`(须在 land_use_codes.json 中), `road_class`(须在 road_classes.json 中), `official_boundary`(bool, site_boundary 专用), `name_zh`, `name_en`, `height_note` 等

**Geometry 文件清单** (9 个):
```
site_boundary.geojson, key_areas.geojson, land_use.geojson, buildings.geojson,
roads.geojson, green_space.geojson, public_space.geojson, constraints.geojson, phasing.geojson
```

**Formal 阶段非空要求**: site_boundary, key_areas, land_use, roads, green_space, public_space, phasing 必须至少有 1 个 feature。

---

## 9. 枚举值汇总

### source_types (来源类型)
```
official_public, official_open_data, osm, user_provided_cleared,
agent_generated_design, agent_inferred_from_public_data, unknown
```

### confidence_levels (可信度)
```
high, medium, low, unknown
```

### geometry_roles (几何角色)
```
official_constraint, provisional_constraint, existing_condition,
design_proposal, analysis_helper, map_viewport
```

### layers (图层 code)
```
SITE_BOUNDARY, KEY_AREA, LAND_USE, PARCEL, BUILDING_FOOTPRINT,
ROAD_CENTERLINE, ROAD_AREA, GREEN_SPACE, PUBLIC_SPACE, WATER_SYSTEM,
HERITAGE_PROTECTION, REGULATORY_CONTROL, PHASE, AI_SERVICE_ZONE,
SCENARIO_NODE, EXISTING_PRIMARY_ROAD, EXISTING_RAIL, EXISTING_WATER
```

### building_types (建筑类型)
```
ai_r_and_d, lab, incubator, office, mixed_use, education, residential,
talent_apartment, community_service, retail, cultural, mobility_hub, existing_retained
```

---

## 10. 文件大小限制

| 类型 | 限制 |
|---|---|
| Markdown | 256 KB |
| JSON | 512 KB |
| GeoJSON | 10 MB |
| Asset (图片) | 5 MB |
| Drawing (PDF) | 10 MB |
| HTML | 2 MB |
| Visual asset | 5 MB |
| 总计 | 40 MB |

---

## 11. 其他验证规则

- **禁止符号链接**: 提交目录不得包含符号链接
- **HTML 安全**: report/proposal.html 禁止 script/iframe/form/fetch/XHR/WebSocket/外部资源加载
- **visual/index.html**: 禁止 iframe/form/fetch/XHR/WebSocket/EventSource/外部资源
- **changelog.md**: 必须有 `# 方案迭代记录` 标题和至少一个 `## v{X.Y} - YYYY-MM-DD` 格式版本标题
- **bilingual**: v2 格式方案需中英双语, 所有展示文件需有对应语言版本
- **sha256 校验**: manifest.json 中列出的文件需包含 sha256 且与实际内容匹配 (professional_design_package 强制)
- **author_github 匹配**: 必须与 PR 作者和提交路径中的用户名一致 (大小写不敏感)
