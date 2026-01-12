# 全局通用配置

此目录包含适用于所有项目的 Claude Code 全局配置。

## 安装方法

将 `.claude` 目录复制到你的用户主目录：

```bash
# macOS/Linux
cp -r .claude ~/

# Windows
copy .claude %USERPROFILE%\
```

## 文件说明

### `.claude/CLAUDE.md`

全局通用的开发规约和编码规范，包括：

- **核心开发原则**：代码修改原则、代码质量原则、安全原则
- **Java 开发规范**：命名、注释、格式、异常处理、空值处理等
- **数据库开发规范**：SQL 编写、MyBatis Mapper、字段命名
- **Spring Boot 开发规范**：依赖注入、Controller、Service 等
- **前端开发规范**：Vue/TypeScript 命名和最佳实践
- **Git 提交规范**：提交格式和类型
- **测试规范**：单元测试编写规范
- **性能优化要点**：数据库和代码优化建议
- **文档维护规范**：何时更新文档、文档质量标准

## 配置生效验证

安装后，在任意项目中打开 Claude Code，询问：

```
请介绍一下 Java 的命名规范
```

如果 Claude 回答了与 `CLAUDE.md` 中一致的规范（如 PascalCase、camelCase 等），说明全局配置已生效。

## 注意事项

- 全局配置会对所有项目生效
- 项目级配置（项目根目录的 `CLAUDE.md`）会覆盖全局配置
- 建议定期更新此配置以保持与团队最新规范同步
