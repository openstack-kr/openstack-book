# OpenStack 실습 데모 페이지 with Quarto

Quarto를 이용한 OpenStack Korea Community 의 Book 컨텐츠 프로젝트입니다.

## Quarto를 이용한 Book 프로젝트 구조

```
.
├── _quarto.yml     # Quarto 설정 파일
├── index.qmd       # 메인 페이지
├── lectures/       # 강의 자료
│   ├── short_lec.qmd   # 단편 강의자료
│   ├──  long_lec/       # 장편 강의자료
│   │  └── long_lec1.qmd # 장편 강의자료 속편
│   └── long_lec.qmd    # 장편 강의자료 메인페이지 (소개, 속편 링크 가이드)
├── community.qmd   # 커뮤니티 페이지
├── styles.css      # 커스텀 스타일
└── docs/          # 빌드된 사이트 (자동 생성)
```

## 기여 시작하기

1. Quarto 설치

```
# macOS
brew install quarto

# Windows
choco install quarto

# Linux
wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.6.0/quarto-1.6.0-linux-amd64.deb
sudo dpkg -i quarto-1.6.0-linux-amd64.deb
```

## 강의 및 실습 가이드 기여 방법

### Github Issue 생성

1. .qmd 파일 생성하기

```
---
title: "페이지 제목"
---

# 내용 작성
```

2. `_quarto.yml`에 네비게이션 추가

```
website:
  navbar:
    left:
      - text: "새 메뉴"
        file: path/to/new.qmd
```


### 강의 자료 추가

1. PDF 파일을 `media/pdf/` 디렉토리에 저장
2. `lectures/<lecutre>.qmd`에 링크 추가

## 사이트 빌드 및 배포

### 로컬 프리뷰

```
quarto preview
```

### 사이트 빌드

```
quarto render
```

빌드된 파일은 `docs/` 디렉토리에 생성됩니다.

### GitHub Pages 배포

1. `docs/` 디렉토리를 Git에 커밋
2. GitHub 저장소 설정에서 GitHub Pages 소스를 `docs/` 폴더로 설정

## 다국어 지원

한글 콘텐츠 작성을 위해 `_quarto.yml`에 다음 설정이 되어있습니다:

```
format:
  html:
    lang: ko
```


## 문서 스타일 가이드

- 제목은 `#`부터 시작
- 코드 블록은 ``` 사용
- 이미지는 `images/` 디렉토리에 저장
- 링크는 상대 경로 사용

## 도움말

- [Quarto 공식 문서](https://quarto.org/docs/guide/)
- [GitHub Discussions](https://github.com/openstack-kr/community-site/discussions)
- [Slack 채널](https://openstack-kr.slack.com)

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.