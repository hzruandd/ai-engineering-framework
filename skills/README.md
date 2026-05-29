# Skills 技能包

本目录包含 22 个可复用的 Claude Code 技能包，以及 OpenClaw Agent 开发参考资料。

## 什么是 Skill

Skill 是 Claude Code 的能力扩展包。每个 Skill 包含一个 `SKILL.md` 文件，定义了触发条件和专业知识。当对话匹配触发条件时，Skill 会自动加载。

## 如何使用

### 安装到全局（所有项目可用）

```bash
cp -r skills/<skill-name> ~/.claude/skills/
```

### 安装到特定项目

```bash
cp -r skills/<skill-name> /path/to/project/.claude/skills/
```

### 批量安装

```bash
# 安装所有 skills
cp -r skills/* ~/.claude/skills/

# 安装某一类（如工程研发类）
for s in java-guide new-crud add-field new-api fix-cache; do
  cp -r skills/$s ~/.claude/skills/
done
```

## 技能包分类

详细清单见 [CATALOG.md](CATALOG.md)。

| 分类 | 数量 | 包含 |
|------|------|------|
| 工程研发 | 7 | java-guide, new-crud, add-field, new-api, fix-cache, mcp-builder, frontend-design |
| 质量保障 | 5 | review-code, diff-report, generate-tests, self-test, webapp-testing |
| 文档工具 | 5 | pdf, pptx, docx, xlsx, doc-coauthoring |
| 设计创意 | 3 | canvas-design, algorithmic-art, theme-factory |
| 元技能 | 2 | skill-creator, thinking-guide |

另外，`openclaw/` 目录存放 OpenClaw Agent 开发参考资料，不是 Claude Code Skill。

## 如何贡献新 Skill

见 [CONTRIBUTING.md](../CONTRIBUTING.md)。
