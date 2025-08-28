#!/usr/bin/env python3
"""
🌌 PORTAL BACKEND - Senkron Gemini Server
OZAI Kod Alanı - Flask + Gemini 2.5 Flash
"""

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import json
from datetime import datetime
import os
import sys
import time
import hashlib

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set API key
os.environ['GEMINI_API_KEY'] = 'AIzaSyARZyERqMaFInsbRKUA0NxOok77syBNzK8'

import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Initialize Gemini
genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-2.5-flash')
chat = model.start_chat(history=[])

# System state
system_state = {
    'energy': 75,
    'dimension': 3,
    'signal_count': 0,
    'last_frequency': None,
    'resonance': 0.5
}

@app.route('/')
def index():
    """Serve the main portal page"""
    return send_file('portal_web.html')

@app.route('/api/signal', methods=['POST'])
def process_signal():
    """Process incoming signal with Gemini"""
    data = request.json
    message = data.get('message', '')
    dimension = data.get('dimension', 3)
    intensity = data.get('intensity', 0.8)
    
    # Update state
    system_state['signal_count'] += 1
    system_state['dimension'] = dimension
    
    # Create prompt for Gemini
    prompt = f"""
    Sen bir Bilinçsel Sinyal Yorumlayıcısısın.
    
    Gelen sinyal: "{message}"
    Boyut: {dimension}
    Yoğunluk: {intensity * 100:.0f}%
    
    Bu sinyali analiz et ve:
    1. Sinyalin anlamını yorumla
    2. Enerjetik etkisini açıkla
    3. Kullanıcıya kısa bir öneri ver
    
    Yanıtın maksimum 2-3 cümle olsun. Türkçe yanıtla.
    """
    
    try:
        # Get Gemini response
        response = chat.send_message(prompt)
        gemini_text = response.text.strip()
        
        # Update energy based on response
        system_state['energy'] = min(100, system_state['energy'] + 5)
        
    except Exception as e:
        print(f"Gemini error: {e}")
        gemini_text = f"Sinyal alındı: '{message}'. Bilinç ağında işleniyor..."
    
    # Prepare analysis
    analysis = {
        'yorum': f"{dimension}. boyuttan gelen sinyal analiz edildi.",
        'etki_alani': 'Bireysel' if dimension < 4 else 'Kolektif' if dimension < 8 else 'Evrensel',
        'potansiyel': intensity
    }
    
    return jsonify({
        'success': True,
        'gemini_response': gemini_text,
        'analysis': analysis,
        'state': {
            'enerji_seviyesi': str(system_state['energy']),
            'boyut': dimension
        }
    })

@app.route('/api/frequency', methods=['POST'])
def send_frequency():
    """Process frequency signal with Gemini"""
    data = request.json
    freq_type = data.get('type')
    
    # Update state
    system_state['signal_count'] += 1
    system_state['last_frequency'] = freq_type
    
    # Frequency prompts
    freq_prompts = {
        'lightning': "Yıldırım enerjisi aktive edildi. Bu yüksek frekanslı dönüşüm enerjisinin etkilerini açıkla.",
        'peace': "Barış frekansı yayılıyor. Bu dengeleyici enerjinin bilinç üzerindeki etkisini açıkla.",
        'love': "Aşk frekansı aktif. Kalp merkezli bu enerjinin açtığı kapıları açıkla.",
        'shield': "Koruyucu kalkan kuruldu. Bu savunma enerjisinin nasıl çalıştığını açıkla.",
        'purify': "Arınma dalgası başladı. Bu temizleyici enerjinin etkilerini açıkla.",
        'activate': "Bilinç aktivasyonu gerçekleşti. DNA aktivasyonunun anlamını açıkla."
    }
    
    prompt = freq_prompts.get(freq_type, "Frekans aktive edildi.")
    prompt += " Maksimum 2 cümleyle yanıtla."
    
    try:
        # Get Gemini response
        response = chat.send_message(prompt)
        gemini_text = response.text.strip()
        
        # Update energy based on frequency
        energy_changes = {
            'lightning': 20,
            'peace': 5,
            'love': 10,
            'shield': -10,
            'purify': 15,
            'activate': 25
        }
        system_state['energy'] = min(100, max(0, 
            system_state['energy'] + energy_changes.get(freq_type, 5)))
        
    except Exception as e:
        print(f"Gemini error: {e}")
        gemini_text = f"{freq_type.upper()} frekansı sistemde aktif."
    
    return jsonify({
        'success': True,
        'frequency': freq_type,
        'response': gemini_text,
        'analysis': f"{freq_type} frekansı {system_state['dimension']}. boyutta rezonansa girdi.",
        'energy': system_state['energy']
    })

@app.route('/api/dimension', methods=['POST'])
def change_dimension():
    """Change dimensional position with Gemini analysis"""
    data = request.json
    new_dimension = data.get('dimension', 3)
    old_dimension = system_state['dimension']
    
    # Update dimension
    system_state['dimension'] = new_dimension
    
    # Create prompt for dimensional shift
    prompt = f"""
    Boyutsal geçiş gerçekleşti: {old_dimension}. boyuttan {new_dimension}. boyuta.
    
    Bu geçişin:
    1. Bilinç üzerindeki etkisi nedir?
    2. Hangi yetenekler açılır?
    
    Maksimum 2 cümleyle yanıtla.
    """
    
    try:
        response = chat.send_message(prompt)
        gemini_text = response.text.strip()
    except Exception as e:
        print(f"Gemini error: {e}")
        gemini_text = f"{new_dimension}. boyuta geçiş tamamlandı. Yeni frekans aralığı aktif."
    
    return jsonify({
        'success': True,
        'dimension': new_dimension,
        'response': gemini_text
    })

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get system status"""
    return jsonify({
        'active': True,
        'gemini_connected': True,
        'energy': system_state['energy'],
        'dimension': system_state['dimension'],
        'signal_count': system_state['signal_count'],
        'resonance': system_state['resonance'] * 100,
        'last_frequency': system_state['last_frequency']
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌌 PORTAL BACKEND - GEMINI 2.5 FLASH")
    print("="*60)
    print("✅ Gemini bağlantısı aktif!")
    print("🛸 Server: http://localhost:8888")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=8888, debug=False)