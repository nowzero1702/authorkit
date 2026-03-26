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

한 번 변환 후 md에서 작업하면 analyze, compare, draft, review 전반에서
토큰을 크게 절약할 수 있습니다.

## 사용법 예시

```
"레퍼런스 PDF를 마크다운으로 변환해줘"
"250~350페이지만 md로 변환해줘"
"내 원고 3장을 이미지 포함해서 md로 변환해줘"
"전부 md로 변환해줘"
```

## 실행 흐름

### 1. 입력 선택

사용자가 지정하는 항목:
- **파일**: 어떤 파일을 변환할지
- **범위** (선택): 페이지, 챕터, 또는 전체
  - 페이지: "10~50페이지"
  - 챕터: "3장" 또는 "3~5장"
  - 전체: 파일 전체 (기본값)

### 2. 텍스트 추출

파일 형식별 처리:

**PDF (pymupdf/fitz 사용):**
```python
import fitz
doc = fitz.open('reference.pdf')
for page_num in range(start, end):
    page = doc[page_num]
    text = page.get_text("text")
    # 구조 감지: 헤딩, 문단, 캡션
```

**docx (python-docx 사용):**
```python
from docx import Document
doc = Document('manuscript.docx')
for para in doc.paragraphs:
    style = para.style.name  # Heading 1, Normal, Caption 등
    text = para.text
    # 스타일을 마크다운으로 변환: Heading → #, Bold → ** 등
```

**hwpx (zipfile + XML 사용):**
```python
import zipfile
with zipfile.ZipFile('document.hwpx') as z:
    # Contents/section0.xml 파싱
    # paragraph 태그에서 텍스트 추출
```

### 3. 이미지 추출

지정된 범위의 모든 이미지를 PNG로 추출하여 저장합니다.

**PDF 이미지:**
```python
import fitz
doc = fitz.open('reference.pdf')
page = doc[page_num]

# 방법 1: 임베디드 이미지 추출
images = page.get_images()
for img_idx, img in enumerate(images):
    xref = img[0]
    pix = fitz.Pixmap(doc, xref)
    if pix.n >= 5:  # CMYK → RGB
        pix = fitz.Pixmap(fitz.csRGB, pix)
    pix.save(f'images/p{page_num}_img{img_idx}.png')

# 방법 2: 복잡한 레이아웃은 페이지 전체를 이미지로 렌더링
pix = page.get_pixmap(dpi=150)
pix.save(f'images/p{page_num}_full.png')
```

**docx 이미지:**
```python
from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE as RT
import os

doc = Document('manuscript.docx')
img_count = 0
for rel in doc.part.rels.values():
    if 'image' in rel.reltype:
        img_data = rel.target_part.blob
        ext = os.path.splitext(rel.target_ref)[1]
        with open(f'images/img_{img_count}{ext}', 'wb') as f:
            f.write(img_data)
        img_count += 1
```

**hwpx 이미지:**
```python
import zipfile
with zipfile.ZipFile('document.hwpx') as z:
    for name in z.namelist():
        if name.startswith('BinData/') and any(
            name.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.bmp']
        ):
            z.extract(name, 'images/')
```

### 4. 마크다운 조립

추출된 텍스트와 이미지를 조합하여 깔끔한 md 파일을 생성합니다.

**변환 규칙:**
- 헤딩 → `#`, `##`, `###` (레벨에 따라)
- 굵은 글씨 → `**텍스트**`
- 목록 → `- 항목`
- 이미지 → `![캡션](images/파일명.png)`
- 표 → 마크다운 표 형식
- 코드 → ``` 코드 블록 ```
- 캡션 → 이미지 아래에 `[그림] 캡션 텍스트` 배치

**이미지 배치:**
- 이미지는 원본 텍스트 흐름상의 위치에 배치
- 캡션이 있는 경우 (예: "그림 4.1 ...") 이미지 참조 아래에 배치
- 캡션이 없으면 주변 문맥을 alt 텍스트로 사용

### 5. 산출물

```
authorkit/converted/
├── ref-001/
│   ├── full.md                    ← 전체 변환 파일
│   ├── ch01.md                    ← 챕터별 (구조 감지 시)
│   ├── ch02.md
│   ├── images/
│   │   ├── p10_img0.png
│   │   ├── p10_img1.png
│   │   ├── p15_img0.png
│   │   └── ...
│   └── conversion-log.md         ← 변환 메타데이터
└── manuscript/
    ├── full.md
    ├── ch03.md
    ├── images/
    └── conversion-log.md
```

**conversion-log.md 예시:**
```markdown
# 변환 기록

- 원본: reference.pdf (1074페이지)
- 범위: 250~350페이지 (4장: 프로세서)
- 변환일: 2025-03-25
- 텍스트: 45,230자
- 이미지: 23개 추출
- 감지된 헤딩: 18개

## 이미지 매핑
| 이미지 파일 | 원본 페이지 | 캡션 |
|-----------|:----------:|---------|
| p252_img0.png | 252 | 그림 4.1 시스템 추상적 관점... |
| p255_img0.png | 255 | 그림 4.2 기본 구현... |
```

## 범위 지정

| 입력 | 해석 |
|------|------|
| "10~50페이지" | PDF 10~50페이지 |
| "3장" | 3장 경계를 감지하여 해당 범위 추출 |
| "3~5장" | 3장~5장 |
| "전체" | 파일 전체 |
| (미지정) | 파일 전체 |

챕터 기반 범위의 경우, 먼저 빠른 구조 스캔으로 챕터 경계를 감지한 뒤
해당 범위를 추출합니다.

## 다른 스킬과의 연동

변환 후 다른 authorkit 스킬은 자동으로 md 파일을 우선 사용합니다.

```
/authorkit.juice ref         ← 레퍼런스를 md로 변환
/authorkit.analyze ref         ← converted/ref-001/*.md에서 읽기 (빠름)
/authorkit.compare ch3         ← PDF 대신 md에서 읽기 (토큰 절약)
/authorkit.draft 3-1           ← md에서 내용 참조 (효율적)
```

`analyze` 스킬은 변환된 md 파일이 있는지 먼저 확인합니다.
존재하면 원본 형식 대신 md에서 읽습니다.

## 필요 패키지

필수 Python 패키지:
- `pymupdf` (fitz) — PDF 텍스트 + 이미지 추출
- `python-docx` — docx 텍스트 + 이미지 추출
- `Pillow` — 이미지 처리
- `openpyxl` — xlsx 지원 (필요 시)

설치:
```bash
pip install pymupdf python-docx Pillow openpyxl
```
