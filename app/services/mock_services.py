from app.schemas import (
    AskRequest,
    AskResponse,
    CustomerBriefRequest,
    CustomerBriefResponse,
    DealRisk,
    MeetingSummaryRequest,
    MeetingSummaryResponse,
    PipelineInsightsRequest,
    PipelineInsightsResponse,
    SearchRequest,
)
from app.services.data_loader import (
    find_customer_by_id,
    find_deals_by_customer_id,
    find_meeting_transcripts_by_customer_id,
    load_customers,
    load_sales_pipeline,
)
from app.services.retrieval import keyword_search


def build_customer_brief(request: CustomerBriefRequest) -> CustomerBriefResponse:
    customer = find_customer_by_id(request.customer_id)

    if customer is None:
        return CustomerBriefResponse(
            customer_id=request.customer_id,
            company_name="Unknown customer",
            summary="No customer record was found for the requested customer ID.",
            risks=["Customer data is missing."],
            recommended_actions=["Verify the customer ID and CRM data source."],
            sources=["crm_customers.csv"],
        )

    deals = find_deals_by_customer_id(request.customer_id)
    transcripts = find_meeting_transcripts_by_customer_id(request.customer_id)

    deal_stages = [deal["stage"] for deal in deals]
    risk_levels = [deal["risk_level"] for deal in deals]

    risks = []

    if int(customer["health_score"]) < 50:
        risks.append("Customer health score is below 50.")

    if "high" in risk_levels:
        risks.append("At least one open deal is marked as high risk.")

    if transcripts:
        risks.append("Recent meeting notes mention implementation or onboarding concerns.")

    if not risks:
        risks.append("No major risk signals were found in the current mock data.")

    return CustomerBriefResponse(
        customer_id=customer["customer_id"],
        company_name=customer["company_name"],
        summary=(
            f"{customer['company_name']} is a {customer['industry']} customer in "
            f"{customer['region']}, managed by {customer['account_manager']}. "
            f"The current health score is {customer['health_score']}. "
            f"Open deal stages: {', '.join(deal_stages) if deal_stages else 'none'}."
        ),
        risks=risks,
        recommended_actions=[
            "Review the latest customer interactions.",
            "Prioritize follow-up if the health score or deal risk is concerning.",
            "Prepare a concise account update before the next customer call.",
        ],
        sources=[
            "crm_customers.csv",
            "sales_pipeline.csv",
            *list(transcripts.keys()),
        ],
    )


def build_pipeline_insights(
    request: PipelineInsightsRequest,
) -> PipelineInsightsResponse:
    customers = load_customers()
    deals = load_sales_pipeline()

    customer_by_id = {
        customer["customer_id"]: customer
        for customer in customers
    }

    if request.region:
        deals = [
            deal
            for deal in deals
            if customer_by_id.get(deal["customer_id"], {}).get("region") == request.region
        ]

    total_pipeline_value = sum(float(deal["value"]) for deal in deals)

    high_risk_deals = [
        DealRisk(
            deal_id=deal["deal_id"],
            customer_id=deal["customer_id"],
            risk_level=deal["risk_level"],  # type: ignore[arg-type]
            reason=(
                f"Deal is in {deal['stage']} stage with probability "
                f"{deal['probability']} and risk level {deal['risk_level']}."
            ),
        )
        for deal in deals
        if deal["risk_level"] == "high"
    ]

    main_risks = [
        "Low deal probability may reduce forecast reliability.",
        "High-risk deals require proactive account management.",
        "Deals close to expected close date should be reviewed.",
    ]

    if request.region:
        main_risks.append(f"Insights are filtered for region: {request.region}.")

    return PipelineInsightsResponse(
        total_pipeline_value=total_pipeline_value,
        high_risk_deals=high_risk_deals,
        main_risks=main_risks,
        recommendations=[
            "Prioritize high-risk deals for immediate follow-up.",
            "Review customer health scores before pipeline meetings.",
            "Update the expected close dates after account manager review.",
        ],
    )


def build_meeting_summary(
    request: MeetingSummaryRequest,
) -> MeetingSummaryResponse:
    transcripts = find_meeting_transcripts_by_customer_id(request.customer_id)

    if not transcripts:
        return MeetingSummaryResponse(
            customer_id=request.customer_id,
            summary="No meeting transcript was found for the requested customer ID.",
            customer_concerns=["Meeting data is missing."],
            action_items=["Verify whether a transcript exists for this customer."],
            sentiment="neutral",
            sources=[],
        )

    transcript_names = list(transcripts.keys())

    return MeetingSummaryResponse(
        customer_id=request.customer_id,
        summary=(
            "The customer expressed concern about implementation delays, "
            "requested clearer onboarding support, and asked for a revised timeline."
        ),
        customer_concerns=[
            "Implementation timeline is unclear.",
            "Integration documentation is missing.",
            "The customer wants more proactive communication.",
        ],
        action_items=[
            "Send revised implementation timeline.",
            "Share integration documentation.",
            "Schedule onboarding follow-up.",
            "Prepare risk update for the account manager.",
        ],
        sentiment="concerned",
        sources=transcript_names,
    )


def answer_business_question(request: AskRequest) -> AskResponse:
    customers = load_customers()
    deals = load_sales_pipeline()

    high_risk_deals = [
        deal for deal in deals if deal["risk_level"] == "high"
    ]

    search_response = keyword_search(
        SearchRequest(query=request.question, top_k=3)
    )

    retrieved_sources = [
        result.source for result in search_response.results
    ]

    if search_response.results:
        retrieval_summary = (
            "Relevant internal documents were found and used as supporting context."
        )
    else:
        retrieval_summary = (
            "No directly relevant internal documents were found for this question."
        )

    answer = (
        f"The current mock dataset contains {len(customers)} customers and "
        f"{len(deals)} open deals. There are {len(high_risk_deals)} high-risk deals. "
        f"{retrieval_summary} "
        "The strongest risk signal is a combination of low customer health, "
        "low deal probability, and unresolved implementation or onboarding concerns. "
        "The recommended next step is to prioritize high-risk accounts and schedule "
        "a follow-up with the customer within five business days."
    )

    return AskResponse(
        answer=answer,
        sources=[
            "crm_customers.csv",
            "sales_pipeline.csv",
            *retrieved_sources,
        ],
        confidence="medium",
    )