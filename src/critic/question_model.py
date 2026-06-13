from __future__ import annotations

from src.schemas.critic_schema import MissingQuestion


QUESTION_BY_EVIDENCE = {
    "holding_exposure": "目标产品对该主体相关资产的持仓权重和估值影响是多少？",
    "product_metric": "目标产品近期风险评分、回撤和集中度是否上升？",
    "issuer_profile": "主体评级、展望和基本信息近期是否发生变化？",
    "bond_market_indicator": "相关债券近30日收益率和信用利差是否明显上行？",
    "financing_pressure": "主体近期是否存在债务到期、展期或融资受阻信息？",
    "sales_pressure": "所属行业销售和融资环境是否持续承压？",
    "research_note": "是否存在可支撑风险传导路径的权威研究资料？",
    "kg_path": "知识图谱中是否能连接主体、行业、事件和产品暴露？",
    "external_fact_stub": "外部新闻、公告或舆情是否出现负面信号？",
}


def propose_missing_questions(dimension: str, missing_evidence_types: list[str]) -> list[MissingQuestion]:
    questions = []
    for evidence_type in missing_evidence_types:
        questions.append(
            MissingQuestion(
                question=QUESTION_BY_EVIDENCE.get(evidence_type, f"是否能补充{evidence_type}证据？"),
                risk_dimension=dimension,
                missing_evidence_type=evidence_type,
            )
        )
    return questions

