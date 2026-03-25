# authorkit

[한국어](docs/README.ko.md) | [中文](docs/README.zh.md) | [日本語](docs/README.ja.md) | [Русский](docs/README.ru.md) | [Français](docs/README.fr.md) | [Deutsch](docs/README.de.md) | [Español](docs/README.es.md) | [Português](docs/README.pt.md) | [العربية](docs/README.ar.md) | [हिन्दी](docs/README.hi.md) | [Türkçe](docs/README.tr.md) | [Italiano](docs/README.it.md)

**Book authoring workflow skills for Claude Code.**

Whether you're writing a university textbook, a practical how-to guide, or translating and adapting a reference book — authorkit systematizes the repetitive tasks of book writing: reference analysis, manuscript proofreading, diagram creation, style/terminology verification, and structure reorganization.

## Who is this for?

- **Professors/Authors** writing academic textbooks with reference books
- **Technical writers** creating practical guides (e.g., "Data Analysis with Python")
- **Translators/Adapters** localizing foreign textbooks for domestic audiences
- **Self-publishers** iterating on their manuscripts

## Installation

```
/plugin marketplace add nowzero1702/authorkit
/plugin install authorkit@authorkit
```

For Korean version:
```
/plugin install authorkit-ko@authorkit
```

## Quick Start

```
/authorkit.init
```

A questionnaire md file is generated. Fill in your answers in your IDE, then run the command again.

---

## Skills & Examples

### `/authorkit.init` — Project Initialization

Sets up your authoring project by generating a questionnaire md file.

**You say:**
> "I'm writing an Operating Systems textbook for 2nd-year undergrads. I have Silberschatz's OS Concepts as a reference."

**authorkit does:**
1. Creates `authorkit/setup-questionnaire.md`:
   ```markdown
   ## 1. Work Type
   - [x] Both (reference + existing manuscript improvement)

   ## 3. Target Audience
   > Answer: 2nd-year undergraduate students, first time learning OS concepts

   ## 5. Reference Materials
   > Answer: C:\Users\...\references
   ```
2. After you fill it in and re-run, generates:
   - `authorkit/constitution.md` — Your writing style rules
   - `authorkit/glossary.md` — Terminology glossary
   - `authorkit/structure.md` — Table of contents
   - `authorkit/drafts/ch01/`, `ch02/`, ... — Chapter folders

---

### `/authorkit.analyze` — Reference/Manuscript Analysis

Extracts structure, figures, key concepts, and issues from any supported file.

**You say:**
> "Analyze the Silberschatz reference book"

**authorkit outputs** (`authorkit/references/ref-001/analysis.md`):
```markdown
## Structure
| Location | Title | Level | Volume |
|----------|-------|:-----:|:------:|
| p.1 | Ch1. Introduction | H1 | 42 pages |
| p.43 | Ch2. Operating-System Structures | H1 | 38 pages |
| p.81 | Ch3. Processes | H1 | 45 pages |
...

## Figures
| ID | Page | Caption | Extracted |
|----|------|---------|:---------:|
| FIG-001 | p.6 | Figure 1.1 Abstract view of system components | ✅ |
| FIG-002 | p.23 | Figure 1.12 Memory layout for a multiprogramming system | ✅ |
...

## Key Terminology
| Term | Abbreviation | First Appearance |
|------|:------------:|-----------------|
| Process Control Block | PCB | Ch3 |
| Context Switch | - | Ch3 |
...

## Issues Found
| Type | Location | Detail |
|------|----------|--------|
| Empty section | Ch7.4 | Heading only, no content |
```

**Supported formats:** pdf, docx, txt, xlsx, hwpx, md

---

### `/authorkit.compare` — Reference ↔ Manuscript Comparison

Compares your manuscript against references to decide what to adopt, skip, or create originally.

**You say:**
> "Compare my Ch3 with Silberschatz Ch3"

**authorkit outputs** (`authorkit/drafts/ch03/compare.md`):
```markdown
## Structure Comparison
| Reference (Silberschatz) | My Manuscript | Mapping |
|-------------------------|---------------|:-------:|
| 3.1 Process Concept | 3-1 프로세스 개념 | Match |
| 3.2 Process Scheduling | 3-2 프로세스 스케줄링 | Match |
| 3.3 Operations on Processes | (missing) | Gap |
| 3.4 Interprocess Communication | 3-4 IPC | Match |

## Content Classification
### Adopt (from reference)
| Reference | Content | Target | Method |
|-----------|---------|--------|--------|
| §3.1 | Process state diagram | 3-1 | Simplify for beginners |
| §3.2 | Scheduling queue figures | 3-2 | Recreate as text block diagram |

### Skip
| Reference | Content | Reason |
|-----------|---------|--------|
| §3.3.2 | Chrome multi-process case study | Too specific, audience won't relate |

### Original Content
| Section | Content | Reason |
|---------|---------|--------|
| 3-1 intro | "Why do we need processes?" motivation | Not in reference, needed for beginners |

## Coherence Issues
| Type | Location | Detail | Severity |
|------|----------|--------|:--------:|
| Forward ref | 3-2 "as we learned in scheduling" | Scheduling not yet taught | High |
```

---

### `/authorkit.draft` — Section-Level Drafting/Proofreading

Extracts a section as `old.md`, rewrites/proofreads it as `new.md`.

**You say:**
> "Proofread section 3-1"

**authorkit creates two files you can compare side-by-side in your IDE:**

`drafts/ch03/3-1-old.md` (extracted from manuscript):
```markdown
## 3-1 프로세스 개념

프로세스는 실행중인 프로그램입니다. 프로세스에는 여러 상태가 있는데
New, Ready, Running, Waiting, Terminated 가 있습니다...
```

`drafts/ch03/3-1-new.md` (proofread):
```markdown
## 3-1 프로세스 개념

프로세스는 실행 중인 프로그램입니다. 프로세스에는 다섯 가지 상태가 있으며,
생성(New), 준비(Ready), 실행(Running), 대기(Waiting), 종료(Terminated)로
나뉩니다...
```

**Change summary:**
| Type | Change | Count |
|------|--------|:-----:|
| Terminology | "실행중인" → "실행 중인" | 3 |
| Terminology format | "New, Ready" → "생성(New), 준비(Ready)" | 5 |
| Spacing | "프로그램입니다.프로세스" → "프로그램입니다. 프로세스" | 2 |

**4 proofreading levels:**
```
"Just fix formatting in 3-1"        → Level 1: formatting only
"Enhance 3-1 with diagrams"         → Level 2: add diagrams, explanations
"Restructure 3-1"                   → Level 3: add/remove/reorder subsections
"Rewrite 3-1 from scratch"          → Level 4: full rewrite
```

---

### `/authorkit.diagram` — Text Block Diagram Creation

Generates text block diagrams in markdown code blocks.

**You say:**
> "Create a diagram for the process state transition"

**authorkit outputs:**
```
[Figure] Process State Transition Diagram (Silberschatz Fig 3.2)

                    admitted              interrupt
  ┌─────┐  ──────────────▶  ┌───────┐  ──────────▶  ┌─────────┐
  │ New │                    │ Ready │               │ Running │
  └─────┘                    └───┬───┘  ◀──────────  └────┬────┘
                                 │      scheduler         │
                                 │      dispatch          │
                                 │                        │
                            I/O or                   exit │
                         event completion                 │
                                 │                        ▼
                            ┌────┴────┐            ┌────────────┐
                            │ Waiting │            │ Terminated │
                            └─────────┘            └────────────┘
```

**4 modes:**
```
"Convert Fig 3.2 to text diagram"       → Reference-based
"Find diagrammable parts in 3-1"        → Scan mode
"Create diagram for the PCB structure"   → Content-based
"Fill in the [Figure] placeholder"       → Auto-fill mode
```

---

### `/authorkit.review` — Style/Terminology/Structure Verification

Verifies your manuscript against constitution and glossary rules.

**You say:**
> "Review chapter 3"

**authorkit outputs** (`authorkit/reviews/review-2025-03-25.md`):
```markdown
# Review Report — Chapter 3

## Summary
| Area | Violations | High | Medium | Low |
|------|:----------:|:----:|:------:|:---:|
| Style | 8 | 0 | 3 | 5 |
| Terminology | 5 | 2 | 1 | 2 |
| Cross-references | 2 | 1 | 1 | 0 |
| Coherence | 1 | 0 | 0 | 1 |
| **Total** | **16** | **3** | **5** | **8** |

## High Severity (fix immediately)
| Location | Found | Expected (glossary) | Type |
|----------|-------|---------------------|------|
| 3-1 line 12 | "프로세스Process" | "프로세스(Process)" | Terminology format |
| 3-2 line 45 | "컨텍스트 스위치" | "문맥 교환(Context Switch)" | Wrong translation |

## Cross-Reference Issues
| Location | Reference | Actual | Status |
|----------|-----------|--------|:------:|
| 3-4 "Ch5에서 설명" | Ch5 Memory | Ch5 exists | ✓ |
| 3-2 "앞서 배운 스케줄링" | Prior section | Not yet taught | ✗ |

## Auto-fixable
The following can be fixed with `/authorkit.draft 3-1 formatting`:
- 5 spacing issues
- 3 terminology format issues
```

---

### `/authorkit.restructure` — Structure Reorganization

Analyzes section ordering and suggests restructuring based on prerequisite dependencies.

**You say:**
> "Analyze chapter 3 structure"

**authorkit outputs:**
```markdown
## Dependency Graph

  3-1 Process Concept
       │
       ├──▶ 3-2 Process Scheduling
       │         │
       │         ▼
       │    3-4 CPU Scheduling
       │
       ▼
  3-3 IPC ──▶ 3-5 Synchronization

## Coherence Violations
| Current Order | Issue |
|---------------|-------|
| 3-4 before 3-2 | 3-4 references scheduling queues from 3-2 |

## Suggested Reordering
| Current | Suggested | Reason |
|---------|-----------|--------|
| 3-1 | 3-1 (keep) | Foundation |
| 3-3 IPC | → 3-2 | Independent of scheduling |
| 3-2 Scheduling | → 3-3 | Prerequisites for 3-4 |
| 3-4 CPU Scheduling | → 3-4 (keep) | Depends on 3-3 |
| 3-5 Sync | → 3-5 (keep) | Depends on IPC |

Impact: 4 cross-references need updating.

Run `/authorkit.restructure apply` to execute.
```

---

## Supported File Formats

| Format | Read | Notes |
|--------|:----:|-------|
| `.pdf` | ✅ | Structure, figures, text extraction |
| `.docx` | ✅ | Headings, styles, images |
| `.txt` | ✅ | Plain text |
| `.xlsx` | ✅ | Sheet-based content |
| `.hwpx` | ✅ | Korean word processor format |
| `.md` | ✅ | Markdown headings |

## Workflow

```
/authorkit.init          Set up project (questionnaire → constitution → glossary)
       ↓
/authorkit.analyze       Analyze references and manuscript
       ↓
/authorkit.compare       Compare reference ↔ manuscript
       ↓
/authorkit.juice       Juice files into clean markdown (token savings)
       ↓
/authorkit.draft         Write/proofread sections (old → new)
       ↓
/authorkit.diagram       Create text block diagrams
       ↓
/authorkit.review        Verify style, terminology, cross-references
       ↓
/authorkit.restructure   Reorganize chapter/section order
```

## Language Versions

| Plugin | Language | Install |
|--------|----------|---------|
| `authorkit` | English | `/plugin install authorkit@authorkit` |
| `authorkit-ko` | 한국어 | `/plugin install authorkit-ko@authorkit` |

## License

MIT
