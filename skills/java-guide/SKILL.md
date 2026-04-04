---
name: java-guide
description: City Parking Java 微服务开发规范。当检测到 Java 项目（pom.xml、*.java 文件、bootstrap.yml）或用户询问 Spring Boot、Dubbo、Nacos、MyBatis Plus 相关问题时自动加载。包含架构规范、编码规范、配置规范、开发流程。适用于创建实体类、编写 Service、实现 DubboApi、配置 Maven、新建微服务项目等场景。
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob
context: inline
---

# City Parking Java 微服务开发规范

> 本规范适用于 City Parking 微服务框架（Spring Boot + Dubbo + Nacos）

## 🎯 自动触发条件

本规范会在以下情况自动加载：

### 文件检测
- 检测到 `pom.xml` 文件
- 检测到 `*.java` 文件
- 检测到 `bootstrap.yml` 或 `bootstrap-*.yml` 文件

### 技术栈关键词
- Spring Boot、Spring Cloud Alibaba
- Dubbo、DubboService、DubboReference
- Nacos、注册中心、配置中心
- MyBatis Plus、BaseMapper
- Redis、Lettuce

### 操作关键词
- 创建实体类、新建 Entity
- 编写 Service、实现 ServiceImpl
- 实现 DubboApi、创建 Controller
- 配置 Maven、配置 POM
- 新建微服务项目、创建 CRUD 功能

## 📚 规范文档导航

本规范包含以下模块，Claude 会根据你的问题自动加载相关内容：

### 1. [架构规范](architecture.md)
- 技术栈说明（Spring Boot、Dubbo、Nacos）
- Maven 模块结构（API 模块、Server 模块）
- BFF 分层架构（下游服务禁止暴露 HTTP 接口）
- 服务分层说明（DubboApi → Service → Mapper → 数据库）

### 2. [编码规范](coding-standards.md)
- 13 条核心规范详细说明
- 实体类规范（BusinessEntity、@TableName、字段填充）
- DubboApi/Controller 规范（薄层原则、职责边界）
- Service 规范（继承 IService、事务控制）
- Mapper 规范（继承 BaseMapper、批量操作）
- 启动类规范（必需注解、可选注解）
- 日志规范（日志级别、敏感信息脱敏）
- Redis 使用规范（缓存策略、分布式锁）
- 代码风格规范（Spring Java Format）

### 3. [配置规范](configuration.md)
- POM 配置（根 POM、API 模块、Server 模块）
- YAML 配置（bootstrap.yml、环境配置）
- 数据库规范（必备字段、可选字段）
- Maven 私库发布策略

### 4. [开发流程](development-workflow.md)
- 新建微服务项目完整步骤
- 新建 CRUD 功能步骤
- 标准方法命名规范
- 验证清单

### 5. [快速参考](quick-reference.md)
- 常见错误对照表
- 快速决策指南（何时使用缓存、分布式锁、事务）
- 重要提醒（绝对不要做的事、必须做的事）
- 推荐工具类

## 🚀 快速开始

### 何时使用本规范

✅ **适用场景**：
- 创建新的微服务项目
- 编写 Entity、Service、DubboApi 代码
- 配置 Maven、YAML 文件
- 遇到框架相关问题
- 代码审查和规范检查

❌ **不适用场景**：
- 非 Java 项目
- 非 City Parking 框架项目
- 纯算法或工具类开发

### 核心原则（必读）

#### 1. DubboApi/Controller 保持薄层
- ✅ **只负责 4 件事**：参数校验 → 调用 Service → 记录日志 → 返回结果
- ❌ **绝对不允许**：复杂业务判断、查询条件构建、直接调用 Mapper、循环处理数据

#### 2. 下游服务禁止暴露 HTTP 接口
- ✅ **BFF 层**（city-parking-bff-*）：允许使用 `@RestController`
- ❌ **下游服务**：禁止使用 `@RestController`，只能提供 `@DubboService`

#### 3. Entity 必须在 api.entity 包下
- ✅ **正确路径**：`cn.city.parking.xxx.api.entity`
- ❌ **错误路径**��`cn.city.parking.xxx.entity`（缺少 api 层级）

#### 4. 所有增删改操作必须加事务
- ✅ **正确写法**：`@Transactional(rollbackFor = Exception.class)`
- ❌ **错误写法**：`@Transactional`（未指定 rollbackFor）

#### 5. 实体类字段显式声明
- BusinessEntity 只包含 3 个字段：id、createTime、updateTime
- 如果数据库有 create_by、update_by、del_flag、revision 字段，**必须在实体类中显式声明**

## 📖 使用方式

### 自动加载（推荐）
当你在 Java 项目中工作时，Claude 会自动加载本规范，无需手动操作。

### 手动查看
如果需要查看完整规范，可以：
- 输入 `/java-guide` 查看本总览
- 询问具体问题，Claude 会自动加载相关规范文档

### 与其他 Skills 配合
本规范会与以下 skills 自动配合使用：
- `/new-crud` - 创建 CRUD 功能时自动应用规范
- `/add-field` - 添加字段时自动应用规范
- `/new-api` - 新增接口时自动应用规范
- `/review-code` - 代码审查时作为审查标准
- `/diff-report` - 生成修改报告时检查规范遵循情况

## ⚠️ 重要提醒

### 绝对不要做的事
1. **不要创建**：common 包、utils 包、BusinessException、ResponseResult（已有独立仓库）
2. **不要使用错误路径**：`cn.city.parking.common.auth.base.BaseDubboApi`（已废弃）
3. **下游服务禁止使用 `@RestController`**：只有 BFF 层可以暴露 HTTP 接口
4. **Entity 包路径错误**：必须在 `xxx.api.entity` 下，不是 `xxx.entity`
5. **不要随意使用 Redis 缓存**：如无必要，不要缓存

### 必须做的事
1. **实体类**：继承 BusinessEntity + @TableName + LocalDateTime 字段 @JsonFormat
2. **配置文件**：必须创建 4 个文件（bootstrap.yml + bootstrap-dev/prod/test.yml）
3. **Service 接口**：继承 IService<T>
4. **Service 实现**：增删改方法 @Transactional(rollbackFor = Exception.class)
5. **DubboApi**：返回 ResponseResult<T> 带泛型 + 分页调用 startDubboPage()

## 📞 获取帮助

如果遇到问题：
1. 查看对应的规范文档（Claude 会自动引导）
2. 查看完整案例（docs/examples/ 目录）
3. 联系架构组获取支持

---

**规范版本**：1.0
**最后更新**：2026-01-24
**适用框架**：City Parking 微服务框架 v2.0.0
