# 变更记录

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

## [v1.1.0] - 2026-04-08

### Added
- 新增 QUICKSTART.md 快速开始指南
- 新增 CONTRIBUTING.md 贡献指南
- 新增 UPDATE.md 更新指南
- 新增 CHANGELOG.md 变更记录
- 新增 skills/README.md 和 skills/CATALOG.md 技能包索引
- 新增 project-templates/CATALOG.md 模板清单
- 新增 open-claw/README.md OpenClaw 平台说明
- 新增 MIGRATION_REPORT.md 改造报告

### Changed
- 重写 README.md，面向"用户 clone 后怎么用"
- 重写 STRUCTURE.md，反映实际磁盘结构
- 更新 global-settings/README.md，补充全局 vs 项目级说明
- 更新 project-templates/README.md，补充模板使用流程

### Removed
- 移除对不存在的 docs/、prompt-core/ 目录的引用

### Migration Notes
- 无破坏性变更。已安装全局配置的用户重新执行 `cp -r global-settings/.claude/* ~/.claude/` 即可更新。

## [v1.0.0] - 2026-04-04

### Added
- 新增 skills/openclaw/ Agent 开发参考资料（5 个参考文档）

### Changed
- 从 open-claw/ 迁移 Agent 开发资料到 skills/openclaw/

## [v0.3.0] - 2026-01-10

### Added
- 重构目录结构，分离全局配置和项目模板
- 新增全局配置安装说明
- 完善项目模板使用指南

## [v0.2.0] - 2026-01-10

### Added
- 完善项目结构说明
- 新增详细使用方法

## [v0.1.0] - 初版

### Added
- 搭建基础框架
- 整理通用编码规范
- 创建停车场项目示例配置
