---
name: authorkit-juice
description: 레퍼런스 또는 원고 파일(pdf, docx, hwpx)에서 핵심만 짜내어(juice) 깨끗한 마크다운으로 변환합니다. 고급 표 추출(테두리+테두리 없는 표), 읽기 순서 보정, 스캔 문서 OCR, 수식 LaTeX 변환, 구조화된 JSON 출력, 하이브리드 AI 처리를 지원합니다. "juice 해줘", "md로 짜줘", "마크다운으로 추출", "토큰 절약", "OCR로 변환", "수식 추출", "표 추출" 등의 요청 시 사용.
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
| **json** | **낮음** | 바운딩 박스 포함 구조화 데이터 |

한 번 변환 후 md에서 작업하면 analyze, compare, draft, review 전반에서
토큰을 크게 절약할 수 있습니다.

## 사용법 예시

```
"레퍼런스 PDF를 마크다운으로 변환해줘"
"250~350페이지만 md로 변환해줘"
"내 원고 3장을 이미지 포함해서 md로 변환해줘"
"전부 md로 변환해줘"
"스캔된 PDF야, OCR로 변환해줘"
"테두리 없는 표도 추출해줘"
"수식은 LaTeX로 보존해줘"
"바운딩 박스 포함 JSON으로 출력해줘"
```

## 실행 흐름

### 1. 입력 선택

사용자가 지정하는 항목:
- **파일**: 어떤 파일을 변환할지
- **범위** (선택): 페이지, 챕터, 또는 전체
  - 페이지: "10~50페이지"
  - 챕터: "3장" 또는 "3~5장"
  - 전체: 파일 전체 (기본값)
- **출력 형식** (선택): `markdown` (기본), `json`, `html`, `text`
- **옵션** (선택): OCR, 표 추출 방식, 읽기 순서, 하이브리드 모드

### 2. 페이지 분류 (하이브리드 처리)

추출 전 각 페이지를 최적 처리 경로로 분류합니다:

**분류 기준:**
- 텍스트 밀도: 추출 가능한 텍스트가 극히 적음 → 스캔 문서
- 이미지 비율: 이미지가 지배적 → AI 분석 필요
- 표 복잡도: 복잡한/테두리 없는 표 → AI 추출 유리
- 수식 존재: 수학 수식 많음 → 전문 처리 필요

**처리 경로:**
| 페이지 유형 | 경로 | 속도 |
|-------------|------|:----:|
| 깨끗한 텍스트, 단순 표 | 로컬 (pymupdf) | 빠름 (~0.05초/페이지) |
| 스캔/이미지 위주 | AI 백엔드 (OCR) | 느림 |
| 복잡한 테두리 없는 표 | AI 백엔드 (표 감지) | 느림 |
| 수식 위주 | AI 백엔드 (LaTeX 추출) | 느림 |

```python
def triage_page(page):
    """페이지를 최적 처리 경로로 분류"""
    text = page.get_text("text")
    images = page.get_images()
    text_density = len(text.strip()) / max(page.rect.width * page.rect.height, 1)

    if text_density < 0.001 and len(images) > 0:
        return "ocr"           # 스캔된 페이지
    if has_complex_tables(page):
        return "ai_table"      # 테두리 없거나 복잡한 표
    if has_math_content(text):
        return "ai_formula"    # 수학 수식
    return "local"             # 표준 추출
```

하이브리드 모드를 사용할 수 없는 경우, 모든 페이지는 로컬 처리로 폴백합니다.

### 3. 텍스트 추출

파일 형식별 처리:

**PDF (pymupdf/fitz 사용):**
```python
import fitz
doc = fitz.open('reference.pdf')

# Tagged PDF 구조 트리 먼저 확인
if doc.is_pdf2:  # Tagged PDF — 구조 트리 활용
    for page_num in range(start, end):
        page = doc[page_num]
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)
        # 구조 트리에서 헤딩 레벨, 목록 항목 등 추출
else:
    for page_num in range(start, end):
        page = doc[page_num]
        text = page.get_text("text")
        # 휴리스틱 구조 감지: 헤딩, 문단, 캡션
```

**PDF OCR (스캔 문서용):**

OCR 엔진은 언어에 따라 우선순위가 다릅니다:

| 언어 | 1순위 | 2순위 | 3순위 |
|------|-------|-------|-------|
| 한국어 (kor) | **PaddleOCR** | pymupdf (Tesseract) | EasyOCR |
| 영어 (eng) | pymupdf (Tesseract) | PaddleOCR | EasyOCR |
| 일본어/중국어 | **PaddleOCR** | EasyOCR | pymupdf |

한국어 문서에서 PaddleOCR이 우선인 이유:
- Tesseract 대비 한글 인식 정확도가 높음
- GPU 가속으로 대량 페이지 처리에 유리
- 각도 보정(angle classification) 내장으로 기울어진 스캔에 강함

```python
import fitz
import re

doc = fitz.open('scanned.pdf')
for page_num in range(start, end):
    page = doc[page_num]
    raw_text = page.get_text("text").strip()

    # pymupdf 추출 텍스트의 한국어 비율로 OCR 필요 여부 판단
    korean_ratio = len(re.findall(r'[가-힣]', raw_text)) / max(len(raw_text), 1)
    use_ocr = len(raw_text) < 50 or korean_ratio < 0.05

    if use_ocr:
        # 방법 1 (권장): PaddleOCR — 한국어 문서에 최적
        from paddleocr import PaddleOCR
        ocr = PaddleOCR(use_angle_cls=True, lang='korean', use_gpu=True, show_log=False)
        mat = fitz.Matrix(2.0, 2.0)  # 2x 줌으로 OCR 정확도 향상
        pix = page.get_pixmap(matrix=mat)
        img_path = f"/tmp/ocr_page_{page_num}.png"
        pix.save(img_path)
        result = ocr.ocr(img_path, cls=True)
        ocr_lines = []
        if result and result[0]:
            for line in result[0]:
                text_content = line[1][0]
                confidence = line[1][1]
                if confidence > 0.5:  # 신뢰도 임계값
                    ocr_lines.append(text_content)
        text = '\n'.join(ocr_lines)

        # 방법 2: pymupdf 내장 OCR (Tesseract) — PaddleOCR 미설치 시 폴백
        tp = page.get_textpage_ocr(language="eng+kor", dpi=300, full=True)
        text = page.get_text("text", textpage=tp)

        # 방법 3: EasyOCR — 추가 폴백
        pix = page.get_pixmap(dpi=300)
        img_bytes = pix.tobytes("png")
        # EasyOCR 엔진에 전달
    else:
        text = raw_text
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

### 4. 읽기 순서 보정

PDF 텍스트 추출은 종종 순서가 뒤섞입니다 (다단 레이아웃, 사이드바,
플로팅 요소 등). XY-Cut 알고리즘으로 올바른 읽기 순서를 복원합니다.

```python
def xycut_reading_order(blocks, page_rect):
    """
    XY-Cut 알고리즘으로 읽기 순서 보정.
    큰 수평/수직 공백 갭을 찾아 페이지를 재귀적으로 분할.
    """
    if len(blocks) <= 1:
        return blocks

    # 수평 분할 시도 (상/하)
    h_gap, h_pos = find_max_horizontal_gap(blocks)
    # 수직 분할 시도 (좌/우)
    v_gap, v_pos = find_max_vertical_gap(blocks)

    if h_gap > v_gap and h_gap > threshold:
        top = [b for b in blocks if b.y1 <= h_pos]
        bottom = [b for b in blocks if b.y0 >= h_pos]
        return xycut_reading_order(top, page_rect) + \
               xycut_reading_order(bottom, page_rect)
    elif v_gap > threshold:
        left = [b for b in blocks if b.x1 <= v_pos]
        right = [b for b in blocks if b.x0 >= v_pos]
        return xycut_reading_order(left, page_rect) + \
               xycut_reading_order(right, page_rect)
    else:
        # 유의미한 갭 없음 — 위→아래, 왼→오른 정렬
        return sorted(blocks, key=lambda b: (b.y0, b.x0))
```

**적용 시점:**
- 다단 학술 논문
- 사이드바/여백 주석이 있는 교재
- 플로팅 그림/표가 있는 PDF
- 복잡한 레이아웃 문서

단순 단일 컬럼 문서에서는 불필요한 처리를 피하기 위해 건너뜁니다.

### 5. 표 추출

표 유형에 따른 이중 전략:

**전략 A: 테두리 기반 (보이는 선이 있는 표)**
```python
def extract_bordered_table(page):
    """보이는 셀 테두리(선/사각형)를 이용한 표 추출"""
    drawings = page.get_drawings()
    lines = [d for d in drawings if d["type"] in ("l", "re")]

    # 수평선, 수직선 찾기
    h_lines = find_horizontal_lines(lines)
    v_lines = find_vertical_lines(lines)

    # 선 교차점으로 그리드 구성
    grid = build_grid(h_lines, v_lines)

    # 각 셀에서 텍스트 추출
    table = []
    for row in grid.rows:
        row_data = []
        for cell in row:
            cell_text = page.get_text("text", clip=cell.rect).strip()
            row_data.append(cell_text)
        table.append(row_data)
    return table
```

**전략 B: 클러스터 기반 (테두리 없는 표)**
```python
def extract_borderless_table(page, blocks):
    """
    공간 정렬 패턴을 기반으로 텍스트 블록을 클러스터링하여
    테두리 없는 표를 감지.
    """
    # 1단계: 수직 정렬로 텍스트 블록 그룹화 (열)
    columns = cluster_by_x_alignment(blocks, tolerance=5)

    # 2단계: 수평 정렬로 그룹화 (행)
    rows = cluster_by_y_alignment(blocks, tolerance=3)

    # 3단계: 표 구조 검증
    if len(columns) >= 2 and len(rows) >= 2:
        # 교차점에서 표 구성
        table = build_table_from_clusters(columns, rows, blocks)
        return table
    return None
```

**자동 감지:**
```python
def detect_table_method(page):
    """표에 테두리가 있는지 자동 감지"""
    drawings = page.get_drawings()
    line_count = sum(1 for d in drawings if d["type"] in ("l", "re"))

    if line_count > 10:
        return "border"     # 테두리 있는 표
    else:
        return "cluster"    # 테두리 없는 표 시도
```

**마크다운 표 출력:**
```markdown
| 헤더 1 | 헤더 2 | 헤더 3 |
|--------|--------|--------|
| 셀 1   | 셀 2   | 셀 3   |
| 셀 4   | 셀 5   | 셀 6   |
```

복잡한 표(병합 셀, 중첩 헤더)는 완전한 충실도를 위해
마크다운 내 HTML 표로 출력합니다.

### 6. 수식 / 공식 추출

수학 수식을 감지하여 LaTeX로 변환합니다:

```python
def extract_formulas(page, text):
    """수학 수식 감지 및 LaTeX 변환"""
    # 방법 1: 폰트 분석으로 수식 영역 감지
    blocks = page.get_text("dict")["blocks"]
    for block in blocks:
        for line in block.get("lines", []):
            fonts = {span["font"] for span in line["spans"]}
            # 수학 폰트: Symbol, Cambria Math, CMMI, CMSY 등
            if any(is_math_font(f) for f in fonts):
                formula_region = line["bbox"]
                # 영역을 이미지로 렌더링하여 LaTeX 변환
                pix = page.get_pixmap(clip=fitz.Rect(formula_region), dpi=300)
                latex = image_to_latex(pix)  # AI 백엔드 또는 pix2tex 사용
                yield f"$${latex}$$"

    # 방법 2: 추출된 텍스트에서 패턴 감지
    import re
    formula_patterns = [
        r'(?:∑|∏|∫|∂|∇|√|∞)',     # 수학 기호
        r'[a-z]\s*=\s*[^,\.\n]+',   # 단순 방정식
        r'\b(?:lim|sin|cos|tan|log|ln|exp)\b',  # 함수
    ]
    for pattern in formula_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            yield f"${match.group()}$"
```

**마크다운 내 출력 형식:**
- 인라인: `$E = mc^2$`
- 디스플레이: `$$\sum_{i=1}^{n} x_i = x_1 + x_2 + \cdots + x_n$$`

### 7. 이미지 추출

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

**AI 이미지 설명 생성 (선택):**
```python
def generate_image_description(image_path, context=""):
    """
    추출된 이미지에 대한 설명적 alt 텍스트를 비전 모델로 생성.
    특히 유용한 경우:
    - 캡션이 없는 다이어그램
    - 차트와 그래프
    - 기술 일러스트
    """
    # Claude 비전 또는 로컬 VLM으로 이미지 설명
    # 주변 텍스트 컨텍스트가 설명 품질을 향상시킴
    description = vision_model.describe(
        image=image_path,
        prompt=f"교재의 이 그림을 설명해주세요. 문맥: {context}"
    )
    return description
```

### 8. 콘텐츠 안전성

잠재적으로 문제가 될 수 있는 콘텐츠를 감지하고 처리합니다:

**숨겨진 텍스트 감지:**
```python
def detect_hidden_text(page):
    """
    프롬프트 인젝션이나 콘텐츠 조작을 나타낼 수 있는
    보이지 않는/숨겨진 텍스트를 감지.
    """
    blocks = page.get_text("dict")["blocks"]
    hidden = []
    for block in blocks:
        for line in block.get("lines", []):
            for span in line["spans"]:
                # 투명하거나 거의 보이지 않는 텍스트 확인
                color = span.get("color", 0)
                size = span.get("size", 12)
                if size < 0.5:           # 0에 가까운 글꼴 크기
                    hidden.append(span["text"])
                if color == 0xFFFFFF:    # 흰 배경에 흰 글씨
                    hidden.append(span["text"])
    if hidden:
        log_warning(f"숨겨진 텍스트 감지: {len(hidden)}개 스팬")
    return hidden
```

**PII 제거 (선택):**
```python
import re

def sanitize_pii(text, options=None):
    """개인 식별 정보(PII)를 제거하거나 마스킹"""
    patterns = {
        "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "phone": r'\b(?:\+?82[-.]?)?0?\d{2,3}[-.]?\d{3,4}[-.]?\d{4}\b',
        "ip": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
        "credit_card": r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
        "resident_id": r'\b\d{6}[-]\d{7}\b',
    }
    for name, pattern in patterns.items():
        if options and name not in options:
            continue
        text = re.sub(pattern, f'[{name.upper()}_삭제됨]', text)
    return text
```

### 9. 마크다운 조립

추출된 텍스트와 이미지를 조합하여 깔끔한 md 파일을 생성합니다.

**변환 규칙:**
- 헤딩 → `#`, `##`, `###` (레벨에 따라)
- 굵은 글씨 → `**텍스트**`
- 목록 → `- 항목` (중첩 지원)
- 이미지 → `![캡션](images/파일명.png)`
- 표 → 마크다운 표 형식 (복잡한 병합 셀은 HTML 표)
- 코드 → ``` 코드 블록 ```
- 캡션 → 이미지 아래에 `[그림] 캡션 텍스트` 배치
- 수식 → `$인라인$` 또는 `$$디스플레이$$` LaTeX
- 각주 → `[^n]` (절 끝에 정의 배치)

**이미지 배치:**
- 이미지는 원본 텍스트 흐름상의 위치에 배치
- 캡션이 있는 경우 (예: "그림 4.1 ...") 이미지 참조 아래에 배치
- 캡션이 없으면 AI 생성 설명 또는 주변 문맥을 alt 텍스트로 사용

### 10. 구조화된 JSON 출력 (선택)

`--format json` 지정 시, 시맨틱 구조와 바운딩 박스 좌표를 포함하여 출력합니다:

```json
{
  "metadata": {
    "source": "reference.pdf",
    "pages": "250-350",
    "converted": "2025-03-25",
    "total_elements": 342
  },
  "pages": [
    {
      "page_num": 250,
      "width": 612,
      "height": 792,
      "elements": [
        {
          "type": "heading",
          "level": 1,
          "text": "제4장: 프로세서",
          "bbox": [72, 85, 540, 120],
          "confidence": 0.95
        },
        {
          "type": "paragraph",
          "text": "이 장에서는 프로세서의...",
          "bbox": [72, 140, 540, 280]
        },
        {
          "type": "table",
          "bbox": [72, 300, 540, 450],
          "rows": 5,
          "cols": 4,
          "data": [["헤더1", "헤더2", "헤더3", "헤더4"], ...]
        },
        {
          "type": "image",
          "bbox": [72, 470, 540, 650],
          "file": "images/p250_img0.png",
          "caption": "그림 4.1 프로세서의 추상적 관점",
          "description": "프로세서 주요 구성 요소를 보여주는 블록도..."
        },
        {
          "type": "formula",
          "bbox": [100, 670, 400, 700],
          "latex": "E = mc^2",
          "display": true
        }
      ]
    }
  ]
}
```

구조화된 출력의 활용:
- 다운스트림 AI 처리를 위한 정확한 요소 위치
- 공간 컨텍스트를 포함한 RAG 인덱스 구축
- 특정 콘텐츠 유형에 대한 프로그래밍 접근

### 11. 산출물

```
authorkit/converted/
├── ref-001/
│   ├── full.md                    ← 전체 변환 파일
│   ├── full.json                  ← 구조화된 JSON (요청 시)
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
- 이미지: 23개 추출 (3개 AI 설명 포함)
- 감지된 헤딩: 18개
- 감지된 표: 12개 (테두리 있음 8개, 테두리 없음 4개)
- 감지된 수식: 15개
- OCR 페이지: 2개 (스캔)
- 숨겨진 텍스트 경고: 0건
- 처리 방식: 하이브리드 (로컬 85, AI 라우팅 15)

## 이미지 매핑
| 이미지 파일 | 원본 페이지 | 캡션 | AI 설명 |
|-----------|:----------:|---------|:------:|
| p252_img0.png | 252 | 그림 4.1 시스템 추상적 관점... | 있음 |
| p255_img0.png | 255 | 그림 4.2 기본 구현... | 없음 |

## 표 요약
| 표 # | 페이지 | 방법 | 행 x 열 | 병합 셀 |
|:----:|:-----:|------|:-------:|:------:|
| 1 | 253 | 테두리 | 5x4 | 없음 |
| 2 | 260 | 클러스터 | 8x3 | 있음 |

## 수식 요약
| # | 페이지 | LaTeX | 디스플레이 |
|:-:|:-----:|-------|:---------:|
| 1 | 270 | E = mc^2 | 예 |
| 2 | 271 | \sum_{i=1}^{n} x_i | 예 |
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

## 옵션 레퍼런스

| 옵션 | 값 | 기본값 | 설명 |
|------|------|--------|------|
| `format` | markdown, json, html, text | markdown | 출력 형식 |
| `table_method` | auto, border, cluster | auto | 표 추출 전략 |
| `reading_order` | auto, xycut, none | auto | 읽기 순서 보정 |
| `ocr` | auto, force, off | auto | 스캔 페이지 OCR |
| `ocr_engine` | auto, paddle, tesseract, easyocr | auto | OCR 엔진 (auto: 언어별 우선순위) |
| `ocr_lang` | eng, kor, jpn, ... | eng+kor | OCR 언어 |
| `formula` | on, off | on | 수식 추출 |
| `image_output` | embedded, external, off | external | 이미지 처리 모드 |
| `image_desc` | on, off | off | AI 이미지 설명 |
| `sanitize` | on, off | off | PII 제거 |
| `hidden_text` | warn, strip, off | warn | 숨겨진 텍스트 처리 |
| `hybrid` | auto, local, full | auto | 처리 경로 |

## 다른 스킬과의 연동

변환 후 다른 authorkit 스킬은 자동으로 md 파일을 우선 사용합니다.

```
/authorkit-juice ref         ← 레퍼런스를 md로 변환
/authorkit-analyze ref         ← converted/ref-001/*.md에서 읽기 (빠름)
/authorkit-compare ch3         ← PDF 대신 md에서 읽기 (토큰 절약)
/authorkit-draft 3-1           ← md에서 내용 참조 (효율적)
```

`analyze` 스킬은 변환된 md 파일이 있는지 먼저 확인합니다.
존재하면 원본 형식 대신 md에서 읽습니다.

## 필요 패키지

필수 Python 패키지:
- `pymupdf` (fitz) — PDF 텍스트 + 이미지 추출 + OCR
- `python-docx` — docx 텍스트 + 이미지 추출
- `Pillow` — 이미지 처리
- `openpyxl` — xlsx 지원 (필요 시)

선택 (고급 기능용):
- `paddlepaddle` + `paddleocr` — **한국어/CJK OCR 최우선** (GPU 가속, 각도 보정 내장)
- `easyocr` — 고급 OCR (80개 이상 언어)
- `pix2tex` — 수식 이미지 → LaTeX 변환

설치:
```bash
# 코어
pip install pymupdf python-docx Pillow openpyxl

# 선택: PaddleOCR (한국어 PDF 추천)
pip install paddlepaddle paddleocr

# 선택: 고급 OCR 및 수식 추출
pip install easyocr pix2tex
```
