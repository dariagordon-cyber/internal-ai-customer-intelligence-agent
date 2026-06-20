from fastapi import APIRouter

from app.schemas import (
    AskRequest,
    AskResponse,
    CustomerBriefRequest,
    CustomerBriefResponse,
    MeetingSummaryRequest,
    MeetingSummaryResponse,
    PipelineInsightsRequest,
    PipelineInsightsResponse,
)
from app.services.mock_services import (
    answer_business_question,
    build_customer_brief,
    build_meeting_summary,
    build_pipeline_insights,
)

router = APIRouter(tags=["Business Intelligence"])


@router.post("/customer-brief", response_model=CustomerBriefResponse)
def create_customer_brief(request: CustomerBriefRequest) -> CustomerBriefResponse:
    return build_customer_brief(request)


@router.post("/pipeline-insights", response_model=PipelineInsightsResponse)
def create_pipeline_insights(
    request: PipelineInsightsRequest,
) -> PipelineInsightsResponse:
    return build_pipeline_insights(request)


@router.post("/meeting-summary", response_model=MeetingSummaryResponse)
def create_meeting_summary(
    request: MeetingSummaryRequest,
) -> MeetingSummaryResponse:
    return build_meeting_summary(request)


@router.post("/ask", response_model=AskResponse)
def ask_business_question(request: AskRequest) -> AskResponse:
    return answer_business_question(request)