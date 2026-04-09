# 工作流编排模板

> Agent 工作流模式、标准模板和最佳实践

## 工作流模式

### 1. 顺序模式（Sequential）

```yaml
workflow:
  name: "顺序执行"
  steps:
    - id: "step-1"
      action: "分析需求"
      input: "user_request"
      output: "requirements"

    - id: "step-2"
      action: "生成代码"
      input: "requirements"
      output: "source_code"
      depends_on: ["step-1"]

    - id: "step-3"
      action: "验证代码"
      input: "source_code"
      output: "validation_result"
      depends_on: ["step-2"]
```

### 2. 条件模式（Conditional）

```yaml
workflow:
  name: "条件分支"
  steps:
    - id: "analyze"
      action: "分析问题类型"
      output: "problem_type"

    - id: "fix-bug"
      action: "修复 Bug"
      condition: "problem_type == 'bug'"
      depends_on: ["analyze"]

    - id: "add-feature"
      action: "添加功能"
      condition: "problem_type == 'feature'"
      depends_on: ["analyze"]

    - id: "refactor"
      action: "重构代码"
      condition: "problem_type == 'refactor'"
      depends_on: ["analyze"]
```

### 3. 并行模式（Parallel）

```yaml
workflow:
  name: "并行执行"
  steps:
    - id: "prepare"
      action: "准备环境"

    - id: "task-a"
      action: "前端修改"
      depends_on: ["prepare"]
      parallel_group: "impl"

    - id: "task-b"
      action: "后端修改"
      depends_on: ["prepare"]
      parallel_group: "impl"

    - id: "task-c"
      action: "数据库变更"
      depends_on: ["prepare"]
      parallel_group: "impl"

    - id: "merge"
      action: "合并结果"
      depends_on: ["task-a", "task-b", "task-c"]
```

### 4. 循环模式（Loop）

```yaml
workflow:
  name: "迭代优化"
  steps:
    - id: "implement"
      action: "实现功能"

    - id: "review"
      action: "审查代码"
      depends_on: ["implement"]

    - id: "check"
      action: "检查是否通过"
      depends_on: ["review"]
      loop:
        condition: "review_result == 'rejected'"
        target: "implement"
        max_iterations: 3
```

### 5. 错误恢复模式（Error Recovery）

```yaml
workflow:
  name: "带错误恢复"
  steps:
    - id: "main-task"
      action: "执行主任务"
      on_error:
        retry:
          max_attempts: 3
          backoff: "exponential"
        fallback: "fallback-task"

    - id: "fallback-task"
      action: "降级处理"
      trigger: "on_error"
```

## 标准工作流模板

### 模板一：代码修改工作流

```yaml
workflow:
  name: "代码修改标准流程"
  description: "从需求到交付的完整代码修改流程"

  steps:
    - id: "1-analyze"
      name: "需求分析"
      action: "分析用户需求，确定修改范围"
      tools: ["Read", "Grep", "Glob"]
      output: "修改计划（涉及文件、修改点）"

    - id: "2-implement"
      name: "代码实现"
      action: "按计划修改代码"
      tools: ["Read", "Edit", "Write"]
      depends_on: ["1-analyze"]
      output: "修改后的代码文件"

    - id: "3-test"
      name: "编写测试"
      action: "为修改的代码编写单元测试"
      tools: ["Write", "Bash"]
      depends_on: ["2-implement"]
      output: "测试代码"

    - id: "4-review"
      name: "自查审核"
      action: "检查代码质量、规范合规"
      tools: ["Read", "Grep"]
      depends_on: ["2-implement", "3-test"]
      output: "审查报告"

    - id: "5-report"
      name: "生成报告"
      action: "生成代码修改报告"
      tools: ["Bash", "Write"]
      depends_on: ["4-review"]
      output: "CHANGE_REPORT.md"
```

### 模板二：文档生成工作流

```yaml
workflow:
  name: "文档生成标准流程"

  steps:
    - id: "1-explore"
      name: "探索代码"
      action: "读取相关源码，理解实现逻辑"
      tools: ["Read", "Grep", "Glob"]

    - id: "2-outline"
      name: "生成大纲"
      action: "根据代码生成文档大纲"
      depends_on: ["1-explore"]

    - id: "3-draft"
      name: "撰写初稿"
      action: "按大纲撰写完整文档"
      depends_on: ["2-outline"]

    - id: "4-review"
      name: "审核校对"
      action: "检查准确性、完整性、格式"
      depends_on: ["3-draft"]

    - id: "5-output"
      name: "输出文档"
      action: "保存最终文档"
      depends_on: ["4-review"]
```

### 模板三：问题排查工作流

```yaml
workflow:
  name: "问题排查标准流程"

  steps:
    - id: "1-gather"
      name: "收集信息"
      action: "收集错误日志、堆栈信息、复现步骤"
      tools: ["Read", "Bash", "Grep"]

    - id: "2-analyze"
      name: "分析根因"
      action: "分析错误模式，定位根因"
      tools: ["Read", "Grep"]
      depends_on: ["1-gather"]

    - id: "3-fix"
      name: "修复问题"
      action: "编写修复代码"
      tools: ["Edit", "Write"]
      depends_on: ["2-analyze"]

    - id: "4-verify"
      name: "验证修复"
      action: "运行测试，验证修复有效"
      tools: ["Bash"]
      depends_on: ["3-fix"]
      loop:
        condition: "验证失败"
        target: "2-analyze"
        max_iterations: 3

    - id: "5-document"
      name: "记录总结"
      action: "记录问题原因、修复方案、防止复发措施"
      depends_on: ["4-verify"]
```

## 编排最佳实践

### 1. 检查点设计

- 每个关键步骤后设置检查点
- 检查点保存当前状态，支持断点续执行
- 检查点间隔不超过 10 步

### 2. 超时与重试

- 每个步骤设置合理的超时时间
- 幂等操作可以安全重试
- 非幂等操作重试前检查状态

### 3. 错误处理

- 区分可恢复错误和不可恢复错误
- 可恢复错误：自动重试
- 不可恢复错误：降级处理或人工介入

### 4. 人工介入点

- 在高风险操作前设置人工审批
- 连续失败超过阈值时通知人工
- 关键决策节点保留人工确认选项

### 5. 日志与追踪

- 每个步骤记录开始时间、结束时间、执行结果
- 记录输入输出的摘要（非完整内容）
- 支持按工作流 ID 查询完整执行记录
