# authorkit

[English](../README.md) | [한국어](README.ko.md) | [中文](README.zh.md) | [日本語](README.ja.md) | [Русский](README.ru.md) | [Français](README.fr.md) | **Deutsch** | [Español](README.es.md) | [Português](README.pt.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | [Italiano](README.it.md)

**Workflow-Skills zum Verfassen von Büchern für Claude Code.**

Systematisieren Sie die wiederkehrenden Aufgaben beim Schreiben von Büchern: Quellenanalyse, Manuskriptkorrektur, Diagrammerstellung, Stil-/Terminologieprüfung und Strukturneuordnung.

## Skills

| Skill | Beschreibung |
|-------|-------------|
| `init` | Projektinitialisierung (Fragebogen md → Einrichtung) |
| `analyze` | Quellen-/Manuskriptanalyse |
| `compare` | Quellen ↔ Manuskript-Vergleich |
| `draft` | Abschnittsweises Verfassen/Korrekturlesen (alt → neu) |
| `diagram` | Erstellung von Textblockdiagrammen |
| `review` | Stil-/Terminologie-/Strukturprüfung |
| `restructure` | Strukturneuordnung |

## Installation

```
/plugin marketplace add Nowzero/authorkit
/plugin install authorkit@authorkit
```

Für die koreanische Version:
```
/plugin install authorkit-ko@authorkit
```

## Schnellstart

```
/authorkit.init
```

Es wird eine Fragebogen-md-Datei generiert. Tragen Sie Ihre Antworten in Ihrer IDE ein und führen Sie den Befehl erneut aus, um die Einrichtung abzuschließen.

## Unterstützte Dateiformate

- Quellen: pdf, docx, txt, xlsx, hwpx
- Manuskripte: pdf, docx, txt, xlsx, hwpx, md
- Ausgabe: md (mit Textblockdiagrammen)

## Workflow

```
/authorkit.init          Projekt einrichten
       ↓
/authorkit.analyze       Quellen und Manuskript analysieren
       ↓
/authorkit.compare       Quellen ↔ Manuskript vergleichen
       ↓
/authorkit.draft         Abschnitte verfassen/korrigieren (alt → neu)
       ↓
/authorkit.diagram       Textblockdiagramme erstellen
       ↓
/authorkit.review        Stil, Terminologie, Querverweise prüfen
       ↓
/authorkit.restructure   Kapitel-/Abschnittsreihenfolge neuordnen
```

## Sprachversionen

| Plugin | Sprache | Installation |
|--------|---------|-------------|
| `authorkit` | English | `/plugin install authorkit@authorkit` |
| `authorkit-ko` | 한국어 | `/plugin install authorkit-ko@authorkit` |

## Lizenz

Apache 2.0
