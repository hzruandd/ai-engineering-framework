# tzh-review 技能升级交付汇总

## 1. 本次完成的核心目标

本次已完成对停智慧代码评审能力的整体升级，目标是把原有评审能力从“偏报告生成、偏温和通过、平台分散”的状态，升级为一套可在 Claude Code 和 Codex 两端复用的正式评审 Skill。

升级后的整体定位是：

```text
薄 Command + 厚 Skill
```

即：

- Command 只负责触发和透传参数
- 核心评审逻辑全部收敛到 `tzh-review` Skill
- 通过统一模板、统一门禁、统一评分与统一输出契约，保证多次评审结果稳定

---

## 2. 已完成的能力升级

### 2.1 架构与平台兼容

已完成：

- 建立薄入口 Command：`.claude/commands/tzh-review.md`
- 建立共享核心 Skill：`.claude/skills/tzh-review/`
- 实现 Claude Code 与 Codex 双端兼容
- 支持命令触发和自然语言触发
- 避免 Command 和 Skill 双份维护核心逻辑

当前推荐触发方式：

```text
/tzh-review tapd=TAPD-123456
帮我评审当前分支代码，tapd=TAPD-123456
生成停智慧代码评审报告，tapd=TAPD-123456 baseline=release/2026.05
```

### 2.2 TAPD 门禁

已完成：

- TAPD 必填
- 缺少 TAPD 时必须主动询问并暂停评审
- 禁止从分支名、commit message 猜 TAPD 后继续
- 支持多 TAPD
- 支持 TAPD 正向追踪矩阵
- 支持 文件/变更 -> TAPD 反向追踪矩阵
- 未映射变更统一进入 `Unknown`

### 2.3 baseline 规则

已完成：

- 默认 baseline 固定为 `master`
- 用户不主动指定时，不询问、不变更
- 仅当用户显式指定 `baseline/base/target/release/tag/commit` 时允许覆盖
- 多项目模式下允许按项目分别记录 baseline

### 2.4 多项目联合评审

已完成：

- 自动识别单项目 / 多项目模式
- 支持多个 Git 仓库、多模块、多服务目录、多部署单元识别
- 支持每个项目分别做 diff、SQL、测试、回滚检查
- 支持输出总报告并保留各项目独立结论
- 任一核心项目 `P0` 时整体不通过
- 任一核心项目未闭环 `P1` 时整体最多有条件通过

### 2.5 数据库与 SQL 专项

已完成：

- 新增数据库专项门禁
- 新增数据库轻门禁清单：`db-sql-gate.md`
- 新增数据库深评审清单：`db-sql-review.md`
- 覆盖 SQL、字段、索引、DDL、DML、修复脚本、Doris、Dinky、MV、报表口径
- 覆盖前滚脚本、回滚脚本、验证 SQL、EXPLAIN、金额字段、状态字段、租户/停车场/商户隔离字段

### 2.6 停智慧业务专项

已完成：

- 新增核心业务链路专项清单：`business-domain-review.md`
- 强化支付、订单、开闸、计费、清分、对账、发票、权限、租户隔离审查
- 强制关注幂等、状态机、补偿、账务一致性、出入场可用性

### 2.7 证据体系与 Unknown 机制

已完成：

- 建立统一证据编号规则：`SRC / SQL / DDL / IDX / EXP / CFG / MQ / JOB / TEST / SONAR / LOG`
- 建立统一判断类型：`Observed / Inferred / Unknown`
- 要求关键结论必须带证据编号
- 要求 Unknown 进入“Unknowns 与人工确认项”
- 核心域 Unknown 至少按 `P1` 处理，严重时直接 `P0`

### 2.8 风险分级与放行规则

已完成：

- 固定 `P0 / P1 / P2 / P3` 风险分级
- 明确禁止预设“通过”
- 明确禁止为了报告好看降低风险等级
- 明确 `P0` 一律不通过
- 明确未闭环 `P1` 不得直接通过
- 明确缺少 TAPD 不允许开始评审

### 2.9 评分体系

已完成：

- 建立显式权重评分
- 建立固定评分公式：`综合评分 = Σ(维度得分 × 权重)`
- 建立固定扣分口径
- 建立各维度评分上限与封顶规则
- 明确分数不能覆盖风险裁决

固定权重如下：

- 业务正确性与链路一致性：`25%`
- 数据库与 SQL 质量：`20%`
- 测试与回滚准备度：`15%`
- 设计与实现合理性：`10%`
- 安全与租户隔离：`10%`
- 性能与容量影响：`8%`
- TAPD 追踪与评审范围识别：`7%`
- 日志与可观测性：`5%`

### 2.10 老项目适配与 token 控制

已完成：

- Sonar 对老项目降为可选补充信息
- 未提供 Sonar 不阻塞评审
- 静态扫描结果只记录与本次变更直接相关的问题
- Skill 采用按需加载策略，避免每次全量加载全部 checklist
- 报告模板与数据库专项做了平衡压缩，降低 token 消耗

### 2.11 报告格式与命名规则

已完成：

- 固定正式报告模板：`code-review-report-v1.4.md`
- 固定主标题、封面表、目录、16 个一级章节、4 个附录
- 新增 `report-format-contract.md` 锁定版式
- 固定默认输出文件名：

```text
智慧停车生态_代码评审报告_v1.4_<日期>.md
```

- 禁止默认追加 `TAPD`、`by_codex`、`by_cc`、分支名、评审人等随机后缀

---

## 3. 已生成的主要文件

### 3.1 Command

- `.claude/commands/tzh-review.md`

作用：

- Claude Code 薄入口
- 只触发 Skill，不承载核心评审逻辑

### 3.2 Skill 主体

- `.claude/skills/tzh-review/SKILL.md`
- `.claude/skills/tzh-review/README.md`

作用：

- 承载 TAPD、baseline、多项目、数据库专项、评分、输出契约、命名规则等核心能力

### 3.3 模板

- `templates/code-review-report-v1.4.md`
- `templates/db-review-section.md`
- `templates/evidence-table.md`
- `templates/risk-matrix.md`
- `templates/action-items.md`

作用：

- 固定报告结构和正式输出样式

### 3.4 检查清单

- `checklists/diff-review.md`
- `checklists/tapd-traceability.md`
- `checklists/multi-project-review.md`
- `checklists/java-spring-review.md`
- `checklists/db-sql-gate.md`
- `checklists/db-sql-review.md`
- `checklists/business-domain-review.md`
- `checklists/security-review.md`
- `checklists/test-review.md`
- `checklists/deploy-rollback-review.md`

作用：

- 支撑执行型评审，而不是只生成报告

### 3.5 示例与契约

- `examples/sample-command-usage.md`
- `examples/sample-natural-language-usage.md`
- `examples/sample-report-outline.md`
- `references/report-format-contract.md`

作用：

- 统一团队使用方式
- 锁定格式与命名规则

### 3.6 汇总文档

- [tzh-review_评审技能升级总结报告_2026-05-09.md](C:/workspace/4codex/tzh-review-codex-prompt-pack/tzh-review_评审技能升级总结报告_2026-05-09.md)

作用：

- 记录本次升级背景、问题诊断、升级方案、成品对比与使用方式

---

## 4. 已完成的全局安装

已同步到以下全局目录：

- Claude 全局 Skill：
  `C:\Users\Administrator\.claude\skills\tzh-review`
- Claude 全局 Command：
  `C:\Users\Administrator\.claude\commands\tzh-review.md`
- Codex 全局 Skill：
  `C:\Users\Administrator\.codex\skills\tzh-review`

说明：

- 当前仓库版和全局版已同步
- 两端全局 Skill 都已包含最新的评分规则、命名规则、格式契约和数据库专项能力

---

## 5. 已完成的报告样例对比结论

本次已对以下成品报告做过对比分析：

- Codex 新版报告
- Claude Code 新版报告
- 旧版报告

当前已确认的结论：

1. 旧版报告存在明显“倾向通过”的问题。  
   会把应上提的异常流、补偿缺失、测试证据不足问题压成 `P2/P3`，并直接给出“通过”。

2. 新版报告已经具备跨平台一致的制度强度。  
   无论由 Codex 还是 Claude Code 生成，只要存在未闭环 `P1`，都不会默认给“通过”。

3. Codex 与 Claude Code 两端的新报告，风险聚焦点仍略有差异。  
   Codex 更关注异常流原子性、补偿缺失、TAPD 范围与回归证据；Claude Code 更关注空指针安全、验证 SQL、EXPLAIN、索引命中、traceId 和存量链路证据。

4. 新版评分体系已经开始服务于裁决规则。  
   分数不再覆盖 `P1/P0/Unknown` 门禁，而是作为辅助解释。

---

## 6. 当前默认行为

当前 `tzh-review` 的默认行为已经固定为：

- 缺 TAPD：先问 TAPD，暂停评审
- baseline 未指定：默认 `master`
- 命中多项目条件：自动进入多项目模式
- 命中数据库条件：先走 `db-sql-gate`，再决定是否展开 `db-sql-review`
- 缺 Sonar：不阻塞评审，按可选补充信息处理
- 缺 EXPLAIN、验证 SQL、回滚证据：保留 `Unknown` 或上提风险
- 存在未闭环 `P1`：最多有条件通过
- 存在 `P0`：直接不通过
- 正式报告默认文件名：`智慧停车生态_代码评审报告_v1.4_<日期>.md`

---

## 7. 仍可继续优化的方向

本次核心升级已经完成，但如果继续往前收敛，一般还可以做三类增强：

1. 增加“典型问题映射样例”。  
   进一步统一 Codex 与 Claude Code 对同类问题的风险聚焦点。

2. 增加“高风险链路优先级排序规则”。  
   让支付、订单、开闸、清分、对账、发票、租户隔离等问题，在不同执行端都更稳定地优先上提。

3. 继续优化正式报告篇幅。  
   在不降低制度强度的前提下，进一步压缩语言长度、优化章节密度和阅读效率。

---

## 8. 本次交付结论

到当前为止，`tzh-review` 已经从一个偏“报告生成”的评审能力，升级为一套：

- 可跨 Claude Code / Codex 复用
- 有 TAPD 强门禁
- 有多项目识别
- 有数据库专项
- 有正式模板
- 有证据体系
- 有固定评分与扣分口径
- 有统一命名规则
- 有全局安装落点

的正式代码评审 Skill。

从交付状态看，这次升级已完成主要建设目标，可以进入团队试运行与样例校准阶段。
