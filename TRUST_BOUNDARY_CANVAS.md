# Trust Boundary Canvas for GenAI Project

## Overview

This canvas places every capability in exactly one zone:
- **Inside Trust Zone**: Project-owned code and data executed fully inside the environment.
- **Trust Boundary Zone**: Interfaces and controls where trust must be explicitly managed.
- **Outside Trust Zone**: External services, APIs, and third-party providers.

---

## Trust Zones

### 1. Inside Trust Zone
These capabilities are fully controlled by the project and executed locally or within the trusted environment.

- `rag_model/data_generator.py`
  - Purpose: generate synthetic travel dataset
  - Trust reason: project-owned data creation

- `rag_model/json_to_text.py`
  - Purpose: convert travel JSON into human-readable text
  - Trust reason: internal data transformation

- `rag_model/chunking.py`
  - Purpose: segment text into retrieval-friendly chunks
  - Trust reason: internal semantic processing

- `rag_model/embedding_generator.py`
  - Purpose: orchestrate embedding generation requests
  - Trust reason: project-controlled embedding workflow

- `rag_model/vector_search.py`
  - Purpose: perform semantic search and build LLM prompts
  - Trust reason: internal retrieval and context assembly logic

- `ticket_triage/ticket_generator.py`
  - Purpose: create synthetic support tickets
  - Trust reason: local test data generation

- `ticket_triage/escalation_service.py`
  - Purpose: business rule routing and team assignment
  - Trust reason: deterministic, owned decision logic

- `ticket_triage/analytics_service.py`
  - Purpose: calculate quality metrics and drift
  - Trust reason: internal KPI and monitoring logic

- `ticket_triage/feedback_service.py`
  - Purpose: append feedback records to CSV
  - Trust reason: project-owned feedback collection

- `functions.py`
  - Purpose: shared utilities such as moderation and prompt assembly
  - Trust reason: project-owned helper logic

- Flask UI (`app.py`, `templates/index.html`, `static/css/styles.css`)
  - Purpose: user interface for travel planning
  - Trust reason: internal application experience

- Streamlit dashboards (`ticket_triage/1_Triage_Review.py`, `ticket_triage/2_Analytics_Dashboard.py`)
  - Purpose: internal quality review and analytics display
  - Trust reason: local review tools

---

### 2. Trust Boundary Zone
These are interfaces where trust must be explicitly managed, including external endpoints and API keys.

- `.env` configuration
  - Purpose: store credentials and endpoint configuration
  - Trust controls: secure file access, never commit secrets to source control

- Local Ollama service (`http://localhost:11434/api/embeddings`)
  - Purpose: embedding inference endpoint
  - Trust controls: local service security, restricted network access, service access rules

- `rag_model/embedding_generator.py` call to Ollama
  - Purpose: embedding generation from project-owned text
  - Trust controls: request formatting, error handling

- `rag_model/vector_search.py` call to Ollama for query embeddings
  - Purpose: encode queries into same semantic space
  - Trust controls: maintain query privacy, local endpoint only

- `ticket_triage/triage_engine.py` call to Google Gemini
  - Purpose: classify support tickets
  - Trust controls: prompt content, API request scope, response validation

- `rag_model/vector_search.py` call to Azure OpenAI
  - Purpose: generate the final travel recommendation
  - Trust controls: prompt safety, use only provided context

- CSV output files (`triage_results.csv`, `routing_decisions.csv`, `feedback.csv`, etc.)
  - Purpose: persisted audit and analytics data
  - Trust controls: data governance, file permissions, data retention

---

### 3. Outside Trust Zone
These are third-party services and models outside direct control.

- **Ollama model `nomic-embed-text`**
  - Role: embedding model implementation
  - Trust note: third-party model weights and inference behavior are outside project control

- **Google Gemini 2.5 Flash**
  - Role: ticket classification LLM
  - Trust note: model behavior, semantics, and API availability are external risks

- **Azure OpenAI deployment**
  - Role: response generation LLM
  - Trust note: provider governance, service availability, and billing risks

- **OpenAI / Azure API services**
  - Role: transport layer and infrastructure
  - Trust note: external telemetry, API abuse controls, latency

- **Third-party libraries** (`pandas`, `numpy`, `sklearn`, `streamlit`, `flask`, `faker`, etc.)
  - Role: runtime dependencies
  - Trust note: supply chain risk, version vulnerabilities

---

## Capability Placement Summary

| Capability | Zone |
|------------|------|
| Travel data generation | Inside Trust |
| Travel JSON conversion | Inside Trust |
| Chunking + embeddings orchestration | Inside Trust |
| Vector search and prompt assembly | Inside Trust |
| Ticket generation | Inside Trust |
| Routing rules | Inside Trust |
| Analytics and feedback capture | Inside Trust |
| Local Ollama embedding service | Trust Boundary |
| Azure OpenAI LLM calls | Trust Boundary |
| Gemini classification calls | Trust Boundary |
| Secure API key handling (.env) | Trust Boundary |
| External model providers | Outside Trust |
| Third-party packages | Outside Trust |

---

## Trust Management Recommendations

1. Keep `.env` files outside version control.
2. Validate all API responses before use.
3. Log only metadata, not raw sensitive user data.
4. Enforce least privilege on local Ollama and Azure endpoints.
5. Use strong secrets management for Gemini and Azure keys.
6. Monitor third-party library versions and apply patches.
7. Clearly document where data enters and exits the trusted boundary.

---

## Suggested Canvas Usage

Use this canvas in a slide or architecture documentation section to show that each capability is mapped to exactly one zone. That delivers a clear security and governance story for reviewers.