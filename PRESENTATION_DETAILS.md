# GenAI Project Presentation Details

## 1. Presentation Structure

### Slide 1: Title & Executive Summary
- Project title: `GenAI Project: RAG Travel Planner + Intelligent Ticket Triage`
- One-line mission: "Build a hybrid intelligence platform that combines retrieval-augmented travel recommendations with automated ticket triage, routing, and quality feedback loops."
- Key value proposition: faster decisions, safer automation, continuous learning.

### Slide 2: Business Goals
- Goal 1: Accelerate support operations by automating ticket classification and routing.
- Goal 2: Improve customer recommendations through semantic retrieval and context-aware travel planning.
- Goal 3: Introduce a measurable feedback loop for quality and drift control.

### Slide 3: System Overview
- Two major subsystems:
  - RAG Travel Planning (travel data ingestion, embeddings, search, LLM generation)
  - Ticket Triage (ticket generation, Gemini classification, escalation, analytics)
- Diagram showing where data enters, how it flows, and where outputs are produced.

### Slide 4: Key Decisions & Rationale
- Use **Ollama** locally for embeddings
  - Rationale: privacy-preserving, cost-efficient, no external embedding API fees.
- Use **Azure OpenAI** for final travel recommendation generation
  - Rationale: enterprise-grade quality, flexible prompt control, supported deployment.
- Use **Google Gemini** for ticket classification
  - Rationale: fast classification, strong instruction following, and simple response parsing.
- Structure travel content as **JSON → text → chunks → embeddings**
  - Rationale: easier control, better retrieval relevance, scalable document ingestion.
- Implement **confidence-based routing** with manual escalation rules
  - Rationale: reduces risk, preserves human oversight for sensitive issues.
- Build **feedback-driven analytics** instead of only outputs
  - Rationale: quality assurance, measurable KPIs, model drift detection.

### Slide 5: RAG Pipeline Details
- Data generation from synthetic travel records.
- Conversion into textual travel documents.
- Chunking into ~300 semantic pieces to maximize retrieval precision.
- Embedding generation via Ollama local model.
- Search using cosine similarity and top-5 context assembly.
- Response generation using Azure OpenAI with context-constrained prompts.
- User interface via Flask and optional terminal flow.

### Slide 6: Ticket Triage Pipeline Details
- Synthetic ticket generation using Faker.
- Classification by Gemini into 9 categories.
- Routing rules in `escalation_service.py`:
  - Auto-route high-confidence tickets
  - Escalate critical categories always
  - Human review for medium confidence
- Feedback capture by manual review UI and CSV logging.
- Analytics covering override rate, acceptance rate, and drift.

### Slide 7: Trust Boundaries & Capability Zones
- Define exactly one capability per zone:
  - **Inside Trust**: owned services and code executed within project boundaries.
  - **Trust Boundary**: external services and APIs with clear boundaries.
  - **Outside Trust**: third-party AI providers and data sources.
- Explain how each capability maps into a zone.

### Slide 8: Quality Metrics and Feedback Loop
- Metrics to highlight:
  - Override Rate
  - Accept Rate
  - Accepted Accuracy
  - Auto Draft Rate
  - Acceptance Rate
  - Drift dashboard
- Show how feedback labels cause continuous adaptation and improvement.

### Slide 9: Failure Mode Register Summary
- Present an FMEA with at least 8 failure modes.
- Show severity, occurrence, detection, and mitigation for each.
- Focus on risks across RAG, ticket triage, trust, and data quality.

### Slide 10: Project Data and Key Insights
- Include dataset size and structure.
- Mention performance assumptions.
- Highlight the reason for local embeddings and hybrid LLM usage.

### Slide 11: Future Roadmap
- Potential enhancements:
  - database-backed storage
  - retraining / auto-retraining workflows
  - multi-model ensemble for classification
  - robust drift alerts and monitoring

### Slide 12: Closing and Questions
- Summarize impact, risks, and readiness.
- Invite questions on architecture, trust, and quality.

---

## 2. Key Decisions with Rationale

### Decision: Local Embeddings via Ollama
- Reason: keep embedding generation self-hosted and avoid embedding API costs.
- Benefit: lower latency for local experimentation, no sensitive data exposure off-prem.

### Decision: Azure OpenAI for LLM Generation
- Reason: enterprise reliability and compatibility with existing Azure infrastructure.
- Benefit: strong natural language response quality and production readiness.

### Decision: Google Gemini for Ticket Triage
- Reason: fast classification and structured JSON output.
- Benefit: strong category extraction and low-cost inference for support workflows.

### Decision: Confidence-based Auto-routing
- Reason: balance automation and safety.
- Benefit: reduce false positives while scaling automation.

### Decision: Human feedback capture in CSV files
- Reason: simple audit trail and explicit training signal.
- Benefit: easy analysis, reproducibility, and manual correction.

### Decision: Separate RAG and Triage Domains
- Reason: different AI workloads and operational requirements.
- Benefit: independent scaling, easier debugging, and clearer architecture.

### Decision: Use Streamlit for Analytics
- Reason: rapid dashboard development.
- Benefit: quick insights without heavy frontend work.

### Decision: Minimal dependency on external DBs
- Reason: keep the prototype lightweight and portable.
- Benefit: easier setup and demonstration without database installation.

---

## 3. Presentation Tips

- Use visuals for flows and boundaries rather than text-heavy slides.
- Keep each slide focused on a single theme.
- Emphasize business value before technical detail.
- Link every technical choice back to risk mitigation or ROI.
- Use the FMEA slide to demonstrate that you considered failure modes deeply.
- Mention the trust boundary canvas to show security and governance awareness.

---

### Suggested Slide Titles
- "Why GenAI Project Matters"
- "RAG System Architecture"
- "Ticket Triage Workflow"
- "AI Model Decisions and Tradeoffs"
- "Trust Boundaries and Data Safety"
- "Quality Assurance and Feedback Loop"
- "Failure Mode Register"
- "Metrics, KPIs, and Drift Detection"
- "Future Enhancements"
- "Demo / Next Steps"
