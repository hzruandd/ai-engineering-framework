---
name: openclaw
description: OpenClaw Agent 开发工具包。当用户需要创建 AI Agent、设计多 Agent 系统、编写 Agent 提示词、定义安全边界或编排工作流时自动加载。适用于创建自主任务执行的 AI 应用、多 Agent 协作系统、Agent 安全边界定义、工作流编排等场景。
---

# OpenClaw Agent 开发工具包

## 触发条件

以下场景自动加载本技能：

- 用户提到"Agent"、"智能体"、"OpenClaw"
- 创建自主任务执行的 AI 应用
- 多 Agent 协作架构设计
- Agent 安全边界定义
- 工作流编排设计

## 核心能力

| 能力 | 参考文档 | 说明 |
|------|----------|------|
| Agent 骨架生成 | [reference/agent-skeleton.md](./reference/agent-skeleton.md) | 标准项目结构、配置模板、5 种类型模板 |
| Agent 提示词模板 | [reference/agent-prompt-template.md](./reference/agent-prompt-template.md) | 系统提示词结构、设计原则、完整示例 |
| 安全边界定义 | [reference/safety-boundary.md](./reference/safety-boundary.md) | 4 级安全分级、边界清单、策略模板 |
| 多 Agent 分工 | [reference/multi-agent-design.md](./reference/multi-agent-design.md) | 4 种协作模式、角色模板、通信协议 |
| 工作流编排 | [reference/workflow-orchestration.md](./reference/workflow-orchestration.md) | 5 种工作流模式、标准模板、最佳实践 |

## 开发流程

```
1. 需求分析     →  明确 Agent 目标、能力边界和使用场景
2. 骨架生成     →  使用 agent-skeleton 模板创建项目结构
3. 提示词编写   →  基于 agent-prompt-template 设计系统提示词
4. 安全约束     →  使用 safety-boundary 模板定义安全边界
5. 工作流定义   →  使用 workflow-orchestration 编排执行流程
6. 多 Agent（可选）→  如需协作，使用 multi-agent-design 设计分工
```

## 适用 Agent 类型

| 类型 | 说明 | 安全等级建议 |
|------|------|-------------|
| 代码助手 | 代码生成、审查、重构 | L2（受限写入） |
| 数据分析 | 数据查询、报表生成 | L1（只读） |
| 文档处理 | 文档生成、格式转换 | L2（受限写入） |
| 运维巡检 | 系统监控、日志分析 | L1（只读）/ L3（自动修复） |
| 测试自动化 | 测试生成、自动执行 | L3（自动执行） |

## 注意事项

1. **安全优先**：所有 Agent 必须先定义安全边界，再实现功能
2. **最小权限**：Agent 只授予完成任务所需的最小权限
3. **可审计**：关键操作必须有日志记录
4. **可中断**：Agent 执行过程必须支持人工中断
