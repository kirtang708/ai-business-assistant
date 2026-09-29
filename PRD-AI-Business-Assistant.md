# Product Requirements Document (PRD)
## AI Business Assistant for Small Businesses

**Author:** [Your Name]
**Date:** [Date]
**Status:** Draft v1.0
**Related Project:** Retail Business Intelligence & Optimization Platform (data source)

---

## 1. Executive Summary

Small business owners and store managers generate large amounts of sales and operational data through POS systems and spreadsheets, but most lack the technical skills or time to translate that data into decisions. This product is a conversational AI assistant that lets a non-technical manager ask plain-language questions about their business ("Why did sales decrease last month?") and receive an accurate, data-grounded explanation, along with supporting charts and a shareable report.

---

## 2. Problem Statement

> Small business managers and owners have access to sales and operations data, but lack the time, tools, or technical expertise to analyze it. As a result, declining sales, stockouts, and underperforming stores are often noticed too late — after the financial impact has already occurred.

Existing BI dashboards (Power BI, Tableau) solve part of this problem, but still require the user to know what to look for and how to interpret it. This product removes that barrier by allowing natural-language interaction.

---

## 3. Goals and Non-Goals

**Goals**
- Let a non-technical user get accurate, explained answers to business performance questions
- Reduce the time to identify the root cause of a business change from ~30 minutes of manual analysis to under 1 minute
- Produce shareable, management-ready summaries automatically

**Non-Goals (out of scope for v1)**
- Real-time streaming data integration (batch/periodic data refresh is sufficient for v1)
- Multi-language support
- Predictive/prescriptive automation (e.g., auto-reordering inventory) — reserved for a future phase
- Enterprise-scale data volumes — v1 targets a single business with up to ~10 store locations

---

## 4. Target Users / Personas

| Persona | Description | Primary Goal | Key Pain Point |
|---|---|---|---|
| **Store Manager** | Runs day-to-day operations of a single location | Spot and react to sales/inventory issues quickly | No time to build or read reports |
| **Business Owner** | Oversees the whole business, often across multiple stores | Understand overall business health at a glance | Not technical; relies on others to interpret data |
| **Operations Manager** | Manages inventory and cross-store performance | Catch inefficiencies and anomalies early | Data is siloed across systems/stores |

---

## 5. User Stories

1. As a **store manager**, I want to ask "why did sales decrease last month?" so that I can understand the cause without running my own reports.
2. As a **business owner**, I want a weekly KPI summary so that I stay informed without logging into a dashboard.
3. As an **operations manager**, I want the assistant to flag anomalies (e.g., an underperforming store or a spike in stockouts) so that I can investigate proactively.
4. As a **store manager**, I want to see a chart alongside a text explanation so that I can visually confirm the trend.
5. As a **business owner**, I want to export a summary as a report so that I can share it with stakeholders or investors.

---

## 6. Functional Requirements

| ID | Requirement |
|---|---|
| FR-1 | System shall accept natural-language questions via a chat-style interface |
| FR-2 | System shall query underlying sales/inventory data (SQL) to compute relevant metrics before generating a response |
| FR-3 | System shall generate a natural-language explanation grounded in the computed metrics (not free-form LLM speculation) |
| FR-4 | System shall generate a relevant chart alongside the text answer where applicable |
| FR-5 | System shall produce a weekly/monthly auto-generated KPI summary |
| FR-6 | System shall detect and surface anomalies (e.g., a store or category deviating significantly from its historical baseline) |
| FR-7 | System shall allow the user to export a report (PDF or shareable summary) |

---

## 7. Non-Functional Requirements

| ID | Requirement |
|---|---|
| NFR-1 | Response latency under ~5 seconds for a standard query |
| NFR-2 | No sensitive business data shall be sent to a third-party LLM API beyond what's needed to generate the explanation (aggregated metrics only, not raw records, where possible) |
| NFR-3 | System shall function correctly with a small dataset (single business, up to 10 stores) without requiring big-data infrastructure |
| NFR-4 | System shall be usable by a non-technical person with no training |

---

## 8. System Architecture (High Level)

```
User Question (Streamlit UI)
        ↓
Query Router (classify: metric lookup / comparison / trend / anomaly)
        ↓
SQL Database (cleaned retail data — reused from Retail BI project)
        ↓
Pandas Analysis Layer (computes % change, category/store breakdown, anomaly flags)
        ↓
LLM API (takes computed numbers + structured prompt → generates explanation in plain language)
        ↓
Streamlit Output (text answer + chart + optional exportable report)
```

**Key design principle:** The LLM does not perform the underlying math — Python/SQL computes the actual metrics, and the LLM's role is limited to explaining pre-computed, verified numbers in natural language. This avoids hallucinated figures and keeps the system auditable.

---

## 9. Acceptance Criteria (v1 / MVP)

- [ ] User can type a question like "why did sales decrease last month?" and receive a response referencing real computed numbers from the dataset
- [ ] Response includes at least one supporting chart
- [ ] KPI summary can be generated on demand for a selected time period
- [ ] At least 3 anomaly types are detected automatically (e.g., store underperformance, category decline, stockout spike)
- [ ] User can export a summary report

---

## 10. KPIs / Success Metrics

| Metric | Target (for this project) |
|---|---|
| Query response accuracy | Correctly identifies the actual driver of a change in test scenarios |
| Time saved vs. manual analysis | Estimated reduction from ~30 min to under 1 min per question |
| Question coverage | Can answer a defined set of ~15-20 common manager questions |
| Report generation | Produces a usable, shareable report in under 10 seconds |

---

## 11. Risks

| Risk | Mitigation |
|---|---|
| LLM hallucinates numbers not grounded in real data | Architecture restricts LLM to explaining pre-computed values only, never generating figures itself |
| Small/synthetic dataset doesn't reflect realistic seasonality or anomalies | Choose or construct a dataset with known seasonal patterns and injected anomalies for testing |
| API costs scale unpredictably | Cache common queries; limit context sent to the LLM to only necessary aggregated data |
| Non-technical users ask ambiguous questions the system can't parse | Provide example prompts/suggested questions in the UI; handle unclear queries with a clarifying response |

---

## 12. Roadmap

| Phase | Deliverable | Target Timeframe |
|---|---|---|
| Phase 1 | KPI dashboard + SQL analysis layer (reuse Retail BI project data) | Weeks 1-2 |
| Phase 2 | LLM integration — natural language Q&A on top of KPI layer | Weeks 3-4 |
| Phase 3 | Anomaly detection (automatic flagging of unusual patterns) | Weeks 5-6 |
| Phase 4 | Automated report generation, polish, demo video | Weeks 7-8 |

---

## 13. Future Features (Post-v1)

- Predictive alerts (e.g., "Store 3 is trending toward a stockout in 5 days")
- Multi-business / franchise-level rollup views
- Voice-based query interface
- Automated recommendation engine (e.g., suggested reorder quantities, promotion targeting)

---

## 14. Technologies

- **Data:** SQL (SQLite/PostgreSQL), Pandas
- **AI:** LLM API (OpenAI, Claude, or similar)
- **Frontend:** Streamlit
- **Visualization:** Matplotlib/Plotly (embedded in Streamlit) or Power BI for the KPI report
- **Version control:** GitHub

---

## 15. Appendix: Sample Interaction

**User:** "Why did sales decrease last month?"

**System (computed):** Overall sales -8.4% MoM. Beverage category -17%. Store 3 transactions -12%.

**System (generated response):** "Sales decreased 8.4% last month, primarily driven by a 17% decline in beverage-category sales and a 12% drop in transactions at Store 3. Recommend investigating Store 3's local demand drivers and reviewing beverage pricing/promotion strategy."
