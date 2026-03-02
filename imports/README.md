# imports/

노션에서 내보낸 ZIP 파일을 넣는 폴더. **lectures/ 와 동일한 챕터 구조**를 사용합니다.

## 폴더 구조

```
imports/
├── ch1/     ← 1장용 ZIP
├── ch2/     ← 2장용 ZIP
├── ch3/
├── ch4/
├── ch5/
└── ch6/     ← 6장 Neutron (Provider/Tenant, SNAT/DNAT 등)
    ├── SNAT, DNAT 개념.zip
    └── provider_network.zip
```

## 사용법

1. 노션에서 **내보내기** → **Markdown & CSV** 선택
2. 다운로드한 ZIP을 해당 챕터 폴더에 복사 (예: `imports/ch6/`)
3. 스크립트 실행:

```bash
cd scripts
python3 import_notion_zip.py "SNAT, DNAT 개념.zip" ch6 snat_dnat
```

파일명만 입력하면 `imports/{챕터}/` 에서 자동으로 찾습니다.
