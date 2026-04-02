# authorkit

[English](../README.md) | [한국어](README.ko.md) | [中文](README.zh.md) | [日本語](README.ja.md) | [Русский](README.ru.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Español](README.es.md) | [Português](README.pt.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | **Türkçe** | [Italiano](README.it.md)

**Claude Code için kitap yazma iş akışı becerileri.**

Kitap yazımındaki tekrarlayan görevleri sistemleştirin: kaynak analizi, el yazması düzeltme, diyagram oluşturma, üslup/terminoloji doğrulama ve yapı yeniden düzenleme.

## Beceriler

| Beceri | Açıklama |
|--------|----------|
| `init` | Proje başlatma (anket md → kurulum) |
| `analyze` | Kaynak/el yazması analizi |
| `compare` | Kaynak ↔ el yazması karşılaştırma |
| `juice` | Dosyaları Markdown'a dönüştürme (OCR, tablo çıkarma, formül LaTeX, token tasarrufu) |
| `draft` | Bölüm düzeyinde yazma/düzeltme (eski → yeni) |
| `diagram` | Metin blok diyagramı oluşturma |
| `review` | Üslup/terminoloji/yapı doğrulama |
| `restructure` | Yapı yeniden düzenleme |

## Kurulum

```
/install nowzero1702/authorkit
```

İngilizce sürüm için:
```
/install nowzero1702/authorkit-en
```

## Hızlı Başlangıç

```
/authorkit-init
```

Bir anket md dosyası oluşturulacaktır. IDE'nizde yanıtları doldurun, ardından kurulumu tamamlamak için komutu tekrar çalıştırın.

## Desteklenen Dosya Biçimleri

- Kaynaklar: pdf, docx, txt, xlsx, hwpx
- El yazmaları: pdf, docx, txt, xlsx, hwpx, md
- Çıktı: md (metin blok diyagramları ile), json

## İş Akışı

```
/authorkit-init          Projeyi kur
       ↓
/authorkit-analyze       Kaynakları ve el yazmasını analiz et
       ↓
/authorkit-compare       Kaynak ↔ el yazmasını karşılaştır
       ↓
/authorkit-juice         Dosyaları Markdown'a dönüştür (token tasarrufu)
       ↓
/authorkit-draft         Bölümleri yaz/düzelt (eski → yeni)
       ↓
/authorkit-diagram       Metin blok diyagramları oluştur
       ↓
/authorkit-review        Üslup, terminoloji, çapraz referansları doğrula
       ↓
/authorkit-restructure   Bölüm sırasını yeniden düzenle
```

## Dil Sürümleri

| Plugin | Dil | Kurulum |
|--------|-----|---------|
| `authorkit` | 한국어 (default) | `/install nowzero1702/authorkit` |
| `authorkit-en` | English | `/install nowzero1702/authorkit-en` |

## Lisans

MIT
