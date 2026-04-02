---
name: authorkit-review
description: Verify manuscript against constitution and glossary for writing style, terminology consistency, cross-reference accuracy, and coherence. Outputs severity-graded report with auto-fix suggestions. Use when "verify", "review", "check style", "check terminology", "check cross-references".
---

# authorkit.review — Style/Terminology/Structure Verification

Verifies manuscript against constitution and glossary standards.

## 4 Verification Areas

### 1. Style (style)
- Sentence endings, honorific level, supplementary element style
- Compared against constitution.md standards

### 2. Terminology (glossary)
- First-appearance format, subsequent format, duplicate translations, unregistered terms
- Compared against glossary.md standards

### 3. Cross-References (xref)
- Chapter/section reference number accuracy
- Forward references, backward references, figure references

### 4. Coherence (coherence)
- Prerequisite ordering, forward reference contradictions, promise fulfillment
- Depth consistency, analogy consistency, intro/summary presence

## Usage Examples

- "Review everything" → All 4 areas
- "Check style in section 6-2" → Specific section + style only
- "Check terminology consistency" → Full manuscript + terminology only

## Output

3-severity-level (high/medium/low) comprehensive report.
Auto-fixable items are flagged with `/authorkit-draft [section] formatting` suggestion.

Reports saved to `authorkit/reviews/review-[DATE].md`
