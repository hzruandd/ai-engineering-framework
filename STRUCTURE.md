# 目录结构说明

> 反映仓库实际磁盘结构（2026-04-08 更新）

```
city-parking-claude-doc/
│
├── README.md                          # 仓库总入口
├── QUICKSTART.md                      # 快速开始（5 分钟上手）
├── CONTRIBUTING.md                    # 贡献指南
├── UPDATE.md                          # 更新指南
├── CHANGELOG.md                       # 变更记录
├── STRUCTURE.md                       # 本文件
├── MIGRATION_REPORT.md                # 本次改造报告
│
├── global-settings/                   # 全局配置（成熟资产）
│   ├── README.md                      # 全局配置说明
│   └── .claude/
│       ├── CLAUDE.md                  # 核心规范（52KB，13 模块）
│       ├── settings.local.json        # 本地设置
│       ├── ignore                     # 忽略规则
│       ├── analyze_slow_queries.py    # Doris 慢查询分析脚本
│       ├── commands/                  # 10 个快捷命令
│       │   ├── add-field.md
│       │   ├── analyze-slow-query.md
│       │   ├── design-doc.md
│       │   ├── diff-report.md
│       │   ├── fix-cache.md
│       │   ├── formal-review.md
│       │   ├── generate-tests.md
│       │   ├── new-api.md
│       │   ├── new-crud.md
│       │   └── review-code.md
│       └── docs/                      # 参考文档
│           ├── architecture/          # 架构设计（6 篇）
│           ├── design/                # 设计规范（1 篇）
│           ├── examples/              # 实战案例（5 篇）
│           └── guides/                # 开发指南（5 篇）
│
├── project-templates/                 # 项目配置模板
│   ├── README.md                      # 模板使用说明
│   ├── CATALOG.md                     # 模板清单
│   └── tzh-parkinglot/               # 停车场管理系统模板
│       ├── CLAUDE.md                  # 项目级配置
│       └── .claude/
│           ├── settings.local.json
│           └── skills/
│               └── parking-in-out/    # 出入车业务 Skill
│
├── open-claw/                         # OpenClaw 平台配置
│   └── README.md                      # OpenClaw 说明（自托管 AI 助手网关）
│
├── mcp/                               # 精选 MCP Server 推荐
│   ├── README.md                      # MCP 总入口与安装说明
│   ├── playwright.md                  # Playwright — 浏览器自动化
│   ├── fetch.md                       # Fetch — 网页内容抓取
│   ├── mysql.md                       # MySQL — 数据库查询
│   └── sequential-thinking.md         # Sequential Thinking — 结构化思考
│
└── skills/                            # 22 个技能包 + OpenClaw 参考资料
    ├── README.md                      # 技能包总入口
    ├── CATALOG.md                     # 技能包分类索引
    ├── add-field/                     # 添加字段
    ├── algorithmic-art/               # 算法艺术
    ├── canvas-design/                 # 视觉设计
    ├── diff-report/                   # 修改报告
    ├── doc-coauthoring/               # 文档协作
    ├── docx/                          # Word 操作
    ├── fix-cache/                     # 缓存修复
    ├── frontend-design/               # 前端设计
    ├── generate-tests/                # 测试生成
    ├── java-guide/                    # Java 开发规范
    ├── mcp-builder/                   # MCP 构建
    ├── new-api/                       # 添加接口
    ├── new-crud/                      # CRUD 生成
    ├── openclaw/                      # OpenClaw Agent 开发参考资料（非 Skill）
    ├── pdf/                           # PDF 操作
    ├── pptx/                          # PPT 操作
    ├── review-code/                   # 代码审查
    ├── self-test/                     # 自动化自测
    ├── skill-creator/                 # Skill 创建工具
    ├── theme-factory/                 # 主题工厂
    ├── thinking-guide/                # 思维引导
    ├── webapp-testing/                # Web 测试
    └── xlsx/                          # Excel 操作
```

## 目录职责

| 目录 | 职责 | 安装位置 |
|------|------|----------|
| global-settings/ | 全公司通用规范、命令、参考文档 | ~/.claude/ |
| project-templates/ | 项目级 Claude 配置模板 | 项目根目录/ |
| open-claw/ | OpenClaw 平台配置（自托管 AI 助手网关） | 按需 |
| mcp/ | 精选 MCP Server 推荐与安装指南 | 参考文档（按需配置到 settings.json） |
| skills/ | 可复用技能包 | ~/.claude/skills/ 或 项目/.claude/skills/ |
