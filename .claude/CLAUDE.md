# City Parking 微服务框架 - 核心规范速查

> **重要说明**：本文档是AI编码助手的快速参考指南，包含核心规范和禁止事项。详细说明请查阅[docs/guides/](docs/guides/)目录。

---

## 🌐 语言输出规范

**IMPORTANT - DOCUMENTATION LANGUAGE REQUIREMENT:**

当你生成或输出任何文档类型的内容时，**MUST use Chinese (简体中文)**。这包括但不限于：

- ✅ **所有markdown文档** (.md文件)
- ✅ **代码审查报告** (CODE_REVIEW_*.md)
- ✅ **代码修改报告** (CHANGE_REPORT_*.md)
- ✅ **README文件**
- ✅ **技术文档**
- ✅ **注释和说明**
- ✅ **自动生成的报告**
- ✅ **文档内的段落、标题、描述**

**例外情况** (可以使用英文)：
- ❌ 代码本身 (Java代码、变量名、方法名)
- ❌ 配置文件中的键名
- ❌ Git commit message (如用户明确要求英文)
- ❌ 专有名词 (如框架名称：Spring Boot、Dubbo)

**核心原则**：用户是中文使用者，所有面向用户的文档、报告、说明都必须用中文输出，确保用户能够直接阅读和理解，无需翻译。

---

## 📑 快速导航

| 场景 | 文档 |
|------|------|
| **框架功能** | [框架已自动配置的10大功能](docs/guides/framework-features.md) |
| **异步任务** | [线程池选择、@Async、MDC传递](docs/guides/detailed-standards.md#1-异步任务使用规范) |
| **幂等性** | [@NoRepeatSubmit、业务唯一键、分布式锁](docs/guides/detailed-standards.md#2-api幂等性规范) |
| **性能优化** | [分页、批量操作、索引使用](docs/guides/detailed-standards.md#4-性能优化规范) |
| **分布式事务** | [本地事务、最终一致性、补偿机制](docs/guides/detailed-standards.md#5-分布式事务处理规范) |
| **配置说明** | [POM、YAML、数据库、代码格式化](docs/guides/configuration-guide.md) |
| **完整案例** | [5个实战场景示例](docs/examples/) |

---

## 项目概述

### 技术栈
- **Spring Boot**: 2.7.18 | **Spring Cloud Alibaba**: 2021.0.5.0
- **Dubbo**: 3.3.2（RPC框架，服务间通信）
- **Nacos**: 2.1.1（注册中心 + 配置中心）
- **MyBatis Plus**: 3.5.7 | **Redis**: Lettuce | **MySQL**: 8.0+

**重要**：服务间调用使用 **Dubbo RPC**（@DubboService、@DubboReference），❌ 不使用Feign

### 服务分层
```
DubboApi实现（Controller层）→ Service层 → Mapper层 → 数据库
```

### Maven模块结构
```
city-parking-xxx/
├── pom.xml                      # 父POM
├── city-parking-xxx-api/       # API模块（发布到Maven私库）
│   └── cn/city/parking/xxx/api/
│       ├── entity/              # ⚠️ 实体类（必须在api包下！）
│       ├── XxxDubboApi.java    # Dubbo接口定义
│       └── dto/                 # DTO（可选）
└── city-parking-xxx-server/    # Server模块（服务实现）
    ├── XxxApplication.java      # 启动类
    ├── dubbo/                   # DubboApi实现
    ├── service/                 # Service层
    └── mapper/                  # Mapper层
```

**⚠️ 关键路径规范**：
- Entity包路径：`cn.city.parking.xxx.api.entity`（**必须在api包下**）
- ❌ 错误：`cn.city.parking.xxx.entity`（缺少api层级）

---

## 核心规范（12条必读）

### 1. 实体类规范

**⚠️ BusinessEntity只包含3个字段**：
- `id`（主键，雪花ID）
- `createTime`（创建时间）
- `updateTime`（更新时间）

**⚠️ 如果数据库有以下字段，必须在实体类中显式声明**：
- `create_by` → 必须声明 `createBy` 字段
- `update_by` → 必须声明 `updateBy` 字段
- `del_flag` → 必须声明 `delFlag` 字段
- `revision` → 必须声明 `revision` 字段（乐观锁）

```java
import cn.city.parking.common.core.web.domain.BusinessEntity;
import com.baomidou.mybatisplus.annotation.TableName;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.FieldFill;
import com.fasterxml.jackson.annotation.JsonFormat;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Size;
import javax.validation.constraints.Email;

@Data
@EqualsAndHashCode(callSuper = true)
@TableName("sys_user")  // ✅ 必须指定表名
@Schema(description = "用户实体")
public class User extends BusinessEntity {

    @Schema(description = "用户名")
    @NotBlank(message = "用户名不能为空")  // ✅ 参数校验注解
    @Size(min = 1, max = 30, message = "用户名长度必须在1-30个字符之间")
    private String username;

    @Schema(description = "邮箱")
    @Email(message = "邮箱格式不正确")  // ✅ 邮箱格式校验
    @Size(max = 50, message = "邮箱长度不能超过50个字符")
    private String email;

    @Schema(description = "生日")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")  // ✅ 日期字段必须添加
    private LocalDateTime birthday;

    // ⚠️ 如果数据库有create_by字段，必须显式声明
    @TableField(value = "create_by", fill = FieldFill.INSERT)
    @Schema(description = "创建者")
    private String createBy;

    // ⚠️ 如果数据库有update_by字段，必须显式声明
    @TableField(value = "update_by", fill = FieldFill.UPDATE)
    @Schema(description = "更新者")
    private String updateBy;

    // ⚠️ 如果数据库有del_flag字段，必须显式声明
    @TableField(value = "del_flag", fill = FieldFill.INSERT)
    @Schema(description = "删除标志（0-存在，1-删除）")
    private Integer delFlag;

    // ⚠️ 如果需要乐观锁，必须显式声明revision字段
    @Version
    @Schema(description = "乐观锁版本号")
    private Long revision;
}
```

**字段填充说明**：
- `createBy`：使用 `FieldFill.INSERT`（插入时自动填充当前用户）
- `updateBy`：使用 `FieldFill.UPDATE`（更新时自动填充当前用户）
- `delFlag`：使用 `FieldFill.INSERT`（插入时自动填充0）

**参数校验注解说明**（jakarta.validation-api）：
- `@NotBlank`：字符串不能为空（不为null、不为空字符串、不为空格）
- `@NotNull`：值不能为null
- `@Size`：字符串/集合/数组长度限制
- `@Email`：邮箱格式校验
- `@Min`/`@Max`：数值范围校验
- `@Pattern`：正则表达式校验
- **message属性**：校验失败时的提示信息

**⚠️ 校验注解使用说明**：
- 可以加在Entity、DTO、VO等任何JavaBean对象的字段上
- 因为框架不强制使用DTO/VO，所以可以直接在Entity上添加
- 如果使用了DTO，建议在DTO上添加校验注解
- 根据业务需要灵活选择是否使用校验注解

### 2. DubboApi/Controller实现规范

**⚠️ 职责边界（架构核心原则）**：
- ✅ **DubboApi/Controller只是薄薄的接口层**，遵循单一职责原则(SRP)
- ✅ **只负责4件事**：参数校验 → 调用Service → 记录日志 → 返回结果
- ❌ **绝对不允许**：
  - 复杂的业务判断和计算
  - 查询条件构建（LambdaQueryWrapper、Specification等）
  - 直接调用Mapper（跨层调用）
  - 循环处理数据、数据转换
  - 事务控制（事务在Service层）
  - 调用多个Service后再做业务处理

**✅ 正确示例**（薄层）：
```java
import cn.city.parking.common.dubbo.filter.base.BaseDubboApi;
import cn.city.parking.common.core.web.domain.ResponseResult;

@Slf4j
@DubboService
public class UserDubboApiImpl extends BaseDubboApi implements UserDubboApi {

    @Autowired
    private IUserService userService;

    @Override
    public ResponseResult<User> getInfo(String id) {
        // 1. 参数校验
        Preconditions.checkArgument(StringUtils.isNotBlank(id), "用户ID不能为空");

        // 2. 调用Service（所有业务逻辑在Service层）
        User user = userService.selectUserById(id);

        // 3. 返回结果（可选：记录日志）
        return ResponseResult.success(user);
    }

    @Override
    public ResponseResult<PageInfo<User>> pageList(User user) {
        // 分页查询必须调用startDubboPage()
        startDubboPage();
        List<User> list = userService.selectUserList(user);
        return ResponseResult.success(new PageInfo<>(list));
    }

    @Override
    public ResponseResult<Integer> add(User user) {
        // 1. 参数校验
        Preconditions.checkNotNull(user, "用户信息不能为空");

        // 2. 记录日志
        log.info("创建用户，用户名：{}", user.getUsername());

        // 3. 调用Service
        int rows = userService.insertUser(user);

        // 4. 返回结果
        return ResponseResult.success(rows);
    }
}
```

**❌ 错误示例**（违反职责边界）：
```java
// ❌ 错误1：在DubboApi中构建查询条件（应该在Service层）
@Override
public ResponseResult<List<User>> listActiveUsers(String name) {
    LambdaQueryWrapper<User> wrapper = new LambdaQueryWrapper<>();
    wrapper.eq(User::getStatus, 1);
    if (StringUtils.isNotBlank(name)) {
        wrapper.like(User::getUsername, name);
    }
    List<User> list = userMapper.selectList(wrapper);  // 还直接调用Mapper！
    return ResponseResult.success(list);
}

// ❌ 错误2：在DubboApi中做业务判断（应该在Service层）
@Override
public ResponseResult<Integer> updateStatus(String id, Integer status) {
    User user = userMapper.selectById(id);
    if (user.getStatus() == 1 && status == 0) {
        // 业务逻辑：如果当前是启用状态，禁用前检查是否有未完成订单
        Long count = orderMapper.selectCount(
            new LambdaQueryWrapper<Order>()
                .eq(Order::getUserId, id)
                .eq(Order::getStatus, "PENDING")
        );
        if (count > 0) {
            throw new BusinessException("该用户有未完成订单，不能禁用");
        }
    }
    user.setStatus(status);
    return ResponseResult.success(userMapper.updateById(user));
}

// ❌ 错误3：在DubboApi中循环调用（应该在Service层批量处理）
@Override
public ResponseResult<Integer> batchUpdate(List<User> users) {
    int count = 0;
    for (User user : users) {
        userMapper.updateById(user);
        count++;
    }
    return ResponseResult.success(count);
}

// ✅ 正确做法：所有业务逻辑放在Service层
@Override
public ResponseResult<Integer> updateStatus(String id, Integer status) {
    // DubboApi只负责参数校验和调用Service
    Preconditions.checkArgument(StringUtils.isNotBlank(id), "用户ID不能为空");
    int rows = userService.updateUserStatus(id, status);  // 业务逻辑在Service
    return ResponseResult.success(rows);
}
```

**Controller层规范（同理）**：
```java
import cn.city.parking.common.core.utils.ValidateUtil;
import cn.city.parking.common.core.web.domain.ResponseResult;

// ✅ Controller也是薄层，职责相同
@RestController
@RequestMapping("/user")
public class UserController {

    @Autowired
    private IUserService userService;

    @GetMapping("/{id}")
    public ResponseResult<User> getInfo(@PathVariable String id) {
        // 1. 参数校验（简单参数）
        Preconditions.checkArgument(StringUtils.isNotBlank(id), "用户ID不能为空");

        // 2. 调用Service
        User user = userService.selectUserById(id);

        // 3. 返回结果
        return ResponseResult.success(user);
    }

    @PostMapping
    public ResponseResult<Integer> add(@RequestBody User user) {
        // 1. 参数校验（复杂对象，使用ValidateUtil）
        ValidateUtil.validate(user);

        // 2. 调用Service
        int rows = userService.insertUser(user);

        // 3. 返回结果
        return ResponseResult.success(rows);
    }
}
```

**参数校验规范**：

有两种参数校验方式，根据场景选择：

**方式1：Preconditions校验**（简单参数）
```java
// ✅ 适用场景：基本类型、字符串等简单参数
import com.google.common.base.Preconditions;

@Override
public ResponseResult<User> getInfo(String id) {
    // 校验非空
    Preconditions.checkArgument(StringUtils.isNotBlank(id), "用户ID不能为空");

    // 校验条件
    Preconditions.checkArgument(age > 0, "年龄必须大于0");

    // 校验非null
    Preconditions.checkNotNull(user, "用户对象不能为空");

    return ResponseResult.success(userService.selectUserById(id));
}
```

**方式2：ValidateUtil.validate()校验**（复杂对象，推荐）
```java
// ✅ 适用场景：复杂对象，需要校验多个字段
import cn.city.parking.common.core.utils.ValidateUtil;

@PostMapping
public ResponseResult<Integer> add(@RequestBody User user) {
    // 自动校验对象中所有带@NotBlank、@Size等注解的字段
    ValidateUtil.validate(user);

    int rows = userService.insertUser(user);
    return ResponseResult.success(rows);
}
```

**ValidateUtil使用说明**：
- ✅ **自动校验**：读取对象中的`@NotBlank`、`@Size`、`@Email`等注解
- ✅ **自动抛异常**：校验失败自动抛出`BusinessException`，全局异常处理器会处理
- ✅ **错误信息**：自动拼接所有校验失败的message，用分号分隔
- ✅ **适用对象**：Entity、DTO、VO等所有JavaBean对象

**关键规范**：
- ✅ **DubboApi继承 `cn.city.parking.common.dubbo.filter.base.BaseDubboApi`**（注意包路径）
- ✅ **返回值必须用ResponseResult<T>带泛型**
- ✅ **分页查询必须调用startDubboPage()**
- ✅ **参数校验（推荐但非强制）**：
  - 简单参数：用`Preconditions.checkArgument()`
  - 复杂对象：用`ValidateUtil.validate()`
  - 校验注解可加在Entity、DTO、VO等任何JavaBean对象上
  - Controller层的参数校验根据实际情况灵活选择
- ✅ **DubboApi/Controller保持薄层，所有业务逻辑必须放在Service层**
- ❌ **不要随意捕获异常**（全局异常处理器会自动处理）
- ❌ **永远不要捕获BusinessException**（业务异常必须向上抛出）
- ❌ **不要在DubboApi/Controller中写业务逻辑**（查询条件构建、业务判断、循环处理等）

### 3-4. Service规范
```java
// Service接口
public interface IUserService extends IService<User> {  // ✅ 继承IService
    User selectUserById(String id);
}

// Service实现
@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements IUserService {

    @Override
    @Transactional(rollbackFor = Exception.class)  // ✅ 增删改必须加事务
    public int insertUser(User user) {
        return baseMapper.insert(user);
    }
}
```

### 5. Mapper规范
```java
// ✅ 不需要@Mapper注解（common-server已自动扫描）
public interface UserMapper extends BaseMapper<User> {
    User selectByUsername(@Param("username") String username);
}

// ✅ 框架已自动注入批量方法
userMapper.insertBatchSomeColumn(userList);  // 批量插入（排除updateTime等UPDATE字段）
```

### 6. 启动类规范
```java
@Slf4j                    // ✅ 只需2个基础注解
@SpringBootApplication
public class CityParkingXxxApplication {
    public static void main(String[] args) {
        SpringApplication.run(CityParkingXxxApplication.class, args);
    }
}
```

**❌ 不需要添加**：`@EnableDubbo`、`@EnableAsync`、`@MapperScan`、`@ComponentScan`、`@EnableDiscoveryClient`（common-server已自动配置）

**✅ 按需添加**：`@EnableCaching`（需要Spring Cache）、`@EnableScheduling`（需要定时任务）

### 7. 日志规范
```java
@Slf4j
public class OrderDubboApiImpl extends BaseDubboApi {

    @Override
    public ResponseResult<Integer> add(Order order) {
        log.info("创建订单，用户ID：{}，金额：{}元", order.getUserId(), order.getAmount());
        int rows = orderService.insertOrder(order);
        log.info("订单创建成功，订单ID：{}", order.getId());
        return ResponseResult.success(rows);
    }
}
```

**日志级别**：
- INFO：关键业务节点（CUD操作）
- WARN：可恢复异常、降级处理
- ERROR：系统错误、需要告警

**必须记录**：CUD操作、外部接口调用、异常捕获、关键分支判断

**敏感信息脱敏**：密码、身份证、手机号、银行卡

### 8. 核心类包路径（重要）
```java
// ✅ 正确路径
import cn.city.parking.common.dubbo.filter.base.BaseDubboApi;
import cn.city.parking.common.core.web.domain.BusinessEntity;
import cn.city.parking.common.core.web.domain.ResponseResult;
import com.github.pagehelper.PageInfo;
import cn.city.parking.common.redis.RedisUtils;

// ❌ 错误路径
import cn.city.parking.common.auth.base.BaseDubboApi;  // 错误！旧路径已废弃
```

### 9. Redis使用规范

**核心原则**：❌ **不要随意使用Redis缓存**（如无必要，不要缓存）

**何时使用缓存**（必须同时满足）：
- ✅ 查询频率 > 100次/分钟
- ✅ 数据变更频率 < 10次/天
- ✅ 数据量 < 1MB
- ✅ 可容忍短暂不一致

```java
// ✅ 基础操作
RedisUtils.setCacheObject("user:info:" + id, user, 3600);  // 存入缓存（3600秒）
User user = RedisUtils.getCacheObject("user:info:" + id, User.class);  // 获取缓存
RedisUtils.deleteObject("user:info:" + id);  // 删除缓存

// ⚠️ 批量删除性能警告
RedisUtils.batchDeleteObj("order:list:*");  // keys命令扫描全库，生产环境禁用！
```

**缓存更新策略**：先更新数据库，再删除缓存

**分布式锁**：
```java
@Autowired
private Locker locker;

locker.lock(lockKey, 10, () -> {
    // 业务逻辑，10秒后自动释放
});
```

### 10. 代码风格规范

**核心原则**：新代码必须遵循 **Spring Java Format** 规范

**Maven配置**：
```xml
<plugin>
    <groupId>io.spring.javaformat</groupId>
    <artifactId>spring-javaformat-maven-plugin</artifactId>
    <version>0.0.39</version>
</plugin>
```

**提交前必做**：
```bash
mvn spring-javaformat:apply    # 格式化代码
mvn spring-javaformat:validate # 检查格式
```

**IDEA插件**：Settings → Plugins → 搜索 `Spring Java Format`

### 11. SOLID设计原则

**核心原则**：编写可维护、可扩展、易测试的代码

#### S - 单一职责原则（Single Responsibility Principle）
**定义**：一个类只负责一件事，只有一个引起它变化的原因

**✅ 正确示例**：
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

**❌ 错误示例**：
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

#### O - 开闭原则（Open-Closed Principle）
**定义**：对扩展开放，对修改关闭

**✅ 正确示例**：
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

**❌ 错误示例**：
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

#### L - 里氏替换原则（Liskov Substitution Principle）
**定义**：子类可以替换父类，且不改变程序的正确性

**✅ 正确示例**：
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

**❌ 错误示例**：
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

#### I - 接口隔离原则（Interface Segregation Principle）
**定义**：使用多个专门的接口，而不是单一的总接口

**✅ 正确示例**：
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

**❌ 错误示例**：
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

#### D - 依赖倒置原则（Dependency Inversion Principle）
**定义**：依赖抽象，不依赖具体实现

**✅ 正确示例**：
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

**❌ 错误示例**：
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

**SOLID综合应用场景**：
- **S**：DubboApi/Controller只负责接口适配，Service负责业务逻辑，Mapper负责数据访问
- **O**：使用策略模式、工厂模式、模板方法模式支持扩展
- **L**：子类增强父类，不改变原有行为（如：VipUserService继承UserService）
- **I**：拆分IUserQueryService、IUserCommandService，而不是一个大而全的IUserService
- **D**：Service依赖抽象接口，通过@Autowired注入，不使用new创建依赖

**实践建议**：
- ✅ 每个类/接口设计前，先问自己：它的单一职责是什么？
- ✅ 新增功能时，优先考虑扩展而不是修改（开闭原则）
- ✅ 依赖注入使用@Autowired，面向接口编程
- ✅ 使用设计模式（策略、工厂、模板方法）应对变化
- ❌ 避免"上帝类"（God Class）：一个类超过500行、职责超过3个
- ❌ 避免"大泥球"（Big Ball of Mud）：所有代码耦合在一起

### 12. 文档生成日期时间规范

**核心原则**：所有自动生成的文档（如修改报告、测试报告、部署文档等）中的日期时间，必须使用环境信息中的系统日期时间

**规范要求**：
- ✅ **日期来源**：从环境信息（`<env>`标签）中的 `Today's date` 字段获取
- ✅ **格式要求**：使用标准格式 `yyyy-MM-dd HH:mm:ss`（例如：2025-11-12 14:30:00）
- ✅ **适用场景**：代码修改报告、提测文档、版本发布记录、变更日志等所有自动生成的文档
- ❌ **不要**：硬编码日期、使用历史日期、或随意填写日期

**示例**：
```markdown
**报告生成时间**：2025-11-12 14:30:00
**文档创建日期**：2025-11-12
**版本发布时间**：2025-11-12 10:00:00
```

**实现说明**：
- 环境信息中的日期格式为 `yyyy-MM-dd`，如需精确时间可补充当前时分秒
- 确保所有快捷命令（如 `/diff-report`、`/generate-tests`）生成的文档都遵循此规范
- 文档更新时，需要更新时间戳以反映最新修改时间

---

## 框架已自动配置功能

**详见** → [框架功能详解](docs/guides/framework-features.md)

common-server已自动配置：
1. **自动注解**：@EnableDubbo、@EnableAsync、@MapperScan、@ComponentScan、@EnableDiscoveryClient、@EnableAspectJAutoProxy
2. **3个线程池**：myThreadPoolTaskExecutor、ttlExecutorService、userTaskThreadPool
3. **自动填充**：createTime、updateTime、createBy、updateBy、delFlag、id（雪花ID）
4. **ID生成策略**：snowflake（默认）、redis-inc、snowflake-seata
5. **批量操作**：insertBatchSomeColumn（排除UPDATE字段）
6. **MyBatis Plus拦截器**：乐观锁、多租户（可选）
7. **数据权限**：@MyDataScope注解
8. **Jackson时区配置**：自动处理Date/LocalDateTime
9. **Sentinel异常处理**：MyWebMvcBlockExceptionHandler
10. **Nacos配置项**：custom-config.server、custom-config.task.pool

---

## 详细规范参考

### 异步任务使用
**详见** → [异步任务使用规范](docs/guides/detailed-standards.md#1-异步任务使用规范)

**线程池选择**：
- `myThreadPoolTaskExecutor`：普通异步任务（不需要traceId）
- `ttlExecutorService`：需要链路追踪（自动传递MDC）
- `userTaskThreadPool`：需要登录信息（传递SaToken上下文）

**@Async默认使用ttlExecutorService**，自动传递MDC，推荐不指定线程池

### API幂等性
**详见** → [API幂等性规范](docs/guides/detailed-standards.md#2-api幂等性规范)

**方式**：
1. @NoRepeatSubmit注解（防止前端重复提交）
2. 业务唯一键（数据库唯一索引）
3. 分布式锁（高并发场景）
4. 状态机（状态变更场景）

### Mapper继承
**详见** → [Mapper继承说明](docs/guides/detailed-standards.md#3-mapper继承说明)

```java
// ✅ 继承BaseMapper即可（框架已注入批量方法）
public interface UserMapper extends BaseMapper<User> {
}

// 使用
userMapper.insertBatchSomeColumn(userList);  // 批量插入
```

### 性能优化
**详见** → [性能优化规范](docs/guides/detailed-standards.md#4-性能优化规范)

**核心原则**：
- ✅ 所有列表查询必须分页
- ✅ 批量操作控制在1000条以内
- ✅ IN条件不超过500个
- ❌ 禁止N+1查询
- ❌ 禁止SELECT *
- ❌ 禁止前导模糊查询（LIKE '%xx%'）

### 分布式事务
**详见** → [分布式事务处理规范](docs/guides/detailed-standards.md#5-分布式事务处理规范)

**方案**：
1. 本地事务（@Transactional）：单库操作
2. 可靠消息最终一致性（推荐）：本地消息表 + 定时补偿
3. 接口幂等性保障（必须）
4. 补偿机制（必须）

---

## 配置规范

**详见** → [配置指南](docs/guides/configuration-guide.md)

### POM配置

**⚠️ 关键架构说明**：
- 根pom（city-parking-xxx/pom.xml）只是**聚合器**，用于本地开发便利
- 根pom **不会发布到Maven私库**（配置deploy skip）
- API和Server模块**直接继承city-parking-parent**，不继承根pom
- 只有API模块会发布到Maven私库

**根POM（city-parking-xxx/pom.xml）**：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>

    <!-- ✅ 根pom的parent是city-parking-parent -->
    <parent>
        <groupId>cn.city-parking</groupId>
        <artifactId>city-parking-parent</artifactId>
        <version>2.0.0-SNAPSHOT</version>
        <relativePath/>
    </parent>

    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-xxx</artifactId>
    <version>2.0.0-SNAPSHOT</version>
    <packaging>pom</packaging>
    <name>city-parking-xxx</name>
    <description>XXX服务</description>

    <!-- ✅ 聚合子模块 -->
    <modules>
        <module>city-parking-xxx-api</module>
        <module>city-parking-xxx-server</module>
    </modules>

    <build>
        <plugins>
            <!-- ✅ 根pom禁止发布到Maven私库 -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-deploy-plugin</artifactId>
                <version>2.8.2</version>
                <configuration>
                    <skip>true</skip>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

**API模块POM（city-parking-xxx-api/pom.xml）**：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>

    <!-- ✅ API模块直接继承city-parking-parent -->
    <!-- ❌ 不要继承根pom（city-parking-xxx） -->
    <parent>
        <groupId>cn.city-parking</groupId>
        <artifactId>city-parking-parent</artifactId>
        <version>2.0.0-SNAPSHOT</version>
        <relativePath/>
    </parent>

    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-xxx-api</artifactId>
    <version>2.0.0-SNAPSHOT</version>
    <packaging>jar</packaging>
    <name>city-parking-xxx-api</name>
    <description>XXX服务API</description>

    <dependencies>
        <!-- ✅ API模块必须依赖city-parking-common-auth -->
        <dependency>
            <groupId>cn.city-parking</groupId>
            <artifactId>city-parking-common-auth</artifactId>
        </dependency>

        <!-- ❌ 错误：不要依赖city-parking-common-core -->
        <!-- common-auth已经包含了common-core -->
    </dependencies>

    <!-- ⚠️ API模块不配置deploy插件，默认会发布到Maven私库 -->
</project>
```

**Server模块POM（city-parking-xxx-server/pom.xml）**：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>

    <!-- ✅ Server模块直接继承city-parking-parent -->
    <!-- ❌ 不要继承根pom（city-parking-xxx） -->
    <parent>
        <groupId>cn.city-parking</groupId>
        <artifactId>city-parking-parent</artifactId>
        <version>2.0.0-SNAPSHOT</version>
        <relativePath/>
    </parent>

    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-xxx-server</artifactId>
    <version>2.0.0-SNAPSHOT</version>
    <packaging>jar</packaging>
    <name>city-parking-xxx-server</name>
    <description>XXX服务实现</description>

    <dependencies>
        <!-- ✅ 1. common-server（已包含Redis、Auth、MySQL、Druid） -->
        <dependency>
            <groupId>cn.city-parking</groupId>
            <artifactId>city-parking-common-server</artifactId>
        </dependency>

        <!-- ✅ 2. 本服务API模块 -->
        <dependency>
            <groupId>cn.city-parking</groupId>
            <artifactId>city-parking-xxx-api</artifactId>
            <version>2.0.0-SNAPSHOT</version>
        </dependency>

        <!-- ❌ 以下依赖不要添加（common-server已包含） -->
        <!-- city-parking-common-redis -->
        <!-- city-parking-common-auth -->
        <!-- mysql-connector-j -->
        <!-- druid-spring-boot-starter -->
    </dependencies>

    <build>
        <plugins>
            <!-- ✅ Spring Boot打包插件（必须配置mainClass） -->
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <version>${spring-boot.version}</version>
                <configuration>
                    <mainClass>cn.city.parking.xxx.CityParkingXxxApplication</mainClass>
                </configuration>
                <executions>
                    <execution>
                        <goals>
                            <goal>repackage</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>

            <!-- ✅ 禁止Server模块发布到Maven私库 -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-deploy-plugin</artifactId>
                <version>2.8.2</version>
                <configuration>
                    <skip>true</skip>
                </configuration>
            </plugin>

            <!-- ✅ 代码格式化插件 -->
            <plugin>
                <groupId>io.spring.javaformat</groupId>
                <artifactId>spring-javaformat-maven-plugin</artifactId>
                <version>0.0.39</version>
            </plugin>
        </plugins>
    </build>
</project>
```

**⚠️ 为什么API和Server不继承根pom？**
1. 根pom不会发布到Maven私库
2. 如果API继承根pom，其他项目引用API时会找不到根pom（因为根pom未发布）
3. city-parking-parent已经配置了所有必要的依赖管理和Maven私库地址
4. 根pom只是一个聚合器，方便本地多模块开发

### 配置文件

**⚠️ 必须创建的配置文件**：
- `bootstrap.yml`（主配置）
- `bootstrap-dev.yml`（开发环境）
- `bootstrap-prod.yml`（生产环境）
- `bootstrap-test.yml`（测试环境）

#### bootstrap.yml（主配置文件）

**⚠️ 关键规范**：
1. 只需修改 `server.port` 和 `spring.application.name`
2. 使用 `@profileActive@` 而非 `${profiles.active:dev}`
3. 使用 `${nacos.server-addr}` 而非 `${custom-config.server.nacos.address}`

```yaml
server:
  port: 9220  # ✅ 1. 修改为你的端口

spring:
  application:
    name: city-parking-xxx  # ✅ 2. 修改为你的服务名
  profiles:
    active: @profileActive@  # ✅ 注意：使用Maven占位符
  main:
    allow-bean-definition-overriding: true
  cloud:
    nacos:
      discovery:
        server-addr: ${nacos.server-addr}  # ✅ 占位符格式
        namespace: ${nacos.namespace}
        group: ${nacos.group}
      config:
        server-addr: ${nacos.server-addr}
        file-extension: yml
        namespace: ${nacos.namespace}
        group: ${nacos.group}
        shared-configs:
          - data-id: application-${spring.profiles.active}.${spring.cloud.nacos.config.file-extension}
            group: ${nacos.group}
            refresh: true
          - data-id: common-${spring.profiles.active}.${spring.cloud.nacos.config.file-extension}
            group: ${nacos.group}
            refresh: true
    sentinel:
      transport:
        dashboard: ${sentinel.server-addr}
      eager: true
      datasource:
        flow:
          nacos:
            server-addr: ${nacos.server-addr}
            data_id: ${spring.application.name}-flow-rules
            namespace: ${sentinel.namespace}
            group_id: ${sentinel.group}
            rule-type: flow
            data-type: json

dubbo:
  application:
    name: ${spring.application.name}
    qos-enable: false
  registry:
    address: nacos://${spring.cloud.nacos.discovery.server-addr}
    parameters:
      namespace: ${spring.cloud.nacos.discovery.namespace}
```

#### bootstrap-dev.yml（开发环境）

```yaml
# 自定义参数（开发环境）
nacos:
  server-addr: @serverAddr@  # ✅ Maven占位符，从pom.xml读取
  namespace: @namespace@
  group: DEFAULT_GROUP
sentinel:
  server-addr: 127.0.0.1:8888
  namespace: sentinel
  group: DEFAULT_GROUP
```

#### bootstrap-prod.yml（生产环境）

```yaml
# 自定义参数（生产环境）
nacos:
  server-addr: your-prod-nacos:8848  # ✅ 直接配置生产环境地址
  namespace: prod
  group: DEFAULT_GROUP
sentinel:
  server-addr: your-prod-sentinel:8888
  namespace: sentinel
  group: DEFAULT_GROUP
```

#### bootstrap-test.yml（测试环境）

```yaml
# 自定义参数（测试环境）
nacos:
  server-addr: 172.26.145.149:8848
  namespace: test
  group: DEFAULT_GROUP
sentinel:
  server-addr: 172.26.145.190:8089
  namespace: sentinel
  group: DEFAULT_GROUP
```

**配置说明**：
- 不同环境通过 `-Dspring.profiles.active=dev/prod/test` 切换
- Maven打包时通过 `-P dev/prod/test` 指定环境，会替换`@serverAddr@`等占位符
- bootstrap-{env}.yml 中的配置会覆盖 bootstrap.yml 中的占位符

**❌ 常见错误**：
- profiles.active: ${profiles.active:dev}（应该是 @profileActive@）
- server-addr: ${custom-config.server.nacos.address}（应该是 ${nacos.server-addr}）
- 忘记创建环境配置文件

### 数据库规范

#### 必备字段（BusinessEntity已包含，无需声明）
```sql
id           VARCHAR(64)   PRIMARY KEY COMMENT '主键（雪花ID）',
create_time  DATETIME      NOT NULL    COMMENT '创建时间',
update_time  DATETIME      NOT NULL    COMMENT '更新时间'
```

#### 可选字段（⚠️ 如果使用，必须在实体类中显式声明）

**创建人/更新人字段**：
```sql
create_by    VARCHAR(64)               COMMENT '创建人',
update_by    VARCHAR(64)               COMMENT '更新人'
```
```java
// ✅ 实体类必须声明
@TableField(value = "create_by", fill = FieldFill.INSERT)
private String createBy;

@TableField(value = "update_by", fill = FieldFill.UPDATE)
private String updateBy;
```

**逻辑删除字段**：
```sql
del_flag     TINYINT(1)    DEFAULT 0   COMMENT '删除标志（0-存在，1-删除）'
```
```java
// ✅ 实体类必须声明
@TableField(value = "del_flag", fill = FieldFill.INSERT)
private Integer delFlag;
```

**乐观锁字段**：
```sql
revision     BIGINT(20)    DEFAULT 0   COMMENT '乐观锁版本号'
```
```java
// ✅ 实体类必须声明
@Version
private Long revision;
```

**备注字段**：
```sql
remark       VARCHAR(500)              COMMENT '备注'
```
```java
// ✅ 实体类必须声明
private String remark;
```

**⚠️ 关键提醒**：
- BusinessEntity **只包含** id、createTime、updateTime
- create_by、update_by、del_flag、revision **不在基类中**
- 如果数据库表有这些字段，**必须在实体类中显式声明**
- 框架的自动填充功能会处理这些字段，但前提是实体类中有对应属性

---

## 完整实战案例

**详见** → [docs/examples/](docs/examples/)

| 案例 | 说明 | 文件 |
|------|------|------|
| **用户管理** | 标准CRUD（Entity、Mapper、Service、DubboApi） | [standard-crud.md](docs/examples/standard-crud.md) |
| **系统配置** | 带缓存的热点查询（Redis使用） | [cache-usage.md](docs/examples/cache-usage.md) |
| **用户导入** | 批量操作与事务（insertBatchSomeColumn） | [batch-operations.md](docs/examples/batch-operations.md) |
| **订单查询** | 复杂查询与多表关联（DTO、Mapper.xml） | [complex-query.md](docs/examples/complex-query.md) |
| **优惠券领取** | 分布式锁防止并发（Locker） | [distributed-lock.md](docs/examples/distributed-lock.md) |

---

## 常见错误对照表

| 错误写法 ❌ | 正确写法 ✅ | 原因 |
|------------|------------|------|
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

## 快速决策指南

### 🤔 何时使用Redis缓存？
**条件**（同时满足）：查询频率 > 100次/分钟 + 数据变更 < 10次/天 + 数据量 < 1MB + 允许短暂不一致

**场景**：
- ✅ 系统配置、字典数据、用户权限
- ❌ 订单信息、库存数据、金融数据

### 🤔 何时使用分布式锁？
**场景**：
- ✅ 库存扣减、优惠券领取、订单号生成、定时任务防重
- ❌ 普通查询、普通新增（ID用雪花算法）

**优先级**：数据库约束 > 乐观锁 > 分布式锁

### 🤔 何时使用事务？
**必须**：所有增删改操作、批量操作、多表操作
**不需要**：纯查询操作

### 🤔 何时记录日志？
**必须**：用户操作（登录、下单、支付）、数据修改、异常情况、外部调用
**不需要**：普通查询、内部方法调用

---

## 重要提醒

### ❌ 绝对不要做的事

**架构层面**：
1. **不要创建**：common包、utils包、BusinessException、ResponseResult（已有独立仓库）
2. **不要使用错误路径**：`cn.city.parking.common.auth.base.BaseDubboApi`（✅ 正确：`cn.city.parking.common.dubbo.filter.base.BaseDubboApi`）
3. **不要使用不存在的方法**：`RedisUtils.deleteKeys()`（✅ 正确：`batchDeleteObj()`）

**模块结构**：
4. **Entity包路径错误**：`cn.city.parking.xxx.entity`（✅ 正确：`cn.city.parking.xxx.api.entity`，必须在api包下）
5. **API模块依赖错误**：依赖`city-parking-common-core`（✅ 正确：`city-parking-common-auth`）
6. **Server模块冗余依赖**：不要重复添加Redis、Auth、MySQL、Druid（common-server已包含）

**配置文件**：
7. **bootstrap.yml占位符错误**：`${custom-config.server.nacos.*}`（✅ 正确：`${nacos.*}`）
8. **profiles.active错误**：`${profiles.active:dev}`（✅ 正确：`@profileActive@`）

**代码规范**：
9. **不要在DubboApi中使用try-catch**（全局异常处理器会自动处理）
10. **不要随意捕获BusinessException**（业务异常必须向上抛出）
11. **不要忘记**：ResponseResult泛型、@TableName、@JsonFormat、@Transactional
12. **不要添加**：@Mapper、@EnableDubbo、@MapperScan（common-server已配置）
13. **不要随意使用Redis缓存**（如无必要，不要缓存）

### ✅ 必须做的事
1. **实体类**：
   - 继承BusinessEntity + @TableName + LocalDateTime字段@JsonFormat
   - Entity包路径必须在`xxx.api.entity`下（不是`xxx.entity`）
   - 如果数据库有create_by、update_by、del_flag、revision字段，必须在实体类中显式声明
2. **配置文件**：
   - 必须创建4个文件：bootstrap.yml + bootstrap-dev/prod/test.yml
   - 使用`@profileActive@`（不是`${profiles.active:dev}`）
3. **Service接口**：继承IService<T>
4. **Service实现**：增删改方法@Transactional(rollbackFor = Exception.class)
5. **DubboApi**：返回ResponseResult<T>带泛型 + 分页调用startDubboPage() + 参数校验Preconditions
6. **关键操作**：添加日志（@Slf4j + log.info）
7. **方法注释**：JavaDoc格式（@param、@return）
8. **代码提交前**：mvn spring-javaformat:apply

---

## 开发流程

### 新建微服务项目（完整步骤）

**1. 创建根POM（city-parking-xxx/pom.xml）**
```xml
<parent>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-parent</artifactId>
    <version>2.0.0-SNAPSHOT</version>
    <relativePath/>
</parent>
<artifactId>city-parking-xxx</artifactId>
<packaging>pom</packaging>
<modules>
    <module>city-parking-xxx-api</module>
    <module>city-parking-xxx-server</module>
</modules>
<build>
    <plugins>
        <!-- 根pom禁止发布到Maven私库 -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-deploy-plugin</artifactId>
            <configuration>
                <skip>true</skip>
            </configuration>
        </plugin>
    </plugins>
</build>
```

**2. 创建API模块（city-parking-xxx-api）**
- ⚠️ **parent直接继承city-parking-parent**（不继承根pom）
- POM依赖：`city-parking-common-auth`
- 不配置deploy插件（默认发布到Maven私库）
- 创建包结构：`cn.city.parking.xxx.api.entity`（⚠️ 必须在api包下）
- 创建Entity：继承BusinessEntity + @TableName + @JsonFormat
- 创建DubboApi接口：6个标准方法

**3. 创建Server模块（city-parking-xxx-server）**
- ⚠️ **parent直接继承city-parking-parent**（不继承根pom）
- POM依赖：`city-parking-common-server` + `city-parking-xxx-api`（⚠️ 不要重复添加Redis、Auth、MySQL、Druid）
- 配置mainClass：`<mainClass>cn.city.parking.xxx.XxxApplication</mainClass>`
- 配置maven-deploy-plugin：`<skip>true</skip>`
- 创建配置文件（⚠️ 必须创建4个文件）：
  - `bootstrap.yml`：主配置，使用`@profileActive@` + `${nacos.server-addr}`
  - `bootstrap-dev.yml`：开发环境，使用`@serverAddr@`占位符
  - `bootstrap-prod.yml`：生产环境，直接配置地址
  - `bootstrap-test.yml`：测试环境，直接配置地址
- 创建启动类：只需`@Slf4j` + `@SpringBootApplication`（⚠️ 不要添加@EnableDubbo等）
- 创建Mapper、Service、DubboApi实现

**4. 验证清单**
- [ ] ⚠️ **API和Server模块的parent都是city-parking-parent**（不是根pom）
- [ ] Entity在`xxx.api.entity`包下（不是`xxx.entity`）
- [ ] 如果数据库有create_by、update_by、del_flag字段，实体类中已显式声明
- [ ] API模块依赖是`common-auth`（不是`common-core`）
- [ ] Server模块只依赖`common-server`和本服务API（没有冗余依赖）
- [ ] 创建了4个配置文件：bootstrap.yml + bootstrap-dev/prod/test.yml
- [ ] bootstrap.yml使用`@profileActive@`（不是`${profiles.active:dev}`）
- [ ] bootstrap.yml占位符是`${nacos.*}`（不是`${custom-config...}`）
- [ ] Server模块配置了mainClass和deploy skip
- [ ] 根pom配置了deploy skip（禁止发布到Maven私库）

### 新建CRUD功能
1. API模块创建Entity（继承BusinessEntity + @TableName + **包路径在api.entity下**）
2. API模块创建DubboApi接口（6个标准方法）
3. Server模块创建Mapper接口（继承BaseMapper）
4. Server模块创建Service接口（继承IService）和实现（继承ServiceImpl + @Transactional）
5. Server模块创建DubboApi实现（继承BaseDubboApi + ResponseResult<T> + startDubboPage()）

### 标准方法命名
**DubboApi**：pageList、allList、getInfo、add、edit、remove
**Service**：select{ClassName}ById、select{ClassName}List、insert{ClassName}、update{ClassName}、delete{ClassName}ById、delete{ClassName}ByIds

---

## 推荐工具类
- **字符串**：`org.apache.commons.lang3.StringUtils`
- **日期**：`cn.hutool.core.date.DateUtil`
- **集合**：`com.google.common.collect.*`（Guava）
- **校验**：`com.google.common.base.Preconditions`
- **Redis**：`cn.city.parking.common.redis.RedisUtils`
- **分布式锁**：`cn.city.parking.common.redis.service.Locker`
- **防重复提交**：`@NoRepeatSubmit`

---

## 快捷命令（Claude Code）
- `/new-crud` - 创建完整CRUD功能
- `/add-field` - 为实体类添加新字段
- `/new-api` - 在已有模块添加新接口
- `/fix-cache` - 修复缓存问题
- `/diff-report` - 生成代码修改报告（提交前自查）
- `/generate-tests` - 生成单元测试代码
- `/review-code` - 代码审查清单

---

## 参考项目
- **city-parking-eop**：运营平台（完整示例）
- **city-parking-template**：服务模板
- **city-parking-bff-eop**：BFF服务示例

---

## 联系与反馈
如有框架问题或改进建议，请联系架构组。
