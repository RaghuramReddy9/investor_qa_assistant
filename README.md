# Investor Q&A Assistant — Live RAG System

A production-style **Hybrid Retrieval-Augmented Generation (Live RAG)** system that answers investor and market-related questions using:

- **Offline knowledge** (vector database over static documents)
- **Live data** (real-time news via external APIs)
- **LLM-based routing logic** to decide the correct data source
- **Safe fallback behavior** when live information is insufficient

This project demonstrates how real-world GenAI systems are designed to avoid stale answers, hallucinations, and unsafe assumptions — especially in **financial and investor-facing use cases**.

## Problem Statement

Traditional Retrieval-Augmented Generation (RAG) systems rely on **static, pre-indexed data** stored in vector databases. While this works well for stable knowledge (definitions, policies, documentation), it becomes **dangerous and misleading** in domains where information changes frequently — such as **financial markets**.

For example:
- Stock prices change daily
- Market sentiment evolves in real time
- News events can invalidate yesterday’s data

An offline-only RAG system may confidently return **outdated or incorrect answers**, giving users a false sense of accuracy.

### Why This Matters in Finance

In investor-facing applications, **stale information is worse than no information**.  
Providing outdated insights about markets or stocks can lead to:
- Poor decision-making
- Loss of trust
- Regulatory and ethical concerns

This project addresses that gap by combining **offline knowledge** with **live market data**, while enforcing strict routing and safety rules.

---

## System Architecture

The system is designed as a **Hybrid Live RAG pipeline** with explicit routing logic to ensure the correct data source is used for each user query.

### High-Level Flow

1. **User submits a question**
2. A **router component** analyzes the intent of the question
3. The system selects one of two paths:
   - **Offline RAG path** for static, conceptual, or evergreen knowledge
   - **Live data path** for time-sensitive market or news-related queries
4. The selected context is passed to a **Large Language Model (LLM)** for grounded answer generation
5. If sufficient information is not available, the system **fails safely** instead of hallucinating

### Offline RAG Path (Vector-Based)

Used for:
- Investment concepts (e.g., diversification, risk)
- Company fundamentals
- General financial knowledge

Steps:
- Documents are embedded using Gemini embeddings
- Stored in a FAISS vector database
- Relevant chunks are retrieved via semantic similarity
- Retrieved context is passed to the LLM for answer generation

### Live Data Path (Real-Time News)

Used for:
- Latest stock-related news
- Recent market events
- Time-sensitive investor questions

Steps:
- User question is cleaned into a **search-friendly query**
- Live news is fetched via an external API
- Raw results are lightly filtered for relevance
- The LLM summarizes the live context into a user-facing answer
- If live data is insufficient, the system explicitly says so

### Safety & Reliability Principles

- **No mixing of stale and live data**
- **No price hallucination**
- **Explicit refusal when data is insufficient**
- **Clear separation between retrieval and reasoning**

This architecture mirrors how real-world, production-grade GenAI systems are built for high-risk domains.

---

## Tech Stack & Design Decisions

This project intentionally uses a **minimal but production-relevant stack**, focusing on clarity, safety, and extensibility rather than unnecessary complexity.

### Large Language Model (LLM)
- **Gemini 2.5 Flash**
- Chosen for fast inference, strong reasoning, and reliable tool usage
- Used strictly for:
  - Routing decisions
  - Grounded answer generation
- Not used for uncontrolled free-form answering

### Embeddings
- **Gemini Embedding Model**
- Used consistently for both document indexing and query embedding
- Ensures semantic compatibility within the vector database


### Vector Database
- **FAISS (local)**
- Lightweight, fast, and well-suited for prototyping and portfolio projects
- Clearly separates **generated artifacts** from source code
- Can be replaced with managed vector databases (Pinecone, Weaviate) without changing system logic

### Live Data Source
- **External News API**
- Provides real-time signals for market and stock-related questions
- Treated as a **noisy signal**, not a source of truth
- All live data is filtered and summarized before being shown to the user

### Orchestration & Routing
- **LLM-based routing logic**
- Determines whether a query should use:
  - Offline vector retrieval
  - Live external data
- Keeps decision-making explicit and testable

### Application Structure
- Modular Python project (`src/` layout)
- Clear separation between:
  - Routing
  - Retrieval
  - Live data access
  - Answer generation
- Designed to be extended into multi-agent or evaluation-driven systems

---

## Example Queries

The system automatically routes questions to the appropriate data source.

### Offline Knowledge (Vector RAG)
These questions are answered using the internal vector database:

- `What is diversification in investing?`
- `What is market risk?`
- `What does Tesla do as a company?`

### Live Data (Real-Time News)
These questions trigger live data retrieval and summarization:

- `Latest news about Tesla stock`
- `What happened to Nvidia this week?`
- `Recent market news affecting AI companies`

### Safe Fallback Behavior
If sufficient live information is not available, the system responds safely:

- `What is the exact current price of Tesla stock?`

Response:
> *I don't have enough live information to answer that.*

This prevents hallucination and misleading answers.

---

## How to Run the Project

### Prerequisites
- Python 3.10+
- API keys for:
  - Gemini (Google Generative AI)
  - News API (for live data)

### Setup

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd investor-qa-assistant
   ```
2. Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # macOS/Linux
    .venv\Scripts\activate     # Windows
    ```
3. Install dependencies:
    ```bash
    Install dependencies:
    ```
4. pip install -r requirements.txt
    ```env
    Create a .env file in the project root:
    ```

### Build the Vector Store (Offline RAG)

Run the ingestion pipeline once:
```bash
python src/ingest.py
```
python src/ingest.py

### Run the Live RAG Assistant
Run the assistant as a module:
```bash
python -m src.assistant
```
python -m src.assistant
- static knowledge questions
- static knowledge questions

### Safety Notes
- This system `does not provide financial advice`

- It intentionally avoids:
    - stock price prediction
    - exact real-time pricing
    - speculative recommendations

- If live data is insufficient, the system fails safely instead of hallucinating

`This design choice reflects best practices for deploying GenAI systems in high-risk domains.`

---

## Author

**Raghuramreddy Thirumalareddy**

Aspiring Generative AI Engineer focused on building **production-grade GenAI systems** using:
- Retrieval-Augmented Generation (RAG)
- Live data integration
- LLM orchestration and safety-first design

🔗 GitHub: https://github.com/RaghuramReddy9  
🔗 LinkedIn: https://www.linkedin.com/in/raghuramreddy-ai
