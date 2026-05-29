# Skills 分类索引

> 22 个技能包，按用途分类。每个 Skill 目录下的 SKILL.md 包含详细说明和触发条件。

## 工程研发

| Skill | 说明 | 触发场景 |
|-------|------|----------|
| [java-guide](java-guide/) | Java 微服务开发规范 | 检测到 Java 项目（pom.xml、*.java） |
| [new-crud](new-crud/) | 创建完整 CRUD 功能 | 创建实体类和增删改查 |
| [add-field](add-field/) | 为实体类添加新字段 | 扩展已有实体 |
| [new-api](new-api/) | 在已有模块添加新接口 | 扩展 API 功能 |
| [fix-cache](fix-cache/) | 添加或修复缓存 | 缓存相关问题 |
| [mcp-builder](mcp-builder/) | MCP Server 构建指南 | 构建 MCP 集成 |
| [frontend-design](frontend-design/) | 前端界面设计 | 构建 Web 组件/页面 |

## 质量保障

| Skill | 说明 | 触发场景 |
|-------|------|----------|
| [review-code](review-code/) | 代码审查清单 | 代码审查 |
| [diff-report](diff-report/) | 代码修改报告 | 提交前自查 |
| [generate-tests](generate-tests/) | 生成单元测试 | 测试覆盖 |
| [self-test](self-test/) | 自动化自测 | 后端自测 |
| [webapp-testing](webapp-testing/) | Web 应用测试 | 前端功能验证 |

## 文档工具

| Skill | 说明 | 触发场景 |
|-------|------|----------|
| [pdf](pdf/) | PDF 读取/创建/编辑 | 涉及 PDF 文件 |
| [pptx](pptx/) | PPT 创建/编辑 | 涉及 .pptx 文件 |
| [docx](docx/) | Word 创建/编辑 | 涉及 .docx 文件 |
| [xlsx](xlsx/) | Excel 创建/编辑 | 涉及 .xlsx/.csv 文件 |
| [doc-coauthoring](doc-coauthoring/) | 文档协作编写 | 协作写文档/提案/技术规格 |

## 设计创意

| Skill | 说明 | 触发场景 |
|-------|------|----------|
| [canvas-design](canvas-design/) | 视觉设计（PNG/PDF） | 创建海报/设计稿 |
| [algorithmic-art](algorithmic-art/) | 算法艺术（p5.js） | 生成艺术/粒子系统 |
| [theme-factory](theme-factory/) | 主题样式工厂 | 为文档/页面应用主题 |

## 元技能

| Skill | 说明 | 触发场景 |
|-------|------|----------|
| [skill-creator](skill-creator/) | 创建新 Skill 的指南 | 创建或更新 Skill |
| [thinking-guide](thinking-guide/) | 结构化思考引导 | 复杂问题分析 |

---

## OpenClaw 参考资料

`openclaw/` 目录存放 OpenClaw Agent 开发的参考资料，不是 Claude Code Skill。

| 文档 | 说明 |
|------|------|
| [openclaw/SKILL.md](openclaw/SKILL.md) | Agent 开发工具包总览 |
| [openclaw/reference/agent-skeleton.md](openclaw/reference/agent-skeleton.md) | Agent 项目骨架模板 |
| [openclaw/reference/agent-prompt-template.md](openclaw/reference/agent-prompt-template.md) | Agent 提示词模板 |
| [openclaw/reference/safety-boundary.md](openclaw/reference/safety-boundary.md) | 安全边界定义（L1-L4） |
| [openclaw/reference/multi-agent-design.md](openclaw/reference/multi-agent-design.md) | 多 Agent 协作设计 |
| [openclaw/reference/workflow-orchestration.md](openclaw/reference/workflow-orchestration.md) | 工作流编排模式 |

详见 [open-claw/README.md](../open-claw/README.md) 了解 OpenClaw 平台。

## 项目专用 Skills

项目专用 Skills 不在本目录，而是在 `project-templates/` 对应模板中：

| 项目 | Skill | 位置 |
|------|-------|------|
| tzh-parkinglot | parking-in-out（出入车业务） | [project-templates/tzh-parkinglot/.claude/skills/](../project-templates/tzh-parkinglot/.claude/skills/) |
