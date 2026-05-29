# 更新指南

## 标准更新流程

### 1. 拉取最新代码

```bash
cd /path/to/city-parking-claude-doc
git pull origin master
```

### 2. 同步全局配置

```bash
# macOS / Linux
cp -r global-settings/.claude/* ~/.claude/

# Windows PowerShell
Copy-Item -Recurse -Force global-settings\.claude\* $env:USERPROFILE\.claude\
```

### 3. 同步项目配置（如有）

如果你的项目使用了项目模板，且模板有更新，手动对比后复制：

```bash
# 对比差异
diff /path/to/your-project/CLAUDE.md project-templates/tzh-parkinglot/CLAUDE.md

# 如需更新 Skills
cp -r project-templates/tzh-parkinglot/.claude/skills/* /path/to/your-project/.claude/skills/
```

## 哪些文件会被同步，哪些不会

### 受仓库管理的文件（同步时会覆盖）

| 文件 | 说明 |
|------|------|
| ~/.claude/CLAUDE.md | 全局核心规范 |
| ~/.claude/commands/*.md | 全局快捷命令 |
| ~/.claude/docs/**/*.md | 全局参考文档 |
| ~/.claude/ignore | 忽略规则 |

**这些文件不建议直接修改**。如果你有自定义需求，请通过项目级配置覆盖。

### 允许本地自定义的文件（同步时不会覆盖）

| 文件 | 说明 |
|------|------|
| ~/.claude/settings.local.json | 个人偏好设置 |
| 项目根目录/CLAUDE.md | 项目级配置（优先级高于全局） |
| 项目根目录/.claude/skills/ | 项目专用 Skills |

**自定义方式**：
- 想修改全局规范中的某条规则？→ 在项目 CLAUDE.md 中覆盖
- 想添加项目专用命令？→ 放在项目 `.claude/commands/` 下
- 想添加项目专用 Skill？→ 放在项目 `.claude/skills/` 下

### 全局 vs 项目级的覆盖关系

```
全局 ~/.claude/CLAUDE.md        ← 团队统一规范（受仓库管理）
  ↓ 被覆盖
项目 /your-project/CLAUDE.md    ← 项目专属规范（你自己维护）
  ↓ 叠加
项目 .claude/skills/            ← 项目专用 Skills（你自己维护）
```

## 冲突处理

### 场景一：全局配置冲突

如果你直接修改过 `~/.claude/CLAUDE.md`，同步时会被覆盖。

**建议**：不要直接改全局文件。把自定义内容放在项目级 CLAUDE.md 中。

**如果已经改了**：
1. 备份你的修改：`cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.bak`
2. 执行同步
3. 把你的自定义内容迁移到项目级 CLAUDE.md

### 场景二：Git 仓库冲突

```bash
git pull origin master
# 如果有冲突
git status                    # 查看冲突文件
# 手动解决冲突后
git add .
git commit -m "merge: 解决配置更新冲突"
```

## 更新频率建议

- **全局配置**：团队通知有更新时同步，或每周一次
- **项目模板**：项目架构变更时同步
- **Skills**：Skills 会随仓库更新自动可用，无需额外操作
