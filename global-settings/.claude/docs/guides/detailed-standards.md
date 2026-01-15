# City Parking 详细规范说明

> 本文档包含异步任务、API幂等性、Mapper继承、性能优化和分布式事务的详细规范

## 1. 异步任务使用规范

框架提供了**3个线程池**（详见 [framework-features.md](framework-features.md#2-自动配置的线程池)），需根据场景选择合适的线程池。

### 1.1 线程池选择场景

| 线程池 | Bean名称 | 使用场景 | MDC传递 | 示例 |
|--------|---------|---------|---------|------|
| 主线程池 | myThreadPoolTaskExecutor | 普通异步任务（不需要traceId） | ❌ 不传递 | 发送邮件、生成报表（无需链路追踪） |
| TTL线程池 | ttlExecutorService | 需要链路追踪 | ✅ 自动传递MDC（traceId、username、platform） | 异步记录操作日志、需要traceId的任务 |
| 用户任务线程池 | userTaskThreadPool | 需要登录信息 | ✅ 传递SaToken上下文 | 异步操作需要用户名 |

**重要提示**：
- **@Async默认使用ttlExecutorService**，自动传递MDC，推荐不指定线程池
- **RocketMQ消息**自动通过消息属性传递traceId，无需使用TTL线程池
- **MQTT消息**自动通过Disruptor队列传递traceId，无需使用TTL线程池
- **普通线程池任务**如果不需要traceId，使用myThreadPoolTaskExecutor性能更好

### 1.2 使用主线程池（推荐）

**适用场景**：大部分异步任务

```java
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

@Service
public class OrderService {

    @Autowired
    @Qualifier("myThreadPoolTaskExecutor")
    private ThreadPoolTaskExecutor executor;

    public void createOrder(Order order) {
        // 同步：保存订单
        orderMapper.insert(order);

        // 异步：发送邮件（不需要上下文信息）
        executor.execute(() -> {
            emailService.sendOrderNotification(order.getUserId(), order.getId());
        });
    }
}
```

### 1.3 使用@Async注解（推荐，自动传递MDC）

**优势**：
- 代码简洁，自动使用配置的线程池
- **框架@Async默认使用ttlExecutorService，自动传递MDC**

```java
import org.springframework.scheduling.annotation.Async;
import cn.city.parking.common.core.utils.MDCTraceUtils;

@Service
public class EmailService {

    // ✅ 不指定线程池：使用默认的ttlExecutorService，自动传递MDC
    @Async
    public void sendEmail(String to, String content) {
        // ✅ 自动获得父线程的MDC（traceId、username等）
        String traceId = MDCTraceUtils.getTraceId();
        log.info("异步发送邮件：{}，traceId：{}", to, traceId);
        // 日志中自动包含：[traceId:xxx] [username:xxx]
        // ... 邮件发送逻辑
    }

    // ✅ 指定线程池myThreadPoolTaskExecutor：不会自动传递MDC
    @Async("myThreadPoolTaskExecutor")
    public void sendSms(String phone) {
        // ⚠️ 普通线程池不传递MDC，MDCTraceUtils.getTraceId()为null
        log.info("发送短信：{}", phone);
    }
}

// 调用
@Autowired
private EmailService emailService;

public void process() {
    // 直接调用，自动异步执行
    emailService.sendEmail("user@example.com", "订单创建成功");
}
```

**@Async执行器配置**（ExecutePoolConfiguration）：
```java
@Bean
public AsyncConfigurer getTTLAsyncConfigurer(@Qualifier("ttlExecutorService") ExecutorService executorService){
    return new AsyncConfigurer(){
        @Override
        public Executor getAsyncExecutor() {
            // ✅ @Async默认使用TTL线程池，自动传递MDC
            return TtlExecutors.getTtlExecutorService(executorService);
        }
    };
}
```

**@Async注意事项**：
- ❌ 不能在同一个类中调用（AOP失效）
- ✅ 返回值使用`Future`或`CompletableFuture`
- ✅ 方法必须是`public`
- ✅ 必须通过Spring代理调用

```java
// ❌ 错误：同类调用，异步失效
@Service
public class OrderService {

    public void methodA() {
        this.methodB();  // 直接调用，@Async失效
    }

    @Async
    public void methodB() {
        // 不会异步执行
    }
}

// ✅ 正确：拆分成两个Service
@Service
public class OrderService {

    @Autowired
    private AsyncTaskService asyncTaskService;

    public void methodA() {
        asyncTaskService.methodB();  // 通过代理调用，异步生效
    }
}

@Service
public class AsyncTaskService {

    @Async("myThreadPoolTaskExecutor")
    public void methodB() {
        // 异步执行
    }
}
```

### 1.4 使用TTL线程池（自动传递MDC）

**适用场景**：异步任务需要访问主线程的ThreadLocal变量（traceId、username等）

**重要说明**：框架已配置TtlMdcListener + TTL线程池，**MDC自动传递，无需手动处理**。

```java
import java.util.concurrent.ExecutorService;
import cn.city.parking.common.core.utils.MDCTraceUtils;

@Service
public class LogService {

    @Autowired
    @Qualifier("ttlExecutorService")
    private ExecutorService ttlExecutorService;

    public void recordLog(String operation) {
        // 主线程的MDC（traceId、username、platform等）

        // ✅ TTL线程池自动传递MDC
        ttlExecutorService.execute(() -> {
            // 子线程自动获得父线程的MDC，无需手动设置
            String traceId = MDCTraceUtils.getTraceId();  // ✅ 自动获取到
            String username = MDCTraceUtils.getUsername();  // ✅ 自动获取到

            log.info("记录操作日志，操作：{}", operation);
            // 日志中自动包含：[traceId:xxx] [username:xxx]
            // ... 保存日志到数据库
        });
        // ❌ 无需finally清理（子线程不影响父线程的MDC）
    }
}
```

### 1.5 使用用户任务线程池（需要登录信息）

**适用场景**：异步任务需要获取当前登录用户信息

```java
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

@Service
public class OperationLogService {

    @Autowired
    @Qualifier("userTaskThreadPool")
    private ThreadPoolTaskExecutor userTaskThreadPool;

    public void recordOperation(String operation) {
        // 主线程有登录用户信息
        String currentUser = SecurityUtils.getUsername();

        // 异步记录操作日志（需要用户名）
        userTaskThreadPool.execute(() -> {
            // SaToken上下文自动传递，可以获取用户信息
            String username = SecurityUtils.getUsername();  // 可以获取到
            log.info("操作日志，用户：{}，操作：{}", username, operation);
            // ... 保存操作日志
        });
    }
}
```

### 1.6 异步方法返回值

**使用Future获取结果**：

```java
import java.util.concurrent.Future;
import org.springframework.scheduling.annotation.AsyncResult;

@Service
public class ReportService {

    @Async("myThreadPoolTaskExecutor")
    public Future<ReportData> generateReport(String userId) {
        // 耗时操作：生成报表
        ReportData data = doGenerate(userId);

        // 返回结果
        return new AsyncResult<>(data);
    }
}

// 调用
@Autowired
private ReportService reportService;

public void process() {
    // 提交异步任务
    Future<ReportData> future = reportService.generateReport("1001");

    // 做其他事情...

    // 获取结果（阻塞等待）
    try {
        ReportData data = future.get(30, TimeUnit.SECONDS);  // 最多等待30秒
        log.info("报表生成完成：{}", data);
    } catch (TimeoutException e) {
        log.error("报表生成超时");
    }
}
```

**使用CompletableFuture（推荐）**：

```java
import java.util.concurrent.CompletableFuture;

@Service
public class OrderService {

    @Autowired
    @Qualifier("myThreadPoolTaskExecutor")
    private ThreadPoolTaskExecutor executor;

    public void createOrder(Order order) {
        // 保存订单
        orderMapper.insert(order);

        // 异步处理（链式调用）
        CompletableFuture.runAsync(() -> {
            // 扣减库存
            stockService.deduct(order.getSkuId(), order.getQuantity());
        }, executor)
        .thenRunAsync(() -> {
            // 发送通知
            emailService.sendNotification(order.getUserId());
        }, executor)
        .exceptionally(e -> {
            // 异常处理
            log.error("异步处理失败，订单ID：{}", order.getId(), e);
            return null;
        });
    }
}
```

### 1.7 异步异常处理

**方式1：在异步方法内部捕获**（推荐）：

```java
@Async("myThreadPoolTaskExecutor")
public void processAsync(String orderId) {
    try {
        // 业务逻辑
        processOrder(orderId);
    } catch (Exception e) {
        // 记录日志
        log.error("异步处理订单失败，订单ID：{}", orderId, e);

        // 发送告警
        alertService.sendAlert("订单处理失败", e.getMessage());

        // 记录失败表
        failRecordService.save(orderId, e.getMessage());
    }
}
```

**方式2：配置全局异常处理器**：

```java
@Configuration
public class AsyncConfig {

    @Bean
    public AsyncUncaughtExceptionHandler asyncUncaughtExceptionHandler() {
        return new CustomAsyncUncaughtExceptionHandler();
    }
}

@Slf4j
public class CustomAsyncUncaughtExceptionHandler implements AsyncUncaughtExceptionHandler {

    @Override
    public void handleUncaughtException(Throwable ex, Method method, Object... params) {
        log.error("异步方法执行异常，方法：{}，参数：{}", method.getName(), params, ex);
        // 发送告警
    }
}
```

### 1.8 线程池监控

**配置Actuator监控**：

```yaml
management:
  endpoints:
    web:
      exposure:
        include: threadpool  # 暴露线程池监控端点
```

**自定义监控**：

```java
@Component
@Slf4j
public class ThreadPoolMonitor {

    @Autowired
    @Qualifier("myThreadPoolTaskExecutor")
    private ThreadPoolTaskExecutor executor;

    @Scheduled(fixedDelay = 60000)  // 每分钟检查一次
    public void monitor() {
        ThreadPoolExecutor pool = executor.getThreadPoolExecutor();

        int active = pool.getActiveCount();
        int poolSize = pool.getPoolSize();
        int queueSize = pool.getQueue().size();
        long completed = pool.getCompletedTaskCount();

        log.info("线程池状态 - 活跃：{}，总数：{}，队列：{}，已完成：{}",
            active, poolSize, queueSize, completed);

        // 告警：队列堆积
        if (queueSize > 100) {
            log.warn("线程池队列堆积，队列大小：{}", queueSize);
        }

        // 告警：线程数接近上限
        if (poolSize >= pool.getMaximumPoolSize() * 0.8) {
            log.warn("线程池接近上限，当前：{}，最大：{}", poolSize, pool.getMaximumPoolSize());
        }
    }
}
```

### 1.9 常见错误

```java
// ❌ 错误1：创建新线程执行（不受管理，可能导致线程泄漏）
new Thread(() -> {
    // 异步任务
}).start();

// ✅ 正确：使用线程池
executor.execute(() -> {
    // 异步任务
});

// ❌ 错误2：在事务中提交异步任务（异步任务立即执行，事务可能未提交）
@Transactional
public void create(Order order) {
    orderMapper.insert(order);
    executor.execute(() -> {
        // 此时事务可能未提交，查询不到刚插入的订单
        Order o = orderMapper.selectById(order.getId());
    });
}

// ✅ 正确：事务提交后执行
@Transactional
public void create(Order order) {
    orderMapper.insert(order);
}

@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
public void afterCommit(OrderCreatedEvent event) {
    executor.execute(() -> {
        // 事务已提交
    });
}

// ❌ 错误3：不处理异常（异常被吞掉）
@Async
public void processAsync() {
    // 如果这里抛异常，不会有任何提示
    throw new RuntimeException("出错了");
}

// ✅ 正确：捕获异常
@Async
public void processAsync() {
    try {
        // 业务逻辑
    } catch (Exception e) {
        log.error("异步任务执行失败", e);
    }
}
```

---

## 2. API幂等性规范

**幂等性定义**：同一个请求，无论调用多少次，结果都一样。

### 2.1 哪些接口需要幂等

**必须支持幂等的接口**：
- ✅ 所有CUD操作（Create、Update、Delete）
- ✅ 支付、退款等金额操作
- ✅ 状态变更操作（订单状态、库存扣减）
- ❌ 查询操作天然幂等，不需要特殊处理

### 2.2 方式1：@NoRepeatSubmit注解（防止前端重复提交）

**适用场景**：防止用户短时间内重复点击提交按钮

```java
import cn.city.parking.common.core.annotation.NoRepeatSubmit;

@DubboService
public class OrderDubboApiImpl extends BaseDubboApi implements OrderDubboApi {

    // ✅ 5秒内禁止重复提交（基于用户ID + 接口路径）
    @NoRepeatSubmit(interval = 5000, message = "请勿重复提交")
    @Override
    public ResponseResult<Integer> add(Order order) {
        int rows = orderService.insertOrder(order);
        return ResponseResult.success(rows);
    }

    // ✅ 自定义幂等key（基于订单号）
    @NoRepeatSubmit(interval = 10000, key = "#order.orderNo")
    @Override
    public ResponseResult<Integer> pay(Order order) {
        payService.pay(order);
        return ResponseResult.success(1);
    }
}
```

**实现原理**：
- 基于Redis，key = userId + 接口路径（或自定义key）
- 第一次请求：Redis中不存在key，放行，并设置key（过期时间=interval）
- 重复请求：Redis中存在key，拒绝

### 2.3 方式2：业务唯一键（推荐）

**适用场景**：分布式环境下的幂等保障

**数据库唯一索引**：

```sql
-- 订单表：订单号唯一
CREATE TABLE t_order (
    id VARCHAR(64) PRIMARY KEY,
    order_no VARCHAR(64) UNIQUE KEY,  -- 唯一索引
    ...
);

-- 支付流水表：订单号+支付流水号联合唯一
CREATE TABLE t_pay_record (
    id VARCHAR(64) PRIMARY KEY,
    order_no VARCHAR(64),
    pay_serial_no VARCHAR(64),
    UNIQUE KEY uk_order_serial (order_no, pay_serial_no)
);
```

**Service实现**：

```java
@Override
@Transactional(rollbackFor = Exception.class)
public int createOrder(Order order) {
    // 检查订单号是否已存在
    Order existing = orderMapper.selectByOrderNo(order.getOrderNo());
    if (existing != null) {
        // ✅ 幂等返回（订单已存在）
        log.info("订单已存在，订单号：{}", order.getOrderNo());
        return 1;
    }

    // 插入订单（订单号唯一索引，重复插入会抛异常）
    try {
        return orderMapper.insert(order);
    } catch (DuplicateKeyException e) {
        // ✅ 并发场景：唯一索引冲突，幂等返回
        log.warn("订单号重复，订单号：{}", order.getOrderNo());
        return 1;
    }
}
```

### 2.4 方式3：分布式锁（高并发场景）

**适用场景**：库存扣减、优惠券领取等高并发场景

```java
import cn.city.parking.common.redis.service.Locker;

@Service
public class StockService {

    @Autowired
    private Locker locker;

    public boolean deductStock(String orderId, String skuId, int quantity) {
        // 分布式锁key
        String lockKey = "lock:stock:" + skuId;

        return locker.tryLock(lockKey, 10, () -> {
            // 1. 检查是否已处理（幂等）
            StockRecord record = stockRecordMapper.selectByOrderId(orderId);
            if (record != null) {
                log.info("订单已扣减库存，订单号：{}", orderId);
                return true;
            }

            // 2. 扣减库存
            int rows = stockMapper.deduct(skuId, quantity);
            if (rows == 0) {
                throw new BusinessException("库存不足");
            }

            // 3. 记录扣减记录（防止重复扣减）
            record = new StockRecord();
            record.setOrderId(orderId);
            record.setSkuId(skuId);
            record.setQuantity(quantity);
            stockRecordMapper.insert(record);

            return true;
        });
    }
}
```

### 2.5 方式4：状态机（状态变更场景）

**适用场景**：订单状态变更、工单流转等

```java
@Override
@Transactional(rollbackFor = Exception.class)
public int payOrder(String orderId) {
    // 1. 查询订单当前状态
    Order order = orderMapper.selectById(orderId);

    // 2. 检查状态是否允许支付
    if (order.getStatus() == OrderStatus.PAID) {
        // ✅ 幂等：订单已支付
        log.info("订单已支付，订单ID：{}", orderId);
        return 1;
    }

    if (order.getStatus() != OrderStatus.PENDING_PAY) {
        // 订单状态不对，不允许支付
        throw new BusinessException("订单状态不允许支付");
    }

    // 3. 更新状态（带状态检查，防止并发）
    int rows = orderMapper.updateStatus(orderId, OrderStatus.PENDING_PAY, OrderStatus.PAID);
    if (rows == 0) {
        // ✅ 并发场景：状态已被其他线程修改
        throw new BusinessException("订单状态已变更，请刷新后重试");
    }

    return rows;
}

// Mapper实现
int updateStatus(@Param("orderId") String orderId,
                 @Param("oldStatus") Integer oldStatus,
                 @Param("newStatus") Integer newStatus);

<!-- XML -->
<update id="updateStatus">
    UPDATE t_order
    SET status = #{newStatus}, update_time = NOW()
    WHERE id = #{orderId}
    AND status = #{oldStatus}  <!-- 乐观锁：只更新指定状态的记录 -->
</update>
```

### 2.6 幂等性测试

**单元测试**：

```java
@Test
public void testIdempotent() {
    String orderId = "ORDER001";

    // 第一次调用
    int result1 = orderService.createOrder(buildOrder(orderId));
    Assert.assertEquals(1, result1);

    // 第二次调用（相同订单号）
    int result2 = orderService.createOrder(buildOrder(orderId));
    Assert.assertEquals(1, result2);  // 幂等，返回成功

    // 验证数据库只有一条记录
    List<Order> orders = orderMapper.selectByOrderNo(orderId);
    Assert.assertEquals(1, orders.size());
}
```

**压测验证**（JMeter/Gatling）：
- 并发100个线程，同时提交相同的订单号
- 验证数据库只创建1条订单记录

### 2.7 幂等性最佳实践

**设计原则**：
1. ✅ 使用业务唯一键（订单号、流水号等）
2. ✅ 数据库唯一索引强约束
3. ✅ 接口设计时考虑幂等性
4. ✅ 状态变更使用状态机
5. ✅ 记录处理记录表

**常见错误**：

```java
// ❌ 错误1：不检查是否已处理，直接执行
public void deductStock(String skuId) {
    stockMapper.deduct(skuId, 1);  // 每次调用都扣减
}

// ✅ 正确：先检查后执行
public void deductStock(String orderId, String skuId) {
    if (已处理(orderId)) {
        return;  // 幂等返回
    }
    stockMapper.deduct(skuId, 1);
    记录处理记录(orderId);
}

// ❌ 错误2：使用时间戳作为唯一键
String orderId = System.currentTimeMillis() + "";  // 并发时可能重复

// ✅ 正确：使用雪花ID或UUID
String orderId = IdUtil.getSnowflakeNextIdStr();
```

---

## 3. Mapper继承说明

框架提供了增强的Mapper接口，支持批量操作。

### 3.1 Mapper继承规范

**标准写法**（推荐）：

```java
import com.baomidou.mybatisplus.core.mapper.BaseMapper;

// ✅ 继承BaseMapper即可（框架已注入批量方法）
public interface UserMapper extends BaseMapper<User> {

    // 自定义查询方法
    List<User> selectUserList(User user);

    User selectUserByUsername(@Param("username") String username);
}
```

**框架已自动注入的批量方法**：

```java
// ✅ 批量插入（排除UPDATE填充字段）
int insertBatchSomeColumn(Collection<User> entityList);

// 使用示例
List<User> userList = Arrays.asList(user1, user2, user3);
int rows = userMapper.insertBatchSomeColumn(userList);
```

**方法说明**：
- `insertBatchSomeColumn`：批量插入，但排除`updateTime`、`updateBy`等UPDATE填充字段
- 每批次建议不超过1000条
- 会自动填充`createTime`、`createBy`等INSERT填充字段

### 3.2 CustomSqlInjector原理

框架通过`CustomSqlInjector`注入批量方法：

```java
// common-server已配置（MyMetaObjectHandler中）
@Bean
public CustomSqlInjector easySqlInjector() {
    return new CustomSqlInjector();
}

// CustomSqlInjector实现
public class CustomSqlInjector extends DefaultSqlInjector {
    @Override
    public List<AbstractMethod> getMethodList(Class<?> mapperClass, TableInfo tableInfo) {
        List<AbstractMethod> methodList = super.getMethodList(mapperClass, tableInfo);
        // 注入批量插入方法（排除UPDATE填充字段）
        methodList.add(new InsertBatchSomeColumn(i -> i.getFieldFill() != FieldFill.UPDATE));
        return methodList;
    }
}
```

**为什么不继承CommonMapper？**

框架提供了`CommonMapper`接口，但**不推荐使用**：

```java
// ❌ 不推荐：CommonMapper已废弃
public interface UserMapper extends CommonMapper<User> {
    // CommonMapper继承了BaseMapper，并定义了insertBatchSomeColumn方法签名
}

// ✅ 推荐：继承BaseMapper
public interface UserMapper extends BaseMapper<User> {
    // CustomSqlInjector已自动注入insertBatchSomeColumn方法
}
```

**原因**：
- `CommonMapper`只是定义了方法签名，实际实现仍来自`CustomSqlInjector`
- 继承`BaseMapper`即可使用所有方法，无需继承`CommonMapper`
- 保持一致性，所有Mapper统一继承`BaseMapper`

### 3.3 批量操作注意事项

**使用限制**：

```java
// ✅ 正确：分批插入
List<User> userList = ...; // 5000条数据

if (userList.size() > 1000) {
    // 使用Guava分批
    List<List<User>> batches = Lists.partition(userList, 1000);
    for (List<User> batch : batches) {
        userMapper.insertBatchSomeColumn(batch);
    }
} else {
    userMapper.insertBatchSomeColumn(userList);
}

// ❌ 错误：一次插入超过1000条
userMapper.insertBatchSomeColumn(userList);  // 5000条，SQL过长
```

**字段填充说明**：

```java
// insertBatchSomeColumn排除的字段（FieldFill.UPDATE）
updateTime  // ❌ 不填充
updateBy    // ❌ 不填充

// 会填充的字段（FieldFill.INSERT）
createTime  // ✅ 自动填充当前时间
createBy    // ✅ 自动填充当前用户
delFlag     // ✅ 自动填充0
id          // ✅ 自动生成雪花ID

// 使用示例
List<User> users = new ArrayList<>();
for (int i = 0; i < 100; i++) {
    User user = new User();
    user.setUsername("user" + i);
    user.setPhone("138000000" + i);
    // ✅ 不需要设置id、createTime、createBy等字段
    users.add(user);
}

// 批量插入（自动填充）
userMapper.insertBatchSomeColumn(users);
```

### 3.4 常见错误

```java
// ❌ 错误1：循环插入（N次SQL）
for (User user : userList) {
    userMapper.insert(user);
}

// ✅ 正确：批量插入（1次SQL）
userMapper.insertBatchSomeColumn(userList);

// ❌ 错误2：批量插入时手动设置updateTime
user.setUpdateTime(new Date());  // 不会生效，insertBatchSomeColumn排除了UPDATE字段

// ✅ 正确：不设置updateTime
// createTime会自动填充

// ❌ 错误3：使用saveBatch（MyBatis Plus自带方法）
userMapper.saveBatch(userList);  // 实际上是循环insert，性能差

// ✅ 正确：使用insertBatchSomeColumn（真正的批量插入）
userMapper.insertBatchSomeColumn(userList);
```

---

## 4. 性能优化规范

### 4.1 分页查询规范

**核心原则**：所有列表查询必须分页，禁止一次性查询大量数据。

```java
// ✅ 正确：使用分页
@Override
public ResponseResult<PageInfo<Order>> pageList(Order order) {
    startDubboPage();  // 必须调用，会从ThreadLocal获取分页参数
    List<Order> list = orderService.selectOrderList(order);
    return ResponseResult.success(new PageInfo<>(list));
}

// ❌ 错误：不分页，查询所有数据
@Override
public ResponseResult<List<Order>> allList(Order order) {
    List<Order> list = orderService.selectOrderList(order);  // 可能返回10万条数据
    return ResponseResult.success(list);
}
```

**分页参数限制**：
```java
// 前端传参限制
if (pageSize > 500) {
    throw new BusinessException("每页最多查询500条数据");
}

// 防止深分页（offset过大导致性能问题）
if (pageNum > 1000) {
    throw new BusinessException("最多查询前1000页数据");
}
```

**深分页优化**：
```java
// ❌ 深分页性能差（offset大时，MySQL需要扫描并跳过大量数据）
SELECT * FROM t_order WHERE user_id = ? LIMIT 100000, 100;

// ✅ 游标分页（使用上一页的最大ID）
SELECT * FROM t_order
WHERE user_id = ? AND id > ?  -- 上一页的最大ID
ORDER BY id ASC
LIMIT 100;

// Java实现
public List<Order> selectByLastId(String userId, String lastId, int limit) {
    LambdaQueryWrapper<Order> wrapper = new LambdaQueryWrapper<>();
    wrapper.eq(Order::getUserId, userId);
    if (StringUtils.isNotBlank(lastId)) {
        wrapper.gt(Order::getId, lastId);  // id > lastId
    }
    wrapper.orderByAsc(Order::getId);
    wrapper.last("LIMIT " + limit);
    return orderMapper.selectList(wrapper);
}
```

### 4.2 批量操作规范

**禁止在循环中执行SQL**（N+1查询问题）：

```java
// ❌ 错误：N+1查询
List<Order> orderList = orderMapper.selectList(null);
for (Order order : orderList) {
    User user = userMapper.selectById(order.getUserId());  // 每次循环都查询
    order.setUser(user);
}

// ✅ 正确：批量查询
List<Order> orderList = orderMapper.selectList(null);
Set<String> userIds = orderList.stream()
    .map(Order::getUserId)
    .collect(Collectors.toSet());
List<User> users = userMapper.selectBatchIds(userIds);  // 一次查询所有

// 转为Map方便匹配
Map<String, User> userMap = users.stream()
    .collect(Collectors.toMap(User::getId, Function.identity()));

// 填充数据
orderList.forEach(order -> order.setUser(userMap.get(order.getUserId())));
```

**批量插入/更新限制**：

```java
// ✅ 批量插入（每批1000条）
List<User> userList = ...; // 5000条数据

// 分批插入
List<List<User>> batches = Lists.partition(userList, 1000);
for (List<User> batch : batches) {
    userMapper.insertBatchSomeColumn(batch);
}

// ❌ 禁止：一次插入超过1000条
userMapper.insertBatchSomeColumn(userList);  // 5000条，SQL过长，性能差
```

**IN条件限制**：

```java
// ✅ IN条件最多500个
if (idList.size() > 500) {
    // 分批查询
    List<List<String>> batches = Lists.partition(idList, 500);
    List<Order> result = new ArrayList<>();
    for (List<String> batch : batches) {
        result.addAll(orderMapper.selectBatchIds(batch));
    }
    return result;
}

// ❌ 禁止：IN条件超过500个
SELECT * FROM t_order WHERE id IN (1, 2, 3, ..., 1000);  // 性能差，且MySQL有限制
```

### 4.3 索引使用规范

**必须建立索引的字段**：
- WHERE条件字段
- ORDER BY字段
- JOIN关联字段
- 高频查询字段

**索引失效场景**（避免）：

```sql
-- ❌ 索引失效1：前导模糊查询
SELECT * FROM user WHERE username LIKE '%zhang%';

-- ✅ 正确：后缀模糊查询（可以用索引）
SELECT * FROM user WHERE username LIKE 'zhang%';

-- ❌ 索引失效2：在索引列上使用函数
SELECT * FROM t_order WHERE DATE(create_time) = '2025-01-03';

-- ✅ 正确：使用范围查询
SELECT * FROM t_order
WHERE create_time >= '2025-01-03 00:00:00'
AND create_time < '2025-01-04 00:00:00';

-- ❌ 索引失效3：隐式类型转换
SELECT * FROM user WHERE phone = 13800138000;  -- phone是VARCHAR，传入了INT

-- ✅ 正确：类型匹配
SELECT * FROM user WHERE phone = '13800138000';

-- ❌ 索引失效4：OR连接（两个字段都要有索引）
SELECT * FROM user WHERE username = 'zhangsan' OR email = 'test@qq.com';

-- ✅ 正确：改为UNION（如果只有一个字段有索引）
SELECT * FROM user WHERE username = 'zhangsan'
UNION
SELECT * FROM user WHERE email = 'test@qq.com';

-- ❌ 索引失效5：不等于（!= 或 <>）
SELECT * FROM user WHERE status != 1;

-- ✅ 正确：如果status取值少，使用IN
SELECT * FROM user WHERE status IN (0, 2, 3);
```

**复合索引最左前缀原则**：

```sql
-- 复合索引：(user_id, status, create_time)

-- ✅ 可以用到索引
WHERE user_id = ?
WHERE user_id = ? AND status = ?
WHERE user_id = ? AND status = ? AND create_time > ?

-- ❌ 不能用到索引（跳过了user_id）
WHERE status = ?
WHERE create_time > ?
WHERE status = ? AND create_time > ?
```

### 4.4 SQL优化规范

**SELECT字段优化**：

```sql
-- ❌ 禁止：SELECT *
SELECT * FROM t_order WHERE id = ?;

-- ✅ 正确：只查询需要的字段
SELECT id, order_no, user_id, amount, status FROM t_order WHERE id = ?;

-- 优点：
-- 1. 减少网络传输
-- 2. 减少内存占用
-- 3. 可能用到覆盖索引（无需回表）
```

**COUNT查询优化**：

```java
// ❌ 效率低：先查总数，再查列表
int total = orderMapper.selectCount(wrapper);
List<Order> list = orderMapper.selectList(wrapper);

// ✅ 推荐：使用PageHelper，只需一次查询
startDubboPage();
List<Order> list = orderMapper.selectList(wrapper);
PageInfo<Order> pageInfo = new PageInfo<>(list);
// pageInfo.getTotal() 自动包含总数
```

**避免全表扫描**：

```java
// ❌ 禁止：查询不带WHERE条件
SELECT * FROM t_order LIMIT 100;

// ✅ 正确：至少带一个过滤条件
SELECT * FROM t_order WHERE create_time >= ? LIMIT 100;
```

### 4.5 大字段处理

**分离大字段**：

```java
// 表设计：将大字段单独存储
t_order: id, order_no, user_id, amount, status  // 主表
t_order_detail: order_id, detail_json           // 大字段表

// 列表查询：不查询大字段
SELECT id, order_no, amount FROM t_order WHERE ...;

// 详情查询：按需关联大字段
SELECT o.*, d.detail_json
FROM t_order o
LEFT JOIN t_order_detail d ON o.id = d.order_id
WHERE o.id = ?;
```

**大字段使用TEXT/BLOB**：

```java
// 实体类中标记大字段（不参与普通查询）
@TableField(select = false)  // 默认查询不返回此字段
private String detailJson;

// 需要时手动查询
@TableField(select = true)
private String detailJson;
```

### 4.6 数据库连接池

**HikariCP配置建议**（已在框架中配置，了解即可）：

```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 20          # 最大连接数（公式：CPU核心数 * 2 + 1）
      minimum-idle: 5                # 最小空闲连接
      connection-timeout: 30000      # 连接超时（30秒）
      idle-timeout: 600000           # 空闲连接超时（10分钟）
      max-lifetime: 1800000          # 连接最大存活时间（30分钟）
```

**连接泄漏排查**：

```java
// ✅ Service方法上必须有@Transactional，自动管理连接
@Override
@Transactional(rollbackFor = Exception.class)
public int updateUser(User user) {
    return userMapper.updateById(user);
}

// ❌ 错误：手动管理连接（容易泄漏）
Connection conn = dataSource.getConnection();
// ... 忘记关闭
```

### 4.7 性能监控建议

**慢SQL记录**（Nacos配置）：

```yaml
mybatis-plus:
  configuration:
    log-impl: org.apache.ibatis.logging.slf4j.Slf4jImpl  # 开发环境打印SQL
  performance-interceptor:  # 性能分析插件（仅测试环境）
    max-time: 3000  # SQL执行超过3秒记录
    format: true    # SQL格式化
```

**接口耗时记录**：

```java
// DubboApi中记录关键接口耗时
@Override
public ResponseResult<Order> getInfo(String id) {
    long startTime = System.currentTimeMillis();
    try {
        Order order = orderService.selectOrderById(id);
        return ResponseResult.success(order);
    } finally {
        long cost = System.currentTimeMillis() - startTime;
        if (cost > 3000) {  // 超过3秒告警
            log.warn("订单查询耗时过长：{}ms，订单ID：{}", cost, id);
        }
    }
}
```

**性能优化检查清单**：
- [ ] 所有列表查询都有分页
- [ ] 没有N+1查询问题
- [ ] 批量操作控制在1000条以内
- [ ] WHERE条件字段都有索引
- [ ] 没有SELECT *
- [ ] 没有前导模糊查询（LIKE '%xx%'）
- [ ] IN条件不超过500个
- [ ] 没有在索引列上使用函数
- [ ] Service方法有@Transactional
- [ ] 大字段单独存储或延迟加载

---

## 5. 分布式事务处理规范

### 5.1 判断是否需要分布式事务

**本地事务**（单库操作，使用@Transactional）：
- ✅ 单个服务内的多表操作
- ✅ 同一个数据库的事务

**分布式事务**（跨服务/跨库操作）：
- ✅ 跨服务调用（订单服务 + 库存服务）
- ✅ 跨数据库操作

**是否需要强一致性？**

| 场景 | 一致性要求 | 解决方案 |
|-----|-----------|---------|
| 订单+支付+库存 | 强一致性 | Seata AT模式 / TCC |
| 订单创建+发送通知 | 最终一致性 | 消息队列（可靠消息） |
| 数据同步 | 最终一致性 | 定时任务补偿 |
| 日志记录 | 无要求 | 异步处理，允许丢失 |

### 5.2 本地事务使用（@Transactional）

```java
import org.springframework.transaction.annotation.Transactional;

// ✅ Service层方法必须添加@Transactional
@Override
@Transactional(rollbackFor = Exception.class)
public int createOrder(Order order) {
    // 1. 插入订单主表
    orderMapper.insert(order);

    // 2. 插入订单明细
    for (OrderItem item : order.getItems()) {
        orderItemMapper.insert(item);
    }

    // 3. 更新用户积分
    userMapper.updatePoints(order.getUserId(), order.getPoints());

    // 任一步骤失败，自动回滚
    return 1;
}

// ❌ 错误：忘记添加@Transactional
public int createOrder(Order order) {
    orderMapper.insert(order);  // 成功
    orderItemMapper.insert(item);  // 失败
    // 订单已插入，但明细失败 → 数据不一致
}
```

**@Transactional注意事项**：
- ✅ 必须是`public`方法
- ✅ 必须通过Spring代理调用（不能是同类内部调用）
- ✅ rollbackFor必须指定Exception.class（默认只回滚RuntimeException）
- ❌ 不要捕获异常后不抛出（事务不会回滚）

```java
// ❌ 错误：同类调用，事务失效
public void methodA() {
    this.methodB();  // 直接调用，@Transactional失效
}

@Transactional
public void methodB() {
    // 事务不会生效
}

// ✅ 正确：使用AOP代理（启动类已配置exposeProxy=true）
public void methodA() {
    OrderService proxy = (OrderService) AopContext.currentProxy();
    proxy.methodB();  // 通过代理调用，事务生效
}
```

### 5.3 分布式事务方案 - 可靠消息最终一致性（推荐）

**适用场景**：允许短暂不一致（秒级），但最终必须一致。

**实现方案**：本地消息表 + 定时补偿

```java
// 1. 创建本地消息表
CREATE TABLE t_local_message (
    id VARCHAR(64) PRIMARY KEY,
    business_id VARCHAR(64),      -- 业务ID（订单号等）
    business_type VARCHAR(32),    -- 业务类型（ORDER_CREATE）
    message_content TEXT,         -- 消息内容（JSON）
    status TINYINT,               -- 状态（0-待发送 1-已发送 2-失败）
    retry_count INT DEFAULT 0,    -- 重试次数
    max_retry INT DEFAULT 3,      -- 最大重试次数
    next_retry_time DATETIME,     -- 下次重试时间
    create_time DATETIME,
    update_time DATETIME
);

// 2. Service实现（本地事务）
@Override
@Transactional(rollbackFor = Exception.class)
public int createOrder(Order order) {
    // 业务操作
    int rows = orderMapper.insert(order);

    // 插入本地消息（同一事务）
    LocalMessage message = new LocalMessage();
    message.setBusinessId(order.getId());
    message.setBusinessType("ORDER_CREATE");
    message.setMessageContent(JSON.toJSONString(order));
    message.setStatus(0);  // 待发送
    message.setNextRetryTime(new Date());
    localMessageMapper.insert(message);

    return rows;
}

// 3. 定时任务扫描并发送消息
@Scheduled(fixedDelay = 5000)  // 每5秒执行一次
public void sendPendingMessages() {
    // 查询待发送的消息
    List<LocalMessage> messages = localMessageMapper.selectPending();

    for (LocalMessage msg : messages) {
        try {
            // 调用远程服务
            switch (msg.getBusinessType()) {
                case "ORDER_CREATE":
                    stockDubboApi.deductStock(msg.getBusinessId());
                    break;
            }

            // 标记为已发送
            msg.setStatus(1);
            localMessageMapper.updateById(msg);

        } catch (Exception e) {
            log.error("发送消息失败：{}", msg.getId(), e);

            // 重试次数+1
            msg.setRetryCount(msg.getRetryCount() + 1);

            if (msg.getRetryCount() >= msg.getMaxRetry()) {
                // 超过最大重试次数，标记为失败，发送告警
                msg.setStatus(2);
            } else {
                // 计算下次重试时间（指数退避：1分钟、2分钟、4分钟）
                long delay = (long) Math.pow(2, msg.getRetryCount()) * 60 * 1000;
                msg.setNextRetryTime(new Date(System.currentTimeMillis() + delay));
            }

            localMessageMapper.updateById(msg);
        }
    }
}
```

### 5.4 接口幂等性保障

**分布式事务中，远程接口必须支持幂等**：

```java
// 远程服务必须幂等
@Override
public ResponseResult<Integer> deductStock(String orderId, String skuId, int quantity) {
    // 1. 检查是否已处理过（通过订单号判断）
    StockRecord record = stockRecordMapper.selectByOrderId(orderId);
    if (record != null) {
        log.info("订单已扣减库存，跳过：{}", orderId);
        return ResponseResult.success(1);  // 幂等返回
    }

    // 2. 扣减库存
    int rows = stockMapper.deduct(skuId, quantity);
    if (rows == 0) {
        throw new BusinessException("库存不足");
    }

    // 3. 记录扣减记录（防止重复扣减）
    record = new StockRecord();
    record.setOrderId(orderId);
    record.setSkuId(skuId);
    record.setQuantity(quantity);
    stockRecordMapper.insert(record);

    return ResponseResult.success(rows);
}
```

### 5.5 补偿机制

**定时任务自动补偿**：

```java
// 定时扫描异常订单并补偿
@Scheduled(cron = "0 */10 * * * ?")  // 每10分钟
public void compensateAbnormalOrders() {
    // 查询创建超过10分钟但未支付的订单
    List<Order> abnormalOrders = orderMapper.selectAbnormal();

    for (Order order : abnormalOrders) {
        try {
            // 检查库存服务是否已扣减
            boolean stockDeducted = stockDubboApi.checkDeducted(order.getId());

            if (stockDeducted) {
                // 库存已扣减，但订单未支付 → 恢复库存
                stockDubboApi.restoreStock(order.getId());
                log.info("补偿：恢复库存，订单ID：{}", order.getId());
            }

            // 取消订单
            order.setStatus(-1);
            orderMapper.updateById(order);
            log.info("补偿：取消订单，订单ID：{}", order.getId());

        } catch (Exception e) {
            log.error("补偿失败，订单ID：{}", order.getId(), e);
        }
    }
}
```

### 5.6 分布式事务最佳实践

**设计原则**：
1. ✅ 优先使用本地事务
2. ✅ 能用最终一致性就不用强一致性
3. ✅ 所有远程接口必须支持幂等
4. ✅ 必须有补偿机制（自动或人工）
5. ✅ 重要操作记录操作日志

**避免的错误**：
```java
// ❌ 错误1：在事务中调用远程服务（耗时长，锁占用时间长）
@Transactional
public int createOrder(Order order) {
    orderMapper.insert(order);
    stockDubboApi.deductStock(order.getId());  // ❌ 远程调用在事务中
    // 如果远程调用超时，本地事务会长时间持有锁
}

// ✅ 正确：事务只包含本地操作
@Transactional
public int createOrder(Order order) {
    orderMapper.insert(order);
    localMessageMapper.insert(message);  // 插入本地消息
}
// 异步发送消息到远程服务

// ❌ 错误2：远程接口不支持幂等
public void deductStock(String skuId) {
    stockMapper.deduct(skuId, 1);  // 每次调用都扣减
    // 重试时会重复扣减
}

// ✅ 正确：支持幂等
public void deductStock(String orderId, String skuId) {
    if (已处理过(orderId)) {
        return;  // 幂等返回
    }
    stockMapper.deduct(skuId, 1);
    记录处理记录(orderId);
}
```
