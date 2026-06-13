# FinRisk Research Agent

面向券商资管投后风控场景的 Deep Research Agent 原型系统。

系统采用 `Planner -> Retriever -> Critic -> Research Package` 的闭环架构，不只是做普通 RAG 问答，而是把开放式投后风控问题拆成关键研究子问题，再检索结构化证据，最后检查事实充分性、数据充分性和风险链路完整度。

## MVP 能力

- 识别三类 Query：`direct`、`react`、`open_research`
- Planner 生成实体、风险类型、候选问题池、最终 3-5 个子问题、工具调用计划
- Retriever 基于 mock SQLite、JSON 知识图谱和本地文档生成 Evidence Card
- Critic 构建问题树，判断证据充分性，并生成缺失问题
- 输出可交给 Reporter Agent 的 `Research Package`
- 提供 Streamlit 演示界面

## 快速开始

```powershell
cd "F:\Financial risk\finrisk-research-agent"
python -m src.workflow.seed_data
python -m src.workflow.main_graph "帮我分析一下产品A持仓中的万科债券最近是否存在信用风险上升。"
streamlit run app/streamlit_app.py
```

## 示例 Query

```text
看一下最近风险异动的固收产品有哪些？
比较一下产品A和产品B的风险。
帮我分析一下产品A持仓中的万科债券最近是否存在信用风险上升。
```

## 项目边界

首版不接真实券商内部数据，不生成投资建议，不实现完整 Reporter Agent，不接 Neo4j/MCP。当前重点是把 Planner-Retriever-Critic 的研究闭环和可追溯证据包跑通。

