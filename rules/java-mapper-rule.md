# Java Mapper Rule

Version: 1.0.0
Updated: 2026-07-10
Canonical source: this file and `global-settings/.claude/CLAUDE.md`

## Rule

停智慧 Java Mapper 默认继承:

```java
import cn.city.parking.common.server.injector.CommonMapper;

public interface UserMapper extends CommonMapper<User> {
}
```

`CommonMapper<T>` 是公司框架在 MyBatis Plus `BaseMapper<T>` 之上的扩展入口，用于保持批量能力和框架注入方式一致。

## Do Not

```java
import com.baomidou.mybatisplus.core.mapper.BaseMapper;

public interface UserMapper extends BaseMapper<User> {
}
```

## Validation

Use `scripts/validate-assets.ps1` to detect active templates or commands that still recommend `extends BaseMapper`.
