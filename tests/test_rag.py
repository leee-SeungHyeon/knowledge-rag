from unittest.mock import MagicMock

from app.rag import Answer, answer_question, build_context


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
    client.chat.completions.create.assert_not_called()


def test_answer_question_returns_sources_and_answer():
    collection = MagicMock()
    collection.query.return_value = {
        "ids": [["a.md::0", "b.md::1"]],
        "documents": [["A 내용", "B 내용"]],
        "metadatas": [[{"source": "a.md"}, {"source": "b.md"}]],
        "distances": [[0.1, 0.2]],
    }

    client = MagicMock()
    client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="이것이 답변입니다."))]
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
    assert len(result.hits) == 2
