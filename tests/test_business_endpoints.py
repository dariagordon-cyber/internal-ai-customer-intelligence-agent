from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_customer_brief_endpoint_returns_expected_structure():
    response = client.post(
        "/customer-brief",
        json={"customer_id": "C002"},
    )

    data = response.json()

    assert response.status_code == 200
    assert data["customer_id"] == "C002"
    assert "summary" in data
    assert isinstance(data["risks"], list)
    assert isinstance(data["recommended_actions"], list)
    assert isinstance(data["sources"], list)


def test_pipeline_insights_endpoint_returns_expected_structure():
    response = client.post(
        "/pipeline-insights",
        json={"region": "Germany"},
    )

    data = response.json()

    assert response.status_code == 200
    assert "total_pipeline_value" in data
    assert isinstance(data["high_risk_deals"], list)
    assert isinstance(data["main_risks"], list)
    assert isinstance(data["recommendations"], list)


def test_meeting_summary_endpoint_returns_expected_structure():
    response = client.post(
        "/meeting-summary",
        json={"customer_id": "C002"},
    )

    data = response.json()

    assert response.status_code == 200
    assert data["customer_id"] == "C002"
    assert "summary" in data
    assert isinstance(data["customer_concerns"], list)
    assert isinstance(data["action_items"], list)
    assert data["sentiment"] in ["positive", "neutral", "concerned", "negative"]


def test_ask_endpoint_returns_answer_with_sources():
    response = client.post(
        "/ask",
        json={"question": "Which customers are at risk and why?"},
    )

    data = response.json()

    assert response.status_code == 200
    assert "answer" in data
    assert isinstance(data["sources"], list)
    assert data["confidence"] in ["low", "medium", "high"]