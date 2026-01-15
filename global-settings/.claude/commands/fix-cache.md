---
description: 为已有功能添加缓存或修复缓存问题
---

# 缓存优化

我需要为已有功能添加缓存或修复缓存问题。

## ⚠️ 重要：何时使用缓存

**核心原则：❌ 不要随意使用Redis缓存（如无必要，不要缓存）**

### 使用缓存的条件（必须同时满足）：
- ✅ 查询频率高（>100次/分钟）
- ✅ 数据变更频率低（<10次/天）
- ✅ 数据量不大（单个对象<1MB）
- ✅ 可容忍短暂的数据不一致（秒级）

### 典型场景：
- ✅ **适合缓存**：系统配置、字典数据、用户基本信息（变更少）、热点商品详情
- ❌ **不适合缓存**：订单列表（查询条件多变）、实时库存（强一致性要求）、金融数据（不允许不一致）

**如果不满足以上条件，请勿添加缓存！**

---

## 请先确认：

1. **实体类名称**（如：User）
2. **所属模块**（如：city-parking-eop）
3. **是否满足缓存使用条件**（见上方）
4. **需要缓存的场景**：
   - 查询操作（添加读缓存）
   - 更新操作（清理缓存）
   - 删除操作（清理缓存）
5. **缓存过期时间**（如：30分钟）

## 缓存设计原则：

### 缓存Key命名规范
```
{模块}:{实体}:{标识}:{值}

示例：
user:id:123456
user:phone:13800138000
parking:lot:code:P001
menu:tree:all
```

### 过期时间建议
- **热点数据**：5-30分钟（如用户信息、菜单树）
- **配置数据**：1-24小时（如字典、常量）
- **Token类**：与业务一致（如2小时）
- **计数器**：根据业务（如1分钟）

## 操作步骤：

### Step 1: 查询添加缓存

**方案A：先查缓存，未命中查数据库**（推荐）
```java
@Override
public ResponseResult<User> getByPhone(String phone) {
    if (StringUtils.isBlank(phone)) {
        return ResponseResult.error("手机号不能为空");
    }

    // 1. 先查缓存
    String cacheKey = "user:phone:" + phone;
    User user = RedisUtils.getCacheObject(cacheKey, User.class);

    // 2. 缓存未命中，查数据库
    if (user == null) {
        user = userService.selectByPhone(phone);

        // 3. 写入缓存
        if (user != null) {
            RedisUtils.setCacheObject(cacheKey, user, 30L, TimeUnit.MINUTES);
        }
    }

    return ResponseResult.success(user);
}
```

**方案B：使用Guava Cache本地缓存**（配置、常量等不常变动的数据）
```java
// 定义缓存
private static final LoadingCache<String, List<Dict>> DICT_CACHE = CacheBuilder.newBuilder()
    .maximumSize(100)
    .expireAfterWrite(1, TimeUnit.HOURS)
    .build(new CacheLoader<String, List<Dict>>() {
        @Override
        public List<Dict> load(String dictType) throws Exception {
            return dictMapper.selectByType(dictType);
        }
    });

// 使用缓存
@Override
public List<Dict> getDictByType(String dictType) {
    try {
        return DICT_CACHE.get(dictType);
    } catch (ExecutionException e) {
        throw new BusinessException("获取字典失败");
    }
}
```

### Step 2: 更新操作清理缓存

```java
@Override
@Transactional(rollbackFor = Exception.class)
public ResponseResult updateUser(User user) {
    // 参数校验
    if (user.getId() == null) {
        return ResponseResult.error("用户ID不能为空");
    }

    // 执行更新
    int result = userService.updateUser(user);

    // 清理缓存
    if (result > 0) {
        // 根据ID清理
        RedisUtils.deleteObject("user:id:" + user.getId());

        // 根据手机号清理
        if (StringUtils.isNotBlank(user.getPhone())) {
            RedisUtils.deleteObject("user:phone:" + user.getPhone());
        }

        // 批量清理（使用模糊匹配）
        // 注意：谨慎使用，影响性能
        // RedisUtils.batchDeleteObj("user:*");
    }

    return ResponseResult.getBooleanResult(result);
}
```

### Step 3: 删除操作清理缓存

```java
@Override
@Transactional(rollbackFor = Exception.class)
public ResponseResult remove(String[] ids) {
    // 先删除缓存
    for (String id : ids) {
        RedisUtils.deleteObject("user:id:" + id);
    }

    // 再删除数据
    int result = userService.deleteUserByIds(ids);

    return ResponseResult.getBooleanResult(result);
}
```

## 缓存常见问题排查：

### 问题1：缓存不生效

**检查清单**：
- [ ] Redis是否启动？
- [ ] Redis配置是否正确？
- [ ] 缓存key是否正确？
- [ ] 对象是否可序列化？
- [ ] 过期时间是否设置？

**解决方案**：
```java
// 检查Redis连接
Boolean hasKey = RedisUtils.hasKey("test");

// 查看过期时间
Long ttl = RedisUtils.getExpire("user:id:123");

// 手动测试存取
RedisUtils.setCacheObject("test", "value", 60L, TimeUnit.SECONDS);
String value = RedisUtils.getStr("test");
```

### 问题2：缓存不一致

**检查清单**：
- [ ] 更新/删除时是否清理了缓存？
- [ ] 多个缓存key是否都清理了？
- [ ] 是否存在缓存穿透？

**解决方案**：
```java
// 确保所有相关缓存都清理
private void clearUserCache(User user) {
    RedisUtils.deleteObject("user:id:" + user.getId());
    if (StringUtils.isNotBlank(user.getPhone())) {
        RedisUtils.deleteObject("user:phone:" + user.getPhone());
    }
    if (StringUtils.isNotBlank(user.getEmail())) {
        RedisUtils.deleteObject("user:email:" + user.getEmail());
    }
}
```

### 问题3：缓存雪崩

**场景**：大量缓存同时过期

**解决方案**：
```java
// 随机过期时间（30分钟 ± 5分钟）
long expire = 30 + ThreadLocalRandom.current().nextInt(-5, 5);
RedisUtils.setCacheObject(key, value, expire, TimeUnit.MINUTES);
```

### 问题4：缓存穿透

**场景**：查询不存在的数据，每次都打DB

**解决方案**：
```java
// 不存在的数据也缓存（设置短过期时间）
User user = userService.selectByPhone(phone);
if (user == null) {
    // 缓存空对象，5分钟过期
    RedisUtils.setCacheObject(cacheKey, new User(), 5L, TimeUnit.MINUTES);
} else {
    RedisUtils.setCacheObject(cacheKey, user, 30L, TimeUnit.MINUTES);
}
```

## 缓存最佳实践：

1. **缓存粒度**：单个对象 > 列表（列表缓存更新复杂）
2. **过期时间**：设置合理过期时间，避免缓存雪崩
3. **缓存清理**：更新/删除时必须清理缓存
4. **空值缓存**：防止缓存穿透
5. **监控告警**：监控缓存命中率

## 检查清单：

- [ ] 缓存key命名规范
- [ ] 过期时间设置合理
- [ ] 更新/删除操作清理缓存
- [ ] 空值缓存防穿透
- [ ] 异常情况处理

请根据实际情况添加或修复缓存。
