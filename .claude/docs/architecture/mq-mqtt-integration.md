# MQ/MQTT集成

## RocketMQ自动traceId传递

### 生产者
**实现位置**：`RocketMQTemplateHandle.buildMessage()` Line 177-181

框架自动从MDC获取traceId并放入消息属性：
```java
String traceId = MDC.get("traceId");
message.putUserProperty("traceId", traceId);
```

### 消费者
**实现位置**：`AbstractRocketMqConsumerSupport.consume()` Line 34-38

框架自动从消息属性提取traceId并放入MDC：
```java
String traceId = message.getUserProperties("traceId");
MDC.put("traceId", traceId);
```

### 使用方式
```java
// 生产者：直接发送，框架自动添加traceId
rocketMQHandle.send(topic, tags, content);

// 消费者：继承基类，框架自动提取traceId
public class MyConsumer extends AbstractRocketMqConsumerSupport {
    @Override
    public Boolean consume(RocketMQConsumerMessage message) {
        // MDC中自动有traceId
        log.info("消费消息：{}", message.getContent());
        return true;
    }
}
```

## MQTT自动traceId传递

### 实现位置
- `MqttAutoConfig.run()` Line 244-266
- `MQTTMsgListener.invoke()` Line 34-42

### 工作原理
1. 接收MQTT消息时，从MDC获取或创建traceId
2. 如果启用Disruptor，将traceId放入队列
3. Disruptor消费线程从队列提取traceId并放入MDC

### 使用方式
```java
// 实现消息处理器
public class MyMqttHandler implements CustomMqttMessageReceiverHandler {
    @Override
    public void handleMessage(Message<?> message) {
        // MDC中自动有traceId
        log.info("处理MQTT消息");
    }
}
```
