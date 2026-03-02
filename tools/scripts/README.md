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
  - 강의 본문(qmd)에는 필요하다면 마지막에 `# 참조` 섹션을 추가하고, 참조 링크를 다음 형식으로 정리해 둔다.
    - `# 참조` 아래에 한 줄씩  
      `[# 이 링크가 무엇을 설명하는지 한글로 요약](https://example.com/doc)`  
      같은 형태로 **설명 + 하이퍼링크**를 쓴다.
    - 예: `neutron_agents.qmd`에서는  
      `[Red Hat OpenStack Platform Neutron 설정 문서](https://docs.redhat.com/ko/documentation/red_hat_openstack_platform/16.2/html/configuration_reference/neutron_2)`  
      처럼, 공식 문서가 무엇을 다루는지 한글로 설명을 붙여 준다.
  - 강의 본문 헤딩(`#`, `##`, `###`)에는 가능하면 **섹션 코드/번호**를 붙인다.  
    - 일반적인 장/절 구조: `## 2.2.5 VM NIC 3개 구성 및 정적 IP 설정`
    - ch6처럼 코드 매핑이 있는 경우: `## 6-1 neutron agent 종류 정리`, `## 6-12 SNAT / DNAT 개념` 처럼 `6-번호` 형식을 사용한다.
    - 번호가 누락된 경우, 에이전트는 상위 헤딩 구조와 순서를 기준으로 번호를 **추론**만 하고, 실제 헤딩 텍스트 수정은 PR/리뷰에서 사람과 함께 확정하는 것을 권장한다.
  - 그림/표 번호는 이 헤딩/코드(예: `6-12`)를 기준으로 `그림 6-12-1`, `표 6-12-1` 처럼 계산한다.
  - 그림을 추가/정리할 때는 다음 형태를 기본으로 사용한다.  
    - `![그림 6-12-1. SNAT/DNAT 예시 흐름](images/ch6/snat_dnat_1.png){width="55%" fig-align="left"}`  
      → **번호 + 한 줄 설명 + 파일명 + 왼쪽 정렬**이 한 번에 정리되도록 돕는다.

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
