---
name: authorkit-restructure
description: Analyze and reorder manuscript chapters/sections based on coherence, prerequisite dependencies, and gap prevention. Uses dependency graph and topological sort to suggest optimal ordering. Use when "reorder", "restructure", "reorganize", "change section order".
---

# authorkit.restructure — Structure Reorganization

Analyzes manuscript chapter/section ordering and suggests restructuring.

## Tasks Performed

### 1. Current Structure Analysis
Identifies core concepts and prerequisite dependencies for each section.

### 2. Dependency Graph
Models inter-section dependencies as a directed graph.

### 3. Coherence Verification
Detects where current ordering breaks dependencies:
- If A depends on B, then B must come before A
- "As we learned earlier" references must actually be earlier

### 4. Reordering Suggestion
Uses topological sort for valid ordering.
Tiebreakers: reference ordering → ascending difficulty → volume balance.

### 5. Impact Analysis
Lists all cross-references that need updating after reordering.

### 6. Apply Mode
- Renames draft folders to match new ordering
- Updates structure.md
- Generates cross-reference fix list

## Circular Dependency Detection

If A → B → A cycles are found:
1. Reports the cycle to the author
2. Asks which dependency to break
3. Proceeds with author's choice

## Output

`authorkit/restructure/proposal-[DATE].md` (reordering proposal)
`authorkit/restructure/impact-[DATE].md` (impact analysis)
