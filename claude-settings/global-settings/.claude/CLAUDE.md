# CLAUDE-gen.md

本文件为 Claude Code 提供**全局通用**的开发规约和规则。

> **重要说明**: 本文件仅包含通用的编码规范、最佳实践和开发约定，不包含业务相关指南。

---

## 核心开发原则

### 代码修改原则
- **最小化修改**: 最小范围修改，避免不必要的变更
- **保持风格一致**: 遵循现有代码风格，不引入新编码风格
- **保留注释**: 如非必要，不删除和修改已有注释
- **向后兼容**: 除非明确要求，避免破坏性修改
- **只做需要的**: 不过度优化或重构未要求修改的代码

### 代码质量原则
- **可读性优先**: 清晰易懂优于炫技
- **命名规范**: 有意义的、描述性的命名
- **单一职责**: 每个方法只做一件事
- **避免重复**: DRY 原则
- **异常处理**: 合理处理，不吞掉异常
- **日志记录**: 关键操作和异常情况需记录

### 安全原则
- **输入验证**: 对所有外部输入验证
- **SQL注入防护**: 使用参数化查询
- **XSS防护**: 对用户输入转义和过滤
- **敏感信息保护**: 不硬编码密码、密钥
- **权限控制**: 严格的权限验证

---

## Java 开发规范

### 命名规范
- **类名**: PascalCase (`UserService`, `OrderController`)
- **接口**: `UserServicei`, `UserMapper`
- **方法**: camelCase (`getUserById`, `isValid`)
- **变量**: camelCase (`userName`, `pageSize`)
- **常量**: UPPER_SNAKE_CASE (`DEFAULT_ENCODING`, `MAX_RETRY_COUNT`)
- **布尔方法**: is/has/can 前缀

### 注释规范
```java
/**
 * 类/方法说明
 * @param userId 用户ID
 * @return 用户信息
 * @author yourname
 * @date 2025-01-10 14:30
 */

//update-begin---author:yourname ---date:20250110  for：[需求编号]功能描述------------
// 修改的代码
//update-end---author:yourname ---date:20250110  for：[需求编号]功能描述--------------
```

### 代码格式
- 4个空格缩进，不用Tab
- 左大括号不换行，右大括号换行
- 单行语句也要加大括号
- 运算符两侧加空格
- 逗号后加空格

### 类成员顺序
1. 静态常量
2. 静态变量
3. 实例变量
4. 构造方法
5. 静态方法
6. 公共方法
7. 保护方法
8. 私有方法
9. getter/setter

### 方法规范
- 单个方法不超过50行（建议）
- 参数不超过5个（建议）
- 超过限制考虑拆分或封装对象

### 异常处理
```java
// 错误：吞掉异常
try { doSomething(); } catch (Exception e) { }

// 正确：记录并抛出
try {
    doSomething();
} catch (Exception e) {
    log.error("操作失败", e);
    throw new BusinessException("操作失败", e);
}

// 推荐：try-with-resources
try (InputStream is = new FileInputStream(file)) {
    // 操作
}
```

### 空值处理
```java
// 使用Optional
public Optional<User> findUser(String id) {
    return Optional.ofNullable(userMap.get(id));
}

// 参数校验
Objects.requireNonNull(user, "用户不能为空");

// 字符串/集合判空
if (StringUtils.isBlank(str)) { }
if (CollectionUtils.isEmpty(list)) { }
```

### 日志规范
```java
// 错误：字符串拼接
log.info("用户登录: " + userName);

// 正确：参数化
log.info("用户登录: {}, 时间: {}", userName, loginTime);

// 级别：debug/info/warn/error
// 敏感信息需脱敏
```

---

## 数据库开发规范

### SQL编写
- 关键字大写
- 适当缩进
- 复杂查询分行

### MyBatis Mapper
- 使用 resultMap 映射
- 抽取通用 SQL 片段
- 动态 SQL 使用 `<where>`, `<if>`

### 字段命名
- 小写字母，下划线分隔 (snake_case)
- 主键: `表名_id` 或 `id`
- 外键: `关联表名_id`
- 布尔: `is_` 前缀
- 时间: `_time` 后缀

---

## Spring Boot 开发规范

### 依赖注入
```java
// 推荐：构造器注入
@Service
public class UserServiceImpl {
    private final UserMapper userMapper;

    public UserServiceImpl(UserMapper userMapper) {
        this.userMapper = userMapper;
    }
}

// 常用：字段注入
@Autowired
private UserMapper userMapper;
```

### Controller
```java
@RestController
@RequestMapping("/api/user")
public class UserController {
    @GetMapping("/{userId}")
    public Result<User> getUser(@PathVariable String userId) {
        return Result.success(userService.getUserById(userId));
    }

    @PostMapping
    public Result<Void> createUser(@RequestBody @Valid UserDTO dto) {
        userService.createUser(dto);
        return Result.success();
    }
}
```

### Service
```java
@Service
public class UserServiceImpl {
    @Override
    @Transactional(rollbackFor = Exception.class)
    public void createUser(UserDTO dto) {
        validateUser(dto);
        User user = convertToEntity(dto);
        userMapper.insert(user);
        log.info("创建用户成功: {}", user.getUserId());
    }
}
```

---

## 前端开发规范（Vue/TypeScript）

### 命名规范
- 文件: kebab-case (`user-list.vue`)
- 组件: PascalCase (`UserList`)
- 变量: camelCase (`userName`)
- 常量: UPPER_SNAKE_CASE (`API_BASE_URL`)
- 类型/接口: PascalCase (`UserInfo`)

### TypeScript
```typescript
// 定义接口
interface User {
  userId: string;
  userName: string;
  email?: string;  // 可选
}

// 类型别名
type UserStatus = 'active' | 'inactive';

// 避免any，使用unknown或具体类型
function processData(data: unknown) {
  if (typeof data === 'string') {
    console.log(data.toUpperCase());
  }
}
```

---

## Git提交规范

### 提交格式
```
<type>(<scope>): <subject>
```

### Type类型
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具变动

### 示例
```bash
git commit -m "feat(user): 添加用户登录功能"
git commit -m "fix(order): 修复订单计算错误"
git commit -m "docs(readme): 更新安装说明"
```

---

## 测试规范

### 单元测试
```java
@Test
void testGetUserById() {
    // Given
    String userId = "123";

    // When
    User user = userService.getUserById(userId);

    // Then
    assertNotNull(user);
    assertEquals(userId, user.getUserId());
}
```

### 命名规范
- `test + 被测方法名 + 测试场景 + 期望结果`
- 使用 Given-When-Then 模式
- 一个测试方法只测一个场景

---

## 性能优化要点

### 数据库
- 使用索引优化查询
- 避免 N+1 查询
- 使用分页
- 避免循环中执行数据库操作
- 合理使用缓存

### 代码
- 避免过度使用反射
- 合理使用线程池
- 避免循环中创建对象
- 使用 StringBuilder 拼接字符串
- 及时关闭资源

---

## 文档维护规范

### 核心原则
代码会过期，文档也会过期。**保持文档与代码同步是开发者的重要职责**。

### 何时必须更新文档

**业务逻辑变更**:
- 修改业务流程 → 更新流程图和说明
- 修改计算逻辑 → 更新计算规则文档
- 新增业务场景 → 补充场景说明
- 修复业务bug → 记录到"常见陷阱"

**代码结构变更**:
- 方法重命名/移动 → 更新方法索引和代码位置
- 类重构 → 更新类图和依赖关系
- 参数修改 → 更新方法签名说明

**配置和规则变更**:
- 新增配置项 → 更新配置说明文档
- 修改默认值 → 更新配置示例
- 新增业务规则 → 补充规则文档

**发现新知识**:
- 发现代码陷阱 → 记录到最佳实践
- 优化方案 → 补充到优化建议
- 调试技巧 → 添加到调试指南

### 文档类型与更新时机

#### CLAUDE.md（项目级）
- 新增/删除模块
- 技术栈升级
- 架构调整
- 部署方式变更

#### CLAUDE-gen.md（规范级）
- 制定新编码规范
- 引入新开发工具
- 更新安全规范
- 调整测试策略

#### Skills 文档（业务级）
- 业务逻辑变更
- 方法签名修改
- 发现新业务场景
- 修复已知问题

### 提交前检查清单

**业务代码修改**:
- [ ] 更新相关 skill reference 文档
- [ ] 更新流程图
- [ ] 更新方法位置索引
- [ ] 记录新注意事项

**配置修改**:
- [ ] 更新配置项说明
- [ ] 更新示例代码
- [ ] 更新默认值说明

**架构调整**:
- [ ] 更新 CLAUDE.md 架构说明
- [ ] 更新模块依赖关系
- [ ] 更新部署说明

**规范调整**:
- [ ] 更新 CLAUDE-gen.md
- [ ] 更新示例代码
- [ ] 更新检查清单

### 文档质量标准

**必须达到**:
1. 准确性：文档与代码完全一致
2. 完整性：覆盖所有关键场景
3. 可用性：能够指导实际开发
4. 时效性：与最新代码同步

**良好文档特征**:
- ✅ 新人能快速上手
- ✅ 能回答90%常见问题
- ✅ 包含足够示例
- ✅ 流程图与代码一致
- ✅ 方法位置准确

**需要改进信号**:
- ❌ 代码示例无法运行
- ❌ 方法位置不符
- ❌ 流程图与逻辑不一致
- ❌ 缺少关键场景说明
- ❌ 更新日期超过3个月

### 维护工作流
```
代码修改 → 检查影响 → 更新文档 → 验证准确 → 提交
```

---

## 常用工具类

- `StringUtils.isBlank()` - 判断字符串空
- `CollectionUtils.isEmpty()` - 判断集合空
- `DateUtil.format()` - 格式化日期
- `JSONObject.toJSONString()` - 对象转JSON

---

## 代码审查清单

**功能性**: 实现需求、边界处理、异常处理
**可读性**: 命名清晰、逻辑清晰、必要注释
**性能**: 无性能问题、资源正确释放
**安全性**: 无安全漏洞、输入验证、敏感信息保护
**可维护性**: 易于维护、遵循规范、无重复代码

---

## 常见问题

1. **并发问题**: 分布式锁、乐观锁、悲观锁
2. **大数据量**: 分页、流式处理、异步处理
3. **接口性能**: 减少查询、使用缓存、异步处理、索引优化
4. **数据一致性**: 事务、分布式事务(Seata)、最终一致性

---

**说明**:
1. `@author` 和 `@date` 字段使用实际开发者和修改日期
2. 具体项目可能有特殊规范，以实际为准
3. 本文档持续更新，请定期查看
