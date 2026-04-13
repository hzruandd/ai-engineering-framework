# MySQL MCP Server

> MySQL 数据库连接 MCP Server，让 Claude Code 能够直接查询数据库、浏览表结构、分析数据。

## 概述

| 项目 | 信息 |
|------|------|
| 名称 | MySQL MCP |
| 包名 | `@benborla29/mcp-server-mysql` |
| 最新版本 | `2.0.8` |
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

- Node.js v20+（推荐 v20 或更高版本）
- MySQL 5.7+（推荐 MySQL 8.0+）
- MySQL 用户需要有相应的数据库权限

### 安装方式

#### 方式一：npx 模式（推荐 ⭐）

**无需安装，直接使用**，适合 Claude Code 用户。每次启动时自动拉取最新版本。

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

**优点**：
- ✅ 无需手动安装和更新
- ✅ 始终使用最新版本
- ✅ 配置简单，适合快速上手

**注意**：如果遇到 `Cannot find package 'dotenv'` 错误，使用以下配置：

```json
{
  "mcpServers": {
    "mysql": {
      "command": "npx",
      "args": ["-y", "-p", "@benborla29/mcp-server-mysql", "-p", "dotenv", "mcp-server-mysql"],
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

#### 方式二：全局安装

适合需要稳定版本或离线使用的场景。

```bash
# 全局安装
npm install -g @benborla29/mcp-server-mysql

# 查看安装路径
npm root -g
```

配置文件：

```json
{
  "mcpServers": {
    "mysql": {
      "command": "node",
      "args": [
        "/path/to/global/node_modules/@benborla29/mcp-server-mysql/dist/index.js"
      ],
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

#### 方式三：本地克隆（开发者模式）

适合需要修改源码或调试的场景。

```bash
# 克隆仓库
git clone https://github.com/benborla/mcp-server-mysql.git
cd mcp-server-mysql

# 安装依赖
npm install

# 构建
npm run build
```

配置文件：

```json
{
  "mcpServers": {
    "mysql": {
      "command": "node",
      "args": [
        "/full/path/to/mcp-server-mysql/dist/index.js"
      ],
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

### 基础配置（只读模式）

默认情况下，MCP Server 以只读模式运行，仅允许 SELECT 查询。

**推荐配置（npx 模式）**：

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

### Claude Code CLI 快捷配置

除了手动编辑 JSON 文件，也可以通过 `claude mcp` 命令快速配置：

```bash
# 添加 MCP Server（本地作用域，仅当前项目可用）
claude mcp add mysql \
  -e MYSQL_HOST="127.0.0.1" \
  -e MYSQL_PORT="3306" \
  -e MYSQL_USER="your_user" \
  -e MYSQL_PASS="your_password" \
  -e MYSQL_DB="your_database" \
  -- npx -y @benborla29/mcp-server-mysql

# 用户级作用域（所有项目可用）
claude mcp add mysql -s user \
  -e MYSQL_HOST="127.0.0.1" \
  -e MYSQL_PORT="3306" \
  -e MYSQL_USER="your_user" \
  -e MYSQL_PASS="your_password" \
  -e MYSQL_DB="your_database" \
  -- npx -y @benborla29/mcp-server-mysql
```

**作用域说明**：

| 作用域 | 说明 | 适用场景 |
|--------|------|----------|
| `local`（默认） | 仅当前项目可用 | 项目独立的数据库连接 |
| `user` (`-s user`) | 所有项目可用 | 个人常用数据库 |
| `project` (`-s project`) | 团队共享（写入 `.mcp.json`） | 团队统一配置 |

> **建议**：包含数据库密码的配置，推荐使用 `local` 或 `user` 作用域，避免密码泄露。

**验证安装**：

```bash
# 查看所有已配置的 MCP Server
claude mcp list

# 查看指定 Server 详情
claude mcp get mysql

# 在 Claude Code 中检查状态
/mcp
```

### 多数据库配置

#### 方式一：多实例配置

为不同数据库配置多个 MCP Server 实例：

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

#### 方式二：Multi-DB 模式

省略 `MYSQL_DB` 环境变量即可启用多数据库模式，允许查询用户有权限访问的所有数据库：

```json
{
  "mcpServers": {
    "mysql-multi": {
      "command": "npx",
      "args": ["-y", "@benborla29/mcp-server-mysql"],
      "env": {
        "MYSQL_HOST": "127.0.0.1",
        "MYSQL_PORT": "3306",
        "MYSQL_USER": "your_user",
        "MYSQL_PASS": "your_password",
        "MULTI_DB_WRITE_MODE": "false"
      }
    }
  }
}
```

Multi-DB 模式下查询需要使用完整表名：

```sql
-- 使用完整限定名
SELECT * FROM database_name.table_name;

-- 或使用 USE 切换数据库
USE database_name;
SELECT * FROM table_name;
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
    "ALLOW_DELETE_OPERATION": "true",
    "ALLOW_DDL_OPERATION": "true"
  }
}
```

> **警告**：仅在开发环境开启写入权限，切勿在生产环境使用！

### Schema 级别权限控制

对不同数据库设置不同的操作权限：

```json
{
  "env": {
    "SCHEMA_INSERT_PERMISSIONS": "development:true,test:true,production:false",
    "SCHEMA_UPDATE_PERMISSIONS": "development:true,test:true,production:false",
    "SCHEMA_DELETE_PERMISSIONS": "development:false,test:true,production:false",
    "SCHEMA_DDL_PERMISSIONS": "development:false,test:true,production:false"
  }
}
```

## 环境变量参考

### 基础连接

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `MYSQL_HOST` | `127.0.0.1` | MySQL 服务器地址 |
| `MYSQL_PORT` | `3306` | MySQL 端口 |
| `MYSQL_USER` | `root` | 用户名 |
| `MYSQL_PASS` | - | 密码 |
| `MYSQL_DB` | - | 数据库名（空则为 Multi-DB 模式） |
| `MYSQL_SOCKET_PATH` | - | Unix Socket 路径（设置后忽略 HOST/PORT） |
| `MYSQL_CONNECTION_STRING` | - | MySQL 连接字符串（设置后优先于单独配置） |

### 性能配置

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `MYSQL_POOL_SIZE` | `10` | 连接池大小 |
| `MYSQL_QUERY_TIMEOUT` | `30000` | 查询超时（毫秒） |
| `MYSQL_CACHE_TTL` | `60000` | 缓存有效期（毫秒） |
| `MYSQL_QUEUE_LIMIT` | `100` | 最大排队连接请求数 |
| `MYSQL_CONNECT_TIMEOUT` | `10000` | 连接超时（毫秒） |

### 安全配置

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `MYSQL_RATE_LIMIT` | `100` | 每分钟最大查询数 |
| `MYSQL_MAX_QUERY_COMPLEXITY` | `1000` | 查询复杂度上限 |
| `MYSQL_SSL` | `false` | 启用 SSL/TLS 加密连接 |
| `ALLOW_INSERT_OPERATION` | `false` | 允许 INSERT 操作 |
| `ALLOW_UPDATE_OPERATION` | `false` | 允许 UPDATE 操作 |
| `ALLOW_DELETE_OPERATION` | `false` | 允许 DELETE 操作 |
| `ALLOW_DDL_OPERATION` | `false` | 允许 DDL 操作（CREATE/ALTER/DROP） |
| `MYSQL_DISABLE_READ_ONLY_TRANSACTIONS` | `false` | 禁用只读事务（⚠️ 慎用） |
| `MULTI_DB_WRITE_MODE` | `false` | Multi-DB 模式下启用写入 |

### 时区配置

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `MYSQL_TIMEZONE` | - | 时区设置（如 `+08:00`、`-05:00`、`Z`、`local`） |
| `MYSQL_DATE_STRINGS` | `false` | 将日期返回为字符串，避免 JS Date 转换 |

### 监控配置

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `MYSQL_ENABLE_LOGGING` | `false` | 启用查询日志 |
| `MYSQL_LOG_LEVEL` | `info` | 日志级别 |
| `MYSQL_METRICS_ENABLED` | `false` | 启用性能指标 |

### 远程 MCP 模式

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `IS_REMOTE_MCP` | `false` | 启用远程模式 |
| `REMOTE_SECRET_KEY` | - | 远程认证密钥 |
| `PORT` | `3000` | 远程模式端口 |

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
- **Multi-DB 模式**：支持同时访问多个数据库
- **Schema 级权限**：不同数据库可设置不同的读写权限
- **远程模式**：支持以远程 MCP 方式运行，多客户端共享
- **DDL 支持**：可选开启 CREATE TABLE 等 DDL 操作
- **查询缓存**：内置查询结果缓存机制
- **速率限制**：可配置查询频率限制
- **SQL 注入防护**：预编译语句防止 SQL 注入

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

## 常见问题排查

### 1. 无法连接 MCP Server

```bash
# 检查 Server 状态
claude mcp list

# 直接测试 Server 是否正常启动
npx @benborla29/mcp-server-mysql
```

### 2. 路径问题（找不到 Node）

在配置中显式设置 PATH：

```json
{
  "env": {
    "PATH": "/path/to/node/bin:/usr/bin:/bin"
  }
}
```

查找 Node 路径：

```bash
# 获取 Node 路径
which node

# 获取 PATH 值
echo "$(which node)/../"

# 获取 NODE_PATH 值
echo "$(which node)/../../lib/node_modules"
```

### 3. MySQL 8.0 认证问题

如果遇到认证失败，尝试使用传统认证方式：

```sql
CREATE USER 'user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
```

### 4. dotenv 模块找不到

使用以下 npx 参数解决：

```json
{
  "args": ["-y", "-p", "@benborla29/mcp-server-mysql", "-p", "dotenv", "mcp-server-mysql"]
}
```

## 注意事项

- **安全第一**：不要在配置文件中存放生产环境密码，建议使用环境变量
- **只读优先**：默认只读模式，仅在开发环境按需开启写入
- **敏感数据**：查询结果可能包含敏感数据，注意信息脱敏
- **配置文件安全**：`settings.local.json` 包含数据库密码，确保已在 `.gitignore` 中排除
- **连接数限制**：注意数据库连接数上限，避免频繁重启 MCP Server
