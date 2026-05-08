# tzh-review 使用说明

`tzh-review` 用于在停智慧智慧停车生态平台场景下，对代码变更执行正式评审。它不是简单的 diff 总结，而是一套带强门禁的评审工作流：先核验 TAPD，再扫描变更，再做代码、数据库、测试、安全、部署回滚评审，最后输出正式报告与放行结论。

## 适用场景

- 提测前代码评审
- 上线前代码评审
- 当前分支质量门禁
- 多项目、多服务联合发布评审
- SQL、字段、索引、DDL、DML、数据修复脚本评审
- Doris、Dinky、MV、报表口径影响评审
- 订单、支付、计费、月租、券包、发票、清分、对账、权限、开闸链路评审

## 触发方式

1. 命令触发

```text
/tzh-review tapd=TAPD-123456
/tzh-review tapd=TAPD-123456,TAPD-123457
/tzh-review tapd=TAPD-123456 baseline=release/2026.05
```

2. 自然语言触发

```text
帮我评审当前分支代码，TAPD-123456
生成停智慧代码评审报告，TAPD-123456
检查这次 SQL 和数据库字段变更风险，TAPD-123456
做一次上线前评审，TAPD-123456,TAPD-123457
```

## 强门禁

### 1. TAPD 必填

- 未提供 TAPD 编号时，必须先补 TAPD，评审暂停。
- 不允许仅凭分支名或 commit message 猜测 TAPD 并继续。
- 支持多个 TAPD，但每个 TAPD 都要对应本次变更目标。

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

## 输出内容

评审结束后，至少应输出：
- 正式评审报告
- TAPD 追踪矩阵
- 文件/变更到 TAPD 的反向追踪矩阵
- 风险矩阵
- 行动项
- 证据表
- Unknowns 与人工确认项
- 单项目或多项目放行结论

## 目录结构

```text
.claude/
├── commands/
│   └── tzh-review.md
└── skills/
    └── tzh-review/
        ├── SKILL.md
        ├── README.md
        ├── templates/
        ├── checklists/
        └── examples/
```

## 推荐使用流程

1. 提供 TAPD 编号与本次变更目标。
2. 如有非 `master` 基线，显式说明 baseline。
3. 让 `tzh-review` 自动识别单项目或多项目模式。
4. 基于正式报告模板输出评审结果。
5. 根据行动项闭环后，再决定是否放行。

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
- 未提供 Sonar、覆盖率、EXPLAIN、回滚脚本等证据时，应保持 Unknown，而不是代写“达标”。
