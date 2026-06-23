# Internal AI Customer Intelligence Agent

A FastAPI-based backend prototype for an internal AI assistant that supports customer intelligence, sales pipeline analysis, meeting summaries, keyword retrieval, semantic retrieval, and retrieval-supported business answers using mock CRM data, sales pipeline records, meeting transcripts, and internal policy documents.

## Project Goal

The goal of this project is to simulate an internal AI-powered business tool that helps sales, customer success, and business operations teams answer questions such as:

* Which customers are at risk?
* What should an account manager know before a customer call?
* What are the main risks in the sales pipeline?
* What happened in the latest customer meeting?
* Which internal policy recommendations apply to a customer or deal?
* Which internal documents are relevant to a business question?
* Which documents are semantically related to a business problem, even when the exact keywords differ?

The current version focuses on a clean FastAPI backend, structured data loading, deterministic business logic, keyword retrieval, semantic retrieval with embeddings, retrieval-supported answering, Docker configuration, GitHub Actions CI, and tested API endpoints.

Future extensions will add hybrid search, grounded LLM answer generation, agent tools, cloud deployment, and a basic MCP server for tool integration.

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
* Improved keyword retrieval with stopword filtering, frequency-based scoring, ranked results, and focused snippets
* Semantic retrieval using Sentence Transformers embeddings
* ChromaDB-based vector search over internal business documents
* Retrieval context used in the `/ask` endpoint
* Docker configuration for containerized execution
* GitHub Actions CI for automated test execution
* Tested business logic with pytest

## API Endpoints

| Method | Endpoint             | Description                                                                                 |
| ------ | -------------------- | ------------------------------------------------------------------------------------------- |
| GET    | `/health`            | Health check endpoint                                                                       |
| POST   | `/customer-brief`    | Generates a customer brief from mock CRM, pipeline, and transcript data                     |
| POST   | `/pipeline-insights` | Returns sales pipeline risk insights                                                        |
| POST   | `/meeting-summary`   | Summarizes customer meeting information                                                     |
| POST   | `/ask`               | Answers a business question using mock business data and retrieval context                  |
| POST   | `/search`            | Searches internal policies and meeting transcripts using keyword retrieval                  |
| POST   | `/semantic-search`   | Searches internal policies and meeting transcripts using embedding-based semantic retrieval |

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
      semantic_retrieval.py
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
  .github/
    workflows/
      ci.yml
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

## Example: Keyword Search Internal Documents

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
      "snippet": "The customer expressed concern about implementation delays and asked for a clearer onboarding plan."
    },
    {
      "source": "internal_policies/high_risk_deal_policy.md",
      "score": 2,
      "snippet": "- The customer has unresolved implementation or onboarding concerns."
    }
  ]
}
```

## Example: Semantic Search Internal Documents

Endpoint:

```http
POST /semantic-search
```

Request body:

```json
{
  "query": "customer is worried about onboarding and implementation timeline",
  "top_k": 3
}
```

Example response:

```json
{
  "query": "customer is worried about onboarding and implementation timeline",
  "results": [
    {
      "source": "meeting_transcripts/medcore_analytics_2026_06_12.txt",
      "score": 0.8123,
      "snippet": "Customer: MedCore Analytics Meeting date: 2026-06-12 Customer ID: C002 Account manager: Luca Bianchi..."
    },
    {
      "source": "internal_policies/high_risk_deal_policy.md",
      "score": 0.7345,
      "snippet": "# High-Risk Deal Policy A deal should be treated as high risk if one or more of the following conditions apply..."
    }
  ]
}
```

The exact score values may differ because they depend on embedding similarity calculations.

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

Expected result:

```text
16 passed
```

## Semantic Retrieval Note

The `/semantic-search` endpoint uses:

* `sentence-transformers/all-MiniLM-L6-v2` for local text embeddings
* ChromaDB as an in-memory vector database
* Embedding-based similarity search over meeting transcripts and internal policy documents

The first semantic search request may take longer because the embedding model may need to be downloaded and loaded locally.

The semantic retrieval layer currently uses an in-memory Chroma collection. This is suitable for a portfolio prototype and local development. A later version can persist the vector store to disk or connect to a managed vector database.

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

## Continuous Integration

The project includes a GitHub Actions CI workflow that runs automatically on push and pull request events.

The CI workflow:

* Checks out the repository
* Sets up Python 3.12
* Installs dependencies from `requirements.txt`
* Runs the pytest test suite

Workflow file:

```text
.github/workflows/ci.yml
```

The semantic search endpoint tests use mocking to keep CI fast and stable. This avoids downloading the embedding model during automated test execution.

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
* Keyword retrieval ranking
* Stopword filtering in search queries
* Semantic search response structure
* Semantic search response schema

## Tech Stack

* Python
* FastAPI
* Pydantic
* pytest
* CSV and text-based mock data
* Keyword retrieval
* Sentence Transformers
* ChromaDB
* Semantic search
* Docker
* GitHub Actions
* REST API design

## Current Architecture

The current backend follows a simple layered structure:

```text
API request
  -> FastAPI router
  -> Pydantic validation
  -> service layer
  -> data loader / retrieval layer
  -> structured API response
```

For keyword retrieval, the `/search` endpoint follows this workflow:

```text
business query
  -> tokenization
  -> stopword filtering
  -> keyword frequency scoring
  -> ranked document snippets
  -> structured search response
```

For semantic retrieval, the `/semantic-search` endpoint follows this workflow:

```text
business query
  -> query embedding
  -> ChromaDB vector search
  -> semantically similar internal documents
  -> structured semantic search response
```

For retrieval-supported answering, the `/ask` endpoint currently follows this workflow:

```text
business question
  -> keyword search over internal documents
  -> retrieved sources and snippets
  -> structured answer with supporting sources
```

This is an early retrieval-augmented workflow. The current `/ask` endpoint does not yet use an external LLM for answer generation.

## Roadmap

Planned next steps:

1. Add hybrid search combining keyword and semantic retrieval.
2. Update `/ask` to use hybrid retrieval context.
3. Add grounded LLM answer generation using retrieved context.
4. Add agent-style tools for customer briefs, pipeline insights, meeting summaries, and document search.
5. Deploy the backend to AWS or GCP.
6. Add a basic MCP server for tool integration.

## Portfolio Relevance

This project demonstrates practical backend and AI engineering skills relevant to internal AI tools, customer intelligence systems, RAG-based assistants, and sales pipeline analytics.

It is intended to show experience with:

* Building structured FastAPI services
* Designing business-focused API endpoints
* Working with structured and unstructured mock business data
* Implementing data loading and retrieval services
* Improving keyword retrieval with ranking and stopword filtering
* Adding semantic retrieval with embeddings and ChromaDB
* Adding retrieval context to answer generation
* Writing tested backend logic
* Adding Docker configuration
* Adding GitHub Actions CI
* Preparing a foundation for hybrid search, RAG, agent tools, and production deployment
