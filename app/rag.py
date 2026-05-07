from dataclasses import dataclass

from openai import OpenAI
from pydantic import BaseModel, Field

from app.store import search

SYSTEM_PROMPT = """\
당신은 사용자의 개인 노트를 기반으로 답변하는 어시스턴트입니다.

규칙:
- 제공된 컨텍스트에 근거해서만 답변하세요.
- 컨텍스트에 답이 없으면 answer에 "관련 정보를 찾지 못했습니다"라고 적고
  cited_sources는 빈 배열로 두세요.
- cited_sources에는 답변(answer)에서 실제로 근거로 사용한 파일명만 포함하세요.
  검색되었지만 답변에 사용하지 않은 출처는 절대 포함하지 마세요.
"""


class CitedAnswer(BaseModel):
    """LLM structured output schema."""

    answer: str = Field(description="사용자 질문에 대한 답변 본문")
    cited_sources: list[str] = Field(
        default_factory=list,
        description="answer에서 실제 근거로 사용한 출처 파일명 목록",
    )


@dataclass
class Answer:
    # answer: LLM이 생성한 답변 본문
    # sources: 검색(retrieval) 단계에서 반환된 모든 출처 파일명 (중복 제거, 정렬)
    # cited_sources: LLM이 답변에서 실제로 인용한 출처 (sources의 부분집합 또는 다른 집합일 수 있음)
    # hits: 검색 결과 원본
    answer: str
    sources: list[str]
    cited_sources: list[str]
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
        return Answer(
            answer="관련 정보를 찾지 못했습니다.",
            sources=[],
            cited_sources=[],
            hits=[],
        )

    context = build_context(hits)

    completion = client.beta.chat.completions.parse(
        model=chat_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"컨텍스트:\n\n{context}\n\n질문: {query}"},
        ],
        response_format=CitedAnswer,
    )

    parsed = completion.choices[0].message.parsed
    answer_text = parsed.answer if parsed else ""
    cited_sources = sorted(set(parsed.cited_sources)) if parsed else []
    sources = sorted({hit["metadata"]["source"] for hit in hits})

    return Answer(
        answer=answer_text,
        sources=sources,
        cited_sources=cited_sources,
        hits=hits,
    )
