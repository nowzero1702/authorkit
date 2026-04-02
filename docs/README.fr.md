# authorkit

[English](../README.md) | [한국어](README.ko.md) | [中文](README.zh.md) | [日本語](README.ja.md) | [Русский](README.ru.md) | **Français** | [Deutsch](README.de.md) | [Español](README.es.md) | [Português](README.pt.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | [Italiano](README.it.md)

**Compétences de workflow pour la rédaction de livres avec Claude Code.**

Systématisez les tâches répétitives de l'écriture de livres : analyse de références, relecture de manuscrits, création de diagrammes, vérification du style et de la terminologie, et réorganisation de la structure.

## Compétences

| Compétence | Description |
|------------|-------------|
| `init` | Initialisation du projet (questionnaire md → configuration) |
| `analyze` | Analyse des références et du manuscrit |
| `compare` | Comparaison références ↔ manuscrit |
| `juice` | Conversion de fichiers en Markdown (OCR, extraction de tableaux, formules LaTeX, économie de tokens) |
| `draft` | Rédaction/relecture par section (ancien → nouveau) |
| `diagram` | Création de diagrammes en blocs de texte |
| `review` | Vérification du style, de la terminologie et de la structure |
| `restructure` | Réorganisation de la structure |

## Installation

```
/plugin marketplace add Nowzero/authorkit
/plugin install authorkit@authorkit
```

Pour la version coréenne :
```
/plugin install authorkit-ko@authorkit
```

## Démarrage rapide

```
/authorkit.init
```

Un fichier md de questionnaire sera généré. Remplissez vos réponses dans votre IDE, puis relancez la commande pour terminer la configuration.

## Formats de fichiers pris en charge

- Références : pdf, docx, txt, xlsx, hwpx
- Manuscrits : pdf, docx, txt, xlsx, hwpx, md
- Sortie : md (avec diagrammes en blocs de texte), json

## Workflow

```
/authorkit.init          Configurer le projet
       ↓
/authorkit.analyze       Analyser les références et le manuscrit
       ↓
/authorkit.compare       Comparer références ↔ manuscrit
       ↓
/authorkit.juice         Convertir les fichiers en Markdown (économie de tokens)
       ↓
/authorkit.draft         Rédiger/relire les sections (ancien → nouveau)
       ↓
/authorkit.diagram       Créer des diagrammes en blocs de texte
       ↓
/authorkit.review        Vérifier le style, la terminologie, les références croisées
       ↓
/authorkit.restructure   Réorganiser l'ordre des chapitres/sections
```

## Versions linguistiques

| Plugin | Langue | Installation |
|--------|--------|-------------|
| `authorkit` | English | `/plugin install authorkit@authorkit` |
| `authorkit-ko` | 한국어 | `/plugin install authorkit-ko@authorkit` |

## Licence

Apache 2.0
