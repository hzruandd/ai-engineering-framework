# 安全边界模板

> Agent 安全分级、边界定义和策略配置

## 安全分级体系

| 等级 | 名称 | 说明 | 适用场景 |
|------|------|------|----------|
| L1 | 只读 | Agent 只能读取信息，不能修改任何内容 | 数据分析、日志查看、代码阅读 |
| L2 | 受限写入 | Agent 可以在指定范围内创建/修改文件 | 代码生成、文档撰写、测试编写 |
| L3 | 自动执行 | Agent 可以执行预定义的命令和操作 | 自动化测试、构建、部署检查 |
| L4 | 全自动 | Agent 可以自主决策并执行复杂操作 | 运维自动化（需人工审批） |

## 安全边界定义清单

### 文件系统边界

```yaml
file_system:
  read:
    allowed:
      - "src/**/*"                  # 源代码
      - "test/**/*"                 # 测试代码
      - "docs/**/*"                 # 文档
      - "config/*.yaml"             # 配置文件
    denied:
      - "**/.env"                   # 环境变量
      - "**/*.key"                  # 密钥文件
      - "**/*.pem"                  # 证书文件
      - "**/credentials*"           # 凭据文件

  write:
    allowed:
      - "src/**/*.java"             # Java 源码
      - "test/**/*.java"            # 测试代码
      - "docs/**/*.md"              # 文档
    denied:
      - "config/**/*"               # 配置文件不允许修改
      - "pom.xml"                   # 构建文件不允许修改
      - ".claude/**/*"              # Claude 配置不允许修改

  delete:
    allowed: []                     # 默认不允许删除
    require_approval: true          # 如需删除，必须人工审批
```

### 网络边界

```yaml
network:
  outbound:
    allowed:
      - "*.internal.company.com"    # 内部服务
      - "maven.aliyun.com"          # Maven 仓库
      - "registry.npmmirror.com"    # NPM 仓库
    denied:
      - "*"                         # 默认拒绝所有外部访问

  inbound:
    allowed: []                     # Agent 不接受外部请求
```

### 数据库边界

```yaml
database:
  allowed_operations:
    - "SELECT"                      # 只读查询
  denied_operations:
    - "INSERT"
    - "UPDATE"
    - "DELETE"
    - "DROP"
    - "ALTER"
    - "TRUNCATE"
  row_limit: 1000                   # 单次查询行数限制
  sensitive_tables:                 # 敏感表（禁止访问）
    - "user_password"
    - "payment_info"
    - "access_token"
```

### API 调用边界

```yaml
api:
  allowed:
    - name: "内部微服务 API"
      methods: ["GET"]
      rate_limit: "60/minute"
    - name: "监控 API"
      methods: ["GET"]
      rate_limit: "30/minute"
  denied:
    - name: "支付 API"
      reason: "涉及资金操作"
    - name: "用户管理 API"
      reason: "涉及权限变更"
```

### 代码执行边界

```yaml
execution:
  allowed_commands:
    - "mvn compile"
    - "mvn test"
    - "npm run build"
    - "npm test"
    - "git status"
    - "git diff"
    - "git log"
  denied_commands:
    - "rm -rf"
    - "git push"
    - "git reset --hard"
    - "mvn deploy"
    - "docker"
    - "kubectl"
  timeout: 300                      # 单命令超时（秒）
  max_concurrent: 3                 # 最大并发命令数
```

## 安全策略模板

### L1 只读策略

```yaml
# safety-policy.yaml
level: L1
name: "只读分析"
description: "Agent 只能读取和分析信息"

permissions:
  file:
    read: true
    write: false
    delete: false
  database:
    query: true
    modify: false
  network:
    outbound: false
  execution:
    commands: false

audit:
  log_all_actions: true
  alert_on_denied: true
```

### L2 受限写入策略

```yaml
# safety-policy.yaml
level: L2
name: "受限开发"
description: "Agent 可以在限定范围内读写代码"

permissions:
  file:
    read: true
    write: true
    write_scope: ["src/**/*.java", "test/**/*.java"]
    delete: false
  database:
    query: true
    modify: false
  network:
    outbound: false
  execution:
    commands: true
    allowed: ["mvn compile", "mvn test"]

approval:
  required_for:
    - "修改超过 5 个文件"
    - "创建新模块"
    - "修改公共组件"

audit:
  log_all_actions: true
  log_file_changes: true
  alert_on_denied: true
```

### L3 自动执行策略

```yaml
# safety-policy.yaml
level: L3
name: "自动化执行"
description: "Agent 可以自动执行预定义的任务流"

permissions:
  file:
    read: true
    write: true
    delete: false
  database:
    query: true
    modify: false
  network:
    outbound: true
    outbound_scope: ["*.internal.company.com"]
  execution:
    commands: true
    allowed: ["mvn", "npm", "git status", "git diff", "curl"]

guardrails:
  max_steps: 100
  timeout_minutes: 60
  checkpoint_interval: 20
  human_review_triggers:
    - "连续 3 次操作失败"
    - "执行时间超过 30 分钟"
    - "修改文件超过 10 个"

audit:
  log_all_actions: true
  log_file_changes: true
  log_commands: true
  alert_on_denied: true
  daily_report: true
```

## 常见场景安全约束

| 场景 | 推荐等级 | 关键约束 |
|------|----------|----------|
| 代码审查 | L1 | 只读，不修改代码 |
| 代码生成 | L2 | 限定目录写入，不修改配置 |
| 单元测试生成 | L2 | 只写 test/ 目录 |
| 自动化构建 | L3 | 限定命令列表 |
| 日志分析 | L1 | 只读，脱敏输出 |
| 文档生成 | L2 | 只写 docs/ 目录 |
