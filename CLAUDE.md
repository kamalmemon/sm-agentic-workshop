# Marketing Analytics Dashboard

FastAPI + htmx + Tailwind + SQLite dashboard for ad campaign analytics.

## Commands
- `make run` - start dev server (port 8000)
- `make run PORT=3000` - start on custom port
- `make test` - run tests
- `make verify` - verify workshop setup
- `make reset-db` - reset database with fresh data

## Structure
- `src/routes/` - API endpoints returning HTML partials for htmx
- `src/templates/components/` - Jinja2 partials for htmx swaps
- `src/models.py` - Pydantic models
- Metrics computed on-the-fly from daily_metrics table

## Conventions
- New metric cards: add route in metrics.py, template in components/
- Charts use Chart.js, data fetched via htmx from charts.py
- All endpoints should have tests
- Use Tailwind utility classes for styling
