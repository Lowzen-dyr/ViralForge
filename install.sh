#!/usr/bin/env bash
# ViralForge kurulum betiği — GitHub Codespaces veya Linux'ta tek komut.
# Tüm bileşenler ücretsizdir.

set -euo pipefail

echo "=== ViralForge kurulumu başlıyor ==="

# 1) Sistem bağımlılıkları (ffmpeg: video montaj, fontlar: altyazı)
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "[1/3] ffmpeg kuruluyor..."
  sudo apt-get update -qq
  sudo apt-get install -y -qq ffmpeg fonts-dejavu-core
else
  echo "[1/3] ffmpeg zaten kurulu ✔"
fi

# 2) Python bağımlılıkları (edge-tts, faster-whisper, pillow)
echo "[2/3] Python paketleri kuruluyor..."
pip install -q -r requirements.txt

# 3) Doğrulama
echo "[3/3] Doğrulama..."
python - <<'PY'
import shutil, importlib

missing = []
for mod in ("edge_tts", "faster_whisper", "PIL"):
    try:
        importlib.import_module(mod)
    except ImportError:
        missing.append(mod)

if shutil.which("ffmpeg") is None:
    missing.append("ffmpeg (PATH'te yok)")

if missing:
    raise SystemExit(f"Eksik: {missing}")
print("Tüm bileşenler hazır ✔")
PY

# Dry-run ile pipeline'ı sına
python pipeline/make.py --topic "kurulum testi" --dry-run

echo ""
echo "=== Kurulum tamamlandı ==="
echo "İlk videonu üretmek için:"
echo '  python pipeline/make.py --topic "konun buraya"'
