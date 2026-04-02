# authorkit 마켓플레이스 배포 가이드라인

## 1. 개요

authorkit은 책 집필을 위한 Claude Code 스킬 플러그인입니다.
이 문서는 authorkit을 Claude Code 플러그인 마켓플레이스에 배포하기 위한
전체 가이드라인을 정리합니다.

---

## 2. 저장소 구조

마켓플레이스 등록을 위해 다음 구조를 **반드시** 따라야 합니다.

```
authorkit/                              ← GitHub 저장소 루트
├── .claude-plugin/
│   └── marketplace.json               ← 마켓플레이스 메타데이터 (필수)
├── README.md                          ← 프로젝트 소개 (필수)
├── LICENSE                            ← MIT (필수)
├── skills/                            ← 스킬 폴더 (필수)
│   ├── init/
│   │   └── SKILL.md
│   ├── analyze/
│   │   └── SKILL.md
│   ├── compare/
│   │   └── SKILL.md
│   ├── draft/
│   │   └── SKILL.md
│   ├── diagram/
│   │   └── SKILL.md
│   ├── review/
│   │   └── SKILL.md
│   └── restructure/
│       └── SKILL.md
└── templates/                         ← 스킬에서 사용하는 리소스
    ├── setup-questionnaire-template.md
    ├── constitution-template.md
    ├── glossary-template.md
    └── structure-template.md
```

### 필수 파일

| 파일 | 역할 | 비고 |
|------|------|------|
| `.claude-plugin/marketplace.json` | 마켓플레이스 메타데이터 | 없으면 마켓플레이스 인식 안 됨 |
| `skills/[name]/SKILL.md` | 각 스킬의 지침 | name + description 프론트매터 필수 |
| `README.md` | 프로젝트 소개 | 스킬 목록, 설치 방법, 사용법 |
| `LICENSE` | 라이선스 | MIT 권장 |

### 선택 파일

| 파일/폴더 | 역할 |
|----------|------|
| `templates/` | init 스킬에서 복사하여 사용하는 템플릿 |
| `skills/[name]/references/` | 스킬에서 참조하는 대용량 문서 |
| `skills/[name]/scripts/` | 스킬에서 사용하는 실행 스크립트 |
| `THIRD_PARTY_NOTICES.md` | 서드파티 라이선스 고지 |

---

## 3. marketplace.json 작성법

### 기본 구조

```json
{
  "name": "authorkit",
  "owner": {
    "name": "소유자 이름",
    "email": "email@example.com",
    "url": "https://github.com/소유자"
  },
  "metadata": {
    "description": "마켓플레이스 설명",
    "version": "1.0.0",
    "license": "MIT"
  },
  "plugins": [
    {
      "name": "플러그인 이름",
      "description": "플러그인 설명",
      "source": "./",
      "strict": false,
      "skills": [
        "./skills/스킬1",
        "./skills/스킬2"
      ]
    }
  ]
}
```

### 필드 상세

| 필드 | 필수 | 설명 |
|------|:----:|------|
| `name` | O | 마켓플레이스 고유 식별자 (소문자, 하이픈) |
| `owner.name` | O | 소유자 이름 |
| `owner.email` | X | 연락처 이메일 |
| `owner.url` | X | GitHub 프로필 URL |
| `metadata.description` | O | 마켓플레이스 설명 |
| `metadata.version` | O | 시맨틱 버전 (예: 1.0.0) |
| `metadata.license` | X | 라이선스 식별자 |
| `plugins[].name` | O | 플러그인 이름 |
| `plugins[].description` | O | 플러그인 설명 (설치 시 표시) |
| `plugins[].source` | O | 소스 경로 (보통 "./") |
| `plugins[].strict` | X | 엄격 모드 (false 권장) |
| `plugins[].skills` | O | 포함된 스킬 경로 배열 |

### 확장 필드 (선택)

```json
{
  "plugins": [
    {
      "version": "1.0.0",
      "author": {
        "name": "작성자",
        "url": "https://github.com/작성자"
      },
      "homepage": "https://github.com/작성자/authorkit",
      "repository": "https://github.com/작성자/authorkit",
      "keywords": ["book", "authoring", "writing", "proofreading"],
      "category": "productivity"
    }
  ]
}
```

---

## 4. SKILL.md 작성법

### 기본 구조

```markdown
---
name: skill-name
description: 스킬 설명. 언제 사용하는지 반드시 포함.
---

# 스킬 제목

[Claude가 따를 지침을 여기에 작성]
```

### 프론트매터 규칙

| 필드 | 필수 | 규칙 |
|------|:----:|------|
| `name` | O | 소문자, 하이픈 구분 (예: `init`, `analyze`) |
| `description` | O | **언제 사용하는지** 반드시 포함 |

### name 명명 규칙

```
✓ init                    (소문자)
✓ analyze                 (소문자)
✓ my-custom-skill         (소문자, 하이픈)
✗ MySkill                 (카멜케이스 금지)
✗ my_skill                (언더스코어 금지)
✗ SKILL                   (대문자 금지)
```

### description 작성 가이드

```
나쁜 예:
"원고 분석 도구"

좋은 예:
"레퍼런스 또는 원고 파일을 분석하여 구조(목차/헤딩), 그림/도표 목록,
핵심 개념/용어, 이슈를 추출합니다. pdf, docx, txt, xlsx, hwpx 형식을
지원합니다. '레퍼런스 분석', '원고 분석', '구조 추출' 등의 요청 시 사용."
```

핵심: **무엇을 하는지** + **언제 트리거되는지** 모두 포함

### 본문 작성 규칙

| 규칙 | 내용 |
|------|------|
| 길이 | 500줄 이하 권장 |
| 큰 문서 | `references/` 폴더로 분리 |
| 코드 | `scripts/` 폴더에 별도 저장 |
| 형식 | 마크다운 |

### 스킬 리소스 분류

```
my-skill/
├── SKILL.md              ← 핵심 지침만 (500줄 이하)
├── scripts/              ← 반복적으로 작성되는 코드
│   ├── process.py
│   └── helper.sh
├── references/           ← 대용량 참고 문서
│   ├── api-docs.md
│   └── schemas.md
└── assets/              ← 출력에 사용될 리소스
    ├── templates/
    └── samples/
```

---

## 5. 배포 절차

### Step 1: GitHub 저장소 생성

```bash
# GitHub에서 저장소 생성 (예: github.com/Nowzero/authorkit)
# 공개(public) 저장소여야 합니다

# 로컬에서
cd authorkit-skills
git init
git add .
git commit -m "Initial release: authorkit v1.0.0"
git remote add origin https://github.com/Nowzero/authorkit-git
git branch -M main
git push -u origin main
```

### Step 2: 마켓플레이스 등록

사용자가 Claude Code에서 실행:

```
/plugin marketplace add Nowzero/authorkit
```

이 명령은:
1. GitHub에서 저장소 정보를 조회
2. `.claude-plugin/marketplace.json` 파일을 읽음
3. 마켓플레이스 메타데이터를 파싱
4. 로컬 캐시에 저장 (`~/.claude/plugins/marketplaces/authorkit/`)
5. 플러그인 브라우저에서 사용 가능하게 표시

### Step 3: 플러그인 설치

방법 1 — 직접 설치:
```
/install nowzero1702/authorkit
```

방법 2 — 브라우저에서:
1. `Browse and install plugins` 선택
2. `authorkit` 마켓플레이스 선택
3. `authorkit` 플러그인 선택
4. `Install now`

### Step 4: 사용

설치 후 스킬 이름이나 트리거 문장을 사용하면 자동으로 해당 스킬이 로드됩니다.

```
"책 쓰기 시작해줘"          → init
"레퍼런스 분석해줘"         → analyze
"5-1절 퇴고해줘"           → draft
"도해 만들어줘"            → diagram
"문체 검증해줘"            → review
```

---

## 6. 업데이트 절차

### 스킬 내용 수정

1. SKILL.md 수정
2. marketplace.json의 `metadata.version` 업데이트
3. git commit + push
4. 사용자 측에서 별도 업데이트 필요 없음 (다음 사용 시 자동 반영)

### 새 스킬 추가

1. `skills/` 폴더에 새 스킬 디렉터리 생성
2. SKILL.md 작성
3. marketplace.json의 `plugins[].skills` 배열에 경로 추가
4. version 업데이트
5. git commit + push

### 버전 관리

시맨틱 버전을 따릅니다:
- MAJOR: 호환성 깨지는 변경 (스킬 삭제, 명령 변경)
- MINOR: 새 스킬 추가, 기능 확장
- PATCH: 버그 수정, 문구 수정

---

## 7. 마켓플레이스 동작 원리

### 로컬 캐시 구조

```
~/.claude/plugins/
├── marketplaces/                       ← 등록된 마켓플레이스
│   ├── anthropic-agent-skills/
│   └── authorkit/                      ← /plugin marketplace add 시 생성
├── cache/                              ← 설치된 플러그인 캐시
│   ├── anthropic-agent-skills/
│   │   ├── document-skills/
│   │   └── example-skills/
│   └── authorkit/                      ← /plugin install 시 생성
│       └── [hash]/
│           ├── skills/
│           └── templates/
└── installed/                          ← 설치 메타데이터
```

### `/plugin marketplace add` 프로세스

```
사용자: /plugin marketplace add Nowzero/authorkit
         │
         ▼
Claude Code: GitHub API로 저장소 조회
         │
         ▼
.claude-plugin/marketplace.json 다운로드 및 파싱
         │
         ▼
마켓플레이스 메타데이터를 로컬 캐시에 저장
         │
         ▼
플러그인 브라우저에 표시
```

### `/plugin install` 프로세스

```
사용자: /install nowzero1702/authorkit
         │
         ▼
Claude Code: 마켓플레이스에서 플러그인 정보 조회
         │
         ▼
GitHub에서 skills/ 폴더 다운로드
         │
         ▼
~/.claude/plugins/cache/authorkit/[hash]/ 에 저장
         │
         ▼
각 SKILL.md의 name + description을 인덱싱
         │
         ▼
사용자 요청 시 description 매칭으로 자동 트리거
```

---

## 8. 트러블슈팅

### 마켓플레이스가 인식되지 않을 때

| 원인 | 해결 |
|------|------|
| 저장소가 비공개(private) | 공개(public)로 변경 |
| marketplace.json 위치 오류 | 반드시 `.claude-plugin/marketplace.json` |
| JSON 형식 오류 | JSON 문법 검증 (쉼표, 따옴표 등) |
| 저장소 URL 오류 | `owner/repo` 형식 확인 |

### 플러그인 설치가 안 될 때

| 원인 | 해결 |
|------|------|
| skills 경로 오류 | marketplace.json의 skills 배열 경로 확인 |
| SKILL.md 없음 | 각 스킬 폴더에 SKILL.md 존재 확인 |
| 프론트매터 오류 | YAML 형식 검증 (`---` 구분자, name/description 존재) |

### 스킬이 트리거되지 않을 때

| 원인 | 해결 |
|------|------|
| description이 불명확 | 트리거 조건("~할 때 사용")을 명시적으로 포함 |
| name이 다른 스킬과 충돌 | 고유한 이름 사용 |
| 플러그인이 설치 안 됨 | `/plugin list`로 설치 상태 확인 |

---

## 9. 품질 체크리스트

### 배포 전 필수 확인

- [ ] GitHub 공개 저장소 생성
- [ ] `.claude-plugin/marketplace.json` 작성 및 JSON 문법 확인
- [ ] 각 스킬 폴더에 `SKILL.md` 존재
- [ ] 모든 SKILL.md에 `name`과 `description` 프론트매터 존재
- [ ] `description`에 트리거 조건 포함
- [ ] README.md 작성 (설치 방법, 스킬 목록, 사용법)
- [ ] LICENSE 파일 포함 (MIT)
- [ ] marketplace.json의 skills 경로가 실제 폴더와 일치

### 품질 권장 사항

- [ ] 각 스킬을 실제 작업으로 테스트
- [ ] SKILL.md 500줄 이하
- [ ] 큰 문서는 references/ 폴더로 분리
- [ ] 사용 예제 포함
- [ ] 모든 파일 UTF-8 인코딩

---

## 10. authorkit 현재 상태

| 항목 | 상태 |
|------|:----:|
| SKILL.md 7개 (init~restructure) | ✅ |
| marketplace.json | ✅ |
| README.md | ✅ |
| LICENSE (MIT) | ✅ |
| templates/ 4개 | ✅ |
| GitHub 저장소 | ⬜ 생성 필요 |
| 실사용 테스트 | ⬜ |
| `/plugin marketplace add` 테스트 | ⬜ |

### 배포까지 남은 작업

1. GitHub에 공개 저장소 생성
2. `authorkit-skills/` 내용을 push
3. `/plugin marketplace add [owner]/authorkit` 테스트
4. `/install nowzero1702/authorkit` 테스트
5. 실제 책 집필 프로젝트에서 각 스킬 테스트
