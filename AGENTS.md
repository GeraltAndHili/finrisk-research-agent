# AGENTS.md

本文件是 FinRisk Research Agent 项目的运行首要约束。后续所有开发、调试、测试和演示都优先遵守这里的约定。

## 运行环境

- 本项目统一使用 conda 环境：`financial`
- 环境路径：`D:\Anacondaenv\financial`
- 不再默认使用 base、系统 Python 或其他 conda 环境
- 进入项目后优先执行：

```powershell
conda activate financial
cd "F:\Financial risk\finrisk-research-agent"
```

如在非交互命令中运行，优先使用 `financial` 环境内的 Python 绝对路径，避免 Windows 控制台在 `conda run` 打印中文 JSON 时触发 GBK 编码错误：

```powershell
D:\Anacondaenv\financial\python.exe -m pytest -q
D:\Anacondaenv\financial\python.exe -m src.workflow.seed_data
D:\Anacondaenv\financial\python.exe -m src.workflow.main_graph "帮我分析一下产品A持仓中的万科债券最近是否存在信用风险上升。"
D:\Anacondaenv\financial\python.exe -m streamlit run app/streamlit_app.py
```

## 项目目标

本项目是面向券商资管投后风控场景的 Deep Research Agent 原型，主线为：

```text
User Query -> Planner -> Retriever -> Critic -> Research Package
```

首版重点是研究闭环、结构化证据和可演示能力，不追求生产级权限系统或真实投资建议。

## 开发约束

- 优先保持离线可运行；真实 LLM、真实搜索 API、真实券商数据都作为可插拔增强
- 输出结构以 `Research Package`、`Evidence Card`、`QuestionNode` 等 schema 为准
- 新增工具必须接入 `src/retriever/tool_registry.py`
- Planner 负责路由和工具计划，Retriever 负责结构化证据，Critic 负责证据充分性和缺失问题
- 不在代码中硬编码 API Key、账号、真实客户敏感信息
- mock 数据只用于演示逻辑，不代表真实投资结论

## 记录规范

- 设计想法、架构推演、方案取舍放入 `design_thoughts/`
- 开发问题、报错、调试过程、待修复事项放入 `dev_issues/`
- README 面向展示和使用说明，AGENTS.md 面向后续 agent/开发者执行约束
