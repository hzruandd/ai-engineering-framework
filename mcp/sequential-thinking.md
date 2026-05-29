# Sequential Thinking MCP Server

> 官方结构化思考 MCP Server，为 Claude Code 提供链式推理能力，适合解决复杂的多步骤问题。

## 概述

| 项目 | 信息 |
|------|------|
| 名称 | Sequential Thinking MCP |
| 包名 | `@modelcontextprotocol/server-sequential-thinking` |
| 来源 | Model Context Protocol 官方 |
| 仓库 | [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking) |
| 运行方式 | 本地运行 |

## 用途

Sequential Thinking MCP 为 Claude Code 提供结构化的分步推理能力，适用于：

- **复杂问题分解**：将大问题拆解为多个有序的思考步骤
- **架构设计**：逐步推演系统架构，权衡利弊
- **Bug 诊断**：系统化排查问题根因，避免遗漏
- **方案评估**：对比多种技术方案，做出合理决策
- **需求分析**：逐层拆解业务需求，识别关键点

## 安装配置

### 前置条件

- Node.js v18+

### 配置 settings.json

在 `~/.claude/settings.json`（全局）或项目 `.claude/settings.local.json` 中添加：

```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    }
  }
}
```

> 无需额外配置项，安装即用。

## 主要功能

| 工具 | 说明 |
|------|------|
| `sequentialthinking` | 执行一步结构化思考 |

### 核心参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `thought` | string | 当前思考步骤的内容 |
| `thoughtNumber` | number | 当前步骤编号 |
| `totalThoughts` | number | 预估总步骤数（可动态调整） |
| `nextThoughtNeeded` | boolean | 是否需要继续思考 |
| `isRevision` | boolean | 是否修正之前的步骤 |
| `revisesThought` | number | 修正哪一步的结论 |
| `branchFromThought` | number | 从哪一步分叉出新思路 |
| `branchId` | string | 分支标识符 |

### 能力特点

- **动态调整**：思考过程中可以增加或减少步骤
- **回溯修正**：发现前面的假设有误时，可以标记修正
- **分支探索**：从某一步分叉出多条推理路径，对比分析
- **假设验证**：提出假设后系统化验证，确保结论可靠

## 使用示例

安装配置后，在 Claude Code 中遇到复杂问题时，Claude 会自动调用此工具进行分步思考。你也可以主动触发：

- "帮我分析一下这个性能瓶颈，用结构化思考逐步排查"
- "设计一个分布式锁的方案，考虑各种边界情况"
- "这个 Bug 可能是什么原因？帮我系统化排查"
- "对比 Redis 和本地缓存方案，哪个更适合我们的场景"

### 思考过程示例

```
思考 1/5：分析问题现象
→ 接口响应时间从 200ms 上升到 2000ms

思考 2/5：列举可能原因
→ 数据库慢查询 / 缓存失效 / 网络延迟 / 代码逻辑变更

思考 3/5：逐一排查
→ 检查慢查询日志 → 发现全表扫描

思考 4/5（修正第2步）：锁定根因
→ 新上线的功能缺少索引，导致全表扫描

思考 5/5：制定解决方案
→ 添加复合索引 + 优化查询条件
```

## 与 thinking-guide Skill 的关系

本仓库的 [skills/thinking-guide](../skills/thinking-guide/) Skill 提供了 Sequential Thinking 的使用指南和最佳实践。两者配合使用：

- **MCP Server**（本文档）：提供底层工具能力
- **thinking-guide Skill**：提供使用方法论和触发规则

建议两者都安装，以获得最佳的结构化思考体验。

## 注意事项

- 此 MCP Server 不需要任何外部服务或 API Key
- 思考过程完全在本地执行，不涉及网络请求
- 对于简单问题不需要使用此工具，避免过度分析
- 团队已在 CLAUDE.md 中配置了自动触发关键词，遇到复杂问题会自动使用
