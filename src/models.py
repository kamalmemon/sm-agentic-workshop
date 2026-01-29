from pydantic import BaseModel
from datetime import date


class Campaign(BaseModel):
    id: int
    name: str
    status: str
    created_at: date


class DailyMetric(BaseModel):
    id: int
    campaign_id: int
    date: date
    impressions: int
    clicks: int
    spend: float
    conversions: int
    revenue: float


class MetricSummary(BaseModel):
    impressions: int
    clicks: int
    spend: float
    conversions: int
