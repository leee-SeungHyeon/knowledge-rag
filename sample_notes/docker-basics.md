# Docker 기초

## 컨테이너 vs VM

VM은 하이퍼바이저 위에서 게스트 OS 전체를 실행하지만, 컨테이너는 호스트 커널을 공유하면서
프로세스 격리만 한다. 그래서 컨테이너는 시작이 빠르고 자원 효율이 높다.

## Dockerfile 핵심

레이어 캐싱을 최대한 활용하려면 자주 바뀌지 않는 명령을 위쪽에 배치한다.

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen
COPY . .
CMD ["python", "-m", "app.main"]
```

의존성 설치를 코드 복사보다 먼저 하면 코드만 바뀌어도 의존성 레이어는 재사용된다.

## Multi-stage Build

빌드 도구는 빌더 이미지에서만 사용하고, 최종 이미지는 런타임만 포함시켜 크기를 줄인다.

```dockerfile
FROM python:3.12 AS builder
RUN pip install --target=/deps fastapi

FROM python:3.12-slim
COPY --from=builder /deps /usr/lib/python3.12/site-packages
```

## 보안

- root 사용자 대신 별도 user 생성 (`USER appuser`)
- `.dockerignore`로 비밀 파일 제외 (`.env`, `.git`)
- 베이스 이미지를 정기적으로 업데이트
