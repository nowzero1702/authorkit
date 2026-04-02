---
name: authorkit-diagram
description: Generate text block diagrams in markdown code block format. Supports reference-based, content-based, auto-fill for [figure] placeholders, and scan mode. Use when "create diagram", "text block diagram", "draw figure", "find diagrammable parts".
---

# authorkit.diagram — Diagram Creation

Generates text block diagrams in markdown code block format.

## 4 Modes

### 1. Reference-Based
Reconstructs a reference figure as a text block diagram.
- "Convert fig-4.34 to a text block diagram"

### 2. Content-Based
Scans body text for diagrammable patterns and generates diagrams.
Patterns: sequential, comparison, components, data flow, hierarchy, timing.

### 3. Auto-Fill [Figure] Placeholders
Generates diagrams where `[Figure]` text references exist without actual diagrams.

### 4. Scan Mode
Scans a section and suggests parts that would benefit from diagrams.
- "Find diagrammable parts in section 6-2"

## Output Format

All diagrams are output as text block diagrams inside markdown code blocks.

Basic elements:
- Boxes: `┌──┐ │  │ └──┘`
- Arrows: `──▶` (data), `══▶` (highlight), `─ ─▶` (inactive)
- Dividers: `║  ║` (pipeline registers)
- Numbers: `① ② ③`

Complexity auto-adjusts based on target audience level in constitution.