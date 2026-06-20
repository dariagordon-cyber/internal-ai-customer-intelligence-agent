# Internal AI Customer Intelligence Agent

A FastAPI-based backend prototype for an internal AI assistant that supports customer intelligence, sales pipeline analysis, meeting summaries, and business decision support using mock CRM data, sales pipeline records, meeting transcripts, and internal policy documents.

## Project Goal

The goal of this project is to simulate an internal AI-powered business tool that helps sales and customer success teams answer questions such as:

* Which customers are at risk?
* What should an account manager know before a customer call?
* What are the main risks in the sales pipeline?
* What happened in the latest customer meeting?
* Which internal policy recommendations apply to a customer or deal?

The current version focuses on a clean FastAPI backend, structured data loading, deterministic business logic, and tested API endpoints. Future extensions will add retrieval-augmented generation, hybrid search, agent tools, Docker, CI/CD, and cloud deployment.

## Current Features

* FastAPI backend with Swagger documentation
* Pydantic request and response schemas
* Business intelligence API endpoints
* Mock CRM customer data
* Mock sales pipeline data
* Mock meeting transcript
* Mock internal policy documents
* Data loader service for CSV and text files
* Tested business logic with pytest

## API Endpoints

| Method | Endpoint             | Description                                                             |
| ------ | -------------------- | ----------------------------------------------------------------------- |
| GET    | `/health`            | Health check endpoint                                                   |
| POST   | `/customer-brief`    | Generates a customer brief from mock CRM, pipeline, and transcript data |
| POST   | `/pipeline-insights` | Returns sales pipeline risk insights                                    |
| POST   | `/meeting-summary`   | Summarizes customer meeting information                                 |
| POST   | `/ask`               | Answers a business question using mock customer and policy data         |

## Project Structure

```text
internal-ai-customer-intelligence-agent/
  app/
    main.py
    schemas.py
    routers/
      business.py
    services/
      data_loader.py
      mock_services.py
  data/
    crm_customers.csv
    sales_pipeline.csv
    meeting_transcripts/
      medcore_analytics_2026_06_12.txt
    internal_policies/
      customer_brief_policy.md
      high_risk_deal_policy.md
  tests/
    test_health.py
    test_business_endpoints.py
  requirements.txt
  pyproject.toml
  README.md
```

## Example: Generate a Customer Brief

Endpoint:

```http
POST /customer-brief
```

Request body:

```json
{
  "customer_id": "C002"
}
```

Example response:

```json
{
  "customer_id": "C002",
  "company_name": "MedCore Analytics",
  "summary": "MedCore Analytics is a Healthcare customer in Germany, managed by Luca Bianchi. The current health score is 45. Open deal stages: Proposal.",
  "risks": [
    "Customer health score is below 50.",
    "At least one open deal is marked as high risk.",
    "Recent meeting notes mention implementation or onboarding concerns."
  ],
  "recommended_actions": [
    "Review the latest customer interactions.",
    "Prioritize follow-up if the health score or deal risk is concerning.",
    "Prepare a concise account update before the next customer call."
  ],
  "sources": [
    "crm_customers.csv",
    "sales_pipeline.csv",
    "medcore_analytics_2026_06_12.txt"
  ]
}
```

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Run tests:

```bash
pytest
```

## Current Test Coverage

The test suite checks:

* Health endpoint behavior
* Customer brief response structure
* Customer brief data loaded from mock CRM and pipeline files
* Handling of unknown customer IDs
* Region-based pipeline filtering
* Meeting summary response structure
* Meeting transcript source usage
* Business question response structure
* Dataset summary usage in `/ask`

## Tech Stack

* Python
* FastAPI
* Pydantic
* pytest
* CSV and text-based mock data
* REST API design

## Roadmap

Planned next steps:

1. Add a simple keyword retrieval layer over internal policies and meeting transcripts.
2. Add semantic retrieval using embeddings and a vector database.
3. Implement hybrid search combining keyword and semantic retrieval.
4. Add grounded LLM answer generation.
5. Add agent-style tools for customer briefs, pipeline insights, and meeting summaries.
6. Add Docker support.
7. Add GitHub Actions CI.
8. Deploy the backend to AWS or GCP.
9. Add a basic MCP server for tool integration.

## Portfolio Relevance

This project demonstrates practical backend and AI engineering skills relevant to internal AI tools, customer intelligence systems, RAG-based assistants, and sales pipeline analytics.

It is intended to show experience with:

* Building structured FastAPI services
* Designing business-focused API endpoints
* Working with structured and unstructured mock business data
* Implementing testable backend logic
* Preparing a foundation for RAG, agent tools, and production deployment
