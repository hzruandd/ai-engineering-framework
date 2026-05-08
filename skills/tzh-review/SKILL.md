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
  - 订单、支付、计费、月租、券包、发票、清分、对账、权限、开闸链路评审
scenarios:
  - "/tzh-review tapd=TAPD-123456"
  - "/tzh-review tapd=TAPD-123456,TAPD-123457 baseline=release/2026.05"
  - "帮我评审当前分支代码，tapd=TAPD-123456"
  - "生成停智慧代码评审报告，tapd=TAPD-123456"
  - "检查这次 SQL 和数据库字段变更风险，tapd=TAPD-123456"
  - "做一次上线前评审，tapd=TAPD-123456,TAPD-123457"
---

# tzh-review

## Purpose

`tzh-review` 是停智慧代码变更质量门禁 Skill，不只是报告生成器。它负责把 Git diff、TAPD、项目边界、数据库与 SQL 变更、业务链路、测试与回滚信息串成一套可追溯、可审计、可裁决的正式评审流程。

核心目标：
- 不放过无法追溯到 TAPD 的变更。
- 不把多项目联合改动误判成单项目评审。
- 不把数据库、SQL、索引、DDL、DML、报表口径等高风险改动降级处理。
- 不预设“通过”，而是根据证据与风险作出结论。

## Platform Compatibility

本 Skill 的核心规则保持平台中性，可同时服务于 Claude Code 与 Codex：
- 在支持自定义命令的平台中，可以通过薄 Command 触发，但 Command 只做入口。
- 在不支持自定义命令的平台中，直接通过自然语言触发。
- 核心门禁、评审流程、检查清单、模板、风险分级、数据库专项、TAPD 追踪逻辑全部只保留在本 Skill 中。

## Fast Trigger

遇到以下表达时，直接进入本 Skill：
- 帮我评审当前分支代码
- 生成代码评审报告
- 提测前评审
- 上线前评审
- SQL 评审
- 数据库变更评审
- 索引评审
- tzh-review

如果缺少 TAPD，先询问 TAPD，并暂停，不做任何后续评审动作。

## Invocation

以下触发都应进入本 Skill：

1. 支持命令的平台，可用命令触发
- `/tzh-review`
- `/tzh-review tapd=TAPD-123456`
- `/tzh-review tapd=TAPD-123456 baseline=release/2026.05`
- `/tzh-review tapd=TAPD-123456,TAPD-123457`

2. 所有平台均可用自然语言触发
- 帮我评审当前分支代码
- 生成停智慧代码评审报告
- 做一次提测前评审
- 做一次上线前代码评审
- 检查这次 SQL 和数据库字段变更风险
- 检查索引变更风险
- 做一次当前分支评审
- tzh-review

## Input Contract

推荐输入字段：
- `tapd`：必填，支持多个
- `baseline`：可选，默认 `master`
- `projects` 或 `services`：可选，用于显式指定项目或服务
- `scope`：可选，例如 SQL、数据库、提测前、上线前

可接受表达：
- `TAPD-123456`
- `tapd=TAPD-123456`
- `tapd=TAPD-123456,TAPD-123457`
- `baseline=release/2026.05`
- `只看 SQL 风险`
- `评审 order-service 和 billing-service`

推荐自然语言写法：
- `帮我评审当前分支代码，tapd=TAPD-123456`
- `生成停智慧代码评审报告，tapd=TAPD-123456 baseline=master`
- `检查这次 SQL 和字段变更风险，tapd=TAPD-123456`

## Optional Command Responsibility

如果当前平台支持 `/tzh-review` 这类自定义命令，则 Command 只负责入口和参数透传，不保留核心逻辑。

必须遵守：
- 评审流程、检查清单、风险分级、数据库专项、TAPD 追踪、多项目识别、报告模板均以本 Skill 为准。
- 如果 Command 内容与 Skill 内容冲突，以本 Skill 为准。
- 不要把详细规则回填到 Command 中。

## TAPD Gate

TAPD 是强门禁，缺失时不得继续评审。

硬规则：
- TAPD 编号必填。
- 如果用户没有明确提供一个或多个 TAPD 编号，先主动询问 TAPD 编号，并暂停评审。
- 缺少 TAPD 时，不允许继续扫描、打分、出结论或生成正式评审报告。
- 不允许仅依据分支名、commit message、目录名自动猜测 TAPD 并继续执行。
- 支持多个 TAPD 同次评审。
- 每个 TAPD 必须对应明确的变更内容摘要。
- 必须同时建立两类映射：
  - `TAPD -> 项目/服务/文件/变更`
  - `文件/变更 -> TAPD` 反向追踪
- 任何无法关联到 TAPD 的代码、SQL、DDL、配置、脚本、测试改动都必须标记为 `Unknown`。
- Unknown 变更若落在核心业务、数据库、SQL、支付、订单、发票、清分、对账、权限、开闸、租户隔离领域，风险等级至少为 `P1`；若已影响核心数据正确性、资金、出入场或核心表安全，直接提升为 `P0`。

执行动作：
1. 从用户输入解析 TAPD 编号列表。
2. 要求每个 TAPD 补充一句“本次变更目标/范围”。
3. 生成 TAPD 追踪矩阵。
4. 生成代码变更到 TAPD 的反向追踪矩阵。
5. 对无法关联项保留 Unknown，并进入人工确认项。

建议提问模板：

```text
开始评审前需要 TAPD 编号。请提供一个或多个 TAPD 编号，并分别说明每个 TAPD 对应的本次变更目标。
示例：TAPD-123456：停车订单补单；TAPD-123457：月租续费索引优化
```

## Baseline Rule

baseline 默认值和覆盖规则必须严格执行。

规则：
- 默认 baseline 是 `master`。
- 用户不主动指定 baseline 时，不询问、不变更。
- 只有用户明确指定 `baseline`、`base`、`target`、目标分支、release 分支、tag、commit 时，才允许覆盖。
- 多项目模式下，每个项目允许有不同 baseline，但都必须记录来源。
- 最终报告必须记录每个项目实际使用的 baseline，以及是否为默认基线。

解析优先级：
1. 用户显式提供的项目级 baseline。
2. 用户显式提供的全局 baseline。
3. 默认 `master`。

## Multi-project Detection

满足以下任一条件时，自动进入多项目模式：
- 检测到多个 Git 仓库。
- 检测到多个应用模块。
- diff 触达多个服务目录。
- 检测到多个 Spring Boot 启动类。
- 检测到多个 `spring.application.name`。
- 检测到多个 Dockerfile、Jenkinsfile 或 k8s 部署单元。
- 用户输入多个项目名、服务名或仓库路径。

多项目模式规则：
1. 每个项目分别执行 diff 分析。
2. 每个项目分别形成变更清单。
3. 每个项目分别做代码质量、SQL、配置、测试、回滚检查。
4. 最后统一做跨项目链路分析。
5. 输出一份总报告。
6. 总报告中保留每个项目的独立结论。
7. 任一核心项目存在 `P0`，整体结论一律为“不通过”。
8. 任一核心项目存在未闭环 `P1`，整体结论最多为“有条件通过”。

## Execution Workflow

按以下顺序执行，不要跳步：

1. 识别触发方式。
2. 校验 TAPD。
3. 解析 baseline。
4. 自动识别单项目或多项目模式。
5. 扫描变更范围。
6. 建立变更地图。
7. 建立 TAPD 追踪矩阵。
8. 执行核心代码评审。
9. 执行数据库与 SQL 专项评审。
10. 执行测试、性能、安全、部署回滚评审。
11. 输出风险分级。
12. 输出放行结论。
13. 生成正式评审报告。

## Change Scanning

先用 Git 信息建立变更地图，再进入判断：

必查命令：
- `git status`
- `git branch --show-current`
- `git log baseline..HEAD`
- `git diff --stat baseline...HEAD`
- `git diff --name-status baseline...HEAD`
- `git diff baseline...HEAD`

多项目模式下，对每个项目分别执行同类命令，并记录项目根路径。

变更分类至少覆盖：
- API、Controller、Dubbo、Feign 或外部接口适配层
- Service、Manager、Handler、Strategy
- Mapper、Repository、XML SQL、Wrapper
- Entity、DTO、VO、BO、Enum
- `application.yml`、`bootstrap.yml`、Nacos key、灰度开关
- XXL-Job、定时任务、批处理
- MQ Producer、Consumer、Topic、重试与补偿
- DDL、DML、迁移脚本、数据修复脚本
- 前端页面、路由、API 调用
- 测试文件、测试数据、压测脚本

建立变更地图时，至少输出：
- 变更文件清单
- 变更类型清单
- 涉及项目/服务列表
- 涉及业务域列表
- 涉及数据库对象、SQL、索引、脚本列表
- 涉及发布单元、配置项、外部依赖列表

## Evidence Rules

所有结论必须带证据。没有证据时，不得伪装成确定结论。

证据编号类型：
- `SRC`：源码
- `SQL`：SQL、Mapper、XML SQL
- `DDL`：数据库脚本
- `IDX`：索引定义
- `EXP`：EXPLAIN 结果
- `CFG`：配置
- `MQ`：消息
- `JOB`：定时任务
- `TEST`：测试
- `SONAR`：Sonar 问题
- `LOG`：日志

判断类型：
- `Observed`：源码、配置、SQL、测试、日志可以直接证明
- `Inferred`：从多处证据推断，但没有直接证明
- `Unknown`：当前仓库或当前输入无法确认

编号建议：
- 采用 `类型-序号`，如 `SRC-01`、`SQL-03`、`DDL-02`
- 同一项目可追加前缀，如 `order-SQL-01`

输出要求：
- 风险项必须绑定证据编号。
- 结论必须标明判断类型。
- Unknown 必须进“Unknowns 与人工确认项”章节。

## Database Review Gate

只要命中以下任意条件，就必须执行数据库与 SQL 专项评审：
- 涉及 SQL
- 涉及字段新增、删除、改名、类型变更、长度变更、精度变更
- 涉及索引新增、删除、调整
- 涉及 DDL
- 涉及 DML
- 涉及数据修复脚本
- 涉及 Doris
- 涉及 Dinky
- 涉及 MV
- 涉及报表口径
- 涉及订单、支付、计费、月租、券包、发票、清分、对账、开闸等核心数据读写

数据库专项至少覆盖：
- SQL 查询质量
- UPDATE、DELETE 精确 WHERE 风险
- 字段兼容性
- 索引设计合理性
- 大表 DDL 风险
- 修复脚本幂等性与可回滚性
- EXPLAIN、扫描行数、命中索引情况
- Doris、Dinky、MV、报表同步影响
- 前滚脚本、回滚脚本、验证 SQL

详单以 `checklists/db-sql-review.md` 为准，正式报告章节以 `templates/db-review-section.md` 为准。

## Business Domain Review Gate

涉及以下领域时，必须执行核心业务链路专项评审：
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
- 上下游依赖与回放能力

## Risk Levels

风险分级必须据实判断，禁止为了报告好看降级。

### P0

出现以下情况之一，直接判定 `P0`：
- 资金错账
- 重复扣款
- 错误退款
- 订单丢失
- 支付状态不一致
- 大量用户无法进出场
- 核心表 `UPDATE/DELETE` 缺少精确 `WHERE`
- 支付回调、券核销、开票缺少幂等
- 大表 DDL 无评估、无回滚、无验证 SQL
- 缺少停车场、商户、租户隔离
- 清分、对账、发票口径变更无验证

### P1

出现以下情况之一，至少判定 `P1`：
- 核心 SQL 未提供 EXPLAIN
- 字段兼容性不明确
- 索引设计依据不足
- 数据修复脚本不可重复执行
- 缺少关键链路日志或 traceId
- Doris、Dinky、报表同步影响未确认
- 测试未覆盖核心异常路径
- 回滚方案只有代码回滚，没有数据回滚或兼容策略
- 关键领域 Unknown 尚未人工确认

### P2

通常用于：
- 非核心链路的可维护性风险
- 中等影响的性能或观测性不足
- 设计边界、异常处理、日志、命名、重复代码问题

### P3

通常用于：
- 轻微优化项
- 注释、风格、局部重构建议
- 对当前放行结论无实质影响的改进项

## Decision Rules

结论只有三类：
- 通过
- 有条件通过
- 不通过

裁决规则：
- 禁止预设“通过”。
- 禁止为了报告好看降低风险等级。
- `P0` 一律“不通过”。
- 未闭环 `P1` 不得直接“通过”。
- 缺少 TAPD 不允许开始评审。
- Unknown 如果落在核心域且未人工确认，不得给“通过”。

判定建议：
- 仅当风险闭环、证据充分、Unknown 已清理或已被明确接受时，才可判定“通过”。
- 存在未闭环 P1、核心 Unknown、待补充 EXPLAIN、待补数据回滚方案时，最多“有条件通过”。
- 存在 P0、核心链路不可验证、数据库高风险无回滚时，“不通过”。

## Output Artifacts

评审输出必须包含：
- 正式评审报告：`templates/code-review-report-v1.4.md`
- 数据库专项章节：`templates/db-review-section.md`
- 证据表：`templates/evidence-table.md`
- 风险矩阵：`templates/risk-matrix.md`
- 行动项：`templates/action-items.md`
- Unknowns 与人工确认项
- TAPD 正向追踪矩阵
- 文件/变更到 TAPD 的反向追踪矩阵

## Checklist Routing

执行时按需加载以下清单：
- 变更总体审查：`checklists/diff-review.md`
- TAPD 追踪：`checklists/tapd-traceability.md`
- 多项目联合评审：`checklists/multi-project-review.md`
- Java / Spring：`checklists/java-spring-review.md`
- 数据库与 SQL：`checklists/db-sql-review.md`
- 业务域：`checklists/business-domain-review.md`
- 安全：`checklists/security-review.md`
- 测试：`checklists/test-review.md`
- 部署与回滚：`checklists/deploy-rollback-review.md`

## Operating Notes

- 先基于事实扫描，再出结论，不要先写结论再找证据。
- 用户没有给 Sonar、覆盖率、EXPLAIN、压测、Doris/Dinky 影响信息时，保持 `Unknown`，不要代填“达标”。
- 多 TAPD、多项目、多服务联合评审时，优先保证映射关系清晰，其次再压缩报告篇幅。
- 正式输出给团队或管理层的 Markdown 内容必须使用中文。
