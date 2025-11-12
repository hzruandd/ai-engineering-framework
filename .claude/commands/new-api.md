---
description: 在已有模块中添加新的接口方法
---

# 添加新接口

我需要在已有模块中添加新的接口方法。

## 请先提供以下信息：

1. **实体类名称**（如：User）
2. **所属模块**（如：city-parking-eop）
3. **接口功能**（如：根据手机号查询用户）
4. **方法名称**（如：getByPhone）
5. **参数列表**（如：String phone）
6. **返回类型**（如：User、List<User>、PageInfo<User>）
7. **是否需要缓存**？
8. **是否需要防重复提交**？

## 开发步骤：

### Step 1: DubboApi接口中定义方法

```java
/**
 * 接口功能说明
 *
 * @param param 参数说明
 * @return 返回值说明
 */
ResponseResult<ReturnType> methodName(ParamType param);
```

### Step 2: DubboApiImpl中实现方法

**⚠️ 职责边界（重要）**：
- ✅ **DubboApi只是薄薄的接口层**，只负责：参数校验 → 调用Service → 返回结果
- ❌ **不要在DubboApi中写业务逻辑**（包括缓存处理、查询条件构建、循环处理等）
- ✅ **所有业务逻辑、缓存逻辑都必须放在Service层**

**基础实现（推荐）**：
```java
@Override
public ResponseResult<ReturnType> methodName(ParamType param) {
    // 1. 参数校验
    Preconditions.checkNotNull(param, "参数不能为null");

    // 2. 调用Service（所有业务逻辑在Service层）
    ReturnType result = xxxService.methodName(param);

    // 3. 返回结果
    return ResponseResult.success(result);
}
```

**❌ 错误示例：在DubboApi中处理缓存**：
```java
// ❌ 错误：缓存逻辑不应该在DubboApi层
@Override
public ResponseResult<User> getByPhone(String phone) {
    if (StringUtils.isBlank(phone)) {
        return ResponseResult.error("手机号不能为空");
    }

    // ❌ 错误：缓存逻辑应该在Service层
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

**✅ 正确做法：缓存逻辑在Service层**：
```java
// ✅ DubboApi层：只负责参数校验和调用Service
@Override
public ResponseResult<User> getByPhone(String phone) {
    Preconditions.checkArgument(StringUtils.isNotBlank(phone), "手机号不能为空");
    User user = userService.selectByPhone(phone);  // Service层处理缓存
    return ResponseResult.success(user);
}

// ✅ Service层：处理缓存逻辑（⚠️ 仅在满足缓存条件时使用）
@Override
public User selectByPhone(String phone) {
    // 先查缓存
    String cacheKey = "user:phone:" + phone;
    User user = RedisUtils.getCacheObject(cacheKey, User.class);

    if (user == null) {
        // 缓存未命中，查数据库
        user = baseMapper.selectByPhone(phone);
        if (user != null) {
            // 写入缓存，30分钟过期
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
public ResponseResult createOrder(Order order) {
    // 业务逻辑
    return ResponseResult.success();
}
```

**分布式锁**：
```java
@Autowired
private Locker locker;

@Override
public ResponseResult processOrder(String orderId) {
    String lockKey = "lock:order:" + orderId;
    try {
        boolean locked = locker.tryLock(lockKey, 10, 30, TimeUnit.SECONDS);
        if (!locked) {
            throw new BusinessException("系统繁忙，请稍后重试");
        }

        // 业务逻辑
        orderService.process(orderId);

        return ResponseResult.success();
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
        throw new BusinessException("操作被中断");
    } finally {
        locker.unlock(lockKey);
    }
}
```

### Step 3: Service接口中添加方法

```java
/**
 * 方法说明
 *
 * @param param 参数说明
 * @return 返回值说明
 */
ReturnType methodName(ParamType param);
```

### Step 4: ServiceImpl中实现方法

```java
@Override
public ReturnType methodName(ParamType param) {
    return baseMapper.methodName(param);
}
```

如果涉及更新/删除，添加事务和缓存清理：
```java
@Override
@Transactional(rollbackFor = Exception.class)
public int updateUser(User user) {
    int result = baseMapper.updateById(user);

    // 清理缓存
    if (result > 0 && StringUtils.isNotBlank(user.getPhone())) {
        RedisUtils.deleteObject("user:phone:" + user.getPhone());
    }

    return result;
}
```

### Step 5: Mapper接口中添加方法

```java
/**
 * 方法说明
 *
 * @param param 参数说明
 * @return 返回值说明
 */
ReturnType methodName(@Param("param") ParamType param);
```

### Step 6: Mapper.xml中编写SQL

```xml
<select id="methodName" parameterType="ParamType" resultMap="ResultMapName">
    select <include refid="selectXxxVo"/>
    where field_name = #{param}
    and del_flag = 0
</select>
```

## 常用SQL模板：

**单条查询**：
```xml
<select id="selectByPhone" resultMap="UserResult">
    select <include refid="selectUserVo"/>
    where phone = #{phone} and del_flag = 0
</select>
```

**列表查询**：
```xml
<select id="selectListByStatus" resultMap="UserResult">
    select <include refid="selectUserVo"/>
    <where>
        <if test="status != null">and status = #{status}</if>
        and del_flag = 0
    </where>
</select>
```

**更新**：
```xml
<update id="updateStatus">
    update user set status = #{status}, update_time = now()
    where id = #{id}
</update>
```

## 检查清单：

- [ ] DubboApi接口定义完整
- [ ] DubboApiImpl实现正确，返回ResponseResult
- [ ] Service接口和实现添加
- [ ] Mapper接口和XML添加
- [ ] 参数校验完整
- [ ] 缓存处理正确（如果需要）
- [ ] 事务注解添加（如果需要）
- [ ] 异常处理使用BusinessException

请根据提供的信息开始添加新接口。
