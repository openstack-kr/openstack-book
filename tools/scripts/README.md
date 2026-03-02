# 노션 글 가져오기

노션에 써둔 글을 이 사이트에 넣을 때 사용하는 도구입니다.

- 이 파일(`scripts/README.md`)은 **사용법 설명만** 수정합니다.
- 실제 동작은 `import_notion_zip.py`가 담당하므로, 코드를 바꾸기 전에는 **이 README의 I/O 요약을 먼저** 확인하세요.

---

## 3단계로 끝내기

### 1단계: 노션에서 내보내기

1. 노션 페이지 오른쪽 상단 **`•••`** 클릭
2. **내보내기** → **Markdown & CSV** 선택
3. **내보내기** 클릭 → ZIP 다운로드

### 2단계: ZIP 파일 넣기

다운로드한 ZIP을 **해당 챕터 폴더**에 복사합니다.

```
tools/imports/
├── ch1/     ← 1장용
├── ch2/     ← 2장용
├── ch3/
├── ch4/
├── ch5/
└── ch6/     ← 6장 Neutron (네트워킹 개념 등)
```

예: 6장에 넣을 글이면 `tools/imports/ch6/` 폴더에 ZIP 복사

### 3단계: 스크립트 실행

```bash
cd openstack-book/tools/scripts
python3 import_notion_zip.py "ZIP파일명.zip" ch6 글슬러그 --title "사이드바에 표시할 제목"
```

**실제 예시**:

```bash
# SNAT/DNAT 글
python3 import_notion_zip.py "SNAT, DNAT 개념.zip" ch6 snat_dnat --title "SNAT/DNAT 개념"
```

끝이에요. 그러면 `lectures/ch6/` 에 문서가 생성되고, 사이드바/목차에도 자동으로 들어갑니다.

---

## 인자 설명

| 입력 | 필수 | 설명 |
|------|:----:|------|
| ZIP파일명 | O | `tools/imports/ch6/` 에 넣은 파일 이름 그대로 (예: `"SNAT, DNAT 개념.zip"`) |
| 챕터 | O | ch1, ch2, ch3, ch4, ch5, ch6 |
| 글슬러그 | △ | 파일명 (생략 시 자동). 예: `snat_dnat` |
| --title | △ | 사이드바에 보일 제목 |

---

## 스크립트 I/O 요약 (에이전트용)

- **입력**
  - ZIP 파일: `tools/imports/{chapter}/*.zip`
  - 명령:  
    `python3 import_notion_zip.py <zip파일> <chapter> [slug] [--title]`
- **출력**
  - 문서: `lectures/{chapter}/{slug}.qmd`
  - 이미지: `lectures/{chapter}/images/{slug}/*`
  - 네비게이션 업데이트: `_quarto.yml`, `lectures/index.qmd`에 항목 추가
  - ZIP 정리: 사용이 끝난 ZIP은 `tools/imports/{chapter}/processed/` 로 이동

- **ZIP 처리 규칙 (중요)**
  - 처리 대상 ZIP은 **항상** `tools/imports/{chapter}/`에서만 찾고, `tools/imports/{chapter}/processed/`는 **검색/실행 대상에 포함하지 않는다.**
  - `tools/imports/{chapter}/processed/` 안의 ZIP 파일은 `import_notion_zip.py`로 **이미 반영이 끝난 파일**이므로, 다시 변환 대상으로 사용하지 않는다.

- **에이전트 후속 작업 체크리스트**
  - 새로 생성된 문서/이미지 경로를 사용자에게 요약해서 알려준다.
  - 해당 챕터에 `lectures/ch{N}_lec.qmd` 같은 **챕터 소개 문서**가 있는 경우:
    - 그 문서에 `## 하위 목차` 섹션이 있으면, 방금 생성한 글을 하위 목차에 **추가할지 사용자에게 묻거나, 사용자가 원하면 직접 추가**한다.
    - 예: `ch6`인 경우 `lectures/ch6_lec.qmd`의 하위 목차에 `lectures/ch6/{slug}.qmd` 링크를 맞춰 준다.

---

## 챕터가 뭔가요?

| 챕터 | 해당 장 |
|------|---------|
| ch1 | 1장. 오픈스택 개요 |
| ch2 | 2장. 오픈스택 설치 해보기 |
| ch3 | 3장. Keystone |
| ch4 | 4장. Nova |
| ch5 | 5장. Glance |
| ch6 | 6장. Neutron (네트워킹 개념) |

---

## 결과물

```
lectures/ch6/
├── images/
│   └── snat_dnat/     ← 이미지들
│       ├── image.png
│       └── image 1.png
└── snat_dnat.qmd      ← 변환된 문서
```

이미지 경로, 사이트 네비게이션, 목차는 모두 자동으로 처리됩니다.
