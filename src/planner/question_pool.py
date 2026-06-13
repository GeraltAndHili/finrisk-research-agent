from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class QuestionTemplate:
    dimension: str
    template: str
    evidence_types: tuple[str, ...]
    keywords: tuple[str, ...]


QUESTION_POOL: list[QuestionTemplate] = [
    QuestionTemplate(
        "portfolio_exposure",
        "{product}是否持有{issuer}相关资产，持仓权重和估值影响是否显著？",
        ("holding_data", "valuation_data"),
        ("产品", "持仓", "暴露", "权重", "估值"),
    ),
    QuestionTemplate(
        "credit_risk",
        "{issuer}近期是否出现评级、展望或信用利差变化？",
        ("rating_change", "market_indicator", "announcement"),
        ("信用", "评级", "展望", "利差", "债券"),
    ),
    QuestionTemplate(
        "liquidity_risk",
        "{issuer}近期是否存在债务到期、展期、现金流或融资压力？",
        ("debt_maturity", "cash_flow", "financing_news"),
        ("债务", "到期", "融资", "现金流", "流动性"),
    ),
    QuestionTemplate(
        "industry_risk",
        "{industry}近期政策、销售和融资环境是否对{issuer}形成负面影响？",
        ("industry_news", "policy_event", "sales_data"),
        ("行业", "政策", "销售", "融资环境", "地产"),
    ),
    QuestionTemplate(
        "market_risk",
        "{issuer}相关债券价格、收益率和信用利差是否出现异常波动？",
        ("bond_price", "yield", "credit_spread"),
        ("价格", "收益率", "利差", "波动", "市场"),
    ),
    QuestionTemplate(
        "public_opinion_risk",
        "{issuer}近期是否出现负面新闻、诉讼、处罚或违约传闻？",
        ("news", "litigation", "penalty"),
        ("舆情", "新闻", "诉讼", "处罚", "违约"),
    ),
    QuestionTemplate(
        "related_party_risk",
        "{issuer}的母公司、子公司或担保方是否出现风险事件？",
        ("related_party_event", "guarantee_info"),
        ("关联", "母公司", "子公司", "担保"),
    ),
    QuestionTemplate(
        "product_risk",
        "{product}近期风险评分、回撤、波动率和集中度是否上升？",
        ("product_metric", "drawdown", "concentration"),
        ("产品", "风险评分", "回撤", "波动率", "集中度"),
    ),
]


def render_question(template: QuestionTemplate, entities: dict[str, list[str]]) -> str:
    product = first(entities, "product", "目标产品")
    issuer = first(entities, "issuer", "目标主体")
    industry = first(entities, "industry", "所属行业")
    return template.template.format(product=product, issuer=issuer, industry=industry)


def first(entities: dict[str, list[str]], key: str, default: str) -> str:
    values = entities.get(key) or []
    return values[0] if values else default

