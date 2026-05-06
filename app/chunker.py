from dataclasses import dataclass

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.loader import Document


@dataclass
class Chunk:
    source: str
    content: str
    chunk_index: int


def chunk_documents(documents: list[Document], chunk_size: int, chunk_overlap: int) -> list[Chunk]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks: list[Chunk] = []
    for doc in documents:
        splits = splitter.split_text(doc.content)
        for i, text in enumerate(splits):
            chunks.append(Chunk(source=doc.source, content=text, chunk_index=i))
    return chunks
