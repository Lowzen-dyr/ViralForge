#!/usr/bin/env python3
"""
ViralForge — gerçekten çalışan TikTok video üretim pipeline'ı.

Çalışır sistemler (hepsi ücretsiz, web/Codespaces uyumlu, CPU'da çalışır):
  1. script  → LLM (GROQ_API_KEY varsa) veya hazır şablon fallback
  2. voice   → edge-tts: gerçek MP3 + kelime zamanlı SRT altyazı
  3. cover   → Pollinations: gerçek 1080x1920 kapak görseli (API key gerekmez)
  4. edit    → ffmpeg: kapak görselinden 9:16 arka plan + hafif zoom
  5. subtitle→ SRT'yi videoya gömer (force_style ile stil)
  6. title   → LLM (varsa) veya şablon fallback + hashtag seti
  7. publish → otomasyon RİSKLİDİR: videoyu elle yüklemeyi önerir (metadata hazır)

Kullanım:
  python pipeline/make.py --topic "gece rutinleri" [--subtitle-style karaoke_pop]
                          [--dry-run]

Gereksinim: ffmpeg, edge-tts, pillow (install.sh hepsini kurar)
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"

# ---------------------------------------------------------------- yardımcılar

def sh(cmd: list[str], dry: bool = False, check: bool = True) -> subprocess.CompletedProcess:
    printable = " ".join(str(c) for c in cmd)
    print(f"  $ {printable}")
    if dry:
        return subprocess.CompletedProcess(cmd, 0, "", "")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        raise RuntimeError(f"Adım başarısız: {printable}")
    return result


def need_ffmpeg() -> None:
    if sh(["ffmpeg", "-version"], check=True).returncode != 0:
        raise RuntimeError("ffmpeg bulunamadı — install.sh çalıştırın")


def http_get(url: str, dest: Path, dry: bool, tries: int = 3) -> None:
    print(f"  ↓ {url[:100]}...")
    if dry:
        return
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:  # noqa: S310
                f.write(r.read())
            return
        except Exception as e:  # noqa: BLE001 — ağ hatası bilgilendirmesi
            print(f"  deneme {i + 1}/{tries} başarısız: {e}")
            time.sleep(3)
    raise RuntimeError(f"İndirilemedi: {url}")


def ffmpeg_escape(path: Path) -> str:
    """ffmpeg filtre argümanı içinde kullanmak için dosya yolunu escape eder."""
    return str(path.resolve()).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")


# ---------------------------------------------------------------- 1) senaryo

SCRIPT_SYSTEM_PROMPT = (
    "Sen bir TikTok senaryo yazarısın. Verilen konu için 30-45 saniyelik "
    "(70-120 kelime) Türkçe bir senaryo yaz. İlk cümle güçlü bir hook olsun "
    "(soru veya şaşırtıcı iddia). 3-4 kısa paragraf. Sonda izleyiciye yorum "
    "yazmaya çağıran bir kapanış. SADECE senaryo metnini döndür, başlık yok."
)


def gen_script(topic: str, dry: bool) -> str:
    """LLM (ücretsiz Groq tier) varsa gerçek senaryo; yoksa şablon."""
    key = os.getenv("GROQ_API_KEY", "").strip()
    if key and not dry:
        payload = json.dumps({
            "model": os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            "temperature": 0.8,
            "messages": [
                {"role": "system", "content": SCRIPT_SYSTEM_PROMPT},
                {"role": "user", "content": f"Konu: {topic}"},
            ],
        }).encode()
        req = urllib.request.Request(  # noqa: S310 — bilinen, kullanıcı tarafından sağlanmış endpoint
            "https://api.groq.com/openai/v1/chat/completions",
            data=payload,
            headers={"Authorization": f"Bearer {key}",
                     "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
        text = data["choices"][0]["message"]["content"].strip()
        print(f"[1] senaryo (LLM): {len(text)} karakter")
        return text

    text = (
        f"{topic} hakkında bildiğin her şey yanlış olabilir. "
        f"Çoğu insan {topic} konusunda en temel hataları yapıyor ve farkında bile değil. "
        f"Birincisi: acele etmeyin — {topic} konusunda başarı küçük adımlardan geçer. "
        f"İkincisi: taklit etmek yerine kendine özgü bir yön seç. "
        f"Üçüncüsü ve en önemlisi: düzenli ol. Bir hafta deneyip bırakanlar değil, "
        f"devam edenler kazanır. "
        f"Sence de en zor kısım hangisi? Yorumlara yaz, en çok oylananı "
        f"bir sonraki videoda işleyelim."
    )
    print("[1] senaryo (şablon fallback — GROQ_API_KEY girilirse LLM kullanılır)")
    return text


# ---------------------------------------------------------------- 2) ses + SRT

def gen_voice(text: str, dry: bool) -> tuple[Path, Path]:
    """edge-tts: MP3 + kelime zamanlı SRT (ücretsiz, key gerekmez)."""
    mp3, srt = OUT / "voice.mp3", OUT / "voice.srt"
    voice = os.getenv("EDGE_TTS_VOICE", "tr-TR-AhmetNeural")
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                      encoding="utf-8") as tf:
        tf.write(text)
        text_file = tf.name
    try:
        sh(["edge-tts", "--voice", voice, "--file", text_file,
            "--write-media", str(mp3), "--write-subtitles", str(srt)], dry)
    finally:
        os.unlink(text_file)
    print(f"[2] ses: {mp3.name} + altyazı: {srt.name} (edge-tts)")
    return mp3, srt


# ---------------------------------------------------------------- 3) kapak

def gen_cover(topic: str, dry: bool) -> Path:
    prompt = urllib.parse.quote(
        f"cinematic vertical thumbnail about {topic}, high contrast, "
        "dramatic lighting, bold focal subject, viral tiktok aesthetic"
    )
    url = (f"https://image.pollinations.ai/prompt/{prompt}"
           "?width=1080&height=1920&nologo=true&model=flux")
    img = OUT / "cover.png"
    http_get(url, img, dry)
    print(f"[3] kapak: {img.name} (Pollinations)")
    return img


# ---------------------------------------------------------------- 4) montaj

def gen_video(cover: Path, mp3: Path, srt: Path, subtitle_style: str, dry: bool) -> Path:
    """ffmpeg: kapak → 9:16 arka plan (hafif zoom) + ses + gömülü altyazı."""
    raw = OUT / "video_raw.mp4"
    final = OUT / "video_final.mp4"

    # 4a) arka plan: ses uzunluğunda, yavaş zoom yapan 1080x1920 video
    sh(["ffmpeg", "-y", "-loop", "1", "-i", str(cover), "-i", str(mp3),
        "-filter_complex",
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,zoompan=z='min(1.0+0.0006*on,1.15)'"
        ":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,"
        "format=yuv420p[v]",
        "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-preset", "fast",
        "-c:a", "aac", "-b:a", "128k", "-shortest", str(raw)], dry)
    print(f"[4] arka plan videosu: {raw.name} (ffmpeg zoompan)")

    # 4b) altyazı gömme (ASS stil şablonu)
    styles = {
        "karaoke_pop": "FontName=DejaVu Sans,Fontsize=22,PrimaryColour=&H00FFFFFF,"
                       "OutlineColour=&H00000000,Outline=3,Bold=1,Alignment=2,MarginV=60",
        "clean_minimal": "FontName=DejaVu Sans,Fontsize=20,PrimaryColour=&H00FFFFFF,"
                        "OutlineColour=&H00000000,Outline=2,Alignment=2,MarginV=40",
        "highlight_box": "FontName=DejaVu Sans,Fontsize=22,PrimaryColour=&H00F5D400,"
                         "OutlineColour=&H00000000,Outline=3,Bold=1,Alignment=2,MarginV=60",
    }
    style = styles.get(subtitle_style, styles["karaoke_pop"])
    vf = f"subtitles={ffmpeg_escape(srt)}:force_style='{style}'"
    sh(["ffmpeg", "-y", "-i", str(raw), "-vf", vf,
        "-c:v", "libx264", "-preset", "fast", "-c:a", "copy", str(final)], dry)
    print(f"[5] altyazı gömüldü: {final.name} (stil: {subtitle_style})")
    return final


# ---------------------------------------------------------------- 6) başlık

TITLE_SYSTEM_PROMPT = (
    "Sen TikTok başlık uzmanısın. Verilen konu için: 1 başlık (max 90 karakter, "
    "merak uyandıran), 4 alakalı hashtag (jenerik #fyp hariç). "
    'Sadece JSON döndür: {"title": "...", "hashtags": ["#a","#b","#c","#d"]}'
)


def gen_title(topic: str, dry: bool) -> dict:
    key = os.getenv("GROQ_API_KEY", "").strip()
    meta = {"title": f"{topic} hakkında kimsenin söylemediği gerçek 👀",
            "hashtags": [f"#{re.sub(r'[^a-z0-9ğüşıöç]', '', topic.lower())}",
                         "#keşfet", "#bilgi", "#tiktoktürkiye"]}
    if key and not dry:
        try:
            payload = json.dumps({
                "model": os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
                "messages": [{"role": "system", "content": TITLE_SYSTEM_PROMPT},
                             {"role": "user", "content": f"Konu: {topic}"}],
            }).encode()
            req = urllib.request.Request(  # noqa: S310
                "https://api.groq.com/openai/v1/chat/completions", data=payload,
                headers={"Authorization": f"Bearer {key}",
                         "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.loads(r.read())
            m = re.search(r"\{.*}", data["choices"][0]["message"]["content"],
                          re.DOTALL)
            if m:
                meta = json.loads(m.group(0))
        except Exception as e:  # noqa: BLE001
            print(f"  LLM başlık başarısız, şablon kullanılıyor: {e}")
    print(f"[6] başlık: {meta['title']}")
    return meta


# ---------------------------------------------------------------- main

def main() -> int:
    p = argparse.ArgumentParser(description="ViralForge video pipeline")
    p.add_argument("--topic", required=True)
    p.add_argument("--subtitle-style", default="karaoke_pop",
                   choices=["karaoke_pop", "clean_minimal", "highlight_box"])
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    dry = a.dry_run

    OUT.mkdir(exist_ok=True)
    print("=== ViralForge /make ===")
    if not dry:
        need_ffmpeg()

    text = gen_script(a.topic, dry)
    (OUT / "script_text.txt").write_text(text, encoding="utf-8")
    mp3, srt = gen_voice(text, dry)
    cover = gen_cover(a.topic, dry)
    final = gen_video(cover, mp3, srt, a.subtitle_style, dry)
    meta = gen_title(a.topic, dry)
    (OUT / "metadata.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print("""
=== BİTTİ ===
Çıktılar (output/):
  video_final.mp4  → TikTok'a yükleyeceğin video
  cover.png        → kapak görseli
  metadata.json    → başlık + hashtag (kopyala-yapıştır)
  voice.mp3        → seslendirme

Yükleme (önerilen, hesap güvenli):
  TikTok @birihtimalofficial → Video yükle → video_final.mp4
  → başlık ve hashtag'leri metadata.json'dan yapıştır
Not: otomatik yükleme (social-auto-upload) TikTok kurallarını ihlal edip
hesabını riske atabilir; bu yüzden varsayılan olarak önerilmiyor.
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
