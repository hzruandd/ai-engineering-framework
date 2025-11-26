---
description: 代码审查清单，用于开发完成后的自测和提测前审查
---

# 代码审查清单

> **使用场景**：开发完成自测后、提测前的代码审查
> **审查原则**：代码质量、安全性、性能、可维护性达到业界标准

---

## 📋 快速索引

- [Spring Java Format代码风格](#一spring-java-format代码风格) - 代码格式规范
- [代码质量检查](#二代码质量检查-clean-code) - Clean Code原则
- [核心框架规范](#三核心框架规范) - 事务、缓存、异常、幂等
- [设计原则检查](#四设计原则检查-solid) - SOLID原则
- [安全规范检查](#五安全规范检查-owasp) - OWASP标准
- [性能优化检查](#六性能优化检查) - 性能最佳实践
- [测试规范检查](#七测试规范检查) - 单元测试
- [代码评审建议](#八代码评审建议) - 设计模式、可扩展性

---

## 一、Spring Java Format代码风格

### 1.1 基础格式规范 ✅

**缩进与空格**：
- [ ] 使用Tab缩进（等同于4个空格），不混用Tab和空格
- [ ] 操作符两侧有空格：`a + b`，`x > 0`
- [ ] 关键字后有空格：`if (condition)`，`for (int i = 0; i < 10; i++)`
- [ ] 方法名和左括号之间无空格：`method()`
- [ ] 括号内侧无空格：`(a + b)`，不是 `( a + b )`

**示例**：
```java
// ✅ 正确格式
public void processOrder(Order order) {
    if (order != null && order.getAmount() > 0) {
        int result = orderService.process(order);
    }
}

// ❌ 错误格式
public void processOrder (Order order) {  // 方法名后多空格
    if( order!=null&&order.getAmount()>0 ){  // 缺少空格
        int result=orderService.process( order );  // 括号内多空格
    }
}
```

**行宽限制**：
- [ ] 每行不超过120字符
- [ ] 超长行自动换行，续行缩进8个空格（2个Tab）
- [ ] 链式调用换行，每行一个方法

**示例**：
```java
// ✅ 正确换行
ResponseResult<PageInfo<User>> result = userDubboApi
        .queryUsers(userId, status, startTime, endTime);

// ✅ 链式调用换行
List<String> userNames = users.stream()
        .filter(user -> user.getStatus() == 1)
        .map(User::getUsername)
        .collect(Collectors.toList());

// ❌ 错误：单行超过120字符
ResponseResult<PageInfo<User>> result = userDubboApi.queryUsers(userId, status, startTime, endTime, includeDetail, includeRoles);
```

**大括号位置**：
- [ ] 左大括号不换行（K&R风格）
- [ ] 右大括号换行
- [ ] `else`、`catch`、`finally` 与右大括号同行
- [ ] 单行语句也必须使用大括号

**示例**：
```java
// ✅ 正确大括号位置
if (condition) {
    doSomething();
}
else {  // else与右大括号同行
    doOther();
}

try {
    processData();
}
catch (Exception e) {  // catch与右大括号同行
    handleError(e);
}
finally {  // finally与右大括号同行
    cleanup();
}

// ✅ 单行也要大括号
if (user == null) {
    return;
}

// ❌ 错误：单行没有大括号
if (user == null) return;
```

### 1.2 命名规范 ✅

**类命名**：
- [ ] 类名使用大驼峰：`UserService`、`OrderMapper`
- [ ] 接口以`I`开头：`IUserService`
- [ ] 实现类以`Impl`结尾：`UserServiceImpl`
- [ ] 抽象类以`Abstract`或`Base`开头：`BaseEntity`
- [ ] 测试类以`Test`结尾：`UserServiceTest`
- [ ] 避免使用拼音、无意义缩写

**方法命名**：
- [ ] 方法名使用小驼峰：`getUserInfo`、`processOrder`
- [ ] 查询方法：`select/get/query/find + 名词`
- [ ] 新增方法：`insert/add/create/save + 名词`
- [ ] 更新方法：`update/modify/edit + 名词`
- [ ] 删除方法：`delete/remove + 名词`
- [ ] 布尔方法：`is/has/can/should + 形容词/动词`

**变量命名**：
- [ ] 变量名使用小驼峰：`userId`、`orderList`
- [ ] 常量全大写，下划线分隔：`MAX_RETRY_COUNT`
- [ ] 布尔变量清晰表达：`isDeleted`、`hasPermission`、`canEdit`
- [ ] 集合变量使用复数：`users`、`orderList`
- [ ] 循环变量可以使用`i`、`j`、`k`，其他避免单字母

**示例**：
```java
// ✅ 正确命名
public class UserServiceImpl implements IUserService {
    private static final int MAX_RETRY_COUNT = 3;

    public User getUserById(String userId) {
        boolean isValid = validateUserId(userId);
        if (!isValid) {
            return null;
        }

        List<User> users = userMapper.selectList(null);
        for (int i = 0; i < users.size(); i++) {
            // ...
        }
        return userMapper.selectById(userId);
    }
}

// ❌ 错误命名
public class userserviceimpl {  // 类名不规范
    private static final int max = 3;  // 常量不规范

    public User get(String id) {  // 方法名不清晰
        boolean b = check(id);  // 变量名无意义
        if (!b) return null;  // 不推荐使用缩写b

        List<User> u = userMapper.selectList(null);  // 变量名太短
        return userMapper.selectById(id);
    }
}
```

### 1.3 代码布局 ✅

**空行使用**：
- [ ] 包声明后空一行
- [ ] import语句组之间空一行
- [ ] 类成员之间空一行
- [ ] 方法之间空一行
- [ ] 方法内逻辑块之间空一行
- [ ] 不要连续多个空行

**示例**：
```java
package cn.city.parking.user.service;

import java.util.List;
import java.util.Map;

import org.springframework.stereotype.Service;

import cn.city.parking.user.api.entity.User;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;

@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, User> {

    private IUserMapper userMapper;

    private RedisUtils redisUtils;

    public User getUserById(String id) {
        // 参数校验
        if (StringUtils.isBlank(id)) {
            return null;
        }

        // 查询数据
        User user = userMapper.selectById(id);

        // 返回结果
        return user;
    }

    public List<User> listUsers() {
        return userMapper.selectList(null);
    }
}
```

**类成员顺序**：
- [ ] 静态常量
- [ ] 实例变量
- [ ] 构造方法
- [ ] 公共方法
- [ ] 私有方法

**示例**：
```java
public class OrderService {
    // 1. 静态常量
    private static final int MAX_ORDER_COUNT = 100;

    // 2. 实例变量
    private IOrderMapper orderMapper;
    private RedisUtils redisUtils;

    // 3. 构造方法
    public OrderService(IOrderMapper orderMapper) {
        this.orderMapper = orderMapper;
    }

    // 4. 公共方法
    public Order createOrder(Order order) {
        validate(order);
        return save(order);
    }

    // 5. 私有方法
    private void validate(Order order) {
        // ...
    }

    private Order save(Order order) {
        // ...
    }
}
```

### 1.4 导入语句规范 ✅

- [ ] 静态导入在前，普通导入在后
- [ ] 按字母顺序排序
- [ ] 不同包之间空行分隔：`java.*`、`javax.*`、`org.*`、`com.*`、项目包
- [ ] 不使用通配符导入：`import java.util.*;`
- [ ] 移除未使用的导入

**示例**：
```java
// ✅ 正确的import顺序
import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.when;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import cn.city.parking.common.core.web.domain.ResponseResult;
import cn.city.parking.user.api.entity.User;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.google.common.base.Preconditions;

// ❌ 错误的import
import java.util.*;  // 不使用通配符
import cn.city.parking.user.api.entity.User;
import org.springframework.stereotype.Service;  // 顺序错误
import java.time.LocalDateTime;  // 顺序错误
```

### 1.5 注释格式规范 ✅

**JavaDoc注释**：
- [ ] 类和公共方法必须有JavaDoc
- [ ] 使用`/** */`格式
- [ ] 第一行是简短描述
- [ ] `@param`、`@return`、`@throws`对齐

**示例**：
```java
/**
 * 用户服务实现类
 *
 * 负责用户的创建、查询、更新等核心业务逻辑
 *
 * @author zhangsan
 * @since 2025-01-03
 */
@Service
public class UserServiceImpl implements IUserService {

    /**
     * 根据用户ID查询用户信息
     *
     * @param userId 用户ID，不能为空
     * @return 用户信息，如果不存在则返回null
     * @throws BusinessException 用户ID格式错误时抛出
     */
    public User getUserById(String userId) {
        // ...
    }
}
```

**单行注释**：
- [ ] 单行注释使用`//`，后面有空格
- [ ] 注释与代码同级缩进
- [ ] 多行注释使用`/* */`

**示例**：
```java
// ✅ 正确的单行注释
public void processOrder(Order order) {
    // 验证订单状态
    if (order.getStatus() != OrderStatus.PENDING) {
        return;
    }

    // 处理订单
    // 这是一个复杂的流程
    doProcess(order);
}

// ❌ 错误的单行注释
public void processOrder(Order order) {
    //验证订单状态（缺少空格）
        // 缩进错误
    if (order.getStatus() != OrderStatus.PENDING) {
        return;
    }
}
```

### 1.6 常见格式错误 ✅

**检查清单**：
- [ ] 没有多余的空格：行尾、空行中
- [ ] 没有Tab和空格混用
- [ ] 没有连续多个空行
- [ ] 文件末尾有一个空行
- [ ] 没有无用的import语句
- [ ] 没有注释掉的代码
- [ ] 字符串连接使用`+`时，换行在`+`前面

**示例**：
```java
// ✅ 字符串连接换行
String message = "这是一个很长的错误提示信息，"
        + "为了可读性，我们将它分成多行显示，"
        + "每行不超过120字符";

// ❌ 错误的字符串连接
String message = "这是一个很长的错误提示信息，" +
        "为了可读性，我们将它分成多行显示，" +
        "每行不超过120字符";
```

**自动格式化**：
```bash
# 使用Maven插件自动格式化
mvn spring-javaformat:apply

# 检查格式是否符合规范
mvn spring-javaformat:validate
```

---

## 二、代码质量检查（Clean Code）

### 2.1 方法设计 ✅

**方法长度**：
- [ ] **方法不超过50行**（包括空行和注释）
- [ ] 超过30行考虑是否可以拆分
- [ ] 每个方法只做一件事（单一职责）

**示例**：
```java
// ❌ 方法过长（80行）
public void processOrder(Order order) {
    // 验证订单
    if (order == null) {
        throw new BusinessException("订单不能为空");
    }
    if (order.getAmount() <= 0) {
        throw new BusinessException("订单金额必须大于0");
    }
    // ... 还有30行验证逻辑

    // 保存订单
    orderMapper.insert(order);

    // 扣减库存
    for (OrderItem item : order.getItems()) {
        Stock stock = stockMapper.selectById(item.getSkuId());
        if (stock.getQuantity() < item.getQuantity()) {
            throw new BusinessException("库存不足");
        }
        stock.setQuantity(stock.getQuantity() - item.getQuantity());
        stockMapper.updateById(stock);
    }
    // ... 还有20行库存处理

    // 发送通知
    // ... 10行通知逻辑
}

// ✅ 拆分成多个方法
public void processOrder(Order order) {
    validateOrder(order);
    saveOrder(order);
    deductStock(order);
    sendNotification(order);
}

private void validateOrder(Order order) {
    Preconditions.checkNotNull(order, "订单不能为空");
    Preconditions.checkArgument(order.getAmount() > 0, "订单金额必须大于0");
    // ... 其他验证
}

private void saveOrder(Order order) {
    orderMapper.insert(order);
}

private void deductStock(Order order) {
    for (OrderItem item : order.getItems()) {
        deductSingleItem(item);
    }
}

private void sendNotification(Order order) {
    // 发送通知逻辑
}
```

**方法参数**：
- [ ] **参数不超过5个**
- [ ] 超过3个考虑封装为对象
- [ ] 避免使用布尔参数（改用枚举或拆分方法）

**示例**：
```java
// ❌ 参数过多
public void createUser(String username, String password, String phone,
                       String email, Integer age, String address,
                       Integer gender, String idCard) {
    // ...
}

// ✅ 封装为对象
public void createUser(UserCreateRequest request) {
    // ...
}

// ❌ 布尔参数不清晰
userService.listUsers(true);  // true表示什么？

// ✅ 使用枚举
userService.listUsers(UserStatus.ACTIVE);
// 或拆分方法
userService.listActiveUsers();
userService.listInactiveUsers();
```

**圈复杂度**：
- [ ] **圈复杂度不超过10**
- [ ] if/else、for、while、case等分支计数
- [ ] 使用卫语句减少嵌套
- [ ] 提前return

**示例**：
```java
// ❌ 嵌套过深，圈复杂度高
public void processOrder(Order order) {
    if (order != null) {
        if (order.getAmount() > 0) {
            if (order.getStatus() == OrderStatus.PENDING) {
                if (stockService.checkStock(order)) {
                    // 处理逻辑
                }
                else {
                    throw new BusinessException("库存不足");
                }
            }
            else {
                throw new BusinessException("订单状态错误");
            }
        }
        else {
            throw new BusinessException("订单金额错误");
        }
    }
    else {
        throw new BusinessException("订单不能为空");
    }
}

// ✅ 使用卫语句，提前return
public void processOrder(Order order) {
    // 卫语句：提前处理异常情况
    if (order == null) {
        throw new BusinessException("订单不能为空");
    }
    if (order.getAmount() <= 0) {
        throw new BusinessException("订单金额错误");
    }
    if (order.getStatus() != OrderStatus.PENDING) {
        throw new BusinessException("订单状态错误");
    }
    if (!stockService.checkStock(order)) {
        throw new BusinessException("库存不足");
    }

    // 正常处理逻辑（无嵌套）
    doProcess(order);
}
```

### 2.2 类设计 ✅

**类长度**：
- [ ] **类不超过500行**
- [ ] 超过300行考虑是否可以拆分
- [ ] 避免"上帝类"（God Class）

**类职责**：
- [ ] 每个类只有一个修改的理由（SRP）
- [ ] 类的字段不超过10个
- [ ] 高内聚、低耦合

**依赖注入**：
- [ ] 使用`@Autowired`注入依赖，不使用`new`
- [ ] 避免循环依赖
- [ ] 优先使用构造器注入（不可变依赖）

**示例**：
```java
// ❌ 使用new创建依赖
@Service
public class OrderService {
    private StockService stockService = new StockService();  // 紧耦合

    public void process(Order order) {
        stockService.deduct(order);
    }
}

// ✅ 依赖注入
@Service
public class OrderService {
    private final StockService stockService;

    // 构造器注入（推荐）
    @Autowired
    public OrderService(StockService stockService) {
        this.stockService = stockService;
    }

    public void process(Order order) {
        stockService.deduct(order);
    }
}
```

### 2.3 代码坏味道检测 ✅

**重复代码（Duplicated Code）**：
- [ ] 相同代码出现3次以上，提取公共方法
- [ ] 类似逻辑使用模板方法模式
- [ ] DRY原则：Don't Repeat Yourself

**示例**：
```java
// ❌ 重复代码
public void processOrderA(Order order) {
    if (order.getAmount() > 10000) {
        log.info("大额订单需要审核");
        order.setStatus(OrderStatus.PENDING_AUDIT);
    }
    orderMapper.insert(order);
}

public void processOrderB(Order order) {
    if (order.getAmount() > 10000) {
        log.info("大额订单需要审核");
        order.setStatus(OrderStatus.PENDING_AUDIT);
    }
    specialHandle(order);
    orderMapper.insert(order);
}

// ✅ 提取公共方法
public void processOrderA(Order order) {
    checkLargeAmount(order);
    orderMapper.insert(order);
}

public void processOrderB(Order order) {
    checkLargeAmount(order);
    specialHandle(order);
    orderMapper.insert(order);
}

private void checkLargeAmount(Order order) {
    if (order.getAmount() > 10000) {
        log.info("大额订单需要审核");
        order.setStatus(OrderStatus.PENDING_AUDIT);
    }
}
```

**过长参数列表（Long Parameter List）**：
- [ ] 参数超过3个，封装为对象
- [ ] 使用Builder模式构建复杂对象

**魔法数字（Magic Numbers）**：
- [ ] 数字字面量使用常量或枚举
- [ ] 常量命名清晰表达含义

**示例**：
```java
// ❌ 魔法数字
if (order.getStatus() == 1) {
    // 1表示什么？
}
if (user.getAge() > 18) {
    // 为什么是18？
}

// ✅ 使用常量
private static final int ORDER_STATUS_PAID = 1;
private static final int ADULT_AGE = 18;

if (order.getStatus() == ORDER_STATUS_PAID) {
    // 已支付
}
if (user.getAge() > ADULT_AGE) {
    // 成年人
}

// ✅ 更好的方式：使用枚举
if (order.getStatus() == OrderStatus.PAID) {
    // 已支付
}
```

**过大的类（Large Class）**：
- [ ] 类超过500行，拆分为多个类
- [ ] 字段超过10个，考虑是否违反SRP

**特性依恋（Feature Envy）**：
- [ ] 方法频繁访问其他类的数据，考虑移动方法

**示例**：
```java
// ❌ 特性依恋：OrderService频繁访问Stock的数据
@Service
public class OrderService {
    public void process(Order order) {
        Stock stock = stockMapper.selectById(order.getSkuId());
        if (stock.getQuantity() < order.getQuantity()) {
            throw new BusinessException("库存不足");
        }
        stock.setQuantity(stock.getQuantity() - order.getQuantity());
        stockMapper.updateById(stock);
    }
}

// ✅ 将逻辑移到StockService
@Service
public class OrderService {
    @Autowired
    private StockService stockService;

    public void process(Order order) {
        stockService.deduct(order.getSkuId(), order.getQuantity());
    }
}

@Service
public class StockService {
    public void deduct(String skuId, int quantity) {
        Stock stock = stockMapper.selectById(skuId);
        if (stock.getQuantity() < quantity) {
            throw new BusinessException("库存不足");
        }
        stock.setQuantity(stock.getQuantity() - quantity);
        stockMapper.updateById(stock);
    }
}
```

### 2.4 重构建议 ✅

**提取方法（Extract Method）**：
- [ ] 方法过长，提取子方法
- [ ] 注释说明的代码块，提取为方法

**提取类（Extract Class）**：
- [ ] 类职责过多，拆分为多个类
- [ ] 一组相关字段和方法，提取为新类

**引入参数对象（Introduce Parameter Object）**：
- [ ] 方法参数过多，封装为对象

**使用策略模式替换条件判断**：
- [ ] 大量if/else或switch，使用策略模式

**示例**：
```java
// ❌ 大量if/else
public BigDecimal calculateDiscount(Order order) {
    if (order.getUserLevel() == 1) {
        return order.getAmount().multiply(new BigDecimal("0.95"));
    }
    else if (order.getUserLevel() == 2) {
        return order.getAmount().multiply(new BigDecimal("0.90"));
    }
    else if (order.getUserLevel() == 3) {
        return order.getAmount().multiply(new BigDecimal("0.85"));
    }
    else {
        return order.getAmount();
    }
}

// ✅ 使用策略模式
public interface DiscountStrategy {
    BigDecimal calculate(BigDecimal amount);
}

@Component
public class NormalDiscountStrategy implements DiscountStrategy {
    public BigDecimal calculate(BigDecimal amount) {
        return amount.multiply(new BigDecimal("0.95"));
    }
}

@Service
public class OrderService {
    @Autowired
    private Map<Integer, DiscountStrategy> strategyMap;  // 策略映射

    public BigDecimal calculateDiscount(Order order) {
        DiscountStrategy strategy = strategyMap.get(order.getUserLevel());
        return strategy != null ? strategy.calculate(order.getAmount()) : order.getAmount();
    }
}
```

---

## 三、核心框架规范

### 3.0 线程池使用规范 ✅

**MDC传递与清理**（防止traceId残留）：
- [ ] ❌ **禁止使用 `Executors.newFixedThreadPool()` 等方法直接创建线程池**
- [ ] ❌ **禁止使用 `new ThreadPoolExecutor()` 创建线程池（除非在ThreadPoolFactory内部）**
- [ ] ❌ **禁止使用 `new ThreadPoolTaskExecutor()` 创建线程池（Spring方式也需要TTL包装）**
- [ ] ✅ **必须使用 `ThreadPoolFactory.newFixedThreadPool()` 创建线程池**
- [ ] ✅ **或者使用 `ThreadPoolFactory.newSpringThreadPool()` （@Bean方式）**
- [ ] ✅ **或者使用 `@Async` 注解（框架自动支持MDC）**
- [ ] ✅ **或者使用注入的 `@Qualifier("ttlExecutorService")` 线程池**
- [ ] ✅ **如果使用@Bean创建ThreadPoolTaskExecutor，必须用TtlExecutors包装后返回ExecutorService**

**违规示例识别**：
```java
// ❌ 错误1：直接使用 Executors（MDC无法传递，会残留）
@Service
public class OrderService {
    private ExecutorService pool = Executors.newFixedThreadPool(10);  // ❌ 禁止
}

// ❌ 错误2：直接new ThreadPoolExecutor（MDC无法传递）
@Service
public class OrderService {
    private ExecutorService pool = new ThreadPoolExecutor(10, 20, ...);  // ❌ 禁止
}

// ❌ 错误3：@Bean方式创建ThreadPoolTaskExecutor，但没有TTL包装
@Configuration
public class ThreadPoolConfig {
    @Bean("myPool")
    public ThreadPoolTaskExecutor myPool() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();  // ❌ 直接new
        executor.setCorePoolSize(10);
        executor.setMaxPoolSize(20);
        executor.setThreadNamePrefix("my-pool-");
        executor.initialize();
        return executor;  // ❌ 直接返回ThreadPoolTaskExecutor，没有TTL包装
    }
}

// ✅ 正确1：使用ThreadPoolFactory（直接创建）
@Service
public class OrderService {
    private ExecutorService pool = ThreadPoolFactory.newFixedThreadPool(10, "order-pool-");
}

// ✅ 正确2：使用ThreadPoolFactory.newSpringThreadPool（@Bean方式，推荐）
@Configuration
public class ThreadPoolConfig {
    @Bean("orderPool")
    public ExecutorService orderPool() {
        // ✅ 直接返回已TTL包装的ExecutorService
        return ThreadPoolFactory.newSpringThreadPool(10, 20, 100, 60, "order-");
    }
}

// ✅ 正确3：@Bean方式手动TTL包装（如果必须使用ThreadPoolTaskExecutor）
@Configuration
public class ThreadPoolConfig {
    @Bean("myPool")
    public ExecutorService myPool() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(10);
        executor.setMaxPoolSize(20);
        executor.setThreadNamePrefix("my-pool-");
        executor.initialize();

        // ✅ 关键：必须用TTL包装后返回ExecutorService
        return TtlExecutors.getTtlExecutorService(executor.getThreadPoolExecutor());
    }
}

// ✅ 正确4：使用@Async
@Service
public class OrderService {
    @Async  // 框架自动支持MDC传递
    public void asyncMethod() {
        log.info("traceId={}", MDCTraceUtils.getTraceId());  // ✅ traceId正确传递
    }
}

// ✅ 正确5：注入框架线程池
@Service
public class OrderService {
    @Autowired
    @Qualifier("ttlExecutorService")
    private ExecutorService executorService;  // ✅ 框架已配置TTL
}
```

**为什么必须这样做？**
- ❌ **直接创建的线程池**：线程复用时会残留上一次请求的 traceId，导致日志混乱
- ✅ **ThreadPoolFactory/TTL包装**：自动传递和清理MDC，线程归还线程池时不会残留traceId
- ✅ **@Async注解**：框架已配置TTL支持，自动传递MDC

**修复建议**：
- 全局搜索：`Executors.new`、`new ThreadPoolExecutor`
- 替换为：`ThreadPoolFactory.newXxx()` 或使用 `@Async`
- 对于无法修改的第三方线程池：`ThreadPoolFactory.wrapExecutorService(legacyPool)`

---

### 3.1 DubboApi/Controller职责边界 ✅

**架构分层原则**（SOLID的S - 单一职责）：
- [ ] DubboApi/Controller只是薄薄的接口层
- [ ] 只负责4件事：参数校验 → 调用Service → 记录日志 → 返回结果
- [ ] 所有业务逻辑必须在Service层

**检查清单**：
- [ ] ❌ 不在DubboApi/Controller中构建查询条件（LambdaQueryWrapper、Specification等）
- [ ] ❌ 不在DubboApi/Controller中做业务判断和计算
- [ ] ❌ 不在DubboApi/Controller中直接调用Mapper（跨层调用）
- [ ] ❌ 不在DubboApi/Controller中循环处理数据
- [ ] ❌ 不在DubboApi/Controller中处理缓存逻辑
- [ ] ❌ 不在DubboApi/Controller中控制事务
- [ ] ❌ 不在DubboApi/Controller中调用多个Service后再做业务处理

**违规示例识别**：
```java
// ❌ 错误1：在DubboApi中构建查询条件
@Override
public ResponseResult<List<User>> listActiveUsers(String name) {
    LambdaQueryWrapper<User> wrapper = new LambdaQueryWrapper<>();  // ❌ 应该在Service层
    wrapper.eq(User::getStatus, 1);
    if (StringUtils.isNotBlank(name)) {
        wrapper.like(User::getUsername, name);
    }
    List<User> list = userMapper.selectList(wrapper);  // ❌ 跨层调用Mapper
    return ResponseResult.success(list);
}

// ❌ 错误2：在DubboApi中处理缓存
@Override
public ResponseResult<User> getUser(String id) {
    String cacheKey = "user:" + id;
    User user = RedisUtils.getCacheObject(cacheKey, User.class);  // ❌ 缓存逻辑应该在Service层
    if (user == null) {
        user = userService.selectById(id);
        RedisUtils.setCacheObject(cacheKey, user, 3600);
    }
    return ResponseResult.success(user);
}

// ❌ 错误3：在DubboApi中做业务判断
@Override
public ResponseResult<Integer> updateStatus(String id, Integer status) {
    User user = userMapper.selectById(id);  // ❌ 跨层调用
    if (user.getStatus() == 1 && status == 0) {  // ❌ 业务判断应该在Service层
        Long count = orderMapper.selectCount(...);  // ❌ 跨层调用
        if (count > 0) {
            throw new BusinessException("该用户有未完成订单");
        }
    }
    user.setStatus(status);
    return ResponseResult.success(userMapper.updateById(user));
}

// ✅ 正确：薄层，只负责参数校验和调用Service
@Override
public ResponseResult<Integer> updateStatus(String id, Integer status) {
    Preconditions.checkArgument(StringUtils.isNotBlank(id), "用户ID不能为空");
    int rows = userService.updateUserStatus(id, status);  // 业务逻辑在Service层
    return ResponseResult.success(rows);
}
```

**修复建议**：
- 将所有业务逻辑、查询条件构建、缓存处理移到Service层
- DubboApi/Controller保持简洁，每个方法不超过10行
- 使用`/new-api`命令生成符合规范的代码

### 3.1 事务与并发 ✅

**事务管理**：
- [ ] 所有CUD方法必须添加`@Transactional(rollbackFor = Exception.class)`
- [ ] 查询方法不添加事务注解
- [ ] 事务方法是public，通过代理调用
- [ ] 避免在事务中调用外部服务（长事务）

**并发安全**：
- [ ] Service不使用成员变量存储请求数据（线程不安全）
- [ ] 共享变量使用`volatile`或`AtomicXxx`
- [ ] 分布式锁使用`Locker`，必须在finally中释放

**示例**：
```java
// ❌ 线程不安全
@Service
public class UserService {
    private User currentUser;  // 成员变量，多线程不安全

    public void process() {
        this.currentUser = getUser();
    }
}

// ✅ 线程安全
@Service
public class UserService {
    public void process() {
        User currentUser = getUser();  // 局部变量，线程安全
    }
}

// ✅ 分布式锁
@Autowired
private Locker locker;

public void processWithLock(String orderId) {
    String lockKey = "lock:order:" + orderId;
    locker.lock(lockKey, 10, () -> {
        // 业务逻辑
        // 10秒后自动释放锁
    });
}
```

### 3.2 缓存与性能 ✅

**缓存使用**：
- [ ] 只缓存热点数据（查询频率>100次/分、变化<10次/天）
- [ ] 缓存必须设置过期时间（30分钟-1小时）
- [ ] 缓存key命名规范：`模块:业务:唯一标识`
- [ ] 更新数据后清理缓存
- [ ] 缓存穿透、击穿、雪崩防护

**性能优化**：
- [ ] 所有列表查询必须分页
- [ ] 避免N+1查询（循环中查询数据库）
- [ ] 避免SELECT *，只查询需要的字段
- [ ] 批量操作每批不超过1000条
- [ ] IN条件不超过500个

### 3.3 异常处理 ✅

**DubboApi异常处理**：
- [ ] 不要随意捕获异常（全局处理器会处理）
- [ ] 永远不要捕获`BusinessException`
- [ ] 可以捕获异常的场景：调用第三方、批量处理、降级处理
- [ ] 捕获异常必须记录完整日志（包括堆栈）

**日志记录**：
- [ ] 使用占位符，不使用字符串拼接
- [ ] CUD操作记录日志（谁、什么时间、做了什么）
- [ ] 敏感信息脱敏（手机号、身份证、银行卡）
- [ ] 不使用`System.out.println()`

### 3.4 幂等性 ✅

**CUD操作幂等**：
- [ ] 使用业务唯一键（订单号、流水号）
- [ ] 数据库唯一索引约束
- [ ] 使用`@NoRepeatSubmit`防止重复提交
- [ ] 状态机控制状态流转
- [ ] 记录处理记录表

### 3.5 敏感功能异常告警规范 ✅

**核心原则**：涉及用户资金或权益的敏感功能，所有异常必须发送告警通知，确保及时发现和处理问题。

#### 3.5.1 敏感功能定义 ✅

**资金交易类**：
- [ ] 支付（微信支付、支付宝支付、银行卡支付）
- [ ] 退款（全额退款、部分退款）
- [ ] 提现（用户提现、商户提现）
- [ ] 充值（账户充值、余额充值）
- [ ] 转账（账户间转账、红包）

**权益开通类**：
- [ ] 开卡（停车卡、会员卡）
- [ ] 开月租（月租车位、月租套餐）
- [ ] 购买优惠券（代金券、折扣券）
- [ ] 购买套餐（停车套餐、服务套餐）
- [ ] 会员升级（普通会员→VIP）

**订单处理类**：
- [ ] 订单创建（支付订单、服务订单）
- [ ] 订单取消（已支付订单取消）
- [ ] 订单退款（订单退款处理）
- [ ] 订单状态变更（待支付→已支付→已完成）

**账户变动类**：
- [ ] 余额变更（增加、扣减）
- [ ] 积分变更（赠送、消费、过期）
- [ ] 会员权益变更（权益开通、权益失效）
- [ ] 优惠券变更（发放、使用、作废）

**核销类**：
- [ ] 优惠券核销
- [ ] 停车券核销
- [ ] 权益核销（会员权益使用）
- [ ] 套餐核销（套餐次数扣减）

#### 3.5.2 告警级别与渠道 ✅

**P0级别（紧急）- 影响所有用户或导致资金损失**：
- **触发条件**：
  - 支付网关宕机（持续5分钟以上）
  - 批量退款失败（连续10笔以上）
  - 数据库死锁导致交易无法进行
  - 分布式事务异常（支付成功但订单创建失败）
- **告警渠道**：短信 + 企业微信 + 电话
- **响应时间**：立即处理（5分钟内）

**P1级别（重要）- 影响部分用户或单笔交易**：
- **触发条件**：
  - 单笔支付失败
  - 单笔退款失败
  - 第三方接口超时（单次）
  - 账户余额不一致
  - 订单状态异常
- **告警渠道**：企业微信 + 钉钉
- **响应时间**：30分钟内处理

**P2级别（一般）- 业务异常但不影响资金**：
- **触发条件**：
  - 用户余额不足（正常业务逻辑）
  - 优惠券已使用
  - 参数校验失败
  - 并发冲突（乐观锁失败，单次）
- **告警渠道**：仅记录日志，不发送告警
- **响应时间**：日常监控

#### 3.5.3 必须告警的场景 ✅

**场景1：支付/退款异常**：
- [ ] 支付成功但订单创建失败（P0）
- [ ] 退款失败（P1）
- [ ] 重复扣款（P0）
- [ ] 支付金额与订单金额不一致（P0）
- [ ] 第三方支付接口异常（P1）

**场景2：数据一致性异常**：
- [ ] 账户余额与流水不一致（P0）
- [ ] 订单状态与支付状态不一致（P0）
- [ ] 库存数据不一致（P1）
- [ ] 优惠券状态异常（P1）

**场景3：第三方服务异常**：
- [ ] 支付网关超时（P1）
- [ ] 银行接口返回失败（P1）
- [ ] 微信/支付宝回调失败（P1）
- [ ] 短信发送失败（P2，涉及验证码则P1）

**场景4：分布式事务异常**：
- [ ] 本地事务提交失败（P0）
- [ ] 补偿事务执行失败（P0）
- [ ] TCC事务超时（P1）
- [ ] 消息队列消费失败（P1）

**场景5：并发冲突超过阈值**：
- [ ] 1分钟内乐观锁冲突超过10次（P1）
- [ ] 1分钟内库存不足超过50次（P1）
- [ ] 疑似刷单行为（同一用户短时间内大量操作）（P0）

#### 3.5.4 告警内容要求 ✅

**必须包含的信息**：
- [ ] **异常时间**：`2025-11-13 14:30:25`
- [ ] **异常类型**：`支付失败`、`退款异常`、`数据不一致`
- [ ] **业务参数**：
  - 订单号（`orderId`）
  - 用户ID（`userId`）
  - 金额（`amount`）
  - 支付方式（`payType`）
- [ ] **异常信息**：
  - 异常类名
  - 异常消息
  - 关键堆栈（前3层）
- [ ] **影响范围**：影响用户数、影响金额
- [ ] **处理建议**：如"请立即检查支付网关"、"需要人工退款"

**告警消息格式**：
```
【P1告警】支付异常
时间：2025-11-13 14:30:25
类型：微信支付失败
订单号：ORDER202511130001
用户ID：USER123456
金额：198.00元
异常：WeChatPayException: 支付网关超时
影响：1笔订单，1个用户
建议：查询支付结果，如未支付成功则关闭订单
```

#### 3.5.5 代码示例 ✅

**示例1：支付异常告警**

```java
// ❌ 错误：敏感功能异常未告警
@Service
public class PaymentService {

    @Transactional(rollbackFor = Exception.class)
    public PaymentResult processPayment(PaymentRequest request) {
        try {
            // 调用支付网关
            PaymentResult result = paymentGateway.pay(request);

            if (!result.isSuccess()) {
                // 仅记录日志，未告警！
                log.error("支付失败，订单号：{}", request.getOrderId());
                throw new BusinessException("支付失败");
            }

            return result;
        } catch (Exception e) {
            // 仅记录日志，未告警！
            log.error("支付异常", e);
            throw new BusinessException("支付处理异常", e);
        }
    }
}

// ✅ 正确：敏感功能异常必须告警
@Service
public class PaymentService {

    @Autowired
    private AlarmService alarmService;  // 告警服务

    @Transactional(rollbackFor = Exception.class)
    public PaymentResult processPayment(PaymentRequest request) {
        try {
            // 调用支付网关
            PaymentResult result = paymentGateway.pay(request);

            if (!result.isSuccess()) {
                // 记录日志
                log.error("支付失败，订单号：{}，原因：{}",
                    request.getOrderId(), result.getFailReason());

                // 发送P1告警
                alarmService.sendAlarm(
                    AlarmLevel.P1,
                    AlarmType.PAYMENT_FAILED,
                    "支付失败",
                    Dict.create()
                        .set("orderId", request.getOrderId())
                        .set("userId", request.getUserId())
                        .set("amount", request.getAmount())
                        .set("payType", request.getPayType())
                        .set("reason", result.getFailReason())
                );

                throw new BusinessException("支付失败");
            }

            return result;
        } catch (PaymentException e) {
            // 记录日志（包含堆栈）
            log.error("支付异常，订单号：{}", request.getOrderId(), e);

            // 发送P0告警（支付异常比失败更严重）
            alarmService.sendAlarm(
                AlarmLevel.P0,
                AlarmType.PAYMENT_ERROR,
                "支付异常",
                Dict.create()
                    .set("orderId", request.getOrderId())
                    .set("userId", request.getUserId())
                    .set("amount", request.getAmount())
                    .set("exception", e.getClass().getName())
                    .set("message", e.getMessage())
            );

            throw new BusinessException("支付处理异常", e);
        }
    }
}
```

**示例2：退款异常告警**

```java
// ✅ 正确示例
@Service
public class RefundService {

    @Autowired
    private AlarmService alarmService;

    @Transactional(rollbackFor = Exception.class)
    public void processRefund(String orderId, BigDecimal amount) {
        try {
            // 调用退款接口
            RefundResult result = refundGateway.refund(orderId, amount);

            if (!result.isSuccess()) {
                log.error("退款失败，订单号：{}，金额：{}，原因：{}",
                    orderId, amount, result.getFailReason());

                // P1告警：退款失败
                alarmService.sendAlarm(
                    AlarmLevel.P1,
                    AlarmType.REFUND_FAILED,
                    "退款失败",
                    Dict.create()
                        .set("orderId", orderId)
                        .set("amount", amount)
                        .set("reason", result.getFailReason())
                );

                throw new BusinessException("退款失败，请稍后重试");
            }

            log.info("退款成功，订单号：{}，金额：{}", orderId, amount);

        } catch (Exception e) {
            log.error("退款异常，订单号：{}，金额：{}", orderId, amount, e);

            // P0告警：退款异常（需要人工介入）
            alarmService.sendAlarm(
                AlarmLevel.P0,
                AlarmType.REFUND_ERROR,
                "退款异常",
                Dict.create()
                    .set("orderId", orderId)
                    .set("amount", amount)
                    .set("exception", e.getMessage())
            );

            throw new BusinessException("退款处理异常", e);
        }
    }
}
```

**示例3：数据一致性检查告警**

```java
// ✅ 定时任务检查数据一致性
@Service
public class DataConsistencyCheckService {

    @Autowired
    private AlarmService alarmService;

    @Scheduled(cron = "0 */10 * * * ?")  // 每10分钟执行一次
    public void checkAccountBalance() {
        try {
            // 查询所有账户
            List<Account> accounts = accountMapper.selectAll();

            for (Account account : accounts) {
                // 计算账户余额（根据流水）
                BigDecimal calculatedBalance = accountFlowMapper.sumByUserId(account.getUserId());

                // 对比账户余额
                if (calculatedBalance.compareTo(account.getBalance()) != 0) {
                    log.error("账户余额不一致，用户ID：{}，账户余额：{}，计算余额：{}",
                        account.getUserId(), account.getBalance(), calculatedBalance);

                    // P0告警：数据不一致
                    alarmService.sendAlarm(
                        AlarmLevel.P0,
                        AlarmType.DATA_INCONSISTENT,
                        "账户余额不一致",
                        Dict.create()
                            .set("userId", account.getUserId())
                            .set("accountBalance", account.getBalance())
                            .set("calculatedBalance", calculatedBalance)
                            .set("diff", account.getBalance().subtract(calculatedBalance))
                    );
                }
            }
        } catch (Exception e) {
            log.error("数据一致性检查异常", e);

            alarmService.sendAlarm(
                AlarmLevel.P1,
                AlarmType.SYSTEM_ERROR,
                "数据一致性检查异常",
                Dict.create().set("exception", e.getMessage())
            );
        }
    }
}
```

**示例4：并发冲突监控告警**

```java
// ✅ 监控并发冲突，超过阈值告警
@Service
public class OrderService {

    @Autowired
    private AlarmService alarmService;

    // 使用AtomicLong统计失败次数
    private final AtomicLong optimisticLockFailCount = new AtomicLong(0);

    @Scheduled(cron = "0 * * * * ?")  // 每分钟检查一次
    public void checkOptimisticLockFail() {
        long failCount = optimisticLockFailCount.getAndSet(0);

        // 阈值：1分钟内失败超过10次
        if (failCount > 10) {
            log.warn("乐观锁冲突频繁，1分钟内失败{}次", failCount);

            // P1告警
            alarmService.sendAlarm(
                AlarmLevel.P1,
                AlarmType.CONCURRENT_CONFLICT,
                "乐观锁冲突频繁",
                Dict.create()
                    .set("failCount", failCount)
                    .set("threshold", 10)
                    .set("suggestion", "检查是否存在热点数据或高并发场景")
            );
        }
    }

    @Transactional(rollbackFor = Exception.class)
    public void updateOrder(Order order) {
        try {
            int rows = orderMapper.updateById(order);
            if (rows == 0) {
                // 乐观锁冲突
                optimisticLockFailCount.incrementAndGet();
                throw new BusinessException("订单已被修改，请重试");
            }
        } catch (Exception e) {
            log.error("更新订单失败", e);
            throw e;
        }
    }
}
```

#### 3.5.6 告警工具类规范 ✅

**推荐实现**：

```java
/**
 * 告警服务接口
 */
public interface AlarmService {

    /**
     * 发送告警
     *
     * @param level 告警级别
     * @param type 告警类型
     * @param title 告警标题
     * @param context 上下文信息
     */
    void sendAlarm(AlarmLevel level, AlarmType type, String title, Dict context);
}

/**
 * 告警级别
 */
public enum AlarmLevel {
    P0("紧急", "短信+企业微信+电话"),
    P1("重要", "企业微信+钉钉"),
    P2("一般", "仅日志");

    private final String name;
    private final String channel;
}

/**
 * 告警类型
 */
public enum AlarmType {
    PAYMENT_FAILED("支付失败"),
    PAYMENT_ERROR("支付异常"),
    REFUND_FAILED("退款失败"),
    REFUND_ERROR("退款异常"),
    DATA_INCONSISTENT("数据不一致"),
    CONCURRENT_CONFLICT("并发冲突"),
    SYSTEM_ERROR("系统错误");

    private final String description;
}
```

**告警去重机制**：

```java
@Service
public class AlarmServiceImpl implements AlarmService {

    @Autowired
    private RedisUtils redisUtils;

    @Autowired
    private WeChatRobotService weChatRobotService;

    @Override
    public void sendAlarm(AlarmLevel level, AlarmType type, String title, Dict context) {
        // 生成告警唯一键
        String alarmKey = buildAlarmKey(level, type, context);

        // 检查是否重复告警（5分钟内相同告警只发送一次）
        String lockKey = "alarm:lock:" + alarmKey;
        if (redisUtils.hasKey(lockKey)) {
            log.info("告警去重，5分钟内已发送，跳过本次告警：{}", title);
            return;
        }

        // 构建告警消息
        String message = buildAlarmMessage(level, type, title, context);

        // 根据告警级别选择渠道
        if (level == AlarmLevel.P0) {
            // P0：短信 + 企业微信
            sendSms(message);
            weChatRobotService.sendMessage(message);
        } else if (level == AlarmLevel.P1) {
            // P1：企业微信
            weChatRobotService.sendMessage(message);
        } else {
            // P2：仅记录日志
            log.warn("告警：{}", message);
        }

        // 记录告警历史
        saveAlarmHistory(level, type, title, context, message);

        // 设置去重锁（5分钟）
        redisUtils.setCacheObject(lockKey, "1", 300);
    }

    private String buildAlarmKey(AlarmLevel level, AlarmType type, Dict context) {
        // 根据告警类型和关键参数生成唯一键
        String orderId = context.getStr("orderId", "");
        String userId = context.getStr("userId", "");
        return level + ":" + type + ":" + orderId + ":" + userId;
    }

    private String buildAlarmMessage(AlarmLevel level, AlarmType type, String title, Dict context) {
        StringBuilder sb = new StringBuilder();
        sb.append("【").append(level.getName()).append("告警】").append(title).append("\n");
        sb.append("时间：").append(DateUtil.now()).append("\n");
        sb.append("类型：").append(type.getDescription()).append("\n");

        // 添加业务参数
        if (context.containsKey("orderId")) {
            sb.append("订单号：").append(context.getStr("orderId")).append("\n");
        }
        if (context.containsKey("userId")) {
            sb.append("用户ID：").append(context.getStr("userId")).append("\n");
        }
        if (context.containsKey("amount")) {
            sb.append("金额：").append(context.getStr("amount")).append("元\n");
        }

        // 添加异常信息
        if (context.containsKey("exception")) {
            sb.append("异常：").append(context.getStr("exception")).append("\n");
        }
        if (context.containsKey("reason")) {
            sb.append("原因：").append(context.getStr("reason")).append("\n");
        }

        // 添加处理建议
        if (context.containsKey("suggestion")) {
            sb.append("建议：").append(context.getStr("suggestion")).append("\n");
        }

        return sb.toString();
    }
}
```

#### 3.5.7 检查清单 ✅

**敏感功能识别**：
- [ ] 方法名包含：`pay`、`refund`、`withdraw`、`recharge`、`purchase`、`order`、`card`等关键词
- [ ] 涉及金额计算的方法（`BigDecimal` 类型参数）
- [ ] 涉及账户余额变更的方法
- [ ] 调用第三方支付接口的方法
- [ ] 涉及用户权益开通/变更的方法

**告警代码检查**：
- [ ] ❌ 敏感功能的catch块中是否添加了告警代码
- [ ] ❌ 告警级别是否合理（P0/P1/P2）
- [ ] ❌ 告警内容是否包含关键信息（订单号、用户ID、金额）
- [ ] ❌ 是否记录了完整的异常堆栈
- [ ] ❌ 是否有告警去重机制（避免告警风暴）
- [ ] ❌ 是否有告警抑制策略（非工作时间P2级别延迟）

**告警测试验证**：
- [ ] 模拟异常场景，验证告警是否正常发送
- [ ] 检查告警消息格式是否规范
- [ ] 检查告警去重是否生效
- [ ] 检查告警渠道是否正确（P0/P1/P2）

**监控与优化**：
- [ ] 是否统计告警数据（按类型、级别、时间）
- [ ] 是否定期review告警记录，优化告警策略
- [ ] 是否有告警响应时长统计
- [ ] 是否有误报率统计（误报率应<5%）

---

## 四、设计原则检查（SOLID）

### 4.1 单一职责原则（SRP）✅
- [ ] 每个类只负责一件事
- [ ] 每个方法只做一件事
- [ ] 不同职责的代码分离

### 4.2 开闭原则（OCP）✅
- [ ] 对扩展开放，对修改关闭
- [ ] 使用接口、抽象类、策略模式

### 4.3 里氏替换原则（LSP）✅
- [ ] 子类可以替换父类
- [ ] 子类不改变父类行为

### 4.4 接口隔离原则（ISP）✅
- [ ] 接口最小化，不强迫实现不需要的方法
- [ ] 大接口拆分成多个小接口

### 4.5 依赖倒置原则（DIP）✅
- [ ] 依赖抽象，不依赖具体实现
- [ ] 面向接口编程

**示例**：
```java
// ❌ 违反DIP
public class OrderService {
    private MySQLOrderDao orderDao = new MySQLOrderDao();  // 依赖具体类
}

// ✅ 符合DIP
public class OrderService {
    @Autowired
    private IOrderDao orderDao;  // 依赖抽象接口
}
```

---

## 五、安全规范检查（OWASP）

### 5.1 SQL注入防护 ✅
- [ ] 所有SQL使用`#{}`预编译，不使用`${}`
- [ ] 动态SQL使用MyBatis Plus的Lambda表达式
- [ ] 用户输入参数必须校验

### 5.2 敏感数据保护 ✅
- [ ] 密码使用BCrypt加密，不可逆
- [ ] 密码、token等不出现在日志中
- [ ] 日志中敏感信息脱敏（手机号、身份证）

**示例**：
```java
// ❌ 禁止：日志打印密码
log.info("用户登录，用户名：{}，密码：{}", username, password);

// ✅ 正确：不打印敏感信息
log.info("用户登录，用户名：{}", username);

// ✅ 脱敏打印
log.info("手机号：{}", maskPhone(phone));  // 138****5678
```

### 5.3 权限校验 ✅
- [ ] 所有DubboApi方法检查权限（除公开接口）
- [ ] 数据权限校验（用户只能访问自己的数据）
- [ ] 垂直权限校验（不同角色不同功能）
- [ ] 水平权限校验（不能访问其他用户数据）

### 5.4 文件上传安全 ✅
- [ ] 校验文件类型（白名单）
- [ ] 校验文件大小
- [ ] 文件名重命名（防止路径穿越）
- [ ] 禁止上传可执行文件

---

## 六、性能优化检查

### 6.1 数据库性能 ✅
- [ ] 所有列表查询必须分页
- [ ] 避免SELECT *
- [ ] WHERE条件字段有索引
- [ ] 避免在索引列上使用函数
- [ ] 避免前导模糊查询：`LIKE '%xxx'`

**示例**：
```java
// ❌ N+1查询
List<Order> orders = orderMapper.selectList(null);
for (Order order : orders) {
    User user = userMapper.selectById(order.getUserId());
}

// ✅ 批量查询
List<Order> orders = orderMapper.selectList(null);
Set<String> userIds = orders.stream()
    .map(Order::getUserId)
    .collect(Collectors.toSet());
List<User> users = userMapper.selectBatchIds(userIds);
```

### 6.2 批量操作 ✅
- [ ] 批量插入使用`insertBatchSomeColumn`
- [ ] 每批不超过1000条
- [ ] 避免在循环中执行SQL

### 6.3 资源释放 ✅
- [ ] IO流使用try-with-resources
- [ ] HTTP连接使用连接池
- [ ] 线程池使用Bean注入，不重复创建

---

## 七、测试规范检查

### 7.1 单元测试 ✅
- [ ] 核心业务逻辑必须有单元测试
- [ ] 测试覆盖率 >= 70%（核心模块 >= 80%）
- [ ] 测试方法命名：`testMethodName_Scenario_ExpectedResult`
- [ ] 使用Mock隔离外部依赖

**示例**：
```java
@Test
public void testCreateOrder_ValidInput_Success() {
    // Given
    Order order = new Order();
    order.setUserId("123");
    order.setAmount(new BigDecimal("100"));

    // When
    int result = orderService.createOrder(order);

    // Then
    Assert.assertEquals(1, result);
    Assert.assertNotNull(order.getId());
}
```

### 7.2 可测试性 ✅
- [ ] 依赖注入，不使用new创建依赖
- [ ] 避免静态方法（难以Mock）
- [ ] 方法职责单一，易于测试

---

## 八、代码评审建议

### 8.1 设计模式应用 ✅

**常用设计模式**：
- [ ] **策略模式**：替换大量if/else
- [ ] **工厂模式**：创建复杂对象
- [ ] **模板方法模式**：抽取相同流程
- [ ] **观察者模式**：事件通知
- [ ] **责任链模式**：多级处理

**示例**：
```java
// ✅ 策略模式替换if/else
public interface PaymentStrategy {
    void pay(Order order);
}

@Component("wechat")
public class WeChatPayStrategy implements PaymentStrategy {
    public void pay(Order order) {
        // 微信支付逻辑
    }
}

@Service
public class PaymentService {
    @Autowired
    private Map<String, PaymentStrategy> strategyMap;

    public void pay(Order order, String payType) {
        PaymentStrategy strategy = strategyMap.get(payType);
        strategy.pay(order);
    }
}
```

### 8.2 可扩展性 ✅

**扩展性检查**：
- [ ] 新增功能是否需要修改原有代码？
- [ ] 是否使用了硬编码？
- [ ] 是否依赖具体实现？
- [ ] 配置项是否外部化？

**改进建议**：
- [ ] 使用接口和抽象类
- [ ] 配置项从代码中分离（Nacos配置中心）
- [ ] 使用SPI机制支持插件化

### 8.3 技术债务识别 ✅

**技术债务清单**：
- [ ] 临时方案（TODO标记）
- [ ] 重复代码未重构
- [ ] 缺少单元测试
- [ ] 缺少文档注释
- [ ] 性能瓶颈未优化

**改进计划**：
- [ ] 记录技术债务到Issue
- [ ] 制定偿还计划（优先级P0-P3）
- [ ] 每个迭代偿还部分债务

---

## 🎯 审查结果模板

### ✅ 符合规范（优点）
1. 代码格式统一，符合Spring Java Format规范
2. 方法长度合理，平均30行左右
3. 命名清晰，见名知意
4. 事务注解正确，SQL使用预编译
5. 有完整的单元测试

### ⚠️ 需要改进（按优先级）

#### 🔴 P0 - 必须立即修改
**1. SQL注入风险**
- **位置**：`OrderMapper.xml:23`
- **问题**：使用`${orderBy}`动态排序
- **风险**：高危安全漏洞
- **修复**：改用白名单校验或MyBatis Plus的OrderBy

#### 🟠 P1 - 本周内修改
**1. 代码格式不符合规范**
- **位置**：`UserServiceImpl.java`全文
- **问题**：行宽超过120字符、缩进不一致、import未排序
- **修复**：执行`mvn spring-javaformat:apply`

**2. 方法过长**
- **位置**：`OrderService.java:45-120`
- **问题**：`createOrder`方法76行，职责过多
- **修复**：拆分为`validateOrder`、`saveOrder`、`deductStock`

#### 🟡 P2 - 两周内优化
**1. 代码重复**
- **位置**：`OrderService.java:34-45` 和 `OrderService.java:78-89`
- **问题**：订单验证逻辑重复
- **修复**：提取公共方法`validateOrderStatus(Order order)`

**2. 缺少单元测试**
- **位置**：`StockService.java`
- **问题**：核心业务逻辑无单元测试
- **修复**：补充单元测试，覆盖率达到80%

#### 🟢 P3 - 有时间再优化
**1. 注释不完整**
- **位置**：`UserService.java`
- **问题**：公共方法缺少JavaDoc注释
- **修复**：补充方法注释（@param、@return）

---

## 📊 代码质量评分

- **代码风格**：75%（存在格式问题）
- **代码质量**：80%（方法略长）
- **安全性**：60%（SQL注入风险）
- **性能**：85%
- **测试覆盖率**：65%（低于标准）

**综合评分**：73 / 100

**评级**：C+（及格，需要改进）

**建议**：
1. 立即修复SQL注入问题（P0）
2. 运行`mvn spring-javaformat:apply`统一代码风格（P1）
3. 拆分过长方法，提高可读性（P1）
4. 补充单元测试，提升覆盖率到70%以上（P2）

---

## 📝 如何使用本清单

**提测前自查流程**：

1. **代码格式化**
   ```bash
   mvn spring-javaformat:apply
   mvn spring-javaformat:validate
   ```

2. **逐项自查**
   - 打印本清单，逐项检查
   - 标记不符合项
   - 记录改进计划

3. **代码质量扫描**
   ```bash
   # SonarQube扫描
   mvn sonar:sonar
   ```

4. **提测检查清单**
   - [ ] 代码格式符合Spring Java Format
   - [ ] 无SQL注入风险
   - [ ] 无敏感信息泄露
   - [ ] 所有CUD方法有事务
   - [ ] 所有列表查询已分页
   - [ ] 核心业务有单元测试
   - [ ] 代码已提交Git

5. **提交代码**
   - 提交到Git
   - 创建Merge Request
   - 填写本次改动说明

---

## 📄 自动生成文档

**执行完成后，必须将审查结果保存到文件**：

1. **文件名格式**：`CODE_REVIEW_{YYYY-MM-DD}.md`
   - 示例：`CODE_REVIEW_2025-11-13.md`
   - 使用环境信息中的日期

2. **保存位置**：项目根目录

3. **文件内容**：包含完整的代码审查结果
   - ✅ 符合规范（优点）
   - ⚠️ 需要改进（按优先级P0-P3）
   - 📊 代码质量评分
   - 建议与改进措施

**⚠️ 重要**：
- 使用 Write 工具将审查结果写入文件
- 文件名中的日期使用环境信息中的 `Today's date`
- 如果文件已存在，直接覆盖
- 审查结果中的日期时间使用环境信息中的系统日期时间，格式为 `yyyy-MM-dd HH:mm:ss`

---

**最后更新**：2025-11-13
**适用版本**：City Parking 2.0.0-SNAPSHOT
