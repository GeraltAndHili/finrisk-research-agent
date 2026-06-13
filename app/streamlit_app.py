from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.workflow.main_graph import run_research


st.set_page_config(page_title="FinRisk Research Agent", layout="wide")

st.title("FinRisk Research Agent")

with st.sidebar:
    query = st.text_area(
        "Query",
        value="帮我分析一下产品A持仓中的万科债券最近是否存在信用风险上升。",
        height=140,
    )
    run = st.button("运行研究", type="primary", use_container_width=True)

if run or query:
    package = run_research(query)
    left, middle, right = st.columns([1, 1.15, 1])

    with left:
        st.subheader("Planner")
        st.metric("Route", package.route)
        st.write("实体")
        st.json(package.planner_result.entities)
        st.write("最终子问题")
        for item in package.planner_result.selected_sub_questions:
            st.markdown(f"- **{item.risk_dimension}** `{item.priority}`  {item.question}")
        st.write("Tool Plan")
        st.json([item.model_dump() for item in package.planner_result.tool_plan])

    with middle:
        st.subheader("Retriever Evidence")
        for card in package.evidence_cards:
            with st.expander(f"{card.evidence_id} · {card.source_name} · {card.event_type}", expanded=False):
                st.write(card.summary)
                st.json(card.model_dump())

    with right:
        st.subheader("Critic")
        result = package.critic_result
        st.metric("Reporter Ready", str(package.reporter_ready))
        st.progress(result.fact_sufficiency, text=f"事实充分性 {result.fact_sufficiency}")
        st.progress(result.data_sufficiency, text=f"数据充分性 {result.data_sufficiency}")
        st.progress(result.evidence_coverage, text=f"证据覆盖率 {result.evidence_coverage}")
        st.progress(result.risk_chain_completeness, text=f"风险链路完整度 {result.risk_chain_completeness}")
        st.write(result.reason)
        if result.missing_questions:
            st.write("缺失问题")
            for item in result.missing_questions:
                st.markdown(f"- **{item.risk_dimension}** {item.question}")
        st.write("Research Package")
        st.download_button(
            "下载 JSON",
            package.model_dump_json(indent=2),
            file_name=f"{package.query_id}.json",
            mime="application/json",
            use_container_width=True,
        )
        st.json(package.model_dump())

