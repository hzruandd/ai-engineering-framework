# 自然语言触发示例

## 示例 1：当前分支评审

```text
帮我评审当前分支代码，tapd=TAPD-123456
```

## 示例 2：生成正式报告

```text
生成停智慧代码评审报告，tapd=TAPD-123456 baseline=release/2026.05
```

## 示例 3：数据库专项

```text
检查这次 SQL 和数据库字段变更风险，tapd=TAPD-123456
```

## 示例 4：多服务联合评审

```text
帮我做一次上线前评审，涉及 order-service 和 billing-service，tapd=TAPD-123456,TAPD-123457
```

## 示例 5：更像命令的参数化自然语言

```text
帮我评审当前分支代码，tapd=TAPD-123456 baseline=master
```

```text
检查这次 SQL 风险，tapd=TAPD-123456 scope=sql
```

## 示例 6：缺少 TAPD 时的正确交互

用户：

```text
帮我评审当前分支代码
```

正确响应：

```text
开始评审前需要 TAPD 编号。请提供一个或多个 TAPD 编号，并分别说明每个 TAPD 对应的本次变更目标。
```
