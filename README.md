# knowledge-rag

개인 노트(마크다운)를 인덱싱하고 자연어로 질의응답하는 RAG 시스템.  
로컬 프로토타입에서 시작해 AWS 클라우드 배포 + Kubernetes 운영까지 단계적으로 진화시키는 학습 프로젝트.

## 목적

1. RAG 시스템 전체 파이프라인 실전 경험
2. AWS 클라우드 인프라 설계 및 운영 경험
3. Claude Code 하네스 엔지니어링 실험 환경

## 로드맵

자세한 내용은 [ROADMAP.md](./ROADMAP.md) 참고.

| Phase | 내용 | 기간 |
|-------|------|------|
| 1 | 로컬 RAG 프로토타입 (FastAPI + Chroma) | 1주 |
| 2 | 컨테이너화 + CI (Docker, GitHub Actions) | 1주 |
| 3 | AWS 배포 + IaC (ECS, S3, Terraform) | 1~2주 |
| 4 | 운영/관측 (CloudWatch, 부하 테스트) | 1주 |
| 5 | (선택) K8s 마이그레이션 (EKS, Helm) | 1~2주 |

## 기술 스택 (계획)

- Python 3.12+, FastAPI, Pydantic
- LangChain, ChromaDB, OpenAI Embeddings
- Docker, GitHub Actions
- AWS (ECS Fargate, S3, RDS, ElastiCache, CloudWatch)
- Terraform
- (선택) Kubernetes, Helm, Prometheus, Grafana

## 디렉토리 구조 (계획)

```
knowledge-rag/
├── app/              # FastAPI 애플리케이션
├── tests/            # pytest 테스트
├── infra/            # Terraform IaC
├── docker/           # Dockerfile, docker-compose
├── .github/          # CI/CD 워크플로우
├── ROADMAP.md
├── OBSERVATIONS.md   # 하네스 개선용 관찰 기록
└── README.md
```
