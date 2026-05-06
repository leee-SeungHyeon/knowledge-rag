# AWS ECS vs EKS 비교

## ECS (Elastic Container Service)

AWS 자체 컨테이너 오케스트레이터. AWS 생태계 통합이 깊고, 학습 곡선이 낮다.

- **Fargate**: 서버리스 컨테이너. 노드 관리 불필요, 사용한 만큼 과금.
- **EC2 모드**: EC2 인스턴스에 직접 띄움. 비용은 더 저렴할 수 있으나 관리 부담.

작은 팀이나 AWS 종속을 감수할 수 있다면 ECS Fargate가 가장 빠른 출시 경로.

## EKS (Elastic Kubernetes Service)

매니지드 Kubernetes. 컨트롤 플레인은 AWS가 관리하고, 워커 노드는 사용자가 관리(또는 Fargate).

- 표준 K8s API 사용 가능 → 멀티 클라우드 이식성
- 풍부한 오픈소스 생태계 (Helm, ArgoCD, Istio 등)
- 학습 곡선 가파름. 운영 인력 필요.

## 선택 기준

| 상황 | 추천 |
|------|------|
| 빠른 출시, 팀 작음 | ECS Fargate |
| 멀티 클라우드 고려 | EKS |
| K8s 생태계 도구 활용 | EKS |
| AWS만 쓰며 단순함 우선 | ECS |

## 비용

ECS Fargate는 컨테이너 단위 과금. EKS는 컨트롤 플레인 시간당 $0.10 추가.
소규모에선 ECS가 저렴, 대규모 워크로드에선 EKS + 노드 그룹이 유리할 수 있다.
