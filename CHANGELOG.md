# Changelog

All notable changes to the Internal AI Customer Intelligence Agent project are documented in this file.

## Unreleased

### Planned

* Optional cloud deployment
* Optional MCP server for tool integration
* Optional persistent vector storage
* Optional advanced LLM-based agent planning

## 0.7.0 - Agent Tools Layer

### Added

* Added `/agent` endpoint.
* Added `AgentRequest` and `AgentResponse` schemas.
* Added deterministic agent-style tool selection.
* Added agent tools for:

  * customer briefs
  * pipeline insights
  * meeting summaries
  * document search
  * general business question answering
* Added tests for agent tool selection.
* Updated README with agent endpoint documentation.

### Changed

* Extended the API from retrieval-supported answering to agent-style tool orchestration.

## 0.6.0 - Grounded Answer Generation

### Added

* Added OpenAI Python SDK dependency.
* Added `llm_service.py`.
* Added retrieval context construction from hybrid search results.
* Added optional OpenAI-based grounded answer generation.
* Added deterministic fallback grounded answer generation when no `OPENAI_API_KEY` is available.
* Updated `/ask` to use hybrid retrieval and grounded answer generation.
* Added tests for the LLM service and fallback behavior.
* Updated README with grounded answer generation documentation.

### Changed

* `/ask` now uses hybrid retrieval context instead of only keyword retrieval context.

## 0.5.0 - Hybrid Search

### Added

* Added `/hybrid-search` endpoint.
* Added `hybrid_retrieval.py`.
* Added `HybridSearchResult` and `HybridSearchResponse` schemas.
* Added hybrid scoring that combines normalized keyword scores and semantic similarity scores.
* Added tests for hybrid search response structure and schema.

### Changed

* Retrieval architecture now supports both keyword and semantic retrieval.

## 0.4.0 - Semantic Retrieval

### Added

* Added ChromaDB dependency.
* Added Sentence Transformers dependency.
* Added `/semantic-search` endpoint.
* Added `semantic_retrieval.py`.
* Added embedding-based document retrieval over meeting transcripts and internal policy documents.
* Added semantic search response schemas.
* Added tests for semantic search endpoint behavior.
* Updated README with semantic retrieval documentation.

### Changed

* Project expanded from keyword retrieval to vector-based semantic retrieval.

## 0.3.0 - Improved Keyword Retrieval

### Added

* Added improved keyword scoring.
* Added stopword filtering.
* Added frequency-based scoring.
* Added focused snippet selection.
* Added tests for ranking and stopword handling.
* Updated README with keyword retrieval documentation.

### Changed

* `/search` became more relevant and stable for internal document search.

## 0.2.0 - Business Endpoints and Retrieval-Supported Asking

### Added

* Added mock CRM customer data.
* Added mock sales pipeline data.
* Added mock meeting transcript.
* Added mock internal policy documents.
* Added data loader service.
* Added `/customer-brief` endpoint.
* Added `/pipeline-insights` endpoint.
* Added `/meeting-summary` endpoint.
* Added `/search` endpoint.
* Added retrieval-supported `/ask` endpoint.
* Added tests for business endpoints.
* Added Dockerfile.
* Added `.dockerignore`.
* Added GitHub Actions CI workflow.

### Changed

* Project moved from a basic FastAPI skeleton to a business-focused AI backend prototype.

## 0.1.0 - Initial FastAPI Project

### Added

* Initialized FastAPI project structure.
* Added `/health` endpoint.
* Added Pydantic schema for health check.
* Added pytest setup.
* Added initial README.
* Added basic project dependencies.
