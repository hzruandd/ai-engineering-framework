# Phase 2 Migration Guide

Updated: 2026-07-10

## For Existing Users

- Continue using `/tzh-review` for formal review.
- `/formal-review` is now only a summary/formatting helper and must not change `tzh-review` decisions.
- Use `/deliver-requirement` for the end-to-end workflow.
- Use `prd-authoring` before design when no PRD exists.
- Use `pre-coding-check` before large/core coding changes.

## Java Mapper Migration

Replace active templates that say:

```java
extends BaseMapper<User>
```

with:

```java
extends CommonMapper<User>
```

using:

```java
import cn.city.parking.common.server.injector.CommonMapper;
```

## Quality Thresholds

Use `config/quality-thresholds.yaml` as the single source for default thresholds. Older documents mentioning 60/70/80 percent are historical unless updated to reference this file.
