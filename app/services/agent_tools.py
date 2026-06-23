from app.schemas import (
    AgentRequest,
    AgentResponse,
    AskRequest,
    CustomerBriefRequest,
    MeetingSummaryRequest,
    PipelineInsightsRequest,
    SearchRequest,
)
from app.services.hybrid_retrieval import hybrid_search
from app.services.mock_services import (
    answer_business_question,
    build_customer_brief,
    build_meeting_summary,
    build_pipeline_insights,
)


def normalize_question(question: str) -> str:
    return question.lower().strip()


def select_agent_tool(question: str) -> tuple[str, str]:
    normalized_question = normalize_question(question)

    if any(
        keyword in normalized_question
        for keyword in ["brief", "account", "customer profile", "health score"]
    ):
        return (
            "customer_brief",
            "The question asks for customer-level account intelligence.",
        )

    if any(
        keyword in normalized_question
        for keyword in ["pipeline", "deal", "forecast", "revenue", "sales risk"]
    ):
        return (
            "pipeline_insights",
            "The question asks about sales pipeline or deal-level risk.",
        )

    if any(
        keyword in normalized_question
        for keyword in ["meeting", "call", "transcript", "summary"]
    ):
        return (
            "meeting_summary",
            "The question asks about meeting or transcript information.",
        )

    if any(
        keyword in normalized_question
        for keyword in ["document", "policy", "source", "evidence", "search"]
    ):
        return (
            "document_search",
            "The question asks for relevant internal documents or evidence.",
        )

    return (
        "business_question_answer",
        "The question is a general business question that requires retrieval-supported answering.",
    )


def run_customer_brief_tool(request: AgentRequest, reason: str) -> AgentResponse:
    if not request.customer_id:
        return AgentResponse(
            question=request.question,
            selected_tool="customer_brief",
            tool_reason=reason,
            answer=(
                "A customer brief requires a customer_id. "
                "Provide a customer_id such as C002."
            ),
            sources=[],
            confidence="low",
        )

    brief = build_customer_brief(
        CustomerBriefRequest(customer_id=request.customer_id)
    )

    return AgentResponse(
        question=request.question,
        selected_tool="customer_brief",
        tool_reason=reason,
        answer=(
            f"{brief.company_name}: {brief.summary} "
            f"Main risks: {'; '.join(brief.risks)} "
            f"Recommended actions: {'; '.join(brief.recommended_actions)}"
        ),
        sources=brief.sources,
        confidence="high",
    )


def run_pipeline_insights_tool(request: AgentRequest, reason: str) -> AgentResponse:
    insights = build_pipeline_insights(
        PipelineInsightsRequest(region=request.region)
    )

    high_risk_deals = [
        f"{deal.deal_id} for customer {deal.customer_id}: {deal.reason}"
        for deal in insights.high_risk_deals
    ]

    if not high_risk_deals:
        high_risk_summary = "No high-risk deals were found for the selected scope."
    else:
        high_risk_summary = "; ".join(high_risk_deals)

    return AgentResponse(
        question=request.question,
        selected_tool="pipeline_insights",
        tool_reason=reason,
        answer=(
            f"Total pipeline value: {insights.total_pipeline_value}. "
            f"High-risk deals: {high_risk_summary} "
            f"Main risks: {'; '.join(insights.main_risks)} "
            f"Recommendations: {'; '.join(insights.recommendations)}"
        ),
        sources=["crm_customers.csv", "sales_pipeline.csv"],
        confidence="high",
    )


def run_meeting_summary_tool(request: AgentRequest, reason: str) -> AgentResponse:
    if not request.customer_id:
        return AgentResponse(
            question=request.question,
            selected_tool="meeting_summary",
            tool_reason=reason,
            answer=(
                "A meeting summary requires a customer_id. "
                "Provide a customer_id such as C002."
            ),
            sources=[],
            confidence="low",
        )

    meeting_summary = build_meeting_summary(
        MeetingSummaryRequest(customer_id=request.customer_id)
    )

    return AgentResponse(
        question=request.question,
        selected_tool="meeting_summary",
        tool_reason=reason,
        answer=(
            f"{meeting_summary.summary} "
            f"Customer concerns: {'; '.join(meeting_summary.customer_concerns)} "
            f"Action items: {'; '.join(meeting_summary.action_items)} "
            f"Sentiment: {meeting_summary.sentiment}."
        ),
        sources=meeting_summary.sources,
        confidence="high",
    )


def run_document_search_tool(request: AgentRequest, reason: str) -> AgentResponse:
    search_response = hybrid_search(
        SearchRequest(query=request.question, top_k=3)
    )

    if not search_response.results:
        return AgentResponse(
            question=request.question,
            selected_tool="document_search",
            tool_reason=reason,
            answer="No relevant internal documents were found for this question.",
            sources=[],
            confidence="low",
        )

    evidence_summary = " ".join(
        result.snippet for result in search_response.results
    )

    return AgentResponse(
        question=request.question,
        selected_tool="document_search",
        tool_reason=reason,
        answer=(
            "The most relevant internal evidence was retrieved using hybrid search. "
            f"Evidence summary: {evidence_summary}"
        ),
        sources=[result.source for result in search_response.results],
        confidence="medium",
    )


def run_business_question_answer_tool(
    request: AgentRequest,
    reason: str,
) -> AgentResponse:
    answer = answer_business_question(
        AskRequest(
            question=request.question,
            customer_id=request.customer_id,
        )
    )

    return AgentResponse(
        question=request.question,
        selected_tool="business_question_answer",
        tool_reason=reason,
        answer=answer.answer,
        sources=answer.sources,
        confidence=answer.confidence,
    )


def run_agent(request: AgentRequest) -> AgentResponse:
    selected_tool, reason = select_agent_tool(request.question)

    if selected_tool == "customer_brief":
        return run_customer_brief_tool(request, reason)

    if selected_tool == "pipeline_insights":
        return run_pipeline_insights_tool(request, reason)

    if selected_tool == "meeting_summary":
        return run_meeting_summary_tool(request, reason)

    if selected_tool == "document_search":
        return run_document_search_tool(request, reason)

    return run_business_question_answer_tool(request, reason)