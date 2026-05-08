# `/tzh-review` 命令触发示例

## 单 TAPD、默认 baseline

```text
/tzh-review tapd=TAPD-123456
```

含义：
- 使用 `master` 作为默认 baseline
- 对当前仓库或当前工作区执行评审

## 单 TAPD、显式 baseline

```text
/tzh-review tapd=TAPD-123456 baseline=release/2026.05
```

含义：
- 使用用户指定的 `release/2026.05` 作为 baseline

## 多 TAPD、联合评审

```text
/tzh-review tapd=TAPD-123456,TAPD-123457 baseline=master
```

含义：
- 同一次评审覆盖多个 TAPD
- 需要分别建立每个 TAPD 的变更映射

## 多项目、多 TAPD

```text
/tzh-review tapd=TAPD-123456,TAPD-123457 order-service:baseline=release/2026.05 billing-service:baseline=master
```

含义：
- 进入多项目模式
- 每个项目可以使用不同 baseline
