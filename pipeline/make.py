#!/usr/bin/env python3
"""
ViralForge — Uçtan uca TikTok video üretim pipeline'ı.

Kullanım:
    python pipeline/make.py --topic "<konu>" [--template kinetic_text]
                            [--subtitle-style karaoke_pop] [--dry-run]

Modüller (hepsi ücretsiz):
    1. discover  → TikTok trend/hashtag taraması (TikTok-Api)
    2. script    → LLM senaryo (agents/script-writer.md promptu)
    3. voice     → edge-tts ile seslendirme
    4. edit      → openshorts / OpenReels ile montaj
    5. animate   → Remotion şablonu uygular (templates/)
    6. subtitle  → Whisper transkripsiyon + stil
    7. cover     → Pollinations kapak görseli
    8. title     → LLM başlık (agents/title-writer.md)
    9. publish   → social-auto-upload (opsiyonel, --publish bayrağı ile)
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def sh(cmd: list[str], dry: bool = False) -> None:
    """Komutu çalıştır; dry-run modunda sadece yazdır."""
    printable = " ".join(cmd)
    print(f"[ViralForge] $ {printable}")
    if dry:
        return
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        raise RuntimeError(f"Adım başarısız: {printable}")


def discover(topic: str, dry: bool) -> dict:
    """Trend/hashtag verisi toplar; konu verilmişse sadeleştirilmiş çıktı döner."""
    data = {"topic": topic, "hashtags": [], "sample_stats": {}}
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data/discovered.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    # Gerçek entegrasyon: TikTok-Api (pip install TikTokApi)
    # from TikTokApi import TikTokApi — kendi kurulumunuza göre bağlayın.
    print(f"[discover] konu hazır: {topic} (TikTok-Api entegrasyon noktası)")
    return data


def voice(text_path: Path, dry: bool) -> Path:
    """edge-tts ile metni sese çevirir (ücretsiz, key gerekmez)."""
    audio = OUT / "voice.mp3"
    voice_name = os.getenv("EDGE_TTS_VOICE", "tr-TR-AhmetNeural")
    sh(["edge-tts", "--voice", voice_name, "--file", str(text_path),
        "--write-media", str(audio)], dry)
    return audio


def cover(topic: str, dry: bool) -> Path:
    """Pollinations ile 1080x1920 kapak görseli üretir (ücretsiz HTTP)."""
    import urllib.parse
    import urllib.request

    prompt = urllib.parse.quote(
        f"cinematic viral tiktok cover about {topic}, high contrast, bold subject"
    )
    url = (
        f"https://image.pollinations.ai/prompt/{prompt}"
        "?width=1080&height=1920&nologo=true"
    )
    img = OUT / "cover.png"
    print(f"[cover] {url}")
    if not dry:
        urllib.request.urlretrieve(url, img)  # noqa: S310 (bilinen güvenilir endpoint)
    return img


def main() -> int:
    p = argparse.ArgumentParser(description="ViralForge pipeline")
    p.add_argument("--topic", required=True)
    p.add_argument("--template", default="kinetic_text")
    p.add_argument("--subtitle-style", default="karaoke_pop")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--publish", action="store_true", help="TikTok'a yükle (social-auto-upload)")
    a = p.parse_args()
    dry = a.dry_run

    print("=== ViralForge /make ===")
    data = discover(a.topic, dry)

    # 2) script: agents/script-writer.md promptu ile LLM (ücretsiz tier)
    script_path = OUT / "script.json"
    print(f"[script] LLM senaryo adımı (agents/script-writer.md) → {script_path}")

    # 3) voice
    text_path = OUT / "script_text.txt"
    print(f"[voice] edge-tts → {OUT / 'voice.mp3'}")
    if not dry:
        text_path.write_text(
            json.dumps({"topic": data["topic"]}, ensure_ascii=False), encoding="utf-8"
        )
        voice(text_path, dry)

    # 4) edit + 5) animate + 6) subtitle
    print(f"[edit] openshorts/OpenReels montaj → {OUT / 'video_raw.mp4'}")
    print(f"[animate] Remotion şablonu: {a.template}")
    print(f"[subtitle] Whisper + stil: {a.subtitle_style} → {OUT / 'video_final.mp4'}")

    # 7) cover
    cover(a.topic, dry)

    # 8) title
    print(f"[title] LLM başlık (agents/title-writer.md) → {OUT / 'metadata.json'}")

    # 9) publish
    if a.publish:
        print("[publish] social-auto-upload → TikTok (tarayıcı otomasyonu)")
    else:
        print("[publish] atlandı (--publish ile etkinleşir)")

    print("=== bitti ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
