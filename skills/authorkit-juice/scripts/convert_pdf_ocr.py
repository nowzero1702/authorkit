#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""authorkit-juice OCR reference implementation: PDF → Markdown via PaddleOCR.

Use this when the PDF is scanned or has very low extractable text.
Preference order for Korean PDFs: PaddleOCR > Tesseract > EasyOCR.

Usage:
    python convert_pdf_ocr.py <pdf_path> <output_dir> <ref_id>
    python convert_pdf_ocr.py --batch <pdf_dir> <out_base_dir> <start_num>

Dependencies:
    pip install pymupdf paddlepaddle paddleocr
"""

import os
import re
import sys
import tempfile
from datetime import datetime

import fitz  # pymupdf


KOREAN_CHAR = re.compile(r"[가-힣]")
MIN_EMBEDDED_IMG = 50  # drop thumbnails / icons smaller than 50px


def _needs_ocr(text: str) -> bool:
    """Heuristic: low text volume or low Korean density means scanned page."""
    if len(text) < 50:
        return True
    korean_ratio = len(KOREAN_CHAR.findall(text)) / max(len(text), 1)
    return korean_ratio < 0.05


def _promote_heading(line: str) -> str:
    if re.match(r"^제?\s*\d+장", line) or re.match(r"^제?\s*[IVX]+\s*[\.장]", line):
        return f"\n## {line}\n"
    if re.match(r"^\d+\.\s+[가-힣A-Z]", line):
        return f"\n## {line}\n"
    if re.match(r"^\d+\.\d+\s+[가-힣A-Z]", line) or re.match(r"^[가-힣]+\s*\d+\.\s", line):
        return f"\n### {line}\n"
    if re.match(r"^\d+\.\d+\.\d+", line):
        return f"\n#### {line}\n"
    return line


def extract_pdf_with_ocr(pdf_path, output_dir, ref_id):
    from paddleocr import PaddleOCR

    ocr = PaddleOCR(use_angle_cls=True, lang="korean", use_gpu=True, show_log=False)
    doc = fitz.open(pdf_path)
    total_pages = doc.page_count

    images_dir = os.path.join(output_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    all_text = []
    image_count = 0
    headings_detected = 0
    ocr_pages = 0

    print(f"Processing: {os.path.basename(pdf_path)} ({total_pages} pages)")
    print("OCR engine: PaddleOCR (Korean + GPU)")

    for page_num in range(total_pages):
        page = doc[page_num]
        raw_text = page.get_text("text").strip()

        if _needs_ocr(raw_text):
            ocr_pages += 1
            mat = fitz.Matrix(2.0, 2.0)  # 2x zoom boosts OCR accuracy
            pix = page.get_pixmap(matrix=mat)
            tmp = os.path.join(tempfile.gettempdir(), f"_juice_ocr_{page_num}.png")
            pix.save(tmp)
            result = ocr.ocr(tmp, cls=True)
            lines = []
            if result and result[0]:
                for line in result[0]:
                    content = line[1][0]
                    conf = line[1][1]
                    if conf > 0.5:
                        lines.append(content)
            text = "\n".join(lines)
            try:
                os.remove(tmp)
            except OSError:
                pass
        else:
            text = raw_text

        for img_idx, img in enumerate(page.get_images()):
            try:
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.n >= 5:
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                if pix.width < MIN_EMBEDDED_IMG or pix.height < MIN_EMBEDDED_IMG:
                    continue
                name = f"p{page_num + 1:04d}_img{img_idx}.png"
                pix.save(os.path.join(images_dir, name))
                image_count += 1
                text += f"\n\n![image {page_num + 1}-{img_idx}](images/{name})\n"
            except Exception as e:
                print(f"  Warning: page {page_num + 1} img {img_idx}: {e}")

        processed = []
        for line in text.split("\n"):
            s = line.strip()
            if not s:
                processed.append("")
                continue
            promoted = _promote_heading(s)
            if promoted != s:
                headings_detected += 1
            processed.append(promoted)
        all_text.append(f"\n---\n<!-- Page {page_num + 1} -->\n" + "\n".join(processed))

        if (page_num + 1) % 10 == 0:
            print(f"  Processed {page_num + 1}/{total_pages}")

    doc.close()

    full_md = "\n".join(all_text)
    with open(os.path.join(output_dir, "full.md"), "w", encoding="utf-8") as f:
        f.write(f"# {os.path.basename(pdf_path)}\n\n")
        f.write(f"> Converted: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"> Ref ID: {ref_id}\n")
        f.write("> OCR engine: PaddleOCR (Korean + GPU)\n\n")
        f.write(full_md)

    with open(os.path.join(output_dir, "conversion-log.md"), "w", encoding="utf-8") as f:
        f.write("# Conversion Log\n\n")
        f.write(f"- **Source**: {os.path.basename(pdf_path)}\n")
        f.write(f"- **Ref ID**: {ref_id}\n")
        f.write(f"- **Pages**: {total_pages}\n")
        f.write(f"- **OCR pages**: {ocr_pages} / {total_pages}\n")
        f.write(f"- **Converted**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("- **OCR engine**: PaddleOCR (Korean + GPU)\n")
        f.write(f"- **Text characters**: {len(full_md):,}\n")
        f.write(f"- **Images extracted**: {image_count}\n")
        f.write(f"- **Headings detected**: {headings_detected}\n")

    print(
        f"Done. chars={len(full_md):,} images={image_count} "
        f"headings={headings_detected} ocr_pages={ocr_pages}"
    )
    return {
        "pages": total_pages,
        "ocr_pages": ocr_pages,
        "characters": len(full_md),
        "images": image_count,
        "headings": headings_detected,
    }


def _run_batch(pdf_dir, out_base, start_num):
    pdfs = sorted(f for f in os.listdir(pdf_dir) if f.lower().endswith(".pdf"))
    print(f"Found {len(pdfs)} PDFs")
    results = {}
    for i, pdf in enumerate(pdfs):
        ref_id = f"ref-{start_num + i:03d}"
        out_dir = os.path.join(out_base, ref_id)
        os.makedirs(out_dir, exist_ok=True)
        print(f"\n[{i + 1}/{len(pdfs)}] {ref_id}: {pdf}")
        results[ref_id] = {
            **extract_pdf_with_ocr(os.path.join(pdf_dir, pdf), out_dir, ref_id),
            "filename": pdf,
        }
    print("\nBATCH SUMMARY")
    for ref_id, info in results.items():
        print(
            f"  {ref_id}: {info['filename']} | pages={info['pages']} "
            f"chars={info['characters']:,} images={info['images']}"
        )


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    if sys.argv[1] == "--batch":
        _run_batch(sys.argv[2], sys.argv[3], int(sys.argv[4]))
    else:
        os.makedirs(sys.argv[2], exist_ok=True)
        extract_pdf_with_ocr(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    main()
