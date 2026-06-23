import os

from openai import OpenAI, OpenAIError

from app.schemas import HybridSearchResult


DEFAULT_MODEL = "gpt-4o-mini"


def build_retrieval_context(results: list[HybridSearchResult]) -> str:
    if not results:
        return "No relevant internal documents were retrieved."

    context_blocks = []

    for index, result in enumerate(results, start=1):
        context_blocks.append(
            "\n".join(
                [
                    f"[{index}] Source: {result.source}",
                    f"Hybrid score: {result.hybrid_score}",
                    f"Keyword score: {result.keyword_score}",
                    f"Semantic score: {result.semantic_score}",
                    f"Snippet: {result.snippet}",
                ]
            )
        )

    return "\n\n".join(context_blocks)


def build_fallback_grounded_answer(
    question: str,
    results: list[HybridSearchResult],
) -> str:
    if not results:
        return (
            "No directly relevant internal documents were retrieved for this question. "
            "The answer is based only on the available mock CRM and sales pipeline data."
        )

    top_sources = ", ".join(result.source for result in results[:3])
    top_snippets = " ".join(result.snippet for result in results[:3])

    return (
        "Based on the retrieved internal context, the main risk signals are connected "
        "to customer health, deal risk, implementation concerns, onboarding issues, "
        "or unresolved customer follow-up needs. "
        f"Most relevant retrieved sources: {top_sources}. "
        f"Retrieved evidence summary: {top_snippets}"
    )


def generate_grounded_answer(
    question: str,
    results: list[HybridSearchResult],
) -> tuple[str, str]:
    if not os.getenv("OPENAI_API_KEY"):
        return build_fallback_grounded_answer(question, results), "medium"

    client = OpenAI()
    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
    retrieval_context = build_retrieval_context(results)

    try:
        response = client.responses.create(
            model=model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are an internal business intelligence assistant. "
                        "Answer only using the provided retrieved context. "
                        "If the context is insufficient, say what is missing. "
                        "Be concise, practical, and business-oriented."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Business question:\n{question}\n\n"
                        f"Retrieved internal context:\n{retrieval_context}\n\n"
                        "Write a grounded answer for a sales or customer success team. "
                        "Mention the key risk signals and recommended next action."
                    ),
                },
            ],
            max_output_tokens=400,
        )

        answer = response.output_text.strip()

        if not answer:
            return build_fallback_grounded_answer(question, results), "medium"

        return answer, "high"

    except OpenAIError:
        return build_fallback_grounded_answer(question, results), "medium"