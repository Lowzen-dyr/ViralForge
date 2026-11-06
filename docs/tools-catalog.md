# 🧰 ViralForge Araç Kataloğu

Tüm bileşenler **ücretsiz** kullanılabilir. Doğrulanma tarihi: 2026-11-06.

| # | Araç | Rol | Lisans | Ücretsiz Kurulum |
|---|---|---|---|---|
| 1 | [tsensei/OpenReels](https://github.com/tsensei/OpenReels) | Ana üretim pipeline'ı: konu→araştırma→senaryo→seslendirme→görsel→müzik→altyazı→montaj | Açık kaynak (TS) | `git clone` + npm |
| 2 | [harry0703/MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) | Web UI iskeleti: konu/keyword→HD kısa video, TTS+altyazı+geçiş efektleri | MIT benzeri | `docker compose` |
| 3 | [mutonby/openshorts](https://github.com/mutonby/openshorts) | Edit motoru: uzun video→viral 9:16, AI an tespiti, yüz takibi, dublaj | MIT | Docker self-host |
| 4 | [remotion-dev/remotion](https://github.com/remotion-dev/remotion) | Animasyon şablonları: React ile programatik video | Ücretsiz çekirdek (şirket kullanımı ücretli olabilir) | `npm i @remotion` |
| 5 | [rany2/edge-tts](https://github.com/rany2/edge-tts) | Ücretsiz TTS seslendirme (Microsoft Edge servisi, key gerekmez) | GPL-3.0 | `pip install edge-tts` |
| 6 | [chidiwilliams/buzz](https://github.com/chidiwilliams/buzz) | Otomatik altyazı: offline Whisper transkripsiyon + çeviri | MIT benzeri | pip/app indirme |
| 7 | [Evil0ctal/Douyin_TikTok_Download_API](https://github.com/Evil0ctal/Douyin_TikTok_Download_API) | Keşif+analiz: TikTok veri toplama, trendler, web konsol, MCP | MIT benzeri | `docker compose up` |
| 8 | [davidteather/TikTok-Api](https://github.com/davidteather/TikTok-Api) | Trend analizi: hashtag, ses trendleri, yorum verisi | MIT | `pip install TikTokApi` |
| 9 | [dreammis/social-auto-upload](https://github.com/dreammis/social-auto-upload) | Otomatik TikTok/youtube yayın + zamanlama | MIT benzeri | pip + çerez oturumu |
| 10 | [gyoridavid/short-video-maker](https://github.com/gyoridavid/short-video-maker) | REST API katmanı: agent'lara video ürettirme | Açık kaynak (TS) | npx/MCP |
| 11 | [pollinations/pollinations](https://github.com/pollinations/pollinations) | **Kapak görseli AI'ı**: key gerektirmeyen prompt→görsel | MIT | HTTP çağrısı, kurulum yok |
| 12 | [Comfy-Org/ComfyUI](https://github.com/Comfy-Org/ComfyUI) | Gelişmiş görsel üretim (node arayüzü, API'li) | GPL-3.0 | pip/git kurulum |
| 13 | [black-forest-labs/flux](https://github.com/black-forest-labs/flux) | FLUX.1 açık model (ComfyUI ile kullanılır) | Açık ağırlıklar | ComfyUI içinden |
| 14 | [sasateguh/awesome-ai-video-for-creators](https://github.com/sasateguh/awesome-ai-video-for-creators) | Haftalık güncellenen araç kataloğu (referans) | — | — |

## Lisans/Ücretsizlik Notları

- **Remotion**: kişisel ve çoğu açık kaynak kullanım için ücretsizdir; büyük şirketlerde ücretli olabilir → `LICENSE.md` kontrol edin.
- **Pollinations**: ücretsiz anonim erişim sunar; yoğun kullanımda kota olabilir → kapak üretimi için yeterli.
- **edge-tts**: Microsoft Edge'in çevrimiçi TTS servisini key'siz kullanır → ücretsizdir, ToS'a uygun kullanın.
- **ComfyUI + FLUX**: tamamen self-host, GPU'da ücretsiz; kapak görseli için opsiyonel gelişmiş moddur.

## Rol Haritası

```
Keşif    → #7, #8
Senaryo  → #1, #2 (LLM promptları: agents/)
Ses      → #5
Edit     → #3, #1, #2
Animasyon→ #4
Altyazı  → #6
Kapak    → #11 (+ #12, #13 opsiyonel)
Yayın    → #9
API      → #10
Katalog  → #14 (yeni araç keşfi için)
```
