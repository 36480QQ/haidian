#!/usr/bin/env bash
# ============================================================
# 上传 AI 设计提交包到 fork (Lyz30/haidian) main 分支，更新 PR #1639
# 用法: bash upload-to-github.sh
# 前置: gh 已登录（gh auth status 通过）
# ============================================================
set -euo pipefail

REPO="Lyz30/haidian"
BRANCH="main"
DEST="submissions/Lyz30/ai-innovation-spine"
SRC="/d/haidian-ai-design"
MSG="fix(ai-innovation-spine): resolve submission validation errors"

gh auth status >/dev/null 2>&1 || { echo "请先运行: gh auth login"; exit 1; }

cd "$SRC"
echo "=== 上传 $REPO:$BRANCH/$DEST ==="

count=0
while IFS= read -r f; do
  rel="${f#./}"
  api_path="$DEST/$rel"

  # 取远端 sha（已存在则更新，不存在则创建）
  existing_sha=$(gh api "repos/$REPO/contents/$api_path?ref=$BRANCH" --jq '.sha' 2>/dev/null || echo "")

  if [ -n "$existing_sha" ]; then
    gh api --method PUT "repos/$REPO/contents/$api_path" \
      -f message="$MSG" \
      -f content="$(base64 -w0 "$rel")" \
      -f sha="$existing_sha" \
      -f branch="$BRANCH" >/dev/null 2>&1 \
      && echo "UPDATE $rel" || echo "FAIL   $rel"
  else
    gh api --method PUT "repos/$REPO/contents/$api_path" \
      -f message="$MSG" \
      -f content="$(base64 -w0 "$rel")" \
      -f branch="$BRANCH" >/dev/null 2>&1 \
      && echo "CREATE $rel" || echo "FAIL   $rel"
  fi
  count=$((count+1))
done < <(find . -type f | sort)

echo "=== 完成，共处理 $count 个文件 ==="
