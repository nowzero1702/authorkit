---
name: juice
description: Juice (extract) reference or manuscript files (pdf, docx, hwpx) into clean markdown with embedded images. Squeezes out the essential text and figures, discarding layout noise to dramatically reduce token consumption. Use when "juice the reference", "extract to md", "squeeze into markdown", "reduce token usage".
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

Converting once and working from md saves significant tokens across
analyze, compare, draft, and review operations.

## Usage Examples

```
"Convert the reference PDF to markdown"
"Convert pages 250-350 of the textbook to md"
"Convert chapter 3 of my manuscript to markdown with images"
"Convert everything to md"
```

## Execution Flow

### 1. Input Selection

User specifies:
- **File**: Which file to convert
- **Range** (optional): Page range, chapter range, or "all"
  - Pages: "pages 10-50"
  - Chapters: "chapter 3" or "ch3-ch5"
  - All: entire file (default)

### 2. Text Extraction

Based on file format:

**PDF (using pymupdf/fitz):**
```python
import fitz
doc = fitz.open('reference.pdf')
for page_num in range(start, end):
    page = doc[page_num]
    text = page.get_text("text")
    # Structure detection: headings, paragraphs, captions
```

**docx (using python-docx):**
```python
from docx import Document
doc = Document('manuscript.docx')
for para in doc.paragraphs:
    style = para.style.name  # Heading 1, Normal, Caption, etc.
    text = para.text
    # Convert styles to markdown: Heading → #, Bold → **, etc.
```

**hwpx (using zipfile + XML):**
```python
import zipfile
with zipfile.ZipFile('document.hwpx') as z:
    # Parse Contents/section0.xml
    # Extract text from paragraph tags
```

### 3. Image Extraction

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
    if pix.n >= 5:  # CMYK → RGB
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

### 4. Markdown Assembly

Combines extracted text and images into a clean md file.

**Conversion rules:**
- Headings → `#`, `##`, `###` based on level
- Bold → `**text**`
- Lists → `- item`
- Images → `![caption](images/filename.png)`
- Tables → markdown table syntax
- Code → ``` code blocks ```
- Captions → `[Figure] caption text` below image

**Image placement:**
- Images are placed at their original position in the text flow
- If an image has a caption (e.g., "FIGURE 4.1 ..."), it's placed below the image reference
- If no caption, surrounding context is used as alt text

### 5. Output

```
authorkit/converted/
├── ref-001/
│   ├── full.md                    ← Complete converted file
│   ├── ch01.md                    ← Per-chapter (if structure detected)
│   ├── ch02.md
│   ├── images/
│   │   ├── p10_img0.png
│   │   ├── p10_img1.png
│   │   ├── p15_img0.png
│   │   └── ...
│   └── conversion-log.md         ← Conversion metadata
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
- Images: 23 extracted
- Headings detected: 18

## Image Mapping
| Image File | Source Page | Caption |
|-----------|:----------:|---------|
| p252_img0.png | 252 | FIGURE 4.1 An abstract view... |
| p255_img0.png | 255 | FIGURE 4.2 The basic implementation... |
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

## Integration with Other Skills

After conversion, other authorkit skills automatically prefer md files:

```
/authorkit.juice ref         ← Convert reference to md
/authorkit.analyze ref         ← Now reads from converted/ref-001/*.md (fast!)
/authorkit.compare ch3         ← Reads md instead of PDF (low tokens!)
/authorkit.draft 3-1           ← References md for content (efficient!)
```

The `analyze` skill checks for converted md files first.
If found, it reads from md instead of the original format.

## Dependencies

Required Python packages:
- `pymupdf` (fitz) — PDF text + image extraction
- `python-docx` — docx text + image extraction
- `Pillow` — Image processing
- `openpyxl` — xlsx support (if needed)

Install:
```bash
pip install pymupdf python-docx Pillow openpyxl
```
