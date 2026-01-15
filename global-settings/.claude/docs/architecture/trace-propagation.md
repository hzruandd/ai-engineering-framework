# 链路追踪实现原理

## 概述

City Parking 框架实现了全自动的分布式链路追踪，开发者无需手动操作MDC。本文档详细说明实现原理和关键组件。

## 核心技术栈

| 组件 | 版本 | 作用 |
|-----|------|-----|
| transmittable-thread-local | 阿里巴巴TTL | 线程池间传递ThreadLocal |
| logback-mdc-ttl | 1.0.2 | 配合TTL的MDC监听器 |
| MDCTraceUtils | 框架工具类 | MDC操作工具 |

## 链路追踪流程

### 完整调用链示例

```
用户请求 → BFF → OrderService → StockService
         ↓       ↓              ↓
      traceId  traceId       traceId
      abc123   abc123        abc123
```

整个调用链使用同一个traceId，便于日志聚合和问题排查。

## 核心组件详解

### 1. TraceFilter (common-auth包)

**文件位置**：`city-parking-common-auth/src/main/java/cn/city/parking/common/auth/filter/TraceFilter.java`

**执行时机**：每次HTTP请求进入时

**核心逻辑**：
```java
@Order(-2)
public class TraceFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain) {
        try {
            // 1. 从请求头获取traceId
            String traceId = request.getHeader(MDCTraceUtils.TRACE_ID_HEADER);  // "x-traceId-header"

            // 2. 如果没有，创建新的traceId
            if (StringUtils.isBlank(traceId)) {
                traceId = MDC.get(MDCTraceUtils.KEY_TRACE_ID);
            }

            if (StringUtils.isNotBlank(traceId)) {
                MDCTraceUtils.putTraceId(ServletUtils.urlDecode(traceId));
            } else {
                MDCTraceUtils.addTraceId();  // 创建UUID
            }

            // 3. 获取其他上下文信息
            String from = request.getHeader(SecurityConstants.FROM_SOURCE);
            MDCTraceUtils.putPlatform(from);

            String clientIP = ServletUtil.getClientIP(request);
            MDC.put("clientIP", clientIP);

            // 4. 继续处理请求
            filterChain.doFilter(new MyRequestWrapper(request), response);
        } finally {
            // 5. 请求结束，清理MDC
            MDCTraceUtils.removeTrace();
            SecurityContextHolder.remove();
        }
    }
}
```

**关键点**：
- `@Order(-2)`：优先级很高，确保最先执行
- 请求头名称：`x-traceId-header`
- 自动创建UUID：`IdUtil.simpleUUID()`
- finally块清理：避免线程池复用导致的MDC污染

### 2. ConsumerDubboFilter (common-dubbo包)

**文件位置**：`city-parking-common-dubbo/src/main/java/cn/city/parking/common/dubbo/filter/ConsumerDubboFilter.java`

**执行时机**：Dubbo消费方调用远程服务前

**核心逻辑**：
```java
@Activate(group = {CommonConstants.CONSUMER})
public class ConsumerDubboFilter implements org.apache.dubbo.rpc.Filter {

    @Override
    public Result invoke(Invoker<?> invoker, Invocation invocation) {
        try {
            Map<String, Object> attachments = invocation.getObjectAttachments();

            // 传递日志追踪信息
            String trace = MDCTraceUtils.getTrace();  // 序列化为JSON
            if (StringUtils.isNotEmpty(trace) && !"{}".equals(trace)) {
                attachments.put(MDCTraceUtils.TRACE_HEADER, trace);  // "x-trace-header"
            }

            // 传递其他上下文
            Map<String, Object> localMap = SecurityContextHolder.getLocalMap();
            attachments.put(SecurityConstants.THREAD_LOCAL_MAP, localMap);

            return invoker.invoke(invocation);
        } finally {
            // ❌ 注意：消费方不清理MDC（需要保留在当前线程）
            // MDCTraceUtils.removeTrace();
        }
    }
}
```

**关键点**：
- 通过Dubbo的attachment机制传递
- 序列化LogTrace对象为JSON
- 消费方不清理MDC（因为还在同一个线程中）

### 3. ProviderDubboFilter (common-dubbo包)

**文件位置**：`city-parking-common-dubbo/src/main/java/cn/city/parking/common/dubbo/filter/ProviderDubboFilter.java`

**执行时机**：Dubbo提供方接收到调用时

**核心逻辑**：
```java
@Activate(group = {CommonConstants.PROVIDER})
public class ProviderDubboFilter implements org.apache.dubbo.rpc.Filter {

    @Override
    public Result invoke(Invoker<?> invoker, Invocation invocation) {
        try {
            // 1. 从attachment获取trace信息
            String trace = (String)invocation.getObjectAttachment(MDCTraceUtils.TRACE_HEADER);

            if (StringUtils.isBlank(trace)) {
                // 如果没有传递，创建新的traceId
                MDCTraceUtils.addTraceId();
            } else {
                // 解析JSON并放入MDC
                MDCTraceUtils.build(trace);
            }

            // 2. 获取其他上下文
            Map map = (Map) invocation.getObjectAttachment(SecurityConstants.THREAD_LOCAL_MAP);
            SecurityContextHolder.setLocalMap(map);
            MDC.put("clientIP", SecurityContextHolder.get("clientIP"));

            // 3. 执行业务逻辑
            return invoker.invoke(invocation);
        } finally {
            // 4. 清理上下文
            SecurityContextHolder.remove();
            MDCTraceUtils.removeTrace();
        }
    }
}
```

**关键点**：
- 提供方必须清理MDC（因为Dubbo线程池会复用线程）
- 如果没有传递traceId，会创建新的（兜底机制）
- 使用`MDCTraceUtils.build()`解析JSON

### 4. MDCTraceUtils工具类

**文件位置**：`city-parking-common-core/src/main/java/cn/city/parking/common/core/utils/MDCTraceUtils.java`

**核心方法**：

```java
public class MDCTraceUtils {

    public static final String KEY_TRACE_ID = "traceId";
    public static final String USERNAME = "username";
    public static final String PLATFORM = "platform";
    public static final String TRACE_ID_HEADER = "x-traceId-header";
    public static final String TRACE_HEADER = "x-trace-header";

    // 创建traceId
    public static String createTraceId() {
        return IdUtil.simpleUUID();  // Hutool的UUID工具
    }

    // 获取完整追踪信息（序列化为JSON）
    public static String getTrace() {
        LogTrace logTrace = new LogTrace();
        logTrace.setTraceId(getTraceId());
        logTrace.setUsername(getUsername());
        logTrace.setPlatform(getPlatform());
        return JSON.toJSONString(logTrace);
    }

    // 解析追踪信息（从JSON反序列化）
    public static void build(String traceJsonStr) {
        if (StringUtils.isNotBlank(traceJsonStr)) {
            LogTrace logTrace = JSONUtil.toBean(traceJsonStr, LogTrace.class);
            MDCTraceUtils.putTraceId(logTrace.getTraceId());
            if (StringUtils.isNotBlank(logTrace.getUsername())) {
                MDCTraceUtils.putUsername(logTrace.getUsername());
            }
            if (StringUtils.isNotBlank(logTrace.getPlatform())) {
                MDCTraceUtils.putPlatform(logTrace.getPlatform());
            }
        }
    }

    // 清理MDC
    public static void removeTrace() {
        MDC.clear();
    }
}
```

### 5. LogTrace实体类

**文件位置**：`city-parking-common-core/src/main/java/cn/city/parking/common/core/domain/LogTrace.java`

```java
@Data
public class LogTrace implements Serializable {
    private String traceId;    // 追踪ID
    private String username;   // 用户名
    private String platform;   // 平台
    private String version;    // 版本号
}
```

## 异步场景的链路追踪

### TTL线程池自动传递

**核心技术**：阿里巴巴 TransmittableThreadLocal (TTL)

**配置位置**：
- `ExecutePoolConfiguration.java` - 配置TTL线程池
- `logback-spring.xml` - 配置TtlMdcListener

**TTL线程池Bean定义**：
```java
@Bean(value = "ttlExecutorService", destroyMethod = "shutdown")
public ExecutorService getExecutorService(ThreadPoolTaskExecutor threadPoolTaskExecutor) {
    // 使用TtlExecutors包装普通线程池
    return TtlExecutors.getTtlExecutorService(threadPoolTaskExecutor.getThreadPoolExecutor());
}
```

**@Async默认配置**：
```java
@Bean
public AsyncConfigurer getTTLAsyncConfigurer(@Qualifier("ttlExecutorService") ExecutorService executorService){
    return new AsyncConfigurer(){
        @Override
        public Executor getAsyncExecutor() {
            // @Async默认使用TTL线程池，自动传递MDC
            return TtlExecutors.getTtlExecutorService(executorService);
        }
    };
}
```

**logback-spring.xml配置**：
```xml
<configuration>
    <!-- TtlMdcListener：监听MDC变化，配合TTL实现自动传递 -->
    <contextListener class="com.ofpay.logback.TtlMdcListener"/>

    <!-- 日志格式包含MDC变量 -->
    <property name="FILE_LOG_PATTERN"
              value="[%X{clientIP}] [%X{traceId}] [%X{username}] [%X{platform}] - %msg%n"/>
</configuration>
```

**工作原理**：
1. `TtlMdcListener`监听MDC的put/remove操作
2. 将MDC的值存储到TransmittableThreadLocal中
3. `TtlExecutors`在提交任务时，自动将父线程的TTL值传递给子线程
4. 子线程执行时，自动恢复MDC的值

**使用示例**：
```java
@Autowired
@Qualifier("ttlExecutorService")
private ExecutorService ttlExecutorService;

public void asyncTask() {
    // 父线程有traceId
    String parentTraceId = MDCTraceUtils.getTraceId();  // "abc123"

    // 提交异步任务
    ttlExecutorService.execute(() -> {
        // 子线程自动获得父线程的MDC
        String childTraceId = MDCTraceUtils.getTraceId();  // "abc123"（相同！）
        log.info("异步任务执行");  // 日志自动包含traceId
    });
}
```

### RocketMQ消息传递

**生产者实现位置**：`RocketMQTemplateHandle.buildMessage()`

```java
private Message buildMessage(String topic, String content, String tags) {
    org.apache.rocketmq.common.message.Message m = new org.apache.rocketmq.common.message.Message();
    m.setBody(content.getBytes());
    m.setTags(tags);
    m.setTopic(topic);

    // 从MDC获取traceId并放入消息属性
    String traceId = MDC.get("traceId");
    if (!StringUtils.hasText(traceId)) {
        traceId = UUID.randomUUID().toString().replace("-", "");
    }
    m.putUserProperty("traceId", traceId);  // ← 关键！

    return RocketMQUtil.convertToSpringMessage(m);
}
```

**消费者实现位置**：`AbstractRocketMqConsumerSupport.consume()`

```java
@Override
public Action consume(Message message, ConsumeContext consumeContext) {
    String body = new String(message.getBody(), StandardCharsets.UTF_8);
    try {
        // 从消息属性提取traceId
        String traceId = message.getUserProperties("traceId");  // ← 关键！
        if (!StringUtils.hasText(traceId)) {
            traceId = UUID.randomUUID().toString().replace("-", "");
        }
        MDC.put("traceId", traceId);
    } catch (Exception e) {
        log.error("获取traceId异常", e);
    }

    try {
        // 执行业务逻辑
        Boolean consume = consume(rocketMQConsumerMessage);
        return consume != null && consume ? Action.CommitMessage : Action.ReconsumeLater;
    } finally {
        // 清理MDC
        MDC.clear();
    }
}
```

### MQTT消息传递

**实现位置**：`MqttAutoConfig.run()`

```java
private boolean run(CustomMqttMessageReceiverHandler handler, Message<?> message, String topic, boolean disruptor) {
    try {
        // 获取或创建traceId
        String traceId = MDC.get("traceId");
        if (!StringUtils.hasText(traceId)) {
            traceId = UUID.randomUUID().toString().replaceAll("-", "");
            MDC.put("traceId", traceId);
        }

        if (disruptor && Objects.nonNull(parallelQueueHandler)) {
            // 使用Disruptor队列处理
            DisruptorEventData data = new DisruptorEventData();
            Map<String, Object> map = new HashMap<>();
            map.put("data", message);
            map.put("handler", handler);
            map.put("traceId", traceId);  // ← 传递traceId
            data.setMessage(map);
            parallelQueueHandler.add(data);
        } else {
            handler.handleMessage(message);
        }
        return true;
    } catch (Exception e) {
        log.error("处理MQTT消息出错", e);
        return false;
    } finally {
        MDC.clear();
    }
}
```

**Disruptor消费者**：`MQTTMsgListener.invoke()`

```java
@Override
protected void invoke(Map<?, ?> map) {
    // 从Map中提取traceId
    String traceId = (String)map.get("traceId");
    MDC.put("traceId", traceId);  // ← 恢复traceId

    Message<?> message = (Message)map.get("data");
    CustomMqttMessageReceiverHandler handler = (CustomMqttMessageReceiverHandler)map.get("handler");

    try {
        handler.handleMessage(message);
    } finally {
        MDC.clear();
    }
}
```

## 日志配置

**logback-spring.xml日志格式**：

```xml
<property name="FILE_LOG_PATTERN"
          value="%date{yyyy-MM-dd HH:mm:ss} [%-5level] [%X{clientIP}] [%X{tid}] [%X{platform}] [%X{version}] [%X{traceId}] [%X{username}] [%thread] [%logger{80}] [%file:%line] [%method] >>>>>> %msg%n"/>
```

**日志输出示例**：
```
2025-01-03 10:30:00 [INFO] [192.168.1.100] [] [cloud-eop] [v1.0.0] [abc123def456] [admin] [http-nio-8080-exec-1] [OrderService] [OrderServiceImpl.java:45] [createOrder] >>>>>> 创建订单成功，订单号：P202501030001
```

**MDC变量说明**：
- `%X{clientIP}`：客户端IP
- `%X{traceId}`：链路追踪ID
- `%X{username}`：用户名
- `%X{platform}`：平台来源（cloud-eop、app等）
- `%X{version}`：版本号

## 常见问题排查

### 问题1：Dubbo调用后traceId丢失

**现象**：
```
BFF日志：[traceId:abc123] 调用订单服务
订单服务日志：[traceId:] 创建订单  ← traceId为空
```

**可能原因**：
1. ProviderDubboFilter未生效
2. attachment传递失败
3. JSON序列化/反序列化失败

**排查步骤**：
```java
// 1. 检查ConsumerDubboFilter是否执行
// 在ConsumerDubboFilter.invoke()中打断点，查看attachment是否包含trace信息

// 2. 检查ProviderDubboFilter是否执行
// 在ProviderDubboFilter.invoke()中打断点，查看是否接收到trace

// 3. 检查JSON格式
String trace = invocation.getObjectAttachment(MDCTraceUtils.TRACE_HEADER);
System.out.println("Received trace: " + trace);
// 应该输出：{"traceId":"abc123","username":"admin","platform":"cloud-eop"}
```

### 问题2：异步任务traceId丢失

**现象**：
```
主线程：[traceId:abc123] 提交异步任务
异步线程：[traceId:] 执行任务  ← traceId为空
```

**可能原因**：
1. 使用了普通线程池（myThreadPoolTaskExecutor）而非TTL线程池
2. TtlMdcListener未配置
3. @Async指定了错误的线程池

**解决方案**：
```java
// ❌ 错误：使用普通线程池
@Async("myThreadPoolTaskExecutor")
public void task() { }

// ✅ 正确：不指定线程池（默认使用ttlExecutorService）
@Async
public void task() { }

// ✅ 或显式指定TTL线程池
@Autowired
@Qualifier("ttlExecutorService")
private ExecutorService ttlExecutorService;

ttlExecutorService.execute(() -> { });
```

### 问题3：RocketMQ消息traceId丢失

**现象**：
```
生产者：[traceId:abc123] 发送消息
消费者：[traceId:] 处理消息  ← traceId为空
```

**可能原因**：
1. 生产者未调用框架的send方法
2. 消费者未继承AbstractRocketMqConsumerSupport
3. 消息属性传递失败

**排查步骤**：
```java
// 1. 检查生产者是否使用框架方法
// ✅ 正确
rocketMQHandle.send(topic, tags, content);

// ❌ 错误：直接使用RocketMQTemplate
rocketMQTemplate.syncSend(topic, content);  // 不会自动添加traceId

// 2. 检查消费者是否继承基类
// ✅ 正确
public class MyConsumer extends AbstractRocketMqConsumerSupport { }

// ❌ 错误：直接实现RocketMQListener
public class MyConsumer implements RocketMQListener<String> { }
```

### 问题4：MDC内存泄漏

**现象**：
- 服务运行一段时间后内存持续增长
- GC频繁但内存无法释放

**可能原因**：
- Filter或Dubbo Filter中未正确清理MDC
- 线程池线程复用但MDC未清理

**检查清理逻辑**：
```java
// ✅ 正确：使用finally确保清理
public void doFilter(...) {
    try {
        MDC.put("traceId", traceId);
        // ...
    } finally {
        MDC.clear();  // ← 必须清理！
    }
}

// ❌ 错误：没有清理
public void doFilter(...) {
    MDC.put("traceId", traceId);
    // ...
    // 忘记清理，导致线程池复用时MDC污染
}
```

## 扩展开发

### 自定义传递更多上下文

**需求**：在链路中传递自定义字段（如租户ID）

**步骤1：扩展LogTrace**
```java
@Data
public class LogTrace implements Serializable {
    private String traceId;
    private String username;
    private String platform;
    private String tenantId;  // ← 新增字段
}
```

**步骤2：修改MDCTraceUtils**
```java
public static final String TENANT_ID = "tenantId";

public static String getTrace() {
    LogTrace logTrace = new LogTrace();
    logTrace.setTraceId(getTraceId());
    logTrace.setUsername(getUsername());
    logTrace.setPlatform(getPlatform());
    logTrace.setTenantId(getTenantId());  // ← 新增
    return JSON.toJSONString(logTrace);
}

public static void build(String traceJsonStr) {
    LogTrace logTrace = JSONUtil.toBean(traceJsonStr, LogTrace.class);
    MDCTraceUtils.putTraceId(logTrace.getTraceId());
    MDCTraceUtils.putUsername(logTrace.getUsername());
    MDCTraceUtils.putPlatform(logTrace.getPlatform());
    MDCTraceUtils.putTenantId(logTrace.getTenantId());  // ← 新增
}
```

**步骤3：更新日志格式**
```xml
<property name="FILE_LOG_PATTERN"
          value="... [%X{traceId}] [%X{tenantId}] ..."/>
```

### 集成第三方链路追踪系统

**需求**：集成Skywalking、Zipkin等APM系统

**方案**：在TraceFilter中同时设置APM的traceId

```java
public class TraceFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(...) {
        try {
            String traceId = MDCTraceUtils.addTraceId(request);

            // 同时设置Skywalking的traceId
            TraceContext.traceId().set(traceId);

            filterChain.doFilter(request, response);
        } finally {
            MDCTraceUtils.removeTrace();
            TraceContext.traceId().remove();
        }
    }
}
```

## 总结

City Parking框架的链路追踪机制通过以下组件实现全自动传递：

1. **HTTP层**：TraceFilter自动从请求头读取或创建traceId
2. **Dubbo层**：ConsumerDubboFilter + ProviderDubboFilter通过attachment传递
3. **异步层**：TTL + TtlMdcListener实现线程池间自动传递
4. **MQ层**：消息属性传递traceId
5. **日志层**：logback-spring.xml统一格式输出

开发者在99%的场景下无需关心实现细节，框架自动处理。只有在以下情况需要查阅本文档：
- 遇到traceId丢失问题
- 需要扩展自定义上下文
- 集成第三方APM系统
- 理解框架设计进行二次开发
