#!/usr/bin/env bash
# 환경 점검: 파이썬 버전 + API 키 + 실제 1회 호출
HERE="$(cd "$(dirname "$0")" && pwd)"
[ -f "$HERE/.env" ] && set -a && . "$HERE/.env" && set +a
python3 -c 'import sys; assert sys.version_info >= (3,10); print("python OK", sys.version.split()[0])'
[ -n "${ANTHROPIC_API_KEY:-}" ] || { echo "ANTHROPIC_API_KEY 없음 -> .env 확인"; exit 1; }
curl -s https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" -H "anthropic-version: 2023-06-01" -H "content-type: application/json" \
  -d "{\"model\":\"${HARNESS_MODEL:-claude-sonnet-5-5}\",\"max_tokens\":20,\"messages\":[{\"role\":\"user\",\"content\":\"say hi\"}]}"
echo
