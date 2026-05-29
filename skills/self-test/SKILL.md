---
name: self-test
description: 自动化测试 Java 后端代码，支持自动组装请求参数、调用接口、验证结果。如果待测试方法没有对应的 HTTP 接口，自动生成测试接口并提示重启项目。适用于开发完成后的功能自测、Service 层方法验证、DubboApi 方法测试。
argument-hint: [类名.方法名] [--需求描述]
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Java 后端自动化自测

自动化测试 Java 后端代码，支持自动组装请求参数、调用接口、验证结果。如果待测试方法没有对应的 HTTP 接口，自动生成测试接口并重启项目。

## 使用方式

```bash
# 测试指定方法
/self-test UserService.insertUser

# 测试指定方法并提供需求描述
/self-test UserService.insertUser --需求：用户名长度必须在3-20个字符之间，邮箱必须是有效格式

# 测试当前打开的文件中的方法
/self-test

# 批量测试整个 Service 类
/self-test UserService --all
```

## 执行流程

### 第一步：识别待测试目标

1. **如果指定了方法路径**（如 `UserService.insertUser`）：
   - 解析类名和方法名
   - 使用 Glob 查找对应的实现类文件
   - 读取文件内容，定位到具体方法

2. **如果未指定方法路径**：
   - 分析当前打开的文件
   - 识别所有公共方法（public 方法）
   - 提示用户选择要测试的方法

3. **支持的测试目标**：
   - Service 层方法（`IUserService.insertUser`）
   - DubboApi 实现方法（`UserDubboApiImpl.getInfo`）
   - Mapper 方法（需要通过 Service 层调用）

### 第二步：检查是否存在测试接口

1. **对于 Service 层方法**：
   - 检查是否有对应的 DubboApi 接口
   - 检查是否有对应的 Controller（BFF 层）
   - 检查是否已存在测试 Controller

2. **对于 DubboApi 方法**：
   - 检查是否有对应的 HTTP 接口（BFF 层）
   - 检查是否已存在测试 Controller

3. **检查策略**：
   - 使用 Grep 搜索 `@RestController` 和 `@RequestMapping`
   - 匹配方法名和参数类型
   - 检查 `src/test/java` 目录下是否有测试接口

### 第三步：自动生成测试接口（如需要）

如果不存在测试接口，自动生成临时测试 Controller：

**生成位置**：`src/test/java/{package}/test/controller/TestController.java`

**生成规范**：
```java
package cn.city.parking.xxx.test.controller;

import cn.city.parking.common.core.web.domain.ResponseResult;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Profile;
import org.springframework.web.bind.annotation.*;

/**
 * 自动生成的测试接口
 * 仅用于开发环境自测，生产环境禁用
 *
 * @author Claude Code Self-Test
 * @date {当前日期}
 */
@Slf4j
@RestController
@RequestMapping("/test")
@Profile({"dev", "test"})  // 仅在开发和测试环境启用
public class TestController {

    @Autowired
    private IUserService userService;

    /**
     * 测试用户插入功能
     * 自动生成的测试接口
     */
    @PostMapping("/user/insert")
    public ResponseResult<Integer> testInsertUser(@RequestBody User user) {
        log.info("[自测] 测试插入用户，参数：{}", user);
        int rows = userService.insertUser(user);
        log.info("[自测] 插入结果：{}", rows);
        return ResponseResult.success(rows);
    }
}
```

**注意事项**：
- 测试接口仅在 dev/test 环境启用（使用 `@Profile`）
- 接口路径统一使用 `/test` 前缀
- 添加详细的日志记录
- 生成后提示用户重启项目

### 第四步：组装测试数据

根据方法签名和业务逻辑，自动生成测试数据：

**数据生成策略**：

1. **基本类型**：
   - `String`: 根据字段名生成（如 `username` → `"test_user_001"`）
   - `Integer/Long`: 使用正数（如 `1`, `100`）
   - `Boolean`: 根据业务逻辑判断（默认 `true`）
   - `Date/LocalDateTime`: 使用当前时间

2. **实体对象**：分析实体类的校验注解
   - `@NotBlank`: 生成非空字符串
   - `@Size(min=x, max=y)`: 生成符合长度的字符串
   - `@Email`: 生成邮箱格式（`test{序号}@example.com`）
   - `@Pattern`: 根据正则生成
   - `@Min/@Max`: 生成符合范围的数值

3. **复杂对象**：递归生成嵌套对象

4. **集合类型**：生成包含 1-3 个元素的集合

**示例测试数据**：
```json
{
  "username": "test_user_001",
  "email": "test001@example.com",
  "phone": "13800138000",
  "age": 25,
  "status": 1,
  "createTime": "2026-01-23 10:30:00"
}
```

**生成多个测试用例**：
- **正常用例**：所有字段符合要求
- **边界用例**：测试字段的最小值、最大值
- **异常用例**：测试参数校验（空值、格式错误等）

### 第五步：执行测试

使用 HTTP 客户端调用接口：

**执行步骤**：

1. **检查服务是否启动**：
   ```bash
   # 检查端口是否监听
   netstat -ano | findstr :{port}
   ```

2. **如果服务未启动或需要重启**：
   - 提示用户启动服务
   - 提供启动命令：`mvn spring-boot:run` 或 `java -jar xxx.jar`
   - 等待用户确认服务已启动

3. **发送 HTTP 请求**：
   ```bash
   curl -X POST http://localhost:{port}/test/user/insert \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer {token}" \
     -d '{测试数据}'
   ```

4. **记录请求和响应**：
   - 记录请求 URL、Headers、Body
   - 记录响应状态码、Headers、Body
   - 记录执行时间

5. **捕获异常**：
   - 网络异常（连接失败、超时）
   - HTTP 异常（4xx、5xx）
   - 业务异常（code != 200）

### 第六步：验证结果

根据业务需求和方法返回值，自动验证结果：

**验证规则**：

1. **HTTP 状态码**：检查是否为 200
2. **响应结构**：检查 ResponseResult 结构（code、message、data）
3. **业务状态码**：检查 code 是否为 200（成功）
4. **返回数据**：验证 data 字段
   - 插入操作：`rows > 0`
   - 查询操作：`data != null`
   - 更新操作：`rows > 0`
   - 删除操作：`rows > 0`
   - 分页查询：`data.list != null && data.total >= 0`

5. **数据库验证**（可选）：
   - 查询数据库确认数据是否正确插入/更新/删除
   - 验证字段值是否符合预期

**验证示例**：
```java
// 验证插入操作
assert response.getCode() == 200;
assert response.getData() > 0;

// 验证查询操作
assert response.getCode() == 200;
assert response.getData() != null;
assert response.getData().getUsername().equals("test_user_001");

// 验证参数校验
assert response.getCode() == 500;
assert response.getMessage().contains("用户名不能为空");
```

### 第七步：生成测试报告

生成详细的测试报告，保存到项目根目录：

**报告路径**：`TEST_REPORT_{timestamp}.md`

**报告内容**：
```markdown
# 自动化测试报告

**测试时间**：2026-01-23 10:30:00
**测试目标**：UserService.insertUser
**测试环境**：dev
**服务端口**：9220

---

## 测试概览

| 项目 | 结果 |
|------|------|
| 测试用例数 | 3 |
| 通过数 | 3 |
| 失败数 | 0 |
| 成功率 | 100% |

---

## 测试详情

### 用例1：正常插入用户

**请求参数**：
```json
{
  "username": "test_user_001",
  "email": "test001@example.com",
  "phone": "13800138000",
  "age": 25,
  "status": 1
}
```

**响应结果**：
```json
{
  "code": 200,
  "message": "操作成功",
  "data": 1
}
```

**验证结果**：✅ 通过
- HTTP 状态码：200
- 业务状态码：200
- 插入行数：1
- 执行时间：125ms

---

### 用例2：参数校验测试（用户名为空）

**请求参数**：
```json
{
  "username": "",
  "email": "test002@example.com"
}
```

**响应结果**：
```json
{
  "code": 500,
  "message": "用户名不能为空",
  "data": null
}
```

**验证结果**：✅ 通过
- 正确触发参数校验
- 返回预期错误信息

---

## 测试总结

### 通过的测试
- ✅ 正常插入用户
- ✅ 参数校验测试
- ✅ 重复用户名测试

### 失败的测试
无

### 建议
1. 所有测试用例均通过，功能正常
2. 参数校验工作正常
3. 建议补充边界值测试

---

**生成工具**：Claude Code Self-Test Skill
**报告版本**：1.0
```

## 高级功能

### 1. 批量测试

测试整个 Service 类的所有方法：
```bash
/self-test UserService --all
```

执行流程：
1. 识别 Service 类中的所有公共方法
2. 逐个生成测试用例
3. 执行所有测试
4. 生成汇总报告

### 2. 回归测试

重新执行之前的测试用例：
```bash
/self-test --regression
```

执行流程：
1. 读取之前的测试报告
2. 提取测试用例
3. 重新执行
4. 对比结果

### 3. 性能测试

测试接口性能（并发、响应时间）：
```bash
/self-test UserService.insertUser --performance --concurrent=10
```

执行流程：
1. 生成测试数据
2. 并发发送请求（10 个线程）
3. 统计响应时间（平均、最小、最大、P95、P99）
4. 生成性能报告

### 4. 数据库验证

测试后验证数据库数据：
```bash
/self-test UserService.insertUser --verify-db
```

执行流程：
1. 执行测试
2. 查询数据库确认数据
3. 验证字段值
4. 清理测试数据（可选）

## 配置选项

在项目根目录创建 `.claude-test.yml` 配置文件：

```yaml
# 自测配置
self-test:
  # 服务端口
  server-port: 9220

  # 测试接口路径前缀
  test-path-prefix: /test

  # 是否自动重启服务
  auto-restart: false

  # 是否自动清理测试数据
  auto-cleanup: true

  # 测试数据前缀
  test-data-prefix: test_

  # 测试用例数量
  test-case-count: 3

  # 是否验证数据库
  verify-database: false

  # 超时时间（秒）
  timeout: 30

  # 并发数（性能测试）
  concurrent: 10

  # 认证 Token（如需要）
  auth-token: ""
```

## 注意事项

### 1. 测试接口安全

- 测试接口仅在 dev/test 环境启用
- 生产环境自动禁用（通过 `@Profile` 注解）
- 测试接口路径统一使用 `/test` 前缀
- 建议在测试完成后删除测试接口

### 2. 数据清理

- 测试完成后，提示用户是否清理测试数据
- 支持自动回滚（使用事务）
- 避免污染数据库
- 测试数据使用 `test_` 前缀，便于识别

### 3. 服务重启

- 生成测试接口后，需要重启服务
- 提示用户重启命令
- 等待用户确认服务已启动
- 检查端口是否监听

### 4. 测试数据

- 测试数据使用 `test_` 前缀，便于识别
- 避免使用真实用户数据
- 敏感数据脱敏（密码、身份证、手机号）
- 根据校验注解生成合法数据

## 故障排查

### 问题1：服务未启动

**错误**：`Connection refused: connect`

**解决**：
1. 检查服务是否启动：`netstat -ano | findstr :9220`
2. 检查端口是否正确
3. 使用 `mvn spring-boot:run` 启动服务

### 问题2：接口404

**错误**：`404 Not Found`

**解决**：
1. 检查测试接口是否生成
2. 检查 `@Profile` 配置
3. 确认当前环境是 dev 或 test
4. 检查 `@RequestMapping` 路径

### 问题3：参数校验失败

**错误**：`参数校验失败`

**解决**：
1. 检查实体类的校验注解
2. 调整测试数据生成策略
3. 手动指定测试数据

### 问题4：认证失败

**错误**：`401 Unauthorized`

**解决**：
1. 检查是否需要认证 Token
2. 在配置文件中配置 `auth-token`
3. 或在测试接口中添加 `@IgnoreAuth` 注解

## 最佳实践

1. **开发完成后立即自测**：每完成一个功能，立即使用 `/self-test` 验证
2. **提交前回归测试**：提交代码前，执行 `/self-test --regression` 确保没有破坏现有功能
3. **结合代码审查**：配合 `/review-code` 使用，确保代码质量
4. **保留测试报告**：测试报告可作为功能验证的证据
5. **清理测试数据**：测试完成后及时清理测试数据
6. **删除测试接口**：测试完成后，删除临时生成的测试接口

## 与其他 Skill 的配合

- **`/new-crud`**：创建 CRUD 功能后，使用 `/self-test` 验证
- **`/add-field`**：添加字段后，使用 `/self-test` 验证相关功能
- **`/review-code`**：代码审查后，使用 `/self-test` 确保功能正常
- **`/generate-tests`**：生成单元测试后，使用 `/self-test` 进行集成测试
- **`/diff-report`**：生成修改报告后，使用 `/self-test` 验证修改是否正确

## 参数说明

- `$ARGUMENTS`：传递给 skill 的参数
  - 格式：`类名.方法名 [选项]`
  - 示例：`UserService.insertUser --需求：用户名长度必须在3-20个字符之间`

## 执行示例

### 示例1：测试指定方法

```bash
/self-test UserService.insertUser
```

**执行过程**：
1. 定位到 `UserServiceImpl.insertUser` 方法
2. 检查是否有对应接口（未找到）
3. 生成测试 Controller：`TestController.testInsertUser`
4. 提示用户重启项目
5. 生成 3 个测试用例（正常、异常、边界）
6. 执行测试并验证结果
7. 生成测试报告：`TEST_REPORT_20260123103000.md`

### 示例2：测试当前文件

```bash
/self-test
```

**执行过程**：
1. 分析当前打开的文件（如 `UserServiceImpl.java`）
2. 识别所有公共方法
3. 提示用户选择要测试的方法
4. 执行测试流程

### 示例3：带需求描述的测试

```bash
/self-test UserService.insertUser --需求：用户名长度必须在3-20个字符之间，邮箱必须是有效格式
```

**执行过程**：
1. 根据需求描述生成更精确的测试用例
2. 包含边界值测试（用户名长度 2、3、20、21）
3. 包含邮箱格式测试（有效、无效）
4. 执行并验证

---

**版本**：1.0.0
**作者**：Claude Code
**更新日期**：2026-01-23
