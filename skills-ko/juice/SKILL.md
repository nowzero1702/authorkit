---
name: juice
description: 레퍼런스 또는 원고 파일(pdf, docx, hwpx)에서 핵심만 짜내어(juice) 깨끗한 마크다운으로 변환합니다. 텍스트와 이미지를 추출하고, 레이아웃 노이즈를 제거하여 토큰 소비를 대폭 줄입니다. "juice 해줘", "md로 짜줘", "마크다운으로 추출", "토큰 절약" 등의 요청 시 사용.
---

# authorkit.juice — 마크다운 변환

레퍼런스 또는 원고 파일을 이미지 포함 마크다운 형식으로 변환합니다.
한 번 변환해 두면 이후 authorkit 작업에서 토큰 소비를 크게 줄일 수 있습니다.

## 왜 변환하는가?

| 형식 | 토큰 비용 | 노이즈 |
|------|:--------:|:-----:|
| PDF | 높음 | 헤더, 푸터, 페이지 번호 등 |
| docx | 중간 | XML 오버헤드, 스타일 메타데이터 |
| **md** | **낮음** | 깨끗한 텍스트, 노이즈 없음 |

## 사용법 예시

```
"레퍼런스 PDF를 마크다운으로 변환해줘"
"250~350페이지만 md로 변환해줘"
"내 원고 3장을 이미지 포함해서 md로 변환해줘"
"전부 md로 변환해줘"
```

## 실행 흐름

### 1. 입력 선택

- 파일: 어떤 파일을 변환할지
- 범위 (선택): 페이지, 챕터, 또는 전체
  - 페이지: "10~50페이지"
  - 챕터: "3장" 또는 "3~5장"
  - 전체: 파일 전체 (기본값)

### 2. 텍스트 추출

파일 형식별 처리:
- PDF: pymupdf(fitz)로 텍스트 + 구조 추출
- docx: python-docx로 문단 + 스타일 추출
- hwpx: ZIP 해제 후 XML 파싱

### 3. 이미지 추출

지정된 범위의 모든 이미지를 PNG로 추출하여 저장합니다.

- PDF: pymupdf로 임베디드 이미지 추출 또는 페이지 전체 렌더링
- docx: python-docx로 임베디드 이미지 추출
- hwpx: ZIP 내 BinData 폴더에서 이미지 추출

### 4. 마크다운 조립

추출된 텍스트와 이미지를 조합하여 깔끔한 md 파일을 생성합니다.

- 헤딩 → `#`, `##`, `###`
- 굵은 글씨 → `**텍스트**`
- 이미지 → `![캡션](images/파일명.png)`
- 표 → 마크다운 표 형식
- 캡션 → 이미지 아래에 `[그림] 캡션` 배치

### 5. 산출물

```
authorkit/converted/
├── ref-001/
│   ├── full.md                    ← 전체 변환 파일
│   ├── ch01.md                    ← 챕터별 (구조 감지 시)
│   ├── images/
│   │   ├── p10_img0.png
│   │   └── ...
│   └── conversion-log.md         ← 변환 메타데이터
└── manuscript/
    ├── full.md
    ├── images/
    └── conversion-log.md
```

## 다른 스킬과의 연동

변환 후 다른 authorkit 스킬은 자동으로 md 파일을 우선 사용합니다.

```
/authorkit.juice ref         ← 레퍼런스를 md로 변환
/authorkit.analyze ref         ← converted/ref-001/*.md에서 읽기 (빠름)
/authorkit.compare ch3         ← PDF 대신 md에서 읽기 (토큰 절약)
/authorkit.draft 3-1           ← md에서 내용 참조 (효율적)
```

## 필요 패키지

```bash
pip install pymupdf python-docx Pillow openpyxl
```
