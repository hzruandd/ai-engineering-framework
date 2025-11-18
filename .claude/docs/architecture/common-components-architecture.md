# City Parking 2.0 Common组件架构文档

**文档版本**: 1.0.0
**创建日期**: 2025-11-17
**维护团队**: 技术架构组
**适用范围**: City Parking 2.0微服务架构

---

## 📋 文档目的

本文档详细描述City Parking 2.0微服务架构中所有Common组件的功能、依赖关系、自动装配机制和使用方式。

**主要用途**：
1. **AI编码助手参考**：在生成代码时快速查找组件功能和使用方法
2. **开发人员参考**：理解Common组件体系架构
3. **架构决策依据**：选择合适的组件解决业务问题

---

## 🏗️ Common组件总体架构

### 组件分类

City Parking 2.0共有**29个Common组件**，按功能分为以下7大类：

```
city-parking-common (29个组件)
├── 基础核心层 (3个)
│   ├── common-core         # 核心工具类和基础功能
│   ├── common-config       # 统一配置和日志收集
│   └── common-concurrent   # 并发工具（Guava、Disruptor）
│
├── 服务集成层 (5个)
│   ├── common-server       # 微服务基础设施（MyBatis Plus + Undertow）
│   ├── common-service      # 微服务基础设施（纯MyBatis版本）
│   ├── common-bff          # BFF聚合层基础设施（Undertow + Dubbo客户端）
│   ├── common-dubbo        # Dubbo RPC增强
│   └── common-auth         # Sa-Token认证授权
│
├── 数据层 (5个)
│   ├── common-redis        # Redis + Redisson
│   ├── common-datasource   # 动态数据源
│   ├── common-datascope    # 数据权限控制
│   ├── common-tenant       # 多租户
│   └── common-seata        # 分布式事务
│
├── 网关/网络层 (3个)
│   ├── common-gateway      # Spring Cloud Gateway网关
│   ├── common-webflux      # WebFlux响应式编程
│   └── common-websocket    # WebSocket长连接
│
├── 第三方集成层 (5个)
│   ├── common-wxmp         # 微信公众号
│   ├── common-wxmp-dubboapi# 微信公众号Dubbo API
│   ├── common-opensdk      # 阿里云/支付宝/极光推送SDK
│   ├── common-mq           # RocketMQ消息队列
│   └── common-mqtt         # MQTT物联网协议
│
├── 工具类层 (6个)
│   ├── common-log          # 操作日志记录
│   ├── common-job          # XXL-Job定时任务
│   ├── common-message      # 阿里云语音消息
│   ├── common-swagger      # Knife4j接口文档
│   ├── common-sensitive    # 数据脱敏
│   └── common-device       # 设备信息工具
│
└── 监控层 (2个)
    ├── common-monitor      # Prometheus监控指标
    └── common-oauth2       # OAuth2.0协议
```

### 自动装配统计

- **有spring.factories的组件**: 24个
- **无spring.factories的组件**: 5个（datasource, device, monitor, tenant, wxmp-dubboapi）

---

## 🔧 组件详细说明

### 一、基础核心层

#### 1.1 common-core（核心模块）

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-core</artifactId>
</dependency>
```

**功能描述**：
- 核心工具类和基础功能
- 提供通用的实体类、异常类、工具类
- 包含Jackson、Fastjson、Hutool、Guava等常用工具

**核心依赖**：
- sa-token-core（权限认证核心）
- pinyin4j（汉字转拼音）
- pagehelper（分页）
- jackson-databind、fastjson（JSON处理）
- commons-lang3、commons-io（Apache工具类）
- poi-ooxml（Excel处理）
- thumbnailator（图片处理）
- transmittable-thread-local（TTL线程变量传递）
- hutool-all（Hutool工具集）
- guava（Google工具集）
- reactor-core（响应式编程）

**自动装配类**：
```java
cn.city.parking.common.core.utils.SpringUtils
cn.city.parking.common.core.utils.SpringContextUtil
```

**核心功能**：
1. 基础实体类：`BusinessEntity`（id、createTime、updateTime）
2. 响应结果封装：`ResponseResult<T>`
3. 通用工具类：字符串、日期、文件、集合等
4. Spring上下文工具：`SpringUtils`、`SpringContextUtil`

**使用示例**：
```java
// 1. 实体类继承
@Data
@EqualsAndHashCode(callSuper = true)
@TableName("sys_user")
public class User extends BusinessEntity {
    private String username;
    private String email;
}

// 2. 响应结果封装
public ResponseResult<User> getUser(String id) {
    User user = userService.selectById(id);
    return ResponseResult.success(user);
}

// 3. Spring上下文获取Bean
UserService userService = SpringUtils.getBean(UserService.class);
```

---

#### 1.2 common-config（统一配置）

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-config</artifactId>
</dependency>
```

**功能描述**：
- 统一的配置管理
- 日志收集（ELK + SkyWalking）
- MDC链路追踪

**核心依赖**：
- logback-mdc-ttl（MDC + TTL）
- logback-gelf（GELF日志格式，用于ELK）
- apm-toolkit-trace（SkyWalking链路追踪API）
- apm-toolkit-logback-1.x（SkyWalking日志集成）
- city-parking-common-monitor（Prometheus监控）

**自动装配类**：
```java
cn.city.parking.common.config.CommonAutoConfig
```

**核心功能**：
1. **日志收集到ELK**：通过logback-gelf自动发送日志到Elasticsearch
2. **SkyWalking链路追踪**：自动关联请求链路
3. **MDC传递**：异步线程自动传递traceId

**配置示例**：
```yaml
# application.yml
logging:
  level:
    cn.city.parking: DEBUG
```

---

#### 1.3 common-concurrent（并发工具）

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-concurrent</artifactId>
</dependency>
```

**功能描述**：
- 并发工具增强
- Disruptor高性能队列

**核心依赖**：
- guava（Google并发工具）
- disruptor（LMAX高性能队列）

**自动装配类**：
```java
cn.city.parking.common.concurrent.config.ConcurrentAutoConfig
```

**使用场景**：
- 高并发场景下的异步处理
- 事件驱动架构

---

### 二、服务集成层

#### 2.1 common-server（微服务基础设施 - MyBatis Plus版）⭐

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-server</artifactId>
</dependency>
```

**功能描述**：
- **微服务基础设施核心组件**
- 集成MyBatis Plus、Undertow、Dubbo、Nacos、Sentinel
- 提供自动配置、线程池、字段填充等功能

**核心依赖**：
- kryo、kryo-serializers（高性能序列化）
- mybatis-plus-boot-starter（MyBatis Plus）
- spring-boot-starter-undertow（Undertow容器）
- mysql-connector-j（MySQL驱动）
- dubbo-spring-boot-starter（Dubbo RPC）
- spring-cloud-starter-alibaba-nacos-discovery（Nacos服务发现）
- spring-cloud-starter-alibaba-nacos-config（Nacos配置中心）
- pagehelper-spring-boot-starter（分页）
- spring-cloud-starter-alibaba-sentinel（Sentinel限流熔断）
- sentinel-datasource-nacos（Sentinel规则存储到Nacos）
- city-parking-common-redis（Redis）
- city-parking-common-datasource（动态数据源）
- knife4j-openapi3-spring-boot-starter（接口文档）
- spring-boot-admin-starter-client（Spring Boot Admin监控）
- city-parking-common-auth（认证授权）
- city-parking-common-tenant（多租户）
- city-parking-common-config（统一配置）

**自动装配类**：
```java
cn.city.parking.common.server.ServerStarterConfig        // 启动配置（@EnableDubbo、@MapperScan等）
cn.city.parking.common.server.MyMetaObjectHandler        // 字段自动填充（createTime、updateTime等）
cn.city.parking.common.server.endpoint.MyThreadPollEndpoint  // 线程池监控端点
cn.city.parking.common.server.ExecutePoolConfiguration   // 线程池配置（3个线程池）
```

**核心功能**：

1. **自动配置注解**（无需在启动类添加）：
   - `@EnableDubbo`
   - `@MapperScan("cn.city.parking.**.mapper")`
   - `@ComponentScan("cn.city.parking.**")`

2. **3个线程池**：
   - `myThreadPoolTaskExecutor`：普通异步任务
   - `ttlExecutorService`：需要链路追踪（自动传递MDC）
   - `userTaskThreadPool`：需要登录信息（传递SaToken上下文）

3. **字段自动填充**：
   - `createTime`、`updateTime`
   - `createBy`、`updateBy`（需要在Entity中显式声明）
   - `delFlag`（需要在Entity中显式声明）
   - `id`（雪花ID）

4. **批量插入增强**：
   - `insertBatchSomeColumn()`：批量插入，排除UPDATE字段

**使用示例**：
```java
// 1. 启动类（只需2个注解）
@Slf4j
@SpringBootApplication
public class CityParkingXxxApplication {
    public static void main(String[] args) {
        SpringApplication.run(CityParkingXxxApplication.class, args);
    }
}

// 2. 异步任务（自动传递MDC）
@Async  // 默认使用ttlExecutorService
public void asyncTask() {
    log.info("TraceId自动传递：{}", MDC.get("traceId"));
}

// 3. 批量插入
List<User> users = ...;
userMapper.insertBatchSomeColumn(users);  // 自动排除updateTime等UPDATE字段
```

**POM配置示例**（Server模块）：
```xml
<dependencies>
    <!-- 只需添加common-server，已包含所有必要依赖 -->
    <dependency>
        <groupId>cn.city-parking</groupId>
        <artifactId>city-parking-common-server</artifactId>
    </dependency>

    <!-- 本服务API模块 -->
    <dependency>
        <groupId>cn.city-parking</groupId>
        <artifactId>city-parking-xxx-api</artifactId>
        <version>2.0.0-SNAPSHOT</version>
    </dependency>
</dependencies>
```

---

#### 2.2 common-service（微服务基础设施 - 纯MyBatis版）

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-service</artifactId>
</dependency>
```

**功能描述**：
- 与common-server类似，但使用**纯MyBatis**（不是MyBatis Plus）
- 适用于不需要MyBatis Plus增强功能的场景

**核心依赖**：
- mybatis-spring-boot-starter（纯MyBatis）
- 其他依赖与common-server类似

**自动装配类**：
```java
cn.city.parking.common.service.ServerStarterConfig
cn.city.parking.common.service.endpoint.MyThreadPollEndpoint
cn.city.parking.common.service.ExecutePoolConfiguration
```

**与common-server的区别**：
- common-server：使用MyBatis Plus，有`BaseMapper`、`IService`等增强
- common-service：使用纯MyBatis，需要手写XML

**选择建议**：
- ✅ 推荐使用**common-server**（MyBatis Plus功能更强大）
- ⚠️ 只在必须使用纯MyBatis时选择common-service

---

#### 2.3 common-bff（BFF聚合层基础设施）⭐

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-bff</artifactId>
</dependency>
```

**功能描述**：
- **BFF（Backend For Frontend）聚合层基础设施**
- 提供Undertow容器 + Dubbo客户端
- 用于PC端、APP端、H5端的BFF服务

**核心依赖**：
- spring-boot-starter-undertow（高性能Web容器）
- dubbo-spring-boot-starter（Dubbo客户端）
- spring-cloud-starter-alibaba-nacos-discovery（服务发现）
- spring-cloud-starter-alibaba-nacos-config（配置中心）
- spring-cloud-starter-alibaba-sentinel（限流熔断）
- sentinel-datasource-nacos（规则存储）
- city-parking-common-redis（Redis）
- city-parking-common-swagger（接口文档）
- city-parking-common-config（统一配置）
- city-parking-common-auth（认证授权）
- city-parking-common-log（日志）
- pagehelper-spring-boot-starter（分页）

**自动装配类**：
```java
cn.city.parking.common.bff.ServerStarterConfig        // BFF启动配置
cn.city.parking.common.bff.ExecutePoolConfiguration   // 线程池配置
```

**核心功能**：
1. **Undertow容器**：性能比Tomcat高30%
2. **Dubbo客户端**：通过`@DubboReference`调用后端微服务
3. **接口聚合**：聚合多个后端服务的数据返回给前端

**使用示例**：
```java
// BFF Controller聚合多个后端服务
@RestController
@RequestMapping("/api/eop/user")
public class EopUserController {

    @DubboReference
    private UserDubboApi userDubboApi;  // 后端用户服务

    @DubboReference
    private RoleDubboApi roleDubboApi;  // 后端角色服务

    @DubboReference
    private DeptDubboApi deptDubboApi;  // 后端部门服务

    /**
     * 聚合用户、角色、部门信息
     */
    @GetMapping("/{id}")
    public ResponseResult<UserDetailVO> getUserDetail(@PathVariable String id) {
        // 1. 调用用户服务
        User user = userDubboApi.getInfo(id).getData();

        // 2. 调用角色服务
        List<Role> roles = roleDubboApi.getRolesByUserId(id).getData();

        // 3. 调用部门服务
        Dept dept = deptDubboApi.getInfo(user.getDeptId()).getData();

        // 4. 聚合数据
        UserDetailVO vo = new UserDetailVO();
        vo.setUser(user);
        vo.setRoles(roles);
        vo.setDept(dept);

        return ResponseResult.success(vo);
    }
}
```

**POM配置示例**（BFF模块）：
```xml
<dependencies>
    <!-- BFF基础设施 -->
    <dependency>
        <groupId>cn.city-parking</groupId>
        <artifactId>city-parking-common-bff</artifactId>
    </dependency>

    <!-- 后端服务API（Dubbo接口） -->
    <dependency>
        <groupId>cn.city-parking</groupId>
        <artifactId>city-parking-rbac-api</artifactId>
    </dependency>
    <dependency>
        <groupId>cn.city-parking</groupId>
        <artifactId>city-parking-eop-api</artifactId>
    </dependency>
    <!-- ...更多后端服务API... -->
</dependencies>
```

---

#### 2.4 common-dubbo（Dubbo RPC增强）

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-dubbo</artifactId>
</dependency>
```

**功能描述**：
- Dubbo RPC增强功能
- 提供`BaseDubboApi`基类
- Sentinel集成（Dubbo限流熔断）

**核心依赖**：
- dubbo-spring-boot-starter
- sa-token-dubbo3（Sa-Token与Dubbo集成）
- sentinel-apache-dubbo3-adapter（Sentinel与Dubbo集成）
- sentinel-transport-simple-http

**自动装配类**：
```java
cn.city.parking.common.dubbo.filter.InitConfig
```

**核心功能**：
1. **BaseDubboApi基类**：
   - 提供`startDubboPage()`方法（分页）
   - 自动处理分页参数

2. **全局异常处理**：
   - 统一处理Dubbo调用异常

**使用示例**：
```java
@DubboService
public class UserDubboApiImpl extends BaseDubboApi implements UserDubboApi {

    @Autowired
    private IUserService userService;

    @Override
    public ResponseResult<PageInfo<User>> pageList(User user) {
        // 调用startDubboPage()处理分页
        startDubboPage();
        List<User> list = userService.selectUserList(user);
        return ResponseResult.success(new PageInfo<>(list));
    }
}
```

**重要路径**：
```java
// ✅ 正确路径
import cn.city.parking.common.dubbo.filter.base.BaseDubboApi;

// ❌ 错误路径（已废弃）
import cn.city.parking.common.auth.base.BaseDubboApi;
```

---

#### 2.5 common-auth（Sa-Token认证授权）⭐

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-auth</artifactId>
</dependency>
```

**功能描述**：
- 基于Sa-Token的认证授权
- 支持单点登录（SSO）
- Redis缓存Token

**核心依赖**：
- city-parking-common-dubbo
- city-parking-common-core
- sa-token-spring-boot-starter（Sa-Token核心）
- sa-token-redis-jackson（Redis存储Token）
- sa-token-alone-redis（权限缓存与业务缓存分离）
- sa-token-sso（单点登录，可选）
- spring-cloud-starter-alibaba-sentinel

**自动装配类**：
```java
cn.city.parking.common.auth.exception.GlobalExceptionHandler  // 全局异常处理
cn.city.parking.common.auth.filter.TraceFilter              // TraceId追踪
cn.city.parking.common.auth.filter.ChunYunFilter            // 自定义过滤器
```

**核心功能**：
1. **登录认证**：`StpUtil.login(userId)`
2. **权限校验**：`StpUtil.checkPermission("user:add")`
3. **角色校验**：`StpUtil.checkRole("admin")`
4. **Token管理**：自动存储到Redis

**使用示例**：
```java
// 1. 登录
@PostMapping("/login")
public ResponseResult<String> login(@RequestBody LoginDTO dto) {
    // 验证用户名密码
    User user = userService.authenticate(dto.getUsername(), dto.getPassword());

    // 登录，Sa-Token自动生成Token并存入Redis
    StpUtil.login(user.getId());

    // 返回Token
    return ResponseResult.success(StpUtil.getTokenValue());
}

// 2. 需要登录的接口
@SaCheckLogin
@GetMapping("/user/info")
public ResponseResult<User> getUserInfo() {
    String userId = StpUtil.getLoginIdAsString();
    User user = userService.selectById(userId);
    return ResponseResult.success(user);
}

// 3. 需要权限的接口
@SaCheckPermission("user:add")
@PostMapping("/user")
public ResponseResult<Integer> addUser(@RequestBody User user) {
    return ResponseResult.success(userService.insertUser(user));
}
```

---

### 三、数据层

#### 3.1 common-redis（Redis + Redisson）⭐

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-redis</artifactId>
</dependency>
```

**功能描述**：
- Redis操作工具类
- Redisson分布式锁
- 防重复提交注解

**核心依赖**：
- redisson-spring-boot-starter（Redisson）
- city-parking-common-core
- spring-boot-starter-aop
- lettuce-core（Redis客户端）

**自动装配类**：
```java
cn.city.parking.common.redis.configure.RedisConfig
```

**核心功能**：

1. **RedisUtils工具类**：
```java
// 存储对象
RedisUtils.setCacheObject("user:info:" + id, user, 3600);  // 3600秒过期

// 获取对象
User user = RedisUtils.getCacheObject("user:info:" + id, User.class);

// 删除
RedisUtils.deleteObject("user:info:" + id);

// 批量删除（⚠️ 生产环境慎用，会扫描全库）
RedisUtils.batchDeleteObj("user:*");
```

2. **Redisson分布式锁**：
```java
@Autowired
private Locker locker;

// 加锁执行
locker.lock("order:create:" + orderId, 10, () -> {
    // 业务逻辑，10秒后自动释放
    orderService.createOrder(order);
});
```

3. **防重复提交注解**：
```java
@NoRepeatSubmit(interval = 5000, message = "请勿重复提交")
@PostMapping("/order")
public ResponseResult<Integer> createOrder(@RequestBody Order order) {
    return ResponseResult.success(orderService.createOrder(order));
}
```

**使用注意**：
- ❌ **不要随意使用Redis缓存**（如无必要，不要缓存）
- ✅ **缓存使用条件**（同时满足）：
  - 查询频率 > 100次/分钟
  - 数据变更频率 < 10次/天
  - 数据量 < 1MB
  - 可容忍短暂不一致

---

#### 3.2 common-datasource（动态数据源）

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-datasource</artifactId>
</dependency>
```

**功能描述**：
- 动态数据源切换
- 读写分离

**核心依赖**：
- dynamic-datasource-spring-boot-starter
- jackson-databind
- jackson-datatype-jsr310

**自动装配**: 无（需要手动配置）

**配置示例**：
```yaml
spring:
  datasource:
    dynamic:
      primary: master  # 默认数据源
      datasource:
        master:
          url: jdbc:mysql://localhost:3306/db1
          username: root
          password: root
        slave:
          url: jdbc:mysql://localhost:3306/db2
          username: root
          password: root
```

**使用示例**：
```java
@DS("slave")  // 切换到从库
public List<User> selectUserList() {
    return userMapper.selectList(null);
}
```

---

#### 3.3 common-datascope（数据权限控制）

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-datascope</artifactId>
</dependency>
```

**功能描述**：
- 数据权限控制
- SQL自动拼接权限条件

**核心依赖**：
- mybatis-plus-boot-starter
- transmittable-thread-local

**自动装配**: 有（已注释，需要手动启用）

**使用场景**：
- 按部门过滤数据
- 按角色过滤数据

---

#### 3.4 common-tenant（多租户）

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-tenant</artifactId>
</dependency>
```

**功能描述**：
- 多租户数据隔离
- SQL自动拼接租户ID

**核心依赖**：
- city-parking-common-core
- mybatis-plus-boot-starter

**自动装配**: 无（需要手动配置）

**使用场景**：
- SaaS多租户系统
- 自动在SQL中添加`WHERE tenant_id = ?`

---

#### 3.5 common-seata（分布式事务）

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-seata</artifactId>
</dependency>
```

**功能描述**：
- Seata分布式事务
- AT模式自动补偿

**核心依赖**：
- spring-cloud-starter-alibaba-seata（排除自带的seata-spring-boot-starter）
- seata-spring-boot-starter

**自动装配类**：
```java
cn.city.parking.common.seata.aspect.SeataTransactionAspect
```

**使用示例**：
```java
@GlobalTransactional
public void createOrder(Order order) {
    // 1. 创建订单
    orderService.insertOrder(order);

    // 2. 扣减库存（调用库存服务）
    stockDubboApi.deduct(order.getProductId(), order.getQuantity());

    // 3. 扣减余额（调用账户服务）
    accountDubboApi.deduct(order.getUserId(), order.getAmount());

    // 任意服务失败，Seata自动回滚所有服务
}
```

---

### 四、网关/网络层

#### 4.1 common-gateway（Spring Cloud Gateway网关）⭐

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-gateway</artifactId>
</dependency>
```

**功能描述**：
- Spring Cloud Gateway网关
- 统一路由、鉴权、限流、熔断
- Sentinel集成

**核心依赖**：
- spring-cloud-starter-gateway（Gateway核心）
- spring-cloud-starter-alibaba-nacos-discovery（服务发现）
- spring-cloud-starter-alibaba-nacos-config（配置中心）
- spring-cloud-starter-alibaba-sentinel（限流熔断）
- spring-cloud-alibaba-sentinel-gateway（Gateway集成Sentinel）
- sentinel-datasource-nacos（规则存储）
- city-parking-common-redis（Redis）
- knife4j-gateway-spring-boot-starter（聚合API文档）
- sa-token-reactor-spring-boot-starter（Sa-Token响应式）
- sa-token-sso（单点登录）
- city-parking-common-oauth2（OAuth2）
- spring-cloud-starter-loadbalancer（负载均衡）

**自动装配类**：
```java
cn.city.parking.common.gateway.config.GatewayConfig
```

**核心功能**：
1. **统一路由**：路由到不同的BFF或微服务
2. **统一鉴权**：通过GlobalFilter验证Token
3. **限流熔断**：集成Sentinel
4. **API文档聚合**：Knife4j聚合所有服务的接口文档

**配置示例**：
```yaml
spring:
  cloud:
    gateway:
      routes:
        # 路由到PC端BFF
        - id: bff-eop-route
          uri: lb://city-parking-bff-eop
          predicates:
            - Path=/api/eop/**
          filters:
            - StripPrefix=1

        # 路由到APP端BFF
        - id: bff-app-route
          uri: lb://city-parking-bff-app
          predicates:
            - Path=/api/app/**
          filters:
            - StripPrefix=1
```

---

#### 4.2 common-webflux（WebFlux响应式）

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-webflux</artifactId>
</dependency>
```

**功能描述**：
- WebFlux响应式编程
- 适用于高并发场景

**核心依赖**：
- city-parking-common-dubbo
- spring-cloud-starter-alibaba-nacos-discovery
- spring-cloud-starter-alibaba-nacos-config
- spring-cloud-starter-alibaba-sentinel
- city-parking-common-redis
- spring-boot-starter-webflux

**自动装配类**：
```java
cn.city.parking.common.webflux.filter.TraceFilter
cn.city.parking.common.webflux.web.WebConfig
cn.city.parking.common.webflux.config.CorsConfig
cn.city.parking.common.webflux.ExecutePoolConfiguration
```

---

#### 4.3 common-websocket（WebSocket长连接）

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-websocket</artifactId>
</dependency>
```

**功能描述**：
- WebSocket长连接
- 实时推送消息

**核心依赖**：
- city-parking-common-redis
- spring-boot-starter-websocket
- fastjson

**自动装配类**：
```java
cn.city.parking.common.websocket.config.WebSocketConfig
```

**使用场景**：
- 实时消息推送
- 设备状态实时监控

---

### 五、第三方集成层

#### 5.1 common-opensdk（阿里云/支付宝/极光推送SDK）

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-opensdk</artifactId>
</dependency>
```

**功能描述**：
- 阿里云SDK（OSS、短信、一键登录、内容安全）
- 支付宝SDK
- 极光推送SDK

**核心依赖**：
- aliyun-java-sdk-dypnsapi（一键登录）
- aliyun-java-sdk-green（内容安全）
- aliyun-sdk-oss（对象存储）
- aliyun-java-sdk-dysmsapi（短信）
- alipay-sdk-java（支付宝）
- jpush-client（极光推送）

**自动装配类**：
```java
cn.city.parking.common.opensdk.modules.alibaba.cloud.AliCloudConfig
cn.city.parking.common.opensdk.modules.alibaba.alipay.AlipayConfig
cn.city.parking.common.opensdk.modules.jiguang.JPushConfig
```

**使用场景**：
- 文件上传（OSS）
- 短信验证码
- 支付宝支付
- 推送通知

---

#### 5.2 common-mq（RocketMQ消息队列）

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-mq</artifactId>
</dependency>
```

**功能描述**：
- RocketMQ消息队列
- 阿里云ONS

**核心依赖**：
- ons-client（阿里云RocketMQ）
- mq-http-sdk
- aliyun-sdk-oss
- rocketmq-spring-boot-starter

**自动装配类**：
```java
cn.city.parking.common.mq.config.RocketMQAutoConfig
```

---

#### 5.3 common-mqtt（MQTT物联网协议）

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-mqtt</artifactId>
</dependency>
```

**功能描述**：
- MQTT协议支持
- 物联网设备通信

**核心依赖**：
- city-parking-common-concurrent
- spring-integration-mqtt

**自动装配类**：
```java
cn.city.parking.common.mqtt.MqttAutoConfig
```

---

#### 5.4 common-wxmp（微信公众号）

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-wxmp</artifactId>
</dependency>
```

**功能描述**：
- 微信公众号SDK封装

**核心依赖**：
- redisson-spring-boot-starter (3.13.6)
- city-parking-common-core
- okhttps（HTTP客户端）
- okhttps-gson

**自动装配类**：
```java
cn.city.parking.common.wxmp.config.WxMpAutoConfig
```

---

#### 5.5 common-wxmp-dubboapi（微信公众号Dubbo API）

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-wxmp-dubboapi</artifactId>
</dependency>
```

**功能描述**：
- 微信公众号Dubbo接口定义

**核心依赖**：
- city-parking-common-auth

**自动装配**: 无

---

### 六、工具类层

#### 6.1 common-log（操作日志记录）

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-log</artifactId>
</dependency>
```

**功能描述**：
- AOP记录操作日志
- 自动记录用户操作

**核心依赖**：
- spring-boot-starter-aop（可选）
- city-parking-common-core
- spring-boot-starter-logging
- spring-boot-starter-jdbc（可选）

**自动装配类**：
```java
cn.city.parking.common.log.LogConfig
```

**使用示例**：
```java
@Log(title = "用户管理", businessType = BusinessType.INSERT)
@PostMapping("/user")
public ResponseResult<Integer> addUser(@RequestBody User user) {
    return ResponseResult.success(userService.insertUser(user));
}
```

---

#### 6.2 common-job（XXL-Job定时任务）

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-job</artifactId>
</dependency>
```

**功能描述**：
- XXL-Job定时任务集成

**核心依赖**：
- xxl-job-core
- hutool-all

**自动装配类**：
```java
cn.city.parking.common.job.config.JobConfig
```

**使用示例**：
```java
@XxlJob("syncUserDataJobHandler")
public void syncUserData() {
    log.info("开始同步用户数据...");
    // 业务逻辑
}
```

---

#### 6.3 common-message（阿里云语音消息）

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-message</artifactId>
</dependency>
```

**功能描述**：
- 阿里云语音通知

**核心依赖**：
- hutool-all
- dyvmsapi20170525 (2.1.4)

**自动装配类**：
```java
cn.city.parking.common.message.voice.config.VoiceConfig
```

---

#### 6.4 common-swagger（Knife4j接口文档）

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-swagger</artifactId>
</dependency>
```

**功能描述**：
- Knife4j接口文档自动生成

**核心依赖**：
- knife4j-openapi3-spring-boot-starter

**自动装配类**：
```java
cn.city.parking.common.swagger.config.SwaggerAutoConfiguration
cn.city.parking.common.swagger.config.SwaggerWebConfiguration
```

**访问地址**：
- http://localhost:9999/doc.html

---

#### 6.5 common-sensitive（数据脱敏）

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-sensitive</artifactId>
</dependency>
```

**功能描述**：
- 数据脱敏（手机号、身份证、银行卡等）

**核心依赖**：
- city-parking-common-core
- spring-boot-starter-aop（可选）
- mybatis

**自动装配类**：
```java
cn.city.parking.common.sensitive.SensitiveAutoConfig
```

**使用示例**：
```java
@Data
public class User {
    @Sensitive(type = SensitiveType.MOBILE_PHONE)
    private String mobile;  // 返回：138****1234

    @Sensitive(type = SensitiveType.ID_CARD)
    private String idCard;  // 返回：110***********1234
}
```

---

#### 6.6 common-device（设备信息工具）

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-device</artifactId>
</dependency>
```

**功能描述**：
- 设备信息工具类
- 二维码生成

**核心依赖**：
- fastjson
- commons-codec
- zxing（二维码）
- city-parking-common-core

**自动装配**: 无

---

### 七、监控层

#### 7.1 common-monitor（Prometheus监控指标）⭐

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-monitor</artifactId>
</dependency>
```

**功能描述**：
- Prometheus监控指标采集
- Dubbo指标监控
- JVM指标监控

**核心依赖**：
- simpleclient_spring_boot（Spring Boot指标）
- simpleclient_hotspot（JVM指标）
- dubbo-metrics-prometheus（Dubbo指标）
- dubbo-observability-spring-boot-starter（Dubbo可观测性）
- micrometer-registry-prometheus（Micrometer集成）
- simpleclient_pushgateway（PushGateway支持）

**自动装配**: 无（通过common-config引用）

**暴露端点**：
- http://localhost:9999/actuator/prometheus

**Grafana监控**：
- 已配通Prometheus + Grafana
- 实时监控服务健康状态

---

#### 7.2 common-oauth2（OAuth2.0）

**Maven坐标**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-oauth2</artifactId>
</dependency>
```

**功能描述**：
- OAuth2.0协议支持

**核心依赖**：
- sa-token-jwt
- sa-token-oauth2
- sa-token-redis-jackson
- sa-token-spring-boot-starter

**自动装配**: 有（已注释，需要手动启用）

---

## 📊 组件依赖关系图

### 核心依赖链

```
common-core (基础)
    ↓
common-config (配置 + 监控)
    ↓
common-redis (Redis)
    ↓
common-auth (认证)
    ↓
common-dubbo (Dubbo增强)
    ↓
┌────────────┬────────────┐
↓            ↓            ↓
common-server  common-bff  common-gateway
(微服务)      (BFF聚合层)  (网关)
```

### 常用组合

**1. 标准微服务（Server模块）**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-server</artifactId>
</dependency>
<!-- common-server已包含：
     - common-config (配置+监控)
     - common-redis (Redis)
     - common-auth (认证)
     - common-datasource (数据源)
     - common-tenant (多租户)
     - MyBatis Plus + Dubbo + Nacos + Sentinel
-->
```

**2. BFF聚合层**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-bff</artifactId>
</dependency>
<!-- common-bff已包含：
     - common-config (配置+监控)
     - common-redis (Redis)
     - common-auth (认证)
     - common-log (日志)
     - Dubbo客户端 + Nacos + Sentinel
-->
```

**3. Gateway网关**：
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-gateway</artifactId>
</dependency>
<!-- common-gateway已包含：
     - common-config (配置+监控)
     - common-redis (Redis)
     - common-oauth2 (OAuth2)
     - Spring Cloud Gateway + Nacos + Sentinel
-->
```

---

## 🎯 最佳实践

### 1. 选择合适的基础组件

**场景1：标准微服务（CRUD业务）**
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-server</artifactId>
</dependency>
```
- ✅ 推荐使用common-server（MyBatis Plus + 完整基础设施）
- ❌ 不要使用common-service（除非必须使用纯MyBatis）

**场景2：BFF聚合层**
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-bff</artifactId>
</dependency>
```
- ✅ 适用于PC端、APP端、H5端的BFF服务
- ✅ 通过Dubbo调用后端微服务，聚合数据返回前端

**场景3：API网关**
```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-gateway</artifactId>
</dependency>
```
- ✅ 统一路由、鉴权、限流、熔断

---

### 2. 避免重复依赖

**❌ 错误示例**（重复依赖）：
```xml
<!-- common-server已经包含Redis、Auth、Dubbo等，不要重复添加 -->
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-server</artifactId>
</dependency>
<dependency>
    <!-- ❌ 错误：common-server已包含Redis -->
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-redis</artifactId>
</dependency>
<dependency>
    <!-- ❌ 错误：common-server已包含Auth -->
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-auth</artifactId>
</dependency>
```

**✅ 正确示例**：
```xml
<!-- Server模块只需依赖common-server -->
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-server</artifactId>
</dependency>

<!-- API模块只需依赖common-auth -->
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-auth</artifactId>
</dependency>
```

---

### 3. 使用自动装配

**✅ 推荐**：利用spring.factories自动装配，无需手动配置

```java
// ✅ 启动类只需2个注解
@Slf4j
@SpringBootApplication
public class CityParkingXxxApplication {
    public static void main(String[] args) {
        SpringApplication.run(CityParkingXxxApplication.class, args);
    }
}
// 以下注解已自动配置，无需添加：
// @EnableDubbo
// @MapperScan
// @ComponentScan
// @EnableAsync
```

---

### 4. Redis缓存使用原则

**❌ 不要随意使用Redis缓存**（如无必要，不要缓存）

**✅ 缓存使用条件**（同时满足）：
- 查询频率 > 100次/分钟
- 数据变更频率 < 10次/天
- 数据量 < 1MB
- 可容忍短暂不一致

**推荐场景**：
- ✅ 系统配置
- ✅ 字典数据
- ✅ 用户权限

**不推荐场景**：
- ❌ 订单信息
- ❌ 库存数据
- ❌ 金融数据

---

### 5. 分布式锁使用原则

**优先级**：数据库约束 > 乐观锁 > 分布式锁

**推荐场景**：
- ✅ 库存扣减
- ✅ 优惠券领取
- ✅ 订单号生成
- ✅ 定时任务防重

**使用示例**：
```java
@Autowired
private Locker locker;

locker.lock("stock:deduct:" + productId, 10, () -> {
    // 1. 查询库存
    Stock stock = stockMapper.selectById(productId);

    // 2. 扣减库存
    if (stock.getQuantity() >= quantity) {
        stock.setQuantity(stock.getQuantity() - quantity);
        stockMapper.updateById(stock);
    } else {
        throw new BusinessException("库存不足");
    }
});
```

---

## 📝 快速参考表

### 按功能快速查找组件

| 功能需求 | 使用组件 | Maven坐标 |
|---------|---------|----------|
| **标准微服务** | common-server | city-parking-common-server |
| **BFF聚合层** | common-bff | city-parking-common-bff |
| **API网关** | common-gateway | city-parking-common-gateway |
| **Redis缓存** | common-redis | city-parking-common-redis |
| **分布式锁** | common-redis | city-parking-common-redis |
| **认证授权** | common-auth | city-parking-common-auth |
| **操作日志** | common-log | city-parking-common-log |
| **定时任务** | common-job | city-parking-common-job |
| **接口文档** | common-swagger | city-parking-common-swagger |
| **数据脱敏** | common-sensitive | city-parking-common-sensitive |
| **动态数据源** | common-datasource | city-parking-common-datasource |
| **多租户** | common-tenant | city-parking-common-tenant |
| **分布式事务** | common-seata | city-parking-common-seata |
| **消息队列** | common-mq | city-parking-common-mq |
| **文件上传** | common-opensdk | city-parking-common-opensdk |
| **短信验证码** | common-opensdk | city-parking-common-opensdk |
| **微信公众号** | common-wxmp | city-parking-common-wxmp |
| **WebSocket** | common-websocket | city-parking-common-websocket |
| **监控指标** | common-monitor | city-parking-common-monitor |

---

## 🔗 相关文档

- [City Parking 2.0架构分析报告](../../city-parking_架构分析报告_2025-11-17.md)
- [CLAUDE.md编码规范](../../CLAUDE.md)

---

## 📞 联系方式

**技术架构组**：architecture@city-parking.cn
**文档维护**：技术部 - 张扬

---

**最后更新时间**：2025-11-17 16:30:00
**下次更新时间**：2026-05-17（每半年更新一次）
