---
description: 端到端交付需求的轻量入口，按当前阶段调用对应 Skill 和 Gate
---

请使用 `deliver-requirement` Skill 交付当前需求。

用户原始输入：
$ARGUMENTS

执行要求：
1. 本 Command 只做入口和参数透传，不复制 PRD、设计、编码、测试、评审细则。
2. 必须读取并遵循 `WORKFLOW.md`。
3. 必须调用 `skills/deliver-requirement` 识别当前阶段、定位已有产物、执行下一步。
4. 正式质量裁决必须交给 `tzh-review`，本 Command 不得自行给出上线通过结论。
5. 遇到 `UNKNOWN` 或 `NOT_EXECUTED` 必须保留并传递到 Gate，不得改写为通过。
