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

### 3.0 DubboApi/Controller职责边界 ✅

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

**最后更新**：2025-01-03
**适用版本**：City Parking 2.0.0-SNAPSHOT
