# 开发流程

本文档包含新建微服务项目和 CRUD 功能的完整步骤。

## 目录

1. [新建微服务项目](#1-新建微服务项目)
2. [新建 CRUD 功能](#2-新建-crud-功能)
3. [标准方法命名](#3-标准方法命名)
4. [验证清单](#4-验证清单)

---

## 1. 新建微服务项目

### 步骤 1：创建根 POM

创建 `city-parking-xxx/pom.xml`：

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

### 步骤 2：创建 API 模块

⚠️ **parent 直接继承 city-parking-parent**（不继承根pom）

创建 `city-parking-xxx-api/pom.xml`：

```xml
<parent>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-parent</artifactId>
    <version>2.0.0-SNAPSHOT</version>
    <relativePath/>
</parent>
<artifactId>city-parking-xxx-api</artifactId>
<dependencies>
    <!-- ✅ API模块必须依赖city-parking-common-auth -->
    <dependency>
        <groupId>cn.city-parking</groupId>
        <artifactId>city-parking-common-auth</artifactId>
    </dependency>
</dependencies>
```

创建包结构：
- `cn.city.parking.xxx.api.entity`（⚠️ 必须在 api 包下）
- `cn.city.parking.xxx.api`（DubboApi 接口）
- `cn.city.parking.xxx.api.dto`（可选）

创建 Entity：
```java
@Data
@EqualsAndHashCode(callSuper = true)
@TableName("sys_user")
@Schema(description = "用户实体")
public class User extends BusinessEntity {
    @Schema(description = "用户名")
    @NotBlank(message = "用户名不能为空")
    private String username;

    @Schema(description = "邮箱")
    @Email(message = "邮箱格式不正确")
    private String email;
}
```

创建 DubboApi 接口：
```java
public interface UserDubboApi {
    ResponseResult<PageInfo<User>> pageList(User user);
    ResponseResult<List<User>> allList(User user);
    ResponseResult<User> getInfo(String id);
    ResponseResult<Integer> add(User user);
    ResponseResult<Integer> edit(User user);
    ResponseResult<Integer> remove(String id);
}
```

### 步骤 3：创建 Server 模块

⚠️ **parent 直接继承 city-parking-parent**（不继承根pom）

创建 `city-parking-xxx-server/pom.xml`：

```xml
<parent>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-parent</artifactId>
    <version>2.0.0-SNAPSHOT</version>
    <relativePath/>
</parent>
<artifactId>city-parking-xxx-server</artifactId>
<dependencies>
    <!-- ✅ 1. common-server -->
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
</dependencies>
<build>
    <plugins>
        <!-- ✅ Spring Boot打包插件 -->
        <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
            <configuration>
                <mainClass>cn.city.parking.xxx.CityParkingXxxApplication</mainClass>
            </configuration>
        </plugin>
        <!-- ✅ 禁止Server模块发布 -->
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

创建配置文件（⚠️ 必须创建 4 个文件）：
- `bootstrap.yml`：主配置，使用 `@profileActive@` + `${nacos.server-addr}`
- `bootstrap-dev.yml`：开发环境，使用 `@serverAddr@` 占位符
- `bootstrap-prod.yml`：生产环境，直接配置地址
- `bootstrap-test.yml`：测试环境，直接配置地址

创建启动类：
```java
@Slf4j
@SpringBootApplication
public class CityParkingXxxApplication {
    public static void main(String[] args) {
        SpringApplication.run(CityParkingXxxApplication.class, args);
    }
}
```

创建 Mapper、Service、DubboApi 实现：
- `cn.city.parking.xxx.mapper.UserMapper`
- `cn.city.parking.xxx.service.IUserService`
- `cn.city.parking.xxx.service.impl.UserServiceImpl`
- `cn.city.parking.xxx.dubbo.UserDubboApiImpl`

---

## 2. 新建 CRUD 功能

### 步骤 1：API 模块创建 Entity

在 `city-parking-xxx-api` 模块中：

```java
package cn.city.parking.xxx.api.entity;  // ⚠️ 必须在 api.entity 包下

@Data
@EqualsAndHashCode(callSuper = true)
@TableName("sys_user")
@Schema(description = "用户实体")
public class User extends BusinessEntity {
    @Schema(description = "用户名")
    @NotBlank(message = "用户名不能为空")
    private String username;

    // 如果数据库有 create_by 字段，必须显式声明
    @TableField(value = "create_by", fill = FieldFill.INSERT)
    private String createBy;
}
```

### 步骤 2：API 模块创建 DubboApi 接口

```java
package cn.city.parking.xxx.api;

public interface UserDubboApi {
    ResponseResult<PageInfo<User>> pageList(User user);
    ResponseResult<List<User>> allList(User user);
    ResponseResult<User> getInfo(String id);
    ResponseResult<Integer> add(User user);
    ResponseResult<Integer> edit(User user);
    ResponseResult<Integer> remove(String id);
}
```

### 步骤 3：Server 模块创建 Mapper

```java
package cn.city.parking.xxx.mapper;

// ✅ 不需要 @Mapper 注解
public interface UserMapper extends CommonMapper<User> {
    // 自定义方法
    User selectByUsername(@Param("username") String username);
}
```

### 步骤 4：Server 模块创建 Service

Service 接口：
```java
package cn.city.parking.xxx.service;

public interface IUserService extends IService<User> {
    User selectUserById(String id);
    List<User> selectUserList(User user);
    int insertUser(User user);
    int updateUser(User user);
    int deleteUserById(String id);
}
```

Service 实现：
```java
package cn.city.parking.xxx.service.impl;

@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, User>
    implements IUserService {

    @Override
    @Transactional(rollbackFor = Exception.class)
    public int insertUser(User user) {
        return baseMapper.insert(user);
    }
}
```

### 步骤 5：Server 模块创建 DubboApi 实现

```java
package cn.city.parking.xxx.dubbo;

@Slf4j
@DubboService
public class UserDubboApiImpl extends BaseDubboApi implements UserDubboApi {

    @Autowired
    private IUserService userService;

    @Override
    public ResponseResult<PageInfo<User>> pageList(User user) {
        startDubboPage();  // ✅ 分页查询必须调用
        List<User> list = userService.selectUserList(user);
        return ResponseResult.success(new PageInfo<>(list));
    }

    @Override
    public ResponseResult<User> getInfo(String id) {
        Preconditions.checkArgument(StringUtils.isNotBlank(id), "用户ID不能为空");
        User user = userService.selectUserById(id);
        return ResponseResult.success(user);
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

---

## 3. 标准方法命名

### DubboApi 方法命名

- `pageList`：分页查询
- `allList`：全量查询
- `getInfo`：根据ID查询
- `add`：新增
- `edit`：修改
- `remove`：删除

### Service 方法命名

- `select{ClassName}ById`：根据ID查询
- `select{ClassName}List`：查询列表
- `insert{ClassName}`：新增
- `update{ClassName}`：修改
- `delete{ClassName}ById`：根据ID删除
- `delete{ClassName}ByIds`：批量删除

示例：
- `selectUserById`
- `selectUserList`
- `insertUser`
- `updateUser`
- `deleteUserById`

---

## 4. 验证清单

### 项目结构验证

- [ ] ⚠️ **API 和 Server 模块的 parent 都是 city-parking-parent**（不是根pom）
- [ ] Entity 在 `xxx.api.entity` 包下（不是 `xxx.entity`）
- [ ] 如果数据库有 create_by、update_by、del_flag 字段，实体类中已显式声明
- [ ] API 模块依赖是 `common-auth`（不是 `common-core`）
- [ ] Server 模块只依赖 `common-server` 和本服务 API（没有冗余依赖）

### 配置文件验证

- [ ] 创建了 4 个配置文件：bootstrap.yml + bootstrap-dev/prod/test.yml
- [ ] bootstrap.yml 使用 `@profileActive@`（不是 `${profiles.active:dev}`）
- [ ] bootstrap.yml 占位符是 `${nacos.*}`（不是 `${custom-config...}`）
- [ ] Server 模块配置了 mainClass 和 deploy skip
- [ ] 根 pom 配置了 deploy skip（禁止发布到Maven私库）

### 代码规范验证

- [ ] Entity 继承 BusinessEntity + @TableName + @JsonFormat
- [ ] Service 接口继承 IService<T>
- [ ] Service 实现继承 ServiceImpl + @Transactional
- [ ] DubboApi 继承 BaseDubboApi + ResponseResult<T> + startDubboPage()
- [ ] Mapper 继承 CommonMapper（不需要 @Mapper 注解）
- [ ] 启动类只有 @Slf4j + @SpringBootApplication

### 功能验证

- [ ] 编译通过：`mvn clean compile`
- [ ] 打包成功：`mvn clean package`
- [ ] 启动成功：运行启动类
- [ ] 接口可用：测试 DubboApi 接口

---

**文档版本**：1.0
**最后更新**：2026-01-24
