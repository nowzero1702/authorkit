# authorkit

[English](../README.md) | [한국어](README.ko.md) | [中文](README.zh.md) | [日本語](README.ja.md) | **Русский** | [Français](README.fr.md) | [Deutsch](README.de.md) | [Español](README.es.md) | [Português](README.pt.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | [Italiano](README.it.md)

**Навыки рабочего процесса написания книг для Claude Code.**

Систематизация повторяющихся задач при написании книг: анализ справочных материалов, корректура рукописей, создание диаграмм, проверка стиля и терминологии, реорганизация структуры.

## Навыки

| Навык | Описание |
|-------|----------|
| `init` | Инициализация проекта (анкета md → настройка) |
| `analyze` | Анализ справочных материалов и рукописи |
| `compare` | Сравнение справочных материалов ↔ рукописи |
| `juice` | Конвертация файлов в Markdown (OCR, извлечение таблиц, формулы LaTeX, экономия токенов) |
| `draft` | Написание/корректура на уровне разделов (старое → новое) |
| `diagram` | Создание текстовых блок-схем |
| `review` | Проверка стиля, терминологии и структуры |
| `restructure` | Реорганизация структуры |

## Установка

```
/plugin marketplace add Nowzero/authorkit
/plugin install authorkit@authorkit
```

Для корейской версии:
```
/plugin install authorkit-ko@authorkit
```

## Быстрый старт

```
/authorkit.init
```

Будет сгенерирован md-файл с анкетой. Заполните ответы в вашей IDE, затем запустите команду повторно для завершения настройки.

## Поддерживаемые форматы файлов

- Справочные материалы: pdf, docx, txt, xlsx, hwpx
- Рукописи: pdf, docx, txt, xlsx, hwpx, md
- Вывод: md (с текстовыми блок-схемами), json

## Рабочий процесс

```
/authorkit.init          Настроить проект
       ↓
/authorkit.analyze       Проанализировать материалы и рукопись
       ↓
/authorkit.compare       Сравнить материалы ↔ рукопись
       ↓
/authorkit.juice         Конвертировать файлы в Markdown (экономия токенов)
       ↓
/authorkit.draft         Написать/откорректировать разделы (старое → новое)
       ↓
/authorkit.diagram       Создать текстовые блок-схемы
       ↓
/authorkit.review        Проверить стиль, терминологию, перекрёстные ссылки
       ↓
/authorkit.restructure   Реорганизовать порядок глав/разделов
```

## Языковые версии

| Plugin | Язык | Установка |
|--------|------|-----------|
| `authorkit` | English | `/plugin install authorkit@authorkit` |
| `authorkit-ko` | 한국어 | `/plugin install authorkit-ko@authorkit` |

## Лицензия

Apache 2.0
