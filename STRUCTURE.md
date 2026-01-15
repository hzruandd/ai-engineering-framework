# 目录结构说明

本仓库用于管理 City Parking 项目的 Claude Code 配置文件和文档。

## 目录结构

```
city-parking-claude-doc/
├── README.md                    # 项目总体说明
├── STRUCTURE.md                 # 本文件，目录结构说明
├── global-settings/             # 全局通用配置
│   ├── README.md                # 全局配置说明
│   └── .claude/                 # Claude 全局配置文件
│       ├── CLAUDE.md            # 项目级规范（完整版）
│       ├── commands/            # 自定义快捷命令
│       ├── docs/                # 详细文档
│       │   ├── architecture/    # 架构设计文档
│       │   ├── design/          # 设计规范
│       │   ├── examples/        # 实战案例
│       │   └── guides/          # 开发指南
│       ├── ignore               # 忽略文件配置
│       ├── settings.local.json  # 本地设置
│       ├── README.md            # .claude目录说明
│       └── analyze_slow_queries.py  # Doris慢查询分析工具
└── project-templates/           # 项目模板
    ├── README.md                # 模板说明
    └── tzh-parkinglot/          # 停车场项目模板
        └── .claude/             # 项目特定配置
            ├── CLAUDE.md        # 项目级配置
            └── skills/          # 业务技能文档

## 使用说明

### 1. 全局配置（global-settings）

**用途**：所有 City Parking 微服务项目通用的开发规范和规则

**包含内容**：
- 编码规范（Java、数据库、前端等）
- 框架核心规范（Spring Boot、Dubbo、MyBatis Plus）
- 设计原则（SOLID）
- 架构设计文档
- 开发指南和最佳实践
- 自定义快捷命令（/new-crud、/add-field 等）

**如何使用**：
```bash
# 方式1：复制到 ~/.claude/（全局生效）
cp -r global-settings/.claude/* ~/.claude/

# 方式2：复制到具体项目（项目级生效）
cp -r global-settings/.claude /path/to/your/project/
```

### 2. 项目模板（project-templates）

**用途**：特定业务项目的配置模板

**包含内容**：
- 项目特定的业务规范
- Skills 技能文档（业务流程、方法索引）
- 项目级的 CLAUDE.md 配置

**如何使用**：
```bash
# 复制模板到新项目
cp -r project-templates/tzh-parkinglot/.claude /path/to/new/project/

# 根据实际业务修改配置
cd /path/to/new/project/.claude
# 编辑 CLAUDE.md 和 skills 文档
```

## 配置优先级

Claude Code 读取配置的优先级（从高到低）：

1. **项目级配置**：项目根目录的 `.claude/CLAUDE.md`
2. **全局配置**：`~/.claude/CLAUDE.md`

**推荐策略**：
- 通用规范放在全局配置（`~/.claude/`）
- 项目特定规范放在项目配置（项目根目录的 `.claude/`）

## 文件说明

### 核心配置文件

| 文件 | 说明 |
|------|------|
| `CLAUDE.md` | Claude Code 的主配置文件，定义开发规范和约束 |
| `ignore` | 指定 Claude Code 应该忽略的文件和目录 |
| `settings.local.json` | 本地设置（如模型选择、代理配置） |

### 文档目录

| 目录 | 说明 |
|------|------|
| `docs/architecture/` | 架构设计文档（缓存、分布式事务、线程池等） |
| `docs/design/` | 设计规范（状态码规范等） |
| `docs/examples/` | 实战案例（CRUD、缓存、批量操作等） |
| `docs/guides/` | 开发指南（编码前检查、详细规范等） |
| `commands/` | 自定义快捷命令（/new-crud、/add-field 等） |
| `skills/` | 业务技能文档（项目特定） |

## 维护指南

### 更新全局配置

当需要更新通用规范时：
1. 修改 `global-settings/.claude/CLAUDE.md` 或相关文档
2. 提交到 Git 仓库
3. 通知团队成员更新本地配置：
   ```bash
   git pull
   cp -r global-settings/.claude/* ~/.claude/
   ```

### 创建新项目模板

当需要为新业务线创建模板时：
1. 在 `project-templates/` 下创建新目录
2. 复制并修改 `tzh-parkinglot` 模板
3. 编写项目特定的 CLAUDE.md 和 skills 文档
4. 更新 `project-templates/README.md`

### 文档维护原则

**核心原则**：代码和文档同步更新

**何时必须更新文档**：
- 业务逻辑变更 → 更新 skills reference 文档
- 代码结构变更 → 更新方法索引和位置
- 配置规则变更 → 更新配置说明
- 框架升级 → 更新 CLAUDE.md 架构说明

详见：[文档维护规范](global-settings/.claude/CLAUDE.md#文档维护规范)

## 相关链接

- [全局配置说明](global-settings/README.md)
- [项目模板说明](project-templates/README.md)
- [City Parking 框架核心规范](global-settings/.claude/CLAUDE.md)
- [Claude Code 官方文档](https://docs.anthropic.com/claude/docs)

## 版本历史

- **2025-01-13**：合并 `.claude` 和 `claude-settings` 目录，统一为新结构
- **2025-01-12**：初始版本

## 联系方式

如有问题或建议，请联系架构组。
