# 架构规范

## 技术栈

### 核心框架
- **Spring Boot**: 2.7.18
- **Spring Cloud Alibaba**: 2021.1
- **Dubbo**: 3.3.2（RPC框架，服务间通信）
- **Nacos**: 2.1.1（注册中心 + 配置中心）
- **MyBatis Plus**: 3.5.7
- **Redis**: Lettuce
- **MySQL**: 8.0+

### 重要说明
⚠️ 服务间调用使用 **Dubbo RPC**（@DubboService、@DubboReference），❌ **不使用 Feign**

## 服务分层

```
DubboApi实现（Controller层）→ Service层 → Mapper层 → 数据库
```

### 职责说明
- **DubboApi/Controller层**：薄层，只负责参数校验、调用Service、记录日志、返回结果
- **Service层**：业务逻辑层，处理所有业务逻辑、事务控制
- **Mapper层**：数据访问层，与数据库交互
- **数据库**：数据持久化

## Maven 模块结构

### 标准项目结构
```
city-parking-xxx/
├── pom.xml                      # 父POM（聚合器，不发布到Maven私库）
├── city-parking-xxx-api/       # API模块（发布到Maven私库）
│   └── cn/city/parking/xxx/api/
│       ├── entity/              # ⚠️ 实体类（必须在api包下！）
│       ├── XxxDubboApi.java    # Dubbo接口定义
│       └── dto/                 # DTO（可选）
└── city-parking-xxx-server/    # Server模块（服务实现，不发布）
    ├── XxxApplication.java      # 启动类
    ├── dubbo/                   # DubboApi实现
    ├── service/                 # Service层
    └── mapper/                  # Mapper层
```

### 关键路径规范

⚠️ **Entity 包路径必须正确**：
- ✅ **正确**：`cn.city.parking.xxx.api.entity`（必须在 api 包下）
- ❌ **错误**：`cn.city.parking.xxx.entity`（缺少 api 层级）

### 模块依赖关系

#### 独立仓库设计
- **city-parking-parent**：独立仓库，**必须发布到Maven私库**，所有微服务都依赖它
- **city-parking-common-xxx**：独立仓库，发布到Maven私库，提供通用组件
- **微服务项目（如city-parking-eop）**：独立仓库，包含：
  - 根pom（city-parking-xxx/pom.xml）：仅作为**聚合器**，用于本地开发，**不发布到Maven私库**
  - API模块：直接继承city-parking-parent（从Maven私库获取），发布到Maven私库
  - Server模块：直接继承city-parking-parent，不发布到Maven私库

#### 发布策略
- ✅ **发布到Maven私库**：city-parking-parent、city-parking-common-xxx、微服务的API模块
- ❌ **不发布到Maven私库**：微服务的根pom（聚合器）、微服务的Server模块

#### 为什么API和Server不继承根pom？
1. 微服务的根pom（聚合器）不会发布到Maven私库
2. 如果API继承根pom，其他项目引用API时会找不到根pom（因为根pom未发布）
3. city-parking-parent已经配置了所有必要的依赖管理和Maven私库地址
4. 根pom只是一个聚合器，方便本地多模块开发

## BFF 分层架构规范

### 核心架构约束

⚠️ **下游服务禁止对外暴露HTTP接口，只能通过BFF层对外提供服务。**

```
┌─────────────────────────────────────────────────────────┐
│                      前端应用                            │
│         （Web端、小程序、App）                           │
└─────────────────────────┬───────────────────────────────┘
                          │ HTTP/HTTPS
                          ▼
┌─────────────────────────────────────────────────────────┐
│               BFF层（Backend For Frontend）              │
│   city-parking-bff-eop、city-parking-bff-app 等         │
│   ✅ 允许使用 @RestController                            │
│   ✅ 对外暴露 HTTP 接口给前端                            │
│   ✅ 负责聚合、裁剪、适配前端需求                        │
└─────────────────────────┬───────────────────────────────┘
                          │ Dubbo RPC（内部通信）
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    下游业务服务                          │
│   city-parking-rbac、city-parking-eop、                 │
│   city-parking-order、city-parking-payment 等           │
│   ❌ 禁止使用 @RestController                            │
│   ❌ 禁止对外暴露 HTTP 接口                              │
│   ✅ 只能提供 @DubboService 接口                         │
│   ✅ 服务间通过 Dubbo RPC 通信                           │
└─────────────────────────────────────────────────────────┘
```

### BFF层（city-parking-bff-*）

✅ **允许的操作**：
- 使用 `@RestController` 注解
- 对外暴露 HTTP 接口给前端应用
- 通过 `@DubboReference` 调用下游服务
- 负责请求的聚合、裁剪、格式转换
- 处理前端特定的业务逻辑（如数据脱敏、字段裁剪）

### 下游业务服务（非BFF服务）

❌ **禁止的操作**：
- **禁止使用 `@RestController` 注解**
- **禁止对外暴露任何 HTTP 接口**

✅ **允许的操作**：
- 只能提供 `@DubboService` 接口供 BFF 层或其他服务调用
- 服务间通信必须通过 Dubbo RPC

### 为什么这样设计？

1. **安全性**：统一入口便于安全管控（鉴权、限流、审计）
2. **解耦**：前端变化不影响下游服务，下游服务专注业务逻辑
3. **灵活性**：不同前端（Web/App/小程序）可以有不同的 BFF 适配
4. **可维护性**：避免接口重复暴露，统一接口管理

### 违规示例

```java
// ❌ 错误：下游服务（city-parking-rbac-server）中写了 Controller
package cn.city.parking.rbac.controller;

@RestController  // ❌ 禁止！下游服务不能有Controller
@RequestMapping("/api/user")
public class UserController {
    // ...
}

// ❌ 错误：下游服务同时暴露 HTTP 和 Dubbo
@RestController  // ❌ 禁止
@DubboService    // ✅ 应该只有这个
public class UserDubboApiImpl implements UserDubboApi {
    // ...
}
```

### 正确示例

```java
// ✅ 正确：BFF层（city-parking-bff-eop）对外暴露HTTP接口
package cn.city.parking.bff.eop.controller;

@Slf4j
@RestController  // ✅ BFF层允许
@RequestMapping("/api/user")
public class UserController {
    @DubboReference  // ✅ 调用下游服务
    private UserDubboApi userDubboApi;

    @GetMapping("/{id}")
    public ResponseResult<UserVO> getUser(@PathVariable String id) {
        ResponseResult<User> result = userDubboApi.getInfo(id);
        // 数据转换、裁剪
        return ResponseResult.success(convertToVO(result.getData()));
    }
}

// ✅ 正确：下游服务（city-parking-rbac-server）只提供Dubbo接口
package cn.city.parking.rbac.dubbo;

@Slf4j
@DubboService  // ✅ 只有 DubboService
public class UserDubboApiImpl extends BaseDubboApi implements UserDubboApi {
    @Autowired
    private IUserService userService;

    @Override
    public ResponseResult<User> getInfo(String id) {
        User user = userService.selectUserById(id);
        return ResponseResult.success(user);
    }
}
```

### 检查方法

```bash
# 检查下游服务是否有 Controller（应该为空）
grep -r "@RestController" city-parking-rbac-server/src/
grep -r "@Controller" city-parking-eop-server/src/

# 只有 BFF 服务可以有 Controller
grep -r "@RestController" city-parking-bff-eop/src/  # 允许
```

## 参考项目

- **city-parking-eop**：运营平台（完整示例）
- **city-parking-template**：服务模板
- **city-parking-bff-eop**：BFF服务示例

---

**文档版本**：1.0
**最后更新**：2026-01-24
