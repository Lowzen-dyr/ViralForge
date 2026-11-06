# 🚀 ViralForge Kurulum Rehberi (Sıfır Maliyet)

Tüm sistem **ücretsiz katmanlarla** çalışır. En hafif kurulum ( sadece keşif+üretim+kapak ) yaklaşık 15 dakikada hazırdır.

## 0. Gereksinimler (ücretsiz)

- Git, Python 3.10+, Node.js 20+, Docker Desktop (openshorts/keşif API için)
- Ücretsiz LLM API key'i (script + title için): [Groq Cloud](https://console.groq.com) ücretsiz tier önerilir

## 1. Repo'yu klonla

```bash
git clone https://github.com/Lowzen-dyr/ViralForge.git
cd ViralForge
```

## 2. Keşif modülü (TikTok trend taraması)

```bash
# Seçenek A: TikTok-Api (hafif)
pip install TikTokApi python-dotenv

# Seçenek B: Douyin_TikTok_Download_API (tam web konsol + MCP)
git clone https://github.com/Evil0ctal/Douyin_TikTok_Download_API.git
cd Douyin_TikTok_Download_API && docker compose up -d   # http://localhost:8080
```

## 3. Üretim pipeline'ı

```bash
# TTS (ücretsiz)
pip install edge-tts

# Ana pipeline — OpenReels
git clone https://github.com/tsensei/OpenReels.git
# → kendi LLM key'ini (ücretsiz tier) config'e gir, README'sini izle

# Web UI — MoneyPrinterTurbo (opsiyonel ama önerilen)
git clone https://github.com/harry0703/MoneyPrinterTurbo.git
cd MoneyPrinterTurbo && docker-compose up --build   # http://localhost:8501
```

## 4. Edit + animasyon

```bash
# AI kesim motoru
docker pull mutonby/openshorts   # veya repodan build; MIT, self-host ücretsiz

# Remotion animasyon şablonları
npm create video@latest -- --template blank
npm i @remotion/player
# ViralForge templates/ içindeki şablonlardan kopyala
```

## 5. Altyazı

```bash
pip install openai-whisper   # veya Buzz uygulamasını indir (GUI, offline)
```

## 6. Kapak görseli (AI)

```bash
# Pollinations — kurulum yok, doğrudan HTTP:
curl "https://image.pollinations.ai/prompt/cinematic%20tiktok%20cover%20about%20<konu>?width=1080&height=1920&nologo=true" -o cover.png
```

Gelişmiş mod: ComfyUI + FLUX.1 kurulumu için `docs/tools-catalog.md` #12–13.

## 7. Yayın

```bash
git clone https://github.com/dreammis/social-auto-upload.git
# TikTok çerez oturumu ile tarayıcı otomasyonu (README'sindeki adımlar)
```

## 8. `.env` ayarla

```
GROQ_API_KEY=
TIKTOK_SESSIONID=
EDGE_TTS_VOICE=tr-TR-AhmetNeural
COVER_ENGINE=pollinations
```

## Doğrulama

```bash
python pipeline/make.py --topic "örnek konu" --dry-run
```

Tüm modüllerin çıktıları `output/` klasöründe görünürse sistem hazırdır.
