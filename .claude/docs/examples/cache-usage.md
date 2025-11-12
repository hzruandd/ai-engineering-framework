# 案例2：带缓存的热点查询

**场景**：系统配置信息，查询频繁，变化少，适合缓存

## 完整代码

```java
package cn.city.parking.config.dubbo;

import cn.city.parking.common.auth.base.BaseDubboApiImpl;
import cn.city.parking.common.core.web.domain.ResponseResult;
import cn.city.parking.common.redis.RedisUtils;
import cn.city.parking.config.api.ConfigDubboApi;
import cn.city.parking.config.api.entity.SystemConfig;
import cn.city.parking.config.service.ISystemConfigService;
import com.google.common.base.Preconditions;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.apache.dubbo.config.annotation.DubboService;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.concurrent.TimeUnit;

@Slf4j
@DubboService
public class ConfigDubboApiImpl extends BaseDubboApiImpl implements ConfigDubboApi {

    @Autowired
    private ISystemConfigService systemConfigService;

    private static final String CACHE_CONFIG_KEY = "config:key:";

    @Override
    public ResponseResult<SystemConfig> getByKey(String configKey) {
        Preconditions.checkArgument(StringUtils.isNotBlank(configKey), "配置键不能为空");

        // ✅ 热点数据，适合缓存
        String cacheKey = CACHE_CONFIG_KEY + configKey;

        // 先查缓存（需要类型转换）
        SystemConfig config = RedisUtils.getCacheObject(cacheKey, SystemConfig.class);
        if (config != null) {
            log.debug("配置命中缓存，key：{}", configKey);
            return ResponseResult.success(config);
        }

        // 缓存未命中，查询数据库
        config = systemConfigService.selectConfigByKey(configKey);

        // 存入缓存（1小时过期）
        if (config != null) {
            RedisUtils.setCacheObject(cacheKey, config, 1L, TimeUnit.HOURS);
            log.debug("配置存入缓存，key：{}", configKey);
        }

        return ResponseResult.success(config);
    }

    @Override
    public ResponseResult<Integer> updateConfig(SystemConfig config) {
        Preconditions.checkNotNull(config, "配置信息不能为空");
        Preconditions.checkArgument(StringUtils.isNotBlank(config.getConfigKey()), "配置键不能为空");

        log.info("更新系统配置，key：{}", config.getConfigKey());
        int rows = systemConfigService.updateConfig(config);

        // ✅ 更新后清理缓存
        String cacheKey = CACHE_CONFIG_KEY + config.getConfigKey();
        RedisUtils.deleteObject(cacheKey);
        log.info("配置更新成功，已清理缓存");

        return ResponseResult.success(rows);
    }
}
```

## 适合缓存的场景

- ✅ 系统配置（查询频繁，几乎不变）
- ✅ 字典数据（读多写少）
- ✅ 权限数据（短时间内不变）
- ❌ 订单数据（实时性要求高）
- ❌ 库存数据（频繁变化）

## 关键点说明

- ✅ 缓存前先检查是否命中
- ✅ 使用 RedisUtils.getCacheObject(key, Class) 指定类型
- ✅ 设置合理的过期时间（1小时）
- ✅ 更新数据后清理缓存
- ✅ 添加日志记录缓存命中情况
