def test_get_impressions_over_time(client):
    response = client.get("/charts/impressions-over-time")
    assert response.status_code == 200
    assert "impressions-chart" in response.text

def test_get_clicks_by_campaign(client):
    response = client.get("/charts/clicks-by-campaign")
    assert response.status_code == 200
    assert "clicks-chart" in response.text

def test_charts_with_filter(client):
    response = client.get("/charts/impressions-over-time?campaign_id=1")
    assert response.status_code == 200
