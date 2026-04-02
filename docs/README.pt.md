# authorkit

[English](../README.md) | [한국어](README.ko.md) | [中文](README.zh.md) | [日本語](README.ja.md) | [Русский](README.ru.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Español](README.es.md) | **Português** | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | [Italiano](README.it.md)

**Habilidades de fluxo de trabalho para escrita de livros com Claude Code.**

Sistematize as tarefas repetitivas da escrita de livros: análise de referências, revisão de manuscritos, criação de diagramas, verificação de estilo e terminologia, e reorganização da estrutura.

## Habilidades

| Habilidade | Descrição |
|------------|-----------|
| `init` | Inicialização do projeto (questionário md → configuração) |
| `analyze` | Análise de referências e manuscrito |
| `compare` | Comparação referências ↔ manuscrito |
| `juice` | Conversão de arquivos para Markdown (OCR, extração de tabelas, fórmulas LaTeX, economia de tokens) |
| `draft` | Redação/revisão por seções (antigo → novo) |
| `diagram` | Criação de diagramas de blocos de texto |
| `review` | Verificação de estilo, terminologia e estrutura |
| `restructure` | Reorganização da estrutura |

## Instalação

```
/plugin marketplace add Nowzero/authorkit
/plugin install authorkit@authorkit
```

Para a versão em coreano:
```
/plugin install authorkit-ko@authorkit
```

## Início rápido

```
/authorkit.init
```

Um arquivo md com questionário será gerado. Preencha as respostas no seu IDE e execute o comando novamente para concluir a configuração.

## Formatos de arquivo suportados

- Referências: pdf, docx, txt, xlsx, hwpx
- Manuscritos: pdf, docx, txt, xlsx, hwpx, md
- Saída: md (com diagramas de blocos de texto), json

## Fluxo de trabalho

```
/authorkit.init          Configurar o projeto
       ↓
/authorkit.analyze       Analisar referências e manuscrito
       ↓
/authorkit.compare       Comparar referências ↔ manuscrito
       ↓
/authorkit.juice         Converter arquivos para Markdown (economia de tokens)
       ↓
/authorkit.draft         Redigir/revisar seções (antigo → novo)
       ↓
/authorkit.diagram       Criar diagramas de blocos de texto
       ↓
/authorkit.review        Verificar estilo, terminologia, referências cruzadas
       ↓
/authorkit.restructure   Reorganizar a ordem dos capítulos/seções
```

## Versões de idioma

| Plugin | Idioma | Instalação |
|--------|--------|------------|
| `authorkit` | English | `/plugin install authorkit@authorkit` |
| `authorkit-ko` | 한국어 | `/plugin install authorkit-ko@authorkit` |

## Licença

Apache 2.0
