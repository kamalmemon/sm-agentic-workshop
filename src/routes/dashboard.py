from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from src.main import templates

router = APIRouter(tags=["dashboard"])


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
