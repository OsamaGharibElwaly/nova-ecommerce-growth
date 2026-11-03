"""Reproducible KPI pipeline for the synthetic NOVA e-commerce dataset."""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"


def read_csv(name: str) -> list[dict]:
    with (RAW / name).open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def money(value: float) -> float:
    return round(value, 2)


def main() -> dict:
    products = {r["product_id"]: r for r in read_csv("products.csv")}
    orders = read_csv("orders.csv")
    campaigns = read_csv("campaigns.csv")
    funnel = read_csv("funnel.csv")
    customers = read_csv("customers.csv")

    completed = [r for r in orders if r["order_status"] == "Completed"]
    net_revenue = sum(float(r["net_revenue"]) for r in completed)
    total_cost = sum(
        int(r["quantity"]) * float(products[r["product_id"]]["unit_cost"])
        for r in completed
    )
    gross_profit = net_revenue - total_cost
    order_count = len(completed)
    aov = net_revenue / order_count if order_count else 0.0

    campaign_rows = []
    for c in campaigns:
        spend = float(c["spend"])
        impressions = int(c["impressions"])
        clicks = int(c["clicks"])
        attributed_orders = int(c["attributed_orders"])
        attributed_revenue = float(c["attributed_revenue"])
        campaign_rows.append({
            "campaign_id": c["campaign_id"],
            "campaign_name": c["campaign_name"],
            "platform": c["platform"],
            "spend_egp": money(spend),
            "impressions": impressions,
            "clicks": clicks,
            "ctr_pct": money(clicks / impressions * 100) if impressions else 0,
            "cpc_egp": money(spend / clicks) if clicks else 0,
            "attributed_orders": attributed_orders,
            "cpa_egp": money(spend / attributed_orders) if attributed_orders else 0,
            "attributed_revenue_egp": money(attributed_revenue),
            "roas": money(attributed_revenue / spend) if spend else 0,
        })
    write_csv(PROCESSED / "campaign_kpis.csv", campaign_rows)

    product_summary = defaultdict(lambda: {"units": 0, "revenue": 0.0, "cost": 0.0})
    for r in completed:
        p = products[r["product_id"]]
        q = int(r["quantity"])
        product_summary[r["product_id"]]["units"] += q
        product_summary[r["product_id"]]["revenue"] += float(r["net_revenue"])
        product_summary[r["product_id"]]["cost"] += q * float(p["unit_cost"])
    product_rows = []
    for pid, values in product_summary.items():
        product_rows.append({
            "product_id": pid,
            "product_name": products[pid]["product_name"],
            "units_sold": values["units"],
            "net_revenue_egp": money(values["revenue"]),
            "gross_profit_egp": money(values["revenue"] - values["cost"]),
        })
    product_rows.sort(key=lambda x: x["net_revenue_egp"], reverse=True)
    write_csv(PROCESSED / "product_performance.csv", product_rows)

    segment_counts = defaultdict(int)
    for c in customers:
        segment_counts[c["customer_segment"]] += 1
    segment_rows = [
        {"customer_segment": k, "customer_count": v}
        for k, v in sorted(segment_counts.items())
    ]
    write_csv(PROCESSED / "customer_segments.csv", segment_rows)

    sessions = sum(int(r["sessions"]) for r in funnel)
    carts = sum(int(r["add_to_carts"]) for r in funnel)
    purchases = sum(int(r["purchases"]) for r in funnel)
    total_spend = sum(float(r["spend"]) for r in campaigns)
    total_attributed_revenue = sum(float(r["attributed_revenue"]) for r in campaigns)
    total_attributed_orders = sum(int(r["attributed_orders"]) for r in campaigns)

    summary = {
        "data_type": "synthetic",
        "completed_orders": order_count,
        "net_revenue_egp": money(net_revenue),
        "average_order_value_egp": money(aov),
        "estimated_product_cost_egp": money(total_cost),
        "gross_profit_egp": money(gross_profit),
        "gross_margin_pct": money(gross_profit / net_revenue * 100) if net_revenue else 0,
        "campaign_spend_egp": money(total_spend),
        "campaign_attributed_revenue_egp": money(total_attributed_revenue),
        "campaign_attributed_orders": total_attributed_orders,
        "blended_campaign_roas": money(total_attributed_revenue / total_spend) if total_spend else 0,
        "funnel_sessions": sessions,
        "funnel_purchases": purchases,
        "session_to_purchase_rate_pct": money(purchases / sessions * 100) if sessions else 0,
        "simplified_cart_abandonment_pct": money((carts - purchases) / carts * 100) if carts else 0,
        "customer_count": len(customers),
        "top_product_by_revenue": product_rows[0]["product_name"] if product_rows else None,
        "notes": [
            "Synthetic demonstration data only.",
            "Campaign attribution is modeled separately from order revenue.",
            "Gross profit excludes operating costs, shipping, payment fees, and marketing."
        ],
    }

    PROCESSED.mkdir(parents=True, exist_ok=True)
    (PROCESSED / "kpi_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    REPORTS.mkdir(parents=True, exist_ok=True)
    report = f"""# NOVA — Synthetic Performance Snapshot

> Generated from synthetic demonstration data. Not real business performance.

| Metric | Value |
|---|---:|
| Completed orders | {summary['completed_orders']:,} |
| Net revenue | {summary['net_revenue_egp']:,.2f} EGP |
| Average order value | {summary['average_order_value_egp']:,.2f} EGP |
| Estimated gross profit | {summary['gross_profit_egp']:,.2f} EGP |
| Gross margin | {summary['gross_margin_pct']:.2f}% |
| Campaign spend | {summary['campaign_spend_egp']:,.2f} EGP |
| Campaign-attributed revenue | {summary['campaign_attributed_revenue_egp']:,.2f} EGP |
| Blended campaign ROAS | {summary['blended_campaign_roas']:.2f}x |
| Session-to-purchase rate | {summary['session_to_purchase_rate_pct']:.2f}% |
| Simplified cart abandonment | {summary['simplified_cart_abandonment_pct']:.2f}% |

## Top product
{summary['top_product_by_revenue'] or 'Not available'}

## Interpretation notes
- Campaign-attributed revenue is separate from order revenue and must not be added to it.
- ROAS is based on the synthetic campaign attribution table.
- Gross profit is a product-level estimate before operating expenses and marketing.
- Funnel rates are calculated from aggregate monthly snapshots.
"""
    (REPORTS / "executive-kpi-report.md").write_text(report, encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    main()
