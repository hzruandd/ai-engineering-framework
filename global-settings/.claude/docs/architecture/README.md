# 架构设计文档

本目录包含 City Parking 微服务框架的详细架构设计文档。

## 📚 文档列表

### 核心机制
- [链路追踪实现原理](trace-propagation.md) - TraceFilter、DubboFilter、TTL传递机制
- [线程池设计](thread-pool-design.md) - 3个线程池的实现和选择
- [缓存设计](cache-design.md) - Redis缓存策略、防击穿/穿透/雪崩

### 分布式能力
- [分布式事务](distributed-transaction.md) - 可靠消息最终一致性方案
- [MQ/MQTT集成](mq-mqtt-integration.md) - RocketMQ、MQTT消息处理

## 📖 阅读指南

### 业务开发者
- 正常开发只需阅读 `.claude/CLAUDE.md`
- 遇到问题时根据指引查阅对应文档

### 架构师/高级开发者
- 建议完整阅读所有架构文档
- 理解框架设计思路和最佳实践

### 问题排查
遇到问题时，根据现象查阅对应文档：

| 问题现象 | 查阅文档 |
|---------|---------|
| traceId丢失、链路断开 | [链路追踪原理](trace-propagation.md) |
| 缓存穿透、击穿、雪崩 | [缓存设计](cache-design.md) |
| 异步任务上下文丢失 | [线程池设计](thread-pool-design.md) |
| 分布式事务失败 | [分布式事务](distributed-transaction.md) |
| MQ/MQTT消息丢失 | [MQ/MQTT集成](mq-mqtt-integration.md) |

## 🔧 二次开发
需要基于框架进行定制开发时，这些文档提供了：
- 核心组件的实现位置
- 扩展点说明
- 最佳实践参考
