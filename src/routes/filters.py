from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from src.database import get_db
from src.main import templates

router = APIRouter(prefix="/filters", tags=["filters"])


@router.get("/campaign", response_class=HTMLResponse)
def get_campaign_filter(request: Request, campaign_id: int | None = Query(None)):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, status FROM campaigns ORDER BY name")
    campaigns = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return templates.TemplateResponse("components/campaign_filter.html", {
        "request": request, "campaigns": campaigns, "selected_id": campaign_id
    })
