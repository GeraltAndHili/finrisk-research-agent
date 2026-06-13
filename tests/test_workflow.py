from src.workflow.main_graph import run_research


def test_workflow_outputs_research_package():
    package = run_research("帮我分析一下产品A持仓中的万科债券最近是否存在信用风险上升。")
    assert package.query_id
    assert package.evidence_cards
    assert package.critic_result.fact_sufficiency >= 0
    assert package.final_sub_questions

