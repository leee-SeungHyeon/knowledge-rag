from app.chunker import chunk_documents
from app.loader import Document


def test_chunk_documents_short_text():
    docs = [Document(source="a.md", content="짧은 글입니다.")]
    chunks = chunk_documents(docs, chunk_size=800, chunk_overlap=100)

    assert len(chunks) == 1
    assert chunks[0].source == "a.md"
    assert chunks[0].chunk_index == 0


def test_chunk_documents_long_text_splits():
    long_text = "문장입니다. " * 500
    docs = [Document(source="long.md", content=long_text)]

    chunks = chunk_documents(docs, chunk_size=200, chunk_overlap=20)

    assert len(chunks) > 1
    assert all(c.source == "long.md" for c in chunks)
    assert [c.chunk_index for c in chunks] == list(range(len(chunks)))


def test_chunk_documents_multiple_sources():
    docs = [
        Document(source="a.md", content="A 내용"),
        Document(source="b.md", content="B 내용"),
    ]
    chunks = chunk_documents(docs, chunk_size=800, chunk_overlap=100)

    sources = {c.source for c in chunks}
    assert sources == {"a.md", "b.md"}
