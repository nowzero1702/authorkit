# Output Format

Every juice run produces the following layout under `<output_dir>`:

```
<output_dir>/
├── full.md              # converted markdown
├── conversion-log.md    # run metadata + image mapping
└── images/
    ├── p0021_img0_508x287.png
    ├── p0022_img0_800x535.png
    └── ...
```

## `full.md` structure

- H1: source filename
- Frontmatter block quote: conversion timestamp, page range, ref ID
- Body: per-page sections separated by `---` and a `<!-- Page N -->`
  comment
- Headings promoted from block text via patterns in
  `korean-pdf-patterns.md`
- Images inserted inline at their page position with captioned alt text
  when a caption was matched:

```markdown
![그림 1 스마트시티에 가장 많이 적용된 기술](images/p0023_img0_1640x853.png)
*그림 1 스마트시티에 가장 많이 적용된 기술*
```

When no caption was matched the alt text falls back to
`image {page}-{idx}`.

## `conversion-log.md` structure

Required bullets:

```markdown
- **Source**: <filename>
- **Ref ID**: <ref_id>
- **Pages (total)**: N
- **Pages (converted)**: from-to
- **Converted**: YYYY-MM-DD HH:MM
- **Text characters**: N,NNN
- **Images kept**: K (min width 300px)
- **Images skipped (decoration)**: S
- **Headings detected**: H
- **Images with caption**: C / K
- **Hidden text warning**: none | N spans across M page(s) — [pages]
```

Followed by an **Image Mapping** section that is critical for
downstream review:

```markdown
## Image Mapping

| Image File | Page | Caption |
|---|---:|---|
| `p0023_img0_1640x853.png` | 23 | 그림 1 스마트시티에 … |
| `p0024_img0_2205x956.png` | 24 | 그림 2 제1차~제3차 스마트도시 … |
| `p0028_img0_424x275.png` | 28 | _(none)_ |
```

Use this table when editing `full.md` by hand — it answers "which
source page did this figure come from?" without re-opening the PDF.

## Page range semantics

- `--from N --to M` is **1-based and inclusive on both ends**
- Omitting both flags converts the entire document
- The script clamps `--to` to `total_pages` so you can safely pass
  `--to 9999` to mean "until the end"

## Image file naming

```
p{page:04d}_img{idx}_{width}x{height}.png
```

Zero-padding to 4 digits keeps filesystem sort order aligned with page
order up to 9999 pages. For longer documents, bump to 5 digits in
`convert_pdf.py` (single constant change).

## Per-chapter split (not yet implemented)

The juice spec calls for optional per-chapter output (`ch01.md`,
`ch02.md`). The current reference implementation does not split —
everything goes into `full.md`. To add splitting, detect `^## 제?\s*\d+장`
headings during the extraction loop and emit each section to its own
file while still maintaining `full.md` as a complete copy.
