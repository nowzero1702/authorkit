# authorkit

[English](../README.md) | [한국어](README.ko.md) | [中文](README.zh.md) | [日本語](README.ja.md) | [Русский](README.ru.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | **Español** | [Português](README.pt.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | [Italiano](README.it.md)

**Habilidades de flujo de trabajo para la redacción de libros con Claude Code.**

Sistematiza las tareas repetitivas de la escritura de libros: análisis de referencias, corrección de manuscritos, creación de diagramas, verificación de estilo y terminología, y reorganización de la estructura.

## Habilidades

| Habilidad | Descripción |
|-----------|-------------|
| `init` | Inicialización del proyecto (cuestionario md → configuración) |
| `analyze` | Análisis de referencias y manuscrito |
| `compare` | Comparación referencias ↔ manuscrito |
| `draft` | Redacción/corrección por secciones (antiguo → nuevo) |
| `diagram` | Creación de diagramas de bloques de texto |
| `review` | Verificación de estilo, terminología y estructura |
| `restructure` | Reorganización de la estructura |

## Instalación

```
/plugin marketplace add Nowzero/authorkit
/plugin install authorkit@authorkit
```

Para la versión en coreano:
```
/plugin install authorkit-ko@authorkit
```

## Inicio rápido

```
/authorkit.init
```

Se generará un archivo md con un cuestionario. Completa las respuestas en tu IDE y luego ejecuta el comando de nuevo para finalizar la configuración.

## Formatos de archivo compatibles

- Referencias: pdf, docx, txt, xlsx, hwpx
- Manuscritos: pdf, docx, txt, xlsx, hwpx, md
- Salida: md (con diagramas de bloques de texto)

## Flujo de trabajo

```
/authorkit.init          Configurar el proyecto
       ↓
/authorkit.analyze       Analizar referencias y manuscrito
       ↓
/authorkit.compare       Comparar referencias ↔ manuscrito
       ↓
/authorkit.draft         Redactar/corregir secciones (antiguo → nuevo)
       ↓
/authorkit.diagram       Crear diagramas de bloques de texto
       ↓
/authorkit.review        Verificar estilo, terminología, referencias cruzadas
       ↓
/authorkit.restructure   Reorganizar el orden de capítulos/secciones
```

## Versiones de idioma

| Plugin | Idioma | Instalación |
|--------|--------|-------------|
| `authorkit` | English | `/plugin install authorkit@authorkit` |
| `authorkit-ko` | 한국어 | `/plugin install authorkit-ko@authorkit` |

## Licencia

Apache 2.0
