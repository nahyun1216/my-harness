# my-harness

[Harness Engineering 101](https://isuruwijesiri.com/harness-engineering-101/)을 5주(평일 1시간 × 25회) 동안 공부하면서 만드는 실습 저장소.

> **하네스(harness)** = LLM을 감싸서 실제로 일하게 만드는 프로그램.
> 대화 배열을 만들고, 도구를 실행하고, 안전을 지킨다. 모델은 "다음 토큰 확률표"만 만들 뿐, 나머지는 전부 하네스의 일이다.

```
[내 노트북]                                [Anthropic 데이터센터]
 하네스 (이 저장소의 my_*.py)  ──HTTP──▶    serving layer
   - 배열 만들기                              ├─ 모델: 확률표 계산
   - 도구 실행                                └─ 토큰 고르기, 반복
                              ◀──JSON──
```

## 진행 상황

| 회 | 진행일 | 장 | 실습 코드 | 노트 |
|---|---|---|---|---|
| 1 | 2026-10-27 (화) | 1장 It's Just a JSON Array | [`my_v1.py`](my_v1.py) | [01-json-array](notes/01-json-array.md) |
| 2 | 2026-10-29 (목) | 2장 The Brain | [`my_brain.py`](my_brain.py) | [02-the-brain](notes/02-the-brain.md) |
| 3 | 2026-10-29 (목) ~ 10-30 (금) | 3장 Tools | [`my_v2.py`](my_v2.py) | [03-tools](notes/03-tools.md) |

전체 일정과 회차별 과제: [CURRICULUM.md](CURRICULUM.md)

## 폴더 구조

```
my-harness/
├── CURRICULUM.md   # 5주 커리큘럼 (25회차, 날짜, 실습 과제, 완료 체크)
├── my_*.py         # 회차별 실습 코드 (원본 대비 바뀐 부분에 주석)
├── notes/          # 회차별 노트: 3줄 요약 · 쉬운 정리 · 내 질문 Q&A · 오답노트
├── run.sh          # .env 를 읽어 원본/내 코드 실행
├── check.sh        # 파이썬 버전 + API 키 + 1회 호출 점검
└── .env.example    # API 키 템플릿 (.env 는 커밋하지 않음)
```

원본 코드는 옆 폴더 `../harness-engineering-101/src/harness/` 에 클론해 두고 참고만 한다 ([원본 저장소](https://github.com/IsuruMaduranga/harness-engineering-101)).

## 실행

```bash
cp .env.example .env        # ANTHROPIC_API_KEY 입력
./check.sh                  # 환경 점검

./run.sh v1                 # 원본 실행 (v1 | v2 | v3 | v4 | full | d)
./run.sh my_v1.py           # 내 코드 실행
```

모델은 `HARNESS_MODEL` 환경변수로 바꿀 수 있다 (기본 `claude-sonnet-5-5`).

## 공부 방식

매 회차 1시간: **읽기(25분) → 실습 코드 diff·실행·관찰 질문(30분) → 노트 정리·커밋(5분)**.
노트의 관찰 질문은 "내 답 → 보충" 형식으로 적어서 오답노트로 쓴다.
