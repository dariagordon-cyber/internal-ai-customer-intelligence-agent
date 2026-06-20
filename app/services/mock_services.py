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
)


def build_customer_brief(request: CustomerBriefRequest) -> CustomerBriefResponse:
    return CustomerBriefResponse(
        customer_id=request.customer_id,
        company_name="MedCore Analytics",
        summary=(
            "MedCore Analytics is a healthcare analytics customer with active "
            "implementation concerns and a medium-to-high renewal risk."
        ),
        risks=[
            "Customer mentioned implementation delays.",
            "Recent engagement level is lower than expected.",
            "The deal is still in proposal stage close to the expected close date.",
        ],
        recommended_actions=[
            "Schedule a follow-up within five business days.",
            "Send a clear onboarding and implementation plan.",
            "Ask the account manager to confirm technical blockers.",
        ],
        sources=[
            "mock_crm_customers.csv",
            "mock_sales_pipeline.csv",
            "meeting_transcript_medcore.txt",
        ],
    )


def build_pipeline_insights(
    request: PipelineInsightsRequest,
) -> PipelineInsightsResponse:
    region_label = request.region or "all regions"

    return PipelineInsightsResponse(
        total_pipeline_value=125000.0,
        high_risk_deals=[
            DealRisk(
                deal_id="D002",
                customer_id="C002",
                risk_level="high",
                reason=(
                    f"Deal in {region_label} has low probability and delayed "
                    "implementation concerns."
                ),
            )
        ],
        main_risks=[
            "Several opportunities are close to the expected close date.",
            "Some customers have unresolved onboarding concerns.",
            "Low recent engagement may reduce conversion probability.",
        ],
        recommendations=[
            "Prioritize high-risk accounts for follow-up.",
            "Review implementation blockers with customer success.",
            "Prepare executive summary for deals above 50,000 EUR.",
        ],
    )


def build_meeting_summary(
    request: MeetingSummaryRequest,
) -> MeetingSummaryResponse:
    return MeetingSummaryResponse(
        customer_id=request.customer_id,
        summary=(
            "The customer expressed concern about implementation delays, "
            "requested clearer onboarding support, and asked for a revised timeline."
        ),
        customer_concerns=[
            "Implementation timeline is unclear.",
            "Onboarding support may not be sufficient.",
            "The customer wants more proactive communication.",
        ],
        action_items=[
            "Send revised implementation timeline.",
            "Schedule onboarding check-in.",
            "Prepare risk update for the account manager.",
        ],
        sentiment="concerned",
        sources=["meeting_transcript_medcore.txt"],
    )


def answer_business_question(request: AskRequest) -> AskResponse:
    return AskResponse(
        answer=(
            "Based on the mock CRM, pipeline, and meeting data, the most urgent "
            "customer risk is related to delayed implementation and low recent engagement. "
            "The recommended next step is to schedule a follow-up and provide a clearer "
            "onboarding plan."
        ),
        sources=[
            "mock_crm_customers.csv",
            "mock_sales_pipeline.csv",
            "meeting_transcript_medcore.txt",
        ],
        confidence="medium",
    )