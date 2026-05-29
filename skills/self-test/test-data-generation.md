# 测试数据生成策略

本文档详细说明如何根据 Java 实体类和校验注解自动生成测试数据。

## 基本类型映射

### 字符串类型（String）

根据字段名智能生成：

| 字段名模式 | 生成规则 | 示例 |
|-----------|---------|------|
| `*name` | `test_{字段名}_{序号}` | `test_username_001` |
| `*email` | `test{序号}@example.com` | `test001@example.com` |
| `*phone` / `*mobile` | `138{8位数字}` | `13800138000` |
| `*address` | `测试地址{序号}` | `测试地址001` |
| `*url` | `http://test.example.com/{序号}` | `http://test.example.com/001` |
| `*code` | `TEST{6位数字}` | `TEST000001` |
| `*id` | 雪花ID或UUID | `1234567890123456789` |
| 其他 | `test_value_{序号}` | `test_value_001` |

### 数值类型

| 类型 | 默认值 | 说明 |
|-----|--------|------|
| `Integer` | `1` | 正整数 |
| `Long` | `1L` | 正长整数 |
| `Double` | `1.0` | 正浮点数 |
| `Float` | `1.0f` | 正浮点数 |
| `BigDecimal` | `new BigDecimal("1.00")` | 金额类型 |
| `Short` | `(short)1` | 短整数 |
| `Byte` | `(byte)1` | 字节 |

### 布尔类型（Boolean）

根据字段名判断：

| 字段名模式 | 默认值 | 说明 |
|-----------|--------|------|
| `is*` / `has*` / `can*` | `true` | 表示状态的字段 |
| `*enabled` / `*active` | `true` | 启用状态 |
| `*deleted` / `*removed` | `false` | 删除标记 |
| 其他 | `true` | 默认为真 |

### 日期时间类型

| 类型 | 生成规则 | 示例 |
|-----|---------|------|
| `Date` | 当前时间 | `new Date()` |
| `LocalDateTime` | 当前时间 | `LocalDateTime.now()` |
| `LocalDate` | 当前日期 | `LocalDate.now()` |
| `LocalTime` | 当前时间 | `LocalTime.now()` |
| `Timestamp` | 当前时间戳 | `new Timestamp(System.currentTimeMillis())` |

## 校验注解处理

### @NotBlank / @NotNull / @NotEmpty

**规则**：必须生成非空值

```java
@NotBlank
private String username;
// 生成：username = "test_username_001"

@NotNull
private Integer age;
// 生成：age = 25
```

### @Size(min=x, max=y)

**规则**：生成符合长度范围的字符串

```java
@Size(min = 3, max = 20)
private String username;
// 生成：username = "test_user_001" (长度在3-20之间)

@Size(min = 6, max = 18)
private String password;
// 生成：password = "test_pass_123456" (长度在6-18之间)
```

**边界测试用例**：
- 最小值：生成长度为 `min` 的字符串
- 最大值：生成长度为 `max` 的字符串
- 小于最小值：生成长度为 `min-1` 的字符串（预期失败）
- 大于最大值：生成长度为 `max+1` 的字符串（预期失败）

### @Email

**规则**：生成有效的邮箱格式

```java
@Email
private String email;
// 生成：email = "test001@example.com"
```

**测试用例**：
- 有效邮箱：`test001@example.com`
- 无效邮箱：`invalid-email`（预期失败）

### @Pattern(regexp="...")

**规则**：根据正则表达式生成匹配的字符串

```java
@Pattern(regexp = "^1[3-9]\\d{9}$")
private String phone;
// 生成：phone = "13800138000"

@Pattern(regexp = "^[A-Z]{2}\\d{6}$")
private String code;
// 生成：code = "AB123456"
```

### @Min / @Max

**规则**：生成符合范围的数值

```java
@Min(18)
@Max(100)
private Integer age;
// 生成：age = 25 (在18-100之间)
```

**边界测试用例**：
- 最小值：`18`
- 最大值：`100`
- 小于最小值：`17`（预期失败）
- 大于最大值：`101`（预期失败）

### @DecimalMin / @DecimalMax

**规则**：生成符合范围的小数

```java
@DecimalMin("0.01")
@DecimalMax("999999.99")
private BigDecimal amount;
// 生成：amount = new BigDecimal("100.00")
```

### @Positive / @PositiveOrZero / @Negative / @NegativeOrZero

**规则**：生成符合条件的数值

```java
@Positive
private Integer quantity;
// 生成：quantity = 1

@PositiveOrZero
private Integer stock;
// 生成：stock = 0

@Negative
private Integer debt;
// 生成：debt = -1
```

### @Past / @PastOrPresent / @Future / @FutureOrPresent

**规则**：生成符合时间条件的日期

```java
@Past
private LocalDateTime birthday;
// 生成：birthday = LocalDateTime.now().minusYears(25)

@Future
private LocalDateTime expireTime;
// 生成：expireTime = LocalDateTime.now().plusDays(30)
```

## 复杂对象生成

### 嵌套对象

**规则**：递归生成嵌套对象的所有字段

```java
public class Order {
    private String orderId;
    private User user;  // 嵌套对象
    private BigDecimal amount;
}

public class User {
    private String userId;
    private String username;
}
```

**生成结果**：
```json
{
  "orderId": "test_order_001",
  "user": {
    "userId": "1234567890123456789",
    "username": "test_username_001"
  },
  "amount": 100.00
}
```

### 集合类型

**规则**：生成包含 1-3 个元素的集合

```java
public class Order {
    private List<OrderItem> items;
}

public class OrderItem {
    private String productId;
    private Integer quantity;
}
```

**生成结果**：
```json
{
  "items": [
    {
      "productId": "test_product_001",
      "quantity": 1
    },
    {
      "productId": "test_product_002",
      "quantity": 2
    }
  ]
}
```

### Map 类型

**规则**：生成包含 1-3 个键值对的 Map

```java
public class Config {
    private Map<String, String> properties;
}
```

**生成结果**：
```json
{
  "properties": {
    "key1": "value1",
    "key2": "value2"
  }
}
```

## 特殊字段处理

### 枚举类型

**规则**：使用枚举的第一个值

```java
public enum UserStatus {
    ACTIVE, INACTIVE, DELETED
}

public class User {
    private UserStatus status;
}
```

**生成结果**：
```json
{
  "status": "ACTIVE"
}
```

### 忽略字段

**规则**：跳过以下字段，不生成测试数据

- `id`（主键，由数据库生成）
- `createTime`（创建时间，自动填充）
- `updateTime`（更新时间，自动填充）
- `createBy`（创建人，自动填充）
- `updateBy`（更新人，自动填充）
- `delFlag`（删除标记，自动填充）
- `revision`（乐观锁版本号，自动填充）

### 敏感字段

**规则**：敏感字段使用脱敏数据

| 字段类型 | 生成规则 | 示例 |
|---------|---------|------|
| 密码 | `test_password_123` | `test_password_123` |
| 身份证 | `11010119900101****` | `11010119900101****` |
| 银行卡 | `6222021234567890****` | `6222021234567890****` |
| 手机号 | `138****8000` | `138****8000` |

## 测试用例生成策略

### 正常用例

**目标**：验证功能正常工作

**生成规则**：
- 所有必填字段都有值
- 所有字段值符合校验规则
- 使用合理的业务数据

**示例**：
```json
{
  "username": "test_user_001",
  "email": "test001@example.com",
  "phone": "13800138000",
  "age": 25,
  "status": 1
}
```

### 边界用例

**目标**：验证边界条件

**生成规则**：
- 测试字段的最小值、最大值
- 测试长度的最小值、最大值
- 测试数值的边界值

**示例**：
```json
// 最小长度
{
  "username": "abc",  // @Size(min=3, max=20)
  "age": 18  // @Min(18)
}

// 最大长度
{
  "username": "abcdefghij1234567890",  // @Size(min=3, max=20)
  "age": 100  // @Max(100)
}
```

### 异常用例

**目标**：验证参数校验

**生成规则**：
- 必填字段为空
- 字段值不符合校验规则
- 字段格式错误

**示例**：
```json
// 用户名为空
{
  "username": "",  // @NotBlank
  "email": "test001@example.com"
}

// 邮箱格式错误
{
  "username": "test_user_001",
  "email": "invalid-email"  // @Email
}

// 年龄超出范围
{
  "username": "test_user_001",
  "age": 17  // @Min(18)
}
```

## 实现示例

### Java 代码示例

```java
public class TestDataGenerator {

    /**
     * 根据实体类生成测试数据
     */
    public static <T> T generateTestData(Class<T> clazz) {
        try {
            T instance = clazz.getDeclaredConstructor().newInstance();
            Field[] fields = clazz.getDeclaredFields();

            for (Field field : fields) {
                field.setAccessible(true);
                Object value = generateFieldValue(field);
                if (value != null) {
                    field.set(instance, value);
                }
            }

            return instance;
        } catch (Exception e) {
            throw new RuntimeException("生成测试数据失败", e);
        }
    }

    /**
     * 根据字段生成值
     */
    private static Object generateFieldValue(Field field) {
        // 忽略自动填充字段
        if (isAutoFillField(field.getName())) {
            return null;
        }

        Class<?> type = field.getType();
        String fieldName = field.getName();

        // 处理校验注解
        if (field.isAnnotationPresent(NotBlank.class)) {
            return generateStringValue(fieldName, field);
        }

        if (field.isAnnotationPresent(Email.class)) {
            return "test001@example.com";
        }

        if (field.isAnnotationPresent(Size.class)) {
            Size size = field.getAnnotation(Size.class);
            return generateStringWithSize(fieldName, size.min(), size.max());
        }

        // 根据类型生成
        if (type == String.class) {
            return generateStringValue(fieldName, field);
        } else if (type == Integer.class || type == int.class) {
            return 1;
        } else if (type == Long.class || type == long.class) {
            return 1L;
        } else if (type == Boolean.class || type == boolean.class) {
            return true;
        } else if (type == LocalDateTime.class) {
            return LocalDateTime.now();
        }

        return null;
    }

    /**
     * 判断是否为自动填充字段
     */
    private static boolean isAutoFillField(String fieldName) {
        return fieldName.equals("id")
            || fieldName.equals("createTime")
            || fieldName.equals("updateTime")
            || fieldName.equals("createBy")
            || fieldName.equals("updateBy")
            || fieldName.equals("delFlag")
            || fieldName.equals("revision");
    }

    /**
     * 根据字段名生成字符串值
     */
    private static String generateStringValue(String fieldName, Field field) {
        if (fieldName.contains("email")) {
            return "test001@example.com";
        } else if (fieldName.contains("phone") || fieldName.contains("mobile")) {
            return "13800138000";
        } else if (fieldName.contains("name")) {
            return "test_" + fieldName + "_001";
        } else {
            return "test_value_001";
        }
    }

    /**
     * 生成指定长度范围的字符串
     */
    private static String generateStringWithSize(String fieldName, int min, int max) {
        String base = "test_" + fieldName + "_";
        int targetLength = (min + max) / 2;  // 取中间值

        if (base.length() >= targetLength) {
            return base.substring(0, targetLength);
        } else {
            return base + "0".repeat(targetLength - base.length());
        }
    }
}
```

---

**版本**：1.0.0
**更新日期**：2026-01-23
