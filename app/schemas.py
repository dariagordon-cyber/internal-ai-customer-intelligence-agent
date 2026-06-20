from typing import Literal

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: Literal["ok"]


class CustomerBriefRequest(BaseModel):
    customer_id: str = Field(..., min_length=1)


class CustomerBriefResponse(BaseModel):
    customer_id: str
    company_name: str
    summary: str
    risks: list[str]
    recommended_actions: list[str]
    sources: list[str]


class PipelineInsightsRequest(BaseModel):
    region: str | None = None


class DealRisk(BaseModel):
    deal_id: str
    customer_id: str
    risk_level: Literal["low", "medium", "high"]
    reason: str


class PipelineInsightsResponse(BaseModel):
    total_pipeline_value: float = Field(..., ge=0)
    high_risk_deals: list[DealRisk]
    main_risks: list[str]
    recommendations: list[str]


class MeetingSummaryRequest(BaseModel):
    customer_id: str = Field(..., min_length=1)


class MeetingSummaryResponse(BaseModel):
    customer_id: str
    summary: str
    customer_concerns: list[str]
    action_items: list[str]
    sentiment: Literal["positive", "neutral", "concerned", "negative"]
    sources: list[str]


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1)
    customer_id: str | None = None


class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: Literal["low", "medium", "high"]