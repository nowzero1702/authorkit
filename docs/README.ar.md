# authorkit

[English](../README.md) | [한국어](README.ko.md) | [中文](README.zh.md) | [日本語](README.ja.md) | [Русский](README.ru.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Español](README.es.md) | [Português](README.pt.md) | **العربية** | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | [Italiano](README.it.md)

**مهارات سير العمل لتأليف الكتب باستخدام Claude Code.**

نظّم المهام المتكررة في كتابة الكتب: تحليل المراجع، تدقيق المخطوطات، إنشاء المخططات، التحقق من الأسلوب والمصطلحات، وإعادة تنظيم البنية.

## المهارات

| المهارة | الوصف |
|---------|-------|
| `init` | تهيئة المشروع (استبيان md → إعداد) |
| `analyze` | تحليل المراجع والمخطوطة |
| `compare` | مقارنة المراجع ↔ المخطوطة |
| `juice` | تحويل الملفات إلى Markdown (التعرف الضوئي، استخراج الجداول، صيغ LaTeX، توفير التوكنات) |
| `draft` | كتابة/تدقيق على مستوى الأقسام (قديم → جديد) |
| `diagram` | إنشاء مخططات الكتل النصية |
| `review` | التحقق من الأسلوب والمصطلحات والبنية |
| `restructure` | إعادة تنظيم البنية |

## التثبيت

```
/install nowzero1702/authorkit
```

للنسخة الإنجليزية:
```
/install nowzero1702/authorkit-en
```

## البدء السريع

```
/authorkit-init
```

سيتم إنشاء ملف md يحتوي على استبيان. املأ إجاباتك في بيئة التطوير الخاصة بك، ثم شغّل الأمر مرة أخرى لإتمام الإعداد.

## صيغ الملفات المدعومة

- المراجع: pdf، docx، txt، xlsx، hwpx
- المخطوطات: pdf، docx، txt، xlsx، hwpx، md
- المخرجات: md (مع مخططات الكتل النصية)، json

## سير العمل

```
/authorkit-init          إعداد المشروع
       ↓
/authorkit-analyze       تحليل المراجع والمخطوطة
       ↓
/authorkit-compare       مقارنة المراجع ↔ المخطوطة
       ↓
/authorkit-juice         تحويل الملفات إلى Markdown (توفير التوكنات)
       ↓
/authorkit-draft         كتابة/تدقيق الأقسام (قديم → جديد)
       ↓
/authorkit-diagram       إنشاء مخططات الكتل النصية
       ↓
/authorkit-review        التحقق من الأسلوب والمصطلحات والإحالات المرجعية
       ↓
/authorkit-restructure   إعادة تنظيم ترتيب الفصول/الأقسام
```

## الإصدارات اللغوية

| Plugin | اللغة | التثبيت |
|--------|-------|---------|
| `authorkit` | 한국어 (default) | `/install nowzero1702/authorkit` |
| `authorkit-en` | English | `/install nowzero1702/authorkit-en` |

## الترخيص

MIT
