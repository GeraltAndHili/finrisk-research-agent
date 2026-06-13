# Evaluation

建议评估四类指标：

- 有效证据召回率：命中的 gold evidence type 数量 / gold evidence type 总数
- 证据支持率：被 Critic 判断能支撑关键子问题的证据数 / 总证据数
- 风险链路完整度：外部事件、主体变化、市场定价、产品影响四段是否闭合
- 平均检索轮次：Open Research Query 完成前的 Retriever 调用轮数

首版可构造 20-30 条 mock Query，分为数据查询、风险归因、外部事件影响三类。

