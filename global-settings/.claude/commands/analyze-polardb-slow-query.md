---
description: 分析PolarDB/MySQL慢SQL（slow log + EXPLAIN + 索引诊断），生成性能分析与优化报告
---

# PolarDB / MySQL 慢 SQL 分析器

> **使用场景**：线上慢 SQL 治理、SQL 性能排查、索引优化分析、查询性能评估
> **目标**：对 PolarDB/MySQL 慢 SQL 做根因分析、执行计划分析、索引与 SQL 优化，产出可落地方案

---

## 定位

本 Command 负责 **PolarDB MySQL 慢 SQL 分析**，适用于：线上慢 SQL 治理、SQL 性能排查、索引优化分析、查询性能评估。

**不负责**：
- 新表设计、数据模型设计 → 由 `database-schema-design` skill 负责。
- 普通 SQL Review → 由 `review-sql` / `tzh-review` 负责。

**与 Doris 能力的关系**：本命令面向 PolarDB/MySQL；已有的 `analyze-slow-query`（Apache Doris 慢查询分析）**保留不动**，两者并存、各司其栈。

## 唯一事实源（必读，禁止复制规则）

所有 SQL 硬规则、索引规则、失效场景、PolarDB 特性，**必须引用**：
`global-settings/.claude/docs/guides/database-engineering-standard.md`

**禁止**复制数据库规则；所有数据库规则以该文件为准。重点引用第 4（索引）、5（SQL 硬规则）、6（慢SQL/失效）、8（PolarDB专项）、9（生产案例）章。

## 与现有能力的调用关系

```
analyze-polardb-slow-query（本命令：慢SQL 入口）
        ↓
sql-performance-review（Skill：SQL 性能分析方法）
        ↓
database-engineering-standard（规范：唯一规则来源）
```

形成闭环：**慢 SQL 输入 → SQL 性能分析 → 优化建议**。本命令负责"接入慢 SQL 数据并组织报告"，具体分析方法复用 `sql-performance-review` skill，不重复其规则。

## 输入要求

支持以下输入（越完整分析越准确）：

### 1. Slow Log
PolarDB/MySQL 慢日志条目：SQL、执行次数、平均耗时、最大耗时、扫描行数、返回行数。

### 2. SQL
完整 SQL 文本。

### 3. 表结构
`CREATE TABLE`：字段、主键、现有索引。

### 4. EXPLAIN
`EXPLAIN` 或 `EXPLAIN ANALYZE`，分析：`type`、`possible_keys`、`key`、`rows`、`filtered`、`Extra`。

> 缺表结构或 EXPLAIN 时，先向用户索取；无法获取则给出"假设前提明确、待 EXPLAIN 验证"的分析。**本命令只分析，不连接生产库、不执行任何 SQL。**

## 执行流程

1. **收集慢 SQL 输入**：slow log / SQL / 表结构 / EXPLAIN，尽量齐全。
2. **TOP 慢 SQL 概览**：按耗时与扫描行排序，列出重点治理对象。
3. **问题分类**：索引问题 / SQL 写法问题 / 数据量问题 / 事务问题。
4. **执行计划分析**：逐项分析 `type` / `key` / `rows` / `Extra`。
5. **SQL 优化建议**：给出优化前后 SQL 与理由。
6. **索引优化方案**：基于访问路径给出索引及理由、收益。
7. **收益评估**：扫描行减少、执行时间降低、索引收益、风险等级。

## 输出模板：《PolarDB 慢 SQL 分析报告》

固定结构如下。

### 1. TOP 慢 SQL 概览

| SQL | 执行次数 | 平均耗时 | 最大耗时 | 扫描行数 | 风险 |
|---|---:|---:|---:|---:|---|
|  |  |  |  |  | P0 / P1 / P2 |

### 2. SQL 问题分类

- **索引问题**：无索引 / 索引未命中 / 联合索引顺序错误 / 索引选择性不足。
- **SQL 写法问题**：`SELECT *` / 函数包字段 / `LIKE` 前置 `%` / 深分页。
- **数据量问题**：大表扫描 / 历史数据过多。
- **事务问题**：大事务 / 锁等待。

### 3. 执行计划分析

- **type**：`ALL`（全表，高危）/ `range` / `ref` / `const`——判断访问类型与风险。
- **key**：实际使用的索引（对比 `possible_keys`，是否未命中/用错）。
- **rows**：扫描规模（结合表总量判断扫描比例）。
- **Extra**：关注 `Using filesort`、`Using temporary`、`Using where`。

### 4. SQL 优化建议

优化前：

```sql
原SQL
```

优化后：

```sql
优化SQL
```

说明：优化原因。

### 5. 索引优化方案

每个索引建议必须包含：

- 索引：`idx_xxx(a, b, c)`
- 支持：什么查询
- 原因：字段顺序设计原因（等值→范围→排序→覆盖）
- 收益：减少扫描范围 / 免回表 / 免 filesort

### 6. 收益评估

- 扫描行减少（量级）
- 执行时间降低（预估）
- 索引收益与写放大权衡
- 风险等级（P0 阻断 / P1 上线风险 / P2 优化建议）

## 内置真实生产案例

### 案例 1：`parking_record_new` —— 车牌片段模糊

问题：

```sql
car_plate LIKE '%xxx%'
```

分析：
- **为什么索引失效**：前置 `%` 使 `car_plate` 上的 BTree 索引无法定位起始位置，退化全表扫描。
- **如何优化**：按检索粒度选择走索引的写法。

规则：

```sql
car_plate = ?          -- 完整车牌：走索引
car_plate LIKE 'xxx%'  -- 前缀：可走索引
-- 片段：限制停车场/时间窗范围，或评估搜索能力（ES 等）
```

### 案例 2：`parking_lot_statistics` —— 日期函数导致索引失效

问题：

```sql
DATE_FORMAT(statistics_time, '%Y%m%d')
```

分析：函数包裹索引列 `statistics_time`，优化器无法使用该列索引，导致全表扫描。

优化：

```sql
statistics_time >= ?
AND statistics_time < ?
```

改为范围条件后命中索引，扫描范围大幅下降。

---

**版本**：1.0.0
**更新日期**：2026-07-27
**规范依据**：`global-settings/.claude/docs/guides/database-engineering-standard.md`


