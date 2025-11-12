# 【通知】City Parking 2.0 框架文档更新

各位同事，大家好！

框架文档已更新，主要新增**参数校验规范**和**2个快捷命令**，请大家查阅。

---

## 📌 核心更新（5分钟快速了解）

### 1️⃣ 参数校验规范（推荐，非强制）

**说明**：参数校验不是强制要求，根据业务场景灵活选择。以下是推荐做法。

**原来的写法**（繁琐）：
```java
@PostMapping
public ResponseResult<Integer> add(@RequestBody User user) {
    if (user == null) {
        throw new BusinessException("用户信息不能为空");
    }
    if (StringUtils.isBlank(user.getUsername())) {
        throw new BusinessException("用户名不能为空");
    }
    if (user.getUsername().length() < 2 || user.getUsername().length() > 30) {
        throw new BusinessException("用户名长度必须在2-30个字符之间");
    }
    // ... 还有N个字段要校验
}
```

**现在的写法**（简洁）：
```java
// 第一步：在Entity或DTO上添加注解
// 可以加在Entity上（框架不强制使用DTO/VO，所以可以直接在Entity上加）
@NotBlank(message = "用户名不能为空")
@Size(min = 2, max = 30, message = "用户名长度必须在2-30个字符之间")
private String username;

// 也可以加在DTO上（如果使用了DTO）
public class UserCreateDTO {
    @NotBlank(message = "用户名不能为空")
    private String username;
}

// 第二步：DubboApi/Controller中一行代码搞定
@PostMapping
public ResponseResult<Integer> add(@RequestBody User user) {
    ValidateUtil.validate(user);  // ✅ 自动校验所有字段

    int rows = userService.insertUser(user);
    return ResponseResult.success(rows);
}
```

**常用注解**：
- `@NotBlank(message = "不能为空")` - 字符串非空
- `@Size(min = 2, max = 30, message = "长度2-30")` - 长度限制
- `@Email(message = "邮箱格式不正确")` - 邮箱格式
- `@Pattern(regexp = "^1[3-9]\\d{9}$", message = "手机号格式不正确")` - 正则校验

**⚠️ 注意**：
- 校验注解可加在Entity、DTO、VO等任何JavaBean对象上
- 如需使用校验注解，message属性必填
- 参数校验不是强制要求，根据业务需要灵活选择

---

### 2️⃣ 新增快捷命令

#### 📊 `/diff-report` - 生成代码修改报告
提交代码前生成一份详细的修改报告，包含：
- 变更文件统计
- 功能变更说明
- 数据库变更
- 风险评估
- 部署说明

**使用**：在Claude Code中输入 `/diff-report`

---

#### 🧪 `/generate-tests` - 生成单元测试
自动为Service、DubboApi生成完整的单元测试代码。

**使用**：在Claude Code中输入 `/generate-tests`

---

### 3️⃣ Controller/DubboApi职责边界（重要规范）

**核心原则**：Controller/DubboApi是**薄薄的接口层**，只负责4件事。

**✅ 只能做**：
1. 参数校验
2. 调用Service
3. 记录日志
4. 返回结果

**❌ 不能做**（必须放在Service层）：
- 复杂的业务判断和计算
- 查询条件构建（LambdaQueryWrapper等）
- 直接调用Mapper（跨层调用）
- 循环处理数据
- 事务控制
- 缓存处理

**错误示例**：
```java
// ❌ 在DubboApi中构建查询条件
public ResponseResult<List<User>> listActiveUsers(String name) {
    LambdaQueryWrapper<User> wrapper = new LambdaQueryWrapper<>();
    wrapper.eq(User::getStatus, 1);
    if (StringUtils.isNotBlank(name)) {
        wrapper.like(User::getUsername, name);
    }
    List<User> list = userMapper.selectList(wrapper);  // 还直接调用Mapper
    return ResponseResult.success(list);
}
```

**正确示例**：
```java
// ✅ DubboApi只负责参数校验和调用Service
public ResponseResult<List<User>> listActiveUsers(String name) {
    List<User> list = userService.listActiveUsers(name);  // 业务逻辑在Service
    return ResponseResult.success(list);
}
```

---

### 4️⃣ SOLID设计原则（架构规范）

**核心5原则**：

| 原则 | 说明 | 示例 |
|------|------|------|
| **S** - 单一职责 | 一个类只负责一件事 | DubboApi负责接口适配，Service负责业务逻辑 |
| **O** - 开闭原则 | 对扩展开放，对修改关闭 | 使用策略模式，新增支付方式不修改原有代码 |
| **L** - 里氏替换 | 子类可以替换父类 | VipUserService继承UserService，增强但不改变原有行为 |
| **I** - 接口隔离 | 多个专门接口，不是大而全 | 拆分IUserQueryService、IUserCommandService |
| **D** - 依赖倒置 | 依赖抽象，不依赖具体实现 | 使用@Autowired注入接口，不使用new创建对象 |

**实践建议**：
- ✅ 每个类设计前，先问自己：它的单一职责是什么？
- ✅ 新增功能时，优先考虑扩展而不是修改
- ✅ 使用@Autowired注入依赖，面向接口编程
- ❌ 避免"上帝类"（一个类超过500行、职责超过3个）

---

## ✅ 行动建议

**立即执行**：
1. ✅ 查看完整文档：`.claude/UPDATE_NOTICE.md`（10分钟）
2. ✅ 查看标准案例：`.claude/docs/examples/standard-crud.md`（5分钟）
3. ✅ 新功能开发时使用新规范

**下次开发时**（推荐但非强制）：
1. ✅ 根据业务需要，在Entity/DTO字段添加校验注解（@NotBlank、@Size等）
2. ✅ DubboApi/Controller使用 `ValidateUtil.validate()` 校验
3. ✅ 提交前使用 `/diff-report` 生成修改报告

---

## 📖 快速示例

```java
// Entity类（api模块）
package cn.city.parking.order.api.entity;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Min;

@Data
@TableName("order_info")
public class Order extends BusinessEntity {

    @NotBlank(message = "订单号不能为空")
    private String orderNo;

    @NotBlank(message = "用户ID不能为空")
    private String userId;

    @Min(value = 0, message = "金额不能小于0")
    private BigDecimal amount;
}

// DubboApiImpl（server模块）
import cn.city.parking.common.core.utils.ValidateUtil;

@DubboService
public class OrderDubboApiImpl extends BaseDubboApi implements OrderDubboApi {

    @Override
    public ResponseResult<Integer> add(Order order) {
        ValidateUtil.validate(order);  // ✅ 一行代码搞定所有校验

        int rows = orderService.insertOrder(order);
        return ResponseResult.success(rows);
    }
}
```

---

## 💡 常见问题

**Q：参数校验是强制要求吗？**
A：不是强制要求，根据业务场景灵活选择。推荐在服务入口（DubboApi）添加校验。

**Q：校验注解可以加在DTO上吗？**
A：可以。可以加在Entity、DTO、VO等任何JavaBean对象上。因为框架不强制使用DTO/VO，所以可以直接在Entity上添加。

**Q：所有字段都要加注解吗？**
A：不是，根据业务需要灵活选择。对于必填字段或有格式要求的字段，推荐添加。

**Q：修改注解需要重启吗？**
A：是的，校验注解在启动时加载。

**Q：什么时候用Preconditions，什么时候用ValidateUtil？**
A：简单参数（String、int）用Preconditions，复杂对象（Entity、DTO）用ValidateUtil。

---

详细文档请查看：**`.claude/UPDATE_NOTICE.md`**

有问题随时反馈，谢谢！

---

**架构组**
2025-01-12
