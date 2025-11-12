# 案例1：用户管理模块（标准CRUD）

**场景**：实现用户基本信息的增删改查

## 完整代码

### 1. 实体类（User.java）

```java
package cn.city.parking.user.api.entity;

import cn.city.parking.common.core.web.domain.BusinessEntity;
import com.baomidou.mybatisplus.annotation.TableName;
import com.fasterxml.jackson.annotation.JsonFormat;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import lombok.EqualsAndHashCode;

import javax.validation.constraints.Email;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;
import javax.validation.constraints.Size;
import java.time.LocalDateTime;

@Data
@EqualsAndHashCode(callSuper = true)
@TableName("sys_user")
@Schema(description = "用户实体")
public class User extends BusinessEntity {

    @Schema(description = "用户名")
    @NotBlank(message = "用户名不能为空")
    @Size(min = 2, max = 30, message = "用户名长度必须在2-30个字符之间")
    private String username;

    @Schema(description = "手机号")
    @Pattern(regexp = "^1[3-9]\\d{9}$", message = "手机号格式不正确")
    private String phone;

    @Schema(description = "邮箱")
    @Email(message = "邮箱格式不正确")
    @Size(max = 50, message = "邮箱长度不能超过50个字符")
    private String email;

    @Schema(description = "状态：0-禁用 1-启用")
    private Integer status;

    @Schema(description = "最后登录时间")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime lastLoginTime;
}
```

### 2. DubboApi接口（UserDubboApi.java）

```java
package cn.city.parking.user.api;

import cn.city.parking.common.core.web.domain.ResponseResult;
import cn.city.parking.user.api.entity.User;
import com.github.pagehelper.PageInfo;

import java.util.List;

public interface UserDubboApi {

    ResponseResult<PageInfo<User>> pageList(User user);

    ResponseResult<List<User>> allList(User user);

    ResponseResult<User> getInfo(String id);

    ResponseResult<Integer> add(User user);

    ResponseResult<Integer> edit(User user);

    ResponseResult<Integer> remove(String[] ids);
}
```

### 3. Service接口（IUserService.java）

```java
package cn.city.parking.user.service;

import cn.city.parking.user.api.entity.User;
import com.baomidou.mybatisplus.extension.service.IService;

import java.util.List;

public interface IUserService extends IService<User> {

    User selectUserById(String id);

    List<User> selectUserList(User user);

    int insertUser(User user);

    int updateUser(User user);

    int deleteUserById(String id);

    int deleteUserByIds(String[] ids);
}
```

### 4. Service实现（UserServiceImpl.java）

```java
package cn.city.parking.user.service.impl;

import cn.city.parking.user.api.entity.User;
import cn.city.parking.user.mapper.UserMapper;
import cn.city.parking.user.service.IUserService;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.apache.commons.lang3.StringUtils;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Arrays;
import java.util.List;

@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements IUserService {

    @Override
    public User selectUserById(String id) {
        return baseMapper.selectById(id);
    }

    @Override
    public List<User> selectUserList(User user) {
        LambdaQueryWrapper<User> wrapper = new LambdaQueryWrapper<>();

        if (StringUtils.isNotBlank(user.getUsername())) {
            wrapper.like(User::getUsername, user.getUsername());
        }
        if (StringUtils.isNotBlank(user.getPhone())) {
            wrapper.eq(User::getPhone, user.getPhone());
        }
        if (user.getStatus() != null) {
            wrapper.eq(User::getStatus, user.getStatus());
        }

        wrapper.orderByDesc(User::getCreateTime);
        return baseMapper.selectList(wrapper);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public int insertUser(User user) {
        return baseMapper.insert(user);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public int updateUser(User user) {
        return baseMapper.updateById(user);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public int deleteUserById(String id) {
        return baseMapper.deleteById(id);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public int deleteUserByIds(String[] ids) {
        return baseMapper.deleteBatchIds(Arrays.asList(ids));
    }
}
```

### 5. DubboApi实现（UserDubboApiImpl.java）

```java
package cn.city.parking.user.dubbo;

import cn.city.parking.common.auth.base.BaseDubboApiImpl;
import cn.city.parking.common.core.utils.ValidateUtil;
import cn.city.parking.common.core.web.domain.ResponseResult;
import cn.city.parking.user.api.UserDubboApi;
import cn.city.parking.user.api.entity.User;
import cn.city.parking.user.service.IUserService;
import com.github.pagehelper.PageInfo;
import com.google.common.base.Preconditions;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.apache.dubbo.config.annotation.DubboService;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;

@Slf4j
@DubboService
public class UserDubboApiImpl extends BaseDubboApiImpl implements UserDubboApi {

    @Autowired
    private IUserService userService;

    @Override
    public ResponseResult<PageInfo<User>> pageList(User user) {
        startDubboPage();
        List<User> list = userService.selectUserList(user);
        return ResponseResult.success(new PageInfo<>(list));
    }

    @Override
    public ResponseResult<List<User>> allList(User user) {
        List<User> list = userService.selectUserList(user);
        return ResponseResult.success(list);
    }

    @Override
    public ResponseResult<User> getInfo(String id) {
        // 简单参数使用Preconditions校验
        Preconditions.checkArgument(StringUtils.isNotBlank(id), "用户ID不能为空");
        User user = userService.selectUserById(id);
        return ResponseResult.success(user);
    }

    @Override
    public ResponseResult<Integer> add(User user) {
        // 复杂对象使用ValidateUtil.validate()校验
        // 自动校验@NotBlank、@Size、@Email等注解
        ValidateUtil.validate(user);

        log.info("创建用户，用户名：{}", user.getUsername());
        int rows = userService.insertUser(user);
        log.info("用户创建成功，用户ID：{}", user.getId());
        return ResponseResult.success(rows);
    }

    @Override
    public ResponseResult<Integer> edit(User user) {
        // 复杂对象使用ValidateUtil.validate()校验
        ValidateUtil.validate(user);
        // ID单独校验（因为ID在基类中，没有@NotBlank注解）
        Preconditions.checkArgument(StringUtils.isNotBlank(user.getId()), "用户ID不能为空");

        log.info("修改用户，用户ID：{}", user.getId());
        int rows = userService.updateUser(user);
        log.info("用户修改成功，影响行数：{}", rows);
        return ResponseResult.success(rows);
    }

    @Override
    public ResponseResult<Integer> remove(String[] ids) {
        // 简单参数使用Preconditions校验
        Preconditions.checkNotNull(ids, "用户ID不能为空");
        Preconditions.checkArgument(ids.length > 0, "至少选择一条数据");

        log.info("删除用户，数量：{}", ids.length);
        int rows = userService.deleteUserByIds(ids);
        log.info("用户删除成功，影响行数：{}", rows);
        return ResponseResult.success(rows);
    }
}
```

## 关键点说明

- ✅ **实体类继承 BusinessEntity**，使用 @TableName 指定表名
- ✅ **参数校验注解**（可选）：可在Entity、DTO、VO等对象字段上添加`@NotBlank`、`@Size`、`@Email`、`@Pattern`等注解
- ✅ **两种参数校验方式**（推荐但非强制）：
  - 简单参数（String、int等）：使用`Preconditions.checkArgument()`
  - 复杂对象（Entity、DTO等）：使用`ValidateUtil.validate()`
- ✅ **DubboApi 返回值**：使用 ResponseResult<T> 带泛型
- ✅ **Service 继承**：接口继承 IService<T>，实现类继承 ServiceImpl
- ✅ **事务管理**：增删改方法必须添加 @Transactional(rollbackFor = Exception.class)
- ✅ **DubboApi 实现**：继承 BaseDubboApiImpl
- ✅ **分页查询**：调用 startDubboPage()
- ✅ **日志记录**：关键操作添加日志记录

## 参数校验最佳实践（可选）

**说明**：参数校验不是强制要求，根据业务场景灵活选择。以下是推荐做法。

**1. 在Entity/DTO中定义校验规则**：
```java
// 可以加在Entity上（框架不强制使用DTO/VO，所以可以直接在Entity上加）
@NotBlank(message = "用户名不能为空")  // 不能为null、空字符串、空格
@Size(min = 2, max = 30, message = "用户名长度必须在2-30个字符之间")
private String username;

@Pattern(regexp = "^1[3-9]\\d{9}$", message = "手机号格式不正确")  // 正则校验
private String phone;

@Email(message = "邮箱格式不正确")  // 邮箱格式
private String email;

// 也可以加在DTO上（如果使用了DTO）
public class UserCreateDTO {
    @NotBlank(message = "用户名不能为空")
    private String username;
    // ...
}
```

**2. 在DubboApi/Controller中调用校验**：
```java
// 方式1：简单参数
Preconditions.checkArgument(StringUtils.isNotBlank(id), "用户ID不能为空");

// 方式2：复杂对象（推荐）
ValidateUtil.validate(user);  // 自动校验所有带注解的字段
```

**3. ValidateUtil的优势**：
- 自动读取对象中的所有校验注解（Entity、DTO、VO都可以）
- 校验失败自动抛出BusinessException，无需手动处理
- 错误信息自动拼接，用户体验好
- 代码简洁，只需一行代码

**4. 灵活使用原则**：
- **DubboApi层**（服务提供方）：推荐添加参数校验，保证数据入口安全
- **Controller层**（BFF层）：根据情况选择，如果直接调用DubboApi，可以不重复校验
- **内部方法**：不需要校验，由调用方保证参数合法性
