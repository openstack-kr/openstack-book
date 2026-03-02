# 노션 글 가져오기

노션에 써둔 글을 이 사이트에 넣을 때 사용하는 도구입니다.

---

## 3단계로 끝내기

### 1단계: 노션에서 내보내기

1. 노션 페이지 오른쪽 상단 **`•••`** 클릭
2. **내보내기** → **Markdown & CSV** 선택
3. **내보내기** 클릭 → ZIP 다운로드

### 2단계: ZIP 파일 넣기

다운로드한 ZIP을 **해당 챕터 폴더**에 복사합니다.

```
imports/
├── ch1/     ← 1장용
├── ch2/     ← 2장용
├── ch3/
├── ch4/
├── ch5/
└── ch6/     ← 6장 Neutron (네트워킹 개념 등)
```

예: 6장에 넣을 글이면 `imports/ch6/` 폴더에 ZIP 복사

### 3단계: 스크립트 실행

```bash
cd openstack-book/scripts
python3 import_notion_zip.py "ZIP파일명.zip" ch6 글슬러그 --title "사이드바에 표시할 제목"
```

**실제 예시**:

```bash
# SNAT/DNAT 글
python3 import_notion_zip.py "SNAT, DNAT 개념.zip" ch6 snat_dnat --title "SNAT/DNAT 개념"

# Provider/Tenant 글
python3 import_notion_zip.py "provider network와 tenant network 개념 정리.zip" ch6 provider_tenant --title "Provider/Tenant Network 개념"
```

끝이에요. 그러면 `lectures/ch6/` 에 문서가 생성되고, 사이드바/목차에도 자동으로 들어갑니다.

---

## 인자 설명

| 입력 | 필수 | 설명 |
|------|:----:|------|
| ZIP파일명 | O | `imports/ch6/` 에 넣은 파일 이름 그대로 (예: `"SNAT, DNAT 개념.zip"`) |
| 챕터 | O | ch1, ch2, ch3, ch4, ch5, ch6 |
| 글슬러그 | △ | 파일명 (생략 시 자동). 예: `snat_dnat` |
| --title | △ | 사이드바에 보일 제목 |

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
