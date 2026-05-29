# 快速参考

本文档提供常见错误对照表、快速决策指南和重要提醒。

## 目录

1. [常见错误对照表](#1-常见错误对照表)
2. [快速决策指南](#2-快速决策指南)
3. [重要提醒](#3-重要提醒)
4. [推荐工具类](#4-推荐工具类)

---

## 1. 常见错误对照表

| 错误写法 ❌ | 正确写法 ✅ | 原因 |
|------------|------------|------|
| 下游服务使用`@RestController` | 只在BFF层使用`@RestController` | 下游服务禁止暴露HTTP接口 |
| `package cn.city.parking.rbac.entity;` | `package cn.city.parking.rbac.api.entity;` | Entity必须在api包下 |
| `<artifactId>city-parking-common-core</artifactId>` | `<artifactId>city-parking-common-auth</artifactId>` | API模块依赖错误 |
| 重复添加Redis、Auth、MySQL、Druid依赖 | 只依赖common-server | common-server已包含 |
| `active: ${profiles.active:dev}` | `active: @profileActive@` | 占位符格式错误 |
| `server-addr: ${custom-config.server.nacos.address}` | `server-addr: ${nacos.server-addr}` | 占位符路径错误 |
| `import cn.city.parking.common.auth.base.BaseDubboApi;` | `import cn.city.parking.common.dubbo.filter.base.BaseDubboApi;` | 路径错误（旧路径已废弃） |
| `RedisUtils.deleteKeys("user:*");` | `RedisUtils.batchDeleteObj("user:*");` | 方法不存在 |
| `User user = RedisUtils.getCacheObject(key);` | `User user = RedisUtils.getCacheObject(key, User.class);` | 需要类型转换 |
| `ResponseResult getInfo(String id)` | `ResponseResult<User> getInfo(String id)` | 缺少泛型 |
| `@Mapper public interface UserMapper` | `public interface UserMapper` | 不需要@Mapper |
| `@Transactional` | `@Transactional(rollbackFor = Exception.class)` | 未指定rollbackFor |
| `public class User extends BusinessEntity` | `@TableName("sys_user") public class User extends BusinessEntity` | 缺少@TableName |
| 缺少mainClass配置 | `<mainClass>cn.city.parking.xxx.XxxApplication</mainClass>` | 无法打包jar |

---

## 2. 快速决策指南

### 何时使用 Redis 缓存？

**条件**（必须同时满足）：
- ✅ 查询频率 > 100次/分钟
- ✅ 数据变更频率 < 10次/天
- ✅ 数据量 < 1MB
- ✅ 可容忍短暂不一致

**适用场景**：
- ✅ 系统配置、字典数据、用户权限
- ❌ 订单信息、库存数据、金融数据

### 何时使用分布式锁？

**适用场景**：
- ✅ 库存扣减、优惠券领取、订单号生成、定时任务防重
- ❌ 普通查询、普通新增（ID用雪花算法）

**优先级**：数据库约束 > 乐观锁 > 分布式锁

### 何时使用事务？

**必须使用**：
- ✅ 所有增删改操作
- ✅ 批量操作
- ✅ 多表操作

**不需要使用**：
- ❌ 纯查询操作

### 何时记录日志？

**必须记录**：
- ✅ 用户操作（登录、下单、支付）
- ✅ 数据修改（CUD操作）
- ✅ 异常情况
- ✅ 外部接口调用

**不需要记录**：
- ❌ 普通查询
- ❌ 内部方法调用

---

## 3. 重要提醒

### 绝对不要做的事

#### 架构层面
1. **不要创建**：common包、utils包、BusinessException、ResponseResult（已有独立仓库）
2. **不要使用错误路径**：`cn.city.parking.common.auth.base.BaseDubboApi`（已废弃）
3. **不要使用不存在的方法**：`RedisUtils.deleteKeys()`（正确：`batchDeleteObj()`）
4. **下游服务禁止使用 `@RestController`**：只有BFF层可以暴露HTTP接口

#### 模块结构
5. **Entity包路径错误**：`cn.city.parking.xxx.entity`（正确：`cn.city.parking.xxx.api.entity`）
6. **API模块依赖错误**：依赖`city-parking-common-core`（正确：`city-parking-common-auth`）
7. **Server模块冗余依赖**：不要重复添加Redis、Auth、MySQL、Druid（common-server已包含）

#### 配置文件
8. **bootstrap.yml占位符错误**：`${custom-config.server.nacos.*}`（正确：`${nacos.*}`）
9. **profiles.active错误**：`${profiles.active:dev}`（正确：`@profileActive@`）

#### 代码规范
10. **不要在DubboApi中使用try-catch**（全局异常处理器会自动处理）
11. **不要随意捕获BusinessException**（业务异常必须向上抛出）
12. **不要忘记**：ResponseResult泛型、@TableName、@JsonFormat、@Transactional
13. **不要添加**：@Mapper、@EnableDubbo、@MapperScan（common-server已配置）
14. **不要随意使用Redis缓存**（如无必要，不要缓存）

### 必须做的事

1. **实体类**：
   - 继承BusinessEntity + @TableName + LocalDateTime字段@JsonFormat
   - Entity包路径必须在`xxx.api.entity`下（不是`xxx.entity`）
   - 如果数据库有create_by、update_by、del_flag、revision字段，必须在实体类中显式声明

2. **配置文件**：
   - 必须创建4个文件：bootstrap.yml + bootstrap-dev/prod/test.yml
   - 使用`@profileActive@`（不是`${profiles.active:dev}`）

3. **Service接口**：继承IService<T>

4. **Service实现**：增删改方法@Transactional(rollbackFor = Exception.class)

5. **DubboApi**：返回ResponseResult<T>带泛型 + 分页调用startDubboPage() + 参数校验

6. **关键操作**：添加日志（@Slf4j + log.info）

7. **方法注释**：JavaDoc格式（@param、@return）

8. **代码提交前**：mvn spring-javaformat:apply

---

## 4. 推荐工具类

### 字符串处理
```java
import org.apache.commons.lang3.StringUtils;

StringUtils.isNotBlank(str);
StringUtils.isEmpty(str);
StringUtils.join(list, ",");
```

### 日期处理
```java
import cn.hutool.core.date.DateUtil;

DateUtil.parse("2024-01-01");
DateUtil.format(date, "yyyy-MM-dd");
DateUtil.between(start, end, DateUnit.DAY);
```

### 集合处理
```java
import com.google.common.collect.*;

Lists.newArrayList();
Maps.newHashMap();
Sets.newHashSet();
```

### 参数校验
```java
import com.google.common.base.Preconditions;

Preconditions.checkArgument(condition, "错误信息");
Preconditions.checkNotNull(obj, "对象不能为空");
```

### Redis操作
```java
import cn.city.parking.common.redis.RedisUtils;

RedisUtils.setCacheObject(key, value, timeout);
RedisUtils.getCacheObject(key, Class.class);
RedisUtils.deleteObject(key);
```

### 分布式锁
```java
import cn.city.parking.common.redis.service.Locker;

@Autowired
private Locker locker;

locker.lock(lockKey, 10, () -> {
    // 业务逻辑
});
```

### 参数校验工具
```java
import cn.city.parking.common.core.utils.ValidateUtil;

ValidateUtil.validate(user);  // 自动校验所有注解
```

### 防重复提交
```java
import cn.city.parking.common.core.annotation.NoRepeatSubmit;

@NoRepeatSubmit(interval = 3000)  // 3秒内不允许重复提交
public ResponseResult<Integer> add(User user) {
    // ...
}
```

---

## 5. 快捷命令

使用 Claude Code 提供的快捷命令：

- `/new-crud` - 创建完整CRUD功能
- `/add-field` - 为实体类添加新字段
- `/new-api` - 在已有模块添加新接口
- `/fix-cache` - 修复缓存问题
- `/diff-report` - 生成代码修改报告（提交前自查）
- `/generate-tests` - 生成单元测试代码
- `/review-code` - 代码审查清单

---

**文档版本**：1.0
**最后更新**：2026-01-24
