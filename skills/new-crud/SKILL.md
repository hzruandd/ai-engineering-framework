---
name: new-crud
description: 创建完整的CRUD功能（Entity + Mapper + Service + DubboApi），包含标准的增删改查方法。适用于新建业务模块、快速搭建基础功能、标准化开发流程等场景。
argument-hint: [实体类名] [表名] [功能名称]
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# 创建完整的CRUD功能

创建完整的CRUD功能模块，包含 Entity、Mapper、Service、DubboApi 四层代码，遵循框架规范。

## 数据库规范（唯一事实源，必读）

本 Skill 的所有数据库产出物**必须遵循**唯一事实源：
`global-settings/.claude/docs/guides/database-engineering-standard.md`

生成前后强制对照该规范的：
- 第 1 章 设计原则（业务场景驱动：场景→访问模式→SQL→索引→表结构）
- 第 2 章 字段设计（类型、必备字段、无依据长度禁令）
- 第 3 章 主键双轨策略（新表 `bigint`，存量 `varchar(64)` 不动，`varchar` 主键需理由）
- 第 4 章 索引设计（基于查询场景，联合索引列顺序，正确/错误案例）
- 第 5 章 SQL 硬规则（禁 `SELECT *`、禁函数包裹索引列、禁深分页、写操作必带 WHERE）
- 第 10 章 生成产出物要求 / 第 11 章 生成自检清单

**正向设计顺序（禁止先建表后补索引）**：`业务场景 → 访问模式 → SQL → 索引 → 表结构`。

## 使用方式

```bash
# 基础用法（交互式）
/new-crud

# 指定实体类和表名
/new-crud ParkingLot parking_lot

# 完整参数
/new-crud ParkingLot parking_lot 停车场管理
```

## 参数说明

如果使用 `$ARGUMENTS`，格式为：`实体类名 表名 功能名称`

示例：
- `ParkingLot parking_lot 停车场管理`
- `Order order_info 订单管理`

## 执行流程

### 第一步：收集信息

如果未提供完整参数，交互式收集以下信息：

1. **实体类名称**（驼峰命名，如：ParkingLot）
2. **表名**（下划线命名，如：parking_lot）
3. **所属模块**（如：city-parking-xxx）
4. **功能名称**（中文，如：停车场管理）
5. **主要字段列表**：
   - 字段名（驼峰）
   - 数据库字段名（下划线）
   - 字段类型
   - 字段说明
   - 是否必填
   - 是否查询条件

6. **可选功能**：
   - 是否需要缓存？
   - 是否需要防重复提交？
   - 是否需要乐观锁？
   - 是否需要逻辑删除？
   - 是否需要Excel导入导出？

### 第一步补充：数据库设计（先于建 Entity）

在生成任何代码前，先按唯一事实源完成数据库设计并输出：

1. **访问模式分析**：列出该模块的主要查询（WHERE / JOIN / ORDER BY / GROUP BY / 分页），据此决定索引。
2. **表结构 DDL**：
   - 字段类型合规：状态 `tinyint`、金额 `decimal`、时间 `datetime`；无业务依据禁止 `varchar(255/512)`。
   - 必备字段：`id`、`create_time`、`update_time`；字符集 `utf8mb4`。
   - 主键：新表默认 `bigint`；若沿用存量 `varchar(64)` 或使用 `varchar` 主键，说明理由（第 3 章）。
3. **索引方案**：基于第 1 步的查询场景设计，联合索引按"高选择性等值 → 范围 → 排序 → 覆盖"排列，单表 ≤ 5，避免重复/低选择性单列索引，并给出**每个索引的理由**（第 4 章）。
4. **性能说明**：关键查询的命中索引与查询路径、潜在风险。

DDL 模板（示例）：

```sql
CREATE TABLE `{table_name}` (
  `id` bigint NOT NULL COMMENT '主键',
  `field_name` varchar(100) NOT NULL COMMENT '{字段说明}',
  `status` tinyint NOT NULL DEFAULT 0 COMMENT '状态',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_field_status` (`field_name`, `status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='{功能名称}';
```

> 仅输出 DDL 文本供人工执行，**禁止连接或修改任何数据库**。

### 第二步：创建 Entity 类

**位置**：`{module}-api/src/main/java/cn/city/parking/{module}/api/entity/{ClassName}.java`

**模板**：
```java
package cn.city.parking.{module}.api.entity;

import cn.city.parking.common.core.web.domain.BusinessEntity;
import com.baomidou.mybatisplus.annotation.TableName;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.FieldFill;
import com.baomidou.mybatisplus.annotation.Version;
import com.fasterxml.jackson.annotation.JsonFormat;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import lombok.EqualsAndHashCode;

import javax.validation.constraints.*;
import java.time.LocalDateTime;
import java.math.BigDecimal;

/**
 * {功能名称}实体
 *
 * @author {作者}
 * @date {日期}
 */
@Data
@EqualsAndHashCode(callSuper = true)
@TableName("{table_name}")
@Schema(description = "{功能名称}实体")
public class {ClassName} extends BusinessEntity {

    /**
     * {字段说明}
     */
    @Schema(description = "{字段说明}")
    @NotBlank(message = "{字段说明}不能为空")
    @Size(max = 100, message = "{字段说明}长度不能超过100个字符")
    private String fieldName;

    /**
     * {日期字段说明}
     */
    @Schema(description = "{日期字段说明}")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime dateField;

    // ⚠️ 如果数据库有以下字段，必须显式声明

    /**
     * 创建者
     */
    @TableField(value = "create_by", fill = FieldFill.INSERT)
    @Schema(description = "创建者")
    private String createBy;

    /**
     * 更新者
     */
    @TableField(value = "update_by", fill = FieldFill.UPDATE)
    @Schema(description = "更新者")
    private String updateBy;

    /**
     * 删除标志（0-存在，1-删除）
     */
    @TableField(value = "del_flag", fill = FieldFill.INSERT)
    @Schema(description = "删除标志（0-存在，1-删除）")
    private Integer delFlag;

    /**
     * 乐观锁版本号
     */
    @Version
    @Schema(description = "乐观锁版本号")
    private Long revision;
}
```

**关键点**：
- ✅ 继承 `BusinessEntity`（包含 id、createTime、updateTime）
- ✅ 使用 `@TableName` 指定表名
- ✅ 使用 `@Schema` 注解（不用 @ApiModelProperty）
- ✅ 日期字段添加 `@JsonFormat`
- ✅ 可选字段根据需要添加：createBy、updateBy、delFlag、revision
- ✅ 参数校验注解（推荐但非强制）：@NotBlank、@Size、@Email、@Pattern 等

### 第三步：创建 Mapper 接口

**位置**：`{module}-server/src/main/java/cn/city/parking/{module}/mapper/{ClassName}Mapper.java`

**模板**：
```java
package cn.city.parking.{module}.mapper;

import cn.city.parking.{module}.api.entity.{ClassName};
import cn.city.parking.common.server.injector.CommonMapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * {功能名称}Mapper接口
 *
 * @author {作者}
 * @date {日期}
 */
public interface {ClassName}Mapper extends CommonMapper<{ClassName}> {

    /**
     * 查询{功能名称}列表
     *
     * @param entity {功能名称}
     * @return {功能名称}集合
     */
    List<{ClassName}> select{ClassName}List({ClassName} entity);

    /**
     * 根据ID查询{功能名称}
     *
     * @param id {功能名称}ID
     * @return {功能名称}
     */
    {ClassName} select{ClassName}ById(@Param("id") String id);
}
```

**关键点**：
- ✅ 继承 `CommonMapper<{ClassName}>`
- ✅ 不需要 `@Mapper` 注解（框架已自动扫描）
- ✅ 定义自定义查询方法

### 第四步：创建 Mapper.xml

**位置**：`{module}-server/src/main/resources/mapper/{ClassName}Mapper.xml`

**模板**：
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
"http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="cn.city.parking.{module}.mapper.{ClassName}Mapper">

    <resultMap id="{ClassName}Result" type="cn.city.parking.{module}.api.entity.{ClassName}">
        <result property="id" column="id" />
        <result property="fieldName" column="field_name" />
        <result property="createTime" column="create_time" />
        <result property="updateTime" column="update_time" />
        <result property="createBy" column="create_by" />
        <result property="updateBy" column="update_by" />
        <result property="delFlag" column="del_flag" />
        <result property="revision" column="revision" />
    </resultMap>

    <sql id="select{ClassName}Vo">
        select id, field_name, create_time, update_time,
               create_by, update_by, del_flag, revision
        from {table_name}
    </sql>

    <select id="select{ClassName}List" parameterType="{ClassName}" resultMap="{ClassName}Result">
        <include refid="select{ClassName}Vo"/>
        <where>
            <if test="fieldName != null and fieldName != ''">
                and field_name like concat('%', #{fieldName}, '%')
            </if>
            and del_flag = 0
        </where>
        order by create_time desc
    </select>

    <select id="select{ClassName}ById" parameterType="String" resultMap="{ClassName}Result">
        <include refid="select{ClassName}Vo"/>
        where id = #{id} and del_flag = 0
    </select>

</mapper>
```

**关键点**：
- ✅ 定义 resultMap
- ✅ 定义公共查询字段（select{ClassName}Vo）
- ✅ 实现列表查询（支持动态条件）
- ✅ 添加逻辑删除条件（del_flag = 0）

### 第五步：创建 Service 接口

**位置**：`{module}-server/src/main/java/cn/city/parking/{module}/service/I{ClassName}Service.java`

**模板**：
```java
package cn.city.parking.{module}.service;

import cn.city.parking.{module}.api.entity.{ClassName};
import com.baomidou.mybatisplus.extension.service.IService;

import java.util.List;

/**
 * {功能名称}Service接口
 *
 * @author {作者}
 * @date {日期}
 */
public interface I{ClassName}Service extends IService<{ClassName}> {

    /**
     * 查询{功能名称}列表
     *
     * @param entity {功能名称}
     * @return {功能名称}集合
     */
    List<{ClassName}> select{ClassName}List({ClassName} entity);

    /**
     * 根据ID查询{功能名称}
     *
     * @param id {功能名称}ID
     * @return {功能名称}
     */
    {ClassName} select{ClassName}ById(String id);

    /**
     * 新增{功能名称}
     *
     * @param entity {功能名称}
     * @return 结果
     */
    int insert{ClassName}({ClassName} entity);

    /**
     * 修改{功能名称}
     *
     * @param entity {功能名称}
     * @return 结果
     */
    int update{ClassName}({ClassName} entity);

    /**
     * 批量删除{功能名称}
     *
     * @param ids 需要删除的{功能名称}ID
     * @return 结果
     */
    int delete{ClassName}ByIds(String[] ids);

    /**
     * 删除{功能名称}信息
     *
     * @param id {功能名称}ID
     * @return 结果
     */
    int delete{ClassName}ById(String id);
}
```

**关键点**：
- ✅ 继承 `IService<{ClassName}>`
- ✅ 定义 7 个标准方法

### 第六步：创建 Service 实现

**位置**：`{module}-server/src/main/java/cn/city/parking/{module}/service/impl/{ClassName}ServiceImpl.java`

**模板**：
```java
package cn.city.parking.{module}.service.impl;

import cn.city.parking.{module}.api.entity.{ClassName};
import cn.city.parking.{module}.mapper.{ClassName}Mapper;
import cn.city.parking.{module}.service.I{ClassName}Service;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Arrays;
import java.util.List;

/**
 * {功能名称}Service业务层处理
 *
 * @author {作者}
 * @date {日期}
 */
@Service
public class {ClassName}ServiceImpl extends ServiceImpl<{ClassName}Mapper, {ClassName}> implements I{ClassName}Service {

    @Override
    public List<{ClassName}> select{ClassName}List({ClassName} entity) {
        return baseMapper.select{ClassName}List(entity);
    }

    @Override
    public {ClassName} select{ClassName}ById(String id) {
        return baseMapper.select{ClassName}ById(id);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public int insert{ClassName}({ClassName} entity) {
        return baseMapper.insert(entity);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public int update{ClassName}({ClassName} entity) {
        return baseMapper.updateById(entity);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public int delete{ClassName}ByIds(String[] ids) {
        return baseMapper.deleteBatchIds(Arrays.asList(ids));
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public int delete{ClassName}ById(String id) {
        return baseMapper.deleteById(id);
    }
}
```

**关键点**：
- ✅ 继承 `ServiceImpl<{ClassName}Mapper, {ClassName}>`
- ✅ 增删改方法添加 `@Transactional(rollbackFor = Exception.class)`

### 第七步：创建 DubboApi 接口

**位置**：`{module}-api/src/main/java/cn/city/parking/{module}/api/{ClassName}DubboApi.java`

**模板**：
```java
package cn.city.parking.{module}.api;

import cn.city.parking.{module}.api.entity.{ClassName};
import cn.city.parking.common.core.web.domain.ResponseResult;
import com.github.pagehelper.PageInfo;

import java.util.List;

/**
 * {功能名称}DubboApi接口
 *
 * @author {作者}
 * @date {日期}
 */
public interface {ClassName}DubboApi {

    /**
     * 分页查询{功能名称}列表
     *
     * @param entity {功能名称}
     * @return {功能名称}集合
     */
    ResponseResult<PageInfo<{ClassName}>> pageList({ClassName} entity);

    /**
     * 查询所有{功能名称}列表
     *
     * @param entity {功能名称}
     * @return {功能名称}集合
     */
    ResponseResult<List<{ClassName}>> allList({ClassName} entity);

    /**
     * 获取{功能名称}详细信息
     *
     * @param id {功能名称}ID
     * @return {功能名称}
     */
    ResponseResult<{ClassName}> getInfo(String id);

    /**
     * 新增{功能名称}
     *
     * @param entity {功能名称}
     * @return 结果
     */
    ResponseResult<Integer> add({ClassName} entity);

    /**
     * 修改{功能名称}
     *
     * @param entity {功能名称}
     * @return 结果
     */
    ResponseResult<Integer> edit({ClassName} entity);

    /**
     * 删除{功能名称}
     *
     * @param ids {功能名称}ID数组
     * @return 结果
     */
    ResponseResult<Integer> remove(String[] ids);
}
```

**关键点**：
- ✅ 定义 6 个标准方法
- ✅ 返回值统一使用 `ResponseResult<T>`

### 第八步：创建 DubboApi 实现

**位置**：`{module}-server/src/main/java/cn/city/parking/{module}/dubbo/{ClassName}DubboApiImpl.java`

**模板**：
```java
package cn.city.parking.{module}.dubbo;

import cn.city.parking.{module}.api.{ClassName}DubboApi;
import cn.city.parking.{module}.api.entity.{ClassName};
import cn.city.parking.{module}.service.I{ClassName}Service;
import cn.city.parking.common.core.web.domain.ResponseResult;
import cn.city.parking.common.dubbo.filter.base.BaseDubboApi;
import com.github.pagehelper.PageInfo;
import com.google.common.base.Preconditions;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.apache.dubbo.config.annotation.DubboService;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;

/**
 * {功能名称}DubboApi实现
 *
 * @author {作者}
 * @date {日期}
 */
@Slf4j
@DubboService
public class {ClassName}DubboApiImpl extends BaseDubboApi implements {ClassName}DubboApi {

    @Autowired
    private I{ClassName}Service {classNameLower}Service;

    @Override
    public ResponseResult<PageInfo<{ClassName}>> pageList({ClassName} entity) {
        // 分页查询必须调用 startDubboPage()
        startDubboPage();
        List<{ClassName}> list = {classNameLower}Service.select{ClassName}List(entity);
        return ResponseResult.success(new PageInfo<>(list));
    }

    @Override
    public ResponseResult<List<{ClassName}>> allList({ClassName} entity) {
        List<{ClassName}> list = {classNameLower}Service.select{ClassName}List(entity);
        return ResponseResult.success(list);
    }

    @Override
    public ResponseResult<{ClassName}> getInfo(String id) {
        // 参数校验
        Preconditions.checkArgument(StringUtils.isNotBlank(id), "{功能名称}ID不能为空");
        {ClassName} entity = {classNameLower}Service.select{ClassName}ById(id);
        return ResponseResult.success(entity);
    }

    @Override
    public ResponseResult<Integer> add({ClassName} entity) {
        // 参数校验
        Preconditions.checkNotNull(entity, "{功能名称}信息不能为空");
        log.info("新增{功能名称}，参数：{}", entity);
        int rows = {classNameLower}Service.insert{ClassName}(entity);
        return ResponseResult.success(rows);
    }

    @Override
    public ResponseResult<Integer> edit({ClassName} entity) {
        // 参数校验
        Preconditions.checkNotNull(entity, "{功能名称}信息不能为空");
        Preconditions.checkArgument(StringUtils.isNotBlank(entity.getId()), "{功能名称}ID不能为空");
        log.info("修改{功能名称}，参数：{}", entity);
        int rows = {classNameLower}Service.update{ClassName}(entity);
        return ResponseResult.success(rows);
    }

    @Override
    public ResponseResult<Integer> remove(String[] ids) {
        // 参数校验
        Preconditions.checkNotNull(ids, "{功能名称}ID不能为空");
        Preconditions.checkArgument(ids.length > 0, "{功能名称}ID不能为空");
        log.info("删除{功能名称}，IDs：{}", ids);
        int rows = {classNameLower}Service.delete{ClassName}ByIds(ids);
        return ResponseResult.success(rows);
    }
}
```

**关键点**：
- ✅ 继承 `BaseDubboApi`（注意包路径：`cn.city.parking.common.dubbo.filter.base.BaseDubboApi`）
- ✅ 添加 `@DubboService` 注解
- ✅ 分页查询调用 `startDubboPage()`
- ✅ 参数校验使用 `Preconditions`（推荐但非强制）
- ✅ 保持薄层：只负责参数校验、调用Service、返回结果
- ❌ 不要在DubboApi中写业务逻辑

## 代码规范检查清单

生成代码后，检查以下规范：

- [ ] Entity 继承 BusinessEntity
- [ ] Entity 使用 @Schema 注解
- [ ] Entity 使用 @TableName 指定表名
- [ ] Entity 日期字段添加 @JsonFormat
- [ ] Mapper 继承 CommonMapper
- [ ] Mapper 不需要 @Mapper 注解
- [ ] Mapper.xml 定义 resultMap
- [ ] Mapper.xml 定义公共查询字段
- [ ] Service 接口继承 IService
- [ ] Service 实现继承 ServiceImpl
- [ ] Service 增删改方法添加 @Transactional
- [ ] DubboApi 返回值使用 ResponseResult<T>
- [ ] DubboApiImpl 继承 BaseDubboApi
- [ ] DubboApiImpl 分页查询调用 startDubboPage()
- [ ] 代码格式化（mvn spring-javaformat:apply）

### 数据库规范自检（对照 database-engineering-standard.md 第 11 章）

- [ ] 已输出表结构 DDL，字段类型合规（状态 tinyint / 金额 decimal / 时间 datetime）
- [ ] 无业务依据的 varchar(255/512) 已消除
- [ ] 必备字段齐全（id / create_time / update_time），字符集 utf8mb4
- [ ] 主键符合双轨策略（新表 bigint；varchar 主键有理由；未擅改存量结构）
- [ ] 索引基于真实查询场景设计，联合索引列顺序正确，已给出索引理由
- [ ] 查询 SQL 无 SELECT *、无函数包裹索引列、无深分页
- [ ] 写操作带 WHERE 与隔离条件，使用 #{} 预编译
- [ ] 已附性能说明（命中索引 / 查询路径 / 风险）

## 可选功能

### 1. 添加缓存

在 Service 实现中添加缓存逻辑（详见 [fix-cache](../fix-cache/SKILL.md)）

### 2. 添加防重复提交

在 DubboApiImpl 的新增方法上添加 `@NoRepeatSubmit` 注解

### 3. 添加乐观锁

在 Entity 中添加 `revision` 字段，并使用 `@Version` 注解

### 4. 添加逻辑删除

在 Entity 中添加 `delFlag` 字段，并在查询条件中添加 `del_flag = 0`

### 5. 添加Excel导入导出

在 Entity 字段上添加 `@Excel` 注解

---

**版本**：1.0.0
**更新日期**：2026-01-23
