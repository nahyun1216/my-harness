#!/usr/bin/env bash
# my-harness 를 회사 GitHub(nahyunkim1) + 개인 GitHub 두 곳에 올리도록 설정.
# 여러 번 실행해도 안전함(이미 된 단계는 건너뜀).
#
# 실행: cd ~/harness/my-harness && bash setup-git-remotes.sh
set -euo pipefail

COMPANY_USER="nahyunkim1"
REPO="my-harness"
KEY=~/.ssh/id_ed25519_personal
cd "$(dirname "$0")"

read -rp "개인 GitHub 아이디를 입력하세요: " PERSONAL_USER
[ -n "$PERSONAL_USER" ] || { echo "아이디가 비어 있음"; exit 1; }

echo
echo "=== [1/5] 개인 계정용 SSH 키 ==="
if [ -e "$KEY" ]; then
  echo "이미 있음: $KEY"
else
  ssh-keygen -t ed25519 -C "chtlaalways@gmail.com" -f "$KEY" -N "" -q
  echo "생성함: $KEY"
fi

echo
echo "=== [2/5] ~/.ssh/config 에 github-personal 별칭 ==="
if grep -q "^Host github-personal" ~/.ssh/config 2>/dev/null; then
  echo "이미 있음"
else
  cp ~/.ssh/config ~/.ssh/config.bak 2>/dev/null || true
  cat >> ~/.ssh/config <<'EOF'

# 개인 GitHub 계정 (git@github-personal:<user>/<repo>.git)
Host github-personal
    Hostname ssh.github.com
    Port 443
    User git
    IdentityFile ~/.ssh/id_ed25519_personal
    IdentitiesOnly yes
EOF
  echo "추가함 (백업: ~/.ssh/config.bak)"
fi

echo
echo "=== [3/5] 웹에서 할 일 ==="
echo "아래 공개키 한 줄을 복사해서 '개인' GitHub > Settings > SSH and GPG keys > New SSH key 에 등록:"
echo
cat "$KEY.pub"
echo
echo "그리고 빈 저장소 2개 만들기 (README 체크 X):"
echo "  - 회사: https://github.com/new  (nahyunkim1 로그인, 이름 $REPO, Private)"
echo "  - 개인: https://github.com/new  ($PERSONAL_USER 로그인, 이름 $REPO)"
read -rp "다 했으면 Enter..."

echo
echo "=== [4/5] 접속 테스트 ==="
for host in github.com github-personal; do
  if ! ssh -T "git@$host" 2>&1 | grep -o "Hi [^!]*"; then
    echo "$host 접속 실패 -> [3/5] 키 등록을 확인하고 다시 실행하세요"; exit 1
  fi
done

echo
echo "=== [5/5] 원격 등록 + push ==="
BRANCH=$(git branch --show-current)
COMPANY_URL="git@github.com:$COMPANY_USER/$REPO.git"
PERSONAL_URL="git@github-personal:$PERSONAL_USER/$REPO.git"

git remote remove company  2>/dev/null || true
git remote remove personal 2>/dev/null || true
git remote remove origin   2>/dev/null || true
git remote add company  "$COMPANY_URL"
git remote add personal "$PERSONAL_URL"
# origin = push 할 때 두 곳에 동시에 올라가는 원격
git remote add origin "$COMPANY_URL"
git remote set-url --add --push origin "$COMPANY_URL"
git remote set-url --add --push origin "$PERSONAL_URL"

git push -u origin "$BRANCH"
echo
git remote -v
echo
echo "완료! 앞으로는 'git push' 한 번이면 회사/개인 둘 다 올라감."
