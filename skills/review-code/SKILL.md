---
name: review-code
description: 代码审查清单，用于开发完成后的自测和提测前审查。检查代码质量、安全性、性能、可维护性，确保符合框架规范和业界标准。适用于提测前自查、代码评审、质量把控等场景。
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash
context: fork
agent: Explore
---

# 代码审查清单

> **使用场景**：开发完成自测后、提测前的代码审查
> **审查原则**：代码质量、安全性、性能、可维护性达到业界标准

## 使用方式

```bash
# 审查当前分支的所有修改
/review-code

# 审查指定文件
/review-code src/main/java/cn/city/parking/xxx/service/UserServiceImpl.java

# 审查指定目录
/review-code src/main/java/cn/city/parking/xxx/
```

## 审查流程

### 第一步：识别修改范围

使用 Git 识别当前分支相对于 master 的修改：

```bash
# 查看修改的文件列表
git diff --name-only master...HEAD

# 查看详细修改内容
git diff master...HEAD
```

### 第二步：执行审查清单

按照以下清单逐项检查代码：

## 📋 审查清单

### 一、Spring Java Format 代码风格

#### 1.1 基础格式规范

- [ ] 使用 Tab 缩进（等同于 4 个空格），不混用 Tab 和空格
- [ ] 操作符两侧有空格：`a + b`，`x > 0`
- [ ] 关键字后有空格：`if (condition)`，`for (int i = 0; i < 10; i++)`
- [ ] 方法名和左括号之间无空格：`method()`
- [ ] 括号内侧无空格：`(a + b)`，不是 `( a + b )`
- [ ] 每行不超过 120 字符
- [ ] 左大括号不换行（K&R 风格）
- [ ] 单行语句也必须使用大括号

**检查命令**：
```bash
# 运行代码格式化检查
mvn spring-javaformat:validate
```

**修复命令**：
```bash
# 自动格式化代码
mvn spring-javaformat:apply
```

### 二、核心框架规范

#### 2.1 微服务分层架构 ⚠️

**核心约束**：下游服务禁止对外暴露 HTTP 接口，只能通过 BFF 层对外提供服务。

- [ ] **下游服务**（非 BFF）禁止使用 `@RestController`
- [ ] **下游服务**只能提供 `@DubboService` 接口
- [ ] **BFF 层**可以使用 `@RestController` 对外暴露 HTTP 接口
- [ ] 服务间通信必须通过 Dubbo RPC

**检查命令**：
```bash
# 检查下游服务是否有 Controller（应该为空）
grep -r "@RestController" city-parking-rbac-server/src/ || echo "✅ 通过"
grep -r "@Controller" city-parking-eop-server/src/ || echo "✅ 通过"
```

#### 2.2 实体类规范

- [ ] 继承 `BusinessEntity`
- [ ] 使用 `@TableName` 指定表名
- [ ] 使用 `@Schema` 注解（不用 @ApiModelProperty）
- [ ] 日期字段添加 `@JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")`
- [ ] Entity 包路径在 `xxx.api.entity` 下（不是 `xxx.entity`）
- [ ] 如果数据库有 create_by、update_by、del_flag、revision 字段，必须在实体类中显式声明

**检查命令**：
```bash
# 检查 Entity 是否继承 BusinessEntity
grep -r "class.*extends BusinessEntity" --include="*.java"

# 检查 Entity 包路径是否正确
find . -name "*.java" -path "*/entity/*" ! -path "*/api/entity/*"
```

#### 2.3 DubboApi/Controller 规范

- [ ] DubboApi 继承 `cn.city.parking.common.dubbo.filter.base.BaseDubboApi`
- [ ] 返回值使用 `ResponseResult<T>` 带泛型
- [ ] 分页查询调用 `startDubboPage()`
- [ ] **保持薄层**：只负责参数校验、调用 Service、返回结果
- [ ] ❌ 不要在 DubboApi/Controller 中写业务逻辑（查询条件构建、缓存处理、循环处理等）

**检查命令**：
```bash
# 检查 DubboApi 是否继承 BaseDubboApi
grep -r "class.*DubboApiImpl extends BaseDubboApi" --include="*.java"

# 检查是否有错误的包路径
grep -r "import cn.city.parking.common.auth.base.BaseDubboApi" --include="*.java"
```

#### 2.4 Service 规范

- [ ] Service 接口继承 `IService<T>`
- [ ] Service 实现继承 `ServiceImpl<Mapper, Entity>`
- [ ] 增删改方法添加 `@Transactional(rollbackFor = Exception.class)`
- [ ] 业务逻辑、缓存逻辑都在 Service 层

**检查命令**：
```bash
# 检查 Service 是否继承 IService
grep -r "interface.*Service extends IService" --include="*.java"

# 检查事务注解
grep -r "@Transactional" --include="*ServiceImpl.java"
```

#### 2.5 Mapper 规范

- [ ] Mapper 继承 `CommonMapper<T>`，事实源见 `rules/java-mapper-rule.md`
- [ ] 不需要 `@Mapper` 注解（框架已自动扫描）
- [ ] 使用框架提供的批量方法：`insertBatchSomeColumn`

**检查命令**：
```bash
# 检查是否有多余的 @Mapper 注解
grep -r "@Mapper" --include="*Mapper.java"
```

### 三、代码质量检查（Clean Code）

#### 3.1 命名规范

- [ ] 类名：大驼峰（PascalCase）
- [ ] 方法名/变量名：小驼峰（camelCase）
- [ ] 常量：全大写下划线（UPPER_SNAKE_CASE）
- [ ] 包名：全小写，不使用下划线
- [ ] 布尔变量：is/has/can 开头

#### 3.2 方法规范

- [ ] 方法长度不超过 50 行
- [ ] 方法参数不超过 5 个
- [ ] 避免嵌套超过 3 层
- [ ] 单一职责：一个方法只做一件事

#### 3.3 注释规范

- [ ] 公共方法必须有 JavaDoc 注释
- [ ] 复杂逻辑必须有行内注释
- [ ] 修改代码添加 update-begin/update-end 注释

**示例**：
```java
//update-begin---author:yourname ---date:20260123  for：[需求编号]功能描述------------
// 修改的代码
//update-end---author:yourname ---date:20260123  for：[需求编号]功能描述--------------
```

### 四、安全规范检查（OWASP）

#### 4.1 SQL 注入防护

- [ ] 使用 `#{}` 而非 `${}`（除非必要）
- [ ] 动态 SQL 使用 MyBatis 的 `<if>` 标签
- [ ] 避免字符串拼接 SQL

#### 4.2 XSS 防护

- [ ] 用户输入进行 HTML 转义
- [ ] 富文本使用白名单过滤

#### 4.3 敏感信息保护

- [ ] 密码使用加密存储（BCrypt）
- [ ] 日志中不输出敏感信息（密码、身份证、银行卡）
- [ ] 敏感数据传输使用 HTTPS

#### 4.4 权限控制

- [ ] 接口添加权限校验
- [ ] 数据权限使用 `@MyDataScope` 注解
- [ ] 避免越权访问

### 五、性能优化检查

#### 5.1 数据库查询

- [ ] 所有列表查询必须分页
- [ ] 避免 SELECT *，只查询需要的字段
- [ ] 避免 N+1 查询
- [ ] IN 条件不超过 500 个
- [ ] 批量操作控制在 1000 条以内

**检查命令**：
```bash
# 检查是否有 SELECT *
grep -r "select \*" --include="*.xml"

# 检查是否有未分页的列表查询
grep -r "selectList" --include="*Mapper.xml" -A 5 | grep -v "limit"
```

#### 5.2 缓存使用

- [ ] 缓存使用符合条件（查询频率 > 100 次/分钟，变更 < 10 次/天）
- [ ] 缓存更新策略：先更新数据库，再删除缓存
- [ ] 避免缓存穿透、击穿、雪崩

**检查命令**：
```bash
# 检查缓存使用
grep -r "RedisUtils" --include="*.java"
```

#### 5.3 异步处理

- [ ] 耗时操作使用异步处理
- [ ] 使用框架提供的线程池（ttlExecutorService、userTaskThreadPool）
- [ ] 异步方法传递 MDC 上下文

### 六、测试规范检查

#### 6.1 单元测试

- [ ] 核心业务逻辑有单元测试
- [ ] 测试覆盖率符合 `config/quality-thresholds.yaml`
- [ ] 测试用例包含正常、异常、边界情况

#### 6.2 集成测试

- [ ] 关键接口有集成测试
- [ ] 测试数据使用 test_ 前缀

### 七、代码评审建议

#### 7.1 设计模式

- [ ] 合理使用设计模式（策略、工厂、模板方法等）
- [ ] 避免过度设计

#### 7.2 可扩展性

- [ ] 新增功能优先扩展而非修改
- [ ] 使用接口而非实现类

#### 7.3 可维护性

- [ ] 避免魔法数字，使用常量
- [ ] 避免重复代码，提取公共方法
- [ ] 代码结构清晰，易于理解

## 审查报告模板

审查完成后，生成以下格式的报告：

```markdown
# 代码审查报告

**审查时间**：{时间}
**审查人员**：Claude Code
**审查范围**：{分支名} 相对于 master 的修改

---

## 审查概览

| 项目 | 结果 |
|------|------|
| 修改文件数 | {数量} |
| 新增代码行数 | {数量} |
| 删除代码行数 | {数量} |
| 发现问题数 | {数量} |
| 严重问题 | {数量} |
| 一般问题 | {数量} |
| 建议优化 | {数量} |

---

## 问题清单

### 严重问题（必须修复）

1. **问题描述**：{描述}
   - **位置**：{文件}:{行号}
   - **原因**：{原因}
   - **修复建议**：{建议}

### 一般问题（建议修复）

1. **问题描述**：{描述}
   - **位置**：{文件}:{行号}
   - **原因**：{原因}
   - **修复建议**：{建议}

### 优化建议

1. **建议描述**：{描述}
   - **位置**：{文件}:{行号}
   - **优化方向**：{方向}

---

## 审查结论

- ✅ 代码质量：{良好/一般/较差}
- ✅ 安全性：{良好/一般/较差}
- ✅ 性能：{良好/一般/较差}
- ✅ 可维护性：{良好/一般/较差}

**总体评价**：{评价}

**是否可以提测**：{是/否}

---

**生成工具**：Claude Code Review-Code Skill
**报告版本**：1.0
```

## 常见问题检查

### 1. 架构问题

- [ ] 下游服务是否有 @RestController（应该没有）
- [ ] Entity 包路径是否正确（必须在 api.entity 下）
- [ ] DubboApi 是否继承正确的 BaseDubboApi

### 2. 依赖问题

- [ ] API 模块是否依赖 common-auth（不是 common-core）
- [ ] Server 模块是否有冗余依赖（Redis、Auth、MySQL、Druid）

### 3. 配置问题

- [ ] bootstrap.yml 占位符是否正确（@profileActive@、${nacos.*}）
- [ ] 是否创建了 4 个配置文件（bootstrap.yml + dev/prod/test）

### 4. 代码规范问题

- [ ] 是否有 try-catch 捕获 BusinessException（不应该有）
- [ ] 是否忘记 ResponseResult 泛型
- [ ] 是否忘记 @TableName、@JsonFormat、@Transactional

## 参考文档

- [编码前检查清单](../../../docs/guides/pre-coding-checklist.md)
- [框架功能详解](../../../docs/guides/framework-features.md)
- [SOLID 设计原则](../../../docs/guides/solid-principles.md)
- [详细规范说明](../../../docs/guides/detailed-standards.md)

---

**版本**：1.0.0
**更新日期**：2026-01-23
