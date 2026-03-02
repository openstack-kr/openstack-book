#!/usr/bin/env python3
"""
노션 ZIP 내보내기 → Quarto QMD 변환 스크립트

사용법:
  python import_notion_zip.py <zip파일> <챕터> [글슬러그]

ZIP 위치: tools/imports/ 가 lectures/ 와 동일한 챕터 구조
  tools/imports/ch6/SNAT, DNAT 개념.zip → ch6 에 넣을 때: "SNAT, DNAT 개념.zip" ch6
  - 파일명만 입력 시 tools/imports/{챕터}/ 에서 찾음
  - 절대/상대 경로로 직접 지정도 가능

챕터: ch1~ch6
예시:
  python import_notion_zip.py "SNAT, DNAT 개념.zip" ch6 snat_dnat
"""

import argparse
import os
import re
import shutil
import zipfile
from pathlib import Path
from urllib.parse import unquote


IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'}

# 프로젝트 루트 기준 경로 (스크립트는 tools/scripts/ 에 있음)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
IMPORTS_DIR = PROJECT_ROOT / 'tools' / 'imports'  # ZIP 파일 기본 위치


def find_images_for_md(md_path: Path, md_content: str, article_slug: str) -> tuple[list[Path], dict[str, str]]:
    """md에서 참조하는 이미지 찾기. 반환: (파일 목록, {원본경로: 새경로} 매핑)"""
    root = md_path.parent
    found_files = []
    path_mapping = {}

    for alt, src in re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', md_content):
        src = src.strip()
        if not src or src.startswith(('http://', 'https://', 'data:')):
            continue
        src_decoded = unquote(src)
        src_path = root / src_decoded.replace('/', os.sep)
        if src_path.exists():
            found_files.append(src_path)
            new_rel = f"images/{article_slug}/{src_path.name}"
            path_mapping[src] = new_rel
            path_mapping[src_decoded] = new_rel

    page_base = re.sub(r'\s+[a-f0-9]{32}$', '', md_path.stem, flags=re.I).strip()
    for folder in root.iterdir():
        if folder.is_dir() and len(page_base) > 3 and (page_base[:20] in folder.name or folder.name in page_base):
            for img in folder.iterdir():
                if img.suffix.lower() in IMAGE_EXTENSIONS:
                    found_files.append(img)
                    rel = f"{folder.name}/{img.name}"
                    path_mapping[rel] = f"images/{article_slug}/{img.name}"
                    path_mapping[f"{folder.name}/{img.name}"] = f"images/{article_slug}/{img.name}"

    return list(set(found_files)), path_mapping


def slugify(name: str) -> str:
    name = re.sub(r'\s+[a-f0-9]{32}$', '', name, flags=re.I)
    slug = re.sub(r'[^\w\s가-힣-]', '', name)
    slug = re.sub(r'[\s,]+', '_', slug).strip('_').lower()
    return slug or 'article'


# 챕터 → index.qmd N장 패턴 매핑
CHAPTER_PATTERNS = {
    'ch1': r'1장',
    'ch2': r'2장',
    'ch3': r'3장',
    'ch4': r'4장',
    'ch5': r'5장',
    'ch6': r'6장',
}


def _update_index_qmd(lectures_dir: Path, chapter: str, article_slug: str, title: str):
    """index.qmd에 지정 챕터 하위로 링크 추가 (top-level 아님)"""
    index_path = lectures_dir / 'index.qmd'
    if not index_path.exists() or f'{chapter}/{article_slug}.qmd' in index_path.read_text():
        return

    pattern = CHAPTER_PATTERNS.get(chapter, chapter.replace('ch', '') + '장')
    lines = index_path.read_text(encoding='utf-8').split('\n')
    new_line = f'  - [{title}]({chapter}/{article_slug}.qmd)'

    insert_idx = None
    base_indent = None
    for i, line in enumerate(lines):
        if pattern in line and re.search(r'\[.*?장\.', line):
            base_indent = len(line) - len(line.lstrip())
            insert_idx = i + 1
            while insert_idx < len(lines):
                next_line = lines[insert_idx]
                next_indent = len(next_line) - len(next_line.lstrip()) if next_line.strip() else 0
                if next_line.strip() and next_indent <= base_indent:
                    break
                insert_idx += 1
            break

    if insert_idx is not None:
        lines.insert(insert_idx, new_line)
        index_path.write_text('\n'.join(lines), encoding='utf-8')
        print("등록됨: lectures/index.qmd")


def _update_quarto_yml(base_dir: Path, chapter: str, article_slug: str, title: str):
    """_quarto.yml에 지정 챕터 섹션 하위로 항목 추가"""
    quarto_yml = base_dir / '_quarto.yml'
    if not quarto_yml.exists():
        return
    yml_text = quarto_yml.read_text(encoding='utf-8')
    if f'lectures/{chapter}/{article_slug}.qmd' in yml_text:
        return

    new_entry = f'            - text: "{title}"\n              file: lectures/{chapter}/{article_slug}.qmd\n'
    pattern = CHAPTER_PATTERNS.get(chapter, chapter.replace('ch', '') + '장')

    # 6장 등 section이 있는 경우: 해당 section의 contents 끝에 추가
    section_re = re.search(
        rf'(- section: ".*{pattern}.*"\s*\n\s*contents:\s*\n)(.*?)(?=\n\s*format:|\n\s{{8}}-(?:\s+section:|\s+text:))',
        yml_text, re.DOTALL
    )
    if section_re:
        prefix, section_body = section_re.group(1), section_re.group(2)
        yml_text = yml_text.replace(
            section_re.group(0),
            prefix + section_body.rstrip() + '\n' + new_entry
        )
    else:
        yml_text = yml_text.replace('\nformat:', '\n' + new_entry + '\nformat:')

    quarto_yml.write_text(yml_text, encoding='utf-8')
    print("등록됨: _quarto.yml")


def add_yaml_frontmatter(content: str, title: str, description: str = '') -> str:
    lines = content.strip().split('\n')
    start = 0
    for i, line in enumerate(lines):
        if re.match(r'^(범주|시리즈|작성시간|참여자):', line.strip()):
            continue
        if line.strip().startswith('# ') or line.strip():
            start = i
            break

    body_lines = [l for l in lines[start:] if not re.match(r'^(범주|시리즈|작성시간|참여자):', l.strip())]
    body = '\n'.join(body_lines).strip()
    doc_title = re.search(r'^#\s+(.+)$', body, re.M)
    doc_title = doc_title.group(1).strip() if doc_title else title

    return f'''---
title: "{doc_title}"
description: "{description or doc_title}"
---

''' + body


def main():
    parser = argparse.ArgumentParser(description='노션 ZIP → Quarto QMD 변환')
    parser.add_argument('zip_path', help='노션 내보내기 ZIP 파일 경로')
    parser.add_argument('chapter', help='챕터 폴더명 (예: ch2, ch3, networking)')
    parser.add_argument('slug', nargs='?', help='글 슬러그 (생략시 md 파일명에서 추출)')
    parser.add_argument('--title', help='사이드바에 표시할 제목')
    parser.add_argument('--no-register', action='store_true', help='_quarto.yml 자동 등록 안 함')
    parser.add_argument('--dry-run', action='store_true', help='실제 파일 생성 없이 확인만')
    args = parser.parse_args()

    base_dir = PROJECT_ROOT
    lectures_dir = base_dir / 'lectures'
    chapter = args.chapter.strip().lower().replace(' ', '_')

    # ZIP 경로: 파일명만이면 tools/imports/{챕터}/ 에서 찾음 (lectures 구조와 동일)
    zip_arg = args.zip_path.strip()
    if '/' not in zip_arg and '\\' not in zip_arg:
        zip_path = IMPORTS_DIR / chapter / zip_arg
    elif zip_arg.startswith('tools/imports/') or zip_arg.startswith('tools\\imports\\'):
        zip_path = PROJECT_ROOT / zip_arg.replace('\\', '/')
    else:
        zip_path = Path(zip_arg).resolve()

    if not zip_path.exists():
            imports_chapter = IMPORTS_DIR / chapter
        if '/' not in zip_arg and '\\' not in zip_arg and not imports_chapter.exists():
            imports_chapter.mkdir(parents=True)
            print(f"tools/imports/{chapter}/ 폴더를 생성했습니다. ZIP 파일을 넣어주세요: {imports_chapter}")
        print(f"오류: ZIP 파일을 찾을 수 없습니다: {zip_path}")
        return 1
    chapter_dir = lectures_dir / chapter
    chapter_dir.mkdir(parents=True, exist_ok=True)
    (IMPORTS_DIR / chapter).mkdir(parents=True, exist_ok=True)
    chapter_dir.mkdir(parents=True, exist_ok=True)

    extract_root = base_dir / '.tmp_extract' / zip_path.stem
    extract_root.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            for name in zf.namelist():
                try:
                    zf.extract(name, extract_root)
                except Exception:
                    pass
        for nested in extract_root.rglob('*.zip'):
            with zipfile.ZipFile(nested, 'r') as zf:
                for name in zf.namelist():
                    try:
                        zf.extract(name, nested.parent)
                    except Exception:
                        pass
            nested.unlink()

        md_files = list(extract_root.rglob('*.md'))
        if not md_files:
            print("오류: ZIP 내에 .md 파일을 찾을 수 없습니다.")
            return 1

        md_path = md_files[0]
        slug = args.slug or slugify(md_path.stem)
        article_slug = slug

        md_content = md_path.read_text(encoding='utf-8', errors='replace')
        found_images, path_mapping = find_images_for_md(md_path, md_content, article_slug)

        images_dir = chapter_dir / 'images' / article_slug
        if not args.dry_run:
            images_dir.mkdir(parents=True, exist_ok=True)
            for img_path in found_images:
                shutil.copy2(img_path, images_dir / img_path.name)

        new_content = md_content
        for old_path in sorted(path_mapping.keys(), key=len, reverse=True):
            new_rel = path_mapping[old_path]
            new_content = new_content.replace(f']({old_path})', f']({new_rel})')
            new_content = new_content.replace(f'="{old_path}"', f'="{new_rel}"')

        title_from_doc = re.search(r'^#\s+(.+)$', md_content, re.M)
        doc_title = title_from_doc.group(1).strip() if title_from_doc else md_path.stem
        qmd_content = add_yaml_frontmatter(new_content, doc_title)
        qmd_path = chapter_dir / f'{article_slug}.qmd'

        if args.dry_run:
            print(f"[DRY-RUN] 생성될 파일:")
            print(f"  - {qmd_path.relative_to(base_dir)}")
            print(f"  - {images_dir.relative_to(base_dir)}/ ({len(found_images)}개 이미지)")
            return 0

        qmd_path.write_text(qmd_content, encoding='utf-8')
        print(f"생성됨: {qmd_path.relative_to(base_dir)}")
        print(f"이미지: {images_dir.relative_to(base_dir)}/ ({len(found_images)}개)")

        if not args.no_register:
            _update_quarto_yml(base_dir, chapter, article_slug, args.title or doc_title)
            _update_index_qmd(lectures_dir, chapter, article_slug, args.title or doc_title)

        # 성공적으로 반영된 ZIP은 processed/ 폴더로 이동해 상태를 구분
        processed_dir = IMPORTS_DIR / chapter / "processed"
        processed_dir.mkdir(parents=True, exist_ok=True)
        try:
            new_zip_path = processed_dir / zip_path.name
            if new_zip_path.exists():
                new_zip_path.unlink()
            shutil.move(str(zip_path), str(new_zip_path))
            print(f"ZIP 이동: {zip_path} -> {new_zip_path}")
        except Exception as e:
            print(f"경고: ZIP 이동 중 오류가 발생했지만 변환은 완료되었습니다: {e}")

    finally:
        if extract_root.exists():
            shutil.rmtree(extract_root, ignore_errors=True)

    return 0


if __name__ == '__main__':
    exit(main())
