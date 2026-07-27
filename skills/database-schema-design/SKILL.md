---
name: database-schema-design
description: 在编码前，从业务需求主动完成数据库设计（业务分析 → 数据模型 → 访问模式 → SQL 设计 → 索引设计 → 表结构 DDL → 容量评估）。适用于新业务开发、新模块设计、新表设计、数据模型设计。所有规则以 database-engineering-standard.md 为准。
allowed-tools: Read, Glob, Grep, Write, Edit
argument-hint: "[模块/功能名称] [PRD或需求描述]"
---

# 数据库设计（Database Schema Design）

在**编码之前**，从业务需求出发，主动产出完整、可执行、自解释的数据库设计方案。

## 定位

本 Skill 负责**数据库设计阶段**，适用于：

- 新业务开发
- 新模块设计
- 新表设计
- 数据模型设计

**不负责**：SQL 专项性能分析、已有慢 SQL 优化——这些由 `sql-performance-review` skill 负责。

## 唯一事实源（必读，禁止复制规则）

所有字段类型、主键、索引、SQL、PolarDB 规则，**必须引用**：
`global-settings/.claude/docs/guides/database-engineering-standard.md`

**禁止**在本 Skill 内复制或另行维护数据库规则；所有数据库设计规则以该文件为准。重点引用：
- 第 1 章 设计原则（业务场景驱动）
- 第 2 章 字段设计 / 第 3 章 主键设计 / 第 4 章 索引设计 / 第 5 章 SQL 硬规则
- 第 8 章 PolarDB/InnoDB 专项 / 第 11 章 生成自检清单

## 强制设计流程（不可颠倒）

**禁止**：

```
先建表 → 开发代码 → 发现慢SQL → 补索引
```

**必须**：

```
业务场景
   ↓
访问模式
   ↓
SQL 设计
   ↓
索引设计
   ↓
表结构设计
   ↓
代码生成
```

## 输入要求

### 业务信息
- PRD / 需求描述
- 业务流程
- 用户场景
- 核心功能

### 数据访问信息
- 查询场景（谁、按什么条件查）
- 写入场景（新增/更新/删除频率）
- 数据规模（初始量级、单表预估行数）
- 增长速度（日/月增量）
- 访问频率（QPS 量级、读写比）

> 若输入缺失，先向用户补齐关键项（尤其访问模式与数据规模），再进入设计。

## 输出要求

必须生成**完整数据库设计方案**，按以下 5 部分顺序输出（顺序即设计流程）：

### 1. 业务模型分析
- 核心实体
- 实体关系（1:1 / 1:N / N:N）
- 数据生命周期（产生、变更、归档/删除）

### 2. 访问模式分析（重点，先于建表）

必须先回答：
- 谁访问数据？
- 如何查询？
- 查询条件是什么？
- 数据量是多少？
- 查询频率是多少？

输出**典型查询场景**列表。示例（查询用户最近订单）：

```sql
WHERE user_id = ?
ORDER BY create_time DESC
```

### 3. SQL 设计

根据访问模式设计核心 SQL，每条 SQL 必须明确：查询字段（禁 `SELECT *`）、查询条件、排序方式、分页方式。遵循第 5 章 SQL 硬规则（禁函数包裹索引列、禁 `LIKE '%x%'` 无约束、禁深分页、写操作必带 WHERE 与隔离条件）。

### 4. 索引设计（必须基于 SQL）

每个索引必须写明**索引定义 / 用途 / 原因**三要素。示例：

- 索引：`idx_user_time (user_id, create_time)`
- 用途：支持 `user_id` 过滤 + `create_time` 排序
- 原因：`user_id` 等值查询（高选择性在前），`create_time` 范围及排序（范围/排序列在后），避免 `Using filesort`

规则（详见第 4 章）：最左前缀、高选择性优先、覆盖索引、冗余治理，单表索引 ≤ 5。

**禁止：没有查询场景直接创建索引。**

### 5. 表结构设计（完整 DDL）

输出完整 DDL，包括：表名、字段、类型、`COMMENT`、默认值、主键、唯一键、索引。字段类型与主键遵循第 2、3 章：状态 `tinyint`、金额 `decimal`、时间 `datetime`；新表主键默认 `bigint`；必备 `id`/`create_time`/`update_time`；字符集 `utf8mb4`。

### 6. 容量评估
- 初始与预估行数、日/月增量
- 单表增长到何量级需分区/归档（呼应第 8 章大表治理）
- 高频写表的索引写放大权衡

## 执行流程

1. **收集/确认输入**：业务信息 + 数据访问信息；缺失项先补齐。
2. **业务模型分析**：产出实体、关系、生命周期。
3. **访问模式分析**：列出典型查询/写入场景与数据规模。
4. **SQL 设计**：为每个场景写核心 SQL。
5. **索引设计**：基于 SQL 设计索引，逐个给出用途与原因。
6. **表结构设计**：产出完整 DDL。
7. **容量评估**：给出规模与增长治理建议。
8. **自检**：对照 `database-engineering-standard.md` 第 11 章自检清单逐项核对。

> 本 Skill 只产出设计文本（DDL/SQL 供人工执行），**禁止连接或修改任何数据库，禁止执行 DDL/DML**。

## 示例：智慧停车订单表设计

演示"SQL 驱动索引设计"的完整流程。

### 1. 业务模型分析
- 核心实体：停车订单（parking_order）。
- 关系：订单 N:1 用户、N:1 停车场；订单含车牌、金额、状态、进出场时间。
- 生命周期：进场生成 → 出场计费 → 支付 → 归档。

### 2. 访问模式分析

| 场景 | 查询条件 | 排序 | 频率/规模 |
|---|---|---|---|
| 用户查询订单 | `user_id = ?` | `create_time DESC` | 高频，用户维度 |
| 车场查询订单 | `parking_lot_id = ?` + 时间范围 | `create_time DESC` | 高频，运营后台 |
| 车牌查询 | `car_plate = ?`（完整值） | `create_time DESC` | 中频 |
| 时间范围查询 | `parking_lot_id = ?` + `create_time BETWEEN ? AND ?` | `create_time` | 报表/对账 |
| 状态查询 | `parking_lot_id = ?` + `status = ?` | `create_time DESC` | 中频 |

### 3. SQL 设计（核心，字段收敛）

```sql
-- 用户查询订单
SELECT id, user_id, parking_lot_id, car_plate, amount, status, create_time
FROM parking_order
WHERE user_id = ? ORDER BY create_time DESC LIMIT ?;

-- 车场 + 时间范围（报表）
SELECT id, user_id, car_plate, amount, status, create_time
FROM parking_order
WHERE parking_lot_id = ? AND create_time >= ? AND create_time < ?
ORDER BY create_time DESC;

-- 车牌精确查询（禁止 LIKE '%车牌%'）
SELECT id, user_id, parking_lot_id, amount, status, create_time
FROM parking_order
WHERE car_plate = ? ORDER BY create_time DESC LIMIT ?;

-- 车场 + 状态
SELECT id, user_id, car_plate, amount, create_time
FROM parking_order
WHERE parking_lot_id = ? AND status = ? ORDER BY create_time DESC LIMIT ?;
```

### 4. 索引设计（由上述 SQL 反推）

| 索引 | 用途 | 原因 |
|---|---|---|
| `idx_user_time (user_id, create_time)` | 用户查订单 + 时间排序 | `user_id` 等值高选择性在前，`create_time` 排序在后，免 filesort |
| `idx_lot_time (parking_lot_id, create_time)` | 车场 + 时间范围/排序 | `parking_lot_id` 等值在前，`create_time` 范围+排序在后 |
| `idx_lot_status_time (parking_lot_id, status, create_time)` | 车场 + 状态 + 排序 | 等值(`lot`)→等值(`status`)→排序(`time`)，最左前缀可复用 `parking_lot_id` |
| `idx_plate_time (car_plate, create_time)` | 车牌精确查询 | `car_plate` 完整值等值命中；禁止片段 `LIKE '%x%'` |

> `idx_lot_status_time` 已覆盖"车场+时间范围"的 `parking_lot_id` 前缀，需评估与 `idx_lot_time` 的冗余（第 4 章冗余治理）：若时间范围查询不带 status，仍保留 `idx_lot_time`；否则可合并。

### 5. 表结构 DDL

```sql
CREATE TABLE `parking_order` (
  `id` bigint NOT NULL COMMENT '主键',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `parking_lot_id` bigint NOT NULL COMMENT '停车场ID',
  `car_plate` varchar(16) NOT NULL COMMENT '车牌号',
  `amount` decimal(10,2) NOT NULL DEFAULT 0.00 COMMENT '金额(元)',
  `status` tinyint NOT NULL DEFAULT 0 COMMENT '订单状态:0进行中,1已支付,2已取消',
  `enter_time` datetime DEFAULT NULL COMMENT '进场时间',
  `exit_time` datetime DEFAULT NULL COMMENT '出场时间',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_time` (`user_id`, `create_time`),
  KEY `idx_lot_time` (`parking_lot_id`, `create_time`),
  KEY `idx_lot_status_time` (`parking_lot_id`, `status`, `create_time`),
  KEY `idx_plate_time` (`car_plate`, `create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='停车订单';
```

### 6. 容量评估
- 假设单城市日均 50 万单，年约 1.8 亿行 → 单表偏大，评估按 `create_time` 分区或冷热分离（第 8 章）。
- 写入高频：索引数量控制在示例的 4 个内，避免写放大；如冗余成立则合并。

---

**版本**：1.0.0
**更新日期**：2026-07-27
**规范依据**：`global-settings/.claude/docs/guides/database-engineering-standard.md`


