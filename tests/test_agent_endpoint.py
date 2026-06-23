from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_agent_selects_customer_brief_tool():
    response = client.post(
        "/agent",
        json={
            "question": "Give me a customer brief for this account",
            "customer_id": "C002",
        },
    )

    data = response.json()

    assert response.status_code == 200
    assert data["selected_tool"] == "customer_brief"
    assert "customer-level account intelligence" in data["tool_reason"]
    assert "MedCore Analytics" in data["answer"]
    assert "crm_customers.csv" in data["sources"]
    assert data["confidence"] == "high"


def test_agent_selects_pipeline_insights_tool():
    response = client.post(
        "/agent",
        json={
            "question": "What are the main pipeline risks in Germany?",
            "region": "Germany",
        },
    )

    data = response.json()

    assert response.status_code == 200
    assert data["selected_tool"] == "pipeline_insights"
    assert "sales pipeline" in data["tool_reason"]
    assert "Total pipeline value: 80000.0" in data["answer"]
    assert "sales_pipeline.csv" in data["sources"]
    assert data["confidence"] == "high"


def test_agent_selects_meeting_summary_tool():
    response = client.post(
        "/agent",
        json={
            "question": "Summarize the latest meeting with this customer",
            "customer_id": "C002",
        },
    )

    data = response.json()

    assert response.status_code == 200
    assert data["selected_tool"] == "meeting_summary"
    assert "meeting or transcript" in data["tool_reason"]
    assert "implementation delays" in data["answer"]
    assert "medcore_analytics_2026_06_12.txt" in data["sources"]
    assert data["confidence"] == "high"


def test_agent_returns_low_confidence_when_customer_id_is_missing():
    response = client.post(
        "/agent",
        json={
            "question": "Give me a customer brief for this account",
        },
    )

    data = response.json()

    assert response.status_code == 200
    assert data["selected_tool"] == "customer_brief"
    assert "requires a customer_id" in data["answer"]
    assert data["sources"] == []
    assert data["confidence"] == "low"