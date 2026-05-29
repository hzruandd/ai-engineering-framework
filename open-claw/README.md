# OpenClaw 配置

> OpenClaw 是一个自托管的个人 AI 助手运行平台 / Agent 网关。

## OpenClaw 是什么

OpenClaw 不是一个聊天机器人网站，而是你在自己的电脑或服务器上运行的 AI 助手底座。它让你把各种聊天渠道、工具能力、技能包、模型配置接进来，让 AI 真正去执行事情。

官方定位："Your own personal AI assistant" — 一个 self-hosted gateway。

## 核心架构

```
┌─────────────────────────────────────────────────────┐
│  入口层（Channels）                                  │
│  Telegram · Slack · 飞书 · WhatsApp · Discord ·     │
│  Google Chat · iMessage · Matrix · Teams · WebChat   │
├─────────────────────────────────────────────────────┤
│  Agent 运行层                                        │
│  每个 Agent 有独立的：                               │
│  - 工作目录（workspace）                             │
│  - 会话历史（session store）                         │
│  - 配置和路由绑定                                    │
├─────────────────────────────────────────────────────┤
│  技能 / 工具层（Skills）                             │
│  带 SKILL.md 的能力目录，教 Agent 如何使用工具、     │
│  接外部服务、完成特定任务                            │
├─────────────────────────────────────────────────────┤
│  模型层（Models）                                    │
│  可接不同大模型作为主模型和兜底模型，不绑定某一家    │
└─────────────────────────────────────────────────────┘
```

## 和普通 ChatGPT / Claude 网页版的区别

| | 普通网页版 | OpenClaw |
|---|----------|----------|
| 定位 | 对话 | 运行和执行 |
| 环境 | 受平台限制 | 接你自己的通道、工具、目录、自动化流程 |
| 数据控制 | 由平台决定 | 你自己掌控运行环境和数据 |

## 适合做什么

- 通过聊天消息让 AI 帮你查资料、整理结果
- 执行本机命令、读写文件、调用外部工具
- 管理日程、邮件、提醒、通知
- 让不同 Agent 分工协作
- 在你自己的环境里保留数据和配置控制权

## 本目录放什么

| 内容 | 说明 |
|------|------|
| Agent 配置 | OpenClaw Agent 的定义、路由、工作目录配置 |
| Skills | 为 OpenClaw Agent 编写的技能包 |
| Workflow | 工作流编排定义 |
| 渠道配置 | 消息渠道接入配置 |
| 示例 | Agent 和 Workflow 的使用示例 |

> 本目录目前为初始状态，后续随 OpenClaw 平台推进逐步补充。

## 和仓库其他目录的关系

| 目录 | 和 OpenClaw 的关系 |
|------|-------------------|
| **open-claw/**（本目录） | OpenClaw 平台的实际配置和资产 |
| **skills/openclaw/** | OpenClaw Agent 开发的参考资料（骨架模板、提示词模板、安全边界等） |
| **global-settings/** | Claude Code 的全局配置，和 OpenClaw 是两套体系 |
| **skills/** | Claude Code 的技能包，部分可复用到 OpenClaw |

## 贡献

新增 OpenClaw 相关内容请放在本目录下。详见 [CONTRIBUTING.md](../CONTRIBUTING.md)。
