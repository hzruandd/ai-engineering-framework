# City Parking 2.0 框架文档更新通知

**更新日期**：2025-01-12
**版本**：v2.0.1
**文档版本**：2025-01-12

---

## 📢 更新概要

本次更新主要补充了**参数校验规范**和**新增2个快捷命令**，优化了开发体验。

---

## 🎯 核心更新内容

### 1. 参数校验规范（推荐）

框架已内置 `ValidateUtil` 工具类和 `jakarta.validation-api` 校验注解，可以简化参数校验代码。

**⚠️ 说明**：参数校验不是强制要求，根据业务场景灵活选择。以下是推荐做法。

#### ✅ 推荐做法

**第一步：在Entity/DTO中添加校验注解**
```java
package cn.city.parking.xxx.api.entity;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Size;
import javax.validation.constraints.Email;
import javax.validation.constraints.Pattern;

@Data
@TableName("sys_user")
public class User extends BusinessEntity {

    @NotBlank(message = "用户名不能为空")
    @Size(min = 2, max = 30, message = "用户名长度必须在2-30个字符之间")
    private String username;

    @Pattern(regexp = "^1[3-9]\\d{9}$", message = "手机号格式不正确")
    private String phone;

    @Email(message = "邮箱格式不正确")
    @Size(max = 50, message = "邮箱长度不能超过50个字符")
    private String email;
}

// 或者在DTO上添加（如果使用了DTO）
public class UserCreateDTO {
    @NotBlank(message = "用户名不能为空")
    private String username;
    // ...
}
```

**说明**：
- 可以加在Entity、DTO、VO等任何JavaBean对象上
- 因为框架不强制使用DTO/VO，所以可以直接在Entity上添加
- 根据业务需要灵活选择是否添加

**第二步：在Controller/DubboApi中调用校验**
```java
import cn.city.parking.common.core.utils.ValidateUtil;

@PostMapping
public ResponseResult<Integer> add(@RequestBody User user) {
    // 一行代码自动校验所有带注解的字段
    ValidateUtil.validate(user);

    int rows = userService.insertUser(user);
    return ResponseResult.success(rows);
}
```

#### 📝 两种校验方式对比

| 场景 | 推荐方式 | 示例 |
|------|---------|------|
| **简单参数**（String、int等） | `Preconditions.checkArgument()` | `Preconditions.checkArgument(StringUtils.isNotBlank(id), "ID不能为空");` |
| **复杂对象**（Entity、DTO等） | `ValidateUtil.validate()` ⭐ | `ValidateUtil.validate(user);` |

#### 🎁 ValidateUtil的优势

- ✅ **自动校验**：读取实体类中的所有校验注解（@NotBlank、@Size、@Email等）
- ✅ **自动抛异常**：校验失败自动抛出`BusinessException`，无需手动try-catch
- ✅ **友好提示**：自动拼接所有校验失败的message，用分号分隔
- ✅ **代码简洁**：只需一行代码，替代大量if判断

#### 📚 常用校验注解

| 注解 | 说明 | 示例 |
|------|------|------|
| `@NotBlank` | 字符串不能为空（不为null、不为空字符串、不为空格） | `@NotBlank(message = "用户名不能为空")` |
| `@NotNull` | 值不能为null | `@NotNull(message = "状态不能为空")` |
| `@Size` | 字符串/集合/数组长度限制 | `@Size(min = 2, max = 30, message = "长度2-30")` |
| `@Email` | 邮箱格式校验 | `@Email(message = "邮箱格式不正确")` |
| `@Pattern` | 正则表达式校验 | `@Pattern(regexp = "^1[3-9]\\d{9}$", message = "手机号格式不正确")` |
| `@Min` / `@Max` | 数值范围校验 | `@Min(value = 0, message = "年龄不能小于0")` |

**⚠️ 注意**：所有校验注解的 `message` 属性必须填写，用于提示用户！

---

### 2. 新增快捷命令

#### 📊 `/diff-report` - 代码修改报告生成器

**功能**：自动对比当前分支与master分支的差异，生成详细的代码修改报告

**使用场景**：
- ✅ 提交代码前自查
- ✅ Code Review前准备
- ✅ 版本发布前评估

**生成的报告内容**：
- 变更文件统计（新增/修改/删除）
- 核心功能变更（新增功能、优化、Bug修复）
- 数据库变更分析
- 配置文件变更
- 依赖变更
- 代码质量和安全检查
- 影响分析和风险评估
- 部署说明和回滚方案

**使用方法**：
```bash
# 在Claude Code中输入
/diff-report
```

报告会保存到项目根目录的 `CHANGE_REPORT.md` 文件。

---

#### 🧪 `/generate-tests` - 单元测试生成器

**功能**：自动识别需要测试的代码，生成完整的单元测试代码

**使用场景**：
- ✅ 新增功能后快速生成测试
- ✅ Bug修复后补充测试用例
- ✅ 重构代码后验证功能

**生成的测试内容**：
- 测试类基础结构（Mock、BeforeEach）
- 正常场景测试（Happy Path）
- 异常场景测试（Exception Path）
- 边界条件测试（Boundary）
- 业务逻辑分支测试

**测试覆盖率要求**：
- 核心业务模块：>= 80%
- 普通业务模块：>= 70%
- 工具类：>= 90%

**使用方法**：
```bash
# 在Claude Code中输入
/generate-tests
```

会自动识别变更的Service、DubboApi类，生成对应的测试代码。

---

## 📖 完整案例

### 标准CRUD开发流程

**1. 创建Entity（在api模块）**
```java
package cn.city.parking.order.api.entity;

import cn.city.parking.common.core.web.domain.BusinessEntity;
import com.baomidou.mybatisplus.annotation.TableName;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Min;

@Data
@TableName("order_info")
public class Order extends BusinessEntity {

    @NotBlank(message = "订单号不能为空")
    private String orderNo;

    @NotBlank(message = "用户ID不能为空")
    private String userId;

    @NotNull(message = "订单金额不能为空")
    @Min(value = 0, message = "订单金额不能小于0")
    private BigDecimal amount;

    private Integer status;
}
```

**2. 创建DubboApiImpl（在server模块）**
```java
package cn.city.parking.order.dubbo;

import cn.city.parking.common.auth.base.BaseDubboApiImpl;
import cn.city.parking.common.core.utils.ValidateUtil;
import cn.city.parking.common.core.web.domain.ResponseResult;

@Slf4j
@DubboService
public class OrderDubboApiImpl extends BaseDubboApiImpl implements OrderDubboApi {

    @Autowired
    private IOrderService orderService;

    @Override
    public ResponseResult<Order> getInfo(String id) {
        // 简单参数用Preconditions
        Preconditions.checkArgument(StringUtils.isNotBlank(id), "订单ID不能为空");

        Order order = orderService.selectOrderById(id);
        return ResponseResult.success(order);
    }

    @Override
    public ResponseResult<Integer> add(Order order) {
        // 复杂对象用ValidateUtil（推荐）
        ValidateUtil.validate(order);

        log.info("创建订单，订单号：{}", order.getOrderNo());
        int rows = orderService.insertOrder(order);
        return ResponseResult.success(rows);
    }

    @Override
    public ResponseResult<PageInfo<Order>> pageList(Order order) {
        // 分页必须调用startDubboPage()
        startDubboPage();
        List<Order> list = orderService.selectOrderList(order);
        return ResponseResult.success(new PageInfo<>(list));
    }
}
```

**3. 创建Controller（BFF模块可选）**
```java
package cn.city.parking.bff.controller;

import cn.city.parking.common.core.utils.ValidateUtil;

@RestController
@RequestMapping("/order")
public class OrderController {

    @DubboReference
    private OrderDubboApi orderDubboApi;

    @PostMapping
    public ResponseResult<Integer> add(@RequestBody Order order) {
        // Controller中也可以使用ValidateUtil
        ValidateUtil.validate(order);
        return orderDubboApi.add(order);
    }
}
```

---

## 🚀 快速上手

### 步骤1：阅读文档
查看 `.claude/CLAUDE.md` 文件，重点关注：
- **第1节**：实体类规范（含参数校验注解）
- **第2节**：Controller/DubboApi规范（含两种校验方式）

### 步骤2：查看示例
查看 `.claude/docs/examples/standard-crud.md`，完整的CRUD示例代码

### 步骤3：使用快捷命令
```bash
# 创建新的CRUD功能
/new-crud

# 生成代码修改报告
/diff-report

# 生成单元测试
/generate-tests

# 代码审查清单
/review-code
```

---

## ❓ 常见问题

### Q1：ValidateUtil.validate()校验失败会怎样？
**A**：自动抛出`BusinessException`，全局异常处理器会捕获并返回友好的错误提示给前端，无需手动处理。

### Q2：是否所有字段都要加校验注解？
**A**：不是。参数校验不是强制要求，根据业务场景灵活选择。对于必填字段、有格式要求的字段，推荐添加注解。

### Q3：校验注解可以加在DTO上吗？
**A**：可以。校验注解可以加在Entity、DTO、VO等任何JavaBean对象上。因为框架不强制使用DTO/VO，所以可以直接在Entity上添加。

### Q4：修改了校验注解，需要重启服务吗？
**A**：是的，校验注解在启动时加载，修改后需要重启服务。

### Q5：DubboApi和Controller都需要校验吗？
**A**：
- **DubboApi**：推荐添加校验（服务提供方，数据入口）
- **Controller**：根据情况灵活选择（如果直接调用DubboApi，可以不重复校验）
- **最佳实践**：在数据入口处校验一次即可

### Q6：什么时候用Preconditions，什么时候用ValidateUtil？
**A**：
- **简单参数**（String id、int count等）：用`Preconditions`
- **复杂对象**（Entity、DTO、VO等）：用`ValidateUtil`
- **推荐**：优先使用ValidateUtil，更简洁、更规范

---

## 📝 checklist（新项目/新功能必查）

- [ ] Entity继承BusinessEntity，@TableName指定表名
- [ ] **可选：Entity/DTO字段添加校验注解**（@NotBlank、@Size等，如需使用，message必填）
- [ ] **可选：DubboApi/Controller中使用ValidateUtil.validate()校验**（推荐但非强制）
- [ ] Service方法添加@Transactional(rollbackFor = Exception.class)
- [ ] DubboApi继承BaseDubboApiImpl
- [ ] 分页查询调用startDubboPage()
- [ ] 返回值使用ResponseResult<T>带泛型
- [ ] 关键操作添加日志（log.info）

---

## 📚 相关文档

- **完整规范**：`.claude/CLAUDE.md`
- **标准案例**：`.claude/docs/examples/standard-crud.md`
- **快捷命令**：`.claude/commands/`目录
- **更新日志**：本文件

---

## 💬 反馈与建议

如有问题或建议，请联系架构组或在项目中提Issue。

---

**重要提醒**：
1. ⚠️ 所有新代码必须遵循本次更新的参数校验规范
2. ⚠️ 提交代码前使用 `/review-code` 进行自查
3. ⚠️ 提交前使用 `/diff-report` 生成修改报告

**祝开发顺利！** 🎉
