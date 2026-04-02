---
name: authorkit-init
description: Initialize a book authoring project. Generates a questionnaire md file for the author to fill out in their IDE, then sets up project structure (constitution, glossary, structure). Use when "start writing a book", "initialize authorkit", "set up authoring project".
---

# authorkit.init — Project Initialization

This skill sets up the initial environment for a book authoring project.
Instead of asking questions in the console, it generates a questionnaire md file
that authors can comfortably fill out in their IDE.

## Execution Flow

### First Run — Generate Questionnaire

If `authorkit/setup-questionnaire.md` does not exist:

1. Create `authorkit/` directory
2. Save the questionnaire template to `authorkit/setup-questionnaire.md`
3. Inform the user: "Questionnaire has been created. Open it in your IDE, fill in your answers, then run this command again."

### Second Run — Parse Answers & Setup

If the questionnaire file exists and answers are filled in:

1. Parse `authorkit/setup-questionnaire.md`
   - Read checkbox `[x]` items
   - Read `> Answer:` text below each question
   - Validate file paths
2. Validate: halt if required fields are missing
3. Generate project structure:
   - `authorkit/constitution.md` — Writing style & terminology rules
   - `authorkit/glossary.md` — Terminology glossary draft
   - `authorkit/structure.md` — Table of contents structure
   - `authorkit/references/` — Reference path record
   - `authorkit/manuscript/` — Manuscript path record
   - `authorkit/drafts/` — Chapter folders based on TOC
4. If existing manuscript provided: auto-analyze writing style → populate constitution
5. Completion message with next steps guide

## Questionnaire Template

```markdown
# authorkit Setup Questionnaire

> Fill in your answers below each `> Answer:` line.
> After completing, run `/authorkit-init` again to finalize setup.

## 1. Work Type
- [ ] Write a new book based on references
- [ ] Continue writing / proofread an existing manuscript
- [ ] Both (reference + existing manuscript improvement)

## 2. Book Category
- [ ] Academic/Technical textbook (e.g., Computer Architecture, OS)
- [ ] Practical/Educational guide (e.g., Excel for Beginners)
- [ ] General non-fiction (e.g., Essays, History)

## 3. Target Audience
> Answer:

## 4. Book Title (tentative)
> Answer:

## 5. Reference Materials
Provide the folder path containing reference files.
Supported formats: pdf, docx, txt, xlsx, hwpx
If no folder, provide file names directly. Enter "none" if no references.
> Answer:

## 6. Existing Manuscript
Provide the folder path containing your manuscript.
Supported formats: pdf, docx, txt, xlsx, hwpx, md
If no folder, provide file names directly. Enter "none" if no manuscript.
> Answer:

## 7. Table of Contents
- [ ] Available (write below or provide file path)
- [ ] Not available (I'd like suggestions based on references)
> Answer:

## 8. Writing Style
Leave blank if you have an existing manuscript — it will be auto-analyzed.

Sentence endings (e.g., formal, casual, academic):
> Answer:

Honorific level (if applicable for your language):
> Answer:

Special elements (e.g., tip boxes, warning boxes, exercises):
> Answer:

Terminology format (e.g., "Korean(English, Abbrev)"):
> Answer:

## 9. Working Directory
Leave blank to create `authorkit/` in the current project root.
> Answer:
```

## Category-Based Default Constitution

When no manuscript exists and style settings are blank, defaults are applied by category:

### Academic/Technical
- Formal sentence endings
- Academic tip style
- Terminology: Native language(English, Abbreviation)
- Cross-references: "See Chapter N", "Explained in Section N-M"

### Practical/Educational
- Semi-formal style
- Friendly tip style
- Terminology: Native language(English)

### General Non-fiction
- Flexible style
- Minimal terminology conventions
- Free-form cross-references

## Existing Manuscript Style Analysis

When an existing manuscript is provided, the following are auto-analyzed:
1. Sentence ending frequency
2. Technical terminology formatting patterns
3. Supplementary element patterns (tips, notes, etc.)
4. Honorific level patterns

Results are populated as defaults in constitution.md with a note:
"Auto-analyzed from your manuscript. Edit constitution.md if adjustments are needed."

## Windows Compatibility

- Paths: Both backslash and forward slash supported
- Encoding: UTF-8
- Line endings: Both LF and CRLF parseable
