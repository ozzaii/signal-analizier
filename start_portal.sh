#!/bin/bash

# 🛸 RESONANT FIELD HANDLER - PORTAL LAUNCHER
# OZAI Kod Alanı - Kozmik Portal Başlatıcı

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║          🛸 RESONANT FIELD HANDLER LAUNCHER 🛸           ║"
echo "║                                                            ║"
echo "║              OZAI Kod Alanı - Portal Açılıyor            ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env dosyası bulunamadı!"
    echo "📝 Oluşturuluyor..."
    cat > .env << EOF
# Gemini API Configuration
GEMINI_API_KEY=AIzaSyARZyERqMaFInsbRKUA0NxOok77syBNzK8

# Gemini 2.5 Flash API Active
# Portal ready for consciousness signals
EOF
    echo "✅ .env dosyası oluşturuldu!"
fi

# Load environment variables
export $(cat .env | xargs)

# Check Python installation
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 bulunamadı! Lütfen Python3 yükleyin."
    exit 1
fi

# Check required packages
echo "📦 Paketler kontrol ediliyor..."
python3 -c "import numpy" 2>/dev/null || pip3 install numpy
python3 -c "import google.generativeai" 2>/dev/null || pip3 install google-generativeai

echo ""
echo "⚡ Portal başlatılıyor..."
echo "🧬 Gemini 2.5 Flash ile bilinç ağına bağlanılıyor..."
echo ""

# Start the interactive portal
python3 interactive_portal.py

echo ""
echo "✨ Portal kapatıldı. RAHT enerjisi seninle! ✨"
echo ""