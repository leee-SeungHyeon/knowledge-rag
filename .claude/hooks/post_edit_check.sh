#!/usr/bin/env bash
# PostToolUse hook: run ruff + pytest after Write/Edit/MultiEdit on app/** or tests/**.
# Exit 0 → silent pass. Exit 2 → block & send stderr back to Claude as feedback.
set -u

PROJECT_ROOT="/Users/lllsh/Developer/personal/knowledge-rag"

# Read hook payload from stdin
input="$(cat)"

# Extract file_path using python (jq not available)
file_path="$(printf '%s' "$input" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    ti = data.get('tool_input', {}) or {}
    print(ti.get('file_path', ''))
except Exception:
    print('')
")"

# Only act on app/** or tests/** Python files
case "$file_path" in
  "$PROJECT_ROOT"/app/*.py|"$PROJECT_ROOT"/tests/*.py) ;;
  *) exit 0 ;;
esac

cd "$PROJECT_ROOT" || exit 0

ruff_out="$(.venv/bin/ruff check app tests 2>&1)"
ruff_status=$?

pytest_out="$(.venv/bin/pytest -q tests 2>&1)"
pytest_status=$?

if [ $ruff_status -eq 0 ] && [ $pytest_status -eq 0 ]; then
  exit 0
fi

{
  echo "[post_edit_check] failures detected after editing: $file_path"
  if [ $ruff_status -ne 0 ]; then
    echo "--- ruff ---"
    echo "$ruff_out"
  fi
  if [ $pytest_status -ne 0 ]; then
    echo "--- pytest ---"
    echo "$pytest_out" | tail -40
  fi
} >&2
exit 2
