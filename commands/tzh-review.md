---
description: 触发停智慧代码变更评审 Skill
---

请使用 `tzh-review` Skill 对当前代码变更进行停智慧代码评审。

用户原始输入：
$ARGUMENTS

执行要求：
1. 本 Command 只作为入口，不包含核心评审逻辑。
2. 必须调用并遵循当前仓库中的 `city-parking-claude-doc\\skills\\tzh-review` Skill，不得在 Command 中自行生成评审结论、风险等级或报告结构。
3. 只接收并透传以下参数：`tapd`、`baseline`、`mode`、`projects`、`services`、`scope`、`output`、`overwrite`。
4. `output=summary` 时，只输出管理层摘要、风险矩阵、Unknowns、行动项，不生成完整报告文件。
5. `output=full-report` 或未指定 `output` 时，由 Skill 生成完整正式评审报告。
6. 支持透传 `overwrite=true` 或 `output.overwrite=true`；Command 不处理报告覆盖逻辑，覆盖策略完全由 Skill 决定。
7. 如果用户未提供 TAPD 编号或未说明对应变更目标，必须由 Skill 主动询问并暂停正式评审。
8. 默认 baseline 为 `master`；只有用户明确指定 `baseline`、`base`、`target`、目标分支、release 分支、tag 或 commit 时才允许变更。
9. 多项目识别、变更地图、数据库专项、安全专项、工具失败降级、报告模板、风险裁决全部以 Skill 为准。

说明：
- 本 Command 不保留详细评审规则。
- 本 Command 不保留数据库检查清单。
- 本 Command 不保留风险分级细则。
- 本 Command 不保留报告模板。
- 本 Command 不保留覆盖同名报告的处理逻辑。
- 核心逻辑全部以 `tzh-review` Skill 为准。
