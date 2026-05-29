---
name: add-field
description: 为已有实体类添加新字段，并更新相关代码（Entity、Mapper.xml、缓存清理）。适用于需要扩展实体类功能、添加新的业务字段、支持新的查询条件等场景。
argument-hint: [实体类名] [字段信息]
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# 为实体类添加新字段

为已有实体类添加新字段，并自动更新相关代码（Entity、Mapper.xml、缓存清理）。

## 使用方式

```bash
# 基础用法（交互式）
/add-field

# 指定实体类
/add-field User

# 完整参数
/add-field User nickname:String:用户昵称:必填:查询条件
```

## 参数说明

如果使用 `$ARGUMENTS`，格式为：`实体类名 字段名:类型:说明:是否必填:是否查询条件`

示例：
- `User nickname:String:用户昵称:必填:查询条件`
- `Order deliveryAddress:String:配送地址:可选:非查询条件`

## 执行流程

### 第一步：收集信息

如果未提供完整参数，交互式收集以下信息：

1. **实体类名称**（如：User）
2. **所属模块**（如：city-parking-eop）
3. **新增字段信息**：
   - 字段名（驼峰，如：nickname）
   - 数据库字段名（下划线，如：nickname）
   - 字段类型（如：String、Integer、LocalDateTime、BigDecimal）
   - 字段说明（如：用户昵称）
   - 是否必填（是/否）
   - 是否作为查询条件（是/否）
   - 字段长度（如果是String类型）
   - 默认值（可选）

### 第二步：定位文件

使用 Glob 和 Grep 定位相关文件：

1. **Entity 文件**：
   ```bash
   # 查找实体类文件
   find . -name "User.java" -path "*/api/entity/*"
   ```

2. **Mapper.xml 文件**：
   ```bash
   # 查找 Mapper.xml 文件
   find . -name "UserMapper.xml"
   ```

3. **Service 文件**（如果需要缓存清理）：
   ```bash
   # 查找 Service 实现类
   find . -name "UserServiceImpl.java"
   ```

### 第三步：生成数据库 SQL

根据字段信息生成 ALTER TABLE 语句：

**基础模板**：
```sql
ALTER TABLE `table_name`
ADD COLUMN `field_name` {类型} {长度} {NULL/NOT NULL} COMMENT '{说明}'
AFTER `existing_field`;
```

**类型映射**：
- `String` → `VARCHAR(长度)` 或 `TEXT`
- `Integer` → `INT`
- `Long` → `BIGINT`
- `BigDecimal` → `DECIMAL(精度,小数位)`
- `LocalDateTime` → `DATETIME`
- `LocalDate` → `DATE`
- `Boolean` → `TINYINT(1)`

**示例**：
```sql
-- String 类型
ALTER TABLE `sys_user`
ADD COLUMN `nickname` VARCHAR(50) NULL COMMENT '用户昵称'
AFTER `username`;

-- Integer 类型
ALTER TABLE `sys_user`
ADD COLUMN `age` INT NULL COMMENT '年龄'
AFTER `birthday`;

-- LocalDateTime 类型
ALTER TABLE `sys_user`
ADD COLUMN `last_login_time` DATETIME NULL COMMENT '最后登录时间'
AFTER `status`;

-- BigDecimal 类型
ALTER TABLE `order`
ADD COLUMN `discount_amount` DECIMAL(10,2) NULL COMMENT '优惠金额'
AFTER `total_amount`;
```

### 第四步：更新 Entity 类

在实体类中添加字段，包含必要的注解：

**基础字段**：
```java
/**
 * {字段说明}
 */
@Schema(description = "{字段说明}")
private {类型} {字段名};
```

**必填字段（添加校验注解）**：
```java
/**
 * {字段说明}
 */
@Schema(description = "{字段说明}")
@NotBlank(message = "{字段说明}不能为空")
private String {字段名};
```

**String 类型（添加长度校验）**：
```java
/**
 * {字段说明}
 */
@Schema(description = "{字段说明}")
@Size(max = {长度}, message = "{字段说明}长度不能超过{长度}个字符")
private String {字段名};
```

**日期类型（添加格式化注解）**：
```java
/**
 * {字段说明}
 */
@Schema(description = "{字段说明}")
@JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
private LocalDateTime {字段名};
```

**邮箱字段**：
```java
/**
 * {字段说明}
 */
@Schema(description = "{字段说明}")
@Email(message = "邮箱格式不正确")
private String email;
```

**手机号字段**：
```java
/**
 * {字段说明}
 */
@Schema(description = "{字段说明}")
@Pattern(regexp = "^1[3-9]\\d{9}$", message = "手机号格式不正确")
private String phone;
```

**数值范围字段**：
```java
/**
 * {字段说明}
 */
@Schema(description = "{字段说明}")
@Min(value = 0, message = "{字段说明}不能小于0")
@Max(value = 100, message = "{字段说明}不能大于100")
private Integer score;
```

**Excel 导出字段（可选）**：
```java
/**
 * {字段说明}
 */
@Schema(description = "{字段说明}")
@Excel(name = "{字段说明}")
private String {字段名};
```

### 第五步：更新 Mapper.xml

#### 5.1 更新 resultMap

在 `<resultMap>` 中添加字段映射：

```xml
<resultMap id="UserResult" type="cn.city.parking.xxx.api.entity.User">
    <!-- 现有字段 -->
    <result property="id" column="id" />
    <result property="username" column="username" />

    <!-- 新增字段 -->
    <result property="nickname" column="nickname" />
</resultMap>
```

#### 5.2 更新查询字段

在 `select{ClassName}Vo` 中添加字段：

```xml
<sql id="selectUserVo">
    select id, username, email, phone,
           nickname,  <!-- 新增字段 -->
           create_time, update_time
    from sys_user
</sql>
```

#### 5.3 添加查询条件（如果是查询条件）

在 `select{ClassName}List` 的 `<where>` 中添加：

**精确匹配**：
```xml
<if test="nickname != null and nickname != ''">
    and nickname = #{nickname}
</if>
```

**模糊查询**：
```xml
<if test="nickname != null and nickname != ''">
    and nickname like concat('%', #{nickname}, '%')
</if>
```

**范围查询（日期）**：
```xml
<if test="params.beginTime != null and params.beginTime != ''">
    and date_format(last_login_time,'%Y-%m-%d') &gt;= date_format(#{params.beginTime},'%Y-%m-%d')
</if>
<if test="params.endTime != null and params.endTime != ''">
    and date_format(last_login_time,'%Y-%m-%d') &lt;= date_format(#{params.endTime},'%Y-%m-%d')
</if>
```

**范围查询（数值）**：
```xml
<if test="minAge != null">
    and age &gt;= #{minAge}
</if>
<if test="maxAge != null">
    and age &lt;= #{maxAge}
</if>
```

**IN 查询**：
```xml
<if test="statusList != null and statusList.size() > 0">
    and status in
    <foreach collection="statusList" item="status" open="(" separator="," close=")">
        #{status}
    </foreach>
</if>
```

### 第六步：更新缓存清理逻辑（如果有缓存）

如果该实体有缓存，需要在 Service 的更新/删除方法中清理缓存：

**检查是否有缓存**：
```bash
# 搜索 RedisUtils.setCacheObject
grep -r "RedisUtils.setCacheObject.*User" --include="*.java"
```

**添加缓存清理**：

在 `updateUser` 方法中：
```java
@Override
@Transactional(rollbackFor = Exception.class)
public int updateUser(User user) {
    int rows = baseMapper.updateById(user);

    // 清理缓存
    if (rows > 0) {
        // 清理用户信息缓存
        RedisUtils.deleteObject("user:info:" + user.getId());

        // 如果新增字段是查询条件，清理相关缓存
        if (StringUtils.isNotBlank(user.getNickname())) {
            RedisUtils.deleteObject("user:nickname:" + user.getNickname());
        }
    }

    return rows;
}
```

在 `deleteUser` 方法中：
```java
@Override
@Transactional(rollbackFor = Exception.class)
public int deleteUserById(String id) {
    // 先查询用户信息（用于清理缓存）
    User user = baseMapper.selectById(id);

    int rows = baseMapper.deleteById(id);

    // 清理缓存
    if (rows > 0 && user != null) {
        RedisUtils.deleteObject("user:info:" + id);
        if (StringUtils.isNotBlank(user.getNickname())) {
            RedisUtils.deleteObject("user:nickname:" + user.getNickname());
        }
    }

    return rows;
}
```

### 第七步：验证清单

生成验证清单，确保所有修改正确：

- [ ] 数据库字段添加成功（执行 SQL）
- [ ] Entity 类字段添加完整（包含注解）
- [ ] Mapper.xml 的 resultMap 更新
- [ ] Mapper.xml 的查询字段更新
- [ ] 查询条件添加（如果需要）
- [ ] 缓存清理逻辑添加（如果有缓存）
- [ ] 代码格式化（mvn spring-javaformat:apply）
- [ ] 编译通过（mvn clean compile）
- [ ] 功能测试通过

## 注意事项

### 1. 字段命名规范

- **Java 字段**：驼峰命名（camelCase）
  - 示例：`userName`、`createTime`、`orderStatus`
- **数据库字段**：下划线命名（snake_case）
  - 示例：`user_name`、`create_time`、`order_status`

### 2. 注解选择

- ✅ 使用 `@Schema`（io.swagger.v3.oas.annotations.media.Schema）
- ❌ 不使用 `@ApiModelProperty`（已废弃）
- ✅ 使用 Jakarta Validation 注解（`@NotBlank`、`@Size`、`@Email` 等）
- ✅ 日期字段必须添加 `@JsonFormat`

### 3. 缓存清理

- **何时需要清理缓存**：
  - 实体类有缓存（使用了 RedisUtils）
  - 新增字段可能影响缓存数据
  - 新增字段是查询条件

- **清理策略**：
  - 更新操作：清理受影响的缓存
  - 删除操作：清理所有相关缓存
  - 批量操作：批量清理缓存

### 4. 向下兼容

- 新增字段不要设置为 `NOT NULL`（除非有默认值）
- 新增字段不要影响已有功能
- 新增字段的查询条件要使用 `<if>` 标签（可选条件）

### 5. 性能考虑

- 避免添加过长的字段（VARCHAR 超过 1000）
- 避免添加过多的索引
- 如果是大字段（TEXT、BLOB），考虑单独存储

## 常见字段类型示例

### 字符串字段
```java
@Schema(description = "用户昵称")
@Size(max = 50, message = "昵称长度不能超过50个字符")
private String nickname;
```

### 整数字段
```java
@Schema(description = "年龄")
@Min(value = 0, message = "年龄不能小于0")
@Max(value = 150, message = "年龄不能大于150")
private Integer age;
```

### 金额字段
```java
@Schema(description = "订单金额")
@DecimalMin(value = "0.00", message = "金额不能小于0")
private BigDecimal amount;
```

### 日期字段
```java
@Schema(description = "最后登录时间")
@JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
private LocalDateTime lastLoginTime;
```

### 枚举字段
```java
@Schema(description = "用户状态（0-禁用，1-启用）")
private Integer status;
```

### 布尔字段
```java
@Schema(description = "是否VIP")
private Boolean isVip;
```

## 完整示例

### 示例：为 User 实体添加 nickname 字段

**1. 数据库 SQL**：
```sql
ALTER TABLE `sys_user`
ADD COLUMN `nickname` VARCHAR(50) NULL COMMENT '用户昵称'
AFTER `username`;
```

**2. Entity 类**：
```java
/**
 * 用户昵称
 */
@Schema(description = "用户昵称")
@Size(max = 50, message = "昵称长度不能超过50个字符")
private String nickname;
```

**3. Mapper.xml - resultMap**：
```xml
<result property="nickname" column="nickname" />
```

**4. Mapper.xml - 查询字段**：
```xml
<sql id="selectUserVo">
    select id, username, nickname, email, phone,
           create_time, update_time
    from sys_user
</sql>
```

**5. Mapper.xml - 查询条件**：
```xml
<if test="nickname != null and nickname != ''">
    and nickname like concat('%', #{nickname}, '%')
</if>
```

**6. Service - 缓存清理**：
```java
@Override
@Transactional(rollbackFor = Exception.class)
public int updateUser(User user) {
    int rows = baseMapper.updateById(user);
    if (rows > 0) {
        RedisUtils.deleteObject("user:info:" + user.getId());
    }
    return rows;
}
```

---

**版本**：1.0.0
**更新日期**：2026-01-23
