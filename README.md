# Internal AI Customer Intelligence Agent

A FastAPI-based backend prototype for an internal AI assistant that supports customer intelligence, sales pipeline analysis, meeting summaries, keyword retrieval, and retrieval-supported business answers using mock CRM data, sales pipeline records, meeting transcripts, and internal policy documents.

## Project Goal

The goal of this project is to simulate an internal AI-powered business tool that helps sales and customer success teams answer questions such as:

* Which customers are at risk?
* What should an account manager know before a customer call?
* What are the main risks in the sales pipeline?
* What happened in the latest customer meeting?
* Which internal policy recommendations apply to a customer or deal?
* Which internal documents are relevant to a business question?

The current version focuses on a clean FastAPI backend, structured data loading, deterministic business logic, keyword retrieval, retrieval-supported answering, Docker configuration, and tested API endpoints.

Future extensions will add semantic retrieval, vector databases, hybrid search, grounded LLM answer generation, agent tools, CI/CD, and cloud deployment.

## Current Features

* FastAPI backend with Swagger documentation
* Pydantic request and response schemas
* Business intelligence API endpoints
* Mock CRM customer data
* Mock sales pipeline data
* Mock meeting transcript
* Mock internal policy documents
* Data loader service for CSV and text files
* Keyword retrieval over meeting transcripts and internal policy documents
* Keyword retrieval context used in the `/ask` endpoint
* Docker configuration for containerized execution
* Tested business logic with pytest

## API Endpoints

| Method | Endpoint             | Description                                                                |
| ------ | -------------------- | -------------------------------------------------------------------------- |
| GET    | `/health`            | Health check endpoint                                                      |
| POST   | `/customer-brief`    | Generates a customer brief from mock CRM, pipeline, and transcript data    |
| POST   | `/pipeline-insights` | Returns sales pipeline risk insights                                       |
| POST   | `/meeting-summary`   | Summarizes customer meeting information                                    |
| POST   | `/ask`               | Answers a business question using mock business data and retrieval context |
| POST   | `/search`            | Searches internal policies and meeting transcripts using keyword retrieval |

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
      retrieval.py
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
  .dockerignore
  Dockerfile
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

## Example: Search Internal Documents

Endpoint:

```http
POST /search
```

Request body:

```json
{
  "query": "implementation delays onboarding",
  "top_k": 3
}
```

Example response:

```json
{
  "query": "implementation delays onboarding",
  "results": [
    {
      "source": "meeting_transcripts/medcore_analytics_2026_06_12.txt",
      "score": 3,
      "snippet": "Customer: MedCore Analytics\nCustomer ID: C002\nDate: 2026-06-12\nParticipants: Luca Bianchi, MedCore Operations Lead, MedCore IT Manager\n\nThe customer expressed concern about implementation delays and asked for a clearer onboarding plan."
    },
    {
      "source": "internal_policies/high_risk_deal_policy.md",
      "score": 2,
      "snippet": "- The customer has unresolved implementation or onboarding concerns."
    }
  ]
}
```

## Example: Ask a Retrieval-Supported Business Question

Endpoint:

```http
POST /ask
```

Request body:

```json
{
  "question": "Which customers have implementation or onboarding risks?"
}
```

Example response:

```json
{
  "answer": "The current mock dataset contains 5 customers and 5 open deals. There are 1 high-risk deals. Relevant internal documents were found and used as supporting context. The strongest risk signal is a combination of low customer health, low deal probability, and unresolved implementation or onboarding concerns. The recommended next step is to prioritize high-risk accounts and schedule a follow-up with the customer within five business days.",
  "sources": [
    "crm_customers.csv",
    "sales_pipeline.csv",
    "meeting_transcripts/medcore_analytics_2026_06_12.txt",
    "internal_policies/high_risk_deal_policy.md"
  ],
  "confidence": "medium"
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

## Docker

The project includes Docker configuration for containerized execution.

Build the Docker image:

```bash
docker build -t internal-ai-customer-intelligence-agent .
```

Run the container:

```bash
docker run -p 8000:8000 internal-ai-customer-intelligence-agent
```

Then open:

```text
http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

Note: Docker Desktop must be installed and running before using these commands.

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
* Keyword search over internal documents
* `top_k` behavior in `/search`
* Retrieval-supported answer generation in `/ask`

## Tech Stack

* Python
* FastAPI
* Pydantic
* pytest
* CSV and text-based mock data
* Keyword retrieval
* Docker
* REST API design

## Current Architecture

The current backend follows a simple layered structure:

```text
API request
  -> FastAPI router
  -> Pydantic validation
  -> service layer
  -> data loader / keyword retrieval
  -> structured API response
```

For retrieval-supported answering, the `/ask` endpoint follows this workflow:

```text
business question
  -> keyword search over internal documents
  -> retrieved sources and snippets
  -> structured answer with supporting sources
```

This is an early retrieval-augmented workflow. It does not yet use embeddings or an external LLM.

## Roadmap

Planned next steps:

1. Improve keyword retrieval scoring and snippets.
2. Add semantic retrieval using embeddings and a vector database.
3. Implement hybrid search combining keyword and semantic retrieval.
4. Add grounded LLM answer generation.
5. Add agent-style tools for customer briefs, pipeline insights, meeting summaries, and document search.
6. Add GitHub Actions CI.
7. Deploy the backend to AWS or GCP.
8. Add a basic MCP server for tool integration.

## Portfolio Relevance

This project demonstrates practical backend and AI engineering skills relevant to internal AI tools, customer intelligence systems, RAG-based assistants, and sales pipeline analytics.

It is intended to show experience with:

* Building structured FastAPI services
* Designing business-focused API endpoints
* Working with structured and unstructured mock business data
* Implementing data loading and retrieval services
* Adding retrieval context to answer generation
* Writing tested backend logic
* Preparing a foundation for RAG, agent tools, Docker, CI/CD, and production deployment
