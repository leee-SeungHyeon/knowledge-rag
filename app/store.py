from pathlib import Path

import chromadb
from chromadb.api.types import EmbeddingFunction
from chromadb.utils.embedding_functions.openai_embedding_function import (
    OpenAIEmbeddingFunction,
)

from app.chunker import Chunk

COLLECTION_NAME = "knowledge"


def build_embedding_function(api_key: str, model: str) -> EmbeddingFunction:
    return OpenAIEmbeddingFunction(api_key=api_key, model_name=model)


def get_collection(persist_dir: Path, embedding_fn: EmbeddingFunction):
    persist_dir.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(persist_dir))
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn,
    )


def upsert_chunks(collection, chunks: list[Chunk]) -> int:
    if not chunks:
        return 0

    ids = [f"{c.source}::{c.chunk_index}" for c in chunks]
    documents = [c.content for c in chunks]
    metadatas = [{"source": c.source, "chunk_index": c.chunk_index} for c in chunks]

    collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
    return len(chunks)


def search(collection, query: str, top_k: int) -> list[dict]:
    result = collection.query(query_texts=[query], n_results=top_k)

    hits = []
    for i in range(len(result["ids"][0])):
        hits.append(
            {
                "id": result["ids"][0][i],
                "content": result["documents"][0][i],
                "metadata": result["metadatas"][0][i],
                "distance": result["distances"][0][i] if result.get("distances") else None,
            }
        )
    return hits
