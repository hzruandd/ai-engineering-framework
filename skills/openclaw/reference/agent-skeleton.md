# Agent 骨架生成模板

> 标准化的 Agent 项目结构和配置模板

## 标准项目结构

```
agent-project/
├── README.md                      # Agent 项目说明
├── CLAUDE.md                      # Agent 的 Claude Code 配置
├── config/
│   ├── agent-config.yaml          # Agent 核心配置
│   └── safety-policy.yaml         # 安全策略配置
├── prompts/
│   ├── system-prompt.md           # 系统提示词
│   ├── task-templates/            # 任务模板
│   │   ├── default.md
│   │   └── complex-task.md
│   └── safety-rules.md            # 安全规则提示词
├── tools/                         # Agent 可用工具
│   ├── file-tools.md              # 文件操作工具定义
│   ├── api-tools.md               # API 调用工具定义
│   └── db-tools.md                # 数据库工具定义
├── workflows/                     # 工作流定义
│   ├── default-workflow.yaml
│   └── review-workflow.yaml
└── tests/                         # Agent 测试
    ├── test-cases.md
    └── evaluation.md
```

## 骨架生成步骤

### 第一步：确定 Agent 类型

```yaml
# agent-config.yaml
agent:
  name: "my-agent"
  type: "code-assistant"           # 见下方类型列表
  version: "1.0.0"
  description: "Agent 的简短描述"
```

### 第二步：定义能力范围

```yaml
# agent-config.yaml（续）
capabilities:
  read:
    - "source-code"
    - "documentation"
    - "configuration"
  write:
    - "source-code"
    - "test-code"
  execute:
    - "build-commands"
    - "test-commands"
  deny:
    - "deploy-commands"
    - "database-migration"
```

### 第三步：配置工具集

```yaml
# agent-config.yaml（续）
tools:
  enabled:
    - name: "file-read"
      scope: "project-directory"
    - name: "file-write"
      scope: "project-directory"
      exclude: ["*.env", "*.key", "*.secret"]
    - name: "bash"
      allowed_commands: ["npm", "mvn", "gradle", "git"]
  disabled:
    - name: "network-access"
      reason: "安全策略限制"
```

### 第四步：设置执行参数

```yaml
# agent-config.yaml（续）
execution:
  max_steps: 50                    # 最大执行步骤
  timeout_minutes: 30              # 超时时间
  retry_policy:
    max_retries: 3
    backoff: "exponential"
  checkpoint:
    enabled: true
    interval_steps: 10             # 每 10 步保存检查点
```

### 第五步：验证骨架

- 检查所有配置文件格式正确
- 确认系统提示词已编写
- 确认安全策略已定义
- 运行测试用例验证

## Agent 类型模板

### 代码助手（code-assistant）

```yaml
agent:
  type: "code-assistant"
capabilities:
  read: ["source-code", "documentation", "test-code"]
  write: ["source-code", "test-code"]
  execute: ["build", "test", "lint"]
  deny: ["deploy", "database-write"]
```

### 数据分析（data-analyst）

```yaml
agent:
  type: "data-analyst"
capabilities:
  read: ["database", "csv-files", "api-responses"]
  write: ["reports", "visualizations"]
  execute: ["sql-queries", "data-scripts"]
  deny: ["database-write", "file-delete"]
```

### 文档处理（doc-processor）

```yaml
agent:
  type: "doc-processor"
capabilities:
  read: ["source-code", "documentation", "templates"]
  write: ["documentation", "reports"]
  execute: ["format-tools", "export-tools"]
  deny: ["source-code-write", "deploy"]
```

### 运维巡检（ops-inspector）

```yaml
agent:
  type: "ops-inspector"
capabilities:
  read: ["logs", "metrics", "configuration"]
  write: ["reports", "alerts"]
  execute: ["health-check", "log-analysis"]
  deny: ["service-restart", "config-change"]
```

### 测试自动化（test-automation）

```yaml
agent:
  type: "test-automation"
capabilities:
  read: ["source-code", "test-code", "test-data"]
  write: ["test-code", "test-reports"]
  execute: ["test-runner", "coverage-tools"]
  deny: ["source-code-write", "deploy"]
```
