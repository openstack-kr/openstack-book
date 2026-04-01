# OpenStack Korea Community Book

OpenInfra Korea User Group과 **아주대학교 소학회 아올다**([aoldacloud.com](http://aoldacloud.com/))가 함께 만드는 오픈스택 학습 자료입니다.

Quarto를 이용해 작성하며, GitHub Actions를 통해 [book.openinfra-kr.org](https://book.openinfra-kr.org)에 자동 배포됩니다.

## 프로젝트 구조

```
.
├── _quarto.yml          # Quarto 설정 파일
├── index.qmd            # 메인 페이지
├── custom.scss          # 커스텀 스타일
├── _footer.html         # 공통 푸터
├── lectures/            # 강의 자료
└── .github/workflows/
    └── publish.yml      # GitHub Actions 배포 워크플로우
```

> `docs/`는 빌드 결과물로 git에서 제외됩니다. GitHub Actions가 자동으로 빌드 후 `gh-pages` 브랜치에 배포합니다.

## 로컬 개발 환경 설정

### Quarto 설치

```bash
# macOS
brew install quarto

# Windows
choco install quarto

# Linux
wget https://github.com/quarto-dev/quarto-cli/releases/latest/download/quarto-linux-amd64.deb
sudo dpkg -i quarto-linux-amd64.deb
```

### 로컬 프리뷰

```bash
quarto preview
```

### 빌드

```bash
quarto render
```

## 기여 방법

### 강의 자료 추가

1. `lectures/` 아래에 `.qmd` 파일 생성

```markdown
---
title: "페이지 제목"
---

# 내용 작성
```

2. `_quarto.yml`의 `sidebar.contents`에 항목 추가

```yaml
- text: "새 강의 제목"
  file: lectures/new_lec.qmd
```

3. PR 생성 → 머지되면 자동 배포

### 이미지 파일

이미지는 해당 강의 디렉토리의 `images/` 폴더에 저장하고 상대 경로로 참조합니다.

## 배포

`main` 브랜치에 push하면 GitHub Actions가 자동으로 빌드 후 `gh-pages` 브랜치에 배포합니다.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.