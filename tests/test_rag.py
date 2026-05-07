from unittest.mock import MagicMock

from app.rag import Answer, CitedAnswer, answer_question, build_context


def test_build_context_includes_source():
    hits = [
        {"metadata": {"source": "a.md"}, "content": "내용 A"},
        {"metadata": {"source": "b.md"}, "content": "내용 B"},
    ]
    context = build_context(hits)

    assert "[출처: a.md]" in context
    assert "[출처: b.md]" in context
    assert "내용 A" in context
    assert "내용 B" in context


def test_cited_answer_schema_instantiation():
    obj = CitedAnswer(answer="hello", cited_sources=["a.md"])
    assert obj.answer == "hello"
    assert obj.cited_sources == ["a.md"]

    # default empty
    obj2 = CitedAnswer(answer="hi")
    assert obj2.cited_sources == []


def test_answer_question_with_no_hits():
    collection = MagicMock()
    collection.query.return_value = {
        "ids": [[]],
        "documents": [[]],
        "metadatas": [[]],
        "distances": [[]],
    }
    client = MagicMock()

    result = answer_question(
        client=client,
        collection=collection,
        query="아무거나",
        top_k=4,
        chat_model="gpt-4o-mini",
    )

    assert isinstance(result, Answer)
    assert result.answer == "관련 정보를 찾지 못했습니다."
    assert result.sources == []
    assert result.cited_sources == []
    client.beta.chat.completions.parse.assert_not_called()


def _mock_parsed_response(answer: str, cited_sources: list[str]) -> MagicMock:
    parsed = CitedAnswer(answer=answer, cited_sources=cited_sources)
    return MagicMock(choices=[MagicMock(message=MagicMock(parsed=parsed))])


def test_answer_question_returns_sources_and_cited_sources():
    collection = MagicMock()
    collection.query.return_value = {
        "ids": [["a.md::0", "b.md::1"]],
        "documents": [["A 내용", "B 내용"]],
        "metadatas": [[{"source": "a.md"}, {"source": "b.md"}]],
        "distances": [[0.1, 0.2]],
    }

    client = MagicMock()
    client.beta.chat.completions.parse.return_value = _mock_parsed_response(
        answer="이것이 답변입니다.",
        cited_sources=["a.md"],
    )

    result = answer_question(
        client=client,
        collection=collection,
        query="질문",
        top_k=2,
        chat_model="gpt-4o-mini",
    )

    assert result.answer == "이것이 답변입니다."
    assert set(result.sources) == {"a.md", "b.md"}
    # cited_sources is a strict subset — only what LLM actually cited
    assert result.cited_sources == ["a.md"]
    assert len(result.hits) == 2


def test_cited_sources_can_differ_from_sources():
    """LLM이 검색된 모든 출처를 인용하지는 않는 일반적인 경우."""
    collection = MagicMock()
    collection.query.return_value = {
        "ids": [["a.md::0", "b.md::1", "c.md::0"]],
        "documents": [["A", "B", "C"]],
        "metadatas": [[{"source": "a.md"}, {"source": "b.md"}, {"source": "c.md"}]],
        "distances": [[0.1, 0.2, 0.3]],
    }

    client = MagicMock()
    client.beta.chat.completions.parse.return_value = _mock_parsed_response(
        answer="답변",
        cited_sources=["b.md"],
    )

    result = answer_question(
        client=client,
        collection=collection,
        query="질문",
        top_k=3,
        chat_model="gpt-4o-mini",
    )

    assert set(result.sources) == {"a.md", "b.md", "c.md"}
    assert result.cited_sources == ["b.md"]
    assert set(result.cited_sources).issubset(set(result.sources))
