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
| `draft` | Bölüm düzeyinde yazma/düzeltme (eski → yeni) |
| `diagram` | Metin blok diyagramı oluşturma |
| `review` | Üslup/terminoloji/yapı doğrulama |
| `restructure` | Yapı yeniden düzenleme |

## Kurulum

```
/plugin marketplace add Nowzero/authorkit
/plugin install authorkit@authorkit
```

Korece sürüm için:
```
/plugin install authorkit-ko@authorkit
```

## Hızlı Başlangıç

```
/authorkit.init
```

Bir anket md dosyası oluşturulacaktır. IDE'nizde yanıtları doldurun, ardından kurulumu tamamlamak için komutu tekrar çalıştırın.

## Desteklenen Dosya Biçimleri

- Kaynaklar: pdf, docx, txt, xlsx, hwpx
- El yazmaları: pdf, docx, txt, xlsx, hwpx, md
- Çıktı: md (metin blok diyagramları ile)

## İş Akışı

```
/authorkit.init          Projeyi kur
       ↓
/authorkit.analyze       Kaynakları ve el yazmasını analiz et
       ↓
/authorkit.compare       Kaynak ↔ el yazmasını karşılaştır
       ↓
/authorkit.draft         Bölümleri yaz/düzelt (eski → yeni)
       ↓
/authorkit.diagram       Metin blok diyagramları oluştur
       ↓
/authorkit.review        Üslup, terminoloji, çapraz referansları doğrula
       ↓
/authorkit.restructure   Bölüm sırasını yeniden düzenle
```

## Dil Sürümleri

| Plugin | Dil | Kurulum |
|--------|-----|---------|
| `authorkit` | English | `/plugin install authorkit@authorkit` |
| `authorkit-ko` | 한국어 | `/plugin install authorkit-ko@authorkit` |

## Lisans

Apache 2.0
