---
name: analyze
description: Analyze reference or manuscript files to extract structure (TOC/headings), figures/diagrams list, key concepts/terminology, and issues. Supports pdf, docx, txt, xlsx, hwpx formats. Use when "analyze reference", "analyze manuscript", "extract structure", "list figures".
---

# authorkit.analyze — Reference/Manuscript Analysis

Analyzes reference or manuscript files to extract structure, figures, key concepts, and issues.

## Usage Examples

- "Analyze the reference" → Full reference analysis
- "Analyze chapter 4 of the manuscript" → Specific chapter
- "Extract structure from this PDF" → Specific file

## Tasks Performed

### 1. Structure Extraction
Extracts TOC/heading structure based on file format:
- PDF: Pattern matching for "Chapter", section numbers
- docx: Heading style-based extraction
- hwpx: ZIP extraction → XML parsing
- txt/md: Markdown heading (#) parsing

### 2. Figures/Diagrams List
- With captions: Caption-based extraction
- Without captions: Scans body text for diagrammable concepts
  - Sequential patterns (Step 1, Step 2, First/Then/Next)
  - Comparison patterns (A vs B, pros/cons)
  - Flow patterns (→, leads to, results in)
  - Component patterns (consists of, three types)

### 3. Key Concepts/Terminology
Detects: parenthetical notation, bilingual terms, bold/emphasis, abbreviation definitions

### 4. Volume Analysis
Line count/word count per section

### 5. Issue Detection
Empty sections, numbering mismatches, terminology inconsistency, broken cross-references, forward references

## Output

Results saved to `authorkit/references/ref-XXX/analysis.md` or `authorkit/manuscript/analysis.md`.
For PDFs, figure pages are extracted as individual PDFs in `figures/` folder.

## Supported Formats

| Format | Processing Method |
|--------|------------------|
| .pdf | pypdf + pdfplumber |
| .docx | python-docx |
| .txt | Direct read (UTF-8) |
| .xlsx | openpyxl |
| .hwpx | ZIP extraction → XML parsing |
| .md | Direct read (heading parsing) |
