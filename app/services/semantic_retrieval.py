from functools import lru_cache

import chromadb
from sentence_transformers import SentenceTransformer

from app.schemas import (
    SearchRequest,
    SemanticSearchResponse,
    SemanticSearchResult,
)
from app.services.retrieval import build_document_collection


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
COLLECTION_NAME = "internal_business_documents"


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_embedding_model()
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
    )

    return embeddings.tolist()


@lru_cache(maxsize=1)
def build_semantic_collection():
    documents = build_document_collection()

    client = chromadb.Client()
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    sources = list(documents.keys())
    contents = list(documents.values())

    if not contents:
        return collection

    embeddings = embed_texts(contents)

    collection.add(
        ids=sources,
        documents=contents,
        embeddings=embeddings,
        metadatas=[{"source": source} for source in sources],
    )

    return collection


def create_semantic_snippet(content: str, max_length: int = 240) -> str:
    clean_content = content.strip().replace("\n", " ")

    if len(clean_content) <= max_length:
        return clean_content

    return clean_content[:max_length].rstrip() + "..."


def distance_to_similarity(distance: float) -> float:
    return round(1 / (1 + distance), 4)


def semantic_search(request: SearchRequest) -> SemanticSearchResponse:
    documents = build_document_collection()

    if not documents:
        return SemanticSearchResponse(query=request.query, results=[])

    collection = build_semantic_collection()
    query_embedding = embed_texts([request.query])[0]

    n_results = min(request.top_k, len(documents))

    query_results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    sources = query_results["ids"][0]
    retrieved_documents = query_results["documents"][0]
    distances = query_results["distances"][0]

    results = [
        SemanticSearchResult(
            source=source,
            score=distance_to_similarity(distance),
            snippet=create_semantic_snippet(document),
        )
        for source, document, distance in zip(
            sources,
            retrieved_documents,
            distances,
            strict=True,
        )
    ]

    return SemanticSearchResponse(
        query=request.query,
        results=results,
    )