---
description: 调用 review-code Skill 做提测前轻量自查，不承担正式质量裁决
---

# 代码自查入口

请使用 `review-code` Skill 对当前代码或指定范围做提测前轻量自查。

用户原始输入：
$ARGUMENTS

## 职责边界

1. 本 Command 只做入口，不复制审查清单。
2. 详细执行逻辑以 `skills/review-code/SKILL.md` 为准。
3. 停智慧正式质量裁决必须使用 `tzh-review`。
4. 本入口可以输出自查问题、建议和风险线索，但不得给出正式上线“通过”结论。
5. 如果发现 P0/P1、核心 Unknown、DB/SQL、安全、发布风险，必须建议进入 `/tzh-review`。

## 质量事实源

- Mapper 规范：`rules/java-mapper-rule.md`
- 覆盖率阈值：`config/quality-thresholds.yaml`
- 正式评审：`skills/tzh-review/SKILL.md`
