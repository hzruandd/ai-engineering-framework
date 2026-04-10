# MySQL MCP Server

> MySQL 数据库连接 MCP Server，让 Claude Code 能够直接查询数据库、浏览表结构、分析数据。

## 概述

| 项目 | 信息 |
|------|------|
| 名称 | MySQL MCP |
| 包名 | `@benborla29/mcp-server-mysql` |
| 来源 | 社区维护 |
| 仓库 | [benborla/mcp-server-mysql](https://github.com/benborla/mcp-server-mysql) |
| 运行方式 | 本地运行，默认只读模式 |

## 用途

MySQL MCP 为 Claude Code 提供数据库交互能力，适用于：

- **表结构浏览**：快速了解数据库 Schema、字段类型、索引
- **数据查询**：执行 SQL 查询，分析业务数据
- **问题排查**：查看数据状态，辅助定位 Bug
- **SQL 辅助**：让 Claude 根据表结构生成正确的 SQL
- **数据库设计**：对比现有表结构，辅助新表设计

## 安装配置

### 前置条件

- Node.js v18+
- MySQL 数据库实例（可访问的连接信息）

### 基础配置（只读模式）

在 `~/.claude/settings.json`（全局）或项目 `.claude/settings.local.json` 中添加：

```json
{
  "mcpServers": {
    "mysql": {
      "command": "npx",
      "args": ["-y", "@benborla29/mcp-server-mysql"],
      "env": {
        "MYSQL_HOST": "127.0.0.1",
        "MYSQL_PORT": "3306",
        "MYSQL_USER": "your_user",
        "MYSQL_PASS": "your_password",
        "MYSQL_DB": "your_database"
      }
    }
  }
}
```

### 多数据库配置

如需连接多个数据库，配置多个 MCP Server 实例：

```json
{
  "mcpServers": {
    "mysql-dev": {
      "command": "npx",
      "args": ["-y", "@benborla29/mcp-server-mysql"],
      "env": {
        "MYSQL_HOST": "127.0.0.1",
        "MYSQL_PORT": "3306",
        "MYSQL_USER": "dev_user",
        "MYSQL_PASS": "dev_password",
        "MYSQL_DB": "parking_dev"
      }
    },
    "mysql-test": {
      "command": "npx",
      "args": ["-y", "@benborla29/mcp-server-mysql"],
      "env": {
        "MYSQL_HOST": "172.26.145.149",
        "MYSQL_PORT": "3306",
        "MYSQL_USER": "test_user",
        "MYSQL_PASS": "test_password",
        "MYSQL_DB": "parking_test"
      }
    }
  }
}
```

### 开启写入权限（谨慎）

默认只读。如需写入，添加以下环境变量：

```json
{
  "env": {
    "MYSQL_HOST": "127.0.0.1",
    "MYSQL_PORT": "3306",
    "MYSQL_USER": "your_user",
    "MYSQL_PASS": "your_password",
    "MYSQL_DB": "your_database",
    "ALLOW_INSERT_OPERATION": "true",
    "ALLOW_UPDATE_OPERATION": "true",
    "ALLOW_DELETE_OPERATION": "true"
  }
}
```

> **警告**：仅在开发环境开启写入权限，切勿在生产环境使用！

## 主要功能

| 工具 | 说明 |
|------|------|
| `mysql_query` | 执行 SQL 查询语句 |

### 功能特点

- **默认只读**：安全第一，防止误操作
- **Schema 浏览**：通过 SQL 查看表结构、索引、约束
- **连接池**：内置连接池管理，性能稳定
- **SSL 支持**：支持加密连接
- **SSH 隧道**：支持通过 SSH 隧道连接远程数据库

## 使用示例

安装配置后，在 Claude Code 中可以直接说：

- "查看 parking_order 表的结构"
- "查一下最近 7 天的订单数据统计"
- "这张表有哪些索引？是否需要优化？"
- "帮我根据这个表结构生成 Entity 类"
- "对比 sys_user 和 sys_role 表的关联关系"

### 常用 SQL 示例

```sql
-- 查看所有表
SHOW TABLES;

-- 查看表结构
DESC parking_order;

-- 查看建表语句（含索引、约束）
SHOW CREATE TABLE parking_order;

-- 查看表数据量
SELECT TABLE_NAME, TABLE_ROWS
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = DATABASE()
ORDER BY TABLE_ROWS DESC;
```

## 注意事项

- **安全第一**：不要在配置文件中存放生产环境密码，建议使用环境变量
- **只读优先**：默认只读模式，仅在开发环境按需开启写入
- **敏感数据**：查询结果可能包含敏感数据，注意信息脱敏
- **配置文件安全**：`settings.local.json` 包含数据库密码，确保已在 `.gitignore` 中排除
- **连接数限制**：注意数据库连接数上限，避免频繁重启 MCP Server
