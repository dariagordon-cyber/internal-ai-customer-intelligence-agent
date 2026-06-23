# Deployment Readiness

This document describes the deployment readiness status of the Internal AI Customer Intelligence Agent.

The project is not currently deployed to a live cloud environment. This is intentional: the current version is prepared as a no-billing portfolio project and avoids requiring an active cloud billing account.

## Current Deployment Status

Current status:

* Local FastAPI execution is supported.
* Docker configuration is included.
* GitHub Actions CI is configured.
* Automated tests pass locally.
* The project is pushed to GitHub.
* No live cloud deployment is currently active.

The project can be run locally with:

```
uvicorn app.main:app --reload
```

The local API documentation is available at:

```
http://127.0.0.1:8000/docs
```

The health check endpoint is available at:

```
http://127.0.0.1:8000/health
```

## Local Execution Readiness

The project supports local execution through a Python virtual environment.

Expected setup flow:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Validation command:

```
pytest
```

Expected result:

```
25 passed
```

## Docker Readiness

The project includes:

* `Dockerfile`
* `.dockerignore`

The Dockerfile defines a containerized FastAPI application using Python 3.12.

Expected Docker build command:

```
docker build -t internal-ai-customer-intelligence-agent .
```

Expected Docker run command:

```
docker run -p 8000:8000 internal-ai-customer-intelligence-agent
```

Expected health check:

```
http://127.0.0.1:8000/health
```

Important note: Docker Desktop must be installed and running before these commands can be tested locally.

## CI Readiness

The project includes a GitHub Actions workflow at:

```
.github/workflows/ci.yml
```

The CI workflow:

* Checks out the repository
* Sets up Python
* Installs project dependencies
* Runs the pytest suite

This confirms that the project can be tested automatically on push and pull request events.

## Environment Variables

The project works without private credentials.

Optional environment variables:

* `OPENAI_API_KEY`
* `OPENAI_MODEL`

If `OPENAI_API_KEY` is not set, the system uses deterministic fallback grounded answer generation.

This design allows:

* Local development without secrets
* CI execution without secrets
* Portfolio review without private API keys

## Cloud Deployment Readiness

The project is structurally ready for cloud deployment because it includes:

* A FastAPI backend
* A Dockerfile
* A health endpoint
* Automated tests
* Clear dependency management
* GitHub version control
* CI validation

A future cloud deployment could use:

* Google Cloud Run
* Azure App Service
* AWS App Runner
* AWS ECS Fargate
* Render
* Railway
* Fly.io

## Google Cloud Run Considerations

For Google Cloud Run, the project would need:

* A Google Cloud project
* Billing enabled
* Cloud Run API enabled
* Cloud Build API enabled
* A container image or source-based deployment
* Public or authenticated service access configuration

Because Cloud Run typically requires a billing account, this project currently avoids live deployment.

A future Cloud Run deployment could use a command similar to:

```
gcloud run deploy internal-ai-customer-intelligence-agent --source . --region europe-west1 --allow-unauthenticated
```

This command is provided only as a deployment reference. It has not been executed for the current no-billing version.

## Production Readiness Gaps

The current project is a portfolio prototype, not a production system.

Main gaps before production use:

* Authentication and authorization
* Secrets management
* Persistent vector store
* Real data connectors
* Observability and logging
* Rate limiting
* Input/output safety checks
* Data privacy review
* Cloud deployment configuration
* Monitoring and alerting
* Error tracking
* Cost controls for LLM usage

