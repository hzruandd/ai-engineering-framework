# 全局配置

> 适用于所有 City Parking 项目的 Claude Code 全局配置。安装后对你机器上所有项目自动生效。

## 包含什么

```
global-settings/
└── .claude/
    ├── CLAUDE.md              # 核心规范（52KB，13 大模块）
    ├── commands/              # 10 个快捷命令
    ├── docs/                  # 18 个参考文档
    ├── ignore                 # 文件忽略规则
    ├── settings.local.json    # 本地设置（安装时跳过）
    └── analyze_slow_queries.py  # Doris 慢查询分析脚本
```

### CLAUDE.md — 核心规范

52KB 的全局开发规范，包含 13 大模块：

1. 编码前强制检查
2. 语言输出规范
3. 实体类规范
4. DubboApi/Controller 实现规范
5. Service 规范
6. Mapper 规范
7. 启动类规范
8. 日志规范
9. Redis 使用规范
10. 代码风格规范
11. SOLID 设计原则
12. 文档日期时间规范
13. 微服务分层架构规范

### commands/ — 快捷命令

| 命令 | 说明 | 使用场景 |
|------|------|----------|
| `/new-crud` | 创建完整 CRUD 功能 | 新建实体和增删改查 |
| `/add-field` | 为实体添加新字段 | 扩展已有实体 |
| `/new-api` | 在已有模块添加新接口 | 扩展 API 功能 |
| `/fix-cache` | 添加或修复缓存 | 性能优化 |
| `/deliver-requirement` | 端到端需求交付入口 | 需求到发布门禁 |
| `/review-code` | 代码审查清单 | 提测前自查 |
| `/diff-report` | 生成代码修改报告 | 提交前总结 |
| `/generate-tests` | 生成单元测试 | 测试覆盖 |
| `/formal-review` | 正式评审摘要格式化 | 面向管理层，裁决继承 tzh-review |
| `/design-doc` | 技术设计文档 | 方案设计 |
| `/analyze-slow-query` | Doris 慢查询分析 | 性能诊断 |

### docs/ — 参考文档

| 目录 | 内容 |
|------|------|
| architecture/ | 架构设计（缓存、Common 组件、分布式事务、线程池、链路追踪、MQ/MQTT） |
| design/ | 设计规范（前后端状态码规范） |
| examples/ | 实战案例（标准 CRUD、缓存使用、批量操作、复杂查询、分布式锁） |
| guides/ | 开发指南（编码前检查、详细规范、框架功能、SOLID 原则、配置指南） |

## 安装方法

```bash
# macOS / Linux
cp -r global-settings/.claude ~/

# Windows PowerShell
Copy-Item -Recurse -Force global-settings\.claude $env:USERPROFILE\.claude
```

### 验证

在任意项目中打开 Claude Code，输入：

```
请介绍一下 Java 的命名规范
```

如果回答了 PascalCase、camelCase 等规范 → 安装成功。

## 更新方法

```bash
# 1. 拉取最新代码
cd /path/to/city-parking-claude-doc
git pull

# 2. 同步全局配置
cp -r global-settings/.claude/* ~/.claude/
```

## 全局配置 vs 项目配置

| | 全局配置 | 项目配置 |
|---|---------|---------|
| 来源 | 本目录（global-settings/） | project-templates/ 中的模板 |
| 安装位置 | ~/.claude/ | 项目根目录/.claude/ + CLAUDE.md |
| 生效范围 | 所有项目 | 仅当前项目 |
| 内容 | 通用规范、命令、参考文档 | 项目专属规范、业务 Skills |
| 优先级 | 低 | 高（覆盖全局） |

两者不冲突。全局配置提供团队通用规范，项目配置提供项目专属上下文。当两者有矛盾时，项目配置优先。

## 注意事项

- `settings.local.json` 是个人偏好文件，安装时不会覆盖
- 不要直接修改 `~/.claude/CLAUDE.md`，应通过本仓库提交变更后同步
- 如需项目级自定义，请在项目根目录创建 CLAUDE.md 覆盖

---

**最后更新**：2026-04-08
