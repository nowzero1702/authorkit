---
name: authorkit-draft
description: Extract a specific section from the manuscript as old.md, then proofread/rewrite based on constitution rules to generate new.md. Supports 4 levels of proofreading (formatting/enhancement/restructure/rewrite). Use when "proofread", "draft section", "old/new comparison", "rewrite".
---

# authorkit.draft — Section-Level Drafting/Proofreading

Extracts a manuscript section into old/new comparison format for proofreading or rewriting.

## Usage Examples

- "Proofread section 5-1" → Auto-determine level
- "Just fix formatting in 5-1" → Level 1
- "Rewrite 6-1 from scratch" → Level 4

## 4 Proofreading Levels

| Level | Name | Scope |
|:-----:|------|-------|
| 1 | Formatting | Spacing, terminology, notation only |
| 2 | Enhancement | Add text block diagrams, supplementary explanations |
| 3 | Restructure | Add/remove/reorder subsections |
| 4 | Rewrite | Full rewrite preserving good analogies/examples |

If no level specified, auto-determined based on manuscript state.

## Execution Flow

1. Extract target section from manuscript → `drafts/chXX/section-old.md`
2. Proofread/rewrite per constitution + glossary → `drafts/chXX/section-new.md`
3. If compare results exist, incorporate reference content
4. Insert text block diagrams where needed
5. Output change summary table

## Version Management

On re-run:
- Current new → becomes old
- New revision → becomes new
- Previous old → archived to past/

## Style Application

Automatically applies constitution.md rules:
- Sentence endings, honorific level, terminology format, supplementary element style
