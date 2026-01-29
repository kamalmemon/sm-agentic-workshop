def test_get_campaign_filter(client):
    response = client.get("/filters/campaign")
    assert response.status_code == 200
    assert "Summer Sale 2026" in response.text
    assert "All Campaigns" in response.text

def test_filter_with_selected(client):
    response = client.get("/filters/campaign?campaign_id=1")
    assert response.status_code == 200
    assert "selected" in response.text
