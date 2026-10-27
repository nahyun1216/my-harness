#!/usr/bin/env python3
"""my_v1: 1장 실습용 채팅 하네스 (원본 v1_chat.py + 관찰 장치).

원본과 다른 점:
  - 모델을 HARNESS_MODEL 환경변수로 고름
  - /show  : 지금 모델에게 보내는 배열 전체를 출력
  - /forget: 마지막 한 턴(질문+답)을 배열에서 지움 -> 모델이 정말로 "잊는지" 확인
  - 매 턴 input_tokens 를 출력 -> 배열 전체를 다시 보낸다는 걸 숫자로 확인

실행: ./run.sh my_v1.py
"""
import json
import os
import urllib.request

API_KEY = os.environ["ANTHROPIC_API_KEY"]
MODEL = os.environ.get("HARNESS_MODEL", "claude-sonnet-5-5")
SYSTEM = os.environ.get("HARNESS_SYSTEM", "You are a concise assistant.")


def call_llm(messages):
    body = {"model": MODEL, "max_tokens": 4096,
            "system": SYSTEM, "messages": messages}
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(body).encode(),
        headers={"content-type": "application/json",
                 "x-api-key": API_KEY,
                 "anthropic-version": "2023-06-01"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def main():
    print(f"model={MODEL}  (명령: /show /forget /clear /quit)")
    messages = []                                   # 이게 "세션"의 전부
    while True:
        user_text = input("\nyou> ").strip()
        if user_text in ("/quit", ""):
            break
        if user_text == "/clear":
            messages = []                           # "새 대화" = 빈 배열
            continue
        if user_text == "/show":
            print(json.dumps({"system": SYSTEM, "messages": messages},
                             indent=2, ensure_ascii=False))
            continue
        if user_text == "/forget":
            messages = messages[:-2]                # 마지막 user+assistant 제거
            print(f"(배열 길이 -> {len(messages)})")
            continue
        messages.append({"role": "user", "content": user_text})
        reply = call_llm(messages)                  # 매번 전부 다시 보냄
        text = "".join(b["text"] for b in reply["content"]
                       if b["type"] == "text")
        messages.append({"role": "assistant", "content": reply["content"]})
        u = reply["usage"]
        print(f"\nassistant> {text}")
        print(f"  [in={u['input_tokens']} out={u['output_tokens']} "
              f"배열 길이={len(messages)}]")


if __name__ == "__main__":
    main()
