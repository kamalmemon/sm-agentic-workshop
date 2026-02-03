from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from src.database import get_db
from src.main import templates

router = APIRouter(prefix="/metrics", tags=["metrics"])


def format_number(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def format_currency(n: float) -> str:
    if n >= 1_000_000:
        return f"${n / 1_000_000:.2f}M"
    elif n >= 1_000:
        return f"${n / 1_000:.1f}K"
    return f"${n:,.2f}"


def format_percent(n: float) -> str:
    """Format as percentage with 2 decimal places."""
    return f"{n:.2f}%"


def format_ratio(n: float) -> str:
    """Format as ratio with 2 decimal places and 'x' suffix."""
    return f"{n:.2f}x"


@router.get("/all", response_class=HTMLResponse)
def get_all_metrics(request: Request, campaign_id: int | None = Query(None)):
    conn = get_db()
    cursor = conn.cursor()

    if campaign_id:
        cursor.execute("""
            SELECT SUM(impressions) as impressions, SUM(clicks) as clicks,
                   SUM(spend) as spend, SUM(conversions) as conversions,
                   SUM(revenue) as revenue
            FROM daily_metrics WHERE campaign_id = ?
        """, (campaign_id,))
    else:
        cursor.execute("""
            SELECT SUM(impressions) as impressions, SUM(clicks) as clicks,
                   SUM(spend) as spend, SUM(conversions) as conversions,
                   SUM(revenue) as revenue
            FROM daily_metrics
        """)

    row = cursor.fetchone()
    conn.close()

    # Volume metrics
    metrics = [
        {"title": "Impressions", "value": format_number(row["impressions"]), "icon": "eye"},
        {"title": "Clicks", "value": format_number(row["clicks"]), "icon": "cursor"},
        {"title": "Spend", "value": format_currency(row["spend"]), "icon": "currency"},
        {"title": "Conversions", "value": format_number(row["conversions"]), "icon": "chart"},
    ]

    # Efficiency metrics (with safe division)
    clicks = row["clicks"] or 1  # Avoid division by zero
    impressions = row["impressions"] or 1
    conversions = row["conversions"] or 1
    spend = row["spend"] or 0
    revenue = row["revenue"] or 0

    ctr = (clicks / impressions) * 100
    cpc = spend / clicks
    conv_rate = (conversions / clicks) * 100
    cpa = spend / conversions
    roas = revenue / spend if spend > 0 else 0

    metrics.extend([
        {"title": "CTR", "value": format_percent(ctr), "icon": "percent"},
        {"title": "CPC", "value": format_currency(cpc), "icon": "currency"},
        {"title": "Conv. Rate", "value": format_percent(conv_rate), "icon": "percent"},
        {"title": "CPA", "value": format_currency(cpa), "icon": "currency"},
        {"title": "ROAS", "value": format_ratio(roas), "icon": "trending"},
    ])

    return templates.TemplateResponse("components/metrics_grid.html", {"request": request, "metrics": metrics})
