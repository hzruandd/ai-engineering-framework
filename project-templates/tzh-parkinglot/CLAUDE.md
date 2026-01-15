# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 提供在此代码库中工作的指导。

## 项目概述

这是一个基于 Spring Boot 和 Dubbo 微服务架构构建的**多模块停车场管理系统**。系统处理停车场运营，包括车辆进出、费用计算、月卡管理、设备集成和业务运营。

父 POM: `tzh-parent` v1.0.1-SNAPSHOT

## 模块结构

代码库包含 6 个独立模块（每个都有自己的 git 仓库）：

### 核心停车系统
- **tzh-parkinglot/** - 主停车场管理系统
  - `tzh-parkinglot-servicei/` - 服务接口和 DTOs
  - `tzh-parkinglot-service/` - 服务实现（约 1,598 个 Java 文件）
  - 入口点: `com.tzh.parkinglot.service.ServerApp`

### 支持模块
- **tzh-monthlycar/** - 月租车子系统
  - `tzh-monthlycar-servicei/` - 服务接口
  - `tzh-monthlycar-service/` - 服务实现

- **tzh-parkinglot-web/** - Web/BFF 层，提供 REST APIs
  - 入口点: `com.tzh.parkinglot.parkinglotweb.ParkingLotWebApplication`

- **city-parking-business/** - 业务运营模块（独立父模块: city-parking-parent v2.0.0-SNAPSHOT）
  - `city-parking-business-api/` - API 契约
  - `city-parking-business-server/` - 业务服务器实现
  - 入口点: `cn.city.parking.business.CityParkingBusinessServerApplication`
  - 端口: 9225

- **tzh-common-dao/** - 共享 DAO 层，包含 MyBatis mappers（199 个 XML mapper 文件）

- **tzh-applet-api/** - 微信小程序 API

## 架构模式

### 分层架构
```
Web 层 (tzh-parkinglot-web)
    ↓ REST API
服务接口层 (-servicei 模块) - DTOs 和契约
    ↓ Dubbo RPC
服务实现层 (-service 模块) - 业务逻辑
    ↓ MyBatis
DAO 层 (tzh-common-dao) - Mappers
    ↓
数据库 (MySQL via Druid)
```

### 服务通信
- **Dubbo 3.x RPC**: 服务通过 `@DubboService` 暴露，通过 `@DubboReference` 消费
- **Nacos**: 服务发现和配置管理
- **Seata**: 分布式事务协调（当前已启用）
- **Sentinel**: 熔断和流控，规则源为 Nacos

## 技术栈

- **框架**: Spring Boot 2.5.7 - 2.7.0, Spring Cloud Alibaba
- **RPC**: Apache Dubbo 3.x，带自定义 GAEA 库封装
- **数据库**: MySQL + MyBatis 3.5.7, Druid 连接池
- **服务网格**: Nacos (服务发现 + 配置), Sentinel (熔断器)
- **事务**: Seata 分布式事务
- **消息队列**: RabbitMQ (spring-boot-starter-amqp)
- **工具库**: Hutool, Lombok, Jackson
- **日志**: Logback + GELF 集成，用于集中式日志
- **API 文档**: Swagger/Springfox 3.0.0

### 外部设备集成
系统集成了多个停车设备厂商：
- 海康威视: `city-parking-hk-api`, `city-parking-hk-upapi`
- 芊熠: `city-parking-qy-api`, `city-parking-qy-upapi`
- HKPlus: `city-parking-hkplus-api`, `city-parking-hkplus-upapi`
- HK Robot: `city-parking-hkrobot-api`, `city-parking-hkrobot-upapi`
- Ice SDK: 华夏开放平台 (v1.1.5-SNAPSHOT)

## 构建和运行命令

### 构建
```bash
# 构建所有模块
mvn clean package

# 构建特定模块
cd tzh-parkinglot && mvn clean package
cd tzh-parkinglot-web && mvn clean package
cd city-parking-business && mvn clean package

# 跳过测试
mvn clean package -DskipTests
```

### 运行应用
```bash
# 运行停车场服务
cd tzh-parkinglot/tzh-parkinglot-service
java -jar target/tzh-parkinglot-service.jar

# 运行 Web 应用
cd tzh-parkinglot-web
java -jar target/tzh-parkinglot-web.jar

# 运行业务服务器（端口 9225）
cd city-parking-business/city-parking-business-server
java -jar target/city-parking-business.jar
```

### 测试
```bash
# 运行特定模块的测试
cd tzh-parkinglot/tzh-parkinglot-service
mvn test

# 运行单个测试类
mvn test -Dtest=YourTestClass

# 运行单个测试方法
mvn test -Dtest=YourTestClass#testMethod
```

## 配置

### 环境配置文件
应用通过 bootstrap-{profile}.yml 支持多环境：
- `dev` - 开发环境
- `test` - 测试环境
- `ready` - 预生产环境
- `prod` - 生产环境

通过 Maven profile 激活: `@profileActive@`

### Nacos 配置
所有服务使用 Nacos 进行：
- **服务发现**: 动态服务注册/发现
- **配置管理**: 共享配置，支持动态刷新
  - `application-{profile}.yml` - 应用特定配置
  - `common-{profile}.yml` - 公共共享配置
- **Sentinel 规则**: 流控、熔断、系统、授权、热点参数规则

### 数据库配置
- **主数据源**: MySQL via Druid（在 Nacos 中配置）
- **MyBatis Mapper 扫描**: `com.tzh.common.dao.mapper.*`
- **Mapper XML 位置**: `src/main/resources/mapper/`
- **ShardingSphere**: 可用但当前已注释（用于读写分离）

## 核心业务域

### 停车运营 (tzh-parkinglot-service)
- **车辆进出**: `carInto`、`appearanceProcessing` 方法（详见 .claude/skills/parking-in-out/reference/）
- **费用计算**: `parkingCalculationFee` 方法，带优惠折扣系统（详见 .claude/skills/parking-in-out/reference/）
- **设备推送**: `devicePushInfo` 方法，用于设备事件处理（详见 .claude/skills/parking-in-out/reference/）
- **场中场**: 嵌套停车场业务逻辑

### 可用的 Claude Skills
本项目配置了专门的 skills 来辅助开发:
- **parking-in-out**: 停车场出入车业务专家，处理车辆入场、出场、计费逻辑
  - 位置: `.claude/skills/parking-in-out/`
  - 包含详细的方法文档和最佳实践
  - 调用方式: 在需要处理出入车相关需求时会自动推荐使用

### 月卡管理 (tzh-monthlycar)
- VIP 卡生命周期管理
- 充值记录和历史跟踪
- 租赁模板和优惠规则
- 储值卡和生命周期管理

## 组件扫描

主服务应用（`ServerApp.java`）扫描：
```java
@ComponentScan({
    "com.tzh.common",
    "com.tzh.parkinglot.service",
    "com.tzh.auth",
    "com.tzh.parkinglot.service.task"
})
@MapperScan({"com.tzh.common.dao.mapper.*"})
@EnableDubbo
@EnableScheduling
@EnableAspectJAutoProxy(exposeProxy = true)
```

## 定时任务
系统具有以下后台任务：
- 设备异步操作（`DeviceAsyncServiceImpl`）
- 停车场统计（`ParkingLotStatisticsTaskServiceImpl`）
- 每日统计聚合（`DayStatisticsTaskServiceImpl`）

## 重要说明

### 安全注意事项
修改支付或访问控制逻辑时，请查看 `业务风险记录.md` 了解已知安全风险，特别是问题 #1766115372 关于已付款车辆开闸漏洞。

### 数据库实体
关键数据库实体（来自 199 个 mapper 文件）：
- **停车**: ParkingInfo, ParkingOrder, ParkingRecord, ParkingBillingRules
- **月卡**: ParkingVipCarInfo, ParkingRechargeRecord, RentalInfo
- **设备**: ParkingDeviceInfo, DeviceDisplayInfo
- **运营**: OperLog, ParkingCarLabel, ParkingBlacklist
- **用户**: ParkingUserInfo, ParkingUserWxmpRelation（在 business 模块中）

### 日志
应用使用 GaeaLog 封装器，带集中式 GELF 日志：
```java
GaeaLogRegisterUtils.createGaeaLogProperty(
    GaeaLogConstant.PARKINGLOT_PRODUCT_ID,
    GaeaLogConstant.PARKINGLOT_MODULE_ID,
    GaeaLogConstant.PARKINGLOT_NODE_ID
);
```

### Maven 部署
服务实现模块（`tzh-parkinglot-service`、`city-parking-business`）配置了 `maven-deploy-plugin` 的 `<skip>true</skip>` - 它们不会部署到 Maven 私服。

---

## 文档维护指南

### 何时更新文档

**重要原则**: 当相关代码/业务逻辑发生变更或获得新的知识后，必须及时更新以下文档：

1. **CLAUDE.md** - 当以下情况发生时更新:
   - 新增/修改模块结构
   - 技术栈升级或变更
   - 架构模式调整
   - 新增核心业务域
   - 配置方式变更
   - 新增/修改重要说明

2. **CLAUDE-gen.md** - 当以下情况发生时更新:
   - 制定新的编码规范
   - 调整开发流程
   - 引入新的最佳实践
   - 更新安全规范

3. **Skills 文档** (`.claude/skills/`) - 当以下情况发生时更新:
   - 核心业务逻辑变更
   - 修复已知问题或陷阱
   - 发现新的业务场景
   - 优化代码实现方式
   - 新增业务规则或配置项
   - 更新相关方法位置

### 文档更新清单

进行代码修改后，请检查以下内容:

- [ ] 是否影响核心业务流程？→ 更新对应 skill 的 reference 文档
- [ ] 是否修改了方法签名或位置？→ 更新方法索引
- [ ] 是否新增/修改配置项？→ 更新配置说明
- [ ] 是否发现新的陷阱或最佳实践？→ 补充到文档中
- [ ] 是否修改了架构或模块结构？→ 更新 CLAUDE.md
- [ ] 是否制定了新的开发规范？→ 更新 CLAUDE-gen.md

### 文档质量标准

- **准确性**: 文档必须反映当前代码的真实情况
- **完整性**: 包含足够的上下文和示例
- **及时性**: 代码变更后应立即更新文档
- **可读性**: 使用清晰的结构和语言
