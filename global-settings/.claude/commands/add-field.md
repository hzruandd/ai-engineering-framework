---
description: 为已有实体类添加新字段，并更新相关代码
---

# 添加字段

我需要为已有实体类添加新字段。

## 请先提供以下信息：

1. **实体类名称**（如：User）
2. **所属模块**（如：city-parking-eop）
3. **新增字段信息**：
   - 字段名（驼峰，如：nickname）
   - 数据库字段名（下划线，如：nickname）
   - 字段类型（如：String、Integer、Date）
   - 字段说明（如：用户昵称）
   - 是否必填
   - 是否作为查询条件

## 操作步骤：

### Step 1: 数据库添加字段
生成ALTER TABLE语句：
```sql
ALTER TABLE `table_name` ADD COLUMN `field_name` VARCHAR(100) COMMENT '字段说明' AFTER `existing_field`;
```

### Step 2: 更新Entity类
在实体类中添加字段：
```java
/** 字段说明 */
@Schema(title = "字段说明")
@Excel(name = "字段说明")
private String fieldName;
```

如果是日期类型，添加格式化注解：
```java
@JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
@Schema(title = "字段说明")
private Date fieldName;
```

如果需要参数校验：
```java
@NotBlank(message = "字段不能为空")
@Schema(title = "字段说明")
private String fieldName;
```

### Step 3: 更新Mapper.xml

在 `<resultMap>` 中添加映射：
```xml
<result property="fieldName" column="field_name" />
```

在 `select{ClassName}Vo` 中添加字段：
```xml
select id, ..., field_name from table_name
```

如果作为查询条件，在 `<where>` 中添加：
```xml
<if test="fieldName != null and fieldName != ''">
    and field_name like concat('%', #{fieldName}, '%')
</if>
```

### Step 4: 清理缓存

如果该实体有缓存，需要在Service的更新/删除方法中清理：
```java
// 清理缓存
RedisUtils.deleteObject("cache:key:" + id);
```

### Step 5: 验证

确认以下内容：
- [ ] 数据库字段添加成功
- [ ] Entity类字段添加完整
- [ ] Mapper.xml映射正确
- [ ] 查询条件生效（如果需要）
- [ ] 缓存清理逻辑添加（如果有缓存）

## 注意事项：

1. **字段命名**：Java字段用驼峰，数据库字段用下划线
2. **注解选择**：使用@Schema（不用@ApiModelProperty）
3. **缓存清理**：修改实体类后记得清理相关缓存
4. **向下兼容**：添加字段不要影响已有功能

请根据提供的信息开始添加字段并更新相关代码。
