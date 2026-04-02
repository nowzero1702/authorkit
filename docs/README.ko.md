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
| `juice` | 파일을 마크다운으로 변환 (OCR, 표 추출, 수식 LaTeX, 토큰 절약) |
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
- 출력: md (텍스트 블록도 포함), json (바운딩 박스 포함 구조화 데이터)

## 워크플로우

```
/authorkit.init          프로젝트 설정
       ↓
/authorkit.analyze       레퍼런스/원고 분석
       ↓
/authorkit.compare       레퍼런스 ↔ 원고 대조
       ↓
/authorkit.juice         파일을 마크다운으로 변환 (토큰 절약)
       ↓
/authorkit.draft         절 단위 집필/퇴고 (old → new)
       ↓
/authorkit.diagram       텍스트 블록도 제작
       ↓
/authorkit.review        문체/용어/상호참조 검증
       ↓
/authorkit.restructure   챕터/절 순서 재배치
```

## juice 주요 기능

[opendataloader-pdf](https://github.com/opendataloader-project/opendataloader-pdf)를 참고하여 강화된 기능:

| 기능 | 설명 |
|------|------|
| 하이브리드 처리 | 페이지별 자동 분류 — 단순 텍스트(로컬) vs 스캔/복잡 표(AI 백엔드) |
| 읽기 순서 보정 | XY-Cut 알고리즘으로 다단 레이아웃 텍스트 순서 복원 |
| 고급 표 추출 | 테두리 기반 + 클러스터 기반(테두리 없는 표) 이중 전략 |
| OCR | 스캔 문서 자동 감지 및 텍스트 추출 (80개+ 언어) |
| 수식 추출 | 수학 수식을 LaTeX로 변환 |
| JSON 출력 | 바운딩 박스 + 시맨틱 타입 포함 구조화 데이터 |
| 콘텐츠 안전 | 숨겨진 텍스트 감지, PII 제거 |
| AI 이미지 설명 | 비전 모델로 캡션 없는 이미지에 alt 텍스트 자동 생성 |

## 라이선스

MIT
