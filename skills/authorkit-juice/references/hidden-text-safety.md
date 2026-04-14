# Hidden Text Safety

PDFs can contain text that renders invisibly but is still extracted by
`page.get_text()`. Three attack/corruption classes to detect:

1. **Prompt injection** — attacker hides instructions in white-on-white
   or 0-point text hoping a downstream LLM will execute them
2. **Watermark leakage** — invisible tracking strings added by the
   original document tool
3. **Accidental corruption** — authoring-tool bugs that leave orphaned
   layers in the text stream

## Detection

`scripts/convert_pdf.py::_detect_hidden_text` walks the page dict and
flags spans that are either:

- **Near-zero size**: `span["size"] < 0.5` — too small to be visible at
  any reasonable rendering DPI
- **White foreground**: `span["color"] == 0xFFFFFF` — white text that
  renders invisibly on the default white background

Spans must have non-empty stripped text to count (pure whitespace is
ignored).

## Reporting

Each run writes a warning line to `conversion-log.md`:

```
- **⚠ Hidden text warning**: 12 spans across 9 page(s) — [23, 24, 25, …]
```

or, when clean:

```
- **Hidden text warning**: none
```

The warning is informational — the script does **not** strip the hidden
content from `full.md`. Downstream consumers should decide whether to:

- Accept (legitimate watermarks, font-size noise from authoring tools)
- Strip (treat as untrusted)
- Escalate (manual review before feeding to an LLM)

## Known false positives

- Footer page numbers in tiny fonts (e.g., 0.4pt artifacts from poor
  export settings). These are benign but noisy.
- White text used for accessibility anchors in some government PDFs
- Decorative glyphs that happen to be white

To reduce noise, either raise the threshold (e.g. `size < 0.3`) or add
a block-level check that the hidden span is inside a rect that overlaps
visible content.

## What this does NOT catch

- Text written at extreme opacity (`alpha < 0.05`) — requires parsing
  the graphics state, not available in the text dict
- Text outside the page mediabox (placed at negative coordinates)
- Rotated/upside-down text that is technically visible but hard for
  humans to read
- Text embedded inside images (those go through OCR, not this path)

If you need deep content-safety guarantees, combine this with a render
diff: compare `page.get_text()` output against a VLM transcription of
the rendered page. Anything present only in the former is suspect.
