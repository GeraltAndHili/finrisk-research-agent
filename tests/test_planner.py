from src.planner.router import plan_query


def test_open_research_route():
    result = plan_query("帮我分析一下产品A持仓中的万科债券最近是否存在信用风险上升。")
    assert result.route == "open_research"
    assert result.selected_sub_questions
    assert any(call.tool_name == "holding_query" for call in result.tool_plan)

