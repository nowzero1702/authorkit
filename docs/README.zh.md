# authorkit

[English](../README.md) | [한국어](README.ko.md) | **中文** | [日本語](README.ja.md) | [Русский](README.ru.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Español](README.es.md) | [Português](README.pt.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | [Italiano](README.it.md)

**适用于 Claude Code 的图书写作工作流技能。**

将图书写作中的重复性工作系统化：参考文献分析、稿件校对、图表创建、风格/术语验证以及结构重组。

## 技能

| 技能 | 说明 |
|------|------|
| `init` | 项目初始化（问卷 md → 设置） |
| `analyze` | 参考文献/稿件分析 |
| `compare` | 参考文献 ↔ 稿件对比 |
| `draft` | 章节级撰写/校对（旧 → 新） |
| `diagram` | 文本框图创建 |
| `review` | 风格/术语/结构验证 |
| `restructure` | 结构重组 |

## 安装

```
/plugin marketplace add Nowzero/authorkit
/plugin install authorkit@authorkit
```

韩语版本：
```
/plugin install authorkit-ko@authorkit
```

## 快速开始

```
/authorkit.init
```

系统将生成一份问卷 md 文件。在 IDE 中填写答案后，再次运行该命令以完成设置。

## 支持的文件格式

- 参考文献：pdf、docx、txt、xlsx、hwpx
- 稿件：pdf、docx、txt、xlsx、hwpx、md
- 输出：md（含文本框图）

## 工作流

```
/authorkit.init          设置项目
       ↓
/authorkit.analyze       分析参考文献和稿件
       ↓
/authorkit.compare       对比参考文献 ↔ 稿件
       ↓
/authorkit.draft         撰写/校对章节（旧 → 新）
       ↓
/authorkit.diagram       创建文本框图
       ↓
/authorkit.review        验证风格、术语、交叉引用
       ↓
/authorkit.restructure   重组章节顺序
```

## 语言版本

| Plugin | 语言 | 安装 |
|--------|------|------|
| `authorkit` | English | `/plugin install authorkit@authorkit` |
| `authorkit-ko` | 한국어 | `/plugin install authorkit-ko@authorkit` |

## 许可证

Apache 2.0
