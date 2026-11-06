# ViralForge Templates

Bu klasörde animasyon ve altyazı şablonları bulunur.

## Dosyalar

- `animation-subtitle-templates.json` — Remotion animasyon şablonları (kinetic text, zoom punch, slide-up, progress bar) + altyazı stil şablonları (karaoke pop, clean minimal, highlight box)

## Kullanım

1. Şablon `id`'sini pipeline komutuna verin:
   ```bash
   python pipeline/make.py --topic "<konu>" --template kinetic_text --subtitle-style karaoke_pop
   ```
2. Remotion projenizde `templates/animation-subtitle-templates.json` içindeki `params` değerlerini ilgili `interpolate()` çağrılarına taşıyın.

## Yeni Şablon Ekleme

JSON'a yeni bir obje ekleyin; `engine` alanı `remotion` ise pipeline otomatik tanır.
