# NOVA | E-commerce, Retail & Marketing Growth Project

> A portfolio-ready proof of concept simulating the work of an in-house e-commerce growth team or a marketing agency serving a retail client.

## Project status
- Type: Portfolio / Proof of Concept
- Business: Fictional Egyptian fashion e-commerce retailer
- Data: 100% synthetic, generated for demonstration
- Currency: EGP
- Time horizon: 30-day campaign planning scenario
- Important: No real customer, transaction, advertising, or company data is used.

## Business brief
NOVA is a fictional online fashion and accessories retailer. The business wants to improve acquisition efficiency, conversion, average order value, and repeat purchasing.

The project demonstrates an end-to-end workflow:
1. Market and competitor research framework
2. Customer personas and segmentation
3. Customer journey mapping
4. Marketing strategy and 30-day campaign planning
5. Content calendar, copywriting, and creative briefs
6. Paid media allocation and campaign measurement
7. E-commerce conversion rate optimization (CRO)
8. CRM, lifecycle messaging, and retention
9. Sales, customer, and campaign analytics
10. Executive reporting and recommendations

## Repository structure

```text
NOVA-Ecommerce-Growth/
├── assets/
│   ├── creative-briefs/
│   └── design-exports/
├── data/
│   ├── raw/                 # Synthetic source CSV files
│   └── processed/           # Generated analytical outputs
├── docs/
│   ├── campaigns/
│   ├── operations/
│   ├── research/
│   └── strategy/
├── reports/                 # KPI summary and executive report
├── src/nova_marketing/      # Reproducible analytics pipeline
├── tests/                   # Standard-library unit tests
├── README.md
└── requirements.txt
```

## Quick start (Windows PowerShell)

The builder script creates this repository and its synthetic data. After generation:

```powershell
python --version
python .\src\nova_marketing\run_analysis.py
python -m unittest discover -s tests -v
```

The analytics pipeline uses Python's standard library; no third-party package is required.

## Key metrics
The pipeline calculates:
- Net revenue and completed orders
- Average order value (AOV)
- Gross profit and gross margin (using the product cost table)
- Campaign click-through rate (CTR)
- Cost per click (CPC)
- Cost per acquisition (CPA)
- Return on ad spend (ROAS)
- Funnel conversion and cart abandonment rates
- Customer segment and channel summaries

Metric definitions and assumptions are documented in `docs/operations/measurement-framework.md`.

## Important analytical assumptions
- Cancelled and returned orders are excluded from recognized sales in the analytics pipeline.
- Campaign attributed revenue is modeled separately from total order revenue; do not add them together.
- Synthetic campaign results are illustrative, not evidence of actual ad performance.
- Customer segment labels are synthetic labels, not inferred from real behavior.
- No causal claim is made that marketing spend caused the simulated revenue.

## Deliverables
- Market research and competitor audit template
- Customer personas and journey map
- 30-day campaign strategy
- 14-day content calendar
- Paid media plan and budget
- CRO audit and product-page recommendations
- CRM lifecycle messages
- Python KPI pipeline and CSV outputs
- Executive summary report

## Next improvements
- Replace synthetic data with a properly licensed public dataset or anonymized client data.
- Connect GA4 / Shopify / WooCommerce exports.
- Add cohort retention and RFM segmentation.
- Build a Power BI dashboard.
- Add channel-level attribution assumptions and sensitivity analysis.
- Add automated data quality checks and CI with GitHub Actions.

## Skills demonstrated
Digital Marketing | E-commerce Operations | Retail Analytics | Market Research | Competitor Analysis | Customer Segmentation | Content Strategy | Copywriting | Paid Media Planning | CRO | CRM | Excel/CSV Analytics | Python | KPI Reporting

## Reproducibility
The dataset is generated with a fixed random seed by the PowerShell builder. Re-running the builder requires an empty target directory. The Python analysis can be run repeatedly without changing source data.
