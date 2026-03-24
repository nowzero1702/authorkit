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
| `draft` | Stesura/correzione per sezioni (vecchio → nuovo) |
| `diagram` | Creazione di diagrammi a blocchi di testo |
| `review` | Verifica di stile, terminologia e struttura |
| `restructure` | Riorganizzazione della struttura |

## Installazione

```
/plugin marketplace add Nowzero/authorkit
/plugin install authorkit@authorkit
```

Per la versione coreana:
```
/plugin install authorkit-ko@authorkit
```

## Avvio rapido

```
/authorkit.init
```

Verrà generato un file md con un questionario. Compila le risposte nel tuo IDE, poi esegui nuovamente il comando per completare la configurazione.

## Formati di file supportati

- Riferimenti: pdf, docx, txt, xlsx, hwpx
- Manoscritti: pdf, docx, txt, xlsx, hwpx, md
- Output: md (con diagrammi a blocchi di testo)

## Workflow

```
/authorkit.init          Configurare il progetto
       ↓
/authorkit.analyze       Analizzare riferimenti e manoscritto
       ↓
/authorkit.compare       Confrontare riferimenti ↔ manoscritto
       ↓
/authorkit.draft         Scrivere/correggere sezioni (vecchio → nuovo)
       ↓
/authorkit.diagram       Creare diagrammi a blocchi di testo
       ↓
/authorkit.review        Verificare stile, terminologia, riferimenti incrociati
       ↓
/authorkit.restructure   Riorganizzare l'ordine dei capitoli/sezioni
```

## Versioni linguistiche

| Plugin | Lingua | Installazione |
|--------|--------|--------------|
| `authorkit` | English | `/plugin install authorkit@authorkit` |
| `authorkit-ko` | 한국어 | `/plugin install authorkit-ko@authorkit` |

## Licenza

Apache 2.0
