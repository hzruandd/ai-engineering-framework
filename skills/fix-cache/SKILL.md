---
name: fix-cache
description: 为已有功能添加缓存或修复缓存问题，包括缓存设计、缓存更新、缓存清理等。适用于性能优化、热点数据缓存、缓存问题修复等场景。
argument-hint: [类名] [方法名]
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# 为功能添加缓存或修复缓存问题

为已有功能添加缓存或修复缓存相关问题，提升系统性能。

## 使用方式

```bash
# 为指定方法添加缓存
/fix-cache UserService.selectByPhone

# 修复缓存问题
/fix-cache UserService --fix

# 分析缓存使用情况
/fix-cache --analyze
```

## 何时使用缓存

**⚠️ 核心原则**：如无必要，不要缓存

**必须同时满足以下条件**：
- ✅ 查询频率 > 100 次/分钟
- ✅ 数据变更频率 < 10 次/天
- ✅ 数据量 < 1MB
- ✅ 可容忍短暂不一致

**适合缓存的场景**：
- ✅ 系统配置、字典数据
- ✅ 用户权限信息
- ✅ 热点商品信息
- ✅ 统计数据（可容忍延迟）

**不适合缓存的场景**：
- ❌ 订单信息（实时性要求高）
- ❌ 库存数据（一致性要求高）
- ❌ 金融数据（准确性要求高）
- ❌ 低频查询数据

## 执行流程

### 第一步：分析是否需要缓存

1. **查询频率分析**：
   - 查看日志，统计方法调用频率
   - 使用监控工具（如 Prometheus）查看 QPS

2. **数据变更频率分析**：
   - 查看数据库更新日志
   - 分析业务场景

3. **数据量分析**：
   - 查看数据大小
   - 评估 Redis 内存占用

4. **一致性要求分析**：
   - 评估业务对数据一致性的要求
   - 确定可容忍的延迟时间

### 第二步：设计缓存方案

#### 2.1 缓存 Key 设计

**规范**：`{业务模块}:{数据类型}:{唯一标识}`

**示例**：
```java
// 用户信息缓存
String cacheKey = "user:info:" + userId;

// 用户手机号缓存
String cacheKey = "user:phone:" + phone;

// 订单列表缓存
String cacheKey = "order:list:" + userId + ":" + status;

// 统计数据缓存
String cacheKey = "stats:daily:" + date;
```

**注意事项**：
- Key 要有明确的业务含义
- Key 要包含唯一标识
- Key 要便于批量删除（使用通配符）

#### 2.2 缓存过期时间设计

**规范**：根据数据特性设置合理的过期时间

**示例**：
```java
// 用户信息：30 分钟
RedisUtils.setCacheObject(cacheKey, user, 30L, TimeUnit.MINUTES);

// 系统配置：1 小时
RedisUtils.setCacheObject(cacheKey, config, 1L, TimeUnit.HOURS);

// 统计数据：1 天
RedisUtils.setCacheObject(cacheKey, stats, 1L, TimeUnit.DAYS);

// 热点数据：5 分钟
RedisUtils.setCacheObject(cacheKey, data, 5L, TimeUnit.MINUTES);
```

**注意事项**：
- 过期时间不要太长（避免数据过期）
- 过期时间不要太短（避免频繁查询数据库）
- 可以添加随机时间（避免缓存雪崩）

#### 2.3 缓存更新策略

**推荐策略**：Cache Aside Pattern（旁路缓存）

**读取流程**：
1. 先查缓存
2. 缓存命中，直接返回
3. 缓存未命中，查数据库
4. 将数据写入缓存
5. 返回数据

**更新流程**：
1. 先更新数据库
2. 再删除缓存

**⚠️ 不要使用以下策略**：
- ❌ 先删除缓存，再更新数据库（可能导致脏数据）
- ❌ 先更新数据库，再更新缓存（可能导致缓存不一致）

### 第三步：在 Service 层添加缓存

**位置**：`{module}-server/src/main/java/cn/city/parking/{module}/service/impl/{ClassName}ServiceImpl.java`

#### 3.1 查询方法添加缓存

```java
@Override
public User selectByPhone(String phone) {
    // 1. 先查缓存
    String cacheKey = "user:phone:" + phone;
    User user = RedisUtils.getCacheObject(cacheKey, User.class);

    if (user == null) {
        // 2. 缓存未命中，查数据库
        user = baseMapper.selectByPhone(phone);

        if (user != null) {
            // 3. 写入缓存，30 分钟过期
            RedisUtils.setCacheObject(cacheKey, user, 30L, TimeUnit.MINUTES);
        }
    }

    return user;
}
```

#### 3.2 更新方法清理缓存

```java
@Override
@Transactional(rollbackFor = Exception.class)
public int updateUser(User user) {
    // 1. 先更新数据库
    int rows = baseMapper.updateById(user);

    // 2. 再删除缓存
    if (rows > 0) {
        // 清理用户信息缓存
        RedisUtils.deleteObject("user:info:" + user.getId());

        // 清理手机号缓存
        if (StringUtils.isNotBlank(user.getPhone())) {
            RedisUtils.deleteObject("user:phone:" + user.getPhone());
        }

        // 清理邮箱缓存
        if (StringUtils.isNotBlank(user.getEmail())) {
            RedisUtils.deleteObject("user:email:" + user.getEmail());
        }
    }

    return rows;
}
```

#### 3.3 删除方法清理缓存

```java
@Override
@Transactional(rollbackFor = Exception.class)
public int deleteUserById(String id) {
    // 1. 先查询用户信息（用于清理缓存）
    User user = baseMapper.selectById(id);

    // 2. 删除数据库记录
    int rows = baseMapper.deleteById(id);

    // 3. 清理缓存
    if (rows > 0 && user != null) {
        RedisUtils.deleteObject("user:info:" + id);

        if (StringUtils.isNotBlank(user.getPhone())) {
            RedisUtils.deleteObject("user:phone:" + user.getPhone());
        }

        if (StringUtils.isNotBlank(user.getEmail())) {
            RedisUtils.deleteObject("user:email:" + user.getEmail());
        }
    }

    return rows;
}
```

### 第四步：处理缓存问题

#### 4.1 缓存穿透

**问题**：查询不存在的数据，导致每次都查询数据库

**解决方案**：缓存空对象

```java
@Override
public User selectByPhone(String phone) {
    String cacheKey = "user:phone:" + phone;
    User user = RedisUtils.getCacheObject(cacheKey, User.class);

    if (user == null) {
        user = baseMapper.selectByPhone(phone);

        if (user != null) {
            // 缓存正常数据，30 分钟
            RedisUtils.setCacheObject(cacheKey, user, 30L, TimeUnit.MINUTES);
        } else {
            // 缓存空对象，5 分钟（防止穿透）
            RedisUtils.setCacheObject(cacheKey, new User(), 5L, TimeUnit.MINUTES);
        }
    }

    // 返回前判断是否为空对象
    return user.getId() != null ? user : null;
}
```

#### 4.2 缓存击穿

**问题**：热点数据过期，大量请求同时查询数据库

**解决方案**：使用分布式锁

```java
@Autowired
private Locker locker;

@Override
public User selectByPhone(String phone) {
    String cacheKey = "user:phone:" + phone;
    User user = RedisUtils.getCacheObject(cacheKey, User.class);

    if (user == null) {
        // 使用分布式锁
        String lockKey = "lock:user:phone:" + phone;
        try {
            boolean locked = locker.tryLock(lockKey, 10, 30, TimeUnit.SECONDS);
            if (locked) {
                // 再次检查缓存（双重检查）
                user = RedisUtils.getCacheObject(cacheKey, User.class);
                if (user == null) {
                    user = baseMapper.selectByPhone(phone);
                    if (user != null) {
                        RedisUtils.setCacheObject(cacheKey, user, 30L, TimeUnit.MINUTES);
                    }
                }
            } else {
                // 获取锁失败，等待后重试
                Thread.sleep(100);
                return selectByPhone(phone);
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new BusinessException("系统繁忙，请稍后重试");
        } finally {
            locker.unlock(lockKey);
        }
    }

    return user;
}
```

#### 4.3 缓存雪崩

**问题**：大量缓存同时过期，导致数据库压力骤增

**解决方案**：过期时间添加随机值

```java
@Override
public User selectByPhone(String phone) {
    String cacheKey = "user:phone:" + phone;
    User user = RedisUtils.getCacheObject(cacheKey, User.class);

    if (user == null) {
        user = baseMapper.selectByPhone(phone);
        if (user != null) {
            // 30 分钟 + 随机 0-5 分钟
            long expireTime = 30 + new Random().nextInt(5);
            RedisUtils.setCacheObject(cacheKey, user, expireTime, TimeUnit.MINUTES);
        }
    }

    return user;
}
```

### 第五步：验证缓存效果

#### 5.1 验证缓存命中

```java
// 添加日志
log.info("查询用户，手机号：{}，缓存命中：{}", phone, user != null);
```

#### 5.2 监控缓存命中率

```bash
# 查看 Redis 统计信息
redis-cli info stats

# 查看缓存命中率
keyspace_hits / (keyspace_hits + keyspace_misses)
```

#### 5.3 性能对比

- 查询响应时间对比
- 数据库查询次数对比
- 系统 QPS 对比

## 常见缓存模式

### 1. Cache Aside（旁路缓存）

**适用场景**：读多写少

**读取**：先查缓存，未命中查数据库，写入缓存
**更新**：先更新数据库，再删除缓存

### 2. Read Through（读穿透）

**适用场景**：读多写少，缓存层封装

**读取**：缓存层自动加载数据
**更新**：缓存层自动更新

### 3. Write Through（写穿透）

**适用场景**：写多读少

**读取**：先查缓存
**更新**：先更新缓存，缓存层更新数据库

### 4. Write Behind（写回）

**适用场景**：写多读少，可容忍数据丢失

**读取**：先查缓存
**更新**：先更新缓存，异步更新数据库

## 缓存最佳实践

### 1. 缓存粒度

- ✅ 缓存单个对象（user:info:1）
- ✅ 缓存列表（user:list:status:1）
- ❌ 不要缓存整个表

### 2. 缓存时间

- ✅ 根据业务特性设置
- ✅ 添加随机时间（防止雪崩）
- ❌ 不要设置永久缓存

### 3. 缓存更新

- ✅ 先更新数据库，再删除缓存
- ❌ 不要先删除缓存，再更新数据库
- ❌ 不要先更新数据库，再更新缓存

### 4. 缓存清理

- ✅ 更新/删除时清理相关缓存
- ✅ 使用通配符批量清理（谨慎使用）
- ❌ 不要忘记清理缓存

### 5. 缓存监控

- ✅ 监控缓存命中率
- ✅ 监控缓存内存使用
- ✅ 监控缓存过期情况

## 注意事项

1. **不要滥用缓存**：只在必要时使用缓存
2. **缓存一致性**：确保缓存与数据库一致
3. **缓存穿透**：防止查询不存在的数据
4. **缓存击穿**：防止热点数据过期
5. **缓存雪崩**：防止大量缓存同时过期
6. **内存管理**：控制缓存大小，避免内存溢出
7. **序列化**：注意对象序列化问题

## 检查清单

- [ ] 确认是否满足缓存使用条件
- [ ] 设计合理的缓存 Key
- [ ] 设置合理的过期时间
- [ ] 在 Service 层添加缓存逻辑
- [ ] 更新/删除方法清理缓存
- [ ] 处理缓存穿透、击穿、雪崩
- [ ] 添加缓存监控和日志
- [ ] 验证缓存效果

---

**版本**：1.0.0
**更新日期**：2026-01-23
