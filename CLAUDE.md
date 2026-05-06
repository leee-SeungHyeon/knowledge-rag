# knowledge-rag

이 프로젝트는 글로벌 `~/.claude/CLAUDE.md` 규칙을 베이스로 하며, 아래 프로젝트 고유 규칙을 추가한다.

## 프로젝트 컨텍스트
- 학습 목적의 RAG 프로젝트. 클라우드/인프라 경험 보강과 하네스 엔지니어링 실험을 겸함.
- Phase 단위로 진화 (`ROADMAP.md` 참고).

## 개발 규칙
- Python 3.12+ 사용. 타입 힌트 필수.
- FastAPI + Pydantic v2 사용.
- 새 의존성 추가 시 `pyproject.toml`에 명시 (uv 또는 pip-tools 사용 예정).
- 모든 외부 호출(OpenAI, AWS 등)은 환경 변수로 키 관리. 코드에 하드코딩 금지.

## 테스트 규칙
- 새 기능에는 pytest 테스트 동반.
- 외부 API는 모킹 (테스트 비용 발생 방지).

## 회고 규칙
- 작업 중 발견한 Claude의 실수/마찰은 `OBSERVATIONS.md`에 즉시 기록.
- 각 Phase 완료 시 짧은 회고를 OBSERVATIONS 마지막에 추가.
