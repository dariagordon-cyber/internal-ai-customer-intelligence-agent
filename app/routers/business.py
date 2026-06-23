from fastapi import APIRouter

from app.schemas import (
    AskRequest,
    AskResponse,
    CustomerBriefRequest,
    CustomerBriefResponse,
    HybridSearchResponse,
    MeetingSummaryRequest,
    MeetingSummaryResponse,
    PipelineInsightsRequest,
    PipelineInsightsResponse,
    SearchRequest,
    SearchResponse,
    SemanticSearchResponse,
)
from app.services.hybrid_retrieval import hybrid_search
from app.services.mock_services import (
    answer_business_question,
    build_customer_brief,
    build_meeting_summary,
    build_pipeline_insights,
)
from app.services.retrieval import keyword_search
from app.services.semantic_retrieval import semantic_search

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


@router.post("/search", response_model=SearchResponse)
def search_internal_documents(request: SearchRequest) -> SearchResponse:
    return keyword_search(request)


@router.post("/semantic-search", response_model=SemanticSearchResponse)
def search_internal_documents_semantically(
    request: SearchRequest,
) -> SemanticSearchResponse:
    return semantic_search(request)


@router.post("/hybrid-search", response_model=HybridSearchResponse)
def search_internal_documents_with_hybrid_retrieval(
    request: SearchRequest,
) -> HybridSearchResponse:
    return hybrid_search(request)