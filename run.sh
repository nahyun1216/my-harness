#!/usr/bin/env bash
# .env 를 읽고 파이썬 스크립트 실행.
#   ./run.sh v1                  -> 원본 저장소의 v1_chat.py
#   ./run.sh v3 / v4 / full / d  -> v3_agent / v4_subagents / harness.py / appendix-d
#   ./run.sh my_v1.py            -> 내가 만든 파일
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
UP="$HERE/../harness-engineering-101/src/harness"
[ -f "$HERE/.env" ] && set -a && . "$HERE/.env" && set +a
: "${ANTHROPIC_API_KEY:?.env 에 ANTHROPIC_API_KEY 를 넣어주세요}"
case "${1:-}" in
  v1) f="$UP/v1_chat.py" ;; v2) f="$UP/v2_tools.py" ;; v3) f="$UP/v3_agent.py" ;;
  v4) f="$UP/v4_subagents.py" ;; full) f="$UP/harness.py" ;; d) f="$UP/appendix-d/harness.py" ;;
  "") echo "usage: ./run.sh v1|v2|v3|v4|full|d|<my_file.py> [args]"; exit 1 ;;
  *) f="$1" ;;
esac
shift
exec python3 "$f" "$@"
