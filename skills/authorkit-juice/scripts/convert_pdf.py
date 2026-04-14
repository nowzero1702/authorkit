#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""authorkit-juice reference implementation: PDF → Markdown.

Block-level text extraction + decorative image filter + page range split
+ caption-aware alt text + hidden text warning + Image Mapping report.

Usage:
    python convert_pdf.py <pdf_path> <output_dir> <ref_id> [--from N] [--to M]

See references/ for the rationale behind each heuristic.
"""

import argparse
import os
import re
from datetime import datetime

import fitz  # pymupdf

MIN_IMG_WIDTH = 300  # images narrower than this are treated as decoration
CAPTION_PATTERNS = [
    re.compile(
        r"^\[?\s*(그림|표|도표|figure|fig\.?|table)\s*\d+[\]\.:]?",
        re.IGNORECASE,
    ),
]


def _format_line(line: str) -> str:
    """Promote Korean/English heading patterns to markdown headings."""
    s = line.strip()
    if not s:
        return ""
    if re.match(r"^제?\s*\d+장", s) or re.match(r"^\d+\.\s+[가-힣]", s):
        return f"\n## {s}\n"
    if re.match(r"^\d+\.\d+\s+[가-힣]", s) or re.match(r"^[가-힣]+\s*\d+\.\s", s):
        return f"\n### {s}\n"
    if re.match(r"^\d+\.\d+\.\d+", s):
        return f"\n#### {s}\n"
    return s


def _looks_like_caption(text: str):
    """Return the matching line if any line in the block matches a caption pattern."""
    for line in text.strip().splitlines():
        line = line.strip()
        if any(p.match(line) for p in CAPTION_PATTERNS):
            return line
    return None


def _find_caption_for_image(page, img_rect):
    """Search within 120pt above/below the image for a caption-like block."""
    if img_rect is None:
        return None
    candidates = []
    for b in page.get_text("blocks"):
        y0, y1, text = b[1], b[3], b[4].strip()
        if not text or not _looks_like_caption(text):
            continue
        if y0 >= img_rect.y1:
            dist = y0 - img_rect.y1
        elif y1 <= img_rect.y0:
            dist = img_rect.y0 - y1
        else:
            dist = 0
        if dist <= 120:
            merged = " ".join(l.strip() for l in text.splitlines() if l.strip())
            candidates.append((dist, merged))
    if not candidates:
        return None
    candidates.sort(key=lambda t: t[0])
    return candidates[0][1]


def _image_rect(page, xref):
    try:
        rects = page.get_image_rects(xref)
        return rects[0] if rects else None
    except Exception:
        return None


def _detect_hidden_text(page) -> int:
    """Count spans that are invisibly small or white-on-white."""
    hidden = 0
    try:
        d = page.get_text("dict")
    except Exception:
        return 0
    for block in d.get("blocks", []):
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                size = span.get("size", 12)
                color = span.get("color", 0)
                if (size < 0.5 or color == 0xFFFFFF) and span.get("text", "").strip():
                    hidden += 1
    return hidden


def extract_pdf_to_markdown(pdf_path, output_dir, ref_id, page_from=None, page_to=None):
    doc = fitz.open(pdf_path)
    total_pages = doc.page_count
    p_from = (page_from or 1) - 1
    p_to = min(page_to or total_pages, total_pages)

    images_dir = os.path.join(output_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    all_chunks = []
    image_mapping = []
    image_count = 0
    skipped_images = 0
    headings_detected = 0
    hidden_spans_total = 0
    pages_with_hidden = []

    print(f"Processing: {os.path.basename(pdf_path)}")
    print(f"Total pages: {total_pages}, range: {p_from + 1}-{p_to}")

    for page_num in range(p_from, p_to):
        page = doc[page_num]

        hidden = _detect_hidden_text(page)
        if hidden:
            hidden_spans_total += hidden
            pages_with_hidden.append(page_num + 1)

        blocks = page.get_text("blocks")
        blocks.sort(key=lambda b: (round(b[1] / 5), b[0]))

        lines_out = []
        for b in blocks:
            text = b[4].strip()
            if not text:
                continue
            formatted = _format_line(text)
            if formatted.startswith("\n#"):
                headings_detected += 1
            lines_out.append(formatted)

        for img_idx, img in enumerate(page.get_images(full=True)):
            xref, _, w, h = img[0], img[1], img[2], img[3]
            if w < MIN_IMG_WIDTH:
                skipped_images += 1
                continue
            try:
                pix = fitz.Pixmap(doc, xref)
                if pix.n >= 5:
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                name = f"p{page_num + 1:04d}_img{img_idx}_{w}x{h}.png"
                pix.save(os.path.join(images_dir, name))
                pix = None
                image_count += 1

                caption = _find_caption_for_image(page, _image_rect(page, xref))
                alt = caption or f"image {page_num + 1}-{img_idx}"
                image_mapping.append((name, page_num + 1, caption or ""))
                lines_out.append(f"\n![{alt}](images/{name})\n")
                if caption:
                    lines_out.append(f"*{caption}*\n")
            except Exception as e:
                print(f"  Warning: page {page_num + 1} image {img_idx}: {e}")

        page_md = "\n".join(lines_out)
        all_chunks.append(f"\n---\n<!-- Page {page_num + 1} -->\n{page_md}")

        if (page_num + 1) % 50 == 0:
            print(f"  Processed {page_num + 1}/{total_pages} pages...")

    doc.close()

    full_md = "\n".join(all_chunks)
    full_md_path = os.path.join(output_dir, "full.md")
    with open(full_md_path, "w", encoding="utf-8") as f:
        f.write(f"# {os.path.basename(pdf_path)}\n\n")
        f.write(f"> Converted: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"> Range: p.{p_from + 1}-{p_to} / {total_pages}\n")
        f.write(f"> Ref ID: {ref_id}\n\n")
        f.write(full_md)

    log_path = os.path.join(output_dir, "conversion-log.md")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("# Conversion Log\n\n")
        f.write(f"- **Source**: {os.path.basename(pdf_path)}\n")
        f.write(f"- **Ref ID**: {ref_id}\n")
        f.write(f"- **Pages (total)**: {total_pages}\n")
        f.write(f"- **Pages (converted)**: {p_from + 1}-{p_to}\n")
        f.write(f"- **Converted**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"- **Text characters**: {len(full_md):,}\n")
        f.write(f"- **Images kept**: {image_count} (min width {MIN_IMG_WIDTH}px)\n")
        f.write(f"- **Images skipped (decoration)**: {skipped_images}\n")
        f.write(f"- **Headings detected**: {headings_detected}\n")
        captioned = sum(1 for _, _, c in image_mapping if c)
        f.write(f"- **Images with caption**: {captioned} / {image_count}\n")
        if hidden_spans_total:
            f.write(
                f"- **⚠ Hidden text warning**: {hidden_spans_total} spans across "
                f"{len(pages_with_hidden)} page(s) — {pages_with_hidden[:10]}"
                f"{'…' if len(pages_with_hidden) > 10 else ''}\n"
            )
        else:
            f.write("- **Hidden text warning**: none\n")
        f.write("\n## Output Files\n\n")
        f.write("- `full.md` — converted markdown\n")
        f.write(f"- `images/` — {image_count} body images\n")

        if image_mapping:
            f.write("\n## Image Mapping\n\n")
            f.write("| Image File | Page | Caption |\n")
            f.write("|---|---:|---|\n")
            for name, page, caption in image_mapping:
                cap = caption.replace("|", "\\|") if caption else "_(none)_"
                f.write(f"| `{name}` | {page} | {cap} |\n")

    print(
        f"Done. chars={len(full_md):,} images={image_count} "
        f"(skipped {skipped_images}) headings={headings_detected} "
        f"hidden_spans={hidden_spans_total}"
    )
    return {
        "pages_total": total_pages,
        "pages_converted": p_to - p_from,
        "characters": len(full_md),
        "images": image_count,
        "images_skipped": skipped_images,
        "headings": headings_detected,
        "hidden_spans": hidden_spans_total,
        "captioned_images": sum(1 for _, _, c in image_mapping if c),
    }


def main():
    ap = argparse.ArgumentParser(description="authorkit-juice PDF → Markdown")
    ap.add_argument("pdf_path")
    ap.add_argument("output_dir")
    ap.add_argument("ref_id")
    ap.add_argument("--from", dest="page_from", type=int, default=None, help="start page (1-based)")
    ap.add_argument("--to", dest="page_to", type=int, default=None, help="end page (inclusive)")
    args = ap.parse_args()
    extract_pdf_to_markdown(
        args.pdf_path, args.output_dir, args.ref_id,
        page_from=args.page_from, page_to=args.page_to,
    )


if __name__ == "__main__":
    main()
