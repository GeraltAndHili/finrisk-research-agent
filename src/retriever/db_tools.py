from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from src.retriever.evidence_card import make_card
from src.schemas.evidence_schema import EvidenceCard


ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "data" / "mock_db" / "finrisk.db"


def rows(sql: str, params: tuple[Any, ...] = ()) -> list[sqlite3.Row]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        return list(conn.execute(sql, params).fetchall())
    finally:
        conn.close()


def product_risk_query(arguments: dict[str, Any]) -> list[EvidenceCard]:
    products = arguments.get("product") or []
    if products:
        placeholders = ",".join("?" for _ in products)
        result = rows(f"select * from product_risk_metrics where product_name in ({placeholders})", tuple(products))
    else:
        top_n = int(arguments.get("top_n", 5))
        result = rows("select * from product_risk_metrics order by risk_score desc limit ?", (top_n,))
    cards = []
    for row in result:
        cards.append(
            make_card(
                source_type="mock_db",
                source_name="product_risk_metrics",
                entity=row["product_name"],
                related_product=row["product_name"],
                risk_tags=["product_risk", "market_risk", "concentration_risk"],
                event_type="product_metric",
                publish_date=row["date"],
                credibility_score=0.9,
                freshness_score=0.86,
                summary=(
                    f"{row['product_name']}风险评分{row['risk_score']}，等级{row['risk_level']}，"
                    f"近30日回撤{row['nav_drawdown_30d']}%，信用暴露分{row['credit_exposure_score']}，"
                    f"流动性风险分{row['liquidity_risk_score']}，集中度分{row['concentration_score']}。"
                ),
                raw_content=str(dict(row)),
            )
        )
    return cards


def holding_query(arguments: dict[str, Any]) -> list[EvidenceCard]:
    product = arguments.get("product")
    issuer = arguments.get("issuer")
    sql = "select * from holdings where 1=1"
    params: list[Any] = []
    if product:
        sql += " and product_name = ?"
        params.append(product)
    if issuer:
        sql += " and issuer_name = ?"
        params.append(issuer)
    result = rows(sql, tuple(params))
    return [
        make_card(
            source_type="mock_db",
            source_name="holdings",
            entity=row["issuer_name"],
            related_product=row["product_name"],
            risk_tags=["portfolio_exposure", "credit_risk"],
            event_type="holding_exposure",
            credibility_score=0.92,
            freshness_score=0.82,
            summary=f"{row['product_name']}持有{row['asset_name']}，权重{row['holding_weight']}%，市值{row['market_value']}，评级{row['rating']}，行业{row['industry']}。",
            raw_content=str(dict(row)),
        )
        for row in result
    ]


def issuer_profile_query(arguments: dict[str, Any]) -> list[EvidenceCard]:
    issuer = arguments.get("issuer", "")
    result = rows("select * from issuer_profile where issuer_name = ?", (issuer,))
    return [
        make_card(
            source_type="mock_db",
            source_name="issuer_profile",
            entity=row["issuer_name"],
            risk_tags=["credit_risk", "industry_risk"],
            event_type="issuer_profile",
            publish_date=row["latest_update_date"],
            credibility_score=0.88,
            freshness_score=0.8,
            summary=f"{row['issuer_name']}所属{row['industry']}，区域{row['region']}，主体评级{row['rating']}，展望{row['rating_outlook']}，主营业务为{row['main_business']}。",
            raw_content=str(dict(row)),
        )
        for row in result
    ]


def risk_event_search(arguments: dict[str, Any]) -> list[EvidenceCard]:
    entity = arguments.get("entity", "")
    result = rows("select * from risk_events where entity_name = ? or affected_industry = ? order by event_date desc", (entity, entity))
    return [
        make_card(
            source_type=row["source_type"],
            source_name="risk_events",
            entity=row["entity_name"],
            risk_tags=[row["risk_type"]],
            event_type=row["event_type"],
            publish_date=row["event_date"],
            credibility_score=row["credibility_score"],
            freshness_score=0.85,
            summary=row["summary"],
            raw_content=str(dict(row)),
            url=row["source_url"] or "",
        )
        for row in result
    ]


def market_indicator_query(arguments: dict[str, Any]) -> list[EvidenceCard]:
    issuer = arguments.get("issuer", "")
    result = rows("select * from market_indicators where issuer_name = ? order by date desc", (issuer,))
    return [
        make_card(
            source_type="mock_db",
            source_name="market_indicators",
            entity=row["issuer_name"],
            risk_tags=["market_risk", "credit_risk"],
            event_type="bond_market_indicator",
            publish_date=row["date"],
            credibility_score=0.88,
            freshness_score=0.88,
            summary=(
                f"{row['asset_name']}价格{row['bond_price']}，到期收益率{row['yield_to_maturity']}%，"
                f"信用利差{row['credit_spread']}bp，近30日利差变化{row['spread_change_30d']}bp。"
            ),
            raw_content=str(dict(row)),
        )
        for row in result
    ]

