# 项目配置模板

> 项目级 Claude 配置模板。复制到你的项目中，让 Claude Code 了解项目的架构和业务。

## 可用模板

详见 [CATALOG.md](CATALOG.md)。

| 模板 | 适用项目 | 技术栈 |
|------|----------|--------|
| [tzh-parkinglot](tzh-parkinglot/) | 停车场管理系统 | Spring Boot + Dubbo + MyBatis + MySQL + Nacos |

## 使用方法

### 1. 选择模板

根据你的项目技术栈选择最接近的模板。

### 2. 复制到项目

```bash
# 复制配置到项目
cp -r project-templates/tzh-parkinglot/.claude /path/to/your-project/
cp project-templates/tzh-parkinglot/CLAUDE.md /path/to/your-project/

# 删除 settings.local.json（会自动生成）
rm /path/to/your-project/.claude/settings.local.json
```

### 3. 自定义

编辑项目根目录的 `CLAUDE.md`，根据实际项目修改：

- 项目名称和概述
- 模块结构
- 技术栈版本
- 构建命令
- 核心业务域
- 删除不需要的 Skills，添加项目特有的业务文档

### 4. 验证

在项目中打开 Claude Code，输入：

```
请介绍一下这个项目的架构
```

如果 Claude 能准确回答你项目的具体架构信息 → 配置已生效。

## 全局配置 vs 项目配置

- **全局配置**（`global-settings/`）：安装到 `~/.claude/`，对所有项目生效
- **项目配置**（本目录的模板）：复制到项目根目录，仅该项目生效
- **优先级**：项目级 > 全局级

两者不冲突。建议先安装全局配置，再按需初始化项目配置。

## 创建新模板

详见 [CONTRIBUTING.md](../CONTRIBUTING.md)。

基本步骤：

1. 创建目录：`mkdir -p project-templates/<project-name>/.claude/skills`
2. 编写 `CLAUDE.md`（项目概述、模块结构、技术栈、构建命令）
3. 添加项目专用 Skills（可选）
4. 在 [CATALOG.md](CATALOG.md) 中添加条目
5. 提交 PR

---

**最后更新**：2026-04-08
