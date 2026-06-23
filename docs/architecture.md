# Architecture

This document describes the architecture of the Internal AI Customer Intelligence Agent.

## Purpose

The project is a FastAPI-based backend prototype for an internal AI assistant that supports customer intelligence, sales pipeline analysis, meeting summaries, retrieval over internal documents, grounded answer generation, and agent-style tool orchestration.

The system is designed as a portfolio-grade prototype that simulates how an internal business assistant could support sales, customer success, and operations teams using structured and unstructured business data.

## High-Level Architecture

The backend follows a layered architecture:

```
API request
  -> FastAPI router
  -> Pydantic validation
  -> service layer
  -> data loader / retrieval layer / LLM layer / agent tools layer
  -> structured API response
```

The main goal of this structure is to keep API routing, validation, business logic, retrieval logic, and answer generation separated.

## Main Components

### FastAPI Application

The FastAPI app is defined in `app/main.py`.

Responsibilities:

* Create the API application
* Register routers
* Expose the health check endpoint
* Provide Swagger documentation

### Router Layer

The main router is defined in `app/routers/business.py`.

Responsibilities:

* Define API endpoints
* Accept validated Pydantic request objects
* Call the relevant service functions
* Return structured Pydantic response objects

Current endpoints:

* `GET /health`
* `POST /customer-brief`
* `POST /pipeline-insights`
* `POST /meeting-summary`
* `POST /ask`
* `POST /search`
* `POST /semantic-search`
* `POST /hybrid-search`
* `POST /agent`

### Schema Layer

The schema layer is defined in `app/schemas.py`.

Responsibilities:

* Define request and response models
* Validate incoming API payloads
* Enforce structured API outputs
* Keep endpoint contracts explicit and testable

The project uses Pydantic models for all main endpoint inputs and outputs.

### Data Layer

The data loading logic is defined in `app/services/data_loader.py`.

Responsibilities:

* Load mock CRM customer data from CSV
* Load mock sales pipeline data from CSV
* Load meeting transcripts from text files
* Load internal policy documents from Markdown files
* Provide helper functions for customer-specific lookups

Data sources:

* `data/crm_customers.csv`
* `data/sales_pipeline.csv`
* `data/meeting_transcripts/`
* `data/internal_policies/`

### Business Logic Layer

The deterministic business logic is defined in `app/services/mock_services.py`.

Responsibilities:

* Generate customer briefs
* Generate pipeline insights
* Generate meeting summaries
* Build retrieval-supported business answers
* Combine mock structured data with retrieved context

This layer simulates business intelligence logic without requiring access to real CRM or sales systems.

### Keyword Retrieval Layer

Keyword retrieval is implemented in `app/services/retrieval.py`.

Responsibilities:

* Build a document collection from internal policies and meeting transcripts
* Tokenize text
* Filter common stopwords
* Score documents using keyword frequency
* Return ranked document snippets

This layer supports the `/search` endpoint.

### Semantic Retrieval Layer

Semantic retrieval is implemented in `app/services/semantic_retrieval.py`.

Responsibilities:

* Load a Sentence Transformers embedding model
* Convert internal documents and queries into embeddings
* Store document embeddings in ChromaDB
* Run embedding-based similarity search
* Return semantically similar internal documents

This layer supports the `/semantic-search` endpoint.

The current implementation uses an in-memory ChromaDB collection, which is suitable for local development and portfolio demonstration.

### Hybrid Retrieval Layer

Hybrid retrieval is implemented in `app/services/hybrid_retrieval.py`.

Responsibilities:

* Run keyword retrieval
* Run semantic retrieval
* Normalize keyword scores
* Combine keyword and semantic scores using weighted scoring
* Return a ranked list of hybrid search results

This layer supports the `/hybrid-search` endpoint and gives the project a more realistic retrieval architecture than keyword search alone.

### Grounded Answer Generation Layer

Grounded answer generation is implemented in `app/services/llm_service.py`.

Responsibilities:

* Build retrieval context from hybrid search results
* Generate grounded answers using the OpenAI API when `OPENAI_API_KEY` is available
* Provide deterministic fallback grounded answers when no API key is available
* Keep the system usable in local development, CI, and portfolio review without requiring private credentials

The `/ask` endpoint uses this layer after hybrid retrieval.

### Agent Tools Layer

Agent-style tool orchestration is implemented in `app/services/agent_tools.py`.

Responsibilities:

* Select the most appropriate internal tool based on the user question
* Route the request to one of several specialized tools
* Return the selected tool, selection reason, answer, sources, and confidence

Current tools:

* `customer_brief`
* `pipeline_insights`
* `meeting_summary`
* `document_search`
* `business_question_answer`

This is a deterministic agent-style layer. It demonstrates tool orchestration without relying on a non-deterministic autonomous agent planner.

## Request Flows

### Customer Brief Flow

```
POST /customer-brief
  -> validate CustomerBriefRequest
  -> load customer, deal, and transcript data
  -> generate customer summary, risks, and recommended actions
  -> return CustomerBriefResponse
```

### Keyword Search Flow

```
POST /search
  -> validate SearchRequest
  -> build internal document collection
  -> tokenize query and documents
  -> calculate keyword frequency scores
  -> return ranked SearchResponse
```

### Semantic Search Flow

```
POST /semantic-search
  -> validate SearchRequest
  -> embed query
  -> query ChromaDB collection
  -> return SemanticSearchResponse
```

### Hybrid Search Flow

```
POST /hybrid-search
  -> run keyword search
  -> run semantic search
  -> normalize keyword scores
  -> combine keyword and semantic scores
  -> return HybridSearchResponse
```

### Grounded Answer Flow

```
POST /ask
  -> validate AskRequest
  -> run hybrid search
  -> build retrieval context
  -> generate answer through OpenAI or fallback logic
  -> return AskResponse with sources and confidence
```

### Agent Flow

```
POST /agent
  -> validate AgentRequest
  -> select internal tool
  -> run selected tool
  -> return AgentResponse with selected tool, reason, sources, and confidence
```

## Design Decisions

### Mock Data Instead of Real CRM Data

The project uses mock CRM, sales pipeline, meeting, and policy data to avoid privacy risks and make the project fully reproducible.

### Deterministic Logic Where Possible

Business endpoints use deterministic logic so that tests remain stable and outputs are easy to inspect.

### Optional LLM Integration

The project supports OpenAI-based answer generation but does not require an API key. This avoids breaking local development and CI.

### Mocking in Tests

Tests mock semantic, hybrid, and LLM-dependent behavior where appropriate. This keeps CI fast and prevents automated tests from downloading embedding models or requiring private API credentials.

### In-Memory Vector Store

The semantic retrieval layer currently uses an in-memory ChromaDB collection. This is enough for a small portfolio prototype. A production version could persist the vector store or use a managed vector database.

## Current Limitations

* The data is mock data, not connected to a real CRM.
* The vector store is in-memory and rebuilt locally.
* The agent layer uses deterministic tool selection rather than an LLM planner.
* The project is not connected to authentication or user permissions.
* The project is not currently deployed to a cloud environment.
* The Dockerfile is configured for containerized execution, but local Docker testing depends on Docker Desktop availability.

## Possible Production Extensions

Possible future extensions include:

* Persistent vector storage
* Authentication and role-based access control
* Real CRM or data warehouse integration
* More robust document ingestion
* Cloud deployment
* Monitoring and logging
* LLM-based agent planning
* MCP server for standardized tool integration
