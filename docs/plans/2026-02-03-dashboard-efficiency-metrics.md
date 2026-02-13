# Dashboard Efficiency Metrics Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add 5 efficiency metrics (CTR, CPC, Conversion Rate, CPA, ROAS) to the marketing dashboard so analysts can assess campaign performance at a glance.

**Architecture:** Extend the existing `/metrics/all` endpoint to compute efficiency ratios from aggregated volume metrics. Add new icons to the metric card component for the new metric types. The dashboard grid will expand from 4 to 8 cards (2 rows of 4).

**Tech Stack:** FastAPI, Jinja2, htmx, Tailwind CSS, SQLite

**Jira Epic:** TESTPROJ-12

---

## Task 1: Add Efficiency Metrics Tests

**Files:**
- Modify: `tests/test_metrics.py`

**Step 1: Write the failing tests for efficiency metrics**

Add these tests to `tests/test_metrics.py`:

```python
def test_efficiency_metrics_present(client):
    """Verify all efficiency metrics are displayed."""
    response = client.get("/metrics/all")
    assert response.status_code == 200
    assert "CTR" in response.text
    assert "CPC" in response.text
    assert "Conv. Rate" in response.text
    assert "CPA" in response.text
    assert "ROAS" in response.text


def test_efficiency_metrics_with_campaign_filter(client):
    """Verify efficiency metrics work with campaign filter."""
    response = client.get("/metrics/all?campaign_id=1")
    assert response.status_code == 200
    assert "CTR" in response.text
    assert "ROAS" in response.text
```

**Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_metrics.py -v`

Expected: 2 FAILED (CTR not in response.text)

**Step 3: Commit the failing tests**

```bash
git add tests/test_metrics.py
git commit -m "test: add failing tests for efficiency metrics

TESTPROJ-12"
```

---

## Task 2: Add Formatting Functions for Efficiency Metrics

**Files:**
- Modify: `src/routes/metrics.py:17-22` (after existing format functions)

**Step 1: Add format_percent and format_ratio functions**

Add after the `format_currency` function in `src/routes/metrics.py`:

```python
def format_percent(n: float) -> str:
    """Format as percentage with 2 decimal places."""
    return f"{n:.2f}%"


def format_ratio(n: float) -> str:
    """Format as ratio with 2 decimal places and 'x' suffix."""
    return f"{n:.2f}x"
```

**Step 2: Run existing tests to ensure no regression**

Run: `uv run pytest tests/test_metrics.py -v`

Expected: 2 passed, 2 failed (new tests still fail, existing pass)

**Step 3: Commit**

```bash
git add src/routes/metrics.py
git commit -m "feat: add format_percent and format_ratio helpers

TESTPROJ-12"
```

---

## Task 3: Update SQL Query to Include Revenue

**Files:**
- Modify: `src/routes/metrics.py:31-41` (the SQL queries)

**Step 1: Add revenue to the SELECT statement**

Update both SQL queries in the `get_all_metrics` function to include revenue:

For the filtered query (line 31-35):
```python
    if campaign_id:
        cursor.execute("""
            SELECT SUM(impressions) as impressions, SUM(clicks) as clicks,
                   SUM(spend) as spend, SUM(conversions) as conversions,
                   SUM(revenue) as revenue
            FROM daily_metrics WHERE campaign_id = ?
        """, (campaign_id,))
```

For the unfiltered query (line 36-41):
```python
    else:
        cursor.execute("""
            SELECT SUM(impressions) as impressions, SUM(clicks) as clicks,
                   SUM(spend) as spend, SUM(conversions) as conversions,
                   SUM(revenue) as revenue
            FROM daily_metrics
        """)
```

**Step 2: Run tests to verify no regression**

Run: `uv run pytest tests/test_metrics.py::test_get_all_metrics -v`

Expected: PASSED

**Step 3: Commit**

```bash
git add src/routes/metrics.py
git commit -m "feat: include revenue in metrics query

TESTPROJ-12"
```

---

## Task 4: Compute Efficiency Metrics in Route

**Files:**
- Modify: `src/routes/metrics.py:46-51` (the metrics list)

**Step 1: Add efficiency metric calculations after the volume metrics**

Replace the metrics list in `get_all_metrics` with:

```python
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
```

**Step 2: Run the efficiency metrics tests**

Run: `uv run pytest tests/test_metrics.py -v`

Expected: 4 passed (but may fail if icons not yet in template)

**Step 3: Commit**

```bash
git add src/routes/metrics.py
git commit -m "feat: compute efficiency metrics (CTR, CPC, Conv Rate, CPA, ROAS)

TESTPROJ-12"
```

---

## Task 5: Add New Icons to Metric Card Template

**Files:**
- Modify: `src/templates/components/metric_card.html:17` (add new icon cases)

**Step 1: Add percent and trending icons**

Add these icon cases before the `{% endif %}` in `metric_card.html`:

```html
                {% elif icon == "percent" %}
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
                {% elif icon == "trending" %}
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
```

The full icon section should now look like:

```html
            {% if icon == "eye" %}
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
            {% elif icon == "cursor" %}
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122"></path>
            {% elif icon == "currency" %}
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            {% elif icon == "chart" %}
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            {% elif icon == "percent" %}
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
            {% elif icon == "trending" %}
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
            {% endif %}
```

**Step 2: Run all tests**

Run: `uv run pytest -v`

Expected: 9 passed (7 original + 2 new efficiency tests)

**Step 3: Commit**

```bash
git add src/templates/components/metric_card.html
git commit -m "feat: add percent and trending icons for efficiency metrics

TESTPROJ-12"
```

---

## Task 6: Update Dashboard Grid Layout

**Files:**
- Modify: `src/templates/dashboard.html:10` (update grid classes)

**Step 1: Update grid to show 4 columns on large screens**

Change line 10 from:
```html
         class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"
```

To (add xl breakpoint for better 8-card layout):
```html
         class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-4 xl:grid-cols-4 gap-4"
```

This ensures:
- 2 columns on mobile (2 rows of 4 = 4 rows total for 8 cards)
- 4 columns on tablet and up (2 rows of 4)

**Step 2: Run tests and manually verify layout**

Run: `uv run pytest -v`

Expected: All 9 tests pass

**Step 3: Commit**

```bash
git add src/templates/dashboard.html
git commit -m "feat: update grid layout for 8 metric cards

TESTPROJ-12"
```

---

## Task 7: Final Verification and Documentation

**Step 1: Run full test suite**

Run: `uv run pytest -v`

Expected: 9 passed, 0 failed

**Step 2: Start dev server and verify visually**

Run: `uv run uvicorn src.main:app --reload --port 8000`

Open: http://localhost:8000

Verify:
- [ ] 8 metric cards displayed in 2 rows
- [ ] Volume metrics row: Impressions, Clicks, Spend, Conversions
- [ ] Efficiency metrics row: CTR, CPC, Conv. Rate, CPA, ROAS
- [ ] Filter dropdown works and updates all metrics
- [ ] Icons display correctly for each metric type

**Step 3: Final commit with all changes verified**

```bash
git status
# Ensure working tree is clean
```

---

## Summary

| Task | Description | Files Changed |
|------|-------------|---------------|
| 1 | Add failing tests | tests/test_metrics.py |
| 2 | Add format helpers | src/routes/metrics.py |
| 3 | Update SQL query | src/routes/metrics.py |
| 4 | Compute efficiency metrics | src/routes/metrics.py |
| 5 | Add new icons | src/templates/components/metric_card.html |
| 6 | Update grid layout | src/templates/dashboard.html |
| 7 | Final verification | - |

**Total new tests:** 2
**Total files modified:** 4
**Estimated commits:** 6
