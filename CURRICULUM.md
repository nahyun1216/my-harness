# Harness Engineering 101 — 5주 커리큘럼 (평일 1시간 × 25회)

- 교재: <https://isuruwijesiri.com/harness-engineering-101/> (온라인으로 읽는 게 제일 편함)
- 원본 코드: `../harness-engineering-101/src/harness/` (수정하지 말고 참고만)
- 내 코드: 이 폴더(`my-harness/`). 실습 코드는 **Claude가 작성**하고, 나는 읽고·실행하고·관찰 질문에 답하는 방식
  (아래 표의 "실습 과제"는 Claude에게 "N회차 실습 코드 만들어줘"라고 하면 됨)
- 기간: 2026-10-27(화) ~ 2026-11-30(월). 밀리면 날짜만 뒤로 미루면 됨

## 매 회차 1시간 루틴

| 시간 | 할 일 |
|---|---|
| 0–25분 | 해당 장 읽기. "무엇이 고장 났고 → 최소 패치는 뭐고 → 그 비용은?" 3줄로 정리 |
| 25–55분 | 실습: Claude가 만든 코드를 원본과 diff로 비교 → 실행 → 관찰 질문에 답하기 |
| 55–60분 | `notes/DD-제목.md`에 3줄 요약 + 막힌 점 기록, `git commit` |

실행: `./run.sh v1` (원본 실행), `./run.sh my_v1.py` (내 코드 실행). 디버깅은 `HARNESS_DEBUG=1 ./run.sh full`.

---

## 1주차 — Part I. The Wire (아무것도 마법이 아니다)

| 회 | 날짜 | 읽기 | 실습 과제 | 완료 |
|---|---|---|---|---|
| 1 | 10/27 화 | 1장 It's Just a JSON Array | `./check.sh`로 키 확인 → `./run.sh v1` 실행 → `my_v1.py` 직접 작성. 매 턴 `messages` 배열을 `json.dumps(indent=2)`로 출력해보기 | [x] |
| 2 | 10/28 수 | 2장 The Brain | 같은 질문을 system 프롬프트만 바꿔 3번 보내고 차이 기록. 응답의 `usage`(input/output 토큰) 출력 추가 | [x] 10/29 |
| 3 | 10/29 목 | 3장 Tools | `./run.sh v2` 실행 → `my_v2.py`에 도구 2개(`read_file`, `list_dir`) 직접 추가. 에러를 모델에게 되돌려주기 | [ ] |
| 4 | 10/30 금 | 4장 The Agent Loop | `my_v3.py`: `stop_reason == "tool_use"`인 동안 도는 루프. 최대 반복 횟수 가드 추가 | [ ] |
| 5 | 11/2 월 | 5장 Caching | `cache_control` 넣고 `cache_read_input_tokens` 비교. system/tools 순서를 바꾸면 캐시가 깨지는지 실험 | [ ] |

## 2주차 — Part II. Running Long (압박받는 배열)

| 회 | 날짜 | 읽기 | 실습 과제 | 완료 |
|---|---|---|---|---|
| 6 | 11/3 화 | 6장 Context Is a Budget | 도구 출력 truncate 함수 작성 (앞뒤만 남기기). 배열 전체 토큰 추정치 출력 | [ ] |
| 7 | 11/4 수 | 6장 복습 실습 | 대화가 길어지면 오래된 턴을 요약해 교체하는 compaction 구현 | [ ] |
| 8 | 11/5 목 | 7장 Subagents | `./run.sh v4` 실행 → 내 하네스에 `agent` 도구 추가 (새 배열로 fork, 결과만 반환) | [ ] |
| 9 | 11/6 금 | 8장 Steering | 루프 도중 `<system-reminder>`를 tool_result 옆에 끼워 넣는 `remind()` 구현 | [ ] |
| 10 | 11/9 월 | 9장 Background Work | 오래 걸리는 명령을 스레드로 돌리고, 끝나면 리마인더로 알려주기 | [ ] |

## 3주차 — Part III. The Ecosystem (이미 아는 것에 이름 붙이기)

| 회 | 날짜 | 읽기 | 실습 과제 | 완료 |
|---|---|---|---|---|
| 11 | 11/10 화 | 10장 Frameworks Are Wrappers | `call_llm`만 Anthropic Python SDK로 바꿔보기 (`uv venv && uv pip install anthropic`). 바뀐 게 얼마나 적은지 확인 | [ ] |
| 12 | 11/11 수 | 11장 Extending the Body (MCP, Skills) | `skills/` 폴더의 md 파일을 이름·설명만 먼저 주고, 필요할 때 본문을 로드하는 deferred loading 구현 | [ ] |
| 13 | 11/12 목 | 11장 (Hooks) | 도구 실행 전/후 훅(`pre_tool`, `post_tool`) 구현. 예: 모든 bash 명령 로그 남기기 | [ ] |
| 14 | 11/13 금 | 12장 Debugging the Array | 매 요청 배열을 `sessions/*.jsonl`로 덤프 → 턴별로 보기 좋게 출력하는 뷰어 스크립트 | [ ] |
| 15 | 11/16 월 | 복습 | 지금 쓰는 Claude Code 기능(CLAUDE.md, hooks, subagent, skills, plan mode)이 몇 장의 어떤 패턴인지 표로 매핑 → `notes/claude-code-map.md` | [ ] |

## 4주차 — Part IV. Trust, Domains, Data + 에필로그

| 회 | 날짜 | 읽기 | 실습 과제 | 완료 |
|---|---|---|---|---|
| 16 | 11/17 화 | 13장 Reflexes and Guardrails | 위험한 명령(`rm`, `sudo`, `push`…) 실행 전 y/n 확인하는 `gate()` | [ ] |
| 17 | 11/18 수 | 13장 실습 | "읽지 않은 파일은 수정 금지" 가드 (파일 mtime 추적) | [ ] |
| 18 | 11/19 목 | 14장 Coding Agents | `edit_file(path, old, new)` 도구: old가 정확히 1번 나올 때만 치환 | [ ] |
| 19 | 11/20 금 | 15장 RAG | grep 기반 `search` 도구로 사내 문서/코드 폴더를 검색하게 해보기 | [ ] |
| 20 | 11/23 월 | 16장 Build Your Own | 원본 `harness.py`(약 300줄) 정독 → 내 하네스와 diff, 빠진 기능 목록화 | [ ] |

## 5주차 — 부록 + 최종 프로젝트

| 회 | 날짜 | 읽기 | 실습 과제 | 완료 |
|---|---|---|---|---|
| 21 | 11/24 화 | 부록 A One Harness, Many Brains | 서브에이전트는 Haiku, 메인은 Sonnet으로 라우팅. 비용 비교 | [ ] |
| 22 | 11/25 수 | 부록 D Retries, Rate Limits, Streaming | 429/529 지수 백오프 재시도 + 스트리밍 출력 (`./run.sh d` 참고) | [ ] |
| 23 | 11/26 목 | 부록 B Worktrees, 부록 C Plan Mode | 읽기 전용 "plan 모드" 토글 (쓰기 도구를 배열에서 빼기) | [ ] |
| 24 | 11/27 금 | — | **최종 프로젝트 설계**: 회사 업무에서 반복되는 작업 하나를 골라 전용 에이전트 설계 (도구 목록, 가드레일, 컨텍스트 전략) | [ ] |
| 25 | 11/30 월 | — | **최종 프로젝트 구현 + 회고**. `notes/retro.md`에 5주간 배운 것 정리 | [ ] |

---

### 막혔을 때
- 원본 코드: `../harness-engineering-101/src/harness/` (v1→v2→v3→v4→harness.py 순서로 진화)
- 같이 보면 좋은 글: Thorsten Ball, [How to Build an Agent](https://ampcode.com/notes/how-to-build-an-agent)
- 원본 `MODEL = "claude-sonnet-5"`가 404(모델 없음)를 내면 그 줄을 `claude-sonnet-5-5`로 바꿔서 실행
