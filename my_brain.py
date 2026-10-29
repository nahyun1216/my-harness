#!/usr/bin/env python3
"""my_brain: 2장 실습. 같은 질문을 "배열 바깥 설정"만 바꿔 보내고 차이를 본다.

my_v1.py 의 call_llm 을 그대로 쓰되, system 과 temperature 를 인자로 받게만 바꿈.
대화 루프 없음: 질문 1개 -> 실험 5번 -> 결과 출력.

  실험 A~C: system 프롬프트만 다름       -> "역할은 훈련된 행동" (규칙 3)
  실험 D~E: 같은 입력, temperature 0 vs 1 -> "고르는 건 모델 밖" (규칙 1)

실행: ./run.sh my_brain.py ["다른 질문"]
"""
import json
import os
import sys
import urllib.error
import urllib.request

API_KEY = os.environ["ANTHROPIC_API_KEY"]
MODEL = os.environ.get("HARNESS_MODEL", "claude-sonnet-5-5")
QUESTION = sys.argv[1] if len(sys.argv) > 1 else "하네스(harness)가 뭐야? 두 문장으로."

EXPERIMENTS = [                     # (이름, system, temperature)
    ("A 기본",   "You are a concise assistant.",                     None),
    ("B 해적",   "You are a pirate. Always talk like a pirate.",     None),
    ("C 거부",   "Never explain anything. Reply only with 'No.'",    None),
    ("D temp=0", "You are a concise assistant.",                     0),
    ("E temp=1", "You are a concise assistant.",                     1),
]


def call_llm(messages, system, temperature=None):          # CHANGED: 인자 2개
    body = {"model": MODEL, "max_tokens": 300,
            "system": system, "messages": messages}
    if temperature is not None:
        body["temperature"] = temperature                  # NEW: 요청마다 보내는 설정
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(body).encode(),
        headers={"content-type": "application/json",
                 "x-api-key": API_KEY,
                 "anthropic-version": "2023-06-01"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def main():
    messages = [{"role": "user", "content": QUESTION}]     # 배열은 5번 모두 똑같음
    print(f"model={MODEL}\nQ: {QUESTION}")
    for name, system, temp in EXPERIMENTS:
        try:
            reply = call_llm(messages, system, temp)
        except urllib.error.HTTPError as e:
            print(f"\n--- {name}: HTTP {e.code} {e.read().decode()[:200]}")
            continue
        text = "".join(b["text"] for b in reply["content"] if b["type"] == "text")
        u = reply["usage"]
        print(f"\n--- {name}  [system={system!r}]")
        print(text)
        print(f"  [in={u['input_tokens']} out={u['output_tokens']} "
              f"stop={reply['stop_reason']}]")


if __name__ == "__main__":
    main()
