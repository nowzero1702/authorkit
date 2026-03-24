# authorkit

[English](../README.md) | [한국어](README.ko.md) | [中文](README.zh.md) | **日本語** | [Русский](README.ru.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Español](README.es.md) | [Português](README.pt.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | [Italiano](README.it.md)

**Claude Code 向けの書籍執筆ワークフロースキル。**

書籍執筆における反復的な作業を体系化します：参考文献の分析、原稿の校正、図表の作成、文体・用語の検証、構成の再編成。

## スキル

| スキル | 説明 |
|--------|------|
| `init` | プロジェクト初期化（アンケート md → セットアップ） |
| `analyze` | 参考文献・原稿の分析 |
| `compare` | 参考文献 ↔ 原稿の比較 |
| `draft` | セクション単位の執筆・校正（旧 → 新） |
| `diagram` | テキストブロック図の作成 |
| `review` | 文体・用語・構成の検証 |
| `restructure` | 構成の再編成 |

## インストール

```
/plugin marketplace add Nowzero/authorkit
/plugin install authorkit@authorkit
```

韓国語版：
```
/plugin install authorkit-ko@authorkit
```

## クイックスタート

```
/authorkit.init
```

アンケート md ファイルが生成されます。IDE で回答を記入した後、再度コマンドを実行するとセットアップが完了します。

## 対応ファイル形式

- 参考文献：pdf、docx、txt、xlsx、hwpx
- 原稿：pdf、docx、txt、xlsx、hwpx、md
- 出力：md（テキストブロック図付き）

## ワークフロー

```
/authorkit.init          プロジェクトをセットアップ
       ↓
/authorkit.analyze       参考文献と原稿を分析
       ↓
/authorkit.compare       参考文献 ↔ 原稿を比較
       ↓
/authorkit.draft         セクションを執筆・校正（旧 → 新）
       ↓
/authorkit.diagram       テキストブロック図を作成
       ↓
/authorkit.review        文体・用語・相互参照を検証
       ↓
/authorkit.restructure   章・セクションの順序を再編成
```

## 言語バージョン

| Plugin | 言語 | インストール |
|--------|------|-------------|
| `authorkit` | English | `/plugin install authorkit@authorkit` |
| `authorkit-ko` | 한국어 | `/plugin install authorkit-ko@authorkit` |

## ライセンス

Apache 2.0
