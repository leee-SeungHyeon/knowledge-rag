from dataclasses import dataclass

from openai import OpenAI

from app.store import search

SYSTEM_PROMPT = """\
당신은 사용자의 개인 노트를 기반으로 답변하는 어시스턴트입니다.

규칙:
- 제공된 컨텍스트에 근거해서만 답변하세요.
- 컨텍스트에 답이 없으면 "관련 정보를 찾지 못했습니다"라고 답하세요.
- 답변 마지막에 출처 파일명을 인용하세요.
"""


@dataclass
class Answer:
    answer: str
    sources: list[str]
    hits: list[dict]


def build_context(hits: list[dict]) -> str:
    blocks = []
    for hit in hits:
        source = hit["metadata"]["source"]
        blocks.append(f"[출처: {source}]\n{hit['content']}")
    return "\n\n---\n\n".join(blocks)


def answer_question(
    *,
    client: OpenAI,
    collection,
    query: str,
    top_k: int,
    chat_model: str,
) -> Answer:
    hits = search(collection, query, top_k)

    if not hits:
        return Answer(answer="관련 정보를 찾지 못했습니다.", sources=[], hits=[])

    context = build_context(hits)

    response = client.chat.completions.create(
        model=chat_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"컨텍스트:\n\n{context}\n\n질문: {query}"},
        ],
    )

    answer_text = response.choices[0].message.content or ""
    sources = sorted({hit["metadata"]["source"] for hit in hits})

    return Answer(answer=answer_text, sources=sources, hits=hits)
