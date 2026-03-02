# 노션 ZIP → Quarto QMD 변환

노션 내보내기 ZIP을 Quarto 프로젝트 구조에 맞게 변환합니다.

## 기본 루트 구조

```
openstack-book/
├── imports/          ← ZIP (lectures와 동일한 챕터 구조)
│   ├── ch1/
│   ├── ch2/
│   └── ch6/          ← 6장용 ZIP
├── scripts/          ← 여기서 실행
└── lectures/         ← 변환 결과
```

## 사용법

```bash
cd openstack-book/scripts
python3 import_notion_zip.py <zip파일> <챕터> [글슬러그]
```

**ZIP**: `imports/{챕터}/` 에 넣고 **파일명만** 입력
- `imports/ch6/SNAT, DNAT 개념.zip` → `"SNAT, DNAT 개념.zip" ch6`
- 다른 경로는 절대/상대 경로로 지정 가능

**챕터**: ch1~ch6
- ch6: 6장. Neutron (네트워킹 개념 등)

예: `python3 import_notion_zip.py "SNAT, DNAT 개념.zip" ch6 snat_dnat`

새 글이 지정한 챕터 **하위**에만 추가됩니다.

## 폴더 구조 (변환 후)

```
lectures/{챕터}/
├── images/{글슬러그}/   ← 이미지
└── {글슬러그}.qmd      ← 문서
```
