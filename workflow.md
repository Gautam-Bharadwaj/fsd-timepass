# Project Workflow — Highwatch AI

This document outlines the operational and development workflows for the Highwatch AI RAG System.

---

## 1. System SDLC Workflow
The standard development lifecycle followed for this project.

```mermaid
graph LR
    A[Requirements] --> B[Architecture Design]
    B --> C[Development]
    C --> D[Integration Testing]
    D --> E[Deployment]
    E --> F[Monitoring & Optimization]
```

---

## 2. Authentication Flow (Google OAuth 2.0)
How the user connects their Google Drive to the system.

```mermaid
graph LR
    User[User] --> Login[GET /auth/login]
    Login --> Google[Google Consent Screen]
    Google --> Callback[GET /auth/callback]
    Callback --> Token[Store Tokens in Storage]
    Token --> Success[Dashboard Unlocked]
```

---

## 3. Data Ingestion & Sync Workflow
The process of transforming raw Drive files into searchable vector embeddings.

```mermaid
graph LR
    Start[Sync Request] --> Fetch[List Drive Files]
    Fetch --> Download[Download PDF/TXT]
    Download --> Extract[Extract Raw Text]
    Extract --> Chunk[Chunking: RecursiveSplitter]
    Chunk --> Embed[Embedding: MiniLM-L6-v2]
    Embed --> Vector[Store in FAISS Index]
```

---

## 4. Retrieval-Augmented Generation (RAG) Flow
How the AI answers questions based on the synced documents.

```mermaid
graph LR
    Input[User Question] --> QEmbed[Embed Query]
    QEmbed --> Search[FAISS Similarity Search]
    Search --> Context[Retrieve Top-K Chunks]
    Context --> Prompt[Augment Prompt with Context]
    Prompt --> LLM[LLM Generation: Llama 3]
    LLM --> Answer[Final Answer + Sources]
```

---

## 5. Directory Structure Overview
Horizontal view of the project architecture.

```mermaid
graph LR
    Root[highminds/] --> API[api/ - Routes]
    Root --> Conn[connectors/ - Drive Auth]
    Root --> Proc[processing/ - Extraction/Chunking]
    Root --> Search[search/ - FAISS Store]
    Root --> LLM[llm/ - AI Logic]
    Root --> UI[frontend/ - UI Files]
```
