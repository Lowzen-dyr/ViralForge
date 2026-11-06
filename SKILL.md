# 🧠 ViralForge SKILL

Bu dosya, ViralForge'un bir "skill" olarak nasıl kullanılacağını tanımlar. Amaç: bir kullanıcının veya AI agent'ın tek bir istekle uçtan uca TikTok videosu üretebilmesi.

## 🎯 Skill Tanımı

**Ad:** `viralforge`
**Amaç:** Trend analizi yaparak, verilen konu (veya otomatik bulunan konu) için seslendirme, edit/animasyon, altyazı, kapak görseli ve optimize başlık içeren, yayına hazır TikTok videosu üretmek.
**Maliyet:** 0 ₺ — tüm bileşenler ücretsiz katmanlarla çalışır.

## 📋 Komutlar

| Komut | Ne yapar | Kullandığı modüller |
|---|---|---|
| `/discover` | TikTok trend/hashtag taraması, viral konu listesi çıkarır | Douyin_TikTok_Download_API, TikTok-Api |
| `/analyze <video_url veya konu>` | Video/istatistik analizi; yorumlardan içerik fikri çıkarır | TikTok-Api, LLM |
| `/script <konu>` | Konudan 30–60 sn'lik senaryo yazar | LLM (agents/script-writer.md) |
| `/voice <metin>` | Metni doğal sese çevirir | edge-tts |
| `/edit <video>` | Uzun videodan 9:16 viral kesim, yüz takibi | openshorts |
| `/animate` | Remotion şablonları ile animasyon/geçiş ekler | Remotion (templates/) |
| `/subtitle <video>` | Otomatik altyazı üretir ve stiller | buzz / Whisper |
| `/cover <konu>` | Kapak görseli üretir | Pollinations (agents/cover-designer.md) |
| `/title <konu>` | Tıklamaya optimize video adı üretir | LLM (agents/title-writer.md) |
| `/publish <video>` | TikTok'a otomatik yükler | social-auto-upload |
| `/make <konu>` | **Tam pipeline**: discover→script→voice→edit→animate→subtitle→cover→title→publish | hepsi |

## 🔀 Akış (default: `/make`)

```
1. /discover veya verilen konu
2. /script      → senaryo (30–60 sn, hook + değer + CTA)
3. /voice       → edge-tts ile ses dosyası
4. /edit        → 9:16 kesim veya sahne montajı
5. /animate     → templates/ içindeki animasyon şablonu uygulanır
6. /subtitle    → Whisper transkripsiyon → stil şablonu
7. /cover       → Pollinations ile 1080x1920 kapak
8. /title       → ≤100 karakter, CTR-optimizasyonlu başlık + hashtag seti
9. /publish     → social-auto-upload ile TikTok
```

## ⚙️ Kurallar

1. **Ücretsiz kalsın** — hiçbir adımda ücretli API zorunlu tutulmaz. LLM için ücretsiz katman (ör. Gemini/Groq ücretsiz tier) kullanılır.
2. **Web tabanlı öncelik** — kullanıcı arayüzü tarayıcıda çalışır (MoneyPrinterTurbo web UI / Remotion Player).
3. **Modülerlik** — her adım bağımsız çalışabilir; tek bir modül değiştirilebilir.
4. **Sıfırdan içerik** — kopyalanmış içerik değil, analizle üretilmiş özgün senaryo.
5. **Lisans** — sadece ücretsiz kullanıma uygun araçlar (bkz. docs/tools-catalog.md).
6. **Oran hedefleri** — 9:16, ≤60 sn, altyazı her zaman açık, kapak 1080x1920.

## 🗂️ Konfigürasyon

Ortam değişkenleri (`.env`):

```
TIKTOK_SESSIONID=        # TikTok-Api için (opsiyonel, keşif adımında)
GROQ_API_KEY=            # ücretsiz LLM katmanı (script + title agent)
EDGE_TTS_VOICE=tr-TR-AhemetNeural   # seslendirme sesi
COVER_ENGINE=pollinations          # pollinations | comfyui
TIKTOK_UPLOAD_USER=      # social-auto-upload hesabı
```
