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


def test_customer_brief_uses_mock_customer_data():
    response = client.post(
        "/customer-brief",
        json={"customer_id": "C002"},
    )

    data = response.json()

    assert response.status_code == 200
    assert data["company_name"] == "MedCore Analytics"
    assert "Healthcare customer in Germany" in data["summary"]
    assert "health score is 45" in data["summary"]
    assert "crm_customers.csv" in data["sources"]
    assert "sales_pipeline.csv" in data["sources"]
    assert "medcore_analytics_2026_06_12.txt" in data["sources"]


def test_customer_brief_handles_unknown_customer_id():
    response = client.post(
        "/customer-brief",
        json={"customer_id": "UNKNOWN"},
    )

    data = response.json()

    assert response.status_code == 200
    assert data["customer_id"] == "UNKNOWN"
    assert data["company_name"] == "Unknown customer"
    assert "No customer record was found" in data["summary"]
    assert "Customer data is missing." in data["risks"]


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


def test_pipeline_insights_filters_by_region():
    response = client.post(
        "/pipeline-insights",
        json={"region": "Germany"},
    )

    data = response.json()

    assert response.status_code == 200
    assert data["total_pipeline_value"] == 80000.0
    assert len(data["high_risk_deals"]) == 1
    assert data["high_risk_deals"][0]["deal_id"] == "D002"
    assert data["high_risk_deals"][0]["customer_id"] == "C002"


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


def test_meeting_summary_uses_transcript_source():
    response = client.post(
        "/meeting-summary",
        json={"customer_id": "C002"},
    )

    data = response.json()

    assert response.status_code == 200
    assert data["sentiment"] == "concerned"
    assert "medcore_analytics_2026_06_12.txt" in data["sources"]
    assert "Integration documentation is missing." in data["customer_concerns"]


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


def test_ask_endpoint_uses_mock_dataset_summary():
    response = client.post(
        "/ask",
        json={"question": "Which customers are at risk and why?"},
    )

    data = response.json()

    assert response.status_code == 200
    assert "5 customers" in data["answer"]
    assert "5 open deals" in data["answer"]
    assert "1 high-risk deals" in data["answer"]
    assert "crm_customers.csv" in data["sources"]
    assert "sales_pipeline.csv" in data["sources"]
    assert "Relevant internal documents were found" in data["answer"]
    assert any(
        "internal_policies/" in source or "meeting_transcripts/" in source
        for source in data["sources"]
    )


def test_search_endpoint_returns_relevant_documents():
    response = client.post(
        "/search",
        json={"query": "implementation delays onboarding", "top_k": 3},
    )

    data = response.json()

    assert response.status_code == 200
    assert data["query"] == "implementation delays onboarding"
    assert isinstance(data["results"], list)
    assert len(data["results"]) >= 1
    assert data["results"][0]["score"] > 0


def test_search_endpoint_respects_top_k():
    response = client.post(
        "/search",
        json={"query": "customer risk deal", "top_k": 1},
    )

    data = response.json()

    assert response.status_code == 200
    assert len(data["results"]) <= 1


def test_search_endpoint_ranks_more_relevant_document_first():
    response = client.post(
        "/search",
        json={"query": "implementation onboarding documentation", "top_k": 3},
    )

    data = response.json()

    assert response.status_code == 200
    assert len(data["results"]) >= 1
    assert data["results"][0]["source"] == (
        "meeting_transcripts/medcore_analytics_2026_06_12.txt"
    )


def test_search_endpoint_ignores_common_stopwords():
    response = client.post(
        "/search",
        json={"query": "what are the implementation risks", "top_k": 3},
    )

    data = response.json()

    assert response.status_code == 200
    assert len(data["results"]) >= 1
    assert all(result["score"] > 0 for result in data["results"])