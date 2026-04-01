#!/bin/bash
# 노션 ZIP → QMD 변환 래퍼
# 사용법: ./import_notion.sh <zip경로> <챕터> [글슬러그]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
python3 import_notion_zip.py "$@"
