# 贡献指南

## 核心原则

1. 新增内容前先确认放在哪个目录
2. 提交前补齐必要信息（场景、适用对象、示例）
3. 不要修改别人的内容而不通知维护人
4. 保持简洁，不要为了"完整"而写空泛内容

## 内容该放哪里？

### 决策流程

```
这个内容是…
├── 全公司通用的开发规范/最佳实践？
│   └── → global-settings/.claude/  （CLAUDE.md 或 docs/）
├── 某个角色常用但不限于特定项目？
│   └── → skills/<skill-name>/
├── 某个项目专用的配置？
│   └── → project-templates/<project>/
├── OpenClaw 平台相关的配置/资产？
│   └── → open-claw/
└── 不确定？
    └── 先放 skills/，后续再归类
```

### 详细分类规则

| 内容类型 | 放在哪里 | 示例 |
|----------|----------|------|
| 全局开发规范 | global-settings/.claude/CLAUDE.md | Java 命名规范、Git 提交规范 |
| 通用快捷命令 | global-settings/.claude/commands/ | /review-code、/diff-report |
| 通用参考文档 | global-settings/.claude/docs/ | 架构设计文档、实战案例 |
| 可复用技能 | skills/<skill-name>/ | java-guide、pdf、webapp-testing |
| 项目配置模板 | project-templates/<project>/ | tzh-parkinglot |
| OpenClaw 配置 | open-claw/ | Agent 定义、Workflow 模板、渠道配置 |

### Skill vs Command vs Doc 怎么区分？

| 类型 | 特点 | 放在哪 |
|------|------|--------|
| Skill | 自动加载、持久上下文、有触发条件 | skills/<name>/SKILL.md |
| Command | 手动触发（/命令名）、一次性执行 | global-settings/.claude/commands/<name>.md |
| Doc | 参考文档、被 CLAUDE.md 或 Skill 引用 | global-settings/.claude/docs/ |

**简单判断**：
- 用户说某个关键词就应该自动生效 → Skill
- 用户主动输入 `/xxx` 才触发 → Command
- 被其他文件引用的背景知识 → Doc

## 新增 Skill

### 1. 创建目录

```bash
mkdir -p skills/your-skill-name/reference
```

### 2. 编写 SKILL.md

必须包含 frontmatter：

```markdown
---
name: your-skill-name
description: 一句话说明这个 Skill 做什么、什么时候触发。
---

# Skill 标题

## 触发条件
说明什么场景下自动加载。

## 核心能力
这个 Skill 能做什么。

## 使用方式
怎么用。
```

### 3. 添加参考文档（可选）

复杂 Skill 可在 `reference/` 下放详细文档。

### 4. 更新索引

在 [skills/CATALOG.md](skills/CATALOG.md) 中添加你的 Skill。

### 5. 提交

```bash
git add skills/your-skill-name/
git commit -m "feat(skill): 添加 your-skill-name 技能包"
```

## 新增 Command

### 1. 创建命令文件

```bash
# 文件名即命令名（不含 /）
touch global-settings/.claude/commands/your-command.md
```

### 2. 编写内容

Command 文件就是一段提示词，Claude Code 会在用户输入 `/your-command` 时注入。

### 3. 提交

```bash
git add global-settings/.claude/commands/your-command.md
git commit -m "feat(command): 添加 /your-command 命令"
```

## 新增项目模板

### 1. 创建目录

```bash
mkdir -p project-templates/your-project/.claude/skills
```

### 2. 必须包含的文件

- `CLAUDE.md` — 项目级配置（项目概述、模块结构、技术栈、构建命令）
- `.claude/settings.local.json` — 本地设置（可选）
- `.claude/skills/` — 项目专用 Skills（可选）

### 3. 更新索引

在 [project-templates/CATALOG.md](project-templates/CATALOG.md) 中添加你的模板。

### 4. 提交

```bash
git add project-templates/your-project/
git commit -m "feat(template): 添加 your-project 项目模板"
```

## 新增 OpenClaw 内容

OpenClaw 相关的 Agent 配置、Workflow 模板、渠道配置放在 `open-claw/` 目录。

Agent 开发的参考资料（提示词模板、安全边界等）在 `skills/openclaw/` 中。

详见 [open-claw/README.md](open-claw/README.md)。

## 提交规范

### Commit 格式

```
<type>(<scope>): <description>
```

### Type

| type | 说明 |
|------|------|
| feat | 新增功能/内容 |
| fix | 修复问题 |
| docs | 仅文档变更 |
| refactor | 重构（不影响功能） |
| chore | 杂项（配置等） |

### Scope

| scope | 说明 |
|-------|------|
| global | global-settings 相关 |
| skill | skills 相关 |
| template | project-templates 相关 |
| openclaw | open-claw 相关 |
| command | commands 相关 |

### 示例

```bash
git commit -m "feat(skill): 添加 vue3-guide 技能包"
git commit -m "fix(global): 修复 CLAUDE.md 中 BaseDubboApi 路径错误"
git commit -m "docs(template): 更新 tzh-parkinglot 模板说明"
```

## 提交前检查清单

- [ ] 内容放在了正确的目录
- [ ] Skill 有 SKILL.md 且包含 frontmatter
- [ ] 更新了对应的 CATALOG.md 或 README.md 索引
- [ ] 文档使用中文
- [ ] Commit message 符合规范
