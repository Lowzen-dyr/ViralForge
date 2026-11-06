# 🔥 ViralForge

**Tamamen ücretsiz ve web tabanlı, uçtan uca otomatik TikTok video üretim sistemi.**

ViralForge; konu keşfi → trend analizi → senaryo → seslendirme → montaj/animasyon → altyazı → kapak görseli → başlık üretimi → otomatik yayın akışını tek bir pipeline'da birleştirir.

> Sıfırdan inşa edilmiş bir "skill": dünyanın en iyi açık kaynak (ücretsiz) araçları birleştirilerek kurulmuştur. Tüm bileşenlerin listesi için [docs/tools-catalog.md](docs/tools-catalog.md).

## ✨ Neler yapar?

- 🔍 **Keşif & Analiz** — TikTok trendlerini, hashtag ve ses trendlerini tarar, viral konuları bulur
- 🎙️ **Otomatik Seslendirme** — Ücretsiz TTS (edge-tts) ile doğal ses
- ✂️ **Edit & Animasyon** — AI an tespiti, 9:16 kesim, yüz takibi, geçiş efektleri
- 💬 **Otomatik Altyazı** — Whisper tabanlı transkripsiyon, stil şablonları
- 🖼️ **Kapak Görseli** — AI ile prompt'tan kapak üretimi (Pollinations; ComfyUI/FLUX ile gelişmiş mod)
- 📝 **Video İsmi** — LLM ile tıklama oranına optimize başlık üretimi
- 🚀 **Otomatik Yayın** — Hazır videoyu TikTok'a otomatik yükleme

## 🏗️ Mimari

```
[Keşif]    Douyin_TikTok_Download_API + TikTok-Api
              → trend konular, hashtag/istatistik analizi
[Üretim]   OpenReels (ana pipeline) + MoneyPrinterTurbo (web UI)
              → senaryo (LLM) → edge-tts seslendirme → görsel/sahne → müzik
[Edit]     openshorts (AI kesim, 9:16, yüz takibi) + Remotion (animasyon şablonları)
[Altyazı]  buzz / Whisper → otomatik altyazı (stil şablonları)
[Görsel]   Pollinations → kapak görseli (ComfyUI/FLUX ile gelişmiş mod)
[Başlık]   LLM → tıklamaya optimize video adı
[Yayın]    social-auto-upload → TikTok otomatik yükleme
[API]      short-video-maker → REST katmanı (agent'lara açık)
```

Detaylı mimari: [docs/architecture.md](docs/architecture.md)

## 📁 Yapı

```
ViralForge/
├── README.md
├── SKILL.md              → Skill tanımı: komutlar + kullanım kuralları
├── docs/
│   ├── architecture.md   → Modül mimarisi
│   ├── tools-catalog.md  → 14 aracın kataloğu (kurulum + lisans)
│   └── setup-guide.md    → Sıfır maliyetli kurulum rehberi
├── templates/            → Animasyon/edit şablon taslakları
├── agents/                → Konu bulma, kapak görseli, video adı üretimi (LLM promptları)
└── pipeline/              → Keşif→üretim→yayın akış betikleri
```

## 🚀 Hızlı Başlangıç

1. Kurulum: [docs/setup-guide.md](docs/setup-guide.md)
2. Skill kullanımı: [SKILL.md](SKILL.md)

## 📜 Lisans Notu

Bu repo bir entegrasyon kılavuzudur; her aracın kendi lisansı geçerlidir. Ücretsiz kullanım koşulları `docs/tools-catalog.md` içinde listelenmiştir.

## ⭐ Kaynaklar

- Haftalık güncellenen açık kaynak video araçları kataloğu: [sasateguh/awesome-ai-video-for-creators](https://github.com/sasateguh/awesome-ai-video-for-creators)
