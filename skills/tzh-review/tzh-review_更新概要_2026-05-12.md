# tzh-review 更新概要

## 2026-05-13 变更记录

### 本次更新时间

- 2026-05-13

### 修改涉及的文件

- `skills/tzh-review/SKILL.md`
- `skills/tzh-review/README.md`
- `skills/tzh-review/checklists/security-review.md`
- `skills/tzh-review/templates/code-review-report-v1.4.md`
- `skills/tzh-review/templates/evidence-table.md`
- `skills/tzh-review/references/report-format-contract.md`
- `skills/tzh-review/examples/sample-command-usage.md`
- `skills/tzh-review/examples/sample-report-outline.md`
- `commands/tzh-review.md`
- `skills/tzh-review/tzh-review_更新概要_2026-05-12.md`

### Command 候选文件与判断依据

- 发现的候选文件：
  - `commands/tzh-review.md`
- 未发现的候选路径：
  - `.claude/commands/tzh-review.md`
  - `.claude/commands/tzh-review/*.md`
- 实际修改的 Command 文件：
  - `commands/tzh-review.md`
- 选择原因：
  - 当前仓库内仅发现一个 `tzh-review` Command 候选文件。
  - 该文件路径符合当前仓库“`commands/` 目录承接命令入口、`skills/tzh-review/` 承接核心逻辑”的结构。
  - 仓库内不存在 `.claude/commands` 下的同名配置，因此没有更高优先级的本地候选项。
- 遗留风险：
  - 当前判断基于仓库文件结构成立。
  - 若外部 Claude Code 运行环境额外注入了仓库外 Command 映射，仍需人工确认是否存在仓库外覆盖入口。

### 核心修改点

1. 修复 `precheck` 与 TAPD 门禁冲突
- 明确 `formal-gate`、`release-gate`、`db-only`、`security-only` 下 TAPD 必填。
- 明确缺少 TAPD 或缺少 TAPD 对应变更目标时，不得启动正式评审，不得输出正式放行结论。
- 明确 `precheck` 允许缺少 TAPD，但只能输出风险预扫结果、`Unknowns`、待补证据项、人工确认项。
- 明确如果 TAPD 目标来自推断，必须标记为 `Inferred`。

2. 新增并强化大 diff 处理规则
- 在 `SKILL.md` 中新增 `Large Diff Handling` 章节。
- 明确进入大 diff 模式的触发条件、扫描顺序、风险优先级展开顺序和未展开文件的 `Unknowns` 处理。
- 明确不得因 token 限制直接给“通过”。
- 在报告模板中新增 `4.3 大 Diff 扫描说明`，要求记录扫描范围、已展开文件、未展开文件及原因。

3. 修正 `db-only` / `security-only` 专项模式的风险收敛问题
- 明确专项模式只限定评审重点，不允许屏蔽由专项变更直接引发的业务、测试、发布、回滚、合规和可用性风险。
- 明确专项模式发现非专项高风险时，必须正常记录。
- 明确专项模式结论需说明“仅针对专项重点范围，但已记录关联风险”。

4. 收紧报告输出与覆盖保护
- 取消“同名文件默认覆盖”规则。
- 明确只有 `overwrite=true` 或 `output.overwrite=true` 才允许覆盖。
- 未显式授权覆盖时，默认自动追加 `_1`、`_2`、`_3` 等后缀，或在交互式场景中提示确认。
- 明确 `output=summary` 只输出摘要、风险矩阵、Unknowns、行动项，不生成完整报告文件。
- 在报告模板中新增 `1.4 输出与覆盖记录`，要求记录输出路径、是否覆盖、是否自动追加后缀。

5. 新增工具失败降级规则
- 在 `SKILL.md` 中新增 `Tool Failure And Degradation` 章节。
- 覆盖 Git 仓库不存在、baseline 不存在、diff 过大、文件读取失败、TAPD 不可访问、测试失败、数据库连接不可用、多项目局部不可读等场景。
- 明确必须记录失败项、失败命令、失败原因、影响范围，不得伪装成已验证。
- 明确关键工具失败或关键证据缺失时，正式门禁不得输出“通过”。
- 在报告模板中新增 `1.5 工具执行失败与降级说明` 子节。

6. 强化敏感信息脱敏输出规则
- 在 `SKILL.md` 中新增 `Sensitive Evidence Redaction` 章节。
- 明确密码、token、`appSecret`、`accessKey`、`secretKey`、证书、私钥、数据库连接串、OSS 凭证、支付密钥、手机号、身份证号、车牌号、支付流水号、用户隐私字段不得完整原样输出。
- 明确证据表和评审输出中只允许展示路径、行号、字段名、掩码值和风险说明。
- 明确高敏凭证疑似泄露至少 `P1`，若已入仓、入日志、入前端包或入发布产物，应按 `P0` 评估并建议立即轮换。

7. 补充简短示例
- 在 `SKILL.md` 中新增三个简短规则执行示例：
  - 同名报告已存在时自动追加 `_1`
  - baseline 不存在时进入 `Unknowns` 且不得给“通过”
  - 发现疑似支付密钥时仅输出掩码值并给出轮换建议

### 为什么修改

- 现有 `precheck` 与 TAPD 门禁存在可执行冲突，真实场景中容易出现“允许预扫”和“禁止开始评审”同时存在的歧义。
- 现有规则对大 diff、工具失败、报告覆盖、敏感证据输出的约束不够强，真实评审时容易出现误放行、漏评、静默覆盖和敏感值外泄。
- 现有专项模式描述偏“聚焦范围”，但没有充分约束“不得忽略关联高风险”，存在误收敛风险。
- Command 入口需要继续保持薄入口，避免核心逻辑从 Skill 漂移到 Command。

### 对 Command 的影响

- `commands/tzh-review.md` 继续保持薄入口。
- Command 明确只接收并透传：
  - `tapd`
  - `baseline`
  - `mode`
  - `projects`
  - `services`
  - `scope`
  - `output`
  - `overwrite`
- Command 明确：
  - 不自行生成评审结论
  - 不自行生成风险等级
  - 不自行生成报告结构
  - 不处理同名报告覆盖逻辑
  - 必须调用并遵循 `skills/tzh-review` 的流程与模板

### 对 Skill 的影响

- `SKILL.md` 成为本次修正规则的唯一权威入口。
- 大 diff、工具失败降级、敏感信息脱敏、报告覆盖保护、`precheck/TAPD` 门禁边界等核心逻辑全部继续沉淀在 Skill。
- 报告模板、格式约束、证据模板和安全清单已同步到新的 Skill 规则。

### 新增参数说明

- `projects`
  - 替代旧的 `project/services` 混合表达，用于明确项目列表。
- `services`
  - 独立表达服务列表，避免与 `projects` 混用。
- `overwrite`
  - 显式允许覆盖同名报告文件。
- `output.overwrite=true`
  - 作为覆盖意图的透传表达，仍由 Skill 处理，不由 Command 执行覆盖逻辑。

### 兼容性说明

- 本次没有新增 TAPD 编号格式兼容规则。
- 本次没有处理 `TAPD1003440`、纯数字 TAPD、多个 TAPD 链接等兼容逻辑。
- 保留了原有正式报告模板、评分体系、专项检查清单和固定章节结构，只做增量修正。
- Command 仍保持薄入口。
- 核心逻辑仍保留在 Skill。

### 后续建议验证场景

1. 无 TAPD 的 `precheck` 预扫
- 预期：允许执行，但只能输出风险预扫结果、`Unknowns`、待补证据项、人工确认项，不得给正式结论。

2. 有 TAPD 的 `formal-gate` 正式评审
- 预期：若缺少 TAPD 目标，继续追问；补齐后按正式门禁输出完整报告。

3. baseline 不存在
- 预期：记录失败命令与原因，进入 `Unknowns`，不得输出“通过”。

4. 多服务大 diff
- 预期：进入大 diff 模式，先输出变更地图，再按风险优先级展开，未展开文件必须进入 `Unknowns`。

5. 同名报告文件已存在
- 预期：未显式允许覆盖时，不覆盖旧文件，自动追加后缀并记录输出策略。

6. 发现疑似敏感配置或密钥
- 预期：证据与报告中只输出掩码值，不输出完整敏感值；按规则评估 `P1` 或 `P0`，并给出轮换与排查建议。

---

## 2026-05-13 第二次更新记录

### 本次更新时间

- 2026-05-13

### 修改涉及的文件

- `skills/tzh-review/SKILL.md`
- `skills/tzh-review/README.md`
- `skills/tzh-review/templates/code-review-report-v1.4.md`
- `skills/tzh-review/references/report-format-contract.md`
- `skills/tzh-review/examples/sample-command-usage.md`
- `skills/tzh-review/examples/sample-natural-language-usage.md`
- `skills/tzh-review/examples/sample-report-outline.md`
- `commands/tzh-review.md`
- `skills/tzh-review/tzh-review_更新概要_2026-05-12.md`

### 核心修改点

1. 移除 `precheck`
- 从 Skill 输入契约、执行模式、TAPD 门禁、风险裁决规则中移除 `precheck`。
- 从 Command 入口说明中移除“允许无 TAPD 预扫”的分支。
- 从报告模板、格式约束、命令示例、自然语言示例和结构示例中移除 `precheck` 相关表述。

2. 收紧正式评审定位
- `tzh-review` 明确为正式评审 Skill，不再承担预评审模式。
- 所有模式下 `tapd` 必填，且必须说明每个 TAPD 的本次变更目标。
- `mode` 保留为正式评审范围控制，支持 `formal-gate`、`db-only`、`security-only`、`release-gate`。

### 为什么修改

- 当前用户确认这个 Skill 只用于正式评审，不需要再兼容预扫路径。
- 保留 `precheck` 会继续制造“正式门禁 Skill 却允许无 TAPD 预扫”的边界噪音，不利于真实使用时的门禁一致性。

### 对 Command 的影响

- `commands/tzh-review.md` 仍保持薄入口。
- Command 不再描述 `precheck` 例外路径。
- Command 继续只做参数透传和 Skill 触发，不包含核心评审逻辑。

### 对 Skill 的影响

- Skill 语义更单一，统一为正式评审门禁。
- TAPD 门禁从“部分模式必填”收紧为“所有模式必填”。
- 评审模式只保留正式评审及正式专项评审，不再包含预评审模式。

### 新增参数说明

- 本次未新增参数。
- 本次仅移除 `precheck` 相关模式说明，现有参数仍为：
  - `tapd`
  - `baseline`
  - `mode`
  - `projects`
  - `services`
  - `scope`
  - `output`
  - `overwrite`

### 兼容性说明

- 本次没有新增 TAPD 编号格式兼容规则。
- Command 仍保持薄入口。
- 核心逻辑仍保留在 Skill。
- 这是一次向更严格正式评审收敛的兼容性调整；如果外部调用方仍传 `mode=precheck`，应视为无效旧参数并改用正式模式。

### 后续建议验证场景

1. 无 TAPD 直接发起评审
- 预期：立即要求补 TAPD 和对应变更目标，不能继续执行。

2. 有 TAPD 的默认正式评审
- 预期：按 `formal-gate` 正式输出结论。

3. 有 TAPD 的 `db-only` / `security-only`
- 预期：仍输出正式专项结论，并保留直接关联的业务、发布、回滚风险。

4. baseline 不存在
- 预期：进入 `Unknowns`，不得输出“通过”。

5. 同名报告文件已存在
- 预期：未显式允许覆盖时，自动追加后缀，不覆盖旧文件。

6. 发现疑似敏感配置或密钥
- 预期：只输出掩码值，不输出完整敏感值。
