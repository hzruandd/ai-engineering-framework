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
/tzh-review tapd=TAPD-123456,TAPD-123457 projects=order-service,billing-service baseline=release/2026.05
```

含义：
- 进入多项目模式
- 由 Skill 继续识别每个项目的实际 diff 与风险边界

## 完整报告并显式允许覆盖

```text
/tzh-review tapd=TAPD-123456 output=full-report overwrite=true
```

含义：
- 生成完整正式评审报告
- 如果同名文件已存在，允许由 Skill 按覆盖策略处理

## 安全专项

```text
/tzh-review tapd=TAPD-123456 mode=security-only
```

含义：
- 只聚焦脱敏、加密、密钥、权限、防重放、审计与租户隔离
