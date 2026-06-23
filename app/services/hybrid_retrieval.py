from app.schemas import (
    HybridSearchResponse,
    HybridSearchResult,
    SearchRequest,
)
from app.services.retrieval import keyword_search
from app.services.semantic_retrieval import semantic_search


KEYWORD_WEIGHT = 0.35
SEMANTIC_WEIGHT = 0.65


def normalize_keyword_score(score: int, max_score: int) -> float:
    if max_score == 0:
        return 0.0

    return round(score / max_score, 4)


def calculate_hybrid_score(keyword_score: float, semantic_score: float) -> float:
    return round(
        (KEYWORD_WEIGHT * keyword_score) + (SEMANTIC_WEIGHT * semantic_score),
        4,
    )


def hybrid_search(request: SearchRequest) -> HybridSearchResponse:
    keyword_response = keyword_search(request)
    semantic_response = semantic_search(request)

    max_keyword_score = max(
        [result.score for result in keyword_response.results],
        default=0,
    )

    results_by_source: dict[str, dict[str, float | str]] = {}

    for result in keyword_response.results:
        results_by_source[result.source] = {
            "source": result.source,
            "keyword_score": normalize_keyword_score(
                result.score,
                max_keyword_score,
            ),
            "semantic_score": 0.0,
            "snippet": result.snippet,
        }

    for result in semantic_response.results:
        if result.source not in results_by_source:
            results_by_source[result.source] = {
                "source": result.source,
                "keyword_score": 0.0,
                "semantic_score": result.score,
                "snippet": result.snippet,
            }
        else:
            results_by_source[result.source]["semantic_score"] = result.score
            results_by_source[result.source]["snippet"] = result.snippet

    hybrid_results = []

    for result_data in results_by_source.values():
        keyword_score = float(result_data["keyword_score"])
        semantic_score = float(result_data["semantic_score"])

        hybrid_results.append(
            HybridSearchResult(
                source=str(result_data["source"]),
                keyword_score=keyword_score,
                semantic_score=semantic_score,
                hybrid_score=calculate_hybrid_score(
                    keyword_score,
                    semantic_score,
                ),
                snippet=str(result_data["snippet"]),
            )
        )

    hybrid_results.sort(
        key=lambda result: result.hybrid_score,
        reverse=True,
    )

    return HybridSearchResponse(
        query=request.query,
        results=hybrid_results[: request.top_k],
    )