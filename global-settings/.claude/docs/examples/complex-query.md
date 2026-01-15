# 案例4：复杂查询与多表关联

**场景**：订单列表查询，关联用户信息和停车场信息

## 完整代码

### DTO（OrderDetailDTO.java）

```java
package cn.city.parking.order.api.dto;

import cn.city.parking.order.api.entity.ParkingOrder;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
@Schema(description = "订单详情DTO")
public class OrderDetailDTO extends ParkingOrder {

    @Schema(description = "用户名")
    private String username;

    @Schema(description = "用户手机号")
    private String userPhone;

    @Schema(description = "停车场名称")
    private String parkingLotName;

    @Schema(description = "停车场地址")
    private String parkingLotAddress;
}
```

### Mapper.xml（ParkingOrderMapper.xml）

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="cn.city.parking.order.mapper.ParkingOrderMapper">

    <resultMap id="OrderDetailResult" type="cn.city.parking.order.api.dto.OrderDetailDTO" autoMapping="true">
        <id property="id" column="id"/>
        <result property="orderNo" column="order_no"/>
        <result property="username" column="username"/>
        <result property="userPhone" column="user_phone"/>
        <result property="parkingLotName" column="parking_lot_name"/>
        <result property="parkingLotAddress" column="parking_lot_address"/>
    </resultMap>

    <select id="selectOrderDetailList" parameterType="cn.city.parking.order.api.entity.ParkingOrder"
            resultMap="OrderDetailResult">
        SELECT
            o.id,
            o.order_no,
            o.user_id,
            o.parking_lot_id,
            o.plate_number,
            o.start_time,
            o.end_time,
            o.amount,
            o.status,
            o.create_time,
            u.username,
            u.phone AS user_phone,
            p.name AS parking_lot_name,
            p.address AS parking_lot_address
        FROM parking_order o
        LEFT JOIN sys_user u ON o.user_id = u.id
        LEFT JOIN parking_lot p ON o.parking_lot_id = p.id
        WHERE 1=1
        <if test="orderNo != null and orderNo != ''">
            AND o.order_no = #{orderNo}
        </if>
        <if test="userId != null and userId != ''">
            AND o.user_id = #{userId}
        </if>
        <if test="status != null">
            AND o.status = #{status}
        </if>
        ORDER BY o.create_time DESC
    </select>

</mapper>
```

### Service实现

```java
@Override
public List<OrderDetailDTO> selectOrderDetailList(ParkingOrder order) {
    // ✅ 使用自定义SQL进行多表关联查询
    return baseMapper.selectOrderDetailList(order);
}
```

## 关键点说明

- ✅ 使用DTO继承实体类，扩展关联字段
- ✅ Mapper.xml 使用 resultMap 映射复杂结果
- ✅ LEFT JOIN 关联多表查询
- ✅ 使用动态SQL（`<if>`）构建查询条件
- ✅ 只查询需要的字段，避免 SELECT *
