# 项目配置模板

此目录包含不同项目的 Claude Code 配置模板，可以复制到实际项目中使用。

## 可用模板

### tzh-parkinglot - 停车场管理系统

Spring Boot + Dubbo 微服务架构的停车场管理系统配置模板。

**适用场景**：
- Spring Boot 2.x 项目
- Dubbo 微服务架构
- MyBatis + MySQL 数据栈
- Nacos 服务发现和配置管理

**包含内容**：
- 项目架构说明
- 模块结构介绍
- 技术栈配置
- 构建和运行命令
- 核心业务域文档
- Skills 业务技能包（停车场出入车业务）

## 使用方法

### 1. 选择合适的模板

根据你的项目技术栈选择最接近的模板。

### 2. 复制到项目中

```bash
# 复制整个配置目录到你的项目
cp -r tzh-parkinglot/.claude /path/to/your-project/
cp tzh-parkinglot/CLAUDE.md /path/to/your-project/
```

### 3. 自定义配置

编辑 `CLAUDE.md` 和 `.claude/skills/`，根据实际项目情况修改：

- 项目名称和概述
- 模块结构
- 技术栈版本
- 构建命令
- 核心业务域
- 删除不需要的 Skills，添加项目特有的业务文档

### 4. 验证配置

在项目中打开 Claude Code，询问：

```
请介绍一下这个项目的架构
```

如果 Claude 能准确回答你项目的具体架构信息，说明配置已生效。

## 创建新模板

如果现有模板都不适合你的项目，可以创建新模板：

### 1. 创建目录结构

```bash
mkdir -p project-templates/your-project-name/.claude/skills
```

### 2. 编写 CLAUDE.md

参考现有模板，包含以下章节：

```markdown
# 项目概述
# 模块结构
# 技术栈
# 架构模式
# 构建和运行命令
# 配置
# 核心业务域
# 重要说明
# 文档维护指南
```

### 3. 创建 Skills（可选）

对于复杂业务逻辑，创建 Skills 文档：

```bash
mkdir -p .claude/skills/your-skill-name/reference
```

编写：
- `SKILL.md` - 技能描述和触发条件
- `reference/*.md` - 详细业务文档

### 4. 提交模板

完成后，提交 PR 分享给团队：

```bash
git add project-templates/your-project-name
git commit -m "feat(template): 添加 xxx 项目配置模板"
git push
```

## 模板维护

- 当项目架构或技术栈变更时，及时更新对应模板
- 发现通用的优化方案，回馈到模板中
- 定期 review 模板内容，确保准确性和时效性
