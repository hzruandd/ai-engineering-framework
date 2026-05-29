# Playwright MCP Server

> 微软官方出品的浏览器自动化 MCP Server，让 Claude Code 能够操作浏览器完成页面交互、测试验证和截图等任务。

## 概述

| 项目 | 信息 |
|------|------|
| 名称 | Playwright MCP |
| 包名 | `@playwright/mcp` |
| 来源 | 微软（Microsoft） |
| 仓库 | [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) |
| 运行方式 | 本地运行，数据不外传 |

## 用途

Playwright MCP 为 Claude Code 提供浏览器自动化能力，适用于：

- **Web 应用测试**：自动化点击、填表、导航，验证页面功能
- **页面截图**：捕获页面快照用于 UI 审查或文档
- **表单自动化**：批量填写表单、选择下拉框、上传文件
- **数据抓取**：从页面提取结构化信息
- **调试辅助**：查看控制台日志、网络请求，定位前端问题

## 安装配置

### 前置条件

- Node.js v18+
- 首次运行会自动下载 Chromium 浏览器

### 配置 settings.json

在 `~/.claude/settings.json`（全局）或项目 `.claude/settings.local.json` 中添加：

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp"]
    }
  }
}
```

### 高级配置

#### 无头模式（不弹出浏览器窗口）

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp", "--headless"]
    }
  }
}
```

#### 指定浏览器

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp", "--browser", "firefox"]
    }
  }
}
```

支持的浏览器：`chromium`（默认）、`firefox`、`webkit`

## 主要功能

| 工具 | 说明 |
|------|------|
| `browser_navigate` | 导航到指定 URL |
| `browser_click` | 点击页面元素 |
| `browser_type` | 在输入框中输入文本 |
| `browser_fill_form` | 批量填写表单字段 |
| `browser_snapshot` | 获取页面无障碍快照（推荐，比截图更适合 AI 理解） |
| `browser_take_screenshot` | 截取页面图片 |
| `browser_select_option` | 选择下拉框选项 |
| `browser_hover` | 悬停在元素上 |
| `browser_press_key` | 按下键盘按键 |
| `browser_evaluate` | 在页面中执行 JavaScript |
| `browser_console_messages` | 查看浏览器控制台日志 |
| `browser_network_requests` | 查看网络请求 |
| `browser_file_upload` | 上传文件 |
| `browser_tabs` | 管理浏览器标签页 |
| `browser_drag` | 拖拽元素 |
| `browser_resize` | 调整浏览器窗口大小 |

## 使用示例

安装配置后，在 Claude Code 中可以直接说：

- "帮我打开 http://localhost:3000 看看页面是否正常"
- "在登录页面填写用户名和密码，测试登录功能"
- "截图当前页面，我想看看布局效果"
- "检查页面控制台有没有报错"

## 注意事项

- 浏览器在本地运行，所有操作在你的机器上执行
- 建议开发/测试环境使用，不要在生产环境操作
- `browser_snapshot` 比 `browser_take_screenshot` 消耗更少 token，推荐优先使用
- 配合团队的 `webapp-testing` Skill 使用效果更佳
