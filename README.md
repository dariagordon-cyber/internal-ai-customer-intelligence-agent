# Internal AI Customer Intelligence Agent

A FastAPI-based backend prototype for an internal AI assistant that supports customer intelligence, sales pipeline analysis, meeting summaries, keyword retrieval, semantic retrieval, hybrid search, grounded answer generation, and agent-style tool orchestration using mock CRM data, sales pipeline records, meeting transcripts, and internal policy documents.

## Project Goal

The goal of this project is to simulate an internal AI-powered business tool that helps sales, customer success, and business operations teams answer questions such as:

* Which customers are at risk?
* What should an account manager know before a customer call?
* What are the main risks in the sales pipeline?
* What happened in the latest customer meeting?
* Which internal policy recommendations apply to a customer or deal?
* Which internal documents are relevant to a business question?
* Which documents are semantically related to a business problem, even when the exact keywords differ?
* What grounded answer can be generated from retrieved internal business context?
* Which internal tool should be used for a given business question?

The current version focuses on a clean FastAPI backend, structured data loading, deterministic business logic, keyword retrieval, semantic retrieval with embeddings, hybrid search, retrieval-supported answering, optional LLM-grounded answer generation, agent-style tool selection, Docker configuration, GitHub Actions CI, and tested API endpoints.

Future extensions may add cloud deployment and a basic MCP server for tool integration.

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
* Hybrid search combining keyword retrieval and semantic retrieval
* Retrieval-supported `/ask` endpoint
* Grounded answer generation layer with optional OpenAI integration
* Fallback grounded answer generation when no `OPENAI_API_KEY` is available
* Agent-style tool orchestration through the `/agent` endpoint
* Deterministic tool selection for customer briefs, pipeline insights, meeting summaries, document search, and general business answering
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
| POST   | `/ask`               | Answers a business question using hybrid retrieval and grounded answer generation           |
| POST   | `/search`            | Searches internal policies and meeting transcripts using keyword retrieval                  |
| POST   | `/semantic-search`   | Searches internal policies and meeting transcripts using embedding-based semantic retrieval |
| POST   | `/hybrid-search`     | Combines keyword and semantic retrieval into a single ranked result list                    |
| POST   | `/agent`             | Selects and runs an internal business tool based on the user question                       |

## Project Structure

```text
internal-ai-customer-intelligence-agent/
  app/
    main.py
    schemas.py
    routers/
      business.py
    services/
      agent_tools.py
      data_loader.py
      mock_services.py
      retrieval.py
      semantic_retrieval.py
      hybrid_retrieval.py
      llm_service.py
  data/
    crm_customers.csv
    sales_pipeline.csv
    meeting_transcripts/
      medcore_analytics_2026_06_12.txt
    internal_policies/
      customer_brief_policy.md
      high_risk_deal_policy.md
  tests/
    test_agent_endpoint.py
    test_business_endpoints.py
    test_health.py
    test_hybrid_search_endpoint.py
    test_llm_service.py
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

## Example: Hybrid Search Internal Documents

Endpoint:

```http
POST /hybrid-search
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
      "hybrid_score": 0.8912,
      "keyword_score": 0.75,
      "semantic_score": 0.9676,
      "snippet": "The customer expressed concern about implementation delays."
    },
    {
      "source": "internal_policies/high_risk_deal_policy.md",
      "hybrid_score": 0.8123,
      "keyword_score": 0.6,
      "semantic_score": 0.9265,
      "snippet": "A deal should be treated as high risk if customer concerns are unresolved."
    }
  ]
}
```

The hybrid score combines normalized keyword relevance and semantic similarity.

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

Example response without an OpenAI API key:

```json
{
  "answer": "The current mock dataset contains 5 customers and 5 open deals. There are 1 high-risk deals. Relevant internal documents were found and used as supporting context. Based on the retrieved internal context, the main risk signals are connected to customer health, deal risk, implementation concerns, onboarding issues, or unresolved customer follow-up needs. Most relevant retrieved sources: meeting_transcripts/medcore_analytics_2026_06_12.txt, internal_policies/high_risk_deal_policy.md. Retrieved evidence summary: The customer expressed concern about implementation delays. A deal should be treated as high risk if customer concerns are unresolved.",
  "sources": [
    "crm_customers.csv",
    "sales_pipeline.csv",
    "meeting_transcripts/medcore_analytics_2026_06_12.txt",
    "internal_policies/high_risk_deal_policy.md"
  ],
  "confidence": "medium"
}
```

When `OPENAI_API_KEY` is available, the `/ask` endpoint can generate a grounded answer using the retrieved hybrid search context. Without an API key, the project still works using deterministic fallback answer generation.

## Example: Agent Tool Selection

Endpoint:

```http
POST /agent
```

Request body:

```json
{
  "question": "Give me a customer brief for this account",
  "customer_id": "C002"
}
```

Example response:

```json
{
  "question": "Give me a customer brief for this account",
  "selected_tool": "customer_brief",
  "tool_reason": "The question asks for customer-level account intelligence.",
  "answer": "MedCore Analytics: MedCore Analytics is a Healthcare customer in Germany, managed by Luca Bianchi. The current health score is 45. Open deal stages: Proposal. Main risks: Customer health score is below 50.; At least one open deal is marked as high risk.; Recent meeting notes mention implementation or onboarding concerns. Recommended actions: Review the latest customer interactions.; Prioritize follow-up if the health score or deal risk is concerning.; Prepare a concise account update before the next customer call.",
  "sources": [
    "crm_customers.csv",
    "sales_pipeline.csv",
    "medcore_analytics_2026_06_12.txt"
  ],
  "confidence": "high"
}
```

The `/agent` endpoint currently uses deterministic tool selection. It routes questions to one of the following internal tools:

* `customer_brief`
* `pipeline_insights`
* `meeting_summary`
* `document_search`
* `business_question_answer`

This provides a clear agent-style orchestration layer while keeping the portfolio project reproducible and easy to test.

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
25 passed
```

## Optional OpenAI Configuration

The project works without an OpenAI API key because it includes fallback grounded answer generation.

To enable LLM-generated grounded answers, set:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

Optional model override:

```bash
export OPENAI_MODEL="gpt-4o-mini"
```

Then run:

```bash
uvicorn app.main:app --reload
```

The `/ask` endpoint will use the retrieved hybrid search context and send it to the configured OpenAI model. If the API key is missing or the API call fails, the system falls back to deterministic grounded answer generation.

## Semantic Retrieval Note

The `/semantic-search` endpoint uses:

* `sentence-transformers/all-MiniLM-L6-v2` for local text embeddings
* ChromaDB as an in-memory vector database
* Embedding-based similarity search over meeting transcripts and internal policy documents

The first semantic search request may take longer because the embedding model may need to be downloaded and loaded locally.

The semantic retrieval layer currently uses an in-memory Chroma collection. This is suitable for a portfolio prototype and local development. A later version can persist the vector store to disk or connect to a managed vector database.

## Grounded Answer Generation Note

The `/ask` endpoint uses the following workflow:

```text
business question
  -> hybrid retrieval
  -> retrieved sources and snippets
  -> grounded answer generation
  -> answer with sources and confidence
```

The LLM service builds a retrieval context from hybrid search results. If `OPENAI_API_KEY` is available, it sends the question and retrieved context to the OpenAI API. If no API key is available, it returns a deterministic fallback grounded answer.

This design keeps the project usable in local development, CI, and portfolio review without requiring private credentials.

## Agent Tools Note

The `/agent` endpoint uses a simple agent-style orchestration pattern:

```text
business question
  -> tool selection
  -> selected internal tool
  -> structured answer
  -> sources and confidence
```

The current version includes five tools:

```text
customer_brief
pipeline_insights
meeting_summary
document_search
business_question_answer
```

This layer demonstrates how an internal AI assistant can route different business questions to specialized tools instead of treating all questions as generic chat prompts.

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

Semantic search, hybrid search, LLM-related tests, and agent endpoint tests use mocking where appropriate to keep CI fast and stable. This avoids downloading the embedding model or requiring an OpenAI API key during automated test execution.

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
* Hybrid search response structure
* Hybrid search response schema
* Retrieval context construction for grounded answer generation
* Fallback grounded answer generation without an API key
* Empty retrieval result handling in the LLM service
* Agent tool selection for customer briefs
* Agent tool selection for pipeline insights
* Agent tool selection for meeting summaries
* Agent behavior when required parameters are missing

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
* Hybrid search
* OpenAI API integration
* Grounded answer generation
* Agent-style tool orchestration
* Docker
* GitHub Actions
* REST API design

## Current Architecture

The current backend follows a layered structure:

```text
API request
  -> FastAPI router
  -> Pydantic validation
  -> service layer
  -> data loader / retrieval layer / LLM layer / agent tools layer
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

For hybrid search, the `/hybrid-search` endpoint follows this workflow:

```text
business query
  -> keyword retrieval
  -> semantic retrieval
  -> score normalization
  -> weighted hybrid scoring
  -> ranked hybrid results
```

For grounded answer generation, the `/ask` endpoint follows this workflow:

```text
business question
  -> hybrid search over internal documents
  -> retrieval context construction
  -> OpenAI grounded answer generation or fallback answer generation
  -> structured answer with sources and confidence
```

For agent-style tool orchestration, the `/agent` endpoint follows this workflow:

```text
business question
  -> deterministic tool selection
  -> specialized internal business tool
  -> structured answer with selected tool, reason, sources, and confidence
```

## Roadmap

Planned next steps:

1. Deploy the backend to AWS or GCP.
2. Add a basic MCP server for tool integration.
3. Optionally add persistent vector storage.
4. Optionally add a more advanced LLM-based agent planner.

## Portfolio Relevance

This project demonstrates practical backend and AI engineering skills relevant to internal AI tools, customer intelligence systems, RAG-based assistants, and sales pipeline analytics.

It is intended to show experience with:

* Building structured FastAPI services
* Designing business-focused API endpoints
* Working with structured and unstructured mock business data
* Implementing data loading and retrieval services
* Improving keyword retrieval with ranking and stopword filtering
* Adding semantic retrieval with embeddings and ChromaDB
* Combining keyword and semantic retrieval through hybrid search
* Building retrieval-supported answer generation
* Adding optional LLM-grounded answer generation with fallback behavior
* Adding agent-style tool routing for internal business workflows
* Writing tested backend logic
* Adding Docker configuration
* Adding GitHub Actions CI
* Preparing a foundation for deployment and MCP tool integration
