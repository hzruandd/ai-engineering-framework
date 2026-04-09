# City Parking — AI 辅助开发配置库

团队统一的 Claude Code 配置仓库。包含全局开发规范、项目配置模板、可复用技能包和 OpenClaw 配置。

**一句话说明**：clone 下来，把全局配置复制到 `~/.claude/`，你的 Claude Code 就拥有了团队统一的开发规范和工具链。

## 这个仓库适合谁

| 角色 | 你会用到 | 从哪开始 |
|------|----------|----------|
| 后端研发 | 全局规范 + Java Skills + Commands | [QUICKSTART.md](QUICKSTART.md) → 全局安装 |
| 前端研发 | 全局规范 + 前端 Skills | [QUICKSTART.md](QUICKSTART.md) → 全局安装 |
| 测试 | 测试相关 Skills | [QUICKSTART.md](QUICKSTART.md) → 按角色选 Skills |
| 产品 | 文档类 Skills | [QUICKSTART.md](QUICKSTART.md) → 产品入口 |
| OpenClaw 建设者 | open-claw/ 配置 | [open-claw/README.md](open-claw/README.md) |

## 仓库结构

```
city-parking-claude-doc/
├── global-settings/         # 全局配置（规范 + Commands + 参考文档）
├── project-templates/       # 项目级 Claude 配置模板
├── open-claw/               # OpenClaw 平台配置（自托管 AI 助手网关）
├── skills/                  # 22 个可复用技能包
├── QUICKSTART.md            # 快速开始（5 分钟上手）
├── CONTRIBUTING.md          # 贡献指南（内容该放哪）
├── UPDATE.md                # 更新指南（如何同步最新配置）
└── CHANGELOG.md             # 变更记录
```

各目录详细说明：[STRUCTURE.md](STRUCTURE.md)

## 全局配置 vs 项目配置

```
┌──────────────────────────────────────────────┐
│  全局配置（~/.claude/）                       │  ← 所有项目自动生效
│  来源：global-settings/.claude/              │
│  内容：开发规范 + 通用 Commands + 参考文档    │
├──────────────────────────────────────────────┤
│  项目配置（项目根目录/.claude/ + CLAUDE.md）  │  ← 仅当前项目生效
│  来源：project-templates/<模板>/             │
│  内容：项目专属规范 + 业务 Skills             │
├──────────────────────────────────────────────┤
│  Skills（按需自动加载）                       │
│  来源：skills/ 或项目内 .claude/skills/      │
│  内容：特定场景的专业能力                     │
└──────────────────────────────────────────────┘

优先级：项目配置 > 全局配置 | Skills 按需加载
```

## 快速开始

```bash
# 1. 克隆
git clone <仓库地址> city-parking-claude-doc
cd city-parking-claude-doc

# 2. 安装全局配置
# macOS / Linux
cp -r global-settings/.claude ~/
# Windows PowerShell
Copy-Item -Recurse -Force global-settings\.claude $env:USERPROFILE\.claude

# 3. 验证（在任意项目中打开 Claude Code）
# 输入：请介绍一下 Java 的命名规范
# 如果回答了 PascalCase、camelCase 等规范 → 安装成功
```

详细步骤见 [QUICKSTART.md](QUICKSTART.md)

## 核心资产一览

### 全局配置（global-settings/）

- 核心规范 CLAUDE.md（52KB，13 大模块）
- 10 个快捷命令：`/new-crud` `/add-field` `/new-api` `/fix-cache` `/review-code` `/diff-report` `/generate-tests` `/formal-review` `/design-doc` `/analyze-slow-query`
- 18 个参考文档（架构设计、实战案例、开发指南）

详见 [global-settings/README.md](global-settings/README.md)

### 技能包（skills/）

22 个 Skills，按用途分类：

| 分类 | Skills |
|------|--------|
| 工程研发 | java-guide · new-crud · add-field · new-api · fix-cache · mcp-builder · frontend-design |
| 质量保障 | review-code · diff-report · generate-tests · self-test · webapp-testing |
| 文档工具 | pdf · pptx · docx · xlsx · doc-coauthoring |
| 设计创意 | canvas-design · algorithmic-art · theme-factory |
| 元技能 | skill-creator · thinking-guide |

详见 [skills/CATALOG.md](skills/CATALOG.md)

### 项目模板（project-templates/）

| 模板 | 适用场景 |
|------|----------|
| tzh-parkinglot | Spring Boot + Dubbo 微服务停车场系统 |

详见 [project-templates/CATALOG.md](project-templates/CATALOG.md)

### OpenClaw（open-claw/）

自托管的个人 AI 助手运行平台 / Agent 网关的配置和资产。

详见 [open-claw/README.md](open-claw/README.md)

## 常用操作

| 我想… | 怎么做 |
|-------|--------|
| 第一次安装 | [QUICKSTART.md](QUICKSTART.md) |
| 更新到最新配置 | [UPDATE.md](UPDATE.md) |
| 给项目启用配置 | 复制 project-templates 中的模板到项目 |
| 贡献新 Skill/Command | [CONTRIBUTING.md](CONTRIBUTING.md) |
| 了解变更历史 | [CHANGELOG.md](CHANGELOG.md) |

## 版本

- 当前版本：v1.1.0
- 更新日期：2026-04-08
