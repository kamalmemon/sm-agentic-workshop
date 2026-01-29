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


@router.get("/all", response_class=HTMLResponse)
def get_all_metrics(request: Request, campaign_id: int | None = Query(None)):
    conn = get_db()
    cursor = conn.cursor()

    if campaign_id:
        cursor.execute("""
            SELECT SUM(impressions) as impressions, SUM(clicks) as clicks,
                   SUM(spend) as spend, SUM(conversions) as conversions
            FROM daily_metrics WHERE campaign_id = ?
        """, (campaign_id,))
    else:
        cursor.execute("""
            SELECT SUM(impressions) as impressions, SUM(clicks) as clicks,
                   SUM(spend) as spend, SUM(conversions) as conversions
            FROM daily_metrics
        """)

    row = cursor.fetchone()
    conn.close()

    metrics = [
        {"title": "Impressions", "value": format_number(row["impressions"]), "icon": "eye"},
        {"title": "Clicks", "value": format_number(row["clicks"]), "icon": "cursor"},
        {"title": "Spend", "value": format_currency(row["spend"]), "icon": "currency"},
        {"title": "Conversions", "value": format_number(row["conversions"]), "icon": "chart"},
    ]

    return templates.TemplateResponse("components/metrics_grid.html", {"request": request, "metrics": metrics})
