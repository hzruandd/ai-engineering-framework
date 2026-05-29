# 快速开始

> 目标：5 分钟内完成安装，让你的 Claude Code 拥有团队统一规范。

## 前置条件

- 已安装 Claude Code（CLI 或 IDE 插件）
- 已安装 Git

## 第一步：克隆仓库

```bash
git clone <仓库地址> city-parking-claude-doc
cd city-parking-claude-doc
```

## 第二步：安装全局配置

全局配置安装后，对你机器上**所有项目**自动生效。

```bash
# macOS / Linux
cp -r global-settings/.claude ~/

# Windows PowerShell
Copy-Item -Recurse -Force global-settings\.claude $env:USERPROFILE\.claude
```

### 安装了什么？

| 内容 | 说明 |
|------|------|
| CLAUDE.md | 52KB 核心开发规范（13 大模块） |
| commands/ | 10 个快捷命令（/new-crud、/review-code 等） |
| docs/ | 18 个参考文档（架构、案例、指南） |

## 第三步：验证安装

在任意项目中打开 Claude Code，输入：

```
请介绍一下 Java 的命名规范
```

如果 Claude 回答了 PascalCase、camelCase 等与团队规范一致的内容 → 安装成功。

## 第四步（可选）：启用项目级配置

如果你的项目有对应的模板（如停车场系统），可以额外启用项目级配置：

```bash
# 复制模板到项目
cp -r project-templates/tzh-parkinglot/.claude /path/to/your-project/
cp project-templates/tzh-parkinglot/CLAUDE.md /path/to/your-project/

# 删除 settings.local.json（会自动生成）
rm /path/to/your-project/.claude/settings.local.json

# 根据实际项目修改 CLAUDE.md
```

项目级配置会**叠加**在全局配置之上，优先级更高。

## 第五步（可选）：安装额外 Skills

如果需要额外的技能包：

```bash
# 查看可用 skills
cat skills/CATALOG.md

# 安装到全局（所有项目可用）
cp -r skills/pdf ~/.claude/skills/

# 或安装到特定项目
cp -r skills/pdf /path/to/your-project/.claude/skills/
```

## 按角色使用指南

### 后端研发

1. **全局规范**已通过第二步安装，自动生效
2. **快捷命令**直接在 Claude Code 中使用：
   - `/new-crud` — 创建完整 CRUD 功能
   - `/add-field` — 为实体添加字段
   - `/new-api` — 添加新接口
   - `/review-code` — 代码审查
   - `/diff-report` — 生成修改报告
3. **Java 开发规范**会在检测到 Java 项目时自动加载（java-guide Skill）

### 前端研发

1. 全局规范自动生效
2. 可用 Skills：`frontend-design`（前端设计）、`webapp-testing`（Web 测试）
3. Skills 会在相关场景自动加载，无需手动操作

### 测试

1. 全局规范自动生效
2. 常用命令：
   - `/generate-tests` — 生成单元测试
   - `/review-code` — 代码审查清单
3. 可用 Skills：`self-test`（自动化自测）、`webapp-testing`（Web 测试）

### 产品

不需要理解 `.claude` 目录结构，直接使用：

1. 安装全局配置（第二步）
2. 在 Claude Code 中直接使用文档类 Skills：
   - 说"帮我做个 PPT" → 自动加载 pptx Skill
   - 说"帮我写个 Word 文档" → 自动加载 docx Skill
   - 说"帮我处理 PDF" → 自动加载 pdf Skill

### OpenClaw 建设者

1. 查看 [open-claw/README.md](open-claw/README.md) 了解 OpenClaw 平台
2. `open-claw/` 目录存放 Agent 配置、Skills、Workflow 等平台资产
3. `skills/openclaw/` 目录有 Agent 开发参考资料

## 下一步

- 了解如何更新配置 → [UPDATE.md](UPDATE.md)
- 了解如何贡献内容 → [CONTRIBUTING.md](CONTRIBUTING.md)
- 查看所有可用 Skills → [skills/CATALOG.md](skills/CATALOG.md)
- 查看所有可用 Commands → [global-settings/README.md](global-settings/README.md)
