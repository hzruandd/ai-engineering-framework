# 多 Agent 分工设计

> 多 Agent 协作模式、角色模板和通信协议

## 协作模式

### 1. 串行模式（Pipeline）

```
Agent A → Agent B → Agent C → 最终结果
```

**适用场景**：流水线式处理，每步依赖前一步结果

**示例**：需求分析 Agent → 代码生成 Agent → 代码审查 Agent

### 2. 并行模式（Fan-out / Fan-in）

```
              ┌→ Agent B ─┐
Agent A ──────┤            ├──→ Agent E（汇总）
              └→ Agent C ─┘
              └→ Agent D ─┘
```

**适用场景**：独立子任务可并发执行

**示例**：任务拆分 Agent → 并行执行（前端 Agent + 后端 Agent + 测试 Agent）→ 汇总 Agent

### 3. 层级模式（Hierarchical）

```
           Coordinator Agent
          ┌───────┼───────┐
     Worker A  Worker B  Worker C
```

**适用场景**：复杂任务需要统一协调和分配

**示例**：项目经理 Agent → 分配给前端开发 Agent、后端开发 Agent、测试 Agent

### 4. 对话模式（Debate / Review）

```
Agent A ←→ Agent B
（互相评审 / 辩论）
```

**适用场景**：需要多角度验证的决策

**示例**：开发 Agent ←→ 审查 Agent（互相提出改进意见直到达成共识）

## 角色模板

### 规划者（Planner）

```yaml
role: planner
responsibilities:
  - 分析任务需求
  - 拆解子任务
  - 分配给合适的执行者
  - 监控整体进度

capabilities:
  read: ["requirements", "task-list", "progress-reports"]
  write: ["task-assignments", "plans"]
  execute: []

output:
  format: "task-list"
  fields: ["task_id", "description", "assigned_to", "priority", "deadline"]
```

### 执行者（Executor）

```yaml
role: executor
responsibilities:
  - 接收并理解任务
  - 执行具体操作
  - 报告执行结果
  - 处理执行异常

capabilities:
  read: ["source-code", "documentation", "task-description"]
  write: ["source-code", "test-code", "progress-report"]
  execute: ["build", "test"]

output:
  format: "execution-report"
  fields: ["task_id", "status", "result", "artifacts", "issues"]
```

### 审查者（Reviewer）

```yaml
role: reviewer
responsibilities:
  - 审查执行结果
  - 检查质量标准
  - 提出改进建议
  - 决定是否通过

capabilities:
  read: ["source-code", "test-results", "quality-standards"]
  write: ["review-report", "feedback"]
  execute: []

output:
  format: "review-report"
  fields: ["review_id", "status", "issues", "suggestions", "verdict"]
```

### 协调者（Coordinator）

```yaml
role: coordinator
responsibilities:
  - 协调多个 Agent 之间的工作
  - 解决冲突和依赖
  - 汇总最终结果
  - 处理异常情况

capabilities:
  read: ["all-reports", "task-status", "conflict-list"]
  write: ["coordination-plan", "final-report"]
  execute: []

output:
  format: "coordination-report"
  fields: ["phase", "status", "resolved_conflicts", "next_actions"]
```

## 通信协议

### 消息格式

```yaml
message:
  id: "msg-001"                    # 消息唯一 ID
  from: "planner"                  # 发送者角色
  to: "executor-backend"           # 接收者角色
  type: "task-assignment"          # 消息类型
  priority: "high"                 # 优先级
  timestamp: "2026-04-04T19:00:00"
  content:
    task_id: "TASK-001"
    description: "实现用户登录接口"
    context:
      - "参考 UserController 现有模式"
      - "使用 JWT 认证"
    expected_output:
      - "UserLoginApi.java"
      - "UserLoginServiceImpl.java"
    deadline: "2026-04-04T20:00:00"
```

### 消息类型

| 类型 | 说明 | 方向 |
|------|------|------|
| `task-assignment` | 任务分配 | 规划者 → 执行者 |
| `progress-update` | 进度更新 | 执行者 → 规划者 |
| `review-request` | 审查请求 | 执行者 → 审查者 |
| `review-feedback` | 审查反馈 | 审查者 → 执行者 |
| `conflict-report` | 冲突报告 | 任意 → 协调者 |
| `resolution` | 冲突解决 | 协调者 → 相关方 |
| `completion` | 任务完成 | 执行者 → 规划者 |

### 状态机

```
PENDING → ASSIGNED → IN_PROGRESS → REVIEW → APPROVED → COMPLETED
                         ↓                     ↓
                      BLOCKED              REJECTED → IN_PROGRESS
                         ↓
                      ESCALATED
```

## 多 Agent 系统设计示例

### 示例：代码修改工作流

```yaml
agents:
  - role: planner
    name: "任务规划"
    description: "分析需求，拆解任务"

  - role: executor
    name: "代码实现"
    description: "编写代码"

  - role: reviewer
    name: "代码审查"
    description: "审查代码质量"

  - role: executor
    name: "测试编写"
    description: "编写单元测试"

workflow:
  1. planner 分析需求 → 生成任务列表
  2. executor(代码实现) 按任务编写代码
  3. reviewer 审查代码
  4. 如果审查通过 → executor(测试编写) 编写测试
  5. 如果审查不通过 → executor(代码实现) 修改代码 → 回到步骤 3
  6. planner 汇总结果
```
