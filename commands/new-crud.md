---
description: 创建完整的CRUD功能（Entity + Mapper + Service + DubboApi）
---

# 创建CRUD功能

我需要创建一个完整的CRUD功能模块。

## 请先提供以下信息：

1. **实体类名称**（驼峰命名，如：ParkingLot）
2. **表名**（下划线命名，如：parking_lot）
3. **所属模块**（如：city-parking-xxx）
4. **功能名称**（中文，如：停车场管理）
5. **主要字段列表**（字段名、类型、说明）

## 开发步骤：

### 1. Entity（实体类）
- 继承 `BusinessEntity`
- 使用 `@Schema` 注解（不用@ApiModel）
- 使用 `@TableName` 指定表名
- **可选：添加参数校验注解**：`@NotBlank`、`@Size`、`@Email`、`@Pattern`等（如需使用，message属性必填）
- 可选字段根据需要添加：revision、createBy、delFlag、updateBy

### 2. Mapper接口
- 继承 `CommonMapper<{ClassName}>`
- 使用 `cn.city.parking.common.server.injector.CommonMapper`
- 定义自定义查询方法：`List<{ClassName}> select{ClassName}List({ClassName} entity)`

### 3. Mapper.xml
- 定义 resultMap
- 定义 select{ClassName}Vo（公共查询字段）
- 实现 select{ClassName}List 方法（支持动态查询）

### 4. Service接口
- 继承 `IService<{ClassName}>`
- 定义7个标准方法

### 5. Service实现
- 继承 `ServiceImpl<{ClassName}Mapper, {ClassName}>`
- 实现接口方法
- 增删改方法添加 `@Transactional(rollbackFor = Exception.class)`

### 6. DubboApi接口
- 定义6个标准方法（pageList、allList、getInfo、add、edit、remove）
- 返回值统一使用 `ResponseResult`

### 7. DubboApiImpl实现
- 继承 `BaseDubboApi`
- 添加 `@DubboService` 注解
- 注入Service
- 实现接口方法（⚠️ 保持薄层：只负责参数校验、调用Service、返回结果）
- pageList方法调用 `startDubboPage()`
- **可选：参数校验两种方式**（根据业务需要灵活选择）：
  - 简单参数（String、int等）：使用`Preconditions.checkArgument()`
  - 复杂对象（Entity、DTO等）：使用`ValidateUtil.validate()`
- ❌ 不要在DubboApi中写业务逻辑（查询条件构建、缓存处理、循环处理等应该在Service层）

## 代码规范要求：

- ✅ **实体类继承BusinessEntity**
- ✅ **使用@Schema注解**（io.swagger.v3.oas.annotations.media.Schema）
- ✅ **返回值使用ResponseResult**
- ✅ **异常使用BusinessException**
- ✅ **参数校验**（推荐但非强制）：
  - 可在Entity、DTO、VO等对象字段添加`@NotBlank`、`@Size`、`@Email`、`@Pattern`等注解（如需使用，message必填）
  - 简单参数使用`Preconditions.checkArgument()`
  - 复杂对象使用`ValidateUtil.validate()`
  - Controller层根据实际情况灵活选择是否校验
- ✅ **事务注解**：@Transactional(rollbackFor = Exception.class)
- ✅ **分页方法调用startDubboPage()**
- ✅ **注释完整，方法说明清晰**

## 额外功能（可选）

如果需要以下功能，请明确说明：
- [ ] 是否需要缓存？（使用RedisUtils）
- [ ] 是否需要防重复提交？（使用@NoRepeatSubmit）
- [ ] 是否需要乐观锁？（添加revision字段）
- [ ] 是否需要逻辑删除？（添加delFlag字段）
- [ ] 是否需要Excel导入导出？（添加@Excel注解）

请根据提供的信息开始生成完整的CRUD代码。
