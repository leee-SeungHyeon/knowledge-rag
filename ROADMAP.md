# ROADMAP

## Phase 1 — 로컬 RAG 프로토타입 (1주)

**목표:** 단일 머신에서 동작하는 RAG API

### 기술
- FastAPI, Pydantic v2
- ChromaDB (로컬 영속화)
- OpenAI Embeddings (text-embedding-3-small)
- OpenAI Chat (gpt-4o-mini)
- pytest

### 작업
- [ ] 프로젝트 구조 + 가상환경
- [ ] 마크다운 로더 (디렉토리 재귀)
- [ ] 청킹 (RecursiveCharacterTextSplitter)
- [ ] 임베딩 + Chroma 저장
- [ ] FastAPI 엔드포인트
  - `POST /ingest` — 문서 인덱싱
  - `POST /query` — 질의응답 (출처 인용 포함)
- [ ] pytest 단위 + 통합 테스트
- [ ] .env 관리 (pydantic-settings)

### 완료 기준
- 로컬에서 본인 노트 폴더 인덱싱
- 질의 응답이 출처 파일명 + 관련 청크 인용
- 테스트 커버리지 70%+

---

## Phase 2 — 컨테이너화 + CI (1주)

**목표:** 어디서든 같은 환경으로 동작

### 기술
- Docker (multi-stage build)
- docker-compose
- GitHub Actions

### 작업
- [ ] Dockerfile (slim 이미지, non-root 사용자)
- [ ] docker-compose.yml (app + Chroma + Redis)
- [ ] .dockerignore
- [ ] GitHub Actions: lint → test → build
- [ ] 이미지 레지스트리 푸시 (GHCR or ECR)
- [ ] 헬스체크 엔드포인트

### 완료 기준
- `docker compose up` 한 번에 전체 스택 기동
- main 브랜치 푸시 시 CI 자동 실행
- 컨테이너 이미지가 레지스트리에 자동 푸시됨

---

## Phase 3 — AWS 배포 + IaC (1~2주)

**목표:** 프로덕션 수준 클라우드 배포

### 기술
- Terraform
- AWS ECS Fargate, ECR, S3, RDS PostgreSQL, ElastiCache Redis, ALB, Route53, IAM, Secrets Manager

### 작업
- [ ] Terraform 모듈 구조 (network, compute, storage, observability)
- [ ] VPC + 서브넷 (public/private 분리)
- [ ] ECR 리포지토리 + 이미지 푸시
- [ ] ECS Cluster + Fargate Task Definition
- [ ] ALB + HTTPS (ACM 인증서)
- [ ] RDS PostgreSQL (메타데이터)
- [ ] ElastiCache Redis (쿼리 캐싱)
- [ ] S3 (원본 문서 저장)
- [ ] Secrets Manager (OpenAI API key 등)
- [ ] IAM 역할 분리 (least privilege)

### 완료 기준
- `terraform apply` 한 번으로 전체 인프라 생성
- 도메인으로 HTTPS 접근
- 비용 월 $20 이하

---

## Phase 4 — 운영/관측 (1주)

**목표:** 운영 가능한 상태로 만들기

### 기술
- CloudWatch (Logs, Metrics, Alarms)
- AWS Budgets
- Locust (부하 테스트)

### 작업
- [ ] 구조화 로깅 (JSON, request_id 포함)
- [ ] 핵심 메트릭 대시보드
  - 요청 수, 에러율, p50/p95/p99 레이턴시
  - 임베딩 생성 시간, OpenAI API 호출 횟수
- [ ] 알람 (에러율 5%↑, p95 레이턴시 2s↑)
- [ ] AWS Budgets ($30/월 알림)
- [ ] Locust로 부하 테스트 → 병목 발견 → 1개 이상 개선

### 완료 기준
- 대시보드에서 시스템 상태 한눈에 파악
- 부하 테스트 결과 + 개선 전후 비교 문서화

---

## Phase 5 (선택) — Kubernetes 마이그레이션 (1~2주)

**목표:** 쿠버네티스 운영 경험

### 기술
- AWS EKS, Helm, ArgoCD, Prometheus, Grafana

### 작업
- [ ] EKS 클러스터 (Terraform)
- [ ] Helm Chart 작성
- [ ] HPA (CPU/메모리 기반)
- [ ] ArgoCD 설치 + GitOps 파이프라인
- [ ] Prometheus + Grafana
- [ ] ECS → EKS로 트래픽 마이그레이션

### 완료 기준
- GitOps로 배포 (커밋 → 자동 반영)
- HPA 동작 확인 (부하에 따라 파드 증감)
- Grafana 대시보드 운영

---

## 진행 원칙

1. **각 Phase 완료 시 회고** — `OBSERVATIONS.md`에 기록
2. **Phase 시작 전 계획 점검** — Codex 교차 검증 활용 (`/xflow`)
3. **모든 변경은 PR 단위** — 작은 PR, 빠른 머지
4. **비용 모니터링** — AWS Budgets 알림 설정 후 시작
