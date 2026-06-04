# Failure Mode and Effects Analysis (FMEA) for GenAI Project

## FMEA Summary

This register describes potential failure modes for the GenAI project, with risk priority and mitigation.

| ID | Failure Mode | Cause | Effect | Severity (1-10) | Occurrence (1-10) | Detection (1-10) | RPN | Mitigation |
|----|--------------|-------|--------|-----------------|------------------|------------------|-----|------------|
| 1 | Embedding service unavailable | Ollama not running or port blocked | RAG search fails, travel recommendations unavailable | 8 | 5 | 6 | 240 | Add health check, restart automation, fallback to cached embeddings |
| 2 | Incorrect embedding alignment | Query embeddings and chunk embeddings mismatch | Wrong or irrelevant travel recommendations | 7 | 4 | 5 | 140 | Use consistent embedding model/version, validate on sample queries |
| 3 | Azure OpenAI prompt hallucination | Poor prompt design or insufficient context | Inaccurate travel suggestions | 9 | 4 | 4 | 144 | Constrain prompt to provided context, use system instructions, human review |
| 4 | Gemini classification error | Incomplete prompt or model misclassification | Wrong ticket category and routing action | 9 | 5 | 4 | 180 | Add prompt validation, use confidence threshold, compare against historical labels |
| 5 | Over-automation of sensitive tickets | Confidence threshold too low or category mapping missing | Critical tickets auto-routed incorrectly | 10 | 3 | 5 | 150 | Always escalate `NEVER_AUTO_RESPOND` categories, tune threshold conservatively |
| 6 | Feedback data corruption | CSV write failure or malformed rows | Analytics inaccurate, wrong KPI decisions | 7 | 3 | 5 | 105 | Add write validation, row schema checks, backup copies |
| 7 | KPI drift undetected | No timestamp or inconsistent dates | Performance degradation hidden | 8 | 4 | 6 | 192 | Enforce date logging, verify drift dashboard data daily |
| 8 | Trust boundary breach | Secrets committed or external endpoint misconfigured | Data leakage, API abuse, compliance risk | 10 | 2 | 4 | 80 | Use `.gitignore`, secure secrets store, restrict network access |
| 9 | Ticket generator bias | Synthetic ticket distribution uneven | Nonrepresentative triage evaluation | 6 | 4 | 6 | 144 | Diversify synthetic ticket categories and language patterns |
| 10 | Service latency spike | External API delay or local model overload | Slow user experience or timeout errors | 7 | 5 | 5 | 175 | Add retries, timeouts, caching, and circuit breaker patterns |
| 11 | Missing or invalid API keys | `.env` misconfiguration | Pipeline fails before running | 8 | 4 | 7 | 224 | Validate environment at startup, provide clear configuration errors |
| 12 | Drift dashboard misinterpretation | Metrics not correctly aggregated | Action taken on wrong signal | 7 | 3 | 6 | 126 | Validate analytics formulas, peer review dashboard logic |

---

## FMEA Details

### 1. Embedding service unavailable
- Cause: Local Ollama server not started or port blocked.
- Effect: RAG travel planner cannot generate or retrieve embeddings, resulting in failed recommendations.
- Mitigation: Implement local service health checks, automated restart scripts, and fallback to cached embeddings.

### 2. Incorrect embedding alignment
- Cause: Embeddings for stored chunks and query are generated using different versions or models.
- Effect: Semantic search returns irrelevant chunks and poor travel recommendations.
- Mitigation: Freeze embedding model version, document exact API endpoint, and run consistency tests.

### 3. Azure OpenAI prompt hallucination
- Cause: LLM tendency to invent unsupported details when context is weak.
- Effect: User receives inaccurate travel advice.
- Mitigation: Restrict output to only provided context, use clear system instructions, and confirm results with human review samples.

### 4. Gemini classification error
- Cause: Complex ticket wording, ambiguous categories, or prompt design issues.
- Effect: Ticket is assigned the wrong category and routed incorrectly.
- Mitigation: Add classification prompt controls, verify model outputs, and retrain prompt template based on failure cases.

### 5. Over-automation of sensitive tickets
- Cause: Confidence threshold set too low or new sensitive categories introduced without rules.
- Effect: VIP and regulatory tickets bypass human oversight.
- Mitigation: Keep strict `NEVER_AUTO_RESPOND` category rules, review thresholds every quarter, and add monitoring alerts.

### 6. Feedback data corruption
- Cause: CSV file write error or invalid row structure from manual review.
- Effect: Analytics and KPI decisions are based on bad data.
- Mitigation: Perform schema validation before appending feedback, archive backups, and use atomic write operations.

### 7. KPI drift undetected
- Cause: Missing `date` field or inconsistent timestamps in feedback records.
- Effect: Drift detection dashboard fails to show real performance degradation.
- Mitigation: Enforce timestamped records, validate drift pipeline input, and add alerts on missing dates.

### 8. Trust boundary breach
- Cause: Credentials stored insecurely, `.env` committed, or external API endpoint exposed.
- Effect: Data leakage, unauthorized access, and compliance failures.
- Mitigation: Add `.gitignore` rules, use secret management, and enforce least-privilege API access.

### 9. Ticket generator bias
- Cause: Synthetic dataset has uneven category distribution or repetitive language.
- Effect: Triage evaluation fails to represent real-world variability.
- Mitigation: Expand ticket generator categories and diversify descriptions.

### 10. Service latency spike
- Cause: External API throttling or local compute resource saturation.
- Effect: Slow responses and user dissatisfaction.
- Mitigation: Add retries with exponential backoff, set timeouts, and cache common responses.

### 11. Missing or invalid API keys
- Cause: Environment variables not set or misconfigured.
- Effect: Application crashes before startup.
- Mitigation: Validate API keys at launch, show clear error messages, and provide setup documentation.

### 12. Drift dashboard misinterpretation
- Cause: Incorrect aggregation logic or wrong metric definitions.
- Effect: Teams make wrong operational decisions.
- Mitigation: Peer review analytics code, add unit tests for metrics, and document definitions clearly.

---

## Risk Priority Numbers and Focus

Focus initial risk reduction on:
- RPN 240: Embedding service unavailable
- RPN 224: Missing or invalid API keys
- RPN 192: KPI drift undetected
- RPN 180: Gemini classification error
- RPN 175: Service latency spike

These items deserve immediate mitigation for a reliable prototype deployment.

---

## Notes for Presentation

- Use the FMEA to demonstrate proactive failure planning.
- Explain how each mitigation maps to a capability and trust zone.
- Show that the system is designed for safe automation, not just raw AI output.
