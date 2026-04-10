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
  - ch6 강의 문서를 처음 다룰 때, frontmatter에 `code:` 필드가 없으면 **가장 먼저** 사용자에게 어떤 섹션 코드로 묶을지 질문한다.  
    - 예: `"이 문서를 ch6 몇 번 코드로 묶을까요? (예: 6-1, 6-12, 6-15 중 하나)"`  
    - 사용자가 선택/응답한 코드를 `code: "6-12"` 처럼 frontmatter에 추가한 뒤, 이후 그림/표 번호 계산에 사용한다.
    - ch6에서는 보통 이 `code` 값을 **제목(title) 앞에 붙여서** 사용한다.  
      - 예: `title: "6-12 SNAT, DNAT 개념 정리"` 처럼 `6-12`를 제목에 포함.
  - 강의 본문(qmd)에는 필요하다면 마지막에 `# 참조` 섹션을 추가하고, 참조 링크를 다음 형식으로 정리해 둔다.
    - `# 참조` 아래에 한 줄씩  
      `[# 이 링크가 무엇을 설명하는지 한글로 요약](https://example.com/doc)`  
      같은 형태로 **설명 + 하이퍼링크**를 쓴다.
    - 예: `neutron_agents.qmd`에서는  
      `[Red Hat OpenStack Platform Neutron 설정 문서](https://docs.redhat.com/ko/documentation/red_hat_openstack_platform/16.2/html/configuration_reference/neutron_2)`  
      처럼, 공식 문서가 무엇을 다루는지 한글로 설명을 붙여 준다.
  - 강의 본문 헤딩(`#`, `##`, `###`) 번호는 **변환 직후 반드시 확인**한다. 특히 ch6 문서는 다음 규칙을 기본값으로 삼는다.
    - 섹션 코드는 **frontmatter의 `code:` 필드**와 **제목(title)** 에 우선 반영한다.
      - 예: `code: "6-12"`, `title: "6-12. SNAT/DNAT란?"`
    - ch6의 **주요 본문 섹션**은 plain heading으로 두지 말고, `# [6-12-1] ...`, `# [6-12-2] ...` 같은 **번호형 H1**으로 맞춘다.
      - 예: `# [6-2-1] 해당 개념들이 생기게 된 이유`
      - 예: `# [6-2-5] 트래픽 흐름 3가지로 이해하기`
    - 번호형 H1 아래의 하위 설명은 필요에 따라 일반 `##`/`###` 헤딩으로 둘 수 있다.
      - 예: `## 테넌트 내부 통신(East-West)`
      - 예: `## VM이 외부로 나감(Egress, 보통 SNAT)`
    - 변환 후에는 최소한 아래를 **무조건 점검**한다.
      - `code:` 값과 제목의 장/절 번호가 서로 일치하는지
      - 본문 주요 섹션 번호가 `[6-2-1]`, `[6-2-2]`처럼 **순서대로 이어지는지**
      - plain `# 제목`이 남아 있지 않은지
      - 새로 끼어든 섹션이 있으면 뒤 번호까지 함께 밀어서 renumber 되었는지
    - 일반적인 장/절 구조(코드 필드가 없는 다른 장)에서는 기존처럼 `## 2.2.5 VM NIC 3개 구성 및 정적 IP 설정` 형태를 사용할 수 있다.
  - 그림/표 번호는 **가장 가까운 번호형 섹션 헤딩 전체**를 기준으로 계산한다.
    - 예: `# [6-2-4] 전체 레이어` 아래 첫 그림이면 `그림 6-2-4-1`
    - 예: `# [6-12-3] 두 가지 전통적인 NAT 방식` 아래 첫 그림이면 `그림 6-12-3-1`
    - 섹션 번호가 바뀌면 그 아래 그림/표 번호도 **같이 renumber** 되었는지 반드시 확인한다.
  - 그림을 추가/정리할 때는 다음 형태를 기본으로 사용한다.
    - `![그림 6-12-3-1. NAPT 동작 원리](images/snat_dnat/image.png){width="55%" fig-align="left"}`
      → **번호 + 한 줄 설명 + 파일명 + 왼쪽 정렬**이 한 번에 정리되도록 돕는다.
  - 코드 블록(```` ``` ````) 언어 태그를 실제 내용과 맞춰 정리한다.
    - 사용자가 `@파일경로 (21-26)`처럼 특정 범위를 가리킬 때, 그 범위가 **명령어**인지 **설정 파일**인지 보고 언어를 결정한다.
      - 리눅스/셸 명령어(`sudo apt ...`, `sudo ovs-vsctl ...`, `openstack server ...` 등)인 경우 → ` ```bash ` 로 맞춘다.
      - ini 형식 설정(`foo = bar`가 연속)인 경우 → ` ```ini ` 또는 맥락에 맞는 형식으로 태그한다.
      - YAML/JSON 등은 해당 포맷에 맞게 ` ```yaml `, ` ```json `을 사용한다.
    - Notion에서 가져온 코드 블록이 언어 없이 내려왔거나 잘못 태그된 경우, **실제 내용에 맞게 언어를 고쳐 주는 것**이 에이전트의 기본 후처리 작업이다.
    - 예: `@lectures/ch6/ovs_vxlan_vpn.qmd (21-26)` 구간은 OVS 설치 명령이므로, 아래처럼 정리한다.
      - 잘못된 예:  
        - ` ``` ` (언어 없음)
      - 정리 후:  
        - ` ```bash`  
          `sudo apt update`  
          `sudo apt install -y openvswitch-switch`  
          `sudo systemctl status openvswitch-switch`  
          ` ````
  - 코드 블록인데 실제로는 **그림/다이어그램을 글로 그려 놓은 경우**도 올바르게 정리한다.
    - 예: 패킷 흐름, 토폴로지, 구성 요소 관계 등을 `|-`, `+`, `->` 같은 문자로 그려 놓은 ASCII 다이어그램.
    - 이런 블록은 실행 가능한 코드가 아니므로, 다음 중 하나로 정리한다.
      - **우선순위 1:** `lectures/{chapter}/images/{slug}/` 아래에 **실제 그림 파일(svg/png 등)** 로 만들고, 본문에서는 다른 문서와 동일하게 `![그림 6-2-5-1. ...](images/{slug}/diagram.svg)` 형태로 넣는다.
      - **우선순위 2:** 설명 위주라면 일반 본문/리스트/표로 풀어서 재작성한다.
      - **마지막 fallback:** 그대로 둘 필요가 있을 때만 언어 태그를 `text` 또는 비워 두어, ` ```text` 처럼 “코드가 아닌 텍스트 블록”임을 드러낸다.
      - 즉, 기존 강의처럼 렌더 결과에 **정식 figcaption** 이 보이게 하려면, 가능한 한 텍스트 블록 대신 실제 이미지 파일로 바꿔 넣는 것을 기본값으로 삼는다.
    - 셸/프로그래밍 언어로 잘못 태그된 ASCII 다이어그램은, 반드시 `text`/무태그로 바꾸거나 일반 문단으로 풀어서 정리한다.

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
