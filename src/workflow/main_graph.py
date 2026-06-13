from __future__ import annotations

import json
import sys
from pathlib import Path

from src.critic.sufficiency_checker import critique
from src.planner.router import plan_query
from src.retriever.tool_registry import execute_tool_plan
from src.schemas.research_package_schema import ResearchPackage
from src.workflow.seed_data import DB_PATH, seed


def run_research(query: str) -> ResearchPackage:
    if not DB_PATH.exists():
        seed()
    planner_result = plan_query(query)
    evidence_cards = execute_tool_plan(planner_result.tool_plan)
    critic_result = critique(planner_result, evidence_cards)
    package = ResearchPackage(
        query_id=planner_result.query_id,
        main_task=planner_result.main_task,
        route=planner_result.route,
        planner_result=planner_result,
        final_sub_questions=[item.question for item in planner_result.selected_sub_questions],
        evidence_cards=evidence_cards,
        critic_result=critic_result,
        risk_chain=build_risk_chain(evidence_cards),
        reporter_ready=critic_result.critic_pass,
    )
    return package


def build_risk_chain(evidence_cards) -> list[str]:
    tags = {tag for card in evidence_cards for tag in card.risk_tags}
    chain = []
    if "industry_risk" in tags:
        chain.append("行业销售或融资环境承压")
    if "liquidity_risk" in tags or "credit_risk" in tags:
        chain.append("主体融资压力和信用风险信号上升")
    if "market_risk" in tags:
        chain.append("债券收益率或信用利差变化反映市场定价压力")
    if "portfolio_exposure" in tags or "product_risk" in tags:
        chain.append("产品持仓暴露可能传导为估值、回撤和风险评分变化")
    return chain


def main() -> None:
    query = " ".join(sys.argv[1:]) or "帮我分析一下产品A持仓中的万科债券最近是否存在信用风险上升。"
    package = run_research(query)
    output_dir = Path(__file__).resolve().parents[2] / "outputs"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"{package.query_id}.json"
    output_path.write_text(package.model_dump_json(indent=2), encoding="utf-8")
    print(json.dumps(package.model_dump(), ensure_ascii=False, indent=2))
    print(f"\nSaved: {output_path}")


if __name__ == "__main__":
    main()

