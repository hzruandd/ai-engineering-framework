# AI Coding 数据库工程化 Phase 1-7 总结与使用指南

> **文档版本**：v1.0  
> **生成时间**：2026-07-28  
> **适用项目**：city-parking 智慧停车微服务框架  
> **技术基线**：PolarDB MySQL 8.x / MyBatis-Plus 3.5.7

---

## 一、整体概述

### 1.1 项目背景

本轮 Phase 1-7 整改，旨在构建完整的**数据库工程化能力链路**，让 AI 在代码生成阶段就具备：

- ✅ **正向设计能力**：需求 → 访问模式 → SQL → 索引 → 表结构
- ✅ **性能分析能力**：SQL Review、执行计划分析、索引优化
- ✅ **生产治理能力**：PolarDB 慢 SQL 分析、大表 DDL 评估
- ✅ **规范一致性**：所有数据库规则收敛至唯一事实源

### 1.2 核心原则

**业务场景驱动数据库设计**（最高原则）：

```
业务场景
   ↓
访问模式（谁、在什么条件下、以什么频率读写）
   ↓
SQL（具体的 WHERE / JOIN / ORDER BY / GROUP BY / 分页）
   ↓
索引（支撑上述 SQL 的最优索引）
   ↓
表结构（字段类型、主键、约束）
```

**禁止先建表、后补索引。**

---

## 二、Phase 1-7 主要变更

### Phase 1-2：建设数据库规范底座

**新增文件**：
```
global-settings/.claude/docs/guides/database-engineering-standard.md
```

**改造文件**：
```
skills/new-crud/SKILL.md
skills/new-api/SKILL.md
skills/add-field/SKILL.md
```

**核心能力**：
- ✅ 建立数据库规范唯一事实源（Single Source of Truth）
- ✅ 三大生成 Skill（new-crud、new-api、add-field）全部接入规范
- ✅ 主键双轨策略：新表 bigint、存量 varchar(64) 不动
- ✅ 字段类型、索引设计、SQL 硬规则全部标准化

---

### Phase 3：新增数据库设计 Skill

**新增文件**：
```
skills/database-schema-design/SKILL.md
skills/database-schema-design/examples/parking-order-example.md
```

**核心能力**：
- ✅ AI 主动完成数据库设计（而非被动生成代码）
- ✅ 输出：业务模型分析 → 访问模式分析 → SQL 设计 → 索引设计 → DDL → 容量评估
- ✅ 强制正向设计流程：场景 → SQL → 索引 → 表结构
- ✅ 包含智慧停车订单表设计完整示例

**适用场景**：
- 新业务开发前的数据库设计
- 新模块设计
- 重要表结构设计
- 需要详细设计文档的场景

---

### Phase 4：新增 SQL 性能分析 Skill

**新增文件**：
```
skills/sql-performance-review/SKILL.md
skills/sql-performance-review/examples/parking_record_new-like-issue.md
skills/sql-performance-review/examples/parking_lot_statistics-function-issue.md
```

**核心能力**：
- ✅ SQL 性能专项分析能力
- ✅ 执行计划深度分析（type、key、rows、Extra）
- ✅ 内置 SQL 反模式检查（SELECT *、函数包字段、LIKE 前置%、深分页等）
- ✅ 沉淀真实生产案例（车牌查询 LIKE、DATE_FORMAT 索引失效）

**适用场景**：
- SQL Review
- 慢 SQL 分析
- SQL 优化
- 索引优化
- 执行计划分析

---

### Phase 5：增强 Review 能力

**修改文件**：
```
skills/tzh-review/checklists/db-sql-review.md
```

**核心能力**：
- ✅ 数据库 Review 能力升级为：数据库设计 + SQL + 索引 + PolarDB 适配
- ✅ 新增检查维度：
  - 数据库设计检查（表设计、字段设计、主键设计）
  - 索引设计检查（查询驱动、联合索引、索引冗余、索引滥用）
  - SQL 性能检查（查询问题、索引失效、模糊查询、分页问题、写操作风险）
  - PolarDB 专项检查（索引结构、大表风险、在线变更、读写分离）
- ✅ 风险分级：P0（阻断上线）、P1（上线风险）、P2（优化建议）

**适用场景**：
- 代码 Review
- 数据库设计 Review
- 上线前质量门禁

---

### Phase 6：新增 PolarDB 慢 SQL 分析命令

**新增文件**：
```
commands/analyze-polardb-slow-query.md
global-settings/.claude/commands/analyze-polardb-slow-query.md
```

**核心能力**：
- ✅ 线上生产环境 PolarDB 慢 SQL 治理入口
- ✅ 支持输入：Slow Log、SQL、表结构、EXPLAIN
- ✅ 输出：TOP 慢 SQL 概览、问题分类、执行计划分析、SQL 优化建议、索引优化方案、收益评估
- ✅ 内置真实案例（parking_record_new、parking_lot_statistics）

**适用场景**：
- 线上慢 SQL 治理
- SQL 性能排查
- 索引优化分析
- 查询性能评估

**调用关系**：
```
analyze-polardb-slow-query
        ↓
sql-performance-review Skill
        ↓
database-engineering-standard
```

---

### Phase 7：补齐 PolarDB 专项规范

**修改文件**：
```
global-settings/.claude/docs/guides/database-engineering-standard.md
```

**核心能力**：
- ✅ 新增第 8 章：PolarDB/MySQL 专项规范
  - InnoDB 存储结构（聚簇索引、二级索引）
  - 主键设计与性能影响
  - Buffer Pool、Redo Log、Undo Log 与 MVCC
  - 大表治理规范（分区、冷热数据）
  - 在线 DDL 规范
  - 读写分离规范
  - HTAP / 列存索引适用场景
- ✅ 新增 PolarDB 设计自检清单
- ✅ 所有相关 Skill 同步引用

**适用场景**：
- PolarDB 数据库设计
- 大表治理
- 在线 DDL 评估
- 读写分离架构设计

---

## 三、使用说明

### 3.1 快速开始

#### 场景 1：新建业务模块（需要数据库设计）

**推荐流程**：

```bash
# 1. 先做数据库设计（Phase 3）
/database-schema-design 停车订单模块

# AI 会输出：
# - 业务模型分析
# - 访问模式分析（关键！）
# - SQL 设计
# - 索引设计（每个索引说明支撑哪个查询）
# - DDL
# - 容量评估

# 2. 确认设计后，生成 CRUD 代码（Phase 1-2）
/new-crud ParkingOrder parking_order 停车订单

# AI 会基于 database-engineering-standard.md 生成代码
```

#### 场景 2：在已有模块添加新接口

```bash
# Phase 1-2 增强的 new-api
/new-api 查询用户最近订单

# AI 会：
# 1. 分析查询场景
# 2. 设计 SQL（WHERE user_id = ? ORDER BY create_time DESC）
# 3. 检查索引依赖（idx_user_time(user_id, create_time)）
# 4. 评估数据量和性能风险
# 5. 生成代码
```

#### 场景 3：为实体类添加新字段

```bash
# Phase 1-2 增强的 add-field
/add-field ParkingOrder payment_time datetime 支付时间

# AI 会检查：
# 1. 是否查询条件？
# 2. 是否需要索引？
# 3. 是否影响大表？
# 4. 是否需要在线 DDL？
```

#### 场景 4：SQL 性能分析

```bash
# Phase 4 新增的 SQL 性能分析 Skill
# 手动调用（需要先找到 Skill 文件）
# 或在代码 Review 时自动触发

# 分析一个 SQL
SELECT * FROM parking_record WHERE car_plate LIKE '%鲁MA8W%';

# AI 会：
# 1. 定位问题（前置 % 导致索引失效）
# 2. 执行计划分析
# 3. 索引优化建议
# 4. SQL 改写建议（改为等值或前缀匹配）
```

#### 场景 5：生产慢 SQL 治理

```bash
# Phase 6 新增的 PolarDB 慢 SQL 分析命令
/analyze-polardb-slow-query

# 需要提供：
# - Slow Log（执行次数、平均耗时、扫描行数）
# - SQL
# - 表结构
# - EXPLAIN（可选）

# AI 会输出：
# - TOP 慢 SQL 概览
# - 问题分类（索引问题、SQL 写法问题、数据量问题）
# - 执行计划分析
# - SQL 优化建议
# - 索引优化方案
# - 收益评估
```

#### 场景 6：代码 Review

```bash
# Phase 5 增强的 Review 能力
/tzh-review

# 或使用快捷命令
/review-code

# AI 会检查：
# - 数据库设计是否合理
# - 索引设计是否合理
# - SQL 是否存在性能问题
# - PolarDB 适配是否正确
# - 风险分级：P0/P1/P2
```

---

### 3.2 能力链路

整个数据库工程化能力链路：

```
需求分析
   ↓
数据库设计（database-schema-design Skill）
   ↓
代码生成（new-crud / new-api / add-field Skill）
   ↓
SQL 分析（sql-performance-review Skill）
   ↓
代码 Review（tzh-review 增强）
   ↓
慢 SQL 治理（analyze-polardb-slow-query Command）
```

---

### 3.3 关键文件位置

| 文件 | 位置 | 说明 |
|------|------|------|
| **数据库规范唯一事实源** | `global-settings/.claude/docs/guides/database-engineering-standard.md` | 所有数据库规则的唯一权威入口 |
| **数据库设计 Skill** | `skills/database-schema-design/SKILL.md` | 需求阶段 → 数据库设计 |
| **SQL 性能分析 Skill** | `skills/sql-performance-review/SKILL.md` | SQL 生成后 → 性能分析 |
| **Review 增强** | `skills/tzh-review/checklists/db-sql-review.md` | 数据库 + SQL + 索引 + PolarDB Review |
| **慢 SQL 分析命令** | `commands/analyze-polardb-slow-query.md` | 生产环境慢 SQL 治理 |
| **CRUD 生成 Skill** | `skills/new-crud/SKILL.md` | 接入数据库规范 |
| **API 生成 Skill** | `skills/new-api/SKILL.md` | 接入数据库规范 |
| **字段添加 Skill** | `skills/add-field/SKILL.md` | 接入数据库规范 |

---

## 四、注意事项

### 4.1 自动化程度

**✅ 已自动化**：
- 所有生成 Skill（new-crud、new-api、add-field）**自动引用**数据库规范
- SQL 性能分析 Skill **自动检查** SQL 反模式
- Review **自动检查**数据库设计、索引、SQL 性能、PolarDB 适配
- 慢 SQL 分析命令**自动调用** SQL 性能分析 Skill

**⚠️ 需要手动触发的场景**：
- 新业务开发前，需要**手动调用** `/database-schema-design` 进行数据库设计
- 慢 SQL 分析，需要**手动调用** `/analyze-polardb-slow-query`（并提供 Slow Log、SQL、表结构）

**📖 需要阅读文档的场景**：
- 深入理解数据库规范：阅读 `database-engineering-standard.md`
- 学习数据库设计最佳实践：阅读 `database-schema-design/examples/`
- 学习 SQL 性能分析最佳实践：阅读 `sql-performance-review/examples/`

---

### 4.2 核心约束

#### 1. 不破坏存量数据库模型

- ✅ 存量实体 `BusinessEntity.id = varchar(64)` **保持不变**
- ❌ **禁止自动** `varchar → bigint`
- ❌ **禁止批量**改主键
- ❌ **禁止修改**存量表结构
- ⚠️ 任何存量结构调整**必须先输出**：影响范围分析 / 迁移方案 / 回滚方案 / 风险评估，等待人工确认

#### 2. 主键双轨策略

- **新表**：默认 `bigint`（聚簇索引友好、二级索引小、顺序写入无页分裂）
- **存量**：保持 `varchar(64)`（禁止自动迁移）
- **新表使用 `varchar` 主键**：必须书面说明属于以下之一——外部系统 ID、跨库全局唯一标识、明确的特殊业务原因

#### 3. 禁止项

- ❌ **禁止 UUID / 随机字符串作为聚簇主键**（随机写入导致页分裂、二级索引膨胀、写放大）
- ❌ **禁止无业务依据的 `varchar(255)` / `varchar(512)`**（每个 `varchar` 长度必须能说明来源）
- ❌ **禁止先建表、后补索引**（必须：场景 → SQL → 索引 → 表结构）
- ❌ **禁止没有查询场景直接创建索引**（每个索引必须能回答：它支撑哪一条 SQL？）
- ❌ **禁止 `SELECT *`**（必须明确字段）
- ❌ **禁止索引字段函数计算**（DATE_FORMAT、YEAR、MONTH、LEFT、HOUR）
- ❌ **禁止 LIKE 前置百分号**（`car_plate LIKE '%xxx%'`）
- ❌ **禁止深分页**（`LIMIT 100000,20`）
- ❌ **禁止无条件更新删除**（`UPDATE table` / `DELETE FROM table`）

---

### 4.3 最佳实践

#### 1. 数据库设计前先分析访问模式

**错误**：
```
先想字段 → 建表 → 写代码 → 发现慢 → 补索引
```

**正确**：
```
业务场景 → 访问模式 → SQL → 索引 → 表结构
```

**示例**：
```
业务场景：用户查询最近订单
   ↓
访问模式：WHERE user_id = ? ORDER BY create_time DESC LIMIT 20
   ↓
SQL：SELECT id, order_no, amount, status, create_time 
     FROM parking_order 
     WHERE user_id = ? 
     ORDER BY create_time DESC 
     LIMIT 20
   ↓
索引：idx_user_time(user_id, create_time)
   - 支持 user_id 过滤
   - 支持 create_time 排序
   - 覆盖索引（避免回表）
   ↓
表结构：parking_order(...)