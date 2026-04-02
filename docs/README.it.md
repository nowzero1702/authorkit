# authorkit

[English](../README.md) | [한국어](README.ko.md) | [中文](README.zh.md) | [日本語](README.ja.md) | [Русский](README.ru.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Español](README.es.md) | [Português](README.pt.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | **Italiano**

**Competenze di workflow per la scrittura di libri con Claude Code.**

Sistematizza le attività ripetitive della scrittura di libri: analisi dei riferimenti, correzione dei manoscritti, creazione di diagrammi, verifica di stile e terminologia, e riorganizzazione della struttura.

## Competenze

| Competenza | Descrizione |
|------------|-------------|
| `init` | Inizializzazione del progetto (questionario md → configurazione) |
| `analyze` | Analisi dei riferimenti e del manoscritto |
| `compare` | Confronto riferimenti ↔ manoscritto |
| `juice` | Conversione file in Markdown (OCR, estrazione tabelle, formule LaTeX, risparmio di token) |
| `draft` | Stesura/correzione per sezioni (vecchio → nuovo) |
| `diagram` | Creazione di diagrammi a blocchi di testo |
| `review` | Verifica di stile, terminologia e struttura |
| `restructure` | Riorganizzazione della struttura |

## Installazione

```
/plugin marketplace add nowzero1702/authorkit
/plugin install authorkit@nowzero1702-authorkit
```

Per la versione inglese:
```
/plugin install authorkit-en@nowzero1702-authorkit
```

Aggiornamento:
```
/plugin marketplace update nowzero1702-authorkit
/reload-plugins
```

## Avvio rapido

```
/authorkit-init
```

Verrà generato un file md con un questionario. Compila le risposte nel tuo IDE, poi esegui nuovamente il comando per completare la configurazione.

## Formati di file supportati

- Riferimenti: pdf, docx, txt, xlsx, hwpx
- Manoscritti: pdf, docx, txt, xlsx, hwpx, md
- Output: md (con diagrammi a blocchi di testo), json

## Workflow

```
/authorkit-init          Configurare il progetto
       ↓
/authorkit-analyze       Analizzare riferimenti e manoscritto
       ↓
/authorkit-compare       Confrontare riferimenti ↔ manoscritto
       ↓
/authorkit-juice         Convertire file in Markdown (risparmio di token)
       ↓
/authorkit-draft         Scrivere/correggere sezioni (vecchio → nuovo)
       ↓
/authorkit-diagram       Creare diagrammi a blocchi di testo
       ↓
/authorkit-review        Verificare stile, terminologia, riferimenti incrociati
       ↓
/authorkit-restructure   Riorganizzare l'ordine dei capitoli/sezioni
```

## Versioni linguistiche

| Plugin | Lingua | Installazione |
|--------|--------|--------------|
| `authorkit` | 한국어 (default) | `/plugin marketplace add nowzero1702/authorkit` → `/plugin install authorkit@nowzero1702-authorkit` |
| `authorkit-en` | English | `/plugin install authorkit-en@nowzero1702-authorkit` |

## Licenza

MIT
