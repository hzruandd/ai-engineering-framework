---
name: tzh-review
description: Use when需要对停智慧智慧停车生态平台代码变更做正式评审，或用户提到代码评审、当前分支评审、提测前评审、上线前评审、SQL评审、数据库变更评审、索引评审、生成代码评审报告、tzh-review。
intent: >-
  Review Tingzhihui code changes before test or release, enforce TAPD traceability,
  detect single-project or multi-project scope, audit code, SQL, database, configuration,
  test and rollback risks, and generate a formal review report with evidence, risks,
  action items, unknowns, and release decision.
type: workflow
best_for:
  - 停智慧代码变更评审
  - 提测前评审
  - 上线前评审
  - 多服务联合变更评审
  - SQL、数据库、索引、DDL、DML 评审
scenarios:
  - "/tzh-review tapd=TAPD-123456"
  - "/tzh-review tapd=TAPD-123456,TAPD-123457 baseline=release/2026.05"
  - "帮我评审当前分支代码，tapd=TAPD-123456"
  - "生成停智慧代码评审报告，tapd=TAPD-123456"
  - "检查这次 SQL 和数据库字段变更风险，tapd=TAPD-123456"
---

# tzh-review

## Purpose

`tzh-review` 是停智慧代码变更评审门禁 Skill。它负责用统一流程把 `Git diff`、`TAPD`、项目边界、数据库风险、测试与回滚信息串成正式评审报告，不预设“通过”。

## Platform Compatibility

- Claude Code：可走薄 Command 或自然语言。
- Codex：走自然语言或全局 Skill。
- 核心规则只保留在本 Skill，平台入口不得分叉核心逻辑。

## Fast Trigger

遇到以下表达，直接进入本 Skill：
- 代码评审
- 当前分支评审
- 提测前评审
- 上线前评审
- SQL 评审
- 数据库变更评审
- 索引评审
- 生成代码评审报告
- `tzh-review`

## Input Contract

- `tapd`：必填，支持多个
- `baseline`：可选，默认 `master`
- `projects`：可选
- `services`：可选
- `scope`：可选，如 `sql`、`db`、`pre-release`
- `mode`：可选，支持 `formal-gate`、`db-only`、`security-only`、`release-gate`
- `output`：可选，支持 `summary`、`full-report`
- `overwrite`：可选，支持 `overwrite=true` 或 `output.overwrite=true`

可接受表达：
- `tapd=TAPD-123456`
- `tapd=TAPD-123456,TAPD-123457 baseline=release/2026.05`
- `帮我评审当前分支代码，tapd=TAPD-123456`
- `检查这次 SQL 风险，tapd=TAPD-123456 scope=sql`

输入约束：
- 所有模式下，除了提供 `tapd`，还必须说明每个 TAPD 对应的本次变更目标。
- 若用户只提供 TAPD 编号但未说明变更目标，正式门禁必须继续追问，不得直接生成正式结论。
- 若根据用户输入、分支名、commit、文件路径或代码变更推断了 TAPD 目标，必须标记为 `Inferred`，不得伪装成 TAPD 原始信息。

## Command Rule

如果平台支持 `/tzh-review`：
- Command 只做入口和参数透传。
- 流程、风险、模板、数据库专项、TAPD 追踪、多项目识别全部以本 Skill 为准。

## Output Filename Rule

- 正式评审报告默认文件名固定为：`智慧停车生态_代码评审报告_v1.4_<日期>.md`
- `<日期>` 固定使用 `YYYY-MM-DD`
- 默认示例：`智慧停车生态_代码评审报告_v1.4_2026-05-09.md`
- 不得在默认文件名中追加 `TAPD`、`by_codex`、`by_cc`、分支名、仓库名、评审人等随机后缀
- 除非用户明确要求其他命名方式，否则统一使用该默认文件名
- 若同一路径下同日期文件已存在，只有在用户明确传入 `overwrite=true` 或 `output.overwrite=true` 时才允许覆盖
- 用户未明确要求覆盖时，不得静默覆盖；优先自动追加 `_1`、`_2`、`_3` 等后缀，或在交互式场景中提示确认
- 报告必须记录输出文件路径、是否覆盖、是否自动追加后缀
- `output=summary` 时，只输出管理层摘要、风险矩阵、Unknowns、行动项，不生成完整报告文件
- `output=full-report` 或未指定 `output` 时，生成完整正式评审报告
- 不得因报告输出失败而伪装成评审完成

## TAPD Gate

硬规则：
- 所有模式下，TAPD 必填；缺失时先询问并暂停。
- 所有模式下，缺少 TAPD 或缺少 TAPD 对应的变更目标时，不得启动正式评审，不得生成正式放行结论。
- 不允许仅凭分支名、目录名、commit message 猜 TAPD 后继续。
- 支持多 TAPD，但每个 TAPD 都必须有本次变更目标。
- 必须同时输出：
  - `TAPD -> 项目/服务/文件/变更`
  - `文件/变更 -> TAPD`
- 若 TAPD 目标由代码、分支、目录或用户上下文推断得到，必须在追踪矩阵和结论中标记为 `Inferred`。
- 无法关联的代码、SQL、DDL、配置、脚本、测试改动标记为 `Unknown`。
- Unknown 命中核心业务、数据库、SQL、支付、订单、发票、清分、对账、权限、开闸、租户隔离时，至少 `P1`；若已影响资金、核心数据正确性或出入场可用性，直接 `P0`。

缺 TAPD 时统一提问：

```text
开始评审前需要 TAPD 编号。请提供一个或多个 TAPD 编号，并分别说明每个 TAPD 对应的本次变更目标。
示例：TAPD-123456：停车订单补单；TAPD-123457：月租续费索引优化
```

## Baseline Rule

- 默认 baseline 是 `master`。
- 用户不主动指定时，不询问、不变更。
- 只有用户明确指定 `baseline/base/target/目标分支/release/tag/commit` 时才允许覆盖。
- 多项目模式下每个项目可独立记录 baseline。
- 报告必须记录每个项目实际 baseline。

优先级：
1. 用户显式指定的项目级 baseline
2. 用户显式指定的全局 baseline
3. 默认 `master`

## Execution Modes

- `formal-gate`
  - 默认模式
  - TAPD 必填
  - 允许给出正式放行结论
- `db-only`
  - 评审重点聚焦数据库、SQL、DDL、DML、索引、数据修复脚本
  - 仍要求 TAPD
  - 不得屏蔽由数据库变更直接引发的业务正确性、数据一致性、发布、回滚、测试验证、对账、报表 / Doris / Dinky / Flink 同步风险
- `security-only`
  - 评审重点聚焦鉴权、授权、脱敏、加密、密钥、审计、租户隔离、防重放
  - 仍要求 TAPD
  - 不得屏蔽由安全变更直接引发的业务不可用、权限误拦截、运营后台无法操作、用户隐私与数据合规、发布与回滚风险
- `release-gate`
  - 上线前门禁模式
  - TAPD 必填
  - 必须补充部署、回滚、上线验证与未提交改动检查

专项模式共通规则：
- `db-only`、`security-only` 只表示评审重点范围，不表示可以忽略关联高风险问题。
- 若专项模式发现非专项但高风险的问题，必须正常记录，不得因为 `mode` 限制而忽略。
- 专项模式输出结论时，必须说明“本次结论仅针对专项重点范围；但已记录由专项变更直接引发的关联风险”。

## Multi-project Detection

命中任一条件即进入多项目模式：
- 多个 Git 仓库
- 多个应用模块
- diff 触达多个服务目录
- 多个 Spring Boot 启动类
- 多个 `spring.application.name`
- 多个 Dockerfile / Jenkinsfile / k8s 部署单元
- 用户一次性点名多个项目、服务或仓库路径

多项目规则：
- 每个项目分别做 diff、变更清单、代码质量、SQL、配置、测试、回滚检查。
- 最后统一做跨项目链路分析，输出一份总报告并保留各项目独立结论。
- 任一核心项目 `P0`，整体“不通过”。
- 任一核心项目存在未闭环 `P1`，整体最多“有条件通过”。

## Execution Workflow

固定顺序：
1. 识别触发方式与执行模式
2. 校验 TAPD
3. 解析 baseline
4. 识别单项目或多项目
5. 扫描 committed / staged / working tree / untracked 变更范围
6. 建立变更地图
7. 建立 TAPD 追踪矩阵
8. 执行代码评审
9. 执行数据库与 SQL 专项
10. 执行测试、性能、安全、部署回滚评审
11. 消费测试、自测、构建、CI、PRD、设计和 Gate 证据
12. 输出风险分级
13. 输出放行结论或预评审限制说明
14. 生成正式评审报告

## Phase 2 Evidence Inputs

正式评审应主动查找并消费以下标准产物；找不到时必须记录为 `Unknown` 或 `NOT_EXECUTED`，不得写成已通过：

- PRD：`docs/requirements/<requirement-id>/prd.md`
- 设计：`docs/requirements/<requirement-id>/design.md`
- 任务：`docs/deliveries/<requirement-id>/tasks.md`
- 测试计划：`docs/deliveries/<requirement-id>/test-plan.md`
- 自测报告：`docs/deliveries/<requirement-id>/self-test-report.md`
- 发布门禁：`docs/deliveries/<requirement-id>/release-gate.md`
- 质量阈值：`config/quality-thresholds.yaml`
- Gate 模型：`gates/README.md`

必须明确回答：

1. 哪些测试实际执行过；
2. 执行命令是什么；
3. 测试结果是什么；
4. 覆盖了哪些需求和验收标准；
5. 哪些测试没有执行；
6. 哪些场景仍为 `Unknown`；
7. 是否存在阻断项；
8. 是否具备提交人工上线签发的条件。

规则：

- 生成了测试代码不等于测试已执行。
- `UNKNOWN` 和 `NOT_EXECUTED` 不得自动等同于 `PASS`。
- 覆盖率阈值以 `config/quality-thresholds.yaml` 为准。

## Token Control Strategy

默认按“轻入口、按需加载”执行，避免每次全量读完所有文档：

1. 总是先加载本 `SKILL.md`。
2. 总是从 `templates/code-review-report-v1.4.md` 复制固定骨架。
3. 只在需要时再加载专项清单：
   - 变更总览：`checklists/diff-review.md`
   - TAPD：`checklists/tapd-traceability.md`
   - 多项目：`checklists/multi-project-review.md`
   - Java / Spring：`checklists/java-spring-review.md`
   - 安全：`checklists/security-review.md`
   - 测试：`checklists/test-review.md`
   - 部署回滚：`checklists/deploy-rollback-review.md`
4. 数据库路径分两层：
   - 先读 `checklists/db-sql-gate.md` 做轻门禁
   - 只有命中 SQL、字段、索引、DDL、DML、修复脚本、Doris、Dinky、MV、报表口径或核心数据读写时，才读 `checklists/db-sql-review.md`
5. `README`、`examples`、`references/report-format-contract.md` 只在说明用法或校验格式漂移时再加载，不作为每次评审默认上下文。

## Change Scanning

先用 Git 建立变更地图，再做判断。必查命令：
- `git status`
- `git status --short`
- `git branch --show-current`
- `git log baseline..HEAD`
- `git diff --stat baseline...HEAD`
- `git diff --name-status baseline...HEAD`
- `git diff baseline...HEAD`
- `git diff --cached`
- `git diff`
- `git ls-files --others --exclude-standard`

多项目模式下对每个项目分别执行，并记录项目根路径。

变更地图至少输出：
- `committed diff`
- `staged diff`
- `working tree diff`
- `untracked files`
- 变更文件清单
- 变更类型清单
- 涉及项目/服务列表
- 涉及业务域列表
- 涉及数据库对象、SQL、索引、脚本列表
- 涉及发布单元、配置项、外部依赖列表

补充规则：
- `release-gate` 模式下，若存在 `staged diff`、`working tree diff` 或 `untracked files` 且用户声称这些改动会随提测/上线进入范围，至少记 `P1`，直到提交边界明确。
- 若用户只要求评审已提交代码，必须在报告中明确未提交改动未纳入正式结论。

## Large Diff Handling

命中以下任一条件时，必须进入大 diff 模式：
- 变更文件超过 `30` 个
- diff 规模超过模型可稳定处理范围
- 多项目 / 多服务联合变更
- 包含大量生成代码、前端构建产物、SQL 脚本或配置文件

大 diff 模式固定顺序：
1. 先执行并分析：
   - `git diff --stat`
   - `git diff --name-status`
   - 必要时执行 `git status --short`
2. 建立完整变更地图，至少区分：
   - `committed diff`
   - `staged diff`
   - `working tree diff`
   - `untracked files`
3. 按风险优先级展开具体 diff：
   - SQL / DDL / DML / Mapper / DAO
   - 支付、订单、计费、月租、券包、发票、清分、对账、开闸
   - 权限、租户隔离、鉴权、导出、脱敏、密钥
   - 配置、Nacos、Dubbo、MQ、XXL-Job、Doris、Dinky
   - 核心业务 Java 代码
   - 测试代码、发布脚本、文档
   - 静态资源、样式、低风险文案
4. 单文件 diff 过大时，先摘要，再针对关键函数、SQL、配置块展开。

大 diff 模式补充规则：
- 无法读取、未展开或只完成摘要的文件不得忽略，必须进入 `Unknowns`。
- 不允许因为 token 限制直接给出“通过”。
- 若 `Unknown` 命中核心业务、数据库、安全或发布链路，至少按 `P1` 处理。
- 报告必须说明大 diff 模式下的扫描范围、已展开文件、未展开文件和原因。

## Evidence Rules

所有结论必须带证据。没有证据时，不得伪装成确定结论。

证据类型：
- `SRC`：源码
- `SQL`：SQL、Mapper、XML SQL
- `DDL`：数据库脚本
- `IDX`：索引定义
- `EXP`：EXPLAIN
- `CFG`：配置
- `MQ`：消息
- `JOB`：定时任务
- `TEST`：测试
- `SONAR`：静态扫描结果（可选）
- `LOG`：日志

判断类型：
- `Observed`
- `Inferred`
- `Unknown`

规则：
- 风险项必须绑定证据编号。
- 结论必须标明判断类型。
- Unknown 必须进入“Unknowns 与人工确认项”。
- 证据若包含敏感信息，只允许记录文件路径、行号、字段名、部分掩码值和风险说明，不得原样复制完整敏感值。

## Database Review Gate

只要涉及以下任一内容，就必须进入数据库专项：
- SQL、字段、索引、DDL、DML、数据修复脚本
- Doris、Dinky、MV、报表口径
- 订单、支付、计费、月租、券包、发票、清分、对账、开闸等核心数据读写

数据库专项至少覆盖：
- SQL 查询质量
- `UPDATE/DELETE` 精确 `WHERE`
- 字段兼容性
- 索引设计
- 大表 DDL
- 修复脚本幂等与回滚
- EXPLAIN
- Doris / Dinky / MV / 报表同步影响
- 前滚脚本、回滚脚本、验证 SQL

## Business Domain Review Gate

命中以下领域时，必须做核心业务链路专项评审：
- 临停缴费
- 月租续费
- 券包核销
- 共享车位
- 发票
- 清分
- 对账
- 设备开闸
- 权限与租户隔离

重点关注：
- 幂等
- 状态机
- 补偿
- 账务一致性
- 出入场可用性
- 多租户隔离

## Security And Compliance Gate

命中以下任一内容时，必须加载 `checklists/security-review.md` 并进入安全与合规专项：
- 登录、权限、角色、租户、停车场、商户、组织隔离
- 手机号、车牌号、身份证、姓名、地址、支付流水号、设备序列号等敏感数据
- 导出、报表、下载、打印、消息推送、Webhook、回调
- 密钥、token、appSecret、支付证书、OSS 凭证、短信签名、Nacos 密文配置
- 支付、核销、开票、开闸、防重、防刷、防重放链路
- 日志、审计、埋点、补偿脚本、数据修复脚本

安全与合规专项至少覆盖：
- 鉴权、授权、越权、租户/停车场/商户隔离
- 敏感字段脱敏、最小化返回、导出脱敏
- 传输与存储加密、密钥管理、配置明文泄露
- 接口签名、防重放、防刷、防重复提交
- 日志脱敏、审计留痕、关键操作可追责
- SQL 注入、XSS、文件上传下载、对象存储访问控制
- 合规留痕：是否能说明敏感数据处理目的、范围、责任人

## Sensitive Evidence Redaction

命中以下敏感信息时，报告与证据表不得完整原样输出：
- 密码
- token
- `appSecret`
- `accessKey`
- `secretKey`
- 证书
- 私钥
- 数据库连接串
- OSS / 云服务凭证
- 支付密钥
- 手机号
- 身份证号
- 车牌号
- 支付流水号
- 用户隐私字段

输出规则：
- 只允许输出文件路径、行号、字段名、部分掩码值和风险说明。
- 掩码示例：
  - `ak_live_****abcd`
  - `jdbc:mysql://host:3306/db?user=****`
  - `陕A****1`
  - `138****1234`
- 高敏凭证疑似泄露时，至少标记为 `P1`。
- 若凭证已经入仓、可能进入日志、可能进入前端包、可能进入发布产物或可能被外部访问，应按 `P0` 评估。
- 必须建议：立即轮换密钥、清理提交历史、检查配置中心、检查发布产物、检查日志与监控系统、通知相关负责人。
- 即使是证据表，也不得原样展示完整敏感值。

## Tool Failure And Degradation

命中以下任一场景时，必须进入工具失败降级处理：
- 当前目录不是 Git 仓库
- baseline 分支、tag 或 commit 不存在
- Git 命令执行失败
- 文件读取失败
- diff 过大无法完整读取
- TAPD 信息不可访问
- 测试命令失败或无法执行
- `EXPLAIN` / 数据库连接不可用
- 静态扫描工具不可用
- 多项目中某个项目无法进入目录或无法读取

降级规则：
- 必须记录失败项、失败命令、失败原因、影响范围。
- 不得假装已经完成验证。
- 受影响部分必须进入 `Unknowns`。
- 若 `Unknown` 命中核心业务、数据库、SQL、支付、订单、发票、清分、对账、权限、开闸、发布链路、回滚链路，至少按 `P1` 处理。
- 如果失败导致正式门禁无法判断，不得给出“通过”。
- 如果只是低风险辅助工具失败，可以继续评审，但必须在报告中说明限制。
- 报告中必须有“工具执行失败与降级说明”小节，或在 `Unknowns` 中体现。

## Risk Levels

### P0

- 资金错账、重复扣款、错误退款
- 订单丢失、支付状态不一致
- 大量用户无法进出场
- 核心表 `UPDATE/DELETE` 缺少精确 `WHERE`
- 支付回调、券核销、开票缺少幂等
- 大表 DDL 无评估、无回滚、无验证 SQL
- 缺少停车场、商户、租户隔离
- 清分、对账、发票口径变更无验证
- 支付密钥、appSecret、证书、短信密钥等高敏凭证明文入库或入仓
- 支付、开票、开闸、核销接口缺少签名校验或可被重放
- 导出、日志、消息体明文泄露大批量敏感信息且无补救措施

### P1

- 核心 SQL 未提供 EXPLAIN
- 字段兼容性不明确
- 索引设计依据不足
- 数据修复脚本不可重复执行
- 缺少关键链路日志或 traceId
- Doris、Dinky、报表同步影响未确认
- 测试未覆盖核心异常路径
- 只有代码回滚，没有数据回滚或兼容策略
- 关键领域 Unknown 未人工确认
- 手机号、车牌号、身份证、支付流水号未按规范脱敏
- 敏感配置是否加密、是否走密文配置中心无法确认
- 关键安全审计、操作留痕、导出留痕缺失
- 存在密钥泄露嫌疑但未完成排查与轮换说明

### P2

- 非核心链路可维护性风险
- 中等影响的性能或观测性不足
- 设计边界、异常处理、日志、命名、重复代码问题

### P3

- 轻微优化项
- 注释、风格、局部重构建议

## Decision Rules

正式门禁结论仅允许：
- 通过
- 有条件通过
- 不通过

裁决规则：
- 禁止预设“通过”。
- 禁止为了报告好看降低风险等级。
- `P0` 一律“不通过”。
- 未闭环 `P1` 不得直接“通过”。
- 所有模式下，缺少 TAPD 或缺少 TAPD 变更目标时，不允许启动正式评审，也不允许输出正式门禁结论。
- 关键证据缺失时，不允许输出“通过”。
- 关键工具失败导致核心链路未验证时，不允许输出“通过”。
- 核心域 `Unknown` 未确认，不得给“通过”。
- `Unknowns` 可通过人工确认闭环时，最多输出“有条件通过”，且必须列出条件、责任人和验证方式。
- `Unknowns` 命中 `P0` 风险时，不得“有条件通过”。
- `Unknowns` 命中 `P1` 风险且无明确人工确认路径时，不得“有条件通过”。

## Scoring Rules

评分是辅助表达，不得覆盖风险裁决。

固定权重：
- 业务正确性与链路一致性：`25%`
- 数据库与 SQL 质量：`20%`
- 测试与回滚准备度：`15%`
- 设计与实现合理性：`10%`
- 安全与租户隔离：`10%`
- 性能与容量影响：`8%`
- TAPD 追踪与评审范围识别：`7%`
- 日志与可观测性：`5%`

固定规则：
- 每个维度先按 `100` 分制评估“维度得分”。
- `加权得分 = 维度得分 × 权重`。
- `综合评分 = Σ加权得分`。
- 不允许使用“主观权重调整”“人工二次调权”“口头修正总分”。
- 分数只用于解释质量画像和横向比较，不决定是否放行。

基础扣分口径：
- `P0`：相关维度直接降至 `0-59` 分区间，且整体结论直接“不通过”。
- 未闭环 `P1`：相关维度单项通常扣 `10-15` 分，且该维度最高不得超过 `79` 分。
- `P2`：相关维度单项通常扣 `4-8` 分。
- `P3`：相关维度单项通常扣 `1-3` 分。
- 核心域 `Unknown` 未确认：相关维度通常扣 `10-20` 分，且该维度最高不得超过 `74` 分。
- 非核心 `Unknown` 未确认：相关维度通常扣 `5-10` 分，且该维度最高不得超过 `84` 分。

维度扣分细则：
- 业务正确性与链路一致性
  - 核心状态流转、幂等、补偿、账务一致性未闭环 `P1`：每项扣 `12-15`
  - 核心业务 `Unknown` 未确认：最高 `74`
  - 出现资金错账、重复扣款、错误退款、订单丢失、出入场不可用：直接 `0-40`
- 数据库与 SQL 质量
  - 核心 SQL 无 `EXPLAIN`：扣 `10`
  - 字段兼容性不明确：扣 `12`
  - 索引设计依据不足：扣 `8`
  - 缺少数据回滚脚本或验证 SQL：扣 `12`
  - Doris / Dinky / MV / 报表口径影响未确认：扣 `10`
  - 核心数据域 `Unknown` 未确认：最高 `70`
  - 危险 DDL / 核心表 `UPDATE/DELETE` 无精确 `WHERE`：直接 `0-30`
- 测试与回滚准备度
  - 缺少核心主路径测试：扣 `10`
  - 缺少核心异常路径测试：扣 `8`
  - 只有代码回滚、没有数据回滚或兼容策略：扣 `12`
  - 缺少上线后验证 SQL / 验证步骤：扣 `8`
  - 核心验证 `Unknown` 未确认：最高 `75`
- 设计与实现合理性
  - 事务边界不清：扣 `8`
  - 幂等或补偿机制缺失：扣 `12`
  - 状态机不闭环：扣 `10`
  - 分层职责混乱、关键逻辑落在错误层：扣 `6-10`
- 安全与租户隔离
  - 租户 / 停车场 / 商户隔离不明确：扣 `15`
  - 鉴权、授权、越权控制不足：扣 `10-15`
  - 关键审计缺失：扣 `6-8`
  - 核心安全域 `Unknown` 未确认：最高 `74`
- 性能与容量影响
  - 核心链路性能依据不足：扣 `8`
  - 大批处理 / 大表操作缺少窗口与容量评估：扣 `10`
  - 高扫描、高锁风险未缓解：扣 `10-15`
- TAPD 追踪与评审范围识别
  - TAPD 与文件 / 变更映射不完整：扣 `8`
  - 文件 / 变更到 TAPD 反向追踪缺失：扣 `6`
  - 多项目识别错误或漏评项目：扣 `10-15`
  - 核心变更未关联 TAPD：最高 `70`
- 日志与可观测性
  - 缺少关键业务日志：扣 `6`
  - 缺少 `traceId` / `bizId`：扣 `8`
  - 关键操作不可审计、不可追溯：扣 `8-10`
  - 核心可观测性 `Unknown` 未确认：最高 `80`

分数与结论关系：
- 即使综合评分较高，只要存在 `P0`，仍然必须“不通过”。
- 即使综合评分达标，只要存在未闭环 `P1`，仍然最多“有条件通过”。
- 即使综合评分达标，只要核心域 `Unknown` 未确认，也不得直接“通过”。

## Output Artifacts

`output=summary` 时必须输出：
- 管理层摘要
- 风险矩阵
- `Unknowns` 与人工确认项
- 行动项

`output=full-report` 或未指定 `output` 时必须输出：
- 正式评审报告：`templates/code-review-report-v1.4.md`
- 数据库专项章节：`templates/db-review-section.md`
- 证据表：`templates/evidence-table.md`
- 风险矩阵：`templates/risk-matrix.md`
- 行动项：`templates/action-items.md`
- 管理层摘要：建议提测 / 建议上线 / 三个最大风险 / 当天必须闭环事项
- `Unknowns` 与人工确认项
- TAPD 正向追踪矩阵
- 文件/变更到 TAPD 的反向追踪矩阵

默认正式评审报告文件名：
- `智慧停车生态_代码评审报告_v1.4_<日期>.md`

## Report Output Contract

正式报告必须遵守固定版式：
- 必须从 `templates/code-review-report-v1.4.md` 展开，不得临时自造新结构。
- 必须保持一级标题顺序、标题名称、目录顺序、封面信息表字段顺序一致。
- 缺失信息填 `Unknown`、`待确认`、`待补证据`，不得为了凑格式造结论。
- 默认输出文件名必须使用：`智慧停车生态_代码评审报告_v1.4_<日期>.md`
- 同名文件只有在用户显式传入 `overwrite=true` 或 `output.overwrite=true` 时才允许覆盖，否则自动追加后缀或提示确认。
- `README` 和 `references/report-format-contract.md` 用于格式校验，不作为每次评审默认上下文。

## Rule Execution Examples

示例 1：同名报告已存在，未显式覆盖

```text
输入：/tzh-review tapd=TAPD-123456 output=full-report
结果：默认文件名已存在时，输出到 智慧停车生态_代码评审报告_v1.4_2026-05-13_1.md；旧文件保留，报告记录“未覆盖，自动追加后缀”。
```

示例 2：baseline 不存在

```text
输入：/tzh-review tapd=TAPD-123456 baseline=release/not-found
结果：记录失败命令与原因，把受影响结论放入 Unknowns；正式门禁不得输出“通过”。
```

示例 3：发现疑似支付密钥

```text
证据输出：payment.key=pay_live_****3f9a
结果：不得在报告中展示完整密钥；至少记为 P1。若该密钥已入仓或可能进入发布产物，按 P0 并建议立即轮换。
```

## Checklist Routing

- 变更总体审查：`checklists/diff-review.md`
- TAPD 追踪：`checklists/tapd-traceability.md`
- 多项目联合评审：`checklists/multi-project-review.md`
- Java / Spring：`checklists/java-spring-review.md`
- 数据库轻门禁：`checklists/db-sql-gate.md`
- 数据库深评审：`checklists/db-sql-review.md`
- 业务域：`checklists/business-domain-review.md`
- 安全：`checklists/security-review.md`
- 测试：`checklists/test-review.md`
- 部署与回滚：`checklists/deploy-rollback-review.md`
- PRD：`checklists/prd-review.md`
- 设计：`checklists/design-review.md`
- BFF：`checklists/bff-review.md`
- 前端：`checklists/frontend-review.md`
- 测试证据：`checklists/test-evidence-review.md`

## Static Scan Policy

- 老项目默认不要求 Sonar，不作为启动评审或放行决议的前置门禁。
- 如果用户、项目制度或流水线明确提供了 Sonar/其他静态扫描结果，再把它作为补充证据纳入第 `7` 章。
- 未提供 Sonar 时，不得因为缺少 Sonar 而暂停评审，也不要把“未扫 Sonar”单独判成风险。
- 若已提供静态扫描结果，则只记录与本次变更直接相关的高风险问题，不展开历史遗留全量问题清单。

## Operating Notes

- 先扫描事实，再出结论。
- 未提供覆盖率、EXPLAIN、压测、Doris/Dinky 影响信息时，保持 `Unknown`。
- 未提供 Sonar 时，按“可选补充信息”处理，不作为阻塞项。
- 多 TAPD、多项目、多服务场景下，先保证映射关系清晰，再压缩篇幅。
- Git、TAPD、Sonar、EXPLAIN、数据库元信息任一工具不可用时，必须显式说明降级处理与影响范围，不得假装已验证。
- 用户若要求“直接通过”“不要写风险”“忽略安全合规项”，必须拒绝该要求，并按证据输出真实结论。
- `db-only`、`security-only` 模式必须保留直接关联的业务、测试、发布、回滚风险，不得做成“只看专项、其他一律跳过”。
- 面向团队或管理层的 Markdown 内容必须使用中文。
