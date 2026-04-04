---
name: new-api
description: 在已有模块中添加新的接口方法（DubboApi + Service + Mapper），支持缓存、防重复提交、分布式锁等功能。适用于扩展现有模块功能、添加新的业务接口等场景。
argument-hint: [实体类名] [方法名] [功能描述]
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# 在已有模块中添加新接口

在已有模块中添加新的接口方法，包含 DubboApi、Service、Mapper 三层代码。

## 使用方式

```bash
# 基础用法（交互式）
/new-api

# 指定实体类和方法名
/new-api User getByPhone

# 完整参数
/new-api User getByPhone 根据手机号查询用户
```

## 参数说明

如果使用 `$ARGUMENTS`，格式为：`实体类名 方法名 功能描述`

示例：
- `User getByPhone 根据手机号查询用户`
- `Order getByStatus 根据状态查询订单列表`

## 执行流程

### 第一步：收集信息

如果未提供完整参数，交互式收集以下信息：

1. **实体类名称**（如：User）
2. **所属模块**（如：city-parking-eop）
3. **接口功能**（如：根据手机号查询用户）
4. **方法名称**（如：getByPhone）
5. **参数列表**（如：String phone）
6. **返回类型**（如：User、List<User>、PageInfo<User>）
7. **是否需要缓存**？
8. **是否需要防重复提交**？
9. **是否需要分布式锁**？

### 第二步：在 DubboApi 接口中定义方法

**位置**：`{module}-api/src/main/java/cn/city/parking/{module}/api/{ClassName}DubboApi.java`

**模板**：
```java
/**
 * {接口功能说明}
 *
 * @param param 参数说明
 * @return 返回值说明
 */
ResponseResult<ReturnType> methodName(ParamType param);
```

**示例**：
```java
/**
 * 根据手机号查询用户
 *
 * @param phone 手机号
 * @return 用户信息
 */
ResponseResult<User> getByPhone(String phone);
```

### 第三步：在 DubboApiImpl 中实现方法

**位置**：`{module}-server/src/main/java/cn/city/parking/{module}/dubbo/{ClassName}DubboApiImpl.java`

**⚠️ 职责边界（重要）**：
- ✅ **DubboApi 只是薄薄的接口层**，只负责：参数校验 → 调用 Service → 返回结果
- ❌ **不要在 DubboApi 中写业务逻辑**（包括缓存处理、查询条件构建、循环处理等）
- ✅ **所有业务逻辑、缓存逻辑都必须放在 Service 层**

**基础实现（推荐）**：
```java
@Override
public ResponseResult<User> getByPhone(String phone) {
    // 1. 参数校验
    Preconditions.checkArgument(StringUtils.isNotBlank(phone), "手机号不能为空");

    // 2. 调用 Service（所有业务逻辑在 Service 层）
    User user = userService.selectByPhone(phone);

    // 3. 返回结果
    return ResponseResult.success(user);
}
```

**❌ 错误示例：在 DubboApi 中处理缓存**：
```java
// ❌ 错误：缓存逻辑不应该在 DubboApi 层
@Override
public ResponseResult<User> getByPhone(String phone) {
    if (StringUtils.isBlank(phone)) {
        return ResponseResult.error("手机号不能为空");
    }

    // ❌ 错误：缓存逻辑应该在 Service 层
    String cacheKey = "user:phone:" + phone;
    User user = RedisUtils.getCacheObject(cacheKey, User.class);

    if (user == null) {
        user = userService.selectByPhone(phone);
        if (user != null) {
            RedisUtils.setCacheObject(cacheKey, user, 30L, TimeUnit.MINUTES);
        }
    }

    return ResponseResult.success(user);
}
```

**✅ 正确做法：缓存逻辑在 Service 层**：
```java
// ✅ DubboApi 层：只负责参数校验和调用 Service
@Override
public ResponseResult<User> getByPhone(String phone) {
    Preconditions.checkArgument(StringUtils.isNotBlank(phone), "手机号不能为空");
    User user = userService.selectByPhone(phone);  // Service 层处理缓存
    return ResponseResult.success(user);
}

// ✅ Service 层：处理缓存逻辑（⚠️ 仅在满足缓存条件时使用）
@Override
public User selectByPhone(String phone) {
    // 先查缓存
    String cacheKey = "user:phone:" + phone;
    User user = RedisUtils.getCacheObject(cacheKey, User.class);

    if (user == null) {
        // 缓存未命中，查数据库
        user = baseMapper.selectByPhone(phone);
        if (user != null) {
            // 写入缓存，30 分钟过期
            RedisUtils.setCacheObject(cacheKey, user, 30L, TimeUnit.MINUTES);
        }
    }

    return user;
}
```

**防重复提交**：
```java
@NoRepeatSubmit(leaseTime = 5, timeUnit = TimeUnit.SECONDS, message = "请勿重复提交")
@Override
public ResponseResult<Integer> createOrder(Order order) {
    Preconditions.checkNotNull(order, "订单信息不能为空");
    int rows = orderService.insertOrder(order);
    return ResponseResult.success(rows);
}
```

**分布式锁**：
```java
@Autowired
private Locker locker;

@Override
public ResponseResult<Integer> processOrder(String orderId) {
    Preconditions.checkArgument(StringUtils.isNotBlank(orderId), "订单ID不能为空");

    String lockKey = "lock:order:" + orderId;
    try {
        boolean locked = locker.tryLock(lockKey, 10, 30, TimeUnit.SECONDS);
        if (!locked) {
            throw new BusinessException("系统繁忙，请稍后重试");
        }

        // 调用 Service 处理业务逻辑
        int rows = orderService.process(orderId);

        return ResponseResult.success(rows);
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
        throw new BusinessException("操作被中断");
    } finally {
        locker.unlock(lockKey);
    }
}
```

### 第四步：在 Service 接口中添加方法

**位置**：`{module}-server/src/main/java/cn/city/parking/{module}/service/I{ClassName}Service.java`

**模板**：
```java
/**
 * {方法说明}
 *
 * @param param 参数说明
 * @return 返回值说明
 */
ReturnType methodName(ParamType param);
```

**示例**：
```java
/**
 * 根据手机号查询用户
 *
 * @param phone 手机号
 * @return 用户信息
 */
User selectByPhone(String phone);
```

### 第五步：在 ServiceImpl 中实现方法

**位置**：`{module}-server/src/main/java/cn/city/parking/{module}/service/impl/{ClassName}ServiceImpl.java`

**基础实现**：
```java
@Override
public User selectByPhone(String phone) {
    return baseMapper.selectByPhone(phone);
}
```

**带缓存的实现**（⚠️ 仅在满足缓存条件时使用）：
```java
@Override
public User selectByPhone(String phone) {
    // 先查缓存
    String cacheKey = "user:phone:" + phone;
    User user = RedisUtils.getCacheObject(cacheKey, User.class);

    if (user == null) {
        // 缓存未命中，查数据库
        user = baseMapper.selectByPhone(phone);
        if (user != null) {
            // 写入缓存，30 分钟过期
            RedisUtils.setCacheObject(cacheKey, user, 30L, TimeUnit.MINUTES);
        }
    }

    return user;
}
```

**涉及更新/删除，添加事务和缓存清理**：
```java
@Override
@Transactional(rollbackFor = Exception.class)
public int updateUser(User user) {
    int result = baseMapper.updateById(user);

    // 清理缓存
    if (result > 0) {
        // 清理用户信息缓存
        RedisUtils.deleteObject("user:info:" + user.getId());

        // 清理手机号缓存
        if (StringUtils.isNotBlank(user.getPhone())) {
            RedisUtils.deleteObject("user:phone:" + user.getPhone());
        }
    }

    return result;
}
```

### 第六步：在 Mapper 接口中添加方法

**位置**：`{module}-server/src/main/java/cn/city/parking/{module}/mapper/{ClassName}Mapper.java`

**模板**：
```java
/**
 * {方法说明}
 *
 * @param param 参数说明
 * @return 返回值说明
 */
ReturnType methodName(@Param("param") ParamType param);
```

**示例**：
```java
/**
 * 根据手机号查询用户
 *
 * @param phone 手机号
 * @return 用户信息
 */
User selectByPhone(@Param("phone") String phone);
```

### 第七步：在 Mapper.xml 中编写 SQL

**位置**：`{module}-server/src/main/resources/mapper/{ClassName}Mapper.xml`

**单条查询**：
```xml
<select id="selectByPhone" resultMap="UserResult">
    <include refid="selectUserVo"/>
    where phone = #{phone} and del_flag = 0
</select>
```

**列表查询**：
```xml
<select id="selectListByStatus" resultMap="UserResult">
    <include refid="selectUserVo"/>
    <where>
        <if test="status != null">and status = #{status}</if>
        and del_flag = 0
    </where>
    order by create_time desc
</select>
```

**更新**：
```xml
<update id="updateStatus">
    update sys_user
    set status = #{status}, update_time = now()
    where id = #{id}
</update>
```

**删除**：
```xml
<delete id="deleteByPhone">
    delete from sys_user
    where phone = #{phone}
</delete>
```

**统计**：
```xml
<select id="countByStatus" resultType="java.lang.Long">
    select count(1)
    from sys_user
    where status = #{status} and del_flag = 0
</select>
```

## 常用 SQL 模板

### 1. 精确匹配查询
```xml
<select id="selectByField" resultMap="ResultMap">
    <include refid="selectVo"/>
    where field_name = #{fieldValue} and del_flag = 0
</select>
```

### 2. 模糊查询
```xml
<select id="selectByKeyword" resultMap="ResultMap">
    <include refid="selectVo"/>
    <where>
        <if test="keyword != null and keyword != ''">
            and (field1 like concat('%', #{keyword}, '%')
            or field2 like concat('%', #{keyword}, '%'))
        </if>
        and del_flag = 0
    </where>
</select>
```

### 3. 范围查询
```xml
<select id="selectByRange" resultMap="ResultMap">
    <include refid="selectVo"/>
    <where>
        <if test="minValue != null">and field_name &gt;= #{minValue}</if>
        <if test="maxValue != null">and field_name &lt;= #{maxValue}</if>
        and del_flag = 0
    </where>
</select>
```

### 4. IN 查询
```xml
<select id="selectByIds" resultMap="ResultMap">
    <include refid="selectVo"/>
    where id in
    <foreach collection="ids" item="id" open="(" separator="," close=")">
        #{id}
    </foreach>
    and del_flag = 0
</select>
```

### 5. 日期范围查询
```xml
<select id="selectByDateRange" resultMap="ResultMap">
    <include refid="selectVo"/>
    <where>
        <if test="params.beginTime != null and params.beginTime != ''">
            and date_format(create_time,'%Y-%m-%d') &gt;= date_format(#{params.beginTime},'%Y-%m-%d')
        </if>
        <if test="params.endTime != null and params.endTime != ''">
            and date_format(create_time,'%Y-%m-%d') &lt;= date_format(#{params.endTime},'%Y-%m-%d')
        </if>
        and del_flag = 0
    </where>
</select>
```

### 6. 批量插入
```xml
<insert id="batchInsert">
    insert into table_name (field1, field2, field3)
    values
    <foreach collection="list" item="item" separator=",">
        (#{item.field1}, #{item.field2}, #{item.field3})
    </foreach>
</insert>
```

### 7. 批量更新
```xml
<update id="batchUpdate">
    <foreach collection="list" item="item" separator=";">
        update table_name
        set field1 = #{item.field1}, field2 = #{item.field2}
        where id = #{item.id}
    </foreach>
</update>
```

## 检查清单

生成代码后，检查以下内容：

- [ ] DubboApi 接口定义完整
- [ ] DubboApiImpl 实现正确，返回 ResponseResult
- [ ] DubboApiImpl 保持薄层，不包含业务逻辑
- [ ] Service 接口和实现添加
- [ ] Mapper 接口和 XML 添加
- [ ] 参数校验完整（使用 Preconditions）
- [ ] 缓存处理正确（如果需要，在 Service 层）
- [ ] 事务注解添加（如果需要）
- [ ] 异常处理使用 BusinessException
- [ ] 代码格式化（mvn spring-javaformat:apply）

## 注意事项

### 1. 职责边界

- **DubboApi 层**：只负责参数校验、调用 Service、返回结果
- **Service 层**：处理所有业务逻辑、缓存逻辑、事务控制
- **Mapper 层**：只负责数据库操作

### 2. 缓存使用

**何时使用缓存**（必须同时满足）：
- ✅ 查询频率 > 100 次/分钟
- ✅ 数据变更频率 < 10 次/天
- ✅ 数据量 < 1MB
- ✅ 可容忍短暂不一致

**缓存更新策略**：
- 先更新数据库，再删除缓存
- 不要使用"先删除缓存，再更新数据库"

### 3. 分布式锁使用

**何时使用分布式锁**：
- ✅ 库存扣减
- ✅ 优惠券领取
- ✅ 订单号生成
- ✅ 定时任务防重

**优先级**：数据库约束 > 乐观锁 > 分布式锁

### 4. 事务使用

**必须使用事务**：
- 所有增删改操作
- 批量操作
- 多表操作

**不需要事务**：
- 纯查询操作

---

**版本**：1.0.0
**更新日期**：2026-01-23
