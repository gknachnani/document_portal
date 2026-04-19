# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install
pip install -r requirements.txt
pip install -e .              # editable install (needed for src/* imports)

# Dev server
uvicorn api.main:app --port 8080 --reload

# Tests
pytest tests/                                        # all tests
pytest tests/test_unit_cases.py                      # single file
pytest tests/test_unit_cases.py::test_home           # single test
```

## Environment Variables

Copy `env.copy` to `.env` before running locally. Required keys:

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Groq API key |
| `GOOGLE_API_KEY` | Google Generative AI key |
| `LLM_PROVIDER` | `"google"` (default) or `"groq"` |
| `ENV` | Set to `"production"` to skip `.env` loading (ECS) |

In production (ECS), `API_KEYS` is a JSON string `{"GROQ_API_KEY": "...", "GOOGLE_API_KEY": "..."}` — `ApiKeyManager` (`utils/model_loader.py`) handles both modes.

Optional overrides: `FAISS_BASE`, `UPLOAD_BASE`, `FAISS_INDEX_NAME`, `DATA_STORAGE_PATH`, `CONFIG_PATH`.

## Architecture

### Request Flow

```
HTTP Request → api/main.py
  /analyze    → DocHandler (save PDF) → DocumentAnalyzer.analyze_document()
  /compare    → DocumentComparator (save PDFs) → DocumentComparatorLLM.compare_documents()
  /chat/index → ChatIngestor.build_retriever() → FAISS index saved to disk
  /chat/query → ConversationalRAG.invoke() → FAISS loaded → LLM answer
```

### Key Classes

- **`utils/model_loader.py`** — `ModelLoader` is the single point for loading embeddings (`google/text-embedding-004`) and LLMs (Groq or Google). Always go through this, never instantiate LLM/embedding clients directly.

- **`src/document_ingestion/data_ingestion.py`** — `FaissManager` wraps FAISS vector store and tracks ingested document fingerprints in a JSON sidecar to prevent re-indexing duplicates. `ChatIngestor` coordinates file upload → text splitting → embedding → `FaissManager`. `DocHandler` / `DocumentComparator` handle upload storage for the non-chat flows.

- **`src/document_chat/retrieval.py`** — `ConversationalRAG` uses an LCEL chain with two prompts: `contextualize_question` (reformulates query using chat history) then `context_qa` (answers using retrieved chunks). Retriever is lazy-loaded from the FAISS index on first call.

- **`src/document_analyzer/data_analysis.py`** — `DocumentAnalyzer` runs a single LLM chain → `JsonOutputParser` (wrapped in `OutputFixingParser`) → returns a `MetaData` Pydantic model.

- **`src/document_compare/document_comparator.py`** — `DocumentComparatorLLM` concatenates both PDFs and prompts the LLM for a page-level diff, returning a list of `ChangeFormat` objects.

### Prompts and Models

All prompt templates live in `prompt/prompt_library.py` under `PROMPT_REGISTRY`, keyed by `PromptType` enum values (defined in `model/models.py`). Pydantic response schemas (`MetaData`, `ChangeFormat`, `SummaryResponse`) are also in `model/models.py`.

### Session Isolation

Chat sessions use a UUID `session_id`. FAISS indices are stored at `{FAISS_BASE}/{session_id}/` and uploaded files at `{UPLOAD_BASE}/{session_id}/`. This allows concurrent users without state collision.

### LLM Configuration

`config/config.yaml` defines model names, temperature, and max tokens for both providers. `ModelLoader` reads this via `utils/config_loader.py`. To add a new LLM provider, extend `ModelLoader.load_llm()` and add a config block.

## CI/CD

- **CI** (`.github/workflows/ci.yml`): runs `pytest tests/` on every push/PR.
- **CD** (`.github/workflows/aws.yml`): triggers on successful CI on `master` → builds Docker image → pushes to ECR → deploys to ECS Fargate. Deployment is non-blocking (`wait-for-service-stability: false`).
- CloudFormation templates are in `infrastructure/`.
