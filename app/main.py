from fastapi import FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel

from app.chunker import chunk_documents
from app.config import settings
from app.loader import load_markdown_files
from app.rag import answer_question
from app.store import build_embedding_function, get_collection, upsert_chunks

app = FastAPI(title="knowledge-rag")

embedding_fn = build_embedding_function(
    api_key=settings.openai_api_key,
    model=settings.embedding_model,
)
collection = get_collection(settings.chroma_dir, embedding_fn)
openai_client = OpenAI(api_key=settings.openai_api_key)


class IngestResponse(BaseModel):
    documents: int
    chunks: int


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ingest", response_model=IngestResponse)
def ingest() -> IngestResponse:
    try:
        documents = load_markdown_files(settings.notes_dir)
    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    chunks = chunk_documents(
        documents,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    upserted = upsert_chunks(collection, chunks)

    return IngestResponse(documents=len(documents), chunks=upserted)


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="query must not be empty")

    result = answer_question(
        client=openai_client,
        collection=collection,
        query=request.query,
        top_k=settings.top_k,
        chat_model=settings.chat_model,
    )
    return QueryResponse(answer=result.answer, sources=result.sources)
