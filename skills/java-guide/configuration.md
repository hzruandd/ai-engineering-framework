# 配置规范

本文档包含 POM 配置、YAML 配置、数据库规范等内容。

## 目录

1. [POM 配置](#1-pom-配置)
2. [YAML 配置](#2-yaml-配置)
3. [数据库规范](#3-数据库规范)

---

## 1. POM 配置

### 独立仓库设计说明

- **city-parking-parent**：独立仓库，**必须发布到Maven私库**
- **city-parking-common-xxx**：独立仓库，发布到Maven私库
- **微服务项目**：独立仓库，包含根pom（聚合器）、API模块、Server模块

### 发布策略

- ✅ **发布到Maven私库**：city-parking-parent、common组件、API模块
- ❌ **不发布到Maven私库**：根pom（聚合器）、Server模块

### 根 POM（city-parking-xxx/pom.xml）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>
    <!-- ✅ 根pom的parent是city-parking-parent -->
    <parent>
        <groupId>cn.city-parking</groupId>
        <artifactId>city-parking-parent</artifactId>
        <version>2.0.0-SNAPSHOT</version>
        <relativePath/>
    </parent>

    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-xxx</artifactId>
    <version>2.0.0-SNAPSHOT</version>
    <packaging>pom</packaging>
    <name>city-parking-xxx</name>
    <description>XXX服务</description>

    <!-- ✅ 聚合子模块 -->
    <modules>
        <module>city-parking-xxx-api</module>
        <module>city-parking-xxx-server</module>
    </modules>

    <build>
        <plugins>
            <!-- ✅ 根pom禁止发布到Maven私库 -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-deploy-plugin</artifactId>
                <version>2.8.2</version>
                <configuration>
                    <skip>true</skip>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

### API 模块 POM（city-parking-xxx-api/pom.xml）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>
    <!-- ✅ API模块直接继承city-parking-parent -->
    <!-- ❌ 不要继承根pom（city-parking-xxx） -->
    <parent>
        <groupId>cn.city-parking</groupId>
        <artifactId>city-parking-parent</artifactId>
        <version>2.0.0-SNAPSHOT</version>
        <relativePath/>
    </parent>

    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-xxx-api</artifactId>
    <version>2.0.0-SNAPSHOT</version>
    <packaging>jar</packaging>
    <name>city-parking-xxx-api</name>
    <description>XXX服务API</description>

    <dependencies>
        <!-- ✅ API模块必须依赖city-parking-common-auth -->
        <dependency>
            <groupId>cn.city-parking</groupId>
            <artifactId>city-parking-common-auth</artifactId>
        </dependency>
        <!-- ❌ 错误：不要依赖city-parking-common-core -->
        <!-- common-auth已经包含了common-core -->
    </dependencies>

    <!-- ⚠️ API模块不配置deploy插件，默认会发布到Maven私库 -->
</project>
```

### Server 模块 POM（city-parking-xxx-server/pom.xml）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>
    <!-- ✅ Server模块直接继承city-parking-parent -->
    <!-- ❌ 不要继承根pom（city-parking-xxx） -->
    <parent>
        <groupId>cn.city-parking</groupId>
        <artifactId>city-parking-parent</artifactId>
        <version>2.0.0-SNAPSHOT</version>
        <relativePath/>
    </parent>

    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-xxx-server</artifactId>
    <version>2.0.0-SNAPSHOT</version>
    <packaging>jar</packaging>
    <name>city-parking-xxx-server</name>
    <description>XXX服务实现</description>

    <dependencies>
        <!-- ✅ 1. common-server（已包含Redis、Auth、MySQL、Druid） -->
        <dependency>
            <groupId>cn.city-parking</groupId>
            <artifactId>city-parking-common-server</artifactId>
        </dependency>

        <!-- ✅ 2. 本服务API模块 -->
        <dependency>
            <groupId>cn.city-parking</groupId>
            <artifactId>city-parking-xxx-api</artifactId>
            <version>2.0.0-SNAPSHOT</version>
        </dependency>

        <!-- ❌ 以下依赖不要添加（common-server已包含） -->
        <!-- city-parking-common-redis -->
        <!-- city-parking-common-auth -->
        <!-- mysql-connector-j -->
        <!-- druid-spring-boot-starter -->
    </dependencies>

    <build>
        <plugins>
            <!-- ✅ Spring Boot打包插件（必须配置mainClass） -->
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <version>${spring-boot.version}</version>
                <configuration>
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

            <!-- ✅ 代码格式化插件 -->
            <plugin>
                <groupId>io.spring.javaformat</groupId>
                <artifactId>spring-javaformat-maven-plugin</artifactId>
                <version>0.0.39</version>
            </plugin>
        </plugins>
    </build>
</project>
```

### 为什么 API 和 Server 不继承根 pom？

1. 微服务的根pom（聚合器）不会发布到Maven私库
2. 如果API继承根pom，其他项目引用API时会找不到根pom
3. city-parking-parent已经配置了所有必要的依赖管理
4. 根pom只是一个聚合器，方便本地多模块开发

---

## 2. YAML 配置

### 必须创建的配置文件

- `bootstrap.yml`（主配置）
- `bootstrap-dev.yml`（开发环境）
- `bootstrap-prod.yml`（生产环境）
- `bootstrap-test.yml`（测试环境）

### bootstrap.yml（主配置文件）

⚠️ **关键规范**：
1. 只需修改 `server.port` 和 `spring.application.name`
2. 使用 `@profileActive@` 而非 `${profiles.active:dev}`
3. 使用 `${nacos.server-addr}` 而非 `${custom-config.server.nacos.address}`

```yaml
server:
  port: 9220  # ✅ 1. 修改为你的端口

spring:
  application:
    name: city-parking-xxx  # ✅ 2. 修改为你的服务名
  profiles:
    active: @profileActive@  # ✅ 注意：使用Maven占位符
  main:
    allow-bean-definition-overriding: true
  cloud:
    nacos:
      discovery:
        server-addr: ${nacos.server-addr}  # ✅ 占位符格式
        namespace: ${nacos.namespace}
        group: ${nacos.group}
      config:
        server-addr: ${nacos.server-addr}
        file-extension: yml
        namespace: ${nacos.namespace}
        group: ${nacos.group}
        shared-configs:
          - data-id: application-${spring.profiles.active}.${spring.cloud.nacos.config.file-extension}
            group: ${nacos.group}
            refresh: true
          - data-id: common-${spring.profiles.active}.${spring.cloud.nacos.config.file-extension}
            group: ${nacos.group}
            refresh: true
    sentinel:
      transport:
        dashboard: ${sentinel.server-addr}
      eager: true

dubbo:
  application:
    name: ${spring.application.name}
    qos-enable: false
  registry:
    address: nacos://${spring.cloud.nacos.discovery.server-addr}
    parameters:
      namespace: ${spring.cloud.nacos.discovery.namespace}
```

### bootstrap-dev.yml（开发环境）

```yaml
# 自定义参数（开发环境）
nacos:
  server-addr: @serverAddr@  # ✅ Maven占位符，从pom.xml读取
  namespace: @namespace@
  group: DEFAULT_GROUP
sentinel:
  server-addr: 127.0.0.1:8888
  namespace: sentinel
  group: DEFAULT_GROUP
```

### bootstrap-prod.yml（生产环境）

```yaml
# 自定义参数（生产环境）
nacos:
  server-addr: your-prod-nacos:8848  # ✅ 直接配置生产环境地址
  namespace: prod
  group: DEFAULT_GROUP
sentinel:
  server-addr: your-prod-sentinel:8888
  namespace: sentinel
  group: DEFAULT_GROUP
```

### bootstrap-test.yml（测试环境）

```yaml
# 自定义参数（测试环境）
nacos:
  server-addr: 172.26.145.149:8848
  namespace: test
  group: DEFAULT_GROUP
sentinel:
  server-addr: 172.26.145.190:8089
  namespace: sentinel
  group: DEFAULT_GROUP
```

### 配置说明

- 不同环境通过 `-Dspring.profiles.active=dev/prod/test` 切换
- Maven打包时通过 `-P dev/prod/test` 指定环境，会替换 `@serverAddr@` 等占位符
- bootstrap-{env}.yml 中的配置会覆盖 bootstrap.yml 中的占位符

### 常见错误

- ❌ `profiles.active: ${profiles.active:dev}`（应该是 `@profileActive@`）
- ❌ `server-addr: ${custom-config.server.nacos.address}`（应该是 `${nacos.server-addr}`）
- ❌ 忘记创建环境配置文件

---

## 3. 数据库规范

### 必备字段（BusinessEntity 已包含，无需声明）

```sql
id           VARCHAR(64)   PRIMARY KEY COMMENT '主键（雪花ID）',
create_time  DATETIME      NOT NULL    COMMENT '创建时间',
update_time  DATETIME      NOT NULL    COMMENT '更新时间'
```

### 可选字段（⚠️ 如果使用，必须在实体类中显式声明）

#### 创建人/更新人字段

```sql
create_by    VARCHAR(64)               COMMENT '创建人',
update_by    VARCHAR(64)               COMMENT '更新人'
```

```java
// ✅ 实体类必须声明
@TableField(value = "create_by", fill = FieldFill.INSERT)
private String createBy;

@TableField(value = "update_by", fill = FieldFill.UPDATE)
private String updateBy;
```

#### 逻辑删除字段

```sql
del_flag     TINYINT(1)    DEFAULT 0   COMMENT '删除标志（0-存在，1-删除）'
```

```java
// ✅ 实体类必须声明
@TableField(value = "del_flag", fill = FieldFill.INSERT)
private Integer delFlag;
```

#### 乐观锁字段

```sql
revision     BIGINT(20)    DEFAULT 0   COMMENT '乐观锁版本号'
```

```java
// ✅ 实体类必须声明
@Version
private Long revision;
```

#### 备注字段

```sql
remark       VARCHAR(500)              COMMENT '备注'
```

```java
// ✅ 实体类必须声明
private String remark;
```

### 关键提醒

- BusinessEntity **只包含** id、createTime、updateTime
- create_by、update_by、del_flag、revision **不在基类中**
- 如果数据库表有这些字段，**必须在实体类中显式声明**
- 框架的自动填充功能会处理这些字段，但前提是实体类中有对应属性

---

**文档版本**：1.0
**最后更新**：2026-01-24
