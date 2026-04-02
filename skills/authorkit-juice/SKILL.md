---
name: authorkit-juice
description: Juice (extract) reference or manuscript files (pdf, docx, hwpx) into clean markdown with embedded images. Supports advanced table extraction (bordered + borderless), reading order correction, OCR for scanned documents, math/formula extraction (LaTeX), structured JSON output, and hybrid AI-enhanced processing. Use when "juice the reference", "extract to md", "squeeze into markdown", "reduce token usage".
---

# authorkit.juice — Juice into Markdown

Converts reference or manuscript files to markdown format with embedded images.
This dramatically reduces token consumption for subsequent authorkit operations
by eliminating the need to re-parse binary formats.

## Why Convert?

| Format | Token Cost | Noise |
|--------|:---------:|:-----:|
| PDF | High | Layout headers, footers, page numbers |
| docx | Medium | XML overhead, style metadata |
| **md** | **Low** | Clean text, no noise |
| **json** | **Low** | Structured with bounding boxes |

Converting once and working from md saves significant tokens across
analyze, compare, draft, and review operations.

## Usage Examples

```
"Convert the reference PDF to markdown"
"Convert pages 250-350 of the textbook to md"
"Convert chapter 3 of my manuscript to markdown with images"
"Convert everything to md"
"Convert with OCR — it's a scanned PDF"
"Extract tables from the PDF — they have no borders"
"Convert with math formulas preserved as LaTeX"
"Output as structured JSON with bounding boxes"
```

## Execution Flow

### 1. Input Selection

User specifies:
- **File**: Which file to convert
- **Range** (optional): Page range, chapter range, or "all"
  - Pages: "pages 10-50"
  - Chapters: "chapter 3" or "ch3-ch5"
  - All: entire file (default)
- **Output format** (optional): `markdown` (default), `json`, `html`, `text`
- **Options** (optional): OCR, table method, reading order, hybrid mode

### 2. Page Triage (Hybrid Processing)

Before extraction, each page is classified for optimal processing:

**Triage criteria:**
- Text density: pages with very low extractable text → likely scanned
- Image ratio: pages dominated by images → may need AI analysis
- Table complexity: complex/borderless tables → benefit from AI extraction
- Formula presence: math-heavy pages → need specialized processing

**Processing routes:**
| Page Type | Route | Speed |
|-----------|-------|:-----:|
| Clean text, simple tables | Local (pymupdf) | Fast (~0.05s/page) |
| Scanned / image-heavy | AI backend (OCR) | Slower |
| Complex borderless tables | AI backend (table detection) | Slower |
| Math / formula heavy | AI backend (LaTeX extraction) | Slower |

```python
def triage_page(page):
    """Classify page for optimal processing route."""
    text = page.get_text("text")
    images = page.get_images()
    text_density = len(text.strip()) / max(page.rect.width * page.rect.height, 1)

    if text_density < 0.001 and len(images) > 0:
        return "ocr"           # Scanned page
    if has_complex_tables(page):
        return "ai_table"      # Borderless or complex tables
    if has_math_content(text):
        return "ai_formula"    # Math formulas
    return "local"             # Standard extraction
```

When hybrid mode is not available, all pages fall back to local processing.

### 3. Text Extraction

Based on file format:

**PDF (using pymupdf/fitz):**
```python
import fitz
doc = fitz.open('reference.pdf')

# Check for tagged PDF structure first
if doc.is_pdf2:  # Tagged PDF — use structure tree
    for page_num in range(start, end):
        page = doc[page_num]
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)
        # Leverage structure tree for heading levels, list items, etc.
else:
    for page_num in range(start, end):
        page = doc[page_num]
        text = page.get_text("text")
        # Heuristic structure detection: headings, paragraphs, captions
```

**PDF with OCR (for scanned documents):**

OCR engine priority varies by language:

| Language | 1st Priority | 2nd Priority | 3rd Priority |
|----------|-------------|-------------|-------------|
| Korean (kor) | **PaddleOCR** | pymupdf (Tesseract) | EasyOCR |
| English (eng) | pymupdf (Tesseract) | PaddleOCR | EasyOCR |
| Japanese/Chinese | **PaddleOCR** | EasyOCR | pymupdf |

PaddleOCR is preferred for Korean because:
- Higher accuracy for Hangul recognition vs Tesseract
- GPU acceleration for bulk page processing
- Built-in angle classification for skewed scans

```python
import fitz
import re

doc = fitz.open('scanned.pdf')
for page_num in range(start, end):
    page = doc[page_num]
    raw_text = page.get_text("text").strip()

    # Determine OCR need based on Korean character ratio
    korean_ratio = len(re.findall(r'[가-힣]', raw_text)) / max(len(raw_text), 1)
    use_ocr = len(raw_text) < 50 or korean_ratio < 0.05

    if use_ocr:
        # Method 1 (recommended): PaddleOCR — best for Korean documents
        from paddleocr import PaddleOCR
        ocr = PaddleOCR(use_angle_cls=True, lang='korean', use_gpu=True, show_log=False)
        mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better OCR accuracy
        pix = page.get_pixmap(matrix=mat)
        img_path = f"/tmp/ocr_page_{page_num}.png"
        pix.save(img_path)
        result = ocr.ocr(img_path, cls=True)
        ocr_lines = []
        if result and result[0]:
            for line in result[0]:
                text_content = line[1][0]
                confidence = line[1][1]
                if confidence > 0.5:  # confidence threshold
                    ocr_lines.append(text_content)
        text = '\n'.join(ocr_lines)

        # Method 2: pymupdf built-in OCR (Tesseract) — fallback if PaddleOCR unavailable
        tp = page.get_textpage_ocr(language="eng+kor", dpi=300, full=True)
        text = page.get_text("text", textpage=tp)

        # Method 3: EasyOCR — additional fallback
        pix = page.get_pixmap(dpi=300)
        img_bytes = pix.tobytes("png")
        # Pass to EasyOCR engine
    else:
        text = raw_text
```

**docx (using python-docx):**
```python
from docx import Document
doc = Document('manuscript.docx')
for para in doc.paragraphs:
    style = para.style.name  # Heading 1, Normal, Caption, etc.
    text = para.text
    # Convert styles to markdown: Heading -> #, Bold -> **, etc.
```

**hwpx (using zipfile + XML):**
```python
import zipfile
with zipfile.ZipFile('document.hwpx') as z:
    # Parse Contents/section0.xml
    # Extract text from paragraph tags
```

### 4. Reading Order Correction

PDF text extraction often produces out-of-order content (multi-column layouts,
sidebars, floating elements). Apply XY-Cut algorithm to reconstruct proper
reading order.

```python
def xycut_reading_order(blocks, page_rect):
    """
    XY-Cut algorithm for reading order correction.
    Recursively splits page into regions by finding
    large horizontal/vertical whitespace gaps.
    """
    if len(blocks) <= 1:
        return blocks

    # Try horizontal split (top/bottom)
    h_gap, h_pos = find_max_horizontal_gap(blocks)
    # Try vertical split (left/right)
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
        # No significant gap — sort top-to-bottom, left-to-right
        return sorted(blocks, key=lambda b: (b.y0, b.x0))
```

**When to apply:**
- Multi-column academic papers
- Textbooks with sidebars/margin notes
- PDFs with floating figures/tables
- Documents with complex layouts

Skip for simple single-column documents to avoid unnecessary processing.

### 5. Table Extraction

Two strategies for different table types:

**Strategy A: Border-based (for tables with visible lines)**
```python
def extract_bordered_table(page):
    """Extract table using visible cell borders (lines/rectangles)."""
    drawings = page.get_drawings()
    lines = [d for d in drawings if d["type"] in ("l", "re")]

    # Find horizontal and vertical lines
    h_lines = find_horizontal_lines(lines)
    v_lines = find_vertical_lines(lines)

    # Build grid from line intersections
    grid = build_grid(h_lines, v_lines)

    # Extract text from each cell
    table = []
    for row in grid.rows:
        row_data = []
        for cell in row:
            cell_text = page.get_text("text", clip=cell.rect).strip()
            row_data.append(cell_text)
        table.append(row_data)
    return table
```

**Strategy B: Cluster-based (for borderless tables)**
```python
def extract_borderless_table(page, blocks):
    """
    Detect borderless tables by clustering text blocks
    based on spatial alignment patterns.
    """
    # Step 1: Group text blocks by vertical alignment
    columns = cluster_by_x_alignment(blocks, tolerance=5)

    # Step 2: Group by horizontal alignment for rows
    rows = cluster_by_y_alignment(blocks, tolerance=3)

    # Step 3: Validate table structure
    if len(columns) >= 2 and len(rows) >= 2:
        # Build table from intersections
        table = build_table_from_clusters(columns, rows, blocks)
        return table
    return None
```

**Auto-detection:**
```python
def detect_table_method(page):
    """Auto-detect whether table has borders."""
    drawings = page.get_drawings()
    line_count = sum(1 for d in drawings if d["type"] in ("l", "re"))

    if line_count > 10:
        return "border"     # Likely bordered table
    else:
        return "cluster"    # Try borderless detection
```

**Markdown table output:**
```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
```

For complex tables (merged cells, nested headers), output as HTML table
within the markdown for full fidelity.

### 6. Math / Formula Extraction

Detect and extract mathematical formulas as LaTeX:

```python
def extract_formulas(page, text):
    """
    Detect and convert mathematical formulas to LaTeX.
    """
    # Method 1: Detect formula regions by font analysis
    blocks = page.get_text("dict")["blocks"]
    for block in blocks:
        for line in block.get("lines", []):
            fonts = {span["font"] for span in line["spans"]}
            # Math fonts: Symbol, Cambria Math, CMMI, CMSY, etc.
            if any(is_math_font(f) for f in fonts):
                formula_region = line["bbox"]
                # Render region as image for LaTeX conversion
                pix = page.get_pixmap(clip=fitz.Rect(formula_region), dpi=300)
                latex = image_to_latex(pix)  # Via AI backend or pix2tex
                yield f"$${latex}$$"

    # Method 2: Pattern detection in extracted text
    # Look for common formula indicators
    import re
    formula_patterns = [
        r'(?:∑|∏|∫|∂|∇|√|∞)',     # Math symbols
        r'[a-z]\s*=\s*[^,\.\n]+',   # Simple equations
        r'\b(?:lim|sin|cos|tan|log|ln|exp)\b',  # Functions
    ]
    for pattern in formula_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            yield f"${match.group()}$"
```

**Output format in markdown:**
- Inline: `$E = mc^2$`
- Display: `$$\sum_{i=1}^{n} x_i = x_1 + x_2 + \cdots + x_n$$`

### 7. Image Extraction

Extracts all images from the specified range and saves as PNG.

**PDF images:**
```python
import fitz
doc = fitz.open('reference.pdf')
page = doc[page_num]

# Method 1: Extract embedded images
images = page.get_images()
for img_idx, img in enumerate(images):
    xref = img[0]
    pix = fitz.Pixmap(doc, xref)
    if pix.n >= 5:  # CMYK -> RGB
        pix = fitz.Pixmap(fitz.csRGB, pix)
    pix.save(f'images/p{page_num}_img{img_idx}.png')

# Method 2: Render full page as image (for complex layouts)
pix = page.get_pixmap(dpi=150)
pix.save(f'images/p{page_num}_full.png')
```

**docx images:**
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

**hwpx images:**
```python
import zipfile
with zipfile.ZipFile('document.hwpx') as z:
    for name in z.namelist():
        if name.startswith('BinData/') and any(
            name.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.bmp']
        ):
            z.extract(name, 'images/')
```

**AI-powered image descriptions (optional):**
```python
def generate_image_description(image_path, context=""):
    """
    Generate descriptive alt text for extracted images
    using vision model. Especially useful for:
    - Diagrams without captions
    - Charts and graphs
    - Technical illustrations
    """
    # Use Claude vision or local VLM to describe the image
    # Context from surrounding text improves description quality
    description = vision_model.describe(
        image=image_path,
        prompt=f"Describe this figure from a textbook. Context: {context}"
    )
    return description
```

### 8. Content Safety

Detect and handle potentially problematic content:

**Hidden text detection:**
```python
def detect_hidden_text(page):
    """
    Detect invisible/hidden text that may indicate
    prompt injection or content manipulation.
    """
    blocks = page.get_text("dict")["blocks"]
    hidden = []
    for block in blocks:
        for line in block.get("lines", []):
            for span in line["spans"]:
                # Check for transparent or near-invisible text
                color = span.get("color", 0)
                size = span.get("size", 12)
                if size < 0.5:           # Near-zero font size
                    hidden.append(span["text"])
                if color == 0xFFFFFF:    # White text on white
                    hidden.append(span["text"])
    if hidden:
        log_warning(f"Hidden text detected: {len(hidden)} spans")
    return hidden
```

**PII sanitization (optional):**
```python
import re

def sanitize_pii(text, options=None):
    """Remove or mask personally identifiable information."""
    patterns = {
        "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "phone": r'\b(?:\+?1[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}\b',
        "ip": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
        "credit_card": r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
    }
    for name, pattern in patterns.items():
        if options and name not in options:
            continue
        text = re.sub(pattern, f'[{name.upper()}_REDACTED]', text)
    return text
```

### 9. Markdown Assembly

Combines extracted text and images into a clean md file.

**Conversion rules:**
- Headings -> `#`, `##`, `###` based on level
- Bold -> `**text**`
- Lists -> `- item` (with nesting support)
- Images -> `![caption](images/filename.png)`
- Tables -> markdown table syntax (or HTML for complex merged cells)
- Code -> ``` code blocks ```
- Captions -> `[Figure] caption text` below image
- Math -> `$inline$` or `$$display$$` LaTeX
- Footnotes -> `[^n]` with definitions at section end

**Image placement:**
- Images are placed at their original position in the text flow
- If an image has a caption (e.g., "FIGURE 4.1 ..."), it's placed below the image reference
- If no caption, AI-generated description or surrounding context is used as alt text

### 10. Structured JSON Output (Optional)

When `--format json` is specified, output includes semantic structure
and bounding box coordinates:

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
          "text": "Chapter 4: The Processor",
          "bbox": [72, 85, 540, 120],
          "confidence": 0.95
        },
        {
          "type": "paragraph",
          "text": "In this chapter we examine...",
          "bbox": [72, 140, 540, 280]
        },
        {
          "type": "table",
          "bbox": [72, 300, 540, 450],
          "rows": 5,
          "cols": 4,
          "data": [["Header1", "Header2", "Header3", "Header4"], ...]
        },
        {
          "type": "image",
          "bbox": [72, 470, 540, 650],
          "file": "images/p250_img0.png",
          "caption": "FIGURE 4.1 An abstract view of the processor",
          "description": "Block diagram showing..."
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

This structured output is useful for:
- Precise element location for downstream AI processing
- Building RAG indexes with spatial context
- Programmatic access to specific content types

### 11. Output

```
authorkit/converted/
├── ref-001/
│   ├── full.md                    <- Complete converted file
│   ├── full.json                  <- Structured JSON (if requested)
│   ├── ch01.md                    <- Per-chapter (if structure detected)
│   ├── ch02.md
│   ├── images/
│   │   ├── p10_img0.png
│   │   ├── p10_img1.png
│   │   ├── p15_img0.png
│   │   └── ...
│   └── conversion-log.md         <- Conversion metadata
└── manuscript/
    ├── full.md
    ├── ch03.md
    ├── images/
    └── conversion-log.md
```

**conversion-log.md example:**
```markdown
# Conversion Log

- Source: reference.pdf (1074 pages)
- Range: pages 250-350 (Chapter 4: The Processor)
- Converted: 2025-03-25
- Text: 45,230 characters
- Images: 23 extracted (3 with AI descriptions)
- Headings detected: 18
- Tables detected: 12 (8 bordered, 4 borderless)
- Formulas detected: 15
- OCR pages: 2 (scanned)
- Hidden text warnings: 0
- Processing: hybrid (85 local, 15 AI-routed)

## Image Mapping
| Image File | Source Page | Caption | AI Description |
|-----------|:----------:|---------|:--------------:|
| p252_img0.png | 252 | FIGURE 4.1 An abstract view... | Yes |
| p255_img0.png | 255 | FIGURE 4.2 The basic implementation... | No |

## Table Summary
| Table # | Page | Method | Rows x Cols | Has Merged Cells |
|:-------:|:----:|--------|:-----------:|:----------------:|
| 1 | 253 | border | 5x4 | No |
| 2 | 260 | cluster | 8x3 | Yes |

## Formula Summary
| # | Page | LaTeX | Display |
|:-:|:----:|-------|:-------:|
| 1 | 270 | E = mc^2 | Yes |
| 2 | 271 | \sum_{i=1}^{n} x_i | Yes |
```

## Range Specification

| Input | Interpretation |
|-------|---------------|
| "pages 10-50" | PDF pages 10 through 50 |
| "chapter 3" | Detect chapter 3 boundaries, extract that range |
| "ch3-ch5" | Chapters 3 through 5 |
| "all" | Entire file |
| (none) | Entire file |

For chapter-based ranges, the skill first runs a quick structure scan
to detect chapter boundaries, then extracts the specified range.

## Options Reference

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `format` | markdown, json, html, text | markdown | Output format |
| `table_method` | auto, border, cluster | auto | Table extraction strategy |
| `reading_order` | auto, xycut, none | auto | Reading order correction |
| `ocr` | auto, force, off | auto | OCR for scanned pages |
| `ocr_engine` | auto, paddle, tesseract, easyocr | auto | OCR engine (auto: priority by language) |
| `ocr_lang` | eng, kor, jpn, ... | eng+kor | OCR languages |
| `formula` | on, off | on | Math formula extraction |
| `image_output` | embedded, external, off | external | Image handling mode |
| `image_desc` | on, off | off | AI image descriptions |
| `sanitize` | on, off | off | PII sanitization |
| `hidden_text` | warn, strip, off | warn | Hidden text handling |
| `hybrid` | auto, local, full | auto | Processing route |

## Integration with Other Skills

After conversion, other authorkit skills automatically prefer md files:

```
/authorkit-juice ref         <- Convert reference to md
/authorkit-analyze ref         <- Now reads from converted/ref-001/*.md (fast!)
/authorkit-compare ch3         <- Reads md instead of PDF (low tokens!)
/authorkit-draft 3-1           <- References md for content (efficient!)
```

The `analyze` skill checks for converted md files first.
If found, it reads from md instead of the original format.

## Dependencies

Required Python packages:
- `pymupdf` (fitz) -- PDF text + image extraction + OCR
- `python-docx` -- docx text + image extraction
- `Pillow` -- Image processing
- `openpyxl` -- xlsx support (if needed)

Optional (for enhanced features):
- `paddlepaddle` + `paddleocr` -- **Recommended for Korean/CJK OCR** (GPU acceleration, built-in angle correction)
- `easyocr` -- Advanced OCR (80+ languages)
- `pix2tex` -- Formula image to LaTeX conversion

Install:
```bash
# Core
pip install pymupdf python-docx Pillow openpyxl

# Optional: PaddleOCR (recommended for Korean PDFs)
pip install paddlepaddle paddleocr

# Optional: enhanced OCR and formula extraction
pip install easyocr pix2tex
```
