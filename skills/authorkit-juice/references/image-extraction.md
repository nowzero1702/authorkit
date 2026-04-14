# Image Extraction

Rules and rationale for extracting body figures from PDFs while
filtering out decorative elements.

## Decoration filter: `MIN_IMG_WIDTH = 300`

PDFs routinely embed dozens of tiny decorative images on cover pages
and section dividers: logo fragments, background gradients, bullet
glyphs. A real body figure in a KISA document is almost always wider
than 300px.

Calibration example (스마트시티 보안모델 PART_1.pdf):

| Range | Images without filter | With `width >= 300` |
|---|---:|---:|
| p.1 (cover) | 48 (all decoration) | 0 |
| p.21-40 (body) | 24 | 24 |

The cutoff is conservative. If you need to keep smaller figures (e.g.
icons used inline with text), lower `MIN_IMG_WIDTH` or switch to a
multi-signal filter (aspect ratio, color count, presence in text flow).

## Caption-to-image matching

`_find_caption_for_image(page, img_rect)` searches all text blocks on
the same page that match `CAPTION_PATTERNS` (see
`korean-pdf-patterns.md`) and picks the one closest to the image along
the vertical axis.

```
for each caption block B:
    if B is fully below image:    dist = B.y0 - image.y1
    elif B is fully above image:  dist = image.y0 - B.y1
    else (B overlaps image):       dist = 0
    if dist <= 120pt: candidate
pick candidate with smallest dist
```

**Why 120pt?** In A4 single-column layouts a caption typically sits
within 30–80pt of its image. 120pt gives slack for looser layouts and
for multi-line captions where `y0` is further away. Wider windows
start producing wrong matches when a page has multiple figures.

The 120pt window is **vertical only**. Horizontal overlap is not
required — this is intentional so that centered captions still match
left-anchored images.

## Embedded image rect resolution

`page.get_image_rects(xref)` returns the placement rectangle(s) for a
given image reference. A single image can be reused in multiple rects
(watermarks, repeating icons). The current script uses the first rect,
which is correct for body figures — they're placed once per page.

If you need the exact rect per occurrence, iterate
`page.get_image_info()` and match by bbox instead.

## CMYK handling

```python
pix = fitz.Pixmap(doc, xref)
if pix.n >= 5:                          # CMYK + alpha
    pix = fitz.Pixmap(fitz.csRGB, pix)  # convert to RGB
pix.save(path)
```

Korean government PDFs produced from InDesign often embed CMYK images.
Skipping this conversion causes PyMuPDF to raise or save unreadable PNGs.

## File naming convention

```
p{page:04d}_img{idx}_{width}x{height}.png
```

Example: `p0023_img0_1640x853.png`

- 4-digit page zero-pad keeps `ls` output naturally ordered
- Including dimensions in the filename helps during review; you can
  spot the decoration filter working correctly at a glance
- Per-page `img{idx}` comes from the PDF's internal order (top-to-bottom
  usually, but not guaranteed)
