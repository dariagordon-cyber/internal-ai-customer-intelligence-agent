import re

from app.schemas import SearchRequest, SearchResponse, SearchResult
from app.services.data_loader import (
    load_internal_policies,
    load_meeting_transcripts,
)


def tokenize(text: str) -> list[str]:
    return re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())


def build_document_collection() -> dict[str, str]:
    documents = {}

    for filename, content in load_internal_policies().items():
        documents[f"internal_policies/{filename}"] = content

    for filename, content in load_meeting_transcripts().items():
        documents[f"meeting_transcripts/{filename}"] = content

    return documents


def create_snippet(content: str, query_terms: set[str], max_length: int = 240) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", content.strip())

    for sentence in sentences:
        sentence_terms = set(tokenize(sentence))
        if sentence_terms & query_terms:
            return sentence[:max_length]

    return content.strip()[:max_length]


def keyword_search(request: SearchRequest) -> SearchResponse:
    documents = build_document_collection()
    query_terms = set(tokenize(request.query))

    results = []

    for source, content in documents.items():
        document_terms = tokenize(content)
        score = sum(1 for term in query_terms if term in document_terms)

        if score > 0:
            results.append(
                SearchResult(
                    source=source,
                    score=score,
                    snippet=create_snippet(content, query_terms),
                )
            )

    results.sort(key=lambda result: result.score, reverse=True)

    return SearchResponse(
        query=request.query,
        results=results[: request.top_k],
    )