from app.schemas import HybridSearchResult
from app.services.llm_service import (
    build_fallback_grounded_answer,
    build_retrieval_context,
    generate_grounded_answer,
)


def test_build_retrieval_context_includes_sources_and_scores():
    results = [
        HybridSearchResult(
            source="internal_policies/high_risk_deal_policy.md",
            hybrid_score=0.8123,
            keyword_score=0.6,
            semantic_score=0.9265,
            snippet="High-risk deals require proactive account management.",
        )
    ]

    context = build_retrieval_context(results)

    assert "Source: internal_policies/high_risk_deal_policy.md" in context
    assert "Hybrid score: 0.8123" in context
    assert "Keyword score: 0.6" in context
    assert "Semantic score: 0.9265" in context
    assert "High-risk deals require proactive account management." in context


def test_generate_grounded_answer_uses_fallback_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    results = [
        HybridSearchResult(
            source="meeting_transcripts/medcore_analytics_2026_06_12.txt",
            hybrid_score=0.8912,
            keyword_score=0.75,
            semantic_score=0.9676,
            snippet="The customer expressed concern about implementation delays.",
        )
    ]

    answer, confidence = generate_grounded_answer(
        question="Which customers are at risk?",
        results=results,
    )

    assert confidence == "medium"
    assert "retrieved internal context" in answer
    assert "meeting_transcripts/medcore_analytics_2026_06_12.txt" in answer
    assert "implementation delays" in answer


def test_build_fallback_grounded_answer_handles_empty_results():
    answer = build_fallback_grounded_answer(
        question="Which customers are at risk?",
        results=[],
    )

    assert "No directly relevant internal documents" in answer