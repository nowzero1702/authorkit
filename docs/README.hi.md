# authorkit

[English](../README.md) | [한국어](README.ko.md) | [中文](README.zh.md) | [日本語](README.ja.md) | [Русский](README.ru.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Español](README.es.md) | [Português](README.pt.md) | [العربية](README.ar.md) | **हिन्दी** | [Türkçe](README.tr.md) | [Italiano](README.it.md)

**Claude Code के लिए पुस्तक लेखन वर्कफ़्लो स्किल।**

पुस्तक लेखन के दोहराव वाले कार्यों को व्यवस्थित करें: संदर्भ विश्लेषण, पांडुलिपि प्रूफ़रीडिंग, आरेख निर्माण, शैली/शब्दावली सत्यापन, और संरचना पुनर्गठन।

## स्किल

| स्किल | विवरण |
|-------|-------|
| `init` | प्रोजेक्ट इनिशियलाइज़ेशन (प्रश्नावली md → सेटअप) |
| `analyze` | संदर्भ/पांडुलिपि विश्लेषण |
| `compare` | संदर्भ ↔ पांडुलिपि तुलना |
| `juice` | फ़ाइलों को Markdown में बदलें (OCR, तालिका निष्कर्षण, सूत्र LaTeX, टोकन बचत) |
| `draft` | खंड-स्तरीय लेखन/प्रूफ़रीडिंग (पुराना → नया) |
| `diagram` | टेक्स्ट ब्लॉक आरेख निर्माण |
| `review` | शैली/शब्दावली/संरचना सत्यापन |
| `restructure` | संरचना पुनर्गठन |

## इंस्टॉलेशन

```
/plugin marketplace add nowzero1702/authorkit
/plugin install authorkit@nowzero1702-authorkit
```

अंग्रेज़ी संस्करण के लिए:
```
/plugin install authorkit-en@nowzero1702-authorkit
```

अपडेट:
```
/plugin marketplace update nowzero1702-authorkit
/reload-plugins
```

## त्वरित शुरुआत

```
/authorkit-init
```

एक प्रश्नावली md फ़ाइल जनरेट होगी। अपनी IDE में उत्तर भरें, फिर सेटअप पूरा करने के लिए कमांड दोबारा चलाएँ।

## समर्थित फ़ाइल प्रारूप

- संदर्भ: pdf, docx, txt, xlsx, hwpx
- पांडुलिपियाँ: pdf, docx, txt, xlsx, hwpx, md
- आउटपुट: md (टेक्स्ट ब्लॉक आरेखों सहित), json

## वर्कफ़्लो

```
/authorkit-init          प्रोजेक्ट सेटअप करें
       ↓
/authorkit-analyze       संदर्भ और पांडुलिपि का विश्लेषण करें
       ↓
/authorkit-compare       संदर्भ ↔ पांडुलिपि की तुलना करें
       ↓
/authorkit-juice         फ़ाइलों को Markdown में बदलें (टोकन बचत)
       ↓
/authorkit-draft         खंड लिखें/प्रूफ़रीड करें (पुराना → नया)
       ↓
/authorkit-diagram       टेक्स्ट ब्लॉक आरेख बनाएँ
       ↓
/authorkit-review        शैली, शब्दावली, क्रॉस-रेफ़रेंस सत्यापित करें
       ↓
/authorkit-restructure   अध्याय/खंड क्रम पुनर्गठित करें
```

## भाषा संस्करण

| Plugin | भाषा | इंस्टॉल |
|--------|------|---------|
| `authorkit` | 한국어 (default) | `/plugin marketplace add nowzero1702/authorkit` → `/plugin install authorkit@nowzero1702-authorkit` |
| `authorkit-en` | English | `/plugin install authorkit-en@nowzero1702-authorkit` |

## लाइसेंस

MIT
