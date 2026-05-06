# Python Asyncio 정리

## 핵심 개념

Asyncio는 단일 스레드에서 협력적 멀티태스킹으로 I/O-bound 작업을 효율적으로 처리한다.
이벤트 루프가 코루틴들을 스케줄링하며, `await` 지점에서 다른 코루틴으로 제어가 넘어간다.

## async/await

`async def`로 정의된 함수는 코루틴 객체를 반환한다.
이 객체는 `await`되거나 `asyncio.run()`을 통해 실행되어야 한다.

```python
async def fetch(url):
    response = await client.get(url)
    return response.json()
```

## 동시 실행

여러 코루틴을 병렬로 실행하려면 `asyncio.gather()`를 사용한다.

```python
results = await asyncio.gather(
    fetch("https://api.example.com/a"),
    fetch("https://api.example.com/b"),
)
```

## 주의사항

- CPU-bound 작업에는 부적합. `ProcessPoolExecutor`를 고려.
- 동기 함수를 코루틴 안에서 호출하면 이벤트 루프를 블록한다. `asyncio.to_thread()` 사용.
- 예외는 코루틴이 await될 때까지 발생하지 않는다.
