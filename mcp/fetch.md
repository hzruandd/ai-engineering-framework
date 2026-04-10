# Fetch MCP Server

> 官方网页抓取 MCP Server，让 Claude Code 能够获取网页内容并自动转为 Markdown，方便分析和引用。

## 概述

| 项目 | 信息 |
|------|------|
| 名称 | Fetch MCP |
| 包名 | `@modelcontextprotocol/server-fetch` |
| 来源 | Model Context Protocol 官方 |
| 仓库 | [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch) |
| 运行方式 | 本地运行，数据不外传 |

## 用途

Fetch MCP 为 Claude Code 提供网页内容获取能力，适用于：

- **技术文档查阅**：抓取官方文档、API 参考，辅助编码
- **API 响应分析**：直接调用 REST API 并分析返回结果
- **网页内容提取**：从网页中提取关键信息，自动转为 Markdown
- **竞品/方案调研**：快速浏览和总结技术方案页面

## 安装配置

### 前置条件

- Node.js v18+

### 配置 settings.json

在 `~/.claude/settings.json`（全局）或项目 `.claude/settings.local.json` 中添加：

```json
{
  "mcpServers": {
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    }
  }
}
```

### 高级配置

#### 自定义 User-Agent

```json
{
  "mcpServers": {
    "fetch": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-fetch",
        "--user-agent",
        "MyBot/1.0"
      ]
    }
  }
}
```

## 主要功能

| 工具 | 说明 |
|------|------|
| `fetch` | 获取 URL 内容，HTML 自动转为 Markdown |

### 功能特点

- **智能转换**：HTML 页面自动去除脚本、样式等无关内容，转为简洁 Markdown
- **内容分块**：大页面自动分块返回，避免超出 token 限制
- **格式支持**：支持 HTML、JSON、纯文本等多种格式
- **安全沙箱**：通过 MCP 协议隔离执行，不会在宿主机执行任意代码

## 使用示例

安装配置后，在 Claude Code 中可以直接说：

- "帮我看一下 Spring Boot 3.0 的迁移文档"
- "抓取这个 API 的 Swagger 文档，分析接口结构"
- "帮我查一下 MyBatis Plus 的条件构造器用法"
- "获取这个 GitHub Issue 的内容"

## 注意事项

- 只能访问公开网页，无法访问需要登录的页面（如 Google Docs、Confluence）
- 对于需要认证的服务，请使用专门的 MCP Server（如 GitHub 用 `gh` CLI）
- 大型页面的内容可能被截断或摘要化
- 尊重网站的 robots.txt 规则
