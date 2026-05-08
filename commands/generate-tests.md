---
description: 根据修改内容生成单元测试
---

# 单元测试生成器

> **使用场景**：新增功能后、Bug修复后、重构代码后
> **目标**：自动生成高质量的单元测试代码，确保代码质量和覆盖率

---

## 📋 任务说明

请执行以下步骤，为修改的代码生成完整的单元测试：

### 步骤1：识别需要测试的代码

1. 获取当前分支的变更文件
   ```bash
   git diff master...HEAD --name-only --diff-filter=AM | grep -E '\.(java)$'
   ```

2. 过滤出需要测试的文件类型：
   - ✅ Service实现类（`*ServiceImpl.java`）
   - ✅ DubboApi实现类（`*DubboApiImpl.java`）
   - ✅ 工具类（`*Utils.java`、`*Helper.java`）
   - ✅ Manager类（`*Manager.java`）
   - ❌ Entity类（不需要单测）
   - ❌ Mapper接口（由集成测试覆盖）
   - ❌ 配置类（不需要单测）

### 步骤2：分析代码逻辑

对每个需要测试的类，分析：
- 所有public方法
- 方法的输入参数
- 方法的返回值
- 方法的异常处理
- 方法的依赖项（需要Mock）
- 业务逻辑分支（if/else、循环）

### 步骤3：生成测试代码

为每个类生成对应的测试类，包含：
- 测试类基础结构
- Mock依赖注入
- 测试数据准备
- 正常场景测试
- 异常场景测试
- 边界条件测试

---

## 🧪 测试代码模板

### 模板1：Service层单元测试

```java
package cn.city.parking.{module}.service;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

import java.util.ArrayList;
import java.util.List;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import cn.city.parking.{module}.api.entity.{Entity};
import cn.city.parking.{module}.mapper.{Entity}Mapper;
import cn.city.parking.common.core.exception.BusinessException;

/**
 * {ClassName}测试类
 *
 * @author Claude Code
 * @since {当前日期}
 */
@ExtendWith(MockitoExtension.class)
@DisplayName("{ClassName}单元测试")
class {ClassName}Test {

    @Mock
    private {Entity}Mapper {entity}Mapper;

    @Mock
    private OtherService otherService;  // 其他依赖

    @InjectMocks
    private {ClassName} {classNameLowerCase};

    private {Entity} test{Entity};

    /**
     * 测试数据准备
     */
    @BeforeEach
    void setUp() {
        // 准备测试数据
        test{Entity} = new {Entity}();
        test{Entity}.setId("test-id-001");
        test{Entity}.set{Field}("test value");
        // ... 设置其他字段
    }

    /**
     * 测试方法：{methodName}
     * 场景：正常情况
     * 预期：成功返回结果
     */
    @Test
    @DisplayName("测试{methodName} - 正常情况")
    void test{MethodName}_ValidInput_Success() {
        // Given（准备测试数据）
        when({entity}Mapper.selectById(anyString())).thenReturn(test{Entity});

        // When（执行测试方法）
        {Entity} result = {classNameLowerCase}.{methodName}("test-id-001");

        // Then（验证结果）
        assertNotNull(result);
        assertEquals("test-id-001", result.getId());
        assertEquals("test value", result.get{Field}());

        // 验证方法调用
        verify({entity}Mapper, times(1)).selectById("test-id-001");
    }

    /**
     * 测试方法：{methodName}
     * 场景：参数为空
     * 预期：抛出BusinessException
     */
    @Test
    @DisplayName("测试{methodName} - 参数为空")
    void test{MethodName}_NullInput_ThrowException() {
        // When & Then
        assertThrows(BusinessException.class, () -> {
            {classNameLowerCase}.{methodName}(null);
        });
    }

    /**
     * 测试方法：{methodName}
     * 场景：数据不存在
     * 预期：返回null
     */
    @Test
    @DisplayName("测试{methodName} - 数据不存在")
    void test{MethodName}_NotFound_ReturnNull() {
        // Given
        when({entity}Mapper.selectById(anyString())).thenReturn(null);

        // When
        {Entity} result = {classNameLowerCase}.{methodName}("not-exist-id");

        // Then
        assertNull(result);
    }

    /**
     * 测试方法：insert{Entity}
     * 场景：正常插入
     * 预期：成功插入，返回1
     */
    @Test
    @DisplayName("测试insert{Entity} - 正常插入")
    void testInsert{Entity}_ValidInput_Success() {
        // Given
        when({entity}Mapper.insert(any({Entity}.class))).thenReturn(1);

        // When
        int result = {classNameLowerCase}.insert{Entity}(test{Entity});

        // Then
        assertEquals(1, result);
        verify({entity}Mapper, times(1)).insert(test{Entity});
    }

    /**
     * 测试方法：update{Entity}
     * 场景：正常更新
     * 预期：成功更新，返回1
     */
    @Test
    @DisplayName("测试update{Entity} - 正常更新")
    void testUpdate{Entity}_ValidInput_Success() {
        // Given
        when({entity}Mapper.selectById(anyString())).thenReturn(test{Entity});
        when({entity}Mapper.updateById(any({Entity}.class))).thenReturn(1);

        // When
        int result = {classNameLowerCase}.update{Entity}(test{Entity});

        // Then
        assertEquals(1, result);
        verify({entity}Mapper, times(1)).updateById(test{Entity});
    }

    /**
     * 测试方法：delete{Entity}ById
     * 场景：正常删除
     * 预期：成功删除，返回1
     */
    @Test
    @DisplayName("测试delete{Entity}ById - 正常删除")
    void testDelete{Entity}ById_ValidInput_Success() {
        // Given
        when({entity}Mapper.deleteById(anyString())).thenReturn(1);

        // When
        int result = {classNameLowerCase}.delete{Entity}ById("test-id-001");

        // Then
        assertEquals(1, result);
        verify({entity}Mapper, times(1)).deleteById("test-id-001");
    }

    /**
     * 测试方法：select{Entity}List
     * 场景：查询列表
     * 预期：返回列表数据
     */
    @Test
    @DisplayName("测试select{Entity}List - 查询列表")
    void testSelect{Entity}List_ValidInput_ReturnList() {
        // Given
        List<{Entity}> list = new ArrayList<>();
        list.add(test{Entity});
        when({entity}Mapper.selectList(any())).thenReturn(list);

        // When
        List<{Entity}> result = {classNameLowerCase}.select{Entity}List(new {Entity}());

        // Then
        assertNotNull(result);
        assertEquals(1, result.size());
        assertEquals("test-id-001", result.get(0).getId());
    }
}
```

### 模板2：DubboApi层单元测试

```java
package cn.city.parking.{module}.dubbo;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

import java.util.ArrayList;
import java.util.List;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import com.github.pagehelper.PageInfo;

import cn.city.parking.{module}.api.entity.{Entity};
import cn.city.parking.{module}.service.I{Entity}Service;
import cn.city.parking.common.core.web.domain.ResponseResult;

/**
 * {ClassName}测试类
 *
 * @author Claude Code
 * @since {当前日期}
 */
@ExtendWith(MockitoExtension.class)
@DisplayName("{ClassName}单元测试")
class {ClassName}Test {

    @Mock
    private I{Entity}Service {entity}Service;

    @InjectMocks
    private {ClassName} {classNameLowerCase};

    private {Entity} test{Entity};

    @BeforeEach
    void setUp() {
        test{Entity} = new {Entity}();
        test{Entity}.setId("test-id-001");
        test{Entity}.set{Field}("test value");
    }

    /**
     * 测试方法：getInfo
     * 场景：正常查询
     * 预期：返回成功结果
     */
    @Test
    @DisplayName("测试getInfo - 正常查询")
    void testGetInfo_ValidId_ReturnSuccess() {
        // Given
        when({entity}Service.select{Entity}ById(anyString())).thenReturn(test{Entity});

        // When
        ResponseResult<{Entity}> result = {classNameLowerCase}.getInfo("test-id-001");

        // Then
        assertTrue(result.isSuccess());
        assertEquals(200, result.getCode());
        assertNotNull(result.getData());
        assertEquals("test-id-001", result.getData().getId());
    }

    /**
     * 测试方法：getInfo
     * 场景：ID为空
     * 预期：抛出IllegalArgumentException
     */
    @Test
    @DisplayName("测试getInfo - ID为空")
    void testGetInfo_EmptyId_ThrowException() {
        // When & Then
        assertThrows(IllegalArgumentException.class, () -> {
            {classNameLowerCase}.getInfo("");
        });
    }

    /**
     * 测试方法：add
     * 场景：正常新增
     * 预期：返回成功结果
     */
    @Test
    @DisplayName("测试add - 正常新增")
    void testAdd_ValidInput_ReturnSuccess() {
        // Given
        when({entity}Service.insert{Entity}(any({Entity}.class))).thenReturn(1);

        // When
        ResponseResult<Integer> result = {classNameLowerCase}.add(test{Entity});

        // Then
        assertTrue(result.isSuccess());
        assertEquals(200, result.getCode());
        assertEquals(1, result.getData());
    }

    /**
     * 测试方法：edit
     * 场景：正常修改
     * 预期：返回成功结果
     */
    @Test
    @DisplayName("测试edit - 正常修改")
    void testEdit_ValidInput_ReturnSuccess() {
        // Given
        when({entity}Service.update{Entity}(any({Entity}.class))).thenReturn(1);

        // When
        ResponseResult<Integer> result = {classNameLowerCase}.edit(test{Entity});

        // Then
        assertTrue(result.isSuccess());
        assertEquals(1, result.getData());
    }

    /**
     * 测试方法：remove
     * 场景：正常删除
     * 预期：返回成功结果
     */
    @Test
    @DisplayName("测试remove - 正常删除")
    void testRemove_ValidId_ReturnSuccess() {
        // Given
        when({entity}Service.delete{Entity}ById(anyString())).thenReturn(1);

        // When
        ResponseResult<Integer> result = {classNameLowerCase}.remove("test-id-001");

        // Then
        assertTrue(result.isSuccess());
        assertEquals(1, result.getData());
    }

    /**
     * 测试方法：pageList
     * 场景：分页查询
     * 预期：返回分页数据
     */
    @Test
    @DisplayName("测试pageList - 分页查询")
    void testPageList_ValidInput_ReturnPageInfo() {
        // Given
        List<{Entity}> list = new ArrayList<>();
        list.add(test{Entity});
        when({entity}Service.select{Entity}List(any({Entity}.class))).thenReturn(list);

        // When
        ResponseResult<PageInfo<{Entity}>> result = {classNameLowerCase}.pageList(new {Entity}());

        // Then
        assertTrue(result.isSuccess());
        assertNotNull(result.getData());
        assertEquals(1, result.getData().getList().size());
    }

    /**
     * 测试方法：allList
     * 场景：查询所有
     * 预期：返回列表数据
     */
    @Test
    @DisplayName("测试allList - 查询所有")
    void testAllList_ValidInput_ReturnList() {
        // Given
        List<{Entity}> list = new ArrayList<>();
        list.add(test{Entity});
        when({entity}Service.select{Entity}List(any({Entity}.class))).thenReturn(list);

        // When
        ResponseResult<List<{Entity}>> result = {classNameLowerCase}.allList(new {Entity}());

        // Then
        assertTrue(result.isSuccess());
        assertNotNull(result.getData());
        assertEquals(1, result.getData().size());
    }
}
```

### 模板3：工具类单元测试

```java
package cn.city.parking.{module}.utils;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * {ClassName}测试类
 *
 * @author Claude Code
 * @since {当前日期}
 */
@DisplayName("{ClassName}单元测试")
class {ClassName}Test {

    /**
     * 测试方法：{methodName}
     * 场景：正常情况
     * 预期：返回预期结果
     */
    @Test
    @DisplayName("测试{methodName} - 正常情况")
    void test{MethodName}_ValidInput_ReturnExpected() {
        // Given
        String input = "test input";

        // When
        String result = {ClassName}.{methodName}(input);

        // Then
        assertNotNull(result);
        assertEquals("expected value", result);
    }

    /**
     * 测试方法：{methodName}
     * 场景：空值输入
     * 预期：返回空字符串或抛出异常
     */
    @Test
    @DisplayName("测试{methodName} - 空值输入")
    void test{MethodName}_NullInput_ReturnEmpty() {
        // When
        String result = {ClassName}.{methodName}(null);

        // Then
        assertEquals("", result);
    }

    /**
     * 测试方法：{methodName}
     * 场景：边界条件
     * 预期：正确处理边界值
     */
    @Test
    @DisplayName("测试{methodName} - 边界条件")
    void test{MethodName}_BoundaryValue_HandleCorrectly() {
        // Given
        String boundary = "";

        // When
        String result = {ClassName}.{methodName}(boundary);

        // Then
        assertNotNull(result);
    }
}
```

---

## 🎯 测试用例设计原则

### 1. 正常场景测试（Happy Path）

- ✅ 测试方法的主要功能
- ✅ 使用有效的输入参数
- ✅ 验证返回值正确
- ✅ 验证依赖方法被正确调用

### 2. 异常场景测试（Exception Path）

- ✅ 参数为null
- ✅ 参数为空字符串
- ✅ 参数格式错误
- ✅ 业务规则校验失败
- ✅ 依赖服务调用失败
- ✅ 数据库操作失败

### 3. 边界条件测试（Boundary）

- ✅ 数值的最大值、最小值、0
- ✅ 字符串的空串、超长字符串
- ✅ 集合的空集合、单元素、大量元素
- ✅ 日期的过去、现在、未来

### 4. 业务逻辑测试

- ✅ 所有if/else分支
- ✅ 循环逻辑
- ✅ 状态流转
- ✅ 计算逻辑

---

## 📊 测试覆盖率要求

### 覆盖率目标

- **核心业务模块**：>= 80%
- **普通业务模块**：>= 70%
- **工具类**：>= 90%

### 覆盖率类型

1. **行覆盖率**：每行代码是否被执行
2. **分支覆盖率**：每个if/else分支是否被执行
3. **方法覆盖率**：每个方法是否被测试

---

## 🛠️ Mock使用规范

### 何时使用Mock

- ✅ 依赖外部服务（数据库、Redis、Dubbo）
- ✅ 依赖其他Service
- ✅ 依赖复杂对象
- ❌ 不Mock简单的POJO对象
- ❌ 不Mock待测试类本身

### Mock示例

```java
// Mock Mapper
@Mock
private UserMapper userMapper;

// Mock Service
@Mock
private OrderService orderService;

// Mock RedisUtils
@Mock
private RedisUtils redisUtils;

// 配置Mock行为
when(userMapper.selectById("123")).thenReturn(user);
when(orderService.getOrder(anyString())).thenReturn(order);
doThrow(new BusinessException("错误")).when(redisUtils).setCacheObject(anyString(), any());

// 验证方法调用
verify(userMapper, times(1)).selectById("123");
verify(orderService, never()).deleteOrder(anyString());
```

---

## ✅ 测试代码检查清单

生成测试代码后，请检查：

### 1. 基础规范
- [ ] 测试类命名：`{ClassName}Test`
- [ ] 测试方法命名：`test{MethodName}_{Scenario}_{ExpectedResult}`
- [ ] 使用`@DisplayName`描述测试用例
- [ ] 使用`@BeforeEach`准备测试数据

### 2. 断言完整性
- [ ] 有明确的断言（assertXxx）
- [ ] 断言覆盖返回值
- [ ] 断言覆盖异常情况
- [ ] 断言覆盖方法调用（verify）

### 3. Mock正确性
- [ ] Mock了所有外部依赖
- [ ] Mock行为配置正确（when...thenReturn）
- [ ] 验证了Mock方法调用（verify）
- [ ] 没有Mock待测试类本身

### 4. 测试数据
- [ ] 测试数据有代表性
- [ ] 测试数据可复用（@BeforeEach）
- [ ] 测试数据独立（不依赖其他测试）

### 5. 覆盖率
- [ ] 覆盖所有public方法
- [ ] 覆盖所有if/else分支
- [ ] 覆盖异常场景
- [ ] 覆盖边界条件

---

## 🚀 执行步骤

我将按照以下步骤为你生成测试代码：

1. **分析变更代码**
   - 识别新增/修改的Service、DubboApi类
   - 分析每个类的public方法
   - 识别方法的依赖项

2. **生成测试类**
   - 为每个需要测试的类生成测试类
   - 创建测试文件（在`src/test/java`目录下）
   - 生成基础结构（Mock、BeforeEach）

3. **生成测试方法**
   - 为每个public方法生成3-5个测试用例
   - 包含正常场景、异常场景、边界条件
   - 配置Mock行为
   - 添加断言

4. **优化测试代码**
   - 提取公共测试数据到@BeforeEach
   - 添加@DisplayName注释
   - 检查Mock配置
   - 确保测试独立性

5. **生成测试报告**
   - 统计生成的测试类数量
   - 统计生成的测试方法数量
   - 预估测试覆盖率
   - 标注需要手工调整的部分

---

## 📝 注意事项

1. **自动生成的测试代码需要人工review**：
   - 验证Mock配置是否正确
   - 验证断言是否完整
   - 补充复杂业务逻辑的测试

2. **特殊情况处理**：
   - 私有方法不生成测试（通过public方法覆盖）
   - 配置类不生成测试
   - Entity类不生成测试

3. **测试数据准备**：
   - 优先使用@BeforeEach准备通用数据
   - 特殊场景在测试方法内准备数据
   - 避免硬编码，使用常量

4. **运行测试**：
   ```bash
   # 运行所有测试
   mvn test

   # 运行指定测试类
   mvn test -Dtest=UserServiceTest

   # 生成测试覆盖率报告
   mvn test jacoco:report
   ```

---

**开始生成测试代码吗？**

请确认需要为哪些文件生成测试：
- [ ] 自动识别本次变更的所有文件
- [ ] 手动指定文件路径
- [ ] 只为Service层生成测试
- [ ] 为Service + DubboApi生成测试
