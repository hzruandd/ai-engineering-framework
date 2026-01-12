---
name: parking-in-out
description: 处理停车场车辆入场、出场、计费业务逻辑。适用于修改 carInto、appearanceProcessing、parkingCalculationFee 方法，处理多位多车、场中场、月租车、储值车、VIP会员等车辆类型，以及计费规则、优惠减免等相关需求。
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# 停车场出入车业务专家

## 业务文档优先原则

在开始任何工作前，**务必先阅读对应的业务文档**：

- **[devicePushInfo方法详解](reference/devicePushInfo方法详解.md)** - 设备推送处理总入口，判断入场/出场
- **[carInto方法详解](reference/carInto方法详解.md)** - 车辆入场完整流程，包含重复入场、多位多车、场中场
- **[appearanceProcessing方法详解](reference/appearanceProcessing方法详解.md)** - 车辆出场完整流程，包含计费、储值车扣费
- **[parkingCalculationFee方法详解](reference/parkingCalculationFee方法详解.md)** - 停车费用计算，5种计费类型详解
- **[代码修改最佳实践](reference/代码修改最佳实践.md)** - 修改指南、代码模板、调试技巧、测试用例

**提示**: 以上文档包含完整的流程图、代码位置索引、配置项说明和常见场景示例。

---

## 核心业务流程

```
设备识别车牌
    ↓
devicePushInfo (设备推送统一入口)
    ├→ 判断入场/出场 (通过车道类型)
    ├→ 查询在场记录 (ParkingList)
    ├→ 无在场记录 → carInto (入场处理)
    └→ 有在场记录 → appearanceProcessing (出场处理)
        ↓
    parkingCalculationFee (费用计算)
        ↓
    优惠减免计算 (DiscountCalculator)
        ↓
    屏显展示 + 开闸放行
        ↓
    推送记录 + 回调通知
```

---

## 场景识别指南

### 场景A: 车辆入场 (carInto)

**触发条件**: 设备识别到车牌 + 车道类型为入口 + 无在场记录

**核心检查项**:
1. **反向车道锁** - 单通道双向冲突检测 (`REVERSE_LANE_ID{laneId}`)
2. **重复入场** - 检查 `isNotPlateRepeat` 配置，调用 `reEntry()` 处理
3. **身份验证** - 军警车/车道权限/通行时段
4. **多位多车** (类型10) - 判断已占位数是否超过车位数，决定是否临停计费
5. **场中场** - 外场创建记录+轨迹，内场仅更新轨迹 (`isSave=false`)

**关键方法**: `ParkingDeviceServiceImpl.java:1678-1917`

**必做操作**:
- 车位数-1: `spaceNumberUpdateService.update(..., (byte) 0, ...)`
- 多位多车占位状态同步: `sendRentalPlateInSpaceStatusUpdate(..., 1)`

---

### 场景B: 车辆出场 (appearanceProcessing)

**触发条件**: 设备识别到车牌 + 车道类型为出口 + 有在场记录

**核心流程**:
1. **身份验证** - 同入场
2. **手动输入处理** - `triggerType=2` 时修改车牌/类型/时间
3. **计费分支**:
   - **非场中场**: 调用 `parkingCalculationFee()` → 扣除已支付 → 追缴处理
   - **场中场**: 结算当前轨迹 → 外场出口调用 `jsa()` 汇总全部区域
4. **储值车扣费** (类型7) - `rechargeTypeInfo()` 检查余额并扣费
5. **优惠计算** - `outCarBeforeNotify()` 第三方优惠接口
6. **待出场处理** - 设置反向车道锁 + 屏显 + 推送监控

**关键方法**: `ParkingDeviceServiceImpl.java:853-1127`

**必做操作**:
- 车位数+1: `spaceNumberUpdateService.update(..., (byte) 1, ...)`
- 场中场外场出口: 必须调用 `jsa()` 汇总所有区域费用

---

### 场景C: 费用计算 (parkingCalculationFee)

**触发条件**: 出场时未支付 或 已支付超过免费时长

**计费类型**:
- 0: 自然天计费 | 1: 日夜分段 | 2: 24小时分段 | 3: 时间段 | 4: 通用时长

**核心逻辑**:
1. **军警车免费** - 车牌/类型/颜色判断
2. **计费规则优先级** - 新能源车 > 储值车 > 多位多车 > 过期月卡 > 临时牌 > 访客 > VIP > 默认
3. **免费时长** - 按次(`freeTimeRule=0`) 或 按时长累计(`=1`)
4. **单次收费** - 查询上次订单，判断是否在有效期内
5. **月租到期分段** - 拆分时段分别算费 (月租/临停/VIP)
6. **无入场记录** - 追缴 或 固定费用
7. **优惠减免** - `DiscountCalculator.calculateFinalAmount()`

**关键方法**: `ParkingFee.java:74-145`

**关键注意**:
- 月租到期边界精确到秒 (14:00到期，14:00:01属于临停)
- 免费时长按时长累计需查询历史避免重复享受
- 自然天从0点开始，不是从支付时间开始

---

### 场景D: 场中场业务

**核心概念**: 停车场分多区域 (外场AREA_A + 内场)，车辆移动产生轨迹 (`ParkingDetail`)

**入场**: 外场创建 ParkingList+轨迹 | 内场仅更新轨迹
**出场**: 内场结算当前轨迹+创建新轨迹 | 外场调用 `jsa()` 汇总全部费用

**关键方法**:
- `nestedEntry()` - 创建轨迹
- `completeRegionDetails()` - 完善轨迹信息
- `billingDetails()` - 结算单个轨迹
- `jsa()` - 汇总所有区域费用 (join settlement amount)

**关键注意**: 外场出口必须调用 `jsa()`，不能只结算最后一个区域

---

## 快速参考

### 车辆类型 (carActType)
- 0: 临停车 | 1: 月卡车 | 2: VIP会员 | 5: 过期月卡 | 7: 储值车 | 10: 多位多车 | 11: 访客车

### 订单状态 (orderStatus)
- 0: 未支付 | 1: 已支付 | 9: 异常

### 异常类型 (exceptionType)
- 0: 正常 | 1: 重复入场 | 2: 无入场记录

### Redis Key速查
```
REVERSE_LANE_ID{laneId}                    # 反向车道锁 (TTL 3分钟)
DEVICE_UNIQUE_ID:{listId}                  # 设备唯一ID (TTL 180分钟)
NO_ENTRY_RECORD{carNumber}{listId}         # 无入场记录标记 (TTL 1200秒)
PRESS_PAYMENT{carNumber}{parkingId}        # 追缴订单关联
READY_PAY_LIST_INFO{listId}                # 预缴费标记
NOT_AREA_FREE_MONTHLY_CARD_TYPE{...}       # 跨区域月租标记
```

### 关键配置 (ParkingInfo)
- `isInterior`: 是否场中场 (0-否, 1-是)
- `isNotPlateRepeat`: 禁止重复入场 (0-允许, 1-禁止)
- `payFreeTime`: 支付后免费时长(分钟)
- `pressPaymentStatus`: 追缴开关 (0-关, 1-开)
- `isNoRecordFixedCost`: 无入场记录处理 (1-固定费用, 2-人工)
- `isPoliceCar`: 军警车免费 (0-否, 1-是)
- `cardPriorityType`: 月租优先 (0-按时段, 1-整单免费)

---

## 常见陷阱 (Top 10)

### 1. 多位多车占位状态不同步
**问题**: 新判断方式依赖 `inParkingSpace` 状态，未及时同步导致错误判断
**方案**: 入场调用 `sendRentalPlateInSpaceStatusUpdate(..., 1)`，出场更新为0

### 2. 车位数更新遗漏
**问题**: 车位数统计不准确
**方案**: 入场-1，出场+1，重复入场先+1旧记录再-1新记录

### 3. 场中场内场移动不保存新记录
**说明**: 这是正常的！`isSave=false` 时仅通过 ParkingDetail 记录轨迹

### 4. 场中场外场出口结算遗漏
**问题**: 只结算最后区域，其他区域费用未计算
**方案**: 外场出口必须调用 `jsa()` 汇总所有区域

### 5. 免费时长重复享受
**问题**: 同一车辆多次进出重复享受免费时长
**方案**: `freeTimeRule=0` 且 `freeType!=1` 时调用 `getOldFree()` 查询已享受记录

### 6. 月租到期边界问题
**问题**: 14:00到期，14:00:01出场费用计算错误
**方案**: 时间段拆分精确到秒

### 7. 单次收费有效期计算错误
**问题**: 支付时间为空导致异常
**方案**: 降级使用入场时间，自然天从0点开始

### 8. 反向车道锁未释放
**问题**: 单通道出口缴费后入口仍无法进入
**方案**: 检查TTL设置，确保异常时也能释放

### 9. 重复入场并发问题
**问题**: 快速连续入场导致两条记录都保存
**方案**: 在 carInto 入口处加分布式锁

### 10. 业务安全风险
**问题**: 已付款车辆便捷放行可能被滥用
**方案**: 修改支付/开闸逻辑时评估安全影响

---

## 工作流程

当收到出入车业务需求时:

1. **识别场景** - 判断属于 A/B/C/D 哪个场景
2. **阅读文档** - 打开 reference 目录下对应的详细文档
3. **定位代码** - 根据文档中的代码位置索引找到相关方法
4. **分析影响** - 评估修改影响的模块和流程
5. **提供方案** - 给出修改方案，包括位置、内容、注意事项
6. **说明风险** - 指出可能的陷阱和风险点
7. **测试建议** - 提供完整的测试建议

## 成功标准

- ✅ 业务逻辑正确无误
- ✅ 数据一致性得到保证
- ✅ 缓存同步及时
- ✅ 日志记录完整
- ✅ 无已知安全风险
- ✅ 性能符合预期

---

**相关资源**:
- 详细流程图: reference 文档中的 Mermaid 流程图
- 代码位置: 每个 reference 文档末尾的"相关方法索引"
- 业务场景: 每个 reference 文档的"常见业务场景"章节
- 修改模板: [代码修改最佳实践](reference/代码修改最佳实践.md)