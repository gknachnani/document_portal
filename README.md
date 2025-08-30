# DocNexus – AI-Powered Document Intelligence  

DocNexus is an **AI-driven platform** for analyzing, comparing, and conversing with documents using **Retrieval-Augmented Generation (RAG)**.  
It combines modern LLMs, embeddings, and scalable cloud deployment to deliver **enterprise-ready document intelligence**.  

---

## 🚀 Features  

- **Document Analysis** – Upload a PDF to extract summaries, insights, and metadata.  
- **Document Comparison** – Compare reference and candidate documents at a **page-level**.  
- **Knowledge Chat** – Conversational interface to query across multiple PDFs, DOCX, and TXT files.  
- **Embeddings & Retrieval**  
  - Google `models/text-embedding-004` with FAISS vector store.  
  - Configurable retriever (Top-K = 10).  
- **LLMs**  
  - **Groq DeepSeek-R1-Distill-LLaMA-70B** (low-latency, high-accuracy responses).  
  - **Google Gemini 2.0 Flash** (fast, scalable).  
- **Frameworks**  
  - **FastAPI** backend  
  - **LangChain** for RAG orchestration  
  - **Pydantic** for robust schema validation  
- **Deployment**  
  - Local testing with **Docker Desktop**  
  - Production CI/CD with **GitHub Actions** → AWS ECR/ECS  
- **Observability & Security**  
  - IAM-based role permissions  
  - Monitoring with Amazon CloudWatch  

---

## 🏗️ Architecture  

```mermaid
flowchart TD
    A[User Interface] -->|Upload / Query| B[FastAPI Backend]
    B -->|Chunk + Embed| C[Google Embeddings: text-embedding-004]
    C -->|Store| D[FAISS Vector DB]
    B -->|Retrieve Context| D
    B -->|Generate Response| E[LLMs: Groq DeepSeek / Google Gemini]
    E -->|Answer| A
    B -->|Logs & Metrics| F[AWS CloudWatch]
    B -->|Deploy| G[AWS ECS via ECR]
