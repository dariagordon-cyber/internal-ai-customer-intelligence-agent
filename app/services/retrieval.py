import re
from collections import Counter

from app.schemas import SearchRequest, SearchResponse, SearchResult
from app.services.data_loader import (
    load_internal_policies,
    load_meeting_transcripts,
)


STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "are",
    "was",
    "were",
    "from",
    "have",
    "has",
    "had",
    "what",
    "which",
    "who",
    "why",
    "how",
    "into",
    "about",
    "using",
    "should",
    "could",
    "would",
    "their",
    "there",
    "when",
    "where",
}


def tokenize(text: str) -> list[str]:
    tokens = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    return [token for token in tokens if token not in STOPWORDS]


def build_document_collection() -> dict[str, str]:
    documents = {}

    for filename, content in load_internal_policies().items():
        documents[f"internal_policies/{filename}"] = content

    for filename, content in load_meeting_transcripts().items():
        documents[f"meeting_transcripts/{filename}"] = content

    return documents


def calculate_keyword_score(query_terms: list[str], document_terms: list[str]) -> int:
    document_term_counts = Counter(document_terms)

    return sum(
        document_term_counts[term]
        for term in query_terms
        if term in document_term_counts
    )


def create_snippet(content: str, query_terms: set[str], max_length: int = 240) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", content.strip())

    best_sentence = ""
    best_score = 0

    for sentence in sentences:
        sentence_terms = tokenize(sentence)
        sentence_score = sum(1 for term in sentence_terms if term in query_terms)

        if sentence_score > best_score:
            best_score = sentence_score
            best_sentence = sentence

    if best_sentence:
        return best_sentence.strip()[:max_length]

    return content.strip()[:max_length]


def keyword_search(request: SearchRequest) -> SearchResponse:
    documents = build_document_collection()
    query_terms = tokenize(request.query)
    query_term_set = set(query_terms)

    results = []

    for source, content in documents.items():
        document_terms = tokenize(content)
        score = calculate_keyword_score(query_terms, document_terms)

        if score > 0:
            results.append(
                SearchResult(
                    source=source,
                    score=score,
                    snippet=create_snippet(content, query_term_set),
                )
            )

    results.sort(key=lambda result: result.score, reverse=True)

    return SearchResponse(
        query=request.query,
        results=results[: request.top_k],
    )