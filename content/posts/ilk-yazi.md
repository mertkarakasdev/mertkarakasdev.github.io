---
title: "Bu blogu nasıl kurdum"
date: 2026-10-03T10:00:00+03:00
draft: false
tags: ["hugo", "papermod"]
summary: "Hugo, PaperMod teması ve GitHub Actions ile yayına alınan bir blog."
ShowToc: true
---

Bu blog [Hugo](https://gohugo.io) ile üretiliyor, teması
[PaperMod](https://github.com/adityatelange/hugo-PaperMod), yayını da
GitHub Actions üzerinden GitHub Pages'e çıkıyor.

## Yazı eklemek

Yeni bir yazı için tek komut yetiyor:

```bash
hugo new content posts/yeni-yazi.md
```

Dosyanın başındaki `draft: true` satırını `false` yaptığımda yazı yayına
hazır hale geliyor. Taslakları yerelde görmek için:

```bash
hugo server -D
```

## Yayınlamak

Push ettiğim anda Actions çalışıyor ve site birkaç dakika içinde
güncelleniyor:

```bash
git add -A
git commit -m "Yeni yazı"
git push
```

> Üretilen `public/` klasörünü commit'lemeye gerek yok — onu Actions
> kendi içinde üretip yayınlıyor.

## Öne çıkan özellikler

PaperMod'un kutudan çıkan özelliklerinden kullandıklarım:

- Açık/koyu tema geçişi
- Arama sayfası (Fuse.js ile, sunucu gerektirmiyor)
- Arşiv ve etiket sayfaları
- Okuma süresi, içindekiler, kod kopyalama düğmesi
