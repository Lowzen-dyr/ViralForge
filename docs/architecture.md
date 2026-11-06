# 🏗️ ViralForge Mimari

## Genel Bakış

ViralForge, 7 katmandan oluşan bir pipeline'dır. Her katman bağımsız bir açık kaynak aracı kullanır ve REST/MCP üzerinden birbirine bağlanır.

```
┌──────────────────────────────────────────────────────────┐
│                  WEB UI (tarayıcı)                        │
│      MoneyPrinterTurbo UI  /  Remotion Player            │
└──────────────┬───────────────────────────────┬───────────┘
               │                               │
   ┌───────────▼───────────┐       ┌───────────▼──────────┐
   │  KATMAN 1 — KEŞİF      │       │  KATMAN 5 — GÖRSEL    │
   │  Douyin_TikTok_API     │       │  Pollinations         │
   │  TikTok-Api            │       │  (ComfyUI/FLUX opsiyo)│
   └───────────┬───────────┘       └──────────────────────┘
               │
   ┌───────────▼───────────┐       ┌──────────────────────┐
   │  KATMAN 2 — SENARYO    │       │  KATMAN 6 — BAŞLIK    │
   │  LLM (ücretsiz tier)   │       │  LLM (title agent)    │
   └───────────┬───────────┘       └──────────────────────┘
               │
   ┌───────────▼───────────┐       ┌──────────────────────┐
   │  KATMAN 3 — ÜRETİM     │       │  KATMAN 7 — YAYIN     │
   │  edge-tts (ses)         │       │  social-auto-upload   │
   │  OpenReels (montaj)     │       │  → TikTok             │
   │  openshorts (kesim)     │       └──────────────────────┘
   │  Remotion (animasyon)   │
   └───────────┬───────────┘       ┌──────────────────────┐
               │                   │  API KATMANI          │
   ┌───────────▼───────────┐       │  short-video-maker    │
   │  KATMAN 4 — ALTYAZI    │◄──────┤  (REST, agent'lara    │
   │  buzz / Whisper         │       │   açık, MCP)          │
   └────────────────────────┘       └──────────────────────┘
```

## Katman Detayları

### 1. Keşif (`/discover`, `/analyze`)
- **Douyin_TikTok_Download_API**: self-host, web konsol; trend veri toplama, video istatistikleri, MCP desteği.
- **TikTok-Api**: hashtag trendleri, ses trendleri, yorum analizi.
- Çıktı: `data/discovered.json` (trend konu + skor + örnek videolar).

### 2. Senaryo (`/script`)
- Ücretsiz LLM (Groq/Gemini free tier), `agents/script-writer.md` promptu.
- Çıktı: `output/script.json` (sahneler + hook + CTA).

### 3. Üretim (`/voice`, `/edit`, `/animate`)
- **edge-tts**: ücretsiz Microsoft TTS, API key'siz.
- **OpenReels**: araştırma→montaj ana pipeline (TypeScript).
- **openshorts**: AI an tespiti, 9:16, yüz takibi (Docker).
- **Remotion**: `templates/` şablonlarıyla programatik animasyon.
- Çıktı: `output/video_raw.mp4` → `output/video_final.mp4`.

### 4. Altyazı (`/subtitle`)
- **buzz/Whisper**: offline transkripsiyon; stil şablonu uygulanır (`templates/subtitle-styles.json`).
- Çıktı: gömülü altyazılı video.

### 5. Kapak Görseli (`/cover`)
- **Pollinations**: prompt→görsel, 1080x1920, ücretsiz.
- Gelişmiş mod: ComfyUI + FLUX.1 (self-host, ücretsiz).
- Çıktı: `output/cover.png`.

### 6. Başlık (`/title`)
- LLM, `agents/title-writer.md`: ≤100 karakter, CTR-optimizasyonlu, 3–5 hashtag.
- Çıktı: `output/metadata.json` (başlık + açıklama + hashtag).

### 7. Yayın (`/publish`)
- **social-auto-upload**: çerezle TikTok oturumu, otomatik yükleme + zamanlama.
- Çıktı: yayınlanmış video URL'si.

## Veri Akışı

```
data/discovered.json → output/script.json → output/voice.mp3
→ output/video_raw.mp4 → output/video_final.mp4
→ output/cover.png + output/metadata.json → TİKTOK
```

## Genişletme

- Yeni araç eklemek için `docs/tools-catalog.md`'ye kaydet, katmana bağla.
- AI agent entegrasyonu: `short-video-maker` REST API veya MCP sunucuları üzerinden.
