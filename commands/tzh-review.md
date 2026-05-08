---
description: 触发停智慧代码变更评审 Skill
---

请使用 `tzh-review` Skill 对当前代码变更进行停智慧代码评审。

用户原始输入：
$ARGUMENTS

执行要求：
1. 本 Command 只作为入口，不包含核心评审逻辑。
2. 所有评审流程、检查清单、风险分级、数据库专项、TAPD 追踪、多项目识别和报告生成逻辑，均以 `tzh-review` Skill 为准。
3. 如果用户未提供 TAPD 编号，必须由 Skill 主动询问 TAPD 编号，并暂停评审。
4. 默认 baseline 为 `master`；只有用户明确指定 `baseline`、`base`、`target`、目标分支、release 分支、tag 或 commit 时才允许变更。
5. 自动识别当前评审是单项目还是多项目。
6. 最终输出正式评审报告、风险矩阵、行动项、证据表、Unknowns 与人工确认项，以及放行结论。

说明：
- 本 Command 不保留详细评审规则。
- 本 Command 不保留数据库检查清单。
- 本 Command 不保留风险分级细则。
- 本 Command 不保留报告模板。
- 核心逻辑全部以 `tzh-review` Skill 为准。
