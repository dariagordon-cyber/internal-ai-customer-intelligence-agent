from fastapi.testclient import TestClient

import app.routers.business as business_router
from app.main import app
from app.schemas import HybridSearchResponse, HybridSearchResult


client = TestClient(app)


def test_hybrid_search_endpoint_returns_expected_structure(monkeypatch):
    def fake_hybrid_search(request):
        return HybridSearchResponse(
            query=request.query,
            results=[
                HybridSearchResult(
                    source="meeting_transcripts/medcore_analytics_2026_06_12.txt",
                    hybrid_score=0.8912,
                    keyword_score=0.75,
                    semantic_score=0.9676,
                    snippet="The customer expressed concern about implementation delays.",
                )
            ],
        )

    monkeypatch.setattr(business_router, "hybrid_search", fake_hybrid_search)

    response = client.post(
        "/hybrid-search",
        json={
            "query": "customer is worried about implementation timeline",
            "top_k": 3,
        },
    )

    data = response.json()

    assert response.status_code == 200
    assert data["query"] == "customer is worried about implementation timeline"
    assert isinstance(data["results"], list)
    assert len(data["results"]) == 1
    assert data["results"][0]["source"] == (
        "meeting_transcripts/medcore_analytics_2026_06_12.txt"
    )
    assert isinstance(data["results"][0]["hybrid_score"], float)
    assert isinstance(data["results"][0]["keyword_score"], float)
    assert isinstance(data["results"][0]["semantic_score"], float)
    assert "implementation delays" in data["results"][0]["snippet"]


def test_hybrid_search_endpoint_respects_response_schema(monkeypatch):
    def fake_hybrid_search(request):
        return HybridSearchResponse(
            query=request.query,
            results=[
                HybridSearchResult(
                    source="internal_policies/high_risk_deal_policy.md",
                    hybrid_score=0.8123,
                    keyword_score=0.6,
                    semantic_score=0.9265,
                    snippet="A deal should be treated as high risk if customer concerns are unresolved.",
                )
            ],
        )

    monkeypatch.setattr(business_router, "hybrid_search", fake_hybrid_search)

    response = client.post(
        "/hybrid-search",
        json={"query": "high risk customer concerns", "top_k": 1},
    )

    data = response.json()

    assert response.status_code == 200
    assert set(data.keys()) == {"query", "results"}
    assert set(data["results"][0].keys()) == {
        "source",
        "hybrid_score",
        "keyword_score",
        "semantic_score",
        "snippet",
    }
    assert data["results"][0]["source"] == "internal_policies/high_risk_deal_policy.md"