#!/usr/bin/env python3
"""my_v2: 3장 실습. 원본 v2_tools.py + 관찰 장치.

원본과 다른 점:
  - 도구: run_command 대신 list_dir (셸 전체 대신 "폴더 보기"만 허용)
  - [tool] 줄에 모델이 보낸 tool_use JSON 과 돌려준 tool_result 앞부분을 출력
  - 두 번째 응답이 또 도구를 원하면 "[버려짐]" 표시 (원본은 조용히 버림 -> 4장)
  - API 에러가 나면 죽지 않고 에러 본문을 출력 (/show 로 배열 확인 가능)

실행: ./run.sh my_v2.py      명령: /show /quit
"""
import json
import os
import urllib.error
import urllib.request

API_KEY = os.environ["ANTHROPIC_API_KEY"]
MODEL = os.environ.get("HARNESS_MODEL", "claude-sonnet-5-5")
SYSTEM = "You are a concise assistant with access to the local machine."

TOOLS = [                                            # 메뉴: 모델이 보는 건 이게 전부
    {"name": "read_file",
     "description": "Read a text file and return its contents.",
     "input_schema": {"type": "object",
                      "properties": {"path": {"type": "string"}},
                      "required": ["path"]}},
    {"name": "list_dir",                             # CHANGED: run_command 대신
     "description": "List entries in a directory with their sizes in bytes.",
     "input_schema": {"type": "object",
                      "properties": {"path": {"type": "string"}},
                      "required": ["path"]}},
]


def call_llm(messages):
    body = {"model": MODEL, "max_tokens": 4096, "system": SYSTEM,
            "messages": messages, "tools": TOOLS}
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(body).encode(),
        headers={"content-type": "application/json",
                 "x-api-key": API_KEY,
                 "anthropic-version": "2023-06-01"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def execute_tool(name, args):                        # 디스패치: 이름 -> 함수
    try:
        if name == "read_file":
            return open(args["path"]).read()
        if name == "list_dir":                       # NEW
            p = args["path"]
            return "\n".join(f"{os.path.getsize(os.path.join(p, n)):>8}  {n}"
                             for n in sorted(os.listdir(p)))
        return f"ERROR: unknown tool {name}"
    except Exception as e:
        return f"ERROR: {e}"                         # 에러도 결과로 모델에게


def show(reply):
    """텍스트는 출력, tool_use 블록은 목록으로 돌려줌."""
    uses = []
    for b in reply["content"]:
        if b["type"] == "text":
            print(f"\nassistant> {b['text']}")
        elif b["type"] == "tool_use":
            uses.append(b)
    return uses


def main():
    print(f"model={MODEL}  (명령: /show /quit)")
    messages = []
    while True:
        user_text = input("\nyou> ").strip()
        if user_text in ("/quit", ""):
            break
        if user_text == "/show":
            print(json.dumps(messages, indent=2, ensure_ascii=False))
            continue
        messages.append({"role": "user", "content": user_text})
        try:
            reply = call_llm(messages)
        except urllib.error.HTTPError as e:          # NEW: 죽지 말고 보여주기
            print(f"\n[API ERROR {e.code}] {e.read().decode()}")
            messages.pop()
            continue
        messages.append({"role": "assistant", "content": reply["content"]})

        for block in show(reply)[:1]:                # 원본처럼 딱 한 번만
            print(f"\n[tool_use]    {json.dumps(block, ensure_ascii=False)}")
            result = execute_tool(block["name"], block["input"])
            print(f"[tool_result] {result[:200]!r}{' ...' if len(result) > 200 else ''}")
            messages.append({"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": block["id"],
                 "content": result}]})
            reply2 = call_llm(messages)
            messages.append({"role": "assistant", "content": reply2["content"]})
            for b2 in show(reply2):                  # NEW: 버려지는 요청 표시
                print(f"\n[버려짐] 모델이 또 {b2['name']}({json.dumps(b2['input'])}) "
                      f"를 원했지만 v2는 한 번만 실행함 -> 4장")


if __name__ == "__main__":
    main()
