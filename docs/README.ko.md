# authorkit

[English](../README.md) | [中文](README.zh.md) | [日本語](README.ja.md) | [Русский](README.ru.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Español](README.es.md) | [Português](README.pt.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | [Italiano](README.it.md)

**Claude Code를 위한 책 집필 워크플로우 스킬.**

레퍼런스 분석, 원고 퇴고, 도해 제작, 문체/용어 검증, 구조 재배치 등 책 집필의 반복 작업을 체계화합니다.

## 스킬 목록

| 스킬 | 설명 |
|------|------|
| `init` | 프로젝트 초기 설정 (질문지 md → 세팅) |
| `analyze` | 레퍼런스/원고 분석 |
| `compare` | 레퍼런스 ↔ 원고 대조 |
| `draft` | 절 단위 집필/퇴고 (old → new) |
| `diagram` | 텍스트 블록도 제작 |
| `review` | 문체/용어/구조 검증 |
| `restructure` | 구조 재배치 |

## 설치

```
/plugin marketplace add Nowzero/authorkit
/plugin install authorkit-ko@authorkit
```

영어 버전:
```
/plugin install authorkit@authorkit
```

## 시작하기

```
/authorkit.init
```

질문지 md 파일이 생성됩니다. IDE에서 답변을 작성한 뒤 다시 실행하면 세팅 완료.

## 지원 파일 형식

- 레퍼런스: pdf, docx, txt, xlsx, hwpx
- 원고: pdf, docx, txt, xlsx, hwpx, md
- 출력: md (텍스트 블록도 포함)

## 워크플로우

```
/authorkit.init          프로젝트 설정
       ↓
/authorkit.analyze       레퍼런스/원고 분석
       ↓
/authorkit.compare       레퍼런스 ↔ 원고 대조
       ↓
/authorkit.draft         절 단위 집필/퇴고 (old → new)
       ↓
/authorkit.diagram       텍스트 블록도 제작
       ↓
/authorkit.review        문체/용어/상호참조 검증
       ↓
/authorkit.restructure   챕터/절 순서 재배치
```

## 라이선스

MIT
