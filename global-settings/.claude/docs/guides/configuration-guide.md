# City Parking 配置指南

> 本文档包含 POM、YAML、数据库、Spring Java Format 等配置的完整说明

## 目录

- [POM配置规范](#pom配置规范)
  - [父POM](#父pom)
  - [API模块依赖](#api模块依赖)
  - [Server模块完整配置](#server模块完整配置)
- [配置文件规范](#配置文件规范)
  - [bootstrap.yml](#bootstraptyml)
- [数据库规范](#数据库规范)
  - [必备字段](#必备字段businessentity已包含)
  - [可选字段](#可选字段)
  - [表设计规范](#表设计规范)
  - [索引规范](#索引规范)
- [Spring Java Format配置](#spring-java-format配置)
  - [Maven配置](#maven配置)
  - [IDEA配置](#idea配置)
  - [开发流程](#开发流程)
  - [核心风格规则](#核心风格规则)
  - [常见格式化问题](#常见格式化问题)
  - [代码审查清单](#代码审查清单)
  - [参考资源](#参考资源)

---

## POM配置规范

### 父POM

所有服务的根POM必须继承统一的父POM：

```xml
<parent>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-parent</artifactId>
    <version>2.0.0-SNAPSHOT</version>
    <relativePath/>
</parent>
```

**要点**：
- ✅ groupId是 `cn.city-parking`（带横杠，不是下划线）
- ✅ parent是 `city-parking-parent`（不是city-parking-common-2.0）
- ✅ relativePath为空（从Maven私库获取）
- ❌ 不要使用本地路径或相对路径

**示例**：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>cn.city-parking</groupId>
        <artifactId>city-parking-parent</artifactId>
        <version>2.0.0-SNAPSHOT</version>
        <relativePath/>
    </parent>

    <artifactId>city-parking-xxx</artifactId>
    <version>2.0.0-SNAPSHOT</version>
    <packaging>pom</packaging>

    <modules>
        <module>city-parking-xxx-api</module>
        <module>city-parking-xxx-server</module>
    </modules>
</project>
```

---

### API模块依赖

API模块（`city-parking-xxx-api`）只需依赖 `common-auth`：

```xml
<dependencies>
    <!-- common-auth（包含实体基类、注解等） -->
    <dependency>
        <groupId>cn.city-parking</groupId>
        <artifactId>city-parking-common-auth</artifactId>
    </dependency>
</dependencies>
```

**说明**：
- ✅ API模块只定义接口、实体类、DTO
- ✅ 不需要指定version（从父POM继承）
- ✅ common-auth包含了 `BusinessEntity`、`@Schema` 等必要依赖
- ❌ 不要依赖 `common-server`（Server模块才需要）

**完整API模块POM**：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>cn.city-parking</groupId>
        <artifactId>city-parking-xxx</artifactId>
        <version>2.0.0-SNAPSHOT</version>
    </parent>

    <artifactId>city-parking-xxx-api</artifactId>
    <version>2.0.0-SNAPSHOT</version>

    <dependencies>
        <!-- common-auth -->
        <dependency>
            <groupId>cn.city-parking</groupId>
            <artifactId>city-parking-common-auth</artifactId>
        </dependency>
    </dependencies>
</project>
```

---

### Server模块完整配置

Server模块（`city-parking-xxx-server`）是服务实现，需要完整的依赖和打包配置：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>cn.city-parking</groupId>
        <artifactId>city-parking-parent</artifactId>
        <version>2.0.0-SNAPSHOT</version>
        <relativePath/>
    </parent>

    <artifactId>city-parking-xxx-server</artifactId>
    <version>2.0.0-SNAPSHOT</version>

    <dependencies>
        <!-- common-server（包含MyBatis Plus、Redis、Dubbo等） -->
        <dependency>
            <groupId>cn.city-parking</groupId>
            <artifactId>city-parking-common-server</artifactId>
        </dependency>

        <!-- 本服务API -->
        <dependency>
            <groupId>cn.city-parking</groupId>
            <artifactId>city-parking-xxx-api</artifactId>
            <version>2.0.0-SNAPSHOT</version>
        </dependency>
    </dependencies>

    <build>
        <finalName>${project.artifactId}</finalName>
        <plugins>
            <!-- Spring Boot打包插件 -->
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <version>${spring-boot.version}</version>
                <configuration>
                    <!-- ✅ 必须指定启动类 -->
                    <mainClass>cn.city.parking.xxx.CityParkingXxxApplication</mainClass>
                </configuration>
                <executions>
                    <execution>
                        <goals>
                            <goal>repackage</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>

            <!-- ✅ 禁止Server模块发布到Maven私库 -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-deploy-plugin</artifactId>
                <version>2.8.2</version>
                <configuration>
                    <skip>true</skip>
                </configuration>
            </plugin>

            <!-- Spring Java Format插件（可选） -->
            <plugin>
                <groupId>io.spring.javaformat</groupId>
                <artifactId>spring-javaformat-maven-plugin</artifactId>
                <version>0.0.39</version>
                <executions>
                    <execution>
                        <phase>validate</phase>
                        <inherited>true</inherited>
                        <goals>
                            <goal>validate</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
```

**重要说明**：

1. **必须配置mainClass**：
   - ✅ 否则无法打包成可执行jar
   - ✅ mainClass是启动类的完整类名
   - ✅ 启动类必须包含`main`方法

2. **必须禁止发布到私库**：
   - ✅ Server模块只用于部署，不需要被其他模块依赖
   - ✅ `<skip>true</skip>` 会跳过deploy阶段

3. **依赖说明**：
   - ✅ `common-server`会传递依赖MyBatis Plus、Redis、Dubbo等
   - ✅ 本服务API需要指定version（与父POM版本一致）

**常见错误**：

```xml
<!-- ❌ 错误1：缺少mainClass配置 -->
<plugin>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-maven-plugin</artifactId>
    <!-- 缺少configuration -->
</plugin>

<!-- ❌ 错误2：没有禁止发布到私库 -->
<!-- Server模块会被错误地发布到Maven私库 -->

<!-- ❌ 错误3：错误的启动类路径 -->
<mainClass>CityParkingXxxApplication</mainClass>  <!-- 缺少包名 -->
```

---

## 配置文件规范

### bootstrap.yml

**核心原则**：只需修改两处，其他配置使用占位符从Nacos读取。

**必须修改的配置**：
1. `server.port`：服务端口
2. `spring.application.name`：服务名称

**完整配置示例**：

```yaml
# ========================================
# 基础配置（必须修改）
# ========================================
server:
  port: 9210  # ✅ 修改为你的服务端口

spring:
  application:
    name: city-parking-xxx  # ✅ 修改为你的服务名
  profiles:
    active: @profileActive@  # ✅ 占位符，从Maven profile读取

# ========================================
# Nacos配置（使用占位符，从Nacos读取）
# ========================================
  cloud:
    nacos:
      discovery:
        server-addr: ${nacos.server-addr}
        namespace: ${nacos.namespace}
        group: ${nacos.group}
      config:
        server-addr: ${nacos.server-addr}
        namespace: ${nacos.namespace}
        group: ${nacos.group}
        file-extension: yml
        refresh-enabled: true

# ========================================
# Dubbo配置（使用占位符，从Nacos读取）
# ========================================
dubbo:
  application:
    name: ${spring.application.name}
  protocol:
    name: dubbo
    port: ${dubbo.protocol.port}
  registry:
    address: ${dubbo.registry.address}
  scan:
    base-packages: cn.city.parking

# ========================================
# 数据源配置（使用占位符，从Nacos读取）
# ========================================
  datasource:
    driver-class-name: ${spring.datasource.driver-class-name}
    url: ${spring.datasource.url}
    username: ${spring.datasource.username}
    password: ${spring.datasource.password}
    hikari:
      maximum-pool-size: ${spring.datasource.hikari.maximum-pool-size:20}
      minimum-idle: ${spring.datasource.hikari.minimum-idle:5}
      connection-timeout: ${spring.datasource.hikari.connection-timeout:30000}

# ========================================
# Redis配置（使用占位符，从Nacos读取）
# ========================================
  redis:
    host: ${spring.redis.host}
    port: ${spring.redis.port}
    password: ${spring.redis.password}
    database: ${spring.redis.database:0}
    timeout: ${spring.redis.timeout:6000}
    lettuce:
      pool:
        max-active: ${spring.redis.lettuce.pool.max-active:8}
        max-idle: ${spring.redis.lettuce.pool.max-idle:8}
        min-idle: ${spring.redis.lettuce.pool.min-idle:0}

# ========================================
# 日志配置
# ========================================
logging:
  level:
    cn.city.parking: ${logging.level.cn.city.parking:INFO}
  file:
    name: logs/${spring.application.name}.log
```

**配置说明**：

1. **端口分配规则**：
   - BFF服务：9000-9099
   - 基础服务（user、rbac）：9100-9199
   - 业务服务：9200-9299
   - 工具服务：9300-9399

2. **服务命名规范**：
   - 格式：`city-parking-{模块名}`
   - 示例：`city-parking-user`、`city-parking-order`、`city-parking-parking`

3. **占位符说明**：
   - `${xxx}`：从Nacos配置中心读取
   - `${xxx:default}`：从Nacos读取，不存在时使用默认值
   - `@xxx@`：从Maven profile读取

**Nacos配置示例**（在Nacos配置中心配置）：

```yaml
# custom-config.yml（所有服务共享配置）
nacos:
  server-addr: 127.0.0.1:8848
  namespace: dev
  group: DEFAULT_GROUP

spring:
  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://localhost:3306/city_parking?useUnicode=true&characterEncoding=utf8&serverTimezone=Asia/Shanghai
    username: root
    password: password
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      connection-timeout: 30000

  redis:
    host: 127.0.0.1
    port: 6379
    password:
    database: 0

dubbo:
  protocol:
    port: -1  # -1表示自动分配端口
  registry:
    address: nacos://${nacos.server-addr}?namespace=${nacos.namespace}

# 业务配置
custom-config:
  server:
    id-type: snowflake
    id-random: false
  task:
    pool:
      core-size: 16
      max-size: 32
      queue-capacity: 200
```

**常见错误**：

```yaml
# ❌ 错误1：端口冲突
server:
  port: 9210  # 与其他服务端口冲突

# ❌ 错误2：服务名不规范
spring:
  application:
    name: xxx-service  # 缺少city-parking前缀

# ❌ 错误3：硬编码配置（不使用占位符）
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/db  # 应该从Nacos读取
    username: root  # 应该从Nacos读取

# ❌ 错误4：占位符语法错误
spring:
  redis:
    host: {spring.redis.host}  # 错误！应该用 ${} 而不是 {}
```

---

## 数据库规范

### 必备字段（BusinessEntity已包含）

所有业务表必须包含以下字段（继承`BusinessEntity`自动包含）：

```sql
-- 主键
id VARCHAR(64) PRIMARY KEY COMMENT '主键ID（雪花算法）'

-- 时间字段
create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
```

**字段说明**：

1. **id字段**：
   - ✅ 类型：`VARCHAR(64)`（存储雪花ID）
   - ✅ 主键约束：`PRIMARY KEY`
   - ✅ 框架自动生成（雪花算法）
   - ❌ 不要使用`INT`自增ID

2. **create_time字段**：
   - ✅ 类型：`DATETIME`
   - ✅ 默认值：`CURRENT_TIMESTAMP`
   - ✅ 框架自动填充（`MyMetaObjectHandler`）

3. **update_time字段**：
   - ✅ 类型：`DATETIME`
   - ✅ 默认值：`CURRENT_TIMESTAMP`
   - ✅ 自动更新：`ON UPDATE CURRENT_TIMESTAMP`
   - ✅ 框架自动填充（`MyMetaObjectHandler`）

**实体类对应**：

```java
@Data
@EqualsAndHashCode(callSuper = true)
@TableName("sys_user")
public class User extends BusinessEntity {
    // BusinessEntity已包含以下字段，无需重复定义：
    // private String id;
    // private Date createTime;
    // private Date updateTime;

    // 业务字段
    private String username;
    private String phone;
}
```

---

### 可选字段

根据业务需要，可以添加以下字段：

```sql
-- 创建人/修改人
create_by VARCHAR(64) COMMENT '创建人'
update_by VARCHAR(64) COMMENT '更新人'

-- 逻辑删除
del_flag TINYINT(1) DEFAULT 0 COMMENT '逻辑删除（0-否 1-是）'

-- 乐观锁版本号
revision BIGINT(20) DEFAULT 0 COMMENT '乐观锁版本号'

-- 备注
remark VARCHAR(500) COMMENT '备注'
```

**字段说明**：

1. **create_by / update_by**：
   - ✅ 类型：`VARCHAR(64)`
   - ✅ 框架自动填充（从`SecurityContext`获取当前用户名）
   - ⚠️ 无登录用户时默认填充"系统"
   - 使用场景：需要记录操作人的业务表

2. **del_flag**：
   - ✅ 类型：`TINYINT(1)`
   - ✅ 默认值：`0`（未删除）
   - ✅ 框架自动填充
   - ✅ MyBatis Plus逻辑删除支持（需配置`@TableLogic`）
   - 使用场景：需要逻辑删除的业务表

3. **revision**：
   - ✅ 类型：`BIGINT(20)`
   - ✅ 默认值：`0`
   - ✅ MyBatis Plus乐观锁支持（需配置`@Version`）
   - 使用场景：高并发更新场景（订单、库存等）

4. **remark**：
   - ✅ 类型：`VARCHAR(500)`
   - 使用场景：需要备注说明的业务表

**实体类对应**：

```java
@Data
@EqualsAndHashCode(callSuper = true)
@TableName("sys_user")
public class User extends BusinessEntity {
    // 业务字段
    private String username;
    private String phone;

    // 可选字段
    private String createBy;     // 创建人
    private String updateBy;     // 更新人

    @TableLogic                 // 逻辑删除
    private Integer delFlag;

    @Version                    // 乐观锁版本号
    private Long revision;

    private String remark;       // 备注
}
```

---

### 表设计规范

**命名规范**：

```sql
-- ✅ 表名：小写+下划线，带模块前缀
sys_user         -- 系统用户表
parking_order    -- 停车订单表
coupon_rule      -- 优惠券规则表

-- ❌ 错误命名
SysUser          -- 不要使用驼峰命名
tbl_user         -- 不要使用tbl前缀
user             -- 缺少模块前缀（可能冲突）

-- ✅ 字段名：小写+下划线
user_name
phone_number
create_time

-- ❌ 错误命名
userName         -- 不要使用驼峰命名
PHONE_NUMBER     -- 不要使用大写
createtime       -- 单词之间要有下划线
```

**字段类型选择**：

| 业务场景 | 推荐类型 | 说明 |
|---------|---------|------|
| 主键ID | VARCHAR(64) | 存储雪花ID |
| 用户名/姓名 | VARCHAR(64) | 可变长字符串 |
| 手机号 | VARCHAR(20) | 固定格式，使用字符串 |
| 身份证号 | VARCHAR(20) | 固定格式，使用字符串 |
| 金额 | DECIMAL(10,2) | 精确小数，避免丢失精度 |
| 数量 | INT | 整数 |
| 状态/类型 | TINYINT | 枚举值（0-255） |
| 布尔值 | TINYINT(1) | 0-否 1-是 |
| 日期时间 | DATETIME | 精确到秒 |
| 文本描述 | VARCHAR(500) | 短文本 |
| 长文本 | TEXT | 长文本（>500字符） |
| JSON数据 | TEXT/JSON | JSON格式数据 |

**字段长度建议**：

```sql
-- 姓名/用户名
username VARCHAR(64)

-- 手机号
phone VARCHAR(20)

-- 身份证号
id_card VARCHAR(20)

-- 邮箱
email VARCHAR(128)

-- 地址
address VARCHAR(255)

-- 短描述/备注
remark VARCHAR(500)

-- 长文本描述
content TEXT

-- URL
url VARCHAR(255)
```

**字段约束**：

```sql
-- ✅ 主键约束
id VARCHAR(64) PRIMARY KEY

-- ✅ 唯一约束（防止重复数据）
order_no VARCHAR(64) UNIQUE KEY COMMENT '订单号'
phone VARCHAR(20) UNIQUE KEY COMMENT '手机号'

-- ✅ 非空约束（重要字段）
username VARCHAR(64) NOT NULL COMMENT '用户名'
status TINYINT NOT NULL DEFAULT 1 COMMENT '状态'

-- ✅ 默认值（避免NULL）
status TINYINT DEFAULT 1 COMMENT '状态：0-禁用 1-启用'
del_flag TINYINT DEFAULT 0 COMMENT '删除标志：0-否 1-是'
create_time DATETIME DEFAULT CURRENT_TIMESTAMP
```

**完整建表示例**：

```sql
CREATE TABLE `sys_user` (
    -- 必备字段
    `id` VARCHAR(64) NOT NULL PRIMARY KEY COMMENT '主键ID',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    -- 可选字段
    `create_by` VARCHAR(64) DEFAULT NULL COMMENT '创建人',
    `update_by` VARCHAR(64) DEFAULT NULL COMMENT '更新人',
    `del_flag` TINYINT(1) DEFAULT 0 COMMENT '逻辑删除：0-否 1-是',
    `revision` BIGINT(20) DEFAULT 0 COMMENT '乐观锁版本号',
    `remark` VARCHAR(500) DEFAULT NULL COMMENT '备注',

    -- 业务字段
    `username` VARCHAR(64) NOT NULL COMMENT '用户名',
    `password` VARCHAR(128) NOT NULL COMMENT '密码',
    `phone` VARCHAR(20) UNIQUE KEY COMMENT '手机号',
    `email` VARCHAR(128) DEFAULT NULL COMMENT '邮箱',
    `status` TINYINT DEFAULT 1 COMMENT '状态：0-禁用 1-启用',
    `last_login_time` DATETIME DEFAULT NULL COMMENT '最后登录时间',

    -- 索引
    INDEX idx_username (`username`),
    INDEX idx_phone (`phone`),
    INDEX idx_status (`status`),
    INDEX idx_create_time (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统用户表';
```

---

### 索引规范

**必须建立索引的字段**：

1. **主键**（自动创建索引）：
```sql
PRIMARY KEY (`id`)
```

2. **唯一字段**（自动创建唯一索引）：
```sql
UNIQUE KEY uk_order_no (`order_no`)
UNIQUE KEY uk_phone (`phone`)
```

3. **WHERE条件字段**：
```sql
-- 高频查询字段
INDEX idx_username (`username`)
INDEX idx_status (`status`)
INDEX idx_user_id (`user_id`)

-- 时间范围查询
INDEX idx_create_time (`create_time`)
```

4. **ORDER BY字段**：
```sql
INDEX idx_create_time (`create_time`)
```

5. **JOIN关联字段**：
```sql
-- 订单表关联用户表
INDEX idx_user_id (`user_id`)

-- 订单明细关联订单主表
INDEX idx_order_id (`order_id`)
```

**复合索引规范**：

```sql
-- ✅ 最左前缀原则：高频查询字段在前
INDEX idx_user_status_time (`user_id`, `status`, `create_time`)

-- 使用场景：
-- WHERE user_id = ?  -- 可以用到索引
-- WHERE user_id = ? AND status = ?  -- 可以用到索引
-- WHERE user_id = ? AND status = ? AND create_time > ?  -- 可以用到索引
-- WHERE status = ?  -- 无法用到索引（跳过了user_id）

-- ❌ 错误：低频字段在前
INDEX idx_time_status_user (`create_time`, `status`, `user_id`)
-- 大多数查询都是按user_id查询，但索引顺序错误
```

**索引命名规范**：

```sql
-- 普通索引：idx_{字段名}
INDEX idx_username (`username`)
INDEX idx_user_id (`user_id`)

-- 复合索引：idx_{字段1}_{字段2}
INDEX idx_user_status (`user_id`, `status`)

-- 唯一索引：uk_{字段名}
UNIQUE KEY uk_order_no (`order_no`)
UNIQUE KEY uk_phone (`phone`)

-- 联合唯一索引：uk_{字段1}_{字段2}
UNIQUE KEY uk_order_serial (`order_no`, `pay_serial_no`)
```

**索引使用建议**：

```sql
-- ✅ 选择性高的字段建索引
INDEX idx_phone (`phone`)  -- 手机号唯一，选择性高
INDEX idx_id_card (`id_card`)  -- 身份证号唯一，选择性高

-- ❌ 选择性低的字段不建索引
-- INDEX idx_gender (`gender`)  -- 性别只有2-3个值，选择性低
-- INDEX idx_status (`status`)  -- 如果状态值只有2-3个，不建议单独索引

-- ✅ 字符串字段可以使用前缀索引
INDEX idx_address (`address`(20))  -- 地址字段很长，只索引前20个字符

-- ✅ 经常一起查询的字段建复合索引
INDEX idx_user_time (`user_id`, `create_time`)
-- 查询：WHERE user_id = ? AND create_time > ?
```

**索引数量控制**：

- ✅ 单表索引数量建议不超过5个
- ✅ 复合索引字段数量建议不超过3个
- ❌ 避免索引过多（影响写入性能）
- ❌ 避免冗余索引

**示例**：

```sql
CREATE TABLE `parking_order` (
    `id` VARCHAR(64) NOT NULL PRIMARY KEY COMMENT '订单ID',
    `order_no` VARCHAR(64) NOT NULL COMMENT '订单号',
    `user_id` VARCHAR(64) NOT NULL COMMENT '用户ID',
    `parking_lot_id` VARCHAR(64) NOT NULL COMMENT '停车场ID',
    `plate_number` VARCHAR(20) NOT NULL COMMENT '车牌号',
    `status` TINYINT NOT NULL COMMENT '状态：0-待支付 1-已支付 2-已完成',
    `amount` DECIMAL(10,2) NOT NULL COMMENT '金额',
    `start_time` DATETIME NOT NULL COMMENT '开始时间',
    `end_time` DATETIME DEFAULT NULL COMMENT '结束时间',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- 索引
    UNIQUE KEY uk_order_no (`order_no`),                        -- 订单号唯一
    INDEX idx_user_id (`user_id`),                             -- 用户维度查询
    INDEX idx_user_status (`user_id`, `status`),               -- 用户+状态查询
    INDEX idx_parking_lot (`parking_lot_id`),                  -- 停车场维度查询
    INDEX idx_create_time (`create_time`)                      -- 时间范围查询
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='停车订单表';
```

---

## Spring Java Format配置

### Maven配置

在 **parent POM** 或 **server 模块 POM** 中添加插件：

```xml
<build>
    <plugins>
        <!-- Spring Java Format 插件 -->
        <plugin>
            <groupId>io.spring.javaformat</groupId>
            <artifactId>spring-javaformat-maven-plugin</artifactId>
            <version>0.0.39</version>
            <executions>
                <execution>
                    <phase>validate</phase>
                    <inherited>true</inherited>
                    <goals>
                        <goal>validate</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

**Maven 命令**：

```bash
# 检查代码格式（不修改文件）
mvn spring-javaformat:validate

# 自动格式化代码
mvn spring-javaformat:apply

# 在编译前自动检查
mvn clean install
```

**说明**：
- ✅ `validate`目标：检查代码格式，不符合规范会报错
- ✅ `apply`目标：自动格式化代码
- ✅ `phase=validate`：在Maven验证阶段自动执行格式检查
- ✅ `inherited=true`：子模块继承此配置

---

### IDEA配置

**方式1：安装插件（推荐）**

1. 打开 IDEA → Settings → Plugins
2. 搜索 `Spring Java Format`
3. 安装并重启 IDEA
4. 插件会自动应用 Spring 代码风格

**方式2：导入配置文件**

1. 下载配置文件：
   ```bash
   wget https://raw.githubusercontent.com/spring-io/spring-javaformat/main/spring-javaformat/spring-javaformat-config/src/main/resources/intellij/Intellij-Spring-Java-Conventions.xml
   ```

2. IDEA → Settings → Editor → Code Style → Java
3. 点击齿轮图标 → Import Scheme → IntelliJ IDEA code style XML
4. 选择下载的 XML 文件

**快捷键**：

- **格式化当前文件**：`Ctrl + Alt + L` (Windows/Linux) 或 `Cmd + Option + L` (Mac)
- **优化Import**：`Ctrl + Alt + O` (Windows/Linux) 或 `Ctrl + Option + O` (Mac)

**自动保存时格式化**（可选）：

1. Settings → Tools → Actions on Save
2. 勾选 `Reformat code`
3. 勾选 `Optimize imports`

---

### 开发流程

**代码提交前必做**：

```bash
# Step 1: 格式化代码
mvn spring-javaformat:apply

# Step 2: 检查格式
mvn spring-javaformat:validate

# Step 3: 如果检查通过，提交代码
git add .
git commit -m "feat: 添加用户查询功能"
```

**CI/CD集成**（可选）：

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up JDK
        uses: actions/setup-java@v2
        with:
          java-version: '8'
      - name: Check code format
        run: mvn spring-javaformat:validate
      - name: Build
        run: mvn clean install
```

---

### 核心风格规则

**缩进与空格**：

```java
// ✅ 使用Tab缩进（等同于4个空格）
public class UserService {

    private IUserMapper userMapper;  // 类成员之间空一行

    public User getUser(String id) {
        if (id == null) {  // if后有空格，括号内无空格
            return null;
        }
        return userMapper.selectById(id);
    }
}
```

**行宽限制**：

```java
// ✅ 每行最多120字符
// ✅ 超长方法调用自动换行并缩进
ResponseResult<User> result = userDubboApi
        .getUserInfo(userId, includeDetail, includeRoles);

// ✅ 超长参数列表换行
public ResponseResult<PageInfo<Order>> queryOrders(
        String userId, String orderNo, Integer status,
        Date startTime, Date endTime) {
    // ...
}
```

**Import语句**：

```java
// ✅ 按字母顺序排序
// ✅ 静态导入在前，普通导入在后
// ✅ 不同包之间空行分隔
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import cn.city.parking.common.core.web.domain.ResponseResult;
import cn.city.parking.user.api.entity.User;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
```

**大括号位置**：

```java
// ✅ 左大括号不换行
public void method() {
    if (condition) {
        // ...
    }
    else {  // else不与右大括号同行
        // ...
    }
}

// ✅ 单行语句也要大括号
if (user == null) {
    return null;
}
```

**空格使用**：

```java
// ✅ 关键字后有空格
if (condition) { }
for (int i = 0; i < 10; i++) { }
while (condition) { }

// ✅ 运算符两侧有空格
int result = a + b * c;
boolean flag = (x > 0) && (y < 100);

// ❌ 方法名和括号之间无空格
method();  // 正确
method ();  // 错误
```

**空行使用**：

```java
public class UserService {
    // ✅ 类成员之间空一行
    private IUserMapper userMapper;

    private RedisUtils redisUtils;

    // ✅ 方法之间空一行
    public User getUser(String id) {
        // ...
    }

    public List<User> listUsers() {
        // ...
    }
}
```

---

### 常见格式化问题

**问题1：格式化后代码冲突**

```java
// ❌ 避免在同一行写多个语句
int a = 1; int b = 2;

// ✅ 每个语句单独一行
int a = 1;
int b = 2;
```

**问题2：注释格式**

```java
// ✅ 单行注释后有空格
// 这是注释

// ❌ 无空格
//这是注释

/**
 * ✅ JavaDoc注释格式正确
 *
 * @param id 用户ID
 * @return 用户信息
 */
public User getUser(String id) {
    // ...
}
```

**问题3：长字符串换行**

```java
// ✅ 长字符串使用 + 连接符换行
String message = "这是一个很长的错误提示信息，"
        + "为了可读性，我们将它分成多行显示，"
        + "每行不超过120字符";

// ⚠️ 或使用文本块（Java 15+）
String sql = """
        SELECT id, username, phone
        FROM sys_user
        WHERE status = 1
        """;
```

**问题4：与现有代码的兼容**

**策略**：
1. ✅ **新代码**严格遵循 Spring Java Format
2. ⚠️ **修改旧代码**时，只格式化修改的部分（避免大面积diff）
3. ✅ **重构模块**时，整体格式化

**IDEA 配置（只格式化修改部分）**：
```
Settings → Editor → Code Style → Formatter
勾选：Only format changed lines
```

---

### 代码审查清单

提交代码前检查：

- [ ] 代码已使用 `mvn spring-javaformat:apply` 格式化
- [ ] `mvn spring-javaformat:validate` 检查通过
- [ ] Import 语句已优化（无未使用的导入）
- [ ] 单行不超过120字符
- [ ] 没有多余的空行或空格
- [ ] 注释格式正确
- [ ] 大括号位置正确
- [ ] 空格使用符合规范

---

### 参考资源

- **官方文档**：https://github.com/spring-io/spring-javaformat
- **Maven插件**：https://docs.spring.io/spring-javaformat/docs/current/reference/html/
- **IDEA插件**：https://plugins.jetbrains.com/plugin/15957-spring-java-format
- **代码示例**：参考 Spring Framework 源码

---

## 附录

### 常见问题

**Q1：为什么Server模块要禁止发布到Maven私库？**

A：Server模块是可执行的应用程序，只用于部署运行，不需要被其他模块依赖。只有API模块才需要发布到Maven私库供其他服务依赖。

**Q2：为什么bootstrap.yml要使用占位符？**

A：使用占位符可以将配置集中管理在Nacos配置中心，方便多环境配置切换（开发、测试、生产），无需修改代码。

**Q3：为什么主键ID使用VARCHAR(64)而不是INT自增？**

A：分布式环境下，自增ID会导致主键冲突。雪花算法生成的ID是Long类型（19位数字），使用VARCHAR(64)存储可以避免精度丢失。

**Q4：为什么要使用Spring Java Format？**

A：统一代码风格可以提高代码可读性，减少代码审查时的格式争议，方便团队协作。Spring Java Format是Spring官方推荐的代码风格，经过大量项目验证。

**Q5：数据库字段create_time和update_time为什么要设置默认值？**

A：设置默认值可以避免忘记填充时间字段，数据库层面自动处理。同时框架的`MyMetaObjectHandler`也会自动填充，双重保障。

---

## 总结

本文档涵盖了City Parking框架的所有配置规范：

1. **POM配置**：父POM继承、API模块依赖、Server模块完整配置
2. **YAML配置**：bootstrap.yml配置、Nacos配置中心使用
3. **数据库规范**：必备字段、可选字段、表设计规范、索引规范
4. **Spring Java Format**：Maven配置、IDEA配置、核心风格规则

遵循这些规范可以确保项目结构清晰、配置统一、代码风格一致，提高开发效率和代码质量。
