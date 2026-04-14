# Korean PDF Patterns

Heuristics for juicing Korean-language reference PDFs (government docs,
KISA guides, textbooks). Load this when working on Korean content.

## Heading promotion

`scripts/convert_pdf.py::_format_line` promotes block text to markdown
headings based on these patterns:

| Pattern | Example | Level |
|---|---|---|
| `^제?\s*\d+장` | `제 2 장`, `2장` | `##` |
| `^\d+\.\s+[가-힣]` | `1. 개요` | `##` |
| `^\d+\.\d+\s+[가-힣]` | `1.1 해외 환경` | `###` |
| `^[가-힣]+\s*\d+\.\s` | `표 1. 정책 현황` | `###` |
| `^\d+\.\d+\.\d+` | `1.1.2` | `####` |

Promotion is applied per text block, not per line. For layouts where the
heading shares a block with the first paragraph, the block gets promoted
based on its leading content — usually correct for Korean government PDFs.

## Caption patterns

```python
CAPTION_PATTERNS = [
    re.compile(r"^\[?\s*(그림|표|도표|figure|fig\.?|table)\s*\d+[\]\.:]?",
               re.IGNORECASE),
]
```

Matches all of these:
- `그림 1`
- `[그림 12]`
- `표 1`
- `도표 5`
- `Figure 3:`
- `Fig. 4`
- `Table 7.`

Caption matching is done **per line within the block**, not just the first
line. Korean PDFs commonly store the descriptive title and the `그림 N`
label in the same block (title first, label second), so a first-line-only
check misses them.

See `references/image-extraction.md` for how captions are matched to
images by spatial proximity.

## Body-text noise to ignore

These patterns appear as blocks but are not real body content — filter
or de-prioritize them when doing downstream analysis:

- Footer page numbers: single-digit or 2-3 digit blocks near y > page.rect.height - 50
- Running headers: `제 N 장  <chapter title>` repeated on every page
- Table-of-contents dot leaders: `· · · · · ·` sequences
- Copyright / KISA footer: blocks containing `한국인터넷진흥원` or `KISA` near bottom

The current `convert_pdf.py` leaves these in (to stay faithful). A
downstream cleanup pass can drop them.

## Multi-column edge cases

KISA PDFs are usually single-column, but some appendices use 2-column
layouts. The current block sort `(round(y / 5), x)` handles 2-column
correctly when the column gutter is wide enough. For academic papers or
densely packed 2-column layouts, consider adding XY-Cut reading order
correction — not yet implemented in the reference scripts.

## Encoding gotchas

- PyMuPDF returns text in Unicode, no codec juggling needed
- On Windows, console output may show mojibake for Korean even when file
  writes are fine — always verify by reading the output file, not the stdout
- Some KISA PDFs embed subset fonts that render fine visually but produce
  wrong glyphs via text extraction. If `korean_ratio < 0.05`, fall back
  to OCR (see `convert_pdf_ocr.py::_needs_ocr`)
