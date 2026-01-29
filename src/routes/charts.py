from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from src.database import get_db
from src.main import templates

router = APIRouter(prefix="/charts", tags=["charts"])


@router.get("/impressions-over-time", response_class=HTMLResponse)
def get_impressions_over_time(request: Request, campaign_id: int | None = Query(None)):
    conn = get_db()
    cursor = conn.cursor()

    if campaign_id:
        cursor.execute("""
            SELECT date, SUM(impressions) as impressions FROM daily_metrics
            WHERE campaign_id = ? GROUP BY date ORDER BY date LIMIT 30
        """, (campaign_id,))
    else:
        cursor.execute("""
            SELECT date, SUM(impressions) as impressions FROM daily_metrics
            GROUP BY date ORDER BY date LIMIT 30
        """)

    rows = cursor.fetchall()
    conn.close()

    labels = [row["date"][5:] for row in rows]
    data = [row["impressions"] for row in rows]

    return templates.TemplateResponse("components/line_chart.html", {
        "request": request, "title": "Impressions Over Time",
        "chart_id": "impressions-chart", "labels": labels, "data": data, "label": "Impressions"
    })


@router.get("/clicks-by-campaign", response_class=HTMLResponse)
def get_clicks_by_campaign(request: Request, campaign_id: int | None = Query(None)):
    conn = get_db()
    cursor = conn.cursor()

    if campaign_id:
        cursor.execute("""
            SELECT c.name, SUM(m.clicks) as clicks FROM daily_metrics m
            JOIN campaigns c ON m.campaign_id = c.id
            WHERE m.campaign_id = ? GROUP BY c.id
        """, (campaign_id,))
    else:
        cursor.execute("""
            SELECT c.name, SUM(m.clicks) as clicks FROM daily_metrics m
            JOIN campaigns c ON m.campaign_id = c.id
            GROUP BY c.id ORDER BY clicks DESC
        """)

    rows = cursor.fetchall()
    conn.close()

    labels = [row["name"] for row in rows]
    data = [row["clicks"] for row in rows]

    return templates.TemplateResponse("components/bar_chart.html", {
        "request": request, "title": "Clicks by Campaign",
        "chart_id": "clicks-chart", "labels": labels, "data": data, "label": "Clicks"
    })
