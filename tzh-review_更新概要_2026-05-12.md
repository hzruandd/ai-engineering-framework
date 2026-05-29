# tzh-review 更新概要

## 更新背景

本次更新是在 `formal-review` 升级为 `tzh-review` 技能后的继续优化，重点根据评审意见补强安全与合规审查能力，并提升技能在正式门禁、预评审、模板一致性方面的可执行性。

## 本次更新重点

### 1. 补强安全与合规审查

- 在 `skills/tzh-review/checklists/security-review.md` 中新增了脱敏规则、加密与密钥管理、签名与防重放、导出与下载权限、日志脱敏、对象存储访问控制、合规留痕等检查项。
- 在 `skills/tzh-review/SKILL.md` 中新增“安全与合规专项门禁”，明确以下场景必须进入安全专项：
  - 权限、角色、租户、停车场、商户隔离相关改动
  - 手机号、车牌号、身份证、支付流水号等敏感数据处理
  - 导出、报表、下载、Webhook、第三方回调
  - 密钥、token、支付证书、OSS 凭证、Nacos 密文配置
  - 支付、核销、开票、开闸等防重、防刷、防重放链路
- 风险分级同步增强，新增了密钥明文入库、接口可重放、大批量敏感数据泄露等 `P0`/`P1` 判定口径。

### 2. 增加执行模式，降低使用僵硬度

- 为 `tzh-review` 增加了以下模式：
  - `formal-gate`
  - `precheck`
  - `db-only`
  - `security-only`
  - `release-gate`
- 其中 `precheck` 允许在缺少 TAPD 时先做风险预扫，但只能输出风险与待补证据项，不能直接给出“通过 / 有条件通过 / 不通过”结论。
- `commands/tzh-review.md`、`README.md`、示例文档都已同步支持 `mode` 和 `output` 参数说明。

### 3. 补上未提交改动扫描规则

- 变更扫描不再只依赖 `baseline...HEAD`。
- 新增要求显式检查：
  - `git diff --cached`
  - `git diff`
  - `git ls-files --others --exclude-standard`
- 报告中新增 `committed diff`、`staged diff`、`working tree diff`、`untracked files` 分类，避免上线评审遗漏未提交内容。
- 在 `release-gate` 模式下，如果未提交改动也属于提测或上线范围，至少标记为 `P1`，直到边界明确。

### 4. 报告模板与行动项模板对齐

- 在正式报告模板 `skills/tzh-review/templates/code-review-report-v1.4.md` 中新增：
  - 执行模式字段
  - 管理层摘要
  - 变更范围分类
  - 更完整的安全审查表
  - `Precheck` 结论限制说明
- 在 `templates/action-items.md` 中补充：
  - 是否阻塞放行
  - 放行前/放行后
  - 验证方式
  - 复验人
- 在 `templates/db-review-section.md` 中补齐判断类型、Doris/Dinky/MV/报表影响等字段，使其与正式报告第 9 章更一致。

### 5. 完善专项清单

- `java-spring-review.md` 增强了 Dubbo、Nacos、Redis/Tair、MQ/任务链路的审查关注点。
- `test-review.md` 增加了停智慧核心业务测试矩阵，补上权限隔离、安全回归、防重放等测试要求。
- `multi-project-review.md` 增加了项目识别优先级和排除规则，减少多项目误判。

### 6. 修正示例与格式约束中的编号问题

- 修复了 `skills/tzh-review/examples/sample-report-outline.md` 中目录编号断裂问题。
- 同步调整了：
  - `skills/tzh-review/templates/code-review-report-v1.4.md`
  - `skills/tzh-review/references/report-format-contract.md`
- 当前子章节编号已统一为：
  - `1.1 评审范围表`
  - `1.2 AI 主持评审与制度门禁`
  - `1.3 管理层摘要`
  - `4.1 变更范围分类`
  - `4.2 变更摘要`

## 涉及文件范围

本次更新主要覆盖以下文件：

- `commands/tzh-review.md`
- `skills/tzh-review/SKILL.md`
- `skills/tzh-review/README.md`
- `skills/tzh-review/checklists/security-review.md`
- `skills/tzh-review/checklists/test-review.md`
- `skills/tzh-review/checklists/java-spring-review.md`
- `skills/tzh-review/checklists/multi-project-review.md`
- `skills/tzh-review/templates/code-review-report-v1.4.md`
- `skills/tzh-review/templates/db-review-section.md`
- `skills/tzh-review/templates/action-items.md`
- `skills/tzh-review/examples/sample-command-usage.md`
- `skills/tzh-review/examples/sample-natural-language-usage.md`
- `skills/tzh-review/examples/sample-report-outline.md`
- `skills/tzh-review/references/report-format-contract.md`

## 当前效果

经过本次更新，`tzh-review` 相比上一版有以下直接提升：

- 安全与合规不再只是简短检查项，而是进入正式门禁和正式报告模板。
- 支持“正式门禁”和“预评审”两种使用方式，兼顾制度强度与日常使用灵活性。
- 未提交改动被纳入评审边界，降低了正式评审遗漏风险。
- 模板、示例、格式约束三者的一致性更高，减少输出漂移。

## 后续可继续优化的方向

- 增加自动取证脚本，例如变更采集、敏感信息扫描、密钥扫描。
- 继续增强 PolarDB、Doris、Dinky 专项规则。
- 为正式报告增加更稳定的“管理层一页摘要”输出样式。
- 补充安装、升级、卸载说明，完善技能分发与落地方式。
