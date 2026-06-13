from __future__ import annotations

import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "data" / "mock_db" / "finrisk.db"
KG_PATH = ROOT / "data" / "kg" / "kg_edges.json"
DOC_PATH = ROOT / "data" / "documents" / "risk_notes.md"


def seed() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript(
        """
        drop table if exists product_risk_metrics;
        drop table if exists holdings;
        drop table if exists issuer_profile;
        drop table if exists market_indicators;
        drop table if exists risk_events;

        create table product_risk_metrics (
            product_id text, product_name text, date text, risk_score real, risk_level text,
            nav_drawdown_7d real, nav_drawdown_30d real, volatility_30d real,
            credit_exposure_score real, liquidity_risk_score real, concentration_score real,
            duration real, leverage_ratio real
        );

        create table holdings (
            product_id text, product_name text, asset_id text, asset_name text, asset_type text,
            issuer_id text, issuer_name text, holding_weight real, market_value real,
            duration real, rating text, industry text, region text
        );

        create table issuer_profile (
            issuer_id text, issuer_name text, industry text, region text, main_business text,
            parent_company text, rating text, rating_outlook text, latest_update_date text
        );

        create table market_indicators (
            asset_id text, asset_name text, issuer_name text, date text, bond_price real,
            yield_to_maturity real, credit_spread real, spread_change_7d real,
            spread_change_30d real, trading_volume real
        );

        create table risk_events (
            event_id text, entity_name text, event_type text, risk_type text, event_date text,
            summary text, source_type text, source_url text, credibility_score real,
            affected_industry text, affected_region text
        );
        """
    )
    cur.executemany(
        "insert into product_risk_metrics values (?,?,?,?,?,?,?,?,?,?,?,?,?)",
        [
            ("P_A", "产品A", "2026-06-10", 78.5, "high", -0.8, -2.4, 4.2, 82, 74, 69, 3.8, 1.12),
            ("P_B", "产品B", "2026-06-10", 55.0, "medium", -0.2, -0.9, 2.1, 48, 44, 39, 2.4, 1.03),
            ("P_C", "稳健固收3号", "2026-06-10", 68.0, "medium_high", -0.5, -1.8, 3.1, 66, 58, 61, 3.1, 1.08),
        ],
    )
    cur.executemany(
        "insert into holdings values (?,?,?,?,?,?,?,?,?,?,?,?,?)",
        [
            ("P_A", "产品A", "BOND_VANKE_01", "万科债券", "bond", "ISS_VANKE", "万科", 8.6, 8600000, 2.7, "AAA", "房地产", "广东"),
            ("P_A", "产品A", "BOND_LONGFOR_01", "龙湖债券", "bond", "ISS_LONGFOR", "龙湖", 4.2, 4200000, 2.1, "AAA", "房地产", "重庆"),
            ("P_B", "产品B", "BOND_CDB_01", "国开债", "bond", "ISS_CDB", "国开行", 12.0, 12000000, 4.9, "AAA", "金融", "北京"),
        ],
    )
    cur.executemany(
        "insert into issuer_profile values (?,?,?,?,?,?,?,?,?)",
        [
            ("ISS_VANKE", "万科", "房地产", "广东", "房地产开发与物业服务", "", "AAA", "稳定观察", "2026-06-01"),
            ("ISS_LONGFOR", "龙湖", "房地产", "重庆", "房地产开发与商业运营", "", "AAA", "稳定", "2026-05-25"),
        ],
    )
    cur.executemany(
        "insert into market_indicators values (?,?,?,?,?,?,?,?,?,?)",
        [
            ("BOND_VANKE_01", "万科债券", "万科", "2026-06-10", 96.8, 5.42, 186, 18, 54, 2100000),
            ("BOND_LONGFOR_01", "龙湖债券", "龙湖", "2026-06-10", 99.2, 4.32, 112, 4, 11, 2800000),
        ],
    )
    cur.executemany(
        "insert into risk_events values (?,?,?,?,?,?,?,?,?,?,?)",
        [
            ("EV001", "万科", "financing_pressure", "liquidity_risk", "2026-05-20", "市场信息显示主体融资环境边际收紧，部分债券信用利差走阔。", "news", "", 0.78, "房地产", "广东"),
            ("EV002", "房地产", "sales_pressure", "industry_risk", "2026-05-28", "房地产销售修复偏弱，行业现金流恢复仍需观察。", "industry_report", "", 0.82, "房地产", ""),
            ("EV003", "产品A", "risk_score_up", "product_risk", "2026-06-10", "产品A信用暴露分和集中度分上升，近30日回撤扩大。", "mock_metric", "", 0.9, "", ""),
        ],
    )
    conn.commit()
    conn.close()

    KG_PATH.parent.mkdir(parents=True, exist_ok=True)
    KG_PATH.write_text(
        json.dumps(
            [
                {"head": "产品A", "relation": "holds", "tail": "万科债券", "weight": 0.86},
                {"head": "万科债券", "relation": "issued_by", "tail": "万科", "weight": 0.95},
                {"head": "万科", "relation": "belongs_to", "tail": "房地产", "weight": 0.9},
                {"head": "房地产", "relation": "affected_by", "tail": "地产销售压力", "weight": 0.75},
                {"head": "融资环境收紧", "relation": "impacts", "tail": "万科", "weight": 0.72},
                {"head": "万科", "relation": "impacts", "tail": "产品A", "weight": 0.68},
            ],
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.write_text(
        """
# 投后风控研究笔记

房地产主体信用风险归因通常需要同时检查：主体评级展望、债务到期压力、现金流恢复、行业销售和融资环境、债券二级市场收益率与信用利差。

若产品对单一主体相关债券持仓权重较高，主体信用利差走阔可能通过估值下跌和流动性折价传导到产品风险评分、回撤和集中度指标。
""".strip(),
        encoding="utf-8",
    )


if __name__ == "__main__":
    seed()
    print(f"Seeded mock data: {DB_PATH}")

