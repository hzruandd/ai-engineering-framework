# City Parking 全局通用配置

此目录包含适用于所有 City Parking 微服务项目的 Claude Code 全局配置。

## 📁 目录结构

```
global-settings/
├── README.md              # 本文件
└── .claude/               # Claude Code 配置目录
    ├── CLAUDE.md          # 项目级规范（完整版，52KB）
    ├── commands/          # 自定义快捷命令（11个）
    │   ├── add-field.md       # /add-field - 添加字段
    │   ├── analyze-slow-query.md  # /analyze-slow-query - 慢查询分析
    │   ├── design-doc.md      # /design-doc - 技术设计文档
    │   ├── diff-report.md     # /diff-report - 代码修改报告
    │   ├── fix-cache.md       # /fix-cache - 缓存优化
    │   ├── formal-review.md   # /formal-review - 正式代码评审
    │   ├── generate-tests.md  # /generate-tests - 生成单元测试
    │   ├── new-api.md         # /new-api - 添加接口
    │   ├── new-crud.md        # /new-crud - 生成CRUD
    │   └── review-code.md     # /review-code - 代码审查
    ├── docs/              # 详细文档
    │   ├── architecture/      # 架构设计文档
    │   │   ├── cache-design.md          # 缓存设计方案
    │   │   ├── common-components-architecture.md  # 29个Common组件详解
    │   │   ├── distributed-transaction.md  # 分布式事务
    │   │   ├── mq-mqtt-integration.md   # MQ/MQTT集成
    │   │   ├── thread-pool-design.md    # 线程池设计
    │   │   └── trace-propagation.md     # 链路追踪
    │   ├── design/            # 设计规范
    │   │   └── 前后端状态码规范设计.md
    │   ├── examples/          # 实战案例
    │   │   ├── batch-operations.md      # 批量操作与事务
    │   │   ├── cache-usage.md           # 缓存使用
    │   │   ├── complex-query.md         # 复杂查询
    │   │   ├── distributed-lock.md      # 分布式锁
    │   │   └── standard-crud.md         # 标准CRUD
    │   └── guides/            # 开发指南
    │       ├── configuration-guide.md   # 配置指南
    │       ├── detailed-standards.md    # 详细规范
    │       ├── framework-features.md    # 框架功能
    │       ├── pre-coding-checklist.md  # 编码前检查清单
    │       └── solid-principles.md      # SOLID设计原则
    ├── ignore             # 忽略文件配置
    ├── settings.local.json  # 本地设置（可选）
    └── analyze_slow_queries.py  # Doris慢查询分析工具
```

## 🚀 安装方法

### 方式1：全局安装（推荐）

将 `.claude` 目录复制到用户主目录，所有项目自动生效：

```bash
# macOS/Linux
cp -r global-settings/.claude ~/

# Windows
xcopy global-settings\.claude %USERPROFILE%\.claude /E /I /Y
```

### 方式2：项目级安装

复制到具体项目根目录，仅该项目生效：

```bash
# 复制到目标项目
cp -r global-settings/.claude /path/to/your/project/

# 删除settings.local.json（会自动生成）
rm /path/to/your/project/.claude/settings.local.json
```

## 📋 配置内容说明

### CLAUDE.md（核心配置文件）

全局通用的开发规约和编码规范，包括：

- **核心开发原则**：代码修改原则、代码质量原则、安全原则
- **Java 开发规范**：命名、注释、格式、异常处理、空值处理等
- **数据库开发规范**：SQL 编写、MyBatis Mapper、字段命名
- **Spring Boot 开发规范**：依赖注入、Controller、Service 等
- **前端开发规范**：Vue/TypeScript 命名和最佳实践
- **Git 提交规范**：提交格式和类型
- **测试规范**：单元测试编写规范
- **性能优化要点**：数据库和代码优化建议
- **文档维护规范**：何时更新文档、文档质量标准
- **City Parking 框架核心规范**：13条必读规范
- **微服务分层架构规范**：BFF层与下游服务的职责边界

### 快捷命令（commands/）

11个自定义快捷命令，覆盖常见开发场景：

| 命令 | 说明 | 使用场景 |
|------|------|----------|
| `/new-crud` | 创建完整CRUD功能 | 新建实体和增删改查 |
| `/add-field` | 为实体添加新字段 | 扩展已有实体 |
| `/new-api` | 在已有模块添加新接口 | 扩展API功能 |
| `/fix-cache` | 添加或修复缓存 | 性能优化 |
| `/review-code` | 代码审查清单 | 提测前自查 |
| `/diff-report` | 生成代码修改报告 | 提交前总结 |
| `/generate-tests` | 生成单元测试 | 测试覆盖 |
| `/formal-review` | 正式代码评审报告 | 面向管理层 |
| `/design-doc` | 技术设计文档 | 方案设计 |
| `/analyze-slow-query` | Doris慢查询分析 | 性能诊断 |

### 详细文档（docs/）

**architecture/**：架构设计文档
- Common组件架构详解（29个组件）
- 缓存设计方案
- 分布式事务处理
- 线程池设计
- 链路追踪传递
- MQ/MQTT集成

**design/**：设计规范
- 前后端状态码规范

**examples/**：实战案例
- 标准CRUD实现
- 缓存使用示例
- 批量操作与事务
- 复杂查询与多表关联
- 分布式锁应用

**guides/**：开发指南
- 编码前检查清单
- 详细开发规范
- 框架自动配置功能
- SOLID设计原则
- 配置指南（POM、YAML、数据库）

## ✅ 配置生效验证

安装后，在任意项目中打开 Claude Code，询问：

```
请介绍一下 Java 的命名规范
```

如果 Claude 回答了与 `CLAUDE.md` 中一致的规范（如 PascalCase、camelCase 等），说明全局配置已生效。

## 🎯 使用场景

### 场景1：开发新功能
```
我：帮我实现用户积分功能，包括积分增加、扣减、查询
Claude：按照框架规范实现完整功能（Entity、Mapper、Service、DubboApi）
```

### 场景2：审查代码
```
我：/review-code
Claude：检查15项规范，列出问题清单
```

### 场景3：添加字段
```
我：/add-field
我：为User实体添加birthday字段，类型为LocalDateTime
Claude：自动更新Entity、Mapper.xml、Service、DubboApi
```

### 场景4：生成测试
```
我：/generate-tests
Claude：根据修改内容生成单元测试代码
```

### 场景5：提交前自查
```
我：/diff-report
Claude：生成代码修改报告，包含变更文件、测试情况、风险评估
```

## 🔧 关键规范速查

### 核心类包路径
```java
// ✅ 正确路径
import cn.city.parking.common.dubbo.filter.base.BaseDubboApi;
import cn.city.parking.common.core.web.domain.BusinessEntity;
import cn.city.parking.common.core.web.domain.ResponseResult;
import com.github.pagehelper.PageInfo;
import cn.city.parking.common.redis.RedisUtils;

// ❌ 错误路径（已废弃）
import cn.city.parking.common.auth.base.BaseDubboApi;  // 错误！
```

### DubboApi实现三要点
```java
@Slf4j
@DubboService
public class XxxDubboApiImpl extends BaseDubboApi implements XxxDubboApi {

    @Override
    public ResponseResult<User> getInfo(String id) {
        // 1. ✅ 参数校验
        Preconditions.checkArgument(StringUtils.isNotBlank(id), "ID不能为空");

        // 2. ✅ 调用Service（所有业务逻辑在Service层）
        User user = userService.selectUserById(id);

        // 3. ✅ 返回值必须带泛型
        return ResponseResult.success(user);

        // ❌ 禁止：try-catch、直接调用Mapper、复杂业务判断
    }
}
```

### 微服务分层规范
```
❌ 下游服务（city-parking-rbac、city-parking-eop等）：
   - 禁止使用 @RestController
   - 禁止对外暴露 HTTP 接口
   - 只能提供 @DubboService 接口

✅ BFF层（city-parking-bff-*）：
   - 允许使用 @RestController
   - 对外暴露 HTTP 接口给前端
   - 通过 @DubboReference 调用下游服务
```

### Mapper接口
```java
// ✅ 正确：不需要@Mapper注解
public interface UserMapper extends BaseMapper<User> {
    User selectByUsername(@Param("username") String username);
}

// ✅ 框架已自动注入批量方法
userMapper.insertBatchSomeColumn(userList);
```

### 启动类
```java
@Slf4j
@SpringBootApplication  // ✅ 只需这两个注解
public class CityParkingXxxApplication {
    // ❌ 不需要：@EnableDubbo、@MapperScan、@EnableAsync等
    // common-server已自动配置
}
```

## ⚠️ 重要提醒

### ❌ 绝对不要做
1. **下游服务使用 @RestController**（只有BFF层可以）
2. **DubboApi中使用try-catch**（全局异常处理器会自动处理）
3. **DubboApi中写业务逻辑**（查询条件构建、业务判断等应该在Service层）
4. **ResponseResult不带泛型**
5. **Mapper接口加@Mapper注解**
6. **启动类加@EnableDubbo、@MapperScan**
7. **创建common包、utils包**（已有独立仓库）
8. **Entity包路径错误**（必须在 `xxx.api.entity`，不是 `xxx.entity`）
9. **随意使用Redis缓存**（必须满足使用条件）

### ✅ 必须做
1. **实体类**：继承BusinessEntity + @TableName + LocalDateTime字段@JsonFormat
2. **返回值**：ResponseResult<T>（必须带泛型）
3. **分页查询**：调用startDubboPage()
4. **参数校验**：Preconditions（简单参数）或 ValidateUtil.validate()（复杂对象）
5. **Service事务**：@Transactional(rollbackFor = Exception.class)
6. **DubboApi职责**：只做参数校验、调用Service、记录日志、返回结果
7. **关键操作**：添加日志（@Slf4j + log.info）
8. **代码提交前**：mvn spring-javaformat:apply

## 📚 推荐工具类

| 用途 | 推荐类 |
|------|--------|
| 字符串 | `org.apache.commons.lang3.StringUtils` |
| 日期 | `cn.hutool.core.date.DateUtil` |
| 集合 | `com.google.common.collect.*` |
| 参数校验 | `com.google.common.base.Preconditions` |
| 对象校验 | `cn.city.parking.common.core.utils.ValidateUtil` |
| Redis | `cn.city.parking.common.redis.RedisUtils` |
| 分布式锁 | `cn.city.parking.common.redis.service.Locker` |
| 防重复提交 | `@NoRepeatSubmit` |

## 🔄 配置更新

### 更新全局配置
```bash
# 1. 拉取最新配置
cd /path/to/city-parking-claude-doc
git pull

# 2. 更新到全局目录
cp -r global-settings/.claude/* ~/.claude/
```

### 更新项目配置
```bash
# 只更新核心配置文件
cp global-settings/.claude/CLAUDE.md /path/to/project/.claude/
```

## 📖 延伸阅读

- [CLAUDE.md 完整规范](global-settings/.claude/CLAUDE.md)
- [Common组件架构详解](global-settings/.claude/docs/architecture/common-components-architecture.md)
- [编码前检查清单](global-settings/.claude/docs/guides/pre-coding-checklist.md)
- [SOLID设计原则](global-settings/.claude/docs/guides/solid-principles.md)
- [项目模板说明](../project-templates/README.md)

## 📞 问题反馈

配置问题或改进建议，请联系架构组。

## 📝 注意事项

- **全局配置**：会对所有项目生效
- **项目级配置**：项目根目录的 `.claude/CLAUDE.md` 会覆盖全局配置
- **配置优先级**：项目级 > 全局级
- **定期更新**：建议定期更新配置以保持与团队最新规范同步
- **settings.local.json**：本地设置文件，包含个人偏好配置，复制到新项目时应删除

---

**最后更新**: 2025-01-13
**框架版本**: City Parking 2.0.0-SNAPSHOT
**配置版本**: v2.0
