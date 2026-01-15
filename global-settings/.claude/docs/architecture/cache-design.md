# 缓存设计

## 何时使用缓存

**必须同时满足以下条件**：
- ✅ 查询频率高（>100次/分钟）
- ✅ 数据变更频率低（<10次/天）
- ✅ 数据量不大（单个对象<1MB）
- ✅ 可容忍短暂的数据不一致（秒级）

## Redis工具类

**位置**：`cn.city.parking.common.redis.RedisUtils`

### 核心方法
```java
// 存储对象
RedisUtils.setCacheObject(key, value);
RedisUtils.setCacheObject(key, value, timeout);  // 带过期时间（秒）

// 获取对象
Object obj = RedisUtils.getCacheObject(key);
User user = RedisUtils.getCacheObject(key, User.class);  // 带类型

// 删除
RedisUtils.deleteObject(key);
RedisUtils.batchDeleteObj(pattern);  // ⚠️ 慎用！会扫描全库

// 判断存在
boolean exists = RedisUtils.hasKey(key);
