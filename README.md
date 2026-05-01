# Highwatch AI

Highwatch AI is a specialized document intelligence platform designed to transform your personal and professional documents into an interactive knowledge base. By integrating directly with Google Drive, the system allows you to chat with your files, extract insights, and find specific information using advanced Retrieval-Augmented Generation (RAG).

## Overview

The core objective of this project is to solve the problem of information fragmentation. Instead of manually searching through dozens of PDFs and text files, Highwatch AI indexes your data into a high-performance vector store, enabling a natural language interface for real-time querying.

## Core Functionality

### 1. Seamless Data Integration
Connect your Google Drive account to the dashboard. The system identifies document formats such as PDF and TXT, fetching them securely for local processing.

### 2. Intelligent Document Indexing
Each document is processed, semantically chunked, and transformed into high-dimensional embeddings. These embeddings are stored in a FAISS vector index, allowing for lightning-fast semantic search that understands the context, not just keywords.

### 3. Context-Aware AI Chat
Using a RAG architecture, the assistant retrieves only the most relevant sections of your documents to answer your questions. This ensures that the AI's responses are grounded in your actual data, significantly reducing hallucinations.

### 4. Privacy and Management
Manage your knowledge library through a dedicated interface. You can track sync status, view indexed documents, or clear your data whenever needed.

## Technical Architecture

The system is built with a focus on speed and modularity:

*   **Backend:** Developed with FastAPI for high-performance asynchronous execution.
*   **AI Infrastructure:** Powered by Groq (Llama 3) and Google Gemini for low-latency language processing.
*   **Vector Engine:** FAISS for efficient similarity search and indexing.
*   **Frontend:** A modern, single-page dashboard built with vanilla JavaScript and CSS, featuring a premium high-contrast theme and responsive navigation.

## Getting Started

### Prerequisites

*   Python 3.9 or higher
*   Google Cloud Console account (for Drive API access)
*   Groq or Gemini API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Gautam-Bharadwaj/fsd-timepass.git
   cd fsd-timepass
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   Create a .env file in the root directory with your credentials:
   ```env
   GOOGLE_CLIENT_ID=your_id
   GOOGLE_CLIENT_SECRET=your_secret
   GROQ_API_KEY=your_key
   GEMINI_API_KEY=your_key
   ```

4. Run the application:
   ```bash
   python main.py
   ```

5. Access the interface:
   Open http://localhost:8000 in your browser.

## Project Structure

*   /api: Core API routes and endpoint logic.
*   /connectors: Google Drive integration and OAuth handlers.
*   /processing: Document extraction and semantic chunking.
*   /search: Vector store management and similarity search.
*   /llm: RAG implementation, caching, and chat memory.
*   /frontend: Web dashboard and landing page assets.

## Attribution

This project was developed as a comprehensive solution for personal document management and AI-driven knowledge retrieval.
