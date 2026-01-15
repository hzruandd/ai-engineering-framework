# 案例5：分布式锁防止并发问题

**场景**：优惠券领取，防止超发

## 完整代码

```java
package cn.city.parking.coupon.service.impl;

import cn.city.parking.common.core.exception.BusinessException;
import cn.city.parking.common.redis.service.Locker;
import cn.city.parking.coupon.api.entity.UserCoupon;
import cn.city.parking.coupon.service.IUserCouponService;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Slf4j
@Service
public class UserCouponServiceImpl implements IUserCouponService {

    @Autowired
    private Locker locker;

    /**
     * 领取优惠券
     *
     * @param userId 用户ID
     * @param couponId 优惠券ID
     * @return 是否成功
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public boolean receiveCoupon(String userId, String couponId) {
        // ✅ 使用分布式锁防止并发
        String lockKey = "coupon:receive:" + couponId + ":" + userId;

        try {
            // 尝试获取锁，等待3秒，锁定10秒
            boolean locked = locker.tryLock(lockKey, 3000, 10000);

            if (!locked) {
                throw new BusinessException("系统繁忙，请稍后重试");
            }

            try {
                // 检查优惠券库存
                Integer stock = baseMapper.selectCouponStock(couponId);
                if (stock <= 0) {
                    throw new BusinessException("优惠券已抢完");
                }

                // 检查用户是否已领取
                Long count = baseMapper.selectCount(
                    new LambdaQueryWrapper<UserCoupon>()
                        .eq(UserCoupon::getUserId, userId)
                        .eq(UserCoupon::getCouponId, couponId)
                );

                if (count > 0) {
                    throw new BusinessException("您已领取过该优惠券");
                }

                // 扣减库存
                int rows = baseMapper.decreaseStock(couponId);
                if (rows == 0) {
                    throw new BusinessException("优惠券已抢完");
                }

                // 发放优惠券
                UserCoupon userCoupon = new UserCoupon();
                userCoupon.setUserId(userId);
                userCoupon.setCouponId(couponId);
                baseMapper.insert(userCoupon);

                log.info("用户领取优惠券成功，userId：{}，couponId：{}", userId, couponId);
                return true;

            } finally {
                // ✅ 释放锁（在finally中确保一定释放）
                locker.unlock(lockKey);
            }

        } catch (Exception e) {
            log.error("领取优惠券失败", e);
            throw new BusinessException("领取优惠券失败：" + e.getMessage());
        }
    }
}
```

## 关键点说明

**分布式锁要点**：
- ✅ 使用 `Locker` 进行分布式锁控制
- ✅ 在 `finally` 中释放锁，确保不会死锁
- ✅ 设置合理的等待时间和锁定时间
- ✅ 锁的粒度要合理（不要锁太大范围）
- ❌ 不要忘记释放锁
- ❌ 锁的时间不要太长（影响性能）

**使用场景**：
- ✅ 防止并发修改同一资源（订单、库存）
- ✅ 定时任务防止重复执行
- ✅ 防止缓存击穿
- ❌ 不要用于长时间操作（>30秒）
