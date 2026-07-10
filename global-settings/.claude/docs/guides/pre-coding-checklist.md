# 编码前强制检查清单

> **CRITICAL - 每次编写业务代码前，必须执行以下检查**

---

## 0. 判断是否是 City Parking 2.0 框架

**首先检查项目的 `pom.xml` 中的 parent：**

```xml
<parent>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-parent</artifactId>  <!-- ✅ 有这个才是 2.0 框架 -->
    <version>2.0.0-SNAPSHOT</version>
</parent>
```

- ✅ **是 2.0 框架**：继续执行下面的检查步骤
- ❌ **不是 2.0 框架**：执行以下流程：
  1. **分析项目架构**：阅读 pom.xml、项目结构、核心代码，理解技术栈和分层规范
  2. **存储到记忆**：使用 `mcp__memory__create_entities` 工具，将项目架构信息存入知识图谱
  3. **后续编码**：从记忆中读取该项目的架构规范，按其实际情况编码

**非 2.0 框架记忆存储示例**：
```json
{
  "name": "project-xxx-architecture",
  "entityType": "ProjectArchitecture",
  "observations": [
    "技术栈：Spring Boot 2.x + MyBatis + Redis",
    "分层：Controller → Service → Dao",
    "命名规范：XxxController, XxxService, XxxDao",
    "实体类：无基类，手动维护 id/createTime/updateTime",
    "事务：Service 层使用 @Transactional"
  ]
}
```

---

## 1. 识别项目类型

**确认是 2.0 框架后，检查 `pom.xml` 依赖了哪个 common 组件：**

| pom.xml 依赖 | 项目类型 | 职责 | 编码规范 |
|-------------|---------|------|---------|
| `city-parking-common-server` | **下游业务服务** | 提供 Dubbo 接口，操作数据库 | 使用 MyBatis-Plus（Mapper/Service/DubboApi） |
| `city-parking-common-bff` | **BFF聚合服务** | 对外暴露 HTTP 接口，调用下游服务 | 使用 @RestController + @DubboReference |
| `city-parking-common-gateway` | **网关服务** | 路由、鉴权、限流、XSS防护 | 使用 Spring Cloud Gateway Filter |

### 下游业务服务（common-server）

```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-server</artifactId>
</dependency>
```

**编码规范**：
- **Mapper**：继承 `CommonMapper<T>`，使用公司框架扩展的 MyBatis-Plus Mapper 能力
- **Service接口**：继承 `IService<T>`
- **Service实现**：继承 `ServiceImpl<Mapper, Entity>`，增删改加 `@Transactional`
- **DubboApi实现**：继承 `BaseDubboApi`，返回 `ResponseResult<T>`
- **Entity**：继承 `BusinessEntity`，添加 `@TableName`
- ❌ **禁止使用 @RestController**

### BFF聚合服务（common-bff）

```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-bff</artifactId>
</dependency>
```

**编码规范**：
- 使用 `@RestController` 对外暴露 HTTP 接口
- 使用 `@DubboReference` 调用下游服务
- 负责数据聚合、裁剪、格式转换
- ❌ **禁止直接操作数据库**（没有 Mapper）

**BFF 层代码结构**：
```
city-parking-bff-xxx/
├── controller/          # 接收请求、参数校验、返回结果
│   └── UserController.java
├── service/             # ✅ BFF 专属 Service（聚合、编排、轻量业务逻辑）
│   └── UserBffService.java
├── converter/           # DTO/VO 转换（可选）
│   └── UserConverter.java
└── vo/                  # 视图对象
    └── UserDetailVO.java
```

**Service 命名规范**：`XxxBffService`（后缀 Bff 区分下游服务）

```java
@Service
public class UserBffService {
    @DubboReference
    private UserDubboApi userDubboApi;
    @DubboReference
    private RoleDubboApi roleDubboApi;

    /**
     * 聚合多个下游服务、数据裁剪、格式转换
     */
    public UserDetailVO getUserDetail(String userId) {
        User user = userDubboApi.getInfo(userId).getData();
        List<Role> roles = roleDubboApi.listByUserId(userId).getData();
        return UserConverter.toDetailVO(user, roles);
    }
}

@RestController
@RequestMapping("/api/user")
public class UserController {
    @Autowired
    private UserBffService userBffService;  // ✅ 调用 BffService

    @GetMapping("/{id}/detail")
    public ResponseResult<UserDetailVO> getDetail(@PathVariable String id) {
        return ResponseResult.success(userBffService.getUserDetail(id));
    }
}
```

**BFF Service 职责**：
- ✅ 聚合多个下游 Dubbo 接口
- ✅ 数据裁剪、格式转换
- ✅ 轻量级业务编排
- ❌ **禁止直接操作数据库**

### 网关服务（common-gateway）

```xml
<dependency>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-common-gateway</artifactId>
</dependency>
```

**编码规范**：
- 使用 Spring Cloud Gateway 的 `GlobalFilter`
- 负责路由转发、鉴权、限流、XSS防护等
- ❌ **禁止写业务逻辑**

---

## 2. 编码前必须查阅 Common 组件

**在编写任何功能前，必须先查阅** [common-components-architecture.md](../architecture/common-components-architecture.md)，确认是否已有现成组件：

| 需求场景 | 先查阅的 Common 组件 |
|---------|---------------------|
| Redis操作、缓存 | `common-redis` → `RedisUtils` |
| 分布式锁 | `common-redis` → `Locker` |
| 防重复提交 | `common-redis` → `@NoRepeatSubmit` |
| 参数校验 | `common-core` → `ValidateUtil` |
| 异常处理 | `common-core` → `BusinessException` |
| 响应封装 | `common-core` → `ResponseResult` |
| 分页查询 | `common-dubbo` → `BaseDubboApi.startDubboPage()` |
| 用户上下文 | `common-auth` → `SecurityUtils` |
| 数据权限 | `common-server` → `@MyDataScope` |
| 日期处理 | Hutool → `DateUtil`（已引入） |
| 字符串处理 | Apache Commons → `StringUtils`（已引入） |
| 集合操作 | Guava → `Lists`, `Maps`（已引入） |

**⚠️ 禁止重复造轮子！优先使用 common 组件中已有的工具类和功能。**
