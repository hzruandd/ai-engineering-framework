---
name: sql-performance-review
description: 对已生成/已有的 SQL 做性能分析与优化（问题定位 → 执行计划分析 → 索引优化 → SQL 改写 → 风险评估）。适用于 SQL Review、慢 SQL 分析、SQL 优化、索引优化、执行计划分析。所有规则以 database-engineering-standard.md 为准。
allowed-tools: Read, Glob, Grep, Write, Edit
argument-hint: "[SQL或Mapper] [表结构/EXPLAIN/slow log 可选]"
---

# SQL 性能分析与优化（SQL Performance Review）

对 SQL 进行性能分析、执行计划分析、索引优化与慢 SQL 治理，产出结构化性能分析报告。

## 定位

本 Skill 负责 **SQL 性能分析和优化**，适用于：

- SQL Review
- 慢 SQL 分析
- SQL 优化
- 索引优化
- 执行计划分析

**不负责**：新表设计、数据模型设计——这些由 `database-schema-design` skill 负责。

## 唯一事实源（必读，禁止复制规则）

所有 SQL 硬规则、索引规则、失效场景、PolarDB 特性，**必须引用**：
`global-settings/.claude/docs/guides/database-engineering-standard.md`

**禁止**在本 Skill 内复制或另行维护数据库规则；所有规则以该文件为准。重点引用：
- 第 4 章 索引设计（列顺序、最左前缀、覆盖、冗余治理）
- 第 5 章 SQL 硬规则（反模式清单）
- 第 6 章 慢 SQL 与索引失效（失效场景、EXPLAIN 关注点、PolarDB/MySQL 分析链路）
- 第 8 章 PolarDB/MySQL 专项规范（聚簇/二级索引、Buffer Pool、Redo/Undo/MVCC、大表治理、在线DDL、读写分离、HTAP）
- 第 9 章 生产案例沉淀

## 输入要求

支持以下任意组合输入，越完整分析越准确：

### SQL
查询 SQL / `INSERT` / `UPDATE` / `DELETE`。

### 表结构
`CREATE TABLE`、字段定义、主键、现有索引。

### 执行计划
`EXPLAIN` 或 `EXPLAIN ANALYZE`，关注：`type`、`possible_keys`、`key`、`rows`、`filtered`、`Extra`。

### 慢 SQL 信息
PolarDB / MySQL slow log：执行次数、平均耗时、最大耗时、扫描行数。

> 若缺少表结构或 EXPLAIN，先向用户索取；无法获取时，基于 SQL 与经验给出**假设前提明确**的分析，并标注"待 EXPLAIN 验证"。

## 输出要求

输出一份 **SQL 性能分析报告**，采用固定结构：

```
# SQL 性能分析报告
```

### 1. SQL 问题定位

按类别定位问题：全表扫描 / 索引未命中 / 索引设计问题 / SQL 写法问题 / 数据量问题 / 锁等待问题。

每个问题说明：**问题现象**、**影响范围**、**风险等级（P0/P1/P2）**。

### 2. 执行计划分析

必须逐项分析：

- **type**：是否存在 `ALL`（全表）；期望达到 `range` / `ref` / `const`。
- **key**：实际使用的索引（与 `possible_keys` 对比，是否用错/未用）。
- **rows**：扫描数据量（结合表总量判断扫描比例）。
- **Extra**：关注 `Using filesort`、`Using temporary`、`Using where`（以及回表 `Using index condition` / 是否 `Using index` 覆盖）。

### 3. 索引优化建议

必须基于**实际 SQL 访问路径**。每个索引建议写明：

- 索引：`idx_xxx(a, b, c)`
- 支持：什么查询
- 原因：为什么字段顺序这样设计（等值→范围→排序→覆盖）
- 收益：减少扫描范围 / 免回表 / 免 filesort

### 4. SQL 优化建议

必须给出：**优化前 SQL**、**优化后 SQL**、**为什么优化**。

### 5. 风险评估

输出 P0 / P1 / P2：

- **P0**：生产高频慢 SQL，影响核心交易（下单/支付/开闸/清分/对账等）。
- **P1**：存在明确性能风险，需要优化。
- **P2**：优化建议，非阻断。

---

## 内置 SQL 反模式检查（必须逐条核对）

对照 `database-engineering-standard.md` 第 5 章，每次分析必须检查：

1. **`SELECT *`** —— 错误：`select *`；规则：必须明确字段。
2. **索引字段函数计算** —— 错误：`DATE_FORMAT(create_time,'%Y-%m-%d')`；检查函数：`DATE_FORMAT`、`YEAR`、`MONTH`、`LEFT`、`HOUR` 等包裹索引列。
3. **LIKE 前置百分号** —— 错误：`car_plate LIKE '%xxx%'`；说明：BTree 索引无法有效利用。
4. **深分页** —— 错误：`LIMIT 100000,20`；建议：游标分页 / 延迟关联。
5. **无条件更新删除** —— 错误：`UPDATE table` / `DELETE FROM table`；必须检查 `WHERE` 条件（含隔离条件）。
6. **隐式类型转换** —— 检查：如 `varchar` 字段与数字比较、字符集不一致导致索引失效。

## 真实生产案例沉淀

（与 `database-engineering-standard.md` 第 9 章一致，此处从性能分析视角展开。）

### 案例 1：`parking_record_new` —— 车牌片段模糊

**问题 SQL**：

```sql
WHERE car_plate LIKE '%鲁MA8W%'
```

**分析**：前置 `%` 使 `car_plate` 上的 BTree 索引无法定位起始位置，退化为全表扫描；随数据增长必然慢查询。

**改写规则**：

```sql
car_plate = ?              -- 完整车牌：走索引
car_plate LIKE '鲁MA8%'    -- 前缀：可走索引
-- 片段检索：限制停车场/时间窗范围，或使用搜索能力（ES 等）
```

### 案例 2：`parking_lot_statistics` —— 日期函数导致全表扫描

**问题 SQL**：

```sql
WHERE DATE_FORMAT(statistics_time, '%Y%m%d') = ?
```

**分析**：对索引列 `statistics_time` 使用 `DATE_FORMAT`，优化器无法使用该列索引，导致全表扫描。

**优化**：

```sql
WHERE statistics_time >= ? AND statistics_time < ?
```

改为范围条件后命中 `statistics_time` 索引，扫描范围大幅下降。

## 执行流程

1. **收集输入**：SQL + （表结构 / EXPLAIN / slow log，尽量齐全）；缺失先索取或标注假设。
2. **问题定位**：按 6 类归类问题，标注现象/影响/风险等级。
3. **执行计划分析**：逐项分析 `type` / `key` / `rows` / `Extra`。
4. **反模式检查**：逐条核对内置 6 项反模式。
5. **索引优化建议**：基于访问路径，给出"索引/支持/原因/收益"。
6. **SQL 优化建议**：给出优化前后 SQL 与理由。
7. **风险评估**：输出 P0/P1/P2 结论。

> 本 Skill 只产出分析与改写建议（SQL 供人工执行），**禁止连接或修改任何数据库，禁止执行 DDL/DML**。

## 测试示例

两个端到端示例，验证输出包含：问题定位 / 执行计划分析 / 索引建议 / SQL 优化。

### 测试示例 1

**输入 SQL**：

```sql
SELECT * FROM parking_order
WHERE DATE_FORMAT(create_time, '%Y-%m-%d') = '2026-07-27'
  AND parking_lot_id = 1001
ORDER BY create_time DESC LIMIT 100000, 20;
```

**输出：SQL 性能分析报告**

#### 1. SQL 问题定位
- **索引未命中（函数包裹）**：`DATE_FORMAT(create_time)` 使时间索引失效。现象：全表扫描；影响：车场订单查询；风险：**P0**（高频核心链路）。
- **SQL 写法问题（SELECT \*）**：宽表回表、网络放大。风险：**P2**。
- **数据量问题（深分页）**：`LIMIT 100000,20` 需扫描并丢弃前 10 万行。风险：**P1**。

#### 2. 执行计划分析
- `type`：预期 `ALL`（因函数包裹无法用索引）→ 需优化为 `range`/`ref`。
- `key`：`NULL`（未命中索引）→ 期望命中 `idx_lot_time`。
- `rows`：接近全表 → 优化后应大幅下降。
- `Extra`：`Using where; Using filesort`（排序未走索引）。

#### 3. 索引优化建议
- 索引：`idx_lot_time (parking_lot_id, create_time)`
- 支持：车场维度 + 时间范围过滤与排序
- 原因：`parking_lot_id` 等值在前（高选择性），`create_time` 范围+排序在后，避免 filesort
- 收益：扫描范围从全表降到当日该车场区间，消除 filesort

#### 4. SQL 优化建议

优化前：

```sql
SELECT * FROM parking_order
WHERE DATE_FORMAT(create_time, '%Y-%m-%d') = '2026-07-27' AND parking_lot_id = 1001
ORDER BY create_time DESC LIMIT 100000, 20;
```

优化后：

```sql
SELECT id, user_id, parking_lot_id, car_plate, amount, status, create_time
FROM parking_order
WHERE parking_lot_id = 1001
  AND create_time >= '2026-07-27 00:00:00'
  AND create_time <  '2026-07-28 00:00:00'
  AND id < ?              -- 游标分页：上一页最后一条 id
ORDER BY create_time DESC LIMIT 20;
```

为什么优化：① 去掉 `DATE_FORMAT`，改范围条件命中索引；② 字段收敛替代 `SELECT *`；③ 游标分页替代深分页。

#### 5. 风险评估
- **P0**：函数包裹导致高频车场查询全表扫描。
- **P1**：深分页。
- **P2**：`SELECT *`。

---

### 测试示例 2

**输入 SQL**：

```sql
UPDATE parking_order SET status = 2 WHERE car_plate LIKE '%鲁MA8W%';
```

**输出：SQL 性能分析报告**

#### 1. SQL 问题定位
- **无精确条件的写操作 + 片段模糊**：`UPDATE` 以 `LIKE '%...%'` 为条件，既全表扫描又可能误更新多行。现象：全表扫描 + 数据一致性风险；影响：订单状态；风险：**P0**。

#### 2. 执行计划分析
- `type`：`ALL`（前置 `%`，`car_plate` 索引失效）。
- `key`：`NULL`。
- `rows`：全表；写操作还将持有较多行锁，`Extra`：`Using where`。

#### 3. 索引优化建议
- 索引：`idx_plate_time (car_plate, create_time)`（仅对**完整车牌等值**查询有效；片段模糊无法利用）。
- 说明：更新应先用主键/唯一键精确定位，而非依赖车牌模糊。

#### 4. SQL 优化建议

优化前：

```sql
UPDATE parking_order SET status = 2 WHERE car_plate LIKE '%鲁MA8W%';
```

优化后：

```sql
-- 先精确查出目标订单主键，再按主键更新（带隔离条件）
UPDATE parking_order
SET status = 2
WHERE id = ? AND parking_lot_id = ?;
-- 若确需按车牌：使用完整车牌等值 + 时间范围收敛
-- WHERE car_plate = '鲁MA8W8' AND create_time >= ? AND create_time < ?
```

为什么优化：① 消除前置 `%` 使索引可用；② 以主键/唯一键精确定位，避免误更新多行；③ 补租户/车场隔离条件。

#### 5. 风险评估
- **P0**：核心表高危写操作，条件不精确且全表扫描。

---

**版本**：1.0.0
**更新日期**：2026-07-27
**规范依据**：`global-settings/.claude/docs/guides/database-engineering-standard.md`



