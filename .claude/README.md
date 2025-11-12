# Claude Code 配置说明

## 📁 文件结构

```
.claude/
├── claude.md              # 项目上下文（自动加载，包含架构说明）
├── instructions.md        # 编码规范（代码生成时参考）
├── ignore                 # 忽略文件模式
├── commands/              # 快捷命令
│   ├── review-code.md    # /review-code - 代码审查
│   ├── new-crud.md       # /new-crud - 生成CRUD（备用）
│   ├── add-field.md      # /add-field - 添加字段
│   ├── new-api.md        # /new-api - 添加接口
│   └── fix-cache.md      # /fix-cache - 缓存优化
└── README.md             # 本文件
```

## 🎯 核心文件说明

### claude.md
- **作用**：每次会话自动加载，提供项目背景
- **内容**：框架架构、技术栈、核心规范、常见问题
- **何时更新**：框架升级、架构调整时

### instructions.md
- **作用**：代码生成时的规范参考
- **内容**：详细的编码规范、代码模板、POM配置、YML配置
- **何时更新**：规范变更时

### ignore
- **作用**：指定Claude Code忽略的文件
- **内容**：node_modules、target、.idea等
- **何时更新**：添加新的忽略目录时

## 🚀 快捷命令使用

### /review-code
检查代码是否符合框架规范，包括15项检查：
```bash
# 在Claude Code中直接输入
/review-code
```

### /new-crud（备用）
快速生成完整的CRUD功能：
```bash
/new-crud
# 然后描述实体名称和字段
```

### /add-field
为已有实体添加新字段：
```bash
/add-field
# 然后说明实体名和新字段
```

### /new-api
在已有模块中添加新接口：
```bash
/new-api
# 然后描述新接口的功能
```

### /fix-cache
添加或优化缓存：
```bash
/fix-cache
# 然后说明需要缓存的功能
```

## ✅ 关键规范速查

### 核心类包路径
```java
// 实体基类和返回值（注意：web.domain，不是domain）
import cn.city.parking.common.core.web.domain.BusinessEntity;
import cn.city.parking.common.core.web.domain.ResponseResult;
import cn.city.parking.common.core.web.domain.BaseDubboApiImpl;

// 分页对象（pagehelper库）
import com.github.pagehelper.PageInfo;
```

### DubboApi实现三要点
```java
@DubboService
public class XxxDubboApiImpl extends BaseDubboApiImpl implements XxxDubboApi {

    @Override
    public ResponseResult<User> getInfo(String id) {
        // 1. ❌ 禁止try-catch
        // 2. ✅ 参数校验用Preconditions
        Preconditions.checkArgument(StringUtils.isNotBlank(id), "ID不能为空");

        // 3. ✅ 返回值必须带泛型
        return ResponseResult.success(user);
    }
}
```

### Mapper接口
```java
// ❌ 不需要@Mapper注解
public interface UserMapper extends BaseMapper<User> {
    User selectByUsername(@Param("username") String username);
}
```

### 启动类
```java
@Slf4j
@SpringBootApplication
public class CityParkingXxxApplication {
    // ❌ 不需要@EnableDubbo、@MapperScan等（common-server已配置）
}
```

### POM配置
```xml
<!-- parent统一使用 -->
<parent>
    <groupId>cn.city-parking</groupId>
    <artifactId>city-parking-parent</artifactId>
    <version>2.0.0-SNAPSHOT</version>
    <relativePath/>
</parent>
```

## 🔧 常见场景

### 场景1：开发新功能
```
我：帮我实现用户积分功能，包括积分增加、扣减、查询
Claude：按照框架规范实现完整功能
```

### 场景2：审查代码
```
我：/review-code
Claude：检查15项规范，列出问题清单
```

### 场景3：修复问题
```
我：这个DubboApi实现有try-catch，帮我改成符合规范的
Claude：移除try-catch，让异常自然抛出
```

### 场景4：添加缓存
```
我：/fix-cache
我：用户信息查询需要加缓存，过期时间30分钟
Claude：添加RedisUtils缓存逻辑
```

## ⚠️ 重要提醒

### ❌ 绝对不要做
1. DubboApi实现中使用try-catch
2. ResponseResult不带泛型
3. Mapper接口加@Mapper注解
4. 启动类加@EnableDubbo、@MapperScan
5. 创建common包、utils包

### ✅ 必须做
1. 实体类继承BusinessEntity
2. 返回值用ResponseResult<T>
3. 分页查询调用startDubboPage()
4. 参数校验用Preconditions
5. 使用推荐工具类（Guava、Hutool、Lang3）

## 📚 推荐工具类

| 用途 | 推荐类 |
|------|--------|
| 字符串 | `org.apache.commons.lang3.StringUtils` |
| 日期 | `cn.hutool.core.date.DateUtil` |
| 集合 | `com.google.common.collect.*` |
| 参数校验 | `com.google.common.base.Preconditions` |
| Redis | `cn.city.parking.common.redis.RedisUtils` |
| 分布式锁 | `cn.city.parking.common.redis.service.Locker` |
| 防重复提交 | `@NoRepeatSubmit` |

## 🔄 配置同步

### 复制到新项目
```bash
# 复制整个.claude目录到新项目根目录
cp -r .claude /path/to/new-project/

# 删除settings.local.json（会自动生成）
rm /path/to/new-project/.claude/settings.local.json
```

### 更新已有项目
```bash
# 只更新核心配置
cp .claude/claude.md /path/to/project/.claude/
cp .claude/instructions.md /path/to/project/.claude/
```

## 📞 问题反馈

配置问题或改进建议，请联系架构组。

---

**最后更新**: 2025-11-02
**框架版本**: City Parking 2.0.0-SNAPSHOT
