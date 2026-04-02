---
name: authorkit-compare
description: Compare reference analysis with manuscript analysis to classify content (adopt/skip/original), map figures, and verify coherence. Use when "compare reference", "cross-reference analysis", "content comparison", "figure mapping".
---

# authorkit.compare — Reference ↔ Manuscript Comparison

Compares references and manuscript to classify content, map figures, and verify coherence.

## Prerequisites

`/authorkit.analyze` must have been run on both references and manuscript.

## Tasks Performed

### 1. Structure Comparison Table
Side-by-side comparison of reference chapters vs manuscript chapters.

### 2. Content Classification
For each chapter/section, classify into three categories:
- **Adopt**: Content to reference from the source and incorporate
- **Skip**: Content beyond target audience level or out of scope
- **Original**: Content not in reference but needed in manuscript

### 3. Figure Mapping
Maps reference figures to manuscript placement locations.
Determines handling method: simplify, convert to text block diagram, create original.

### 4. Coherence Verification
- Prerequisite ordering: Does B come before A when A depends on B?
- Forward references: No referencing unexplained concepts
- Gaps: No missing core concepts
- Depth consistency: No uneven detail levels across similar topics

### 5. Section Reordering Suggestion
Suggests reordering if serious coherence issues are found.

## Multi-Reference Support

When multiple references exist, each is compared separately, then a unified view is provided.

## Output

`authorkit/drafts/chXX/compare.md` or `authorkit/compare-overview.md`
