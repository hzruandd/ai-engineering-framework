# tzh-review 使用说明

`tzh-review` 用于在停智慧智慧停车生态平台场景下，对代码变更执行正式评审。它不是简单的 diff 总结，而是一套带强门禁的评审工作流：先核验 TAPD，再扫描变更，再做代码、数据库、测试、安全、部署回滚评审，最后输出正式报告与放行结论。

这份 Skill 设计为一套可兼容 Claude Code 与 Codex 的共享核心：
- Claude Code 可通过薄 Command 或自然语言触发。
- Codex 可通过自然语言、路由规则或全局 Skill 触发。
- 无论在哪个平台，核心评审逻辑都以 Skill 为准。

## 适用场景

- 提测前代码评审
- 上线前代码评审
- 当前分支质量门禁
- 多项目、多服务联合发布评审
- SQL、字段、索引、DDL、DML、数据修复脚本评审
- Doris、Dinky、MV、报表口径影响评审
- 订单、支付、计费、月租、券包、发票、清分、对账、权限、开闸链路评审

## 触发方式

1. 支持命令的平台，可用命令触发

```text
/tzh-review tapd=TAPD-123456
/tzh-review tapd=TAPD-123456,TAPD-123457
/tzh-review tapd=TAPD-123456 baseline=release/2026.05
```

2. 所有平台均可用自然语言触发

```text
帮我评审当前分支代码，tapd=TAPD-123456
生成停智慧代码评审报告，tapd=TAPD-123456
检查这次 SQL 和数据库字段变更风险，tapd=TAPD-123456
做一次上线前评审，tapd=TAPD-123456,TAPD-123457
```

## 推荐输入契约

推荐用户尽量用“自然语言 + 参数化字段”的方式输入，这样在 Claude Code 和 Codex 上都更稳定：

```text
帮我评审当前分支代码，tapd=TAPD-123456
生成停智慧代码评审报告，tapd=TAPD-123456 baseline=release/2026.05
检查这次 SQL 风险，tapd=TAPD-123456 scope=sql
帮我评审 order-service 和 billing-service，tapd=TAPD-123456,TAPD-123457
```

推荐字段：
- `tapd`：必填
- `baseline`：可选，默认 `master`
- `scope`：可选
- `projects` 或 `services`：可选
- `mode`：可选，支持 `formal-gate`、`db-only`、`security-only`、`release-gate`
- `output`：可选，支持 `summary`、`full-report`
- `overwrite`：可选，支持 `overwrite=true` 或 `output.overwrite=true`

## 强门禁

### 1. TAPD 必填

- 未提供 TAPD 编号时，必须先补 TAPD，正式评审暂停。
- 不允许仅凭分支名或 commit message 猜测 TAPD 并继续。
- 支持多个 TAPD，但每个 TAPD 都要对应本次变更目标。
- 如果只给 TAPD 编号、未给本次变更目标，正式门禁必须继续追问。
- 若根据代码或上下文推断 TAPD 目标，必须标记为 `Inferred`。

### 2. baseline 默认 `master`

- 用户不指定时，默认用 `master`。
- 用户不主动指定时，不询问、不变更。
- 只有用户明确指定 `baseline`、`base`、`target`、目标分支、release 分支、tag、commit 时，才允许覆盖。

### 3. 多项目自动识别

命中以下任一情况即进入多项目模式：
- 多个 Git 仓库
- 多个应用模块
- diff 触达多个服务目录
- 多个 Spring Boot 启动类
- 多个 `spring.application.name`
- 多个 Dockerfile、Jenkinsfile、k8s 部署单元
- 用户一次性点名多个项目或服务

### 4. 未提交改动必须显式识别

- 除 `baseline...HEAD` 外，还要检查 `staged diff`、`working tree diff`、`untracked files`。
- `release-gate` 模式下，如果未提交改动也被用户纳入提测或上线范围，至少标为 `P1`，直到提交边界清晰。

## 输出内容

评审结束后，至少应输出：
- 管理层摘要
- 正式评审报告
- TAPD 追踪矩阵
- 文件/变更到 TAPD 的反向追踪矩阵
- 风险矩阵
- 行动项
- 证据表
- Unknowns 与人工确认项
- 单项目或多项目放行结论

## 输出文件命名

- 正式评审报告默认文件名固定为：`智慧停车生态_代码评审报告_v1.4_<日期>.md`
- `<日期>` 固定使用 `YYYY-MM-DD`
- 默认示例：`智慧停车生态_代码评审报告_v1.4_2026-05-09.md`
- 不再默认使用 `TAPD1003440`、`by_codex`、`by_cc`、分支名、评审人等附加后缀
- 除非用户明确要求其他命名方式，否则统一按该文件名输出
- 同名文件只有在用户显式传入 `overwrite=true` 或 `output.overwrite=true` 时才允许覆盖
- 未显式允许覆盖时，不得静默覆盖；优先自动追加 `_1`、`_2`、`_3` 等后缀

## 格式稳定性要求

这套 Skill 的正式报告不是“每次自由发挥”的 Markdown，而是固定模板输出：
- 必须从 `templates/code-review-report-v1.4.md` 展开。
- 必须保持主标题、封面信息表、目录、一级章节顺序、附录顺序一致。
- 如遇新增场景，优先在既有章节内补子标题或补表格行，不新造一级章节。
- 详细约束见 `references/report-format-contract.md`。

## Token 使用策略

为避免每次评审都消耗过多 token，这套 Skill 默认采用按需加载：
- 总是先读取 `SKILL.md`。
- 总是先复制 `templates/code-review-report-v1.4.md` 的固定骨架。
- 只在命中对应场景时再读取专项清单，不默认全量读取全部 checklist。
- 数据库路径先读 `checklists/db-sql-gate.md`，只有确认命中数据库专项后，再读 `checklists/db-sql-review.md`。
- `README`、`examples`、`references/report-format-contract.md` 只在说明用法或校验格式时再使用。

推荐理解为：
- `SKILL.md`：运行时门禁与路由
- `template`：固定输出骨架
- `gate checklist`：快速判断是否要进入专项
- `deep checklist`：只有命中专项才加载

## 执行模式

- `formal-gate`
  - 默认正式评审模式
  - TAPD 必填
  - 输出正式结论
- `db-only`
  - 聚焦数据库、SQL、DDL、DML、索引与修复脚本
  - 仍需记录由数据库变更直接引发的业务、测试、发布、回滚、对账与报表同步风险
- `security-only`
  - 聚焦脱敏、加密、密钥、审计、权限、防重放、租户隔离
  - 仍需记录由安全变更直接引发的可用性、误拦截、运营后台、合规、发布与回滚风险
- `release-gate`
  - 上线前门禁
  - 强制补充部署、回滚、上线验证和未提交改动边界

## 静态扫描策略

- 老项目默认不要求 Sonar，不作为评审启动条件，也不作为默认放行门禁。
- 若用户或项目已提供 Sonar/其他静态扫描结果，可作为第 `7` 章补充证据写入报告。
- 未提供 Sonar 时，不需要停下来补扫；只要如实说明“未提供”或“不要求”即可。
- 已提供静态扫描结果时，只记录与本次变更直接相关的问题，不展开历史遗留全量问题。

## 评分规则

这套 Skill 保留 `100` 分制，但分数是辅助表达，不覆盖风险裁决。

固定权重如下：
- 业务正确性与链路一致性：`25%`
- 数据库与 SQL 质量：`20%`
- 测试与回滚准备度：`15%`
- 设计与实现合理性：`10%`
- 安全与租户隔离：`10%`
- 性能与容量影响：`8%`
- TAPD 追踪与评审范围识别：`7%`
- 日志与可观测性：`5%`

固定计算规则：
- 每个维度先按 `100` 分制打“维度得分”。
- `加权得分 = 维度得分 × 权重`
- `综合评分 = Σ加权得分`
- 不允许写“主观权重调整”或人工二次调权。

基础扣分口径：
- `P0`：相关维度直接落入 `0-59` 分区间，且整体直接不通过。
- 未闭环 `P1`：相关维度通常每项扣 `10-15` 分，且该维度最高不超过 `79` 分。
- `P2`：相关维度通常每项扣 `4-8` 分。
- `P3`：相关维度通常每项扣 `1-3` 分。
- 核心域 `Unknown` 未确认：相关维度最高不超过 `74` 分。
- 非核心 `Unknown` 未确认：相关维度最高不超过 `84` 分。

维度重点扣分参考：
- 业务正确性：幂等、状态机、补偿、账务一致性问题优先重扣。
- 数据库与 SQL：`EXPLAIN`、字段兼容性、索引依据、回滚脚本、验证 SQL、报表口径影响优先重扣。
- 测试与回滚：核心主路径、异常路径、数据回滚、上线验证缺失优先重扣。
- TAPD 追踪：核心变更未关联 TAPD、多项目漏评优先重扣。

结论优先级：
- 有 `P0`：直接不通过
- 有未闭环 `P1`：最多有条件通过
- 分数再高，也不能覆盖上述门禁

## 目录结构

```text
tzh-review/
├── SKILL.md
├── README.md
├── templates/
├── checklists/
└── examples/
```

平台入口可以不同，但 Skill 目录内容应保持一致：
- Claude Code 可搭配 `.claude/commands/tzh-review.md`
- Codex 可安装到 `.codex/skills/tzh-review`
- 核心逻辑不要分叉到多个平台专属版本

## 推荐使用流程

1. 提供 TAPD 编号与本次变更目标。
2. 如有非 `master` 基线，显式说明 baseline。
3. 如需专项评审，可显式指定 `mode=db-only`、`mode=security-only` 或 `mode=release-gate`。
4. 让 `tzh-review` 自动识别单项目或多项目模式，并区分 committed / staged / working tree / untracked。
5. 基于正式报告模板输出评审结果。
6. 根据行动项闭环后，再决定是否放行。

## 何时一定要走数据库专项

只要变更涉及以下任一内容，就不能跳过数据库与 SQL 专项评审：
- SQL
- 字段
- 索引
- DDL
- DML
- 修复脚本
- Doris
- Dinky
- MV
- 报表口径
- 订单、支付、计费、月租、券包、发票、清分、对账、开闸核心数据读写

## 注意事项

- 禁止预设“通过”。
- 禁止为了报告好看降低风险等级。
- P0 一律不通过。
- 未闭环 P1 不得直接通过。
- 大 diff、工具失败、baseline 不存在或关键证据缺失时，不得因为上下文或 token 限制直接给“通过”。
- 涉及手机号、车牌号、身份证、支付流水号、密钥、证书、日志导出、回调签名时，必须进入安全与合规专项。
- 评审输出中的敏感证据必须脱敏，只允许展示掩码值。
- 未提供 Sonar 时，按可选补充信息处理，不作为阻塞项。
- 未提供覆盖率、EXPLAIN、回滚脚本等证据时，应保持 Unknown，而不是代写“达标”。
