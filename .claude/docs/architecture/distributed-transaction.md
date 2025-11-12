# 分布式事务

## 推荐方案：可靠消息最终一致性

### 本地消息表设计
```sql
CREATE TABLE t_local_message (
    id VARCHAR(64) PRIMARY KEY,
    business_id VARCHAR(64),
    business_type VARCHAR(32),
    message_content TEXT,
    status TINYINT,  -- 0:待发送 1:已发送 2:失败
    retry_count INT DEFAULT 0,
    next_retry_time DATETIME,
    create_time DATETIME
);
```

### Service实现
```java
@Transactional(rollbackFor = Exception.class)
public int createOrder(Order order) {
    // 1. 插入订单（本地事务）
    orderMapper.insert(order);

    // 2. 插入本地消息（同一事务）
    LocalMessage message = new LocalMessage();
    message.setBusinessId(order.getId());
    message.setBusinessType("ORDER_CREATED");
    message.setMessageContent(JSON.toJSONString(order));
    message.setStatus(0);
    localMessageMapper.insert(message);

    return 1;
}
```

### 定时任务发送消息
```java
@Scheduled(fixedDelay = 5000)
public void sendPendingMessages() {
    List<LocalMessage> messages = localMessageMapper.selectPending();
    for (LocalMessage msg : messages) {
        try {
            // 调用下游服务
            stockDubboApi.deductStock(msg.getBusinessId());
            msg.setStatus(1);
            localMessageMapper.updateById(msg);
        } catch (Exception e) {
            // 指数退避重试
            msg.setRetryCount(msg.getRetryCount() + 1);
            long delay = Math.pow(2, msg.getRetryCount()) * 60 * 1000;
            msg.setNextRetryTime(new Date(System.currentTimeMillis() + delay));
            localMessageMapper.updateById(msg);
        }
    }
}
```
