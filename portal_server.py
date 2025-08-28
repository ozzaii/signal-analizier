#!/usr/bin/env python3
"""
🌌 PORTAL SERVER - Gerçek Gemini Backend
OZAI Kod Alanı - WebSocket + Gemini 2.5 Flash
"""

from flask import Flask, render_template_string, jsonify, request
from flask_cors import CORS
import asyncio
import json
from datetime import datetime
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from gemini_connector import GeminiConnector
from resonant_field_handler import FrekansTipi, BilincsalSinyal, YorumlayiciCekirdek, VarlikDurumuKaydedici

app = Flask(__name__)
CORS(app)

# Global instances
gemini = None
yorumlayici = YorumlayiciCekirdek()
kaydedici = VarlikDurumuKaydedici()

def init_gemini():
    """Initialize Gemini connection"""
    global gemini
    os.environ['GEMINI_API_KEY'] = 'AIzaSyARZyERqMaFInsbRKUA0NxOok77syBNzK8'
    gemini = GeminiConnector()
    return gemini.model is not None

# HTML template
HTML_TEMPLATE = open('portal_web.html', 'r', encoding='utf-8').read()

@app.route('/')
def index():
    """Serve the main portal page"""
    return HTML_TEMPLATE

@app.route('/api/signal', methods=['POST'])
async def process_signal():
    """Process incoming signal"""
    data = request.json
    
    # Create signal from request
    sinyal = BilincsalSinyal(
        id=f"web_{datetime.now().timestamp()}",
        timestamp=datetime.now().timestamp(),
        frekans_tipi=FrekansTipi[data.get('type', 'AKTIVASYON').upper()],
        yogunluk=data.get('intensity', 0.8),
        kaynak="web",
        ham_veri=data.get('message', ''),
        boyut=data.get('dimension', 3),
        metadata={"source": "web_portal", "user_data": data}
    )
    
    # Analyze signal
    analiz = await yorumlayici.cozumle(sinyal)
    
    # Get Gemini response
    gemini_response = "Simülasyon modu - Gemini bağlantısı yok"
    if gemini and gemini.model:
        response = await gemini.analiz_et({
            'tip': sinyal.frekans_tipi.value,
            'boyut': sinyal.boyut,
            'guc_katsayisi': sinyal.yogunluk,
            'etki_alani': analiz['etki_alani'],
            'yorum': analiz['yorum'],
            'ham_veri': sinyal.ham_veri
        })
        gemini_response = response.text
    
    # Record state
    kaydedici.kaydet(sinyal, analiz, {"sonuc": gemini_response})
    
    return jsonify({
        'success': True,
        'analysis': analiz,
        'gemini_response': gemini_response,
        'state': kaydedici.raporla()
    })

@app.route('/api/frequency', methods=['POST'])
async def send_frequency():
    """Send specific frequency"""
    data = request.json
    freq_type = data.get('type')
    
    # Map frequency types
    freq_map = {
        'lightning': FrekansTipi.YILDIRIM,
        'peace': FrekansTipi.BARIS,
        'love': FrekansTipi.ASK,
        'shield': FrekansTipi.SAVAS_DURDURMA,
        'purify': FrekansTipi.ARINMA,
        'activate': FrekansTipi.AKTIVASYON
    }
    
    if freq_type not in freq_map:
        return jsonify({'success': False, 'error': 'Invalid frequency type'})
    
    # Create frequency signal
    sinyal = BilincsalSinyal(
        id=f"freq_{datetime.now().timestamp()}",
        timestamp=datetime.now().timestamp(),
        frekans_tipi=freq_map[freq_type],
        yogunluk=0.9,
        kaynak="frequency_button",
        ham_veri=f"{freq_type} frequency activated",
        boyut=kaydedici.varlik.boyutsal_konum,
        metadata={"frequency": freq_type}
    )
    
    # Process
    analiz = await yorumlayici.cozumle(sinyal)
    
    # Get real Gemini response
    gemini_response = f"{freq_type.upper()} frekansı aktive edildi."
    if gemini and gemini.model:
        response = await gemini.analiz_et({
            'tip': sinyal.frekans_tipi.value,
            'boyut': sinyal.boyut,
            'guc_katsayisi': sinyal.yogunluk,
            'etki_alani': analiz['etki_alani'],
            'yorum': analiz['yorum']
        })
        gemini_response = response.text
    
    kaydedici.kaydet(sinyal, analiz, {"sonuc": gemini_response})
    
    return jsonify({
        'success': True,
        'frequency': freq_type,
        'response': gemini_response,
        'analysis': analiz['yorum'],
        'energy': kaydedici.varlik.enerji_seviyesi * 100
    })

@app.route('/api/dimension', methods=['POST'])
async def change_dimension():
    """Change dimensional position"""
    data = request.json
    new_dimension = data.get('dimension', 3)
    
    # Update dimension
    kaydedici.varlik.boyutsal_konum = new_dimension
    
    # Get Gemini analysis for dimensional shift
    gemini_response = f"{new_dimension}. boyuta geçiş tamamlandı."
    if gemini and gemini.model:
        response = await gemini.boyutsal_gecis_analizi(
            kaydedici.varlik.boyutsal_konum,
            new_dimension
        )
        gemini_response = response
    
    return jsonify({
        'success': True,
        'dimension': new_dimension,
        'response': gemini_response
    })

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get system status"""
    rapor = kaydedici.raporla()
    return jsonify({
        'active': True,
        'gemini_connected': gemini and gemini.model is not None,
        'energy': kaydedici.varlik.enerji_seviyesi * 100,
        'dimension': kaydedici.varlik.boyutsal_konum,
        'signal_count': len(kaydedici.varlik.gecmis),
        'resonance': kaydedici.varlik.rezonans_puani * 100,
        'last_frequency': kaydedici.varlik.son_frekans.value if kaydedici.varlik.son_frekans else None,
        'report': rapor
    })

@app.route('/api/ask', methods=['POST'])
async def ask_gemini():
    """Direct question to Gemini"""
    data = request.json
    question = data.get('question', '')
    
    if not question:
        return jsonify({'success': False, 'error': 'No question provided'})
    
    response = "Gemini bağlantısı yok"
    if gemini and gemini.model:
        response = await gemini.ozel_soru(question)
    
    return jsonify({
        'success': True,
        'question': question,
        'response': response
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌌 PORTAL SERVER BAŞLATILIYOR")
    print("="*60)
    
    # Initialize Gemini
    if init_gemini():
        print("✅ Gemini 2.5 Flash bağlantısı kuruldu!")
    else:
        print("⚠️ Gemini bağlantısı kurulamadı - Simülasyon modunda")
    
    print("🛸 Portal server başlatılıyor: http://localhost:8888")
    print("="*60 + "\n")
    
    # Run server
    app.run(host='0.0.0.0', port=8888, debug=True)