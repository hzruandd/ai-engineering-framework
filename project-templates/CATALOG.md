# 项目模板清单

> 项目级 Claude 配置模板。复制到你的项目中，让 Claude Code 了解项目的架构和规范。

## 可用模板

| 模板 | 适用项目 | 技术栈 | 包含 Skills |
|------|----------|--------|-------------|
| [tzh-parkinglot](tzh-parkinglot/) | 停车场管理系统 | Spring Boot + Dubbo + MyBatis + MySQL | parking-in-out（出入车业务） |

## 使用方法

### 1. 选择模板

根据你的项目技术栈选择最接近的模板。

### 2. 复制到项目

```bash
# 复制到项目
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

## 创建新模板

详见 [CONTRIBUTING.md](../CONTRIBUTING.md)。

基本步骤：
1. `mkdir -p project-templates/<project-name>/.claude/skills`
2. 编写 `CLAUDE.md`（项目概述、模块结构、技术栈、构建命令）
3. 添加项目专用 Skills（可选）
4. 在本文件中添加条目
5. 提交 PR
