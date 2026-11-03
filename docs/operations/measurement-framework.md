# Measurement Framework

| Metric | Formula | Interpretation |
|---|---|---|
| Net revenue | Sum of completed net order revenue | Recognized simulated sales |
| Orders | Count of completed orders | Completed transactions |
| AOV | Net revenue / completed orders | Average order value |
| Gross profit | Net revenue - estimated product cost | Before marketing and operating expenses |
| Gross margin | Gross profit / net revenue | Product-level margin proxy |
| CTR | Clicks / impressions | Ad click-through rate |
| CPC | Spend / clicks | Average cost per click |
| CPA | Spend / attributed orders | Cost per attributed order |
| ROAS | Attributed revenue / spend | Platform/campaign modeled return |
| Funnel purchase rate | Purchases / sessions | Session-to-purchase rate |
| Cart abandonment | (Carts - purchases) / carts | Simplified proxy; stages must align |

## Caveats
- The generated order data and campaign attribution are independent synthetic tables.
- Campaign attributed revenue must not be added to order revenue.
- CPA and ROAS use campaign-provided attributed orders/revenue.
- Funnel metrics are aggregate monthly snapshots.
- Gross profit excludes shipping, payment fees, returns handling, overhead, and marketing.
- These figures are not audited financial results.
