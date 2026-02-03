def test_get_all_metrics(client):
    response = client.get("/metrics/all")
    assert response.status_code == 200
    assert "Impressions" in response.text
    assert "Clicks" in response.text
    assert "Spend" in response.text
    assert "Conversions" in response.text

def test_get_metrics_with_campaign_filter(client):
    response = client.get("/metrics/all?campaign_id=1")
    assert response.status_code == 200
    assert "Impressions" in response.text


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
