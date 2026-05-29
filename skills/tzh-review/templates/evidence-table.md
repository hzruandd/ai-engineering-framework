# 证据表模板

| 证据编号 | 证据类型 | 判断类型 | 项目/服务 | 位置 | 摘要 | 关联风险/结论 |
|---|---|---|---|---|---|---|
| SRC-01 | SRC | Observed |  |  |  |  |
| SQL-01 | SQL | Observed |  |  |  |  |
| DDL-01 | DDL | Observed |  |  |  |  |
| IDX-01 | IDX | Observed |  |  |  |  |
| EXP-01 | EXP | Observed |  |  |  |  |
| CFG-01 | CFG | Observed |  |  |  |  |
| MQ-01 | MQ | Inferred |  |  |  |  |
| JOB-01 | JOB | Inferred |  |  |  |  |
| TEST-01 | TEST | Observed |  |  |  |  |
| SONAR-01 | SONAR | Unknown |  |  | 静态扫描结果（可选） |  |
| LOG-01 | LOG | Inferred |  |  |  |  |

## 使用规则

- `Observed`：当前仓库、测试、SQL、日志、配置能直接证明。
- `Inferred`：根据多处信息合理推断，但没有单点直接证据。
- `Unknown`：当前仓库或输入无法确认。
- 所有高风险结论必须至少绑定一个证据编号。
- 对核心域的 `Unknown` 不得忽略，必须进入人工确认项。
- 命中密码、token、密钥、证书、连接串、手机号、身份证号、车牌号、支付流水号等敏感值时，只允许写路径、行号、字段名和掩码值，不得完整原样输出。
