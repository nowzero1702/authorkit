---
name: authorkit-juice
description: Juice (extract) reference or manuscript files (pdf, docx, hwpx) into clean markdown with embedded images. Supports advanced table extraction (bordered + borderless), reading order correction, OCR for scanned documents, math/formula extraction (LaTeX), structured JSON output, caption-aware image alt text, hidden text safety warnings, and hybrid AI-enhanced processing. Use when "juice the reference", "extract to md", "squeeze into markdown", "reduce token usage".
---

# authorkit-juice — Juice into Markdown

Converts reference or manuscript files to markdown format with embedded
images. This dramatically reduces token consumption for subsequent
authorkit operations by eliminating the need to re-parse binary formats.

## Why Convert?

| Format | Token Cost | Noise |
|---|:-:|:-:|
| PDF | High | Layout headers, footers, page numbers |
| docx | Medium | XML overhead, style metadata |
| **md** | **Low** | Clean text, no noise |
| **json** | **Low** | Structured with bounding boxes |

Converting once and working from md saves significant tokens across
analyze, compare, draft, and review operations.

## Quick start

```bash
# Install (core)
pip install pymupdf python-docx Pillow

# Convert a full PDF
python scripts/convert_pdf.py path/to/reference.pdf authorkit/converted/ref-001 ref-001

# Convert a page range (safer for huge PDFs)
python scripts/convert_pdf.py path/to/reference.pdf authorkit/converted/ref-001 ref-001 --from 21 --to 40

# Scanned PDF (Korean) via PaddleOCR
pip install paddlepaddle paddleocr
python scripts/convert_pdf_ocr.py path/to/scanned.pdf authorkit/converted/ref-002 ref-002

# Batch convert a directory of PDFs
python scripts/convert_pdf_ocr.py --batch path/to/pdfs/ authorkit/converted/ 1
```

Output lands in `<output_dir>/full.md`, `<output_dir>/images/`, and
`<output_dir>/conversion-log.md`. See
[`references/output-format.md`](references/output-format.md) for the
full layout spec.

## When to use which script

| Script | Use when | Backend |
|---|---|---|
| `scripts/convert_pdf.py` | Text-based PDF (government docs, exports, typeset books) | PyMuPDF blocks |
| `scripts/convert_pdf_ocr.py` | Scanned PDF, low text density, garbled extraction | PaddleOCR (kor) |

The OCR script auto-detects per page whether OCR is needed by checking
Korean character density; pages with enough extractable text bypass OCR.

## Execution Flow

### 1. Input selection

User specifies:
- **File**: which file to convert
- **Range** (optional): `--from N --to M` (1-based, inclusive)
- **Output dir**: where `full.md`, `images/`, `conversion-log.md` go
- **Ref ID**: tag for cross-referencing (e.g. `ref-001`)

### 2. Page triage (hybrid processing)

Before extraction, each page is classified:

| Page Type | Route | Speed |
|---|---|:-:|
| Clean text, simple tables | Local (pymupdf) | Fast (~0.05s/page) |
| Scanned / image-heavy | OCR (PaddleOCR for kor) | Slower |
| Complex borderless tables | AI backend | Slower |
| Math / formula heavy | AI backend | Slower |

```python
def triage_page(page):
    text = page.get_text("text")
    images = page.get_images()
    density = len(text.strip()) / max(page.rect.width * page.rect.height, 1)
    if density < 0.001 and images:
        return "ocr"
    if has_complex_tables(page):
        return "ai_table"
    if has_math_content(text):
        return "ai_formula"
    return "local"
```

When hybrid mode is not available, all pages fall back to local
processing.

### 3. Text extraction — block-level, reading-order aware

Use `page.get_text("blocks")` rather than `"text"`. Raw `"text"` mode
loses paragraph structure and can split each word onto its own line.
Blocks preserve paragraph groupings; sort by `(round(y / 5), x)` to
approximate natural reading order for single-column layouts.

For Korean PDFs, heading promotion and caption detection use the
patterns documented in
[`references/korean-pdf-patterns.md`](references/korean-pdf-patterns.md).
Read that reference when tuning for a new document type.

### 4. Caption-aware image extraction

Each extracted image gets an alt text that matches the PDF's own
caption (e.g. `그림 1 스마트시티에 가장 많이 적용된 기술`) by:

1. Filtering decorative images (`width < 300px`) — see
   [`references/image-extraction.md`](references/image-extraction.md)
2. Locating the image's placement rect via `page.get_image_rects(xref)`
3. Searching text blocks within 120pt vertically for a block whose
   text matches `CAPTION_PATTERNS`
4. Picking the closest match; if none found, falling back to
   `image {page}-{idx}`

This turns `![image 23-0](...)` into
`![그림 1 ...](...)` automatically, which is critical when an LLM
later has to reason about figure references.

### 5. Hidden text safety

Every page is scanned for invisible spans (font size < 0.5 or color
0xFFFFFF) and the count is reported in `conversion-log.md`. This
catches prompt-injection attempts hiding in white-on-white text and
accidental corruption from authoring tools. See
[`references/hidden-text-safety.md`](references/hidden-text-safety.md)
for false-positive modes and mitigation.

### 6. OCR fallback (scanned PDFs)

OCR engine preference for Korean content:

| Language | 1st | 2nd | 3rd |
|---|---|---|---|
| Korean (kor) | **PaddleOCR** | pymupdf (Tesseract) | EasyOCR |
| English (eng) | pymupdf (Tesseract) | PaddleOCR | EasyOCR |
| Japanese/Chinese | **PaddleOCR** | EasyOCR | pymupdf |

PaddleOCR is preferred for Korean because:
- Higher Hangul accuracy than Tesseract
- GPU acceleration for bulk pages
- Built-in angle classification for skewed scans

```python
from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='korean', use_gpu=True)
mat = fitz.Matrix(2.0, 2.0)  # 2x zoom before OCR
pix = page.get_pixmap(matrix=mat)
pix.save(tmp_png)
result = ocr.ocr(tmp_png, cls=True)
# Keep spans with confidence > 0.5
```

Implementation: `scripts/convert_pdf_ocr.py`.

### 7. Advanced extraction (not yet in reference scripts)

These features are part of the juice spec but not yet implemented in
the bundled scripts. Implement as needed per project:

**Reading order correction (XY-Cut)** — recursively split the page by
horizontal/vertical whitespace gaps. Useful for multi-column academic
papers.

**Bordered table extraction** — use `page.get_drawings()` to find cell
borders, build a grid, extract per-cell text with `page.get_text("text", clip=rect)`.

**Borderless table extraction** — cluster text blocks by x-alignment
(columns) and y-alignment (rows) within a tolerance.

**Formula detection** — scan for math fonts in `page.get_text("dict")`
and for math symbol patterns; render the region and pass to a LaTeX
converter (e.g. `pix2tex`).

**Per-chapter split** — detect chapter headings and emit `ch01.md`,
`ch02.md` alongside `full.md`.

**Structured JSON output** — emit `full.json` with element types,
bounding boxes, and per-page structure for downstream RAG indexing.

### 8. Output format

```
authorkit/converted/ref-001/
├── full.md              # converted markdown
├── conversion-log.md    # run metadata + Image Mapping table
└── images/
    ├── p0021_img0_508x287.png
    ├── p0022_img0_800x535.png
    └── ...
```

`conversion-log.md` includes an **Image Mapping** table that answers
"which source page did this figure come from?" without re-opening the
PDF. Full spec:
[`references/output-format.md`](references/output-format.md).

## Range Specification

| Input | Interpretation |
|---|---|
| `--from 10 --to 50` | PDF pages 10 through 50 inclusive |
| `--from 10` (no `--to`) | pages 10 to end of document |
| `--to 50` (no `--from`) | pages 1 through 50 |
| (neither flag) | entire document |

Chapter-based ranges (`chapter 3`, `ch3-ch5`) require a prior
structure scan and are not implemented in the current scripts.

## Options Reference

Current reference scripts expose only the flags below. Options marked
*(spec only)* are part of the juice spec but not yet bundled — treat
as extension points.

| Option | Script | Values | Default |
|---|---|---|---|
| `--from`, `--to` | both | int | none (full doc) |
| `ocr_engine` *(spec only)* | — | auto, paddle, tesseract, easyocr | auto by lang |
| `table_method` *(spec only)* | — | auto, border, cluster | auto |
| `reading_order` *(spec only)* | — | auto, xycut, none | auto |
| `formula` *(spec only)* | — | on, off | on |
| `image_output` | both | external | external |
| `hidden_text` | `convert_pdf.py` | warn (fixed) | warn |

## Integration with other authorkit skills

After conversion, other authorkit skills automatically prefer md files:

```
/authorkit-juice ref        # convert reference to md
/authorkit-analyze ref      # reads converted/ref-001/full.md (fast!)
/authorkit-compare ch3      # reads md instead of PDF (low tokens!)
/authorkit-draft 3-1        # references md for content (efficient!)
```

The `analyze` skill checks for converted md files first. If found, it
reads from md instead of the original format.

## Dependencies

**Core** (required for `convert_pdf.py`):
```bash
pip install pymupdf python-docx Pillow openpyxl
```

**OCR** (required for `convert_pdf_ocr.py`, recommended for Korean):
```bash
pip install paddlepaddle paddleocr
```

**Optional enhancements**:
```bash
pip install easyocr pix2tex   # additional OCR + formula-to-LaTeX
```

## Bundled Resources

- **`scripts/convert_pdf.py`** — text-based PDF converter with caption
  detection, decoration filter, hidden text warning, Image Mapping
- **`scripts/convert_pdf_ocr.py`** — PaddleOCR-backed converter for
  scanned Korean PDFs, supports single-file and batch modes
- **`references/korean-pdf-patterns.md`** — heading + caption regex
  patterns for Korean content, noise filtering tips
- **`references/image-extraction.md`** — `MIN_IMG_WIDTH` rationale,
  caption matching algorithm, CMYK handling
- **`references/hidden-text-safety.md`** — detection logic, false
  positives, mitigation strategies
- **`references/output-format.md`** — full.md structure,
  conversion-log.md schema, file naming conventions

Load references on demand — they are not loaded into context until the
skill routes into a relevant sub-task.
