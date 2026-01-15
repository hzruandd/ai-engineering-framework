# SOLID 设计原则详解

> **核心原则**：编写可维护、可扩展、易测试的代码

SOLID 是面向对象设计的五大基本原则，遵循这些原则可以帮助我们编写出高内聚、低耦合的代码。

---

## S - 单一职责原则（Single Responsibility Principle）

**定义**：一个类只负责一件事，只有一个引起它变化的原因。

### ✅ 正确示例

```java
// ✅ UserService只负责用户业务逻辑
@Service
public class UserServiceImpl implements IUserService {
    public User getUserById(String id) {
        return userMapper.selectById(id);
    }
}

// ✅ UserNotificationService只负责用户通知
@Service
public class UserNotificationService {
    public void sendWelcomeEmail(User user) {
        // 发送欢迎邮件
    }
}
```

### ❌ 错误示例

```java
// ❌ UserService职责过多：业务逻辑 + 通知 + 导出
@Service
public class UserService {
    public User createUser(User user) {
        userMapper.insert(user);
        sendWelcomeEmail(user);  // 通知职责
        return user;
    }

    private void sendWelcomeEmail(User user) {
        // 发送邮件逻辑
    }

    public byte[] exportUsers() {
        // 导出Excel逻辑
    }
}
```

### 实践要点

- 每个类/接口设计前，先问自己：它的单一职责是什么？
- 如果一个类超过 500 行代码，考虑是否职责过多需要拆分
- 如果描述一个类的功能需要用"和"字连接，说明职责可能不单一

---

## O - 开闭原则（Open-Closed Principle）

**定义**：对扩展开放，对修改关闭。

### ✅ 正确示例

```java
// ✅ 使用策略模式，新增支付方式不需要修改原有代码
public interface PaymentStrategy {
    void pay(Order order);
}

@Component("wechat")
public class WeChatPayStrategy implements PaymentStrategy {
    public void pay(Order order) { /* 微信支付 */ }
}

@Component("alipay")
public class AlipayStrategy implements PaymentStrategy {
    public void pay(Order order) { /* 支付宝支付 */ }
}

@Service
public class PaymentService {
    @Autowired
    private Map<String, PaymentStrategy> strategyMap;  // Spring自动注入

    public void pay(Order order, String payType) {
        PaymentStrategy strategy = strategyMap.get(payType);
        strategy.pay(order);
    }
}
```

### ❌ 错误示例

```java
// ❌ 每次新增支付方式都要修改这个方法
public void pay(Order order, String payType) {
    if ("wechat".equals(payType)) {
        // 微信支付
    }
    else if ("alipay".equals(payType)) {
        // 支付宝支付
    }
    else if ("union".equals(payType)) {  // 新增就要改这里
        // 银联支付
    }
}
```

### 实践要点

- 新增功能时，优先考虑扩展而不是修改
- 使用策略模式、工厂模式、模板方法模式支持扩展
- 利用 Spring 的依赖注入自动收集策略实现

---

## L - 里氏替换原则（Liskov Substitution Principle）

**定义**：子类可以替换父类，且不改变程序的正确性。

### ✅ 正确示例

```java
// ✅ 子类增强父类行为，不改变原有逻辑
public abstract class BaseUserService {
    public User getUser(String id) {
        return userMapper.selectById(id);
    }
}

public class VipUserService extends BaseUserService {
    @Override
    public User getUser(String id) {
        User user = super.getUser(id);
        // 增强：加载VIP特权信息
        user.setVipInfo(loadVipInfo(id));
        return user;
    }
}
```

### ❌ 错误示例

```java
// ❌ 子类改变了父类行为，返回null违反约定
public class RestrictedUserService extends BaseUserService {
    @Override
    public User getUser(String id) {
        // 错误：改变了父类的行为，父类永远不返回null
        if (isRestricted(id)) {
            return null;  // 违反父类约定
        }
        return super.getUser(id);
    }
}
```

### 实践要点

- 子类应该增强父类，而不是改变父类的行为
- 子类方法的前置条件不能比父类更严格
- 子类方法的后置条件不能比父类更宽松
- 如果子类无法完全替换父类，考虑使用组合而非继承

---

## I - 接口隔离原则（Interface Segregation Principle）

**定义**：使用多个专门的接口，而不是单一的总接口。

### ✅ 正确示例

```java
// ✅ 拆分成多个小接口
public interface IUserQueryService {
    User getUserById(String id);
    List<User> getUserList(User query);
}

public interface IUserCommandService {
    int createUser(User user);
    int updateUser(User user);
    int deleteUser(String id);
}

// 实现类可以只实现需要的接口
@Service
public class UserQueryServiceImpl implements IUserQueryService {
    // 只实现查询方法
}
```

### ❌ 错误示例

```java
// ❌ 大而全的接口，强迫实现不需要的方法
public interface IUserService {
    User getUserById(String id);
    List<User> getUserList(User query);
    int createUser(User user);
    int updateUser(User user);
    int deleteUser(String id);
    void exportToExcel();  // 不是所有实现类都需要导出功能
    void sendEmail();      // 不是所有实现类都需要发邮件
}
```

### 实践要点

- 接口应该小而专一
- 按职责拆分接口（如：查询接口、命令接口）
- 客户端不应该被迫依赖它不使用的方法

---

## D - 依赖倒置原则（Dependency Inversion Principle）

**定义**：依赖抽象，不依赖具体实现。

### ✅ 正确示例

```java
// ✅ 依赖接口，不依赖具体实现
@Service
public class OrderService {
    @Autowired
    private IPaymentService paymentService;  // 依赖抽象接口

    @Autowired
    private INotificationService notificationService;  // 依赖抽象接口

    public void createOrder(Order order) {
        orderMapper.insert(order);
        paymentService.process(order);  // 不关心具体是哪种支付方式
        notificationService.send(order);  // 不关心具体是邮件还是短信
    }
}
```

### ❌ 错误示例

```java
// ❌ 依赖具体实现，紧耦合
@Service
public class OrderService {
    // 直接依赖具体实现类
    private WeChatPayService weChatPayService = new WeChatPayService();
    private EmailService emailService = new EmailService();

    public void createOrder(Order order) {
        orderMapper.insert(order);
        weChatPayService.pay(order);  // 紧耦合，无法替换
        emailService.sendEmail(order);  // 紧耦合，无法替换
    }
}
```

### 实践要点

- 依赖注入使用 `@Autowired`，面向接口编程
- 高层模块不应该依赖低层模块，两者都应该依赖抽象
- 不要使用 `new` 创建依赖对象

---

## SOLID 在 City Parking 框架中的应用

| 原则 | 框架应用场景 |
|------|-------------|
| **S** | DubboApi/Controller 只负责接口适配，Service 负责业务逻辑，Mapper 负责数据访问 |
| **O** | 使用策略模式、工厂模式、模板方法模式支持扩展 |
| **L** | 子类增强父类，不改变原有行为（如：VipUserService 继承 UserService） |
| **I** | 拆分 IUserQueryService、IUserCommandService，而不是一个大而全的 IUserService |
| **D** | Service 依赖抽象接口，通过 @Autowired 注入，不使用 new 创建依赖 |

---

## 实践建议清单

### ✅ 推荐做法

- 每个类/接口设计前，先问自己：它的单一职责是什么？
- 新增功能时，优先考虑扩展而不是修改（开闭原则）
- 依赖注入使用 `@Autowired`，面向接口编程
- 使用设计模式（策略、工厂、模板方法）应对变化

### ❌ 避免做法

- **上帝类（God Class）**：一个类超过 500 行、职责超过 3 个
- **大泥球（Big Ball of Mud）**：所有代码耦合在一起
- **过度设计**：简单问题复杂化，为不存在的需求预留扩展点

---

## 参考资料

- [SOLID Principles - Wikipedia](https://en.wikipedia.org/wiki/SOLID)
- [Clean Architecture - Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
