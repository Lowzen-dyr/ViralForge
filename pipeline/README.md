# ViralForge Pipeline

Keşif → üretim → yayın akış betikleri.

## Dosyalar

- `make.py` — uçtan uca orkestratör. Tüm adımları sırayla çalıştırır:
  `discover → script → voice → edit → animate → subtitle → cover → title → publish`

## Kullanım

```bash
# Kuru çalıştırma (hiçbir şey üretmez, adımları gösterir):
python pipeline/make.py --topic "gece rutinleri" --dry-run

# Tam üretim (cover + title dahil, yayınlamadan):
python pipeline/make.py --topic "gece rutinleri"

# TikTok'a otomatik yayınla:
python pipeline/make.py --topic "gece rutinleri" --publish
```

## Bağımlılıklar

```
pip install edge-tts TikTokApi openai-whisper python-dotenv
```

Entegrasyon noktaları `make.py` içinde yorumlarla işaretlidir:
- LLM senaryo/başlık: `agents/script-writer.md`, `agents/title-writer.md` promptları (ücretsiz tier key: `.env` → `GROQ_API_KEY`)
- Montaj: OpenReels / openshorts (Docker)
- Altyazı: Whisper (buzz alternatifi)
- Kapak: Pollinations (ücretsiz HTTP) veya ComfyUI/FLUX (gelişmiş mod)
- Yayın: social-auto-upload (TikTok çerez oturumu)
