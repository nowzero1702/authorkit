# authorkit

[한국어](docs/README.ko.md) | [中文](docs/README.zh.md) | [日本語](docs/README.ja.md) | [Русский](docs/README.ru.md) | [Français](docs/README.fr.md) | [Deutsch](docs/README.de.md) | [Español](docs/README.es.md) | [Português](docs/README.pt.md) | [العربية](docs/README.ar.md) | [हिन्दी](docs/README.hi.md) | [Türkçe](docs/README.tr.md) | [Italiano](docs/README.it.md)

**Book authoring workflow skills for Claude Code.**

Systematize the repetitive tasks of book writing: reference analysis, manuscript proofreading, diagram creation, style/terminology verification, and structure reorganization.

## Skills

| Skill | Description |
|-------|-------------|
| `init` | Project initialization (questionnaire md → setup) |
| `analyze` | Reference/manuscript analysis |
| `compare` | Reference ↔ manuscript comparison |
| `draft` | Section-level drafting/proofreading (old → new) |
| `diagram` | Text block diagram creation |
| `review` | Style/terminology/structure verification |
| `restructure` | Structure reorganization |

## Installation

```
/plugin marketplace add Nowzero/authorkit
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

A questionnaire md file will be generated. Fill in your answers in your IDE, then run the command again to complete setup.

## Supported File Formats

- References: pdf, docx, txt, xlsx, hwpx
- Manuscripts: pdf, docx, txt, xlsx, hwpx, md
- Output: md (with text block diagrams)

## Workflow

```
/authorkit.init          Set up project
       ↓
/authorkit.analyze       Analyze references and manuscript
       ↓
/authorkit.compare       Compare reference ↔ manuscript
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

Apache 2.0
