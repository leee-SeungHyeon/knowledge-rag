# OBSERVATIONS

작업 중 발견한 Claude의 실수, 마찰 지점, 개선 아이디어를 한 줄씩 기록.  
3~5번 반복되는 패턴이 보이면 글로벌 하네스(`~/.claude/CLAUDE.md`, 훅 등)에 반영.

## 형식

```
YYYY-MM-DD | Phase | 카테고리 | 내용
```

카테고리:
- `mistake` — Claude의 실수
- `friction` — 작업 흐름이 끊긴 지점
- `idea` — 하네스 개선 아이디어
- `pattern` — 반복 발견 패턴

## 기록

```
2026-05-06 | -       | -        | 프로젝트 시작
2026-05-06 | Phase 1 | mistake  | sources 필드가 검색된 모든 청크를 반환 — 실제 인용된 출처와 차이. top_k가 작은 코퍼스에서는 거의 모든 문서가 sources에 포함됨. 답변 텍스트의 인용과 분리 필요.
2026-05-06 | Phase 1 | idea     | 답변에 인용된 출처만 추출하려면 (a) LLM에 structured output으로 cited_sources 받거나, (b) 답변 텍스트 후처리로 [출처: X.md] 패턴 파싱.
```

## Phase 1 회고 (2026-05-06)

**잘 된 점**
- 5개 노트로 시작해 검색 품질 즉시 검증 가능했음.
- 코드 리뷰가 파일명 충돌 버그 1건 발견 — 실제 수정 가치 있음.
- 11개 단위 테스트 통과, 외부 API 모킹으로 비용 0.

**개선할 점**
- `sources` 필드 의미 모호 (검색 vs 인용).
- FastAPI가 모듈 로드 시 Chroma/OpenAI 초기화 — 통합 테스트 작성 시 부담될 것.

**하네스 측면**
- 글로벌 자동 ruff 포맷이 자연스럽게 작동, 신경 쓸 필요 없었음.
- code-reviewer 서브에이전트가 실제 가치 있는 minor 발견 (파일명 충돌). Critical 없음 = 워크플로우 적정 수준 작동.

## v1 build 루프 + Tier A 훅 도입 (2026-05-07)

**도입한 것**
- `/build` 슬래시 커맨드 (`.claude/commands/build.md`) — 계획→구현→자가점검→보고 루프, Claude 단독.
- PostToolUse 훅 (`.claude/hooks/post_edit_check.sh`) — `app/**` 또는 `tests/**` 편집 시 자동으로 ruff + pytest 실행, 실패 시 exit 2로 컨텍스트에 전달.

**v1 시범 가동 — cited_sources 기능 추가**
- Stage A 작업 분해 5개, Stage B 구현, Stage C 자가 점검(ruff + pytest 5/5), Stage D 보고까지 끊김 없이 진행.
- 실 LLM 호출 검증 3건 모두 통과: cited_sources가 sources의 진부분집합, "정보 없음" 시 빈 배열, 환각 없음.
- v2 승격 신호: 0건. v1 충분히 작동.

**Tier A 훅 검증**
- `import os` 추가 시도 → 글로벌 auto-fix가 미사용 import를 즉시 제거 → 프로젝트 훅까지 도달 못 함. 두 layer가 보완 관계.
- pytest 실패 유도(assert 문자열 변경) → 프로젝트 훅이 정확히 잡음 → exit 2 + stderr 전달 → Claude 자동 인지 후 되돌림.
- 결론: lint는 글로벌 auto-fix가, 의미적 실패(테스트)는 프로젝트 훅이 담당하는 분업 성립.

**관찰**
- 2026-05-07 | Phase 1→2 | pattern  | 글로벌 자동 fix가 너무 잘 동작해서 단순 lint 검증으로는 프로젝트 훅 동작 확인 어려움. 향후 hook 검증은 auto-fix 영역 밖(테스트, E501 등)으로 시나리오 잡아야 함.
- 2026-05-07 | Phase 1→2 | idea     | Tier B (`/smoke`) — 실 LLM 호출 옵트인 통합 테스트는 Phase 2 이후 도입 검토. 비용 통제 위해 자동 트리거 안 함.
- 2026-05-07 | Phase 2  | friction | Tier A 훅은 Python 파일(`app/**`, `tests/**`)만 검증. Dockerfile, docker-compose, GitHub Actions yaml 등 비-Python 변경은 자동 검증 사각지대. Phase 2 진행하며 패턴 누적되면 hook 확장(예: `docker build` 검증, `actionlint`) 검토.
- 2026-05-07 | Phase 2  | mistake  | PR1 v1 가동 시 Stage A 계획에서 "non-root 사용자 + chroma_db 쓰기 경로" 충돌을 사전 예측 못함. 첫 docker run에서 PermissionError 발생 후 수정. 패턴: 런타임 권한/경로 점검이 v1 계획 단계에서 빠짐.
- 2026-05-07 | Phase 2  | idea     | v1 Stage A 계획 룰에 "런타임 쓰기 경로 / 권한 의존" 점검 항목 추가 검토. 또는 v1 Stage C에 "비-Python 산출물(Docker, IaC)에 대해서는 실제 기동 검증" 단계 추가.
- 2026-05-07 | Phase 2  | mistake  | PR1 이미지 크기 722MB로 목표(300MB) 크게 초과. chromadb 0.5+의 onnxruntime/heavy deps가 원인 추정. v1 Stage A에서 의존성 그래프 사전 검토 부재 — 수용 기준을 비현실적으로 잡음. 슬림화는 별도 PR로 분리.
