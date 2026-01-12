# Claude Settings - 团队 AI 辅助开发配置库

## 📖 项目简介

这是一个面向团队的 Claude Code 提示词工程，提供**全局通用编码规范**和**项目级配置模板**，帮助团队成员在使用 Claude Code 进行 AI 辅助开发时保持一致的代码质量和开发效率。

- **本提示词工程的特点**：
  - ✅ **持久化** - 将提示内容写入配置文件，长期生效，无需每次输入
  - ✅ **结构化** - 分层设计（全局/项目/Skills），自动在适当时机加载
  - ✅ **团队级** - 通过 Git 版本管理，团队共享统一的"AI 行为规范"
  - ✅ **工程化** - 提示词即代码（Prompt as Code），可维护、可迭代、可复用


这是一种**让 AI 辅助开发更加标准化、可控化的工程实践**。

## 🎯 背景与用途

### 为什么需要这个库？

在团队协作开发中，不同成员使用 AI 助手时可能会产生风格各异的代码。本配置库通过以下方式解决这一问题：

1. **统一编码规范**: 通过全局配置为 AI 提供团队级开发指南，确保生成的代码符合团队标准
2. **沉淀业务知识**: 通过项目配置将复杂业务逻辑文档化，让 AI 理解并正确处理核心业务
3. **提升开发效率**: 新成员通过配置文件即可让 AI 快速理解项目，减少上手时间
4. **持续优化**: 集中管理和迭代团队的 AI 使用最佳实践

### 适用场景

- 多人协作的 Java/Spring Boot 项目
- 需要统一代码风格和开发规范的团队
- 希望将复杂业务逻辑文档化并辅助 AI 理解的项目
- 需要快速培训新成员的团队

## 📂 目录结构

```
claude-settings/                                   # 配置库根目录
│
├── README.md                                      # 项目总体说明文档（本文件）
│
├── global-settings/                               # 全局通用配置（团队级）
│   ├── README.md                                  # 安装说明
│   └── .claude/                                   # 复制到 ~/.claude/
│       └── CLAUDE.md                              # 全局编码规范
│                                                  # 包含：Java/Spring Boot/数据库/Git 规范
│
└── project-templates/                             # 项目配置模板
    ├── README.md                                  # 模板使用说明
    │
    └── tzh-parkinglot/                           # 停车场项目模板（示例）
        ├── CLAUDE.md                              # 项目架构文档
        │                                          # 复制到项目根目录
        │
        └── .claude/                               # 项目级 Claude 配置
            ├── settings.local.json                # 本地设置（权限等）
            │
            └── skills/                            # 业务技能包
                └── parking-in-out/                # 停车场出入车业务
                    ├── SKILL.md                   # 技能描述和触发条件
                    │
                    └── reference/                 # 详细参考文档
                        ├── carInto方法详解.md
                        ├── appearanceProcessing方法详解.md
                        ├── devicePushInfo方法详解.md
                        ├── parkingCalculationFee方法详解.md
                        └── 代码修改最佳实践.md
```

### 配置生效范围

| 配置位置 | 生效范围 | 包含内容 |
|---------|---------|---------|
| `~/.claude/CLAUDE.md` | 所有项目 | 通用编码规范 |
| `项目根目录/CLAUDE.md` | 当前项目 | 项目架构、业务逻辑 |
| `项目根目录/.claude/skills/` | 当前项目 | 复杂业务场景文档 |

## 🚀 快速开始

### 第一步：安装全局配置（所有团队成员）

全局配置包含团队通用的编码规范，适用于所有项目。

```bash
# 1. 克隆配置库
git clone <repository-url> claude-settings
cd claude-settings

# 2. 复制全局配置到用户主目录
# macOS/Linux
cp -r global-settings/.claude ~/

# Windows
copy global-settings\.claude %USERPROFILE%\
```

**验证安装**：在任意项目中打开 Claude Code，询问：
```
请介绍一下 Java 的命名规范
```

如果 Claude 回答了 PascalCase、camelCase 等具体规范，说明全局配置已生效。

### 第二步：为项目添加专属配置（可选）

项目配置包含特定项目的架构、技术栈和业务逻辑文档。

```bash
# 1. 选择合适的模板（如 tzh-parkinglot）
cd project-templates/tzh-parkinglot

# 2. 复制到你的项目中
cp -r .claude /path/to/your-project/
cp CLAUDE.md /path/to/your-project/

# 3. 根据实际项目修改配置
cd /path/to/your-project
# 编辑 CLAUDE.md 和 .claude/skills/
```

**验证配置**：在项目中打开 Claude Code，询问：
```
请介绍一下这个项目的架构
```

如果 Claude 能准确回答项目的具体架构信息，说明项目配置已生效。

## 📋 两种配置的区别

| 配置类型 | 位置 | 作用范围 | 包含内容 | 使用场景 |
|---------|------|---------|---------|---------|
| **全局配置** | `~/.claude/` | 所有项目 | 通用编码规范、最佳实践 | 团队统一代码风格 |
| **项目配置** | 项目根目录 | 单个项目 | 项目架构、业务逻辑、Skills | 项目专属知识 |

### 全局配置（global-settings）

**内容**：
- Java/Spring Boot 编码规范
- 数据库开发规范
- Git 提交规范
- 性能优化要点
- 文档维护规范

**特点**：
- 一次安装，所有项目生效
- 团队成员保持一致
- 定期更新同步

### 项目配置（project-templates）

**内容**：
- 项目概述和模块结构
- 技术栈和架构模式
- 构建和运行命令
- 核心业务域文档
- Skills 业务技能包

**特点**：
- 每个项目独立配置
- 包含项目专属知识
- 复杂业务逻辑文档化

## 💡 使用场景示例

### 场景一：新成员入职

```bash
# 1. 安装全局配置（了解团队规范）
cp -r global-settings/.claude ~/

# 2. 拉取项目代码
git clone <project-repo>

# 3. 应用项目配置（如果项目中已包含）
# 项目中已有 CLAUDE.md 和 .claude/，直接使用

# 4. 开始开发，Claude 已了解团队规范和项目架构
```

### 场景二：启动新项目

```bash
# 1. 创建项目目录
mkdir new-project && cd new-project

# 2. 选择合适的模板
cp -r ../claude-settings/project-templates/tzh-parkinglot/.claude .
cp ../claude-settings/project-templates/tzh-parkinglot/CLAUDE.md .

# 3. 根据新项目修改配置
# 编辑 CLAUDE.md，更新项目信息
# 修改或删除 .claude/skills/ 中不需要的业务文档

# 4. 提交配置到项目仓库
git add CLAUDE.md .claude/
git commit -m "docs: 添加 Claude Code 配置"
```

### 场景三：日常开发

```bash
# 全局配置已安装，项目配置在项目中
# 直接使用 Claude Code 开发，AI 会：
# - 遵循团队编码规范（全局配置）
# - 理解项目架构和业务逻辑（项目配置）
# - 自动应用相关 Skills 处理复杂业务
```

## 🤝 贡献方式

欢迎所有团队成员参与完善配置库！

### 1. 优化全局规范

发现更好的编码实践 → 更新 `global-settings/.claude/CLAUDE.md`

```bash
cd global-settings
# 编辑 .claude/CLAUDE.md
git commit -m "docs(global): 更新 Java 异常处理规范"
```

### 2. 分享项目模板

为新项目类型创建配置模板 → 添加到 `project-templates/`

```bash
cd project-templates
mkdir my-new-project
# 创建 CLAUDE.md 和 .claude/
git commit -m "feat(template): 添加 Vue3 项目配置模板"
```

### 3. 完善业务文档

补充项目 Skills 业务逻辑 → 更新 `.claude/skills/`

```bash
# 在项目模板中
cd project-templates/tzh-parkinglot/.claude/skills/
# 添加或更新 reference/*.md
git commit -m "docs(parking): 补充月卡计费业务文档"
```

### 4. 报告问题

发现配置错误或过时内容 → 提 Issue 或直接修正

```bash
git commit -m "fix(global): 修正 MyBatis 配置示例错误"
```

### 提交规范

遵循 Git 提交规范（见全局配置）：

```bash
git commit -m "docs(global): 更新 Java 异常处理规范"
git commit -m "feat(template): 新增停车计费 skill 文档"
git commit -m "fix(readme): 修正安装路径说明"
```

## 📖 配置编写指南

### 全局配置（CLAUDE.md）应包含

- 核心开发原则（代码修改、质量、安全）
- 各语言编码规范（命名、格式、注释）
- 框架使用规范（Spring Boot、Vue 等）
- Git 提交规范
- 测试规范
- 性能优化要点
- 文档维护规范

参考：`global-settings/.claude/CLAUDE.md`

### 项目配置（CLAUDE.md）应包含

1. **项目概述**: 简要描述项目功能和定位
2. **模块结构**: 列出所有模块及其职责
3. **技术栈**: 框架版本、中间件、工具库
4. **架构模式**: 分层架构、服务通信方式
5. **构建命令**: Maven/Gradle 构建和运行命令
6. **配置说明**: 环境变量、配置文件位置
7. **核心业务域**: 关键业务流程和方法
8. **重要说明**: 安全注意事项、已知问题

参考：`project-templates/tzh-parkinglot/CLAUDE.md`

### Skills 技能包应包含

**SKILL.md**:
- 技能名称和描述
- 触发条件（何时使用该技能）
- 参考文档列表

**reference/ 详细文档**:
- 方法详解（参数、返回值、流程图）
- 业务规则说明
- 代码示例
- 常见陷阱和最佳实践

参考：`project-templates/tzh-parkinglot/.claude/skills/parking-in-out/`

## 🔧 最佳实践

### 1. 配置分层管理

- **全局配置**：团队通用规范，所有成员统一安装
- **项目配置**：项目专属知识，提交到项目仓库
- **Skills 文档**：复杂业务逻辑，按业务域组织

### 2. 保持文档与代码同步

**重要原则**：代码会过期，文档也会过期。

- 修改业务逻辑 → 更新 Skills 文档
- 调整项目架构 → 更新项目 CLAUDE.md
- 制定新规范 → 更新全局 CLAUDE.md

### 3. 适度文档化

并非所有代码都需要 Skills：

- **需要**：复杂业务流程、多步骤计算、易出错逻辑
- **不需要**：简单 CRUD、标准框架用法、通用工具方法

### 4. 定期更新全局配置

建议每季度 review 一次全局配置：

```bash
# 从仓库拉取最新配置
cd claude-settings
git pull

# 更新本地全局配置
cp -r global-settings/.claude ~/
```

## ❓ 常见问题

### Q: 全局配置和项目配置会冲突吗？

A: 不会。项目配置（项目根目录的 `CLAUDE.md`）优先级更高，会补充或覆盖全局配置。两者是互补关系。

### Q: 必须同时安装两种配置吗？

A: 不是。
- **只安装全局配置**：适用于简单项目，AI 会遵循团队编码规范
- **同时安装**：适用于复杂项目，AI 还能理解项目架构和业务逻辑

### Q: 项目配置需要提交到项目仓库吗？

A: 建议提交。这样所有团队成员拉取代码后，Claude Code 就能自动理解项目，无需额外配置。

### Q: 如何让新成员快速上手？

A:
1. 安装全局配置：`cp -r global-settings/.claude ~/`
2. 拉取项目代码（已包含项目配置）
3. 在 Claude Code 中直接询问项目相关问题

### Q: Skills 文档会自动生效吗？

A: 是的。当你在对话中提到相关业务（如"车辆入场"），Claude 会自动加载对应的 Skill 文档作为上下文。

### Q: 可以在项目中引用全局配置吗？

A: 可以，但不建议。因为：
- 全局配置在 `~/.claude/`，已自动生效
- 项目配置在项目根目录，专注于项目专属内容
- 两者分工明确，避免重复维护

## 📚 参考示例

### 全局配置示例

查看 `global-settings/.claude/CLAUDE.md`

包含：Java 规范、Spring Boot 规范、数据库规范、Git 规范等。

### 项目配置示例

查看 `project-templates/tzh-parkinglot/CLAUDE.md`

包含：项目架构、模块结构、技术栈、构建命令等。

### Skills 文档示例

查看 `project-templates/tzh-parkinglot/.claude/skills/parking-in-out/`

- `SKILL.md` - 技能描述和触发条件
- `reference/carInto方法详解.md` - 车辆入场方法详解
- `reference/parkingCalculationFee方法详解.md` - 停车计费方法详解
- `reference/代码修改最佳实践.md` - 修改建议和注意事项

## 🔮 后续计划

- [ ] 补充更多项目模板（Vue、Python、Go 等）
- [ ] 建立配置文件有效性检查脚本
- [ ] 整理常用 Skills 模板库
- [ ] 开发配置同步工具
- [ ] 建立团队最佳实践案例库

## 📝 更新历史

### v0.3.0 (2026-01-10)
- 重构目录结构，分离全局配置和项目模板
- 新增全局配置安装说明
- 完善项目模板使用指南
- 优化文档组织结构

### v0.2.0 (2026-01-10)
- 完善项目结构说明
- 新增详细使用方法
- 补充配置编写指南
- 优化贡献流程说明

### v0.1.0 (初版)
- 搭建基础框架
- 整理通用编码规范
- 创建停车场项目示例配置

## 💬 反馈与支持

如有任何问题或建议，欢迎：

- 提交 Issue 讨论
- 通过团队沟通渠道反馈
- 参加定期的经验分享会

---

**让 Claude Code 成为团队开发的得力助手！** 🚀
