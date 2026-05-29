---
name: generate-tests
description: 根据修改内容生成单元测试代码，支持 Service 层、Mapper 层、工具类等的测试用例生成。适用于开发完成后补充测试、提高代码覆盖率等场景。
argument-hint: [类名] [方法名]
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# 生成单元测试代码

根据修改内容自动生成单元测试代码，提高代码覆盖率。

## 使用方式

```bash
# 为当前修改的代码生成测试
/generate-tests

# 为指定类生成测试
/generate-tests UserService

# 为指定方法生成测试
/generate-tests UserService.insertUser
```

## 执行流程

### 第一步：识别待测试代码

1. **如果未指定类名**：
   - 使用 Git 识别当前分支的修改
   - 提取修改的 Java 类
   - 过滤出需要测试的类（Service、Mapper、工具类等）

2. **如果指定了类名**：
   - 定位到指定的类文件
   - 读取类的所有公共方法

### 第二步：分析代码结构

读取待测试类的代码，分析：
- 类的依赖关系（@Autowired 的字段）
- 方法的参数和返回值
- 方法的业务逻辑
- 异常处理逻辑

### 第三步：生成测试代码

根据不同的类型生成对应的测试代码：

#### 1. Service 层测试

**位置**：`src/test/java/{package}/service/{ClassName}ServiceTest.java`

**模板**：
```java
package cn.city.parking.{module}.service;

import cn.city.parking.{module}.api.entity.{ClassName};
import cn.city.parking.{module}.mapper.{ClassName}Mapper;
import cn.city.parking.{module}.service.impl.{ClassName}ServiceImpl;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

/**
 * {ClassName}Service 单元测试
 *
 * @author Claude Code
 * @date {当前日期}
 */
@ExtendWith(MockitoExtension.class)
class {ClassName}ServiceTest {

    @Mock
    private {ClassName}Mapper {classNameLower}Mapper;

    @InjectMocks
    private {ClassName}ServiceImpl {classNameLower}Service;

    private {ClassName} test{ClassName};

    @BeforeEach
    void setUp() {
        // 准备测试数据
        test{ClassName} = new {ClassName}();
        test{ClassName}.setId("1");
        test{ClassName}.setFieldName("test_value");
    }

    @Test
    void testSelect{ClassName}ById_Success() {
        // Given
        String id = "1";
        when({classNameLower}Mapper.select{ClassName}ById(id)).thenReturn(test{ClassName});

        // When
        {ClassName} result = {classNameLower}Service.select{ClassName}ById(id);

        // Then
        assertNotNull(result);
        assertEquals("1", result.getId());
        assertEquals("test_value", result.getFieldName());
        verify({classNameLower}Mapper, times(1)).select{ClassName}ById(id);
    }

    @Test
    void testSelect{ClassName}ById_NotFound() {
        // Given
        String id = "999";
        when({classNameLower}Mapper.select{ClassName}ById(id)).thenReturn(null);

        // When
        {ClassName} result = {classNameLower}Service.select{ClassName}ById(id);

        // Then
        assertNull(result);
        verify({classNameLower}Mapper, times(1)).select{ClassName}ById(id);
    }

    @Test
    void testInsert{ClassName}_Success() {
        // Given
        when({classNameLower}Mapper.insert(any({ClassName}.class))).thenReturn(1);

        // When
        int result = {classNameLower}Service.insert{ClassName}(test{ClassName});

        // Then
        assertEquals(1, result);
        verify({classNameLower}Mapper, times(1)).insert(test{ClassName});
    }

    @Test
    void testUpdate{ClassName}_Success() {
        // Given
        when({classNameLower}Mapper.updateById(any({ClassName}.class))).thenReturn(1);

        // When
        int result = {classNameLower}Service.update{ClassName}(test{ClassName});

        // Then
        assertEquals(1, result);
        verify({classNameLower}Mapper, times(1)).updateById(test{ClassName});
    }

    @Test
    void testDelete{ClassName}ById_Success() {
        // Given
        String id = "1";
        when({classNameLower}Mapper.deleteById(id)).thenReturn(1);

        // When
        int result = {classNameLower}Service.delete{ClassName}ById(id);

        // Then
        assertEquals(1, result);
        verify({classNameLower}Mapper, times(1)).deleteById(id);
    }

    @Test
    void testSelect{ClassName}List_Success() {
        // Given
        {ClassName} query = new {ClassName}();
        List<{ClassName}> expectedList = Arrays.asList(test{ClassName});
        when({classNameLower}Mapper.select{ClassName}List(any({ClassName}.class))).thenReturn(expectedList);

        // When
        List<{ClassName}> result = {classNameLower}Service.select{ClassName}List(query);

        // Then
        assertNotNull(result);
        assertEquals(1, result.size());
        verify({classNameLower}Mapper, times(1)).select{ClassName}List(query);
    }
}
```

#### 2. Mapper 层测试

**位置**：`src/test/java/{package}/mapper/{ClassName}MapperTest.java`

**模板**：
```java
package cn.city.parking.{module}.mapper;

import cn.city.parking.{module}.api.entity.{ClassName};
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

/**
 * {ClassName}Mapper 单元测试
 *
 * @author Claude Code
 * @date {当前日期}
 */
@SpringBootTest
@Transactional  // 测试后自动回滚
class {ClassName}MapperTest {

    @Autowired
    private {ClassName}Mapper {classNameLower}Mapper;

    @Test
    void testInsert() {
        // Given
        {ClassName} entity = new {ClassName}();
        entity.setFieldName("test_value");

        // When
        int result = {classNameLower}Mapper.insert(entity);

        // Then
        assertEquals(1, result);
        assertNotNull(entity.getId());
    }

    @Test
    void testSelectById() {
        // Given
        {ClassName} entity = new {ClassName}();
        entity.setFieldName("test_value");
        {classNameLower}Mapper.insert(entity);

        // When
        {ClassName} result = {classNameLower}Mapper.select{ClassName}ById(entity.getId());

        // Then
        assertNotNull(result);
        assertEquals("test_value", result.getFieldName());
    }

    @Test
    void testSelectList() {
        // Given
        {ClassName} query = new {ClassName}();
        query.setFieldName("test");

        // When
        List<{ClassName}> result = {classNameLower}Mapper.select{ClassName}List(query);

        // Then
        assertNotNull(result);
    }

    @Test
    void testUpdate() {
        // Given
        {ClassName} entity = new {ClassName}();
        entity.setFieldName("test_value");
        {classNameLower}Mapper.insert(entity);

        entity.setFieldName("updated_value");

        // When
        int result = {classNameLower}Mapper.updateById(entity);

        // Then
        assertEquals(1, result);

        {ClassName} updated = {classNameLower}Mapper.select{ClassName}ById(entity.getId());
        assertEquals("updated_value", updated.getFieldName());
    }

    @Test
    void testDelete() {
        // Given
        {ClassName} entity = new {ClassName}();
        entity.setFieldName("test_value");
        {classNameLower}Mapper.insert(entity);

        // When
        int result = {classNameLower}Mapper.deleteById(entity.getId());

        // Then
        assertEquals(1, result);

        {ClassName} deleted = {classNameLower}Mapper.select{ClassName}ById(entity.getId());
        assertNull(deleted);
    }
}
```

#### 3. 工具类测试

**位置**：`src/test/java/{package}/util/{ClassName}UtilTest.java`

**模板**：
```java
package cn.city.parking.{module}.util;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.*;

/**
 * {ClassName}Util 单元测试
 *
 * @author Claude Code
 * @date {当前日期}
 */
class {ClassName}UtilTest {

    @Test
    void testMethodName_Success() {
        // Given
        String input = "test_input";

        // When
        String result = {ClassName}Util.methodName(input);

        // Then
        assertNotNull(result);
        assertEquals("expected_output", result);
    }

    @Test
    void testMethodName_NullInput() {
        // Given
        String input = null;

        // When & Then
        assertThrows(IllegalArgumentException.class, () -> {
            {ClassName}Util.methodName(input);
        });
    }

    @ParameterizedTest
    @CsvSource({
        "input1, output1",
        "input2, output2",
        "input3, output3"
    })
    void testMethodName_MultipleInputs(String input, String expected) {
        // When
        String result = {ClassName}Util.methodName(input);

        // Then
        assertEquals(expected, result);
    }

    @ParameterizedTest
    @ValueSource(strings = {"", " ", "  "})
    void testMethodName_EmptyInput(String input) {
        // When & Then
        assertThrows(IllegalArgumentException.class, () -> {
            {ClassName}Util.methodName(input);
        });
    }
}
```

### 第四步：生成测试数据

为测试用例生成合理的测试数据：

```java
/**
 * 测试数据构建器
 */
private {ClassName} buildTest{ClassName}() {
    {ClassName} entity = new {ClassName}();
    entity.setId("test_id_001");
    entity.setFieldName("test_value");
    entity.setStatus(1);
    entity.setCreateTime(LocalDateTime.now());
    return entity;
}

/**
 * 构建测试数据列表
 */
private List<{ClassName}> buildTest{ClassName}List() {
    return Arrays.asList(
        buildTest{ClassName}(),
        buildTest{ClassName}(),
        buildTest{ClassName}()
    );
}
```

### 第五步：生成测试配置

如果需要，生成测试配置文件：

**位置**：`src/test/resources/application-test.yml`

```yaml
spring:
  datasource:
    driver-class-name: org.h2.Driver
    url: jdbc:h2:mem:testdb
    username: sa
    password:

  h2:
    console:
      enabled: true

mybatis-plus:
  configuration:
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
```

## 测试类型

### 1. 单元测试（Unit Test）

- 测试单个方法的功能
- 使用 Mock 隔离依赖
- 快速执行

### 2. 集成测试（Integration Test）

- 测试多个组件的协作
- 使用真实的数据库
- 测试完整的业务流程

### 3. 参数化测试（Parameterized Test）

- 使用多组参数测试同一方法
- 提高测试覆盖率
- 减少重复代码

## 测试规范

### 1. 测试方法命名

格式：`test{方法名}_{场景}`

示例：
- `testInsertUser_Success`
- `testInsertUser_NullInput`
- `testInsertUser_DuplicateUsername`

### 2. 测试结构（Given-When-Then）

```java
@Test
void testMethodName_Success() {
    // Given - 准备测试数据
    String input = "test";

    // When - 执行测试方法
    String result = service.methodName(input);

    // Then - 验证结果
    assertEquals("expected", result);
}
```

### 3. 断言使用

```java
// 基本断言
assertEquals(expected, actual);
assertNotEquals(expected, actual);
assertTrue(condition);
assertFalse(condition);
assertNull(object);
assertNotNull(object);

// 异常断言
assertThrows(Exception.class, () -> {
    service.methodName(null);
});

// 集合断言
assertIterableEquals(expectedList, actualList);
assertArrayEquals(expectedArray, actualArray);
```

### 4. Mock 使用

```java
// Mock 返回值
when(mapper.selectById(anyString())).thenReturn(entity);

// Mock 抛出异常
when(mapper.insert(any())).thenThrow(new RuntimeException("error"));

// 验证调用
verify(mapper, times(1)).selectById("1");
verify(mapper, never()).deleteById(anyString());
```

## 测试覆盖率

生成测试后，运行覆盖率检查：

```bash
# 运行测试并生成覆盖率报告
mvn clean test jacoco:report

# 查看覆盖率报告
open target/site/jacoco/index.html
```

**目标覆盖率**：
- 行覆盖率 > 70%
- 分支覆盖率 > 60%
- 核心业务逻辑 > 90%

## 注意事项

1. **测试独立性**：每个测试用例应该独立，不依赖其他测试
2. **测试数据**：使用 `test_` 前缀，测试后自动清理
3. **事务回滚**：集成测试使用 `@Transactional` 自动回滚
4. **Mock 使用**：单元测试使用 Mock，集成测试使用真实依赖
5. **异常测试**：测试异常情况和边界条件

---

**版本**：1.0.0
**更新日期**：2026-01-23
