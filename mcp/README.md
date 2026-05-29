# MCP 精选推荐

> MCP（Model Context Protocol）是 Anthropic 推出的开放协议，让 AI 助手能够安全地连接外部工具和数据源。
> 本目录收录经过团队验证的精选 MCP Server，每个都附有详细说明和安装配置指南。

## 什么是 MCP

MCP Server 是运行在本地的轻量服务，通过标准化协议为 Claude Code 提供额外能力——比如操作浏览器、查询数据库、获取网页内容等。所有数据处理都在本地完成，安全可控。

## 如何安装

MCP Server 在 Claude Code 中通过 `settings.json` 配置。配置文件位置：

- **全局**（所有项目生效）：`~/.claude/settings.json`
- **项目级**（仅当前项目）：`项目根目录/.claude/settings.local.json`

配置格式：

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@scope/package-name"],
      "env": {}
    }
  }
}
```

> 前置条件：需要安装 [Node.js](https://nodejs.org/)（v18+）。

## 精选列表

| MCP Server | 用途 | 文档 |
|------------|------|------|
| Playwright | 浏览器自动化（页面操作、截图、表单填写） | [playwright.md](playwright.md) |
| Fetch | 网页内容抓取（HTML 转 Markdown、API 调用） | [fetch.md](fetch.md) |
| MySQL | 数据库查询（Schema 浏览、SQL 执行） | [mysql.md](mysql.md) |
| Sequential Thinking | 结构化思考（复杂问题分步推理） | [sequential-thinking.md](sequential-thinking.md) |

## 使用建议

- **日常开发**：Playwright + MySQL 组合，覆盖前端测试和数据库调试
- **文档研究**：Fetch 用于抓取技术文档和 API 参考
- **复杂分析**：Sequential Thinking 用于架构设计和问题诊断

## 贡献新 MCP

如果你发现好用的 MCP Server，欢迎按照现有格式添加说明文档。详见 [CONTRIBUTING.md](../CONTRIBUTING.md)。
