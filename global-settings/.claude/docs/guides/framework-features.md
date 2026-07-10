# City Parking 框架功能详解

> 本文档详细说明 common-server 已自动配置的功能

**重要**：`city-parking-common-server` 已经自动配置了大量功能，无需在业务服务中重复配置。

## 1. 自动配置的注解

ServerStarterConfig 已配置以下注解，**业务服务启动类无需添加**：

```java
@EnableDubbo                     // ✅ 自动扫描Dubbo服务（cn.city.parking）
@EnableAsync                      // ✅ 自动启用异步任务支持
@MapperScan                      // ✅ 自动扫描Mapper接口（cn.city.parking.**.mapper）
@ComponentScan                   // ✅ 自动扫描Spring组件（cn.city.parking）
@EnableDiscoveryClient           // ✅ 自动启用Nacos服务发现
@EnableAspectJAutoProxy(exposeProxy = true)  // ✅ 启用AOP代理
```

## 2. 自动配置的线程池

框架提供了**3个线程池**，可直接使用：

### 主线程池（myThreadPoolTaskExecutor）

```java
@Autowired
@Qualifier("myThreadPoolTaskExecutor")
private ThreadPoolTaskExecutor executor;

// 使用示例
executor.execute(() -> {
    // 异步任务
});
```

**配置项**（Nacos配置中心 - custom-config.task.pool）：
- `core-size`：核心线程数（默认：4 * CPU核心数）
- `max-size`：最大线程数（默认：核心线程数 * 2）
- `queue-capacity`：队列容量（默认：200）
- `keep-alive`：空闲线程存活时间（默认：60s）
- `thread-name-prefix`：线程名称前缀（默认：my-task-executor-）
- `allow-core-thread-timeout`：是否允许核心线程超时（默认：false）

### TTL线程池（ttlExecutorService）

```java
@Autowired
@Qualifier("ttlExecutorService")
private ExecutorService ttlExecutorService;

// 支持上下文传递（ThreadLocal、InheritableThreadLocal）
```

### 用户任务线程池（userTaskThreadPool）

```java
@Autowired
@Qualifier("userTaskThreadPool")
private ThreadPoolTaskExecutor userTaskThreadPool;

// 支持SaToken上下文传递，用于需要登录用户信息的异步任务
```

## 3. 自动填充功能（MyMetaObjectHandler）

框架自动填充以下字段，**实体类无需手动赋值**：

### Insert时自动填充

```java
createTime   // Date类型，自动填充当前时间
updateTime   // Date类型，自动填充当前时间
createBy     // String类型，自动填充当前登录用户名（从SecurityContext获取）
delFlag      // Integer类型，自动填充0（未删除）
```

### Update时自动填充

```java
updateTime   // Date类型，自动填充当前时间
updateBy     // String类型，自动填充当前登录用户名（从SecurityContext获取）
```

**注意**：
- 字段名可通过Nacos配置自定义（custom-config.server）
- createBy/updateBy 在无登录用户时默认填充"系统"
- 实体类字段需要存在才会填充（BusinessEntity已包含基础字段）

## 4. ID生成策略（IdentifierGenerator）

框架自动生成主键ID，**无需手动设置**：

### 支持3种策略（通过Nacos配置 custom-config.server.id-type）

```yaml
# 雪花算法（默认，推荐）
id-type: snowflake

# Redis自增
id-type: redis-inc

# Seata兼容的雪花算法
id-type: snowflake-seata
```

### 雪花ID配置

```yaml
# 是否对ID低位随机化（分布式数据库分片场景）
id-random: false  # 默认false
```

**工作原理**：
- 雪花ID基于MAC地址或IP+端口生成workerId
- 自动处理时钟回拨（重新初始化Snowflake实例）
- 生成的ID是Long类型，实体类使用String存储

## 5. 批量操作（CustomSqlInjector）

框架注入了**批量插入方法**，Mapper继承CommonMapper即可使用：

```java
public interface UserMapper extends CommonMapper<User> {
    // 无需定义，框架自动注入
}

// 使用
List<User> userList = Arrays.asList(user1, user2, user3);
userMapper.insertBatchSomeColumn(userList);  // ✅ 批量插入（排除updateTime等UPDATE填充字段）
```

**注意事项**：
- 每批次建议控制在1000条以内
- 会自动处理createTime、createBy等INSERT填充字段
- 不会填充updateTime、updateBy等UPDATE填充字段

## 6. MyBatis Plus拦截器

框架自动配置了以下拦截器：

### 乐观锁拦截器（自动配置）

```java
// 实体类添加version字段
@Version
private Long revision;  // 乐观锁版本号

// 更新时自动处理
user.setRevision(1L);
userMapper.updateById(user);  // version会自动+1，并且WHERE条件会带上version=1
```

### 多租户拦截器（可选）

```java
// 需要在业务服务中配置TenantLineInnerInterceptor Bean
// 框架检测到该Bean后会自动加入拦截器链
```

## 7. 数据权限（可选）

框架支持数据权限控制，**按需配置**：

```java
// Mapper方法添加注解即可使用
@MyDataScope
List<User> selectUserList(User user);
```

**注意**：数据权限功能已内置到框架，直接在Mapper方法上使用`@MyDataScope`注解即可，**无需在启动类添加任何注解**。

## 8. Jackson时区配置

框架自动配置Jackson使用系统默认时区，**Date/LocalDateTime等时间类型自动处理**。

## 9. Sentinel降级异常处理

框架自动配置了MyWebMvcBlockExceptionHandler，处理Sentinel限流降级异常。

## 10. 配置项汇总

**Nacos配置中心** - custom-config.server：

```yaml
custom-config:
  server:
    id-type: snowflake              # ID生成策略（snowflake/redis-inc/snowflake-seata）
    id-random: false                # 雪花ID是否低位随机化
    create-time-field: createTime   # 创建时间字段名
    update-time-field: updateTime   # 更新时间字段名
    del-flag-field: delFlag         # 逻辑删除字段名
    create-by-field: createBy       # 创建人字段名
    update-by-field: updateBy       # 更新人字段名
    uuid-binary: false              # 是否启用UUID Binary类型处理
  task:
    pool:
      core-size: 16                 # 核心线程数（默认4*CPU核心数）
      max-size: 32                  # 最大线程数（默认核心数*2）
      queue-capacity: 200           # 队列容量
      keep-alive: 60s               # 空闲线程存活时间
      thread-name-prefix: my-task-executor-
      allow-core-thread-timeout: false
```
