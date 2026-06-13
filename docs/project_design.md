# Project Design

## 定位

FinRisk Research Agent 是面向券商资管投后风控人员的研究型 Agent。首版聚焦三类任务：

- 风险异动查询
- 产品风险对比
- 主体信用风险归因

## 架构

```text
User Query
  -> Planner: 路由、实体识别、问题池打分、工具计划
  -> Retriever: mock 数据库、知识图谱、本地文档、外部检索占位
  -> Critic: 问题树、证据充分性、缺失问题
  -> Research Package: Reporter Agent 可消费的结构化证据包
```

## 当前边界

不接真实投资数据，不输出投资建议，不做生产级权限控制。外部检索目前是 stub，后续替换为搜索 API 或公告源即可。

