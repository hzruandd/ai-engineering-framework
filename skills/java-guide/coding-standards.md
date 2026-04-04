# 编码规范

本文档包含 City Parking 微服务框架的核心编码规范。

## 目录

1. [实体类规范](#1-实体类规范)
2. [DubboApi/Controller 实现规范](#2-dubboapicontroller-实现规范)
3. [Service 规范](#3-service-规范)
4. [Mapper 规范](#4-mapper-规范)
5. [启动类规范](#5-启动类规范)
6. [日志规范](#6-日志规范)
7. [核心类包路径](#7-核心类包路径)
8. [Redis 使用规范](#8-redis-使用规范)
9. [代码风格规范](#9-代码风格规范)
10. [SOLID 设计原则](#10-solid-设计原则)

---

## 1. 实体类规范

### BusinessEntity 基类说明

⚠️ **BusinessEntity 只包含 3 个字段**：
- `id`（主键，雪花ID）
- `createTime`（创建时间）
- `updateTime`（更新时间）

### 可选字段显式声明

⚠️ **如果数据库有以下字段，必须在实体类中显式声明**：
- `create_by` → 必须声明 `createBy` 字段
- `update_by` → 必须声明 `updateBy` 字段
- `del_flag` → 必须声明 `delFlag` 字段
- `revision` → 必须声明 `revision` 字段（乐观锁）

### 完整示例

```java
import cn.city.parking.common.core.web.domain.BusinessEntity;
import com.baomidou.mybatisplus.annotation.*;
import com.fasterxml.jackson.annotation.JsonFormat;
import io.swagger.v3.oas.annotations.media.Schema;
import javax.validation.constraints.*;
import lombok.Data;
import lombok.EqualsAndHashCode;
import java.time.LocalDateTime;

@Data
@EqualsAndHashCode(callSuper = true)
@TableName("sys_user")  // ✅ 必须指定表名
@Schema(description = "用户实体")
public class User extends BusinessEntity {

    @Schema(description = "用户名")
    @NotBlank(message = "用户名不能为空")
    @Size(min = 1, max = 30, message = "用户名长度必须在1-30个字符之间")
    private String username;

    @Schema(description = "邮箱")
    @Email(message = "邮箱格式不正确")
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

### 参数校验注解说明

- `@NotBlank`：字符串不能为空
- `@NotNull`：值不能为null
- `@Size`：字符串/集合/数组长度限制
- `@Email`：邮箱格式校验
- `@Min`/`@Max`：数值范围校验
- `@Pattern`：正则表达式校验

---

## 2. DubboApi/Controller 实现规范

### 职责边界（架构核心原则）

⚠️ **DubboApi/Controller 只是薄薄的接口层**

✅ **只负责 4 件事**：
1. 参数校验
2. 调用 Service
3. 记录日志
4. 返回结果

❌ **绝对不允许**：
- 复杂的业务判断和计算
- 查询条件构建（LambdaQueryWrapper等）
- 直接调用 Mapper
- 循环处理数据
- 事务控制

### 正确示例

```java
import cn.city.parking.common.dubbo.filter.base.BaseDubboApi;
import cn.city.parking.common.core.web.domain.ResponseResult;
import com.google.common.base.Preconditions;
import org.apache.dubbo.config.annotation.DubboService;
import com.github.pagehelper.PageInfo;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@DubboService
public class UserDubboApiImpl extends BaseDubboApi implements UserDubboApi {

    @Autowired
    private IUserService userService;

    @Override
    public ResponseResult<User> getInfo(String id) {
        // 1. 参数校验
        Preconditions.checkArgument(StringUtils.isNotBlank(id), "用户ID不能为空");
        // 2. 调用Service
        User user = userService.selectUserById(id);
        // 3. 返回结果
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
        Preconditions.checkNotNull(user, "用户信息不能为空");
        log.info("创建用户，用户名：{}", user.getUsername());
        int rows = userService.insertUser(user);
        return ResponseResult.success(rows);
    }
}
```

### 参数校验方式

#### 方式1：Preconditions（简单参数）

```java
import com.google.common.base.Preconditions;

Preconditions.checkArgument(StringUtils.isNotBlank(id), "用户ID不能为空");
Preconditions.checkNotNull(user, "用户对象不能为空");
```

#### 方式2：ValidateUtil（复杂对象，推荐）

```java
import cn.city.parking.common.core.utils.ValidateUtil;

ValidateUtil.validate(user);  // 自动校验所有注解
```

### 关键规范

- ✅ DubboApi 继承 `cn.city.parking.common.dubbo.filter.base.BaseDubboApi`
- ✅ 返回值必须用 `ResponseResult<T>` 带泛型
- ✅ 分页查询必须调用 `startDubboPage()`
- ✅ 保持薄层，所有业务逻辑放在 Service 层
- ❌ 不要随意捕获异常
- ❌ 永远不要捕获 BusinessException

---

## 3. Service 规范

### Service 接口

```java
import com.baomidou.mybatisplus.extension.service.IService;

// ✅ 继承 IService<T>
public interface IUserService extends IService<User> {
    User selectUserById(String id);
    List<User> selectUserList(User user);
    int insertUser(User user);
    int updateUser(User user);
    int deleteUserById(String id);
}
```

### Service 实现

```java
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, User>
    implements IUserService {

    @Override
    @Transactional(rollbackFor = Exception.class)  // ✅ 增删改必须加事务
    public int insertUser(User user) {
        return baseMapper.insert(user);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public int updateUser(User user) {
        return baseMapper.updateById(user);
    }
}
```

---

## 4. Mapper 规范

```java
import com.baomidou.mybatisplus.core.mapper.BaseMapper;

// ✅ 不需要 @Mapper 注解（common-server 已自动扫描）
public interface UserMapper extends BaseMapper<User> {
    User selectByUsername(@Param("username") String username);
}

// ✅ 框架已自动注入批量方法
userMapper.insertBatchSomeColumn(userList);
```

---

## 5. 启动类规范

```java
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@Slf4j
@SpringBootApplication  // ✅ 只需2个基础注解
public class CityParkingXxxApplication {
    public static void main(String[] args) {
        SpringApplication.run(CityParkingXxxApplication.class, args);
    }
}
```

❌ **不需要添加**：`@EnableDubbo`、`@EnableAsync`、`@MapperScan`（已自动配置）

✅ **按需添加**：`@EnableCaching`、`@EnableScheduling`

---

## 6. 日志规范

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

### 日志级别

- **INFO**：关键业务节点（CUD操作）
- **WARN**：可恢复异常、降级处理
- **ERROR**：系统错误、需要告警

### 必须记录

- CUD操作
- 外部接口调用
- 异常捕获
- 关键分支判断

### 敏感信息脱敏

密码、身份证、手机号、银行卡

---

## 7. 核心类包路径

```java
// ✅ 正确路径
import cn.city.parking.common.dubbo.filter.base.BaseDubboApi;
import cn.city.parking.common.core.web.domain.BusinessEntity;
import cn.city.parking.common.core.web.domain.ResponseResult;
import com.github.pagehelper.PageInfo;
import cn.city.parking.common.redis.RedisUtils;

// ❌ 错误路径（已废弃）
import cn.city.parking.common.auth.base.BaseDubboApi;
```

---

## 8. Redis 使用规范

### 核心原则

❌ **不要随意使用Redis缓存**（如无必要，不要缓存）

### 何时使用缓存（必须同时满足）

- ✅ 查询频率 > 100次/分钟
- ✅ 数据变更频率 < 10次/天
- ✅ 数据量 < 1MB
- ✅ 可容忍短暂不一致

### 基础操作

```java
// 存入缓存（3600秒）
RedisUtils.setCacheObject("user:info:" + id, user, 3600);

// 获取缓存
User user = RedisUtils.getCacheObject("user:info:" + id, User.class);

// 删除缓存
RedisUtils.deleteObject("user:info:" + id);
```

### 分布式锁

```java
@Autowired
private Locker locker;

locker.lock(lockKey, 10, () -> {
    // 业务逻辑，10秒后自动释放
});
```

---

## 9. 代码风格规范

### 核心原则

新代码必须遵循 **Spring Java Format** 规范

### 提交前必做

```bash
mvn spring-javaformat:apply    # 格式化代码
mvn spring-javaformat:validate # 检查格式
```

### IDEA 插件

Settings → Plugins → 搜索 `Spring Java Format`

---

## 10. SOLID 设计原则

| 原则 | 定义 | 框架应用 |
|------|------|----------|
| **S** - 单一职责 | 一个类只负责一件事 | DubboApi、Service、Mapper 各司其职 |
| **O** - 开闭原则 | 对扩展开放，对修改关闭 | 使用策略模式、工厂模式 |
| **L** - 里氏替换 | 子类可替换父类 | 子类增强父类行为 |
| **I** - 接口隔离 | 使用多个专门接口 | 拆分查询和命令接口 |
| **D** - 依赖倒置 | 依赖抽象不依赖实现 | @Autowired 注入接口 |

### 实践要点

- ✅ 每个类设计前先问：它的单一职责是什么？
- ✅ 新增功能优先扩展而非修改
- ✅ 面向接口编程
- ❌ 避免"上帝类"（超过500行、职责超过3个）

---

**文档版本**：1.0
**最后更新**：2026-01-24
