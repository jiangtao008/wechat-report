#!/usr/bin/env bash
# generate-index.sh — 扫描 group-* 目录下的所有 .html 文件，生成 index.json
# 用法：bash generate-index.sh [项目根目录]
# 默认根目录为脚本所在目录

set -euo pipefail

ROOT="${1:-$(cd "$(dirname "$0")" && pwd)}"
cd "$ROOT"

OUTPUT="$ROOT/index.json"

echo "🔍 扫描 $ROOT/group-* 目录下的 HTML 报告..."

# Build JSON
json='{\n  "updated": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'",\n  "groups": ['

first_group=true
for group_dir in $(ls -d group-*/ 2>/dev/null | sort -V); do
  group_name="${group_dir%/}"

  html_files=()
  while IFS= read -r -d '' f; do
    html_files+=("$f")
  done < <(find "$group_dir" -maxdepth 1 -name "*.html" -print0 | sort -z)

  [[ ${#html_files[@]} -eq 0 ]] && continue

  $first_group && first_group=false || json+=","
  json+='\n    {'
  json+='\n      "name": "'"$group_name"'",'
  json+='\n      "files": ['

  first_file=true
  for f in "${html_files[@]}"; do
    basename_f=$(basename "$f")
    relpath="${group_name}/${basename_f}"

    # 从文件名推断标题：去掉 _YYYYMMDD.html 或 .html 后缀
    title="${basename_f%.html}"
    title="${title%_群聊周报}"
    title="${title%_周报}"
    title="${title%_日报}"
    title="${title%_月报}"
    title="${title%_202[0-9]*}"  # strip date suffix like _20260729
    title="${title%%_20[0-9][0-9][0-9][0-9]}"

    $first_file && first_file=false || json+=","
    json+='\n        {'
    json+='\n          "title": "'"$title"'",'
    json+='\n          "file": "'"$relpath"'",'
    json+='\n          "meta": "'"$group_name"' · '"$basename_f"'"'
    json+='\n        }'
  done

  json+='\n      ]'
  json+='\n    }'
done

json+='\n  ]\n}'

echo -e "$json" > "$OUTPUT"
echo "✅ 已生成 $OUTPUT"
echo "   共收录 $(grep -c '"file"' "$OUTPUT" || true) 个报告"
