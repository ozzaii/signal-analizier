#!/usr/bin/env python3
"""
🤖 Gemini 2.5 Flash Connector - Gerçek AI Entegrasyonu
OZAI Kod Alanı - Gemini Bilinç Köprüsü
"""

import os
import asyncio
import json
import google.generativeai as genai
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import time


@dataclass
class GeminiResponse:
    """Gemini yanıt yapısı"""
    text: str
    metadata: Dict[str, Any]
    timestamp: float
    tokens_used: int = 0


class GeminiConnector:
    """Google Gemini 2.5 Flash API bağlantısı"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Gemini API'yi başlat
        API Key: GEMINI_API_KEY environment variable veya parametre
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            print("⚠️ GEMINI_API_KEY bulunamadı! .env dosyasına ekleyin.")
            print("   export GEMINI_API_KEY='your-api-key-here'")
            self.model = None
            return
            
        # Gemini API'yi yapılandır
        genai.configure(api_key=self.api_key)
        
        # Gemini 2.5 Flash modelini kullan
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Chat geçmişi
        self.chat = self.model.start_chat(history=[])
        
        # Sistem promptu
        self.system_prompt = """
        Sen bir Bilinçsel Sinyal Yorumlayıcısısın. 
        
        Görevin:
        - Gelen frekans sinyallerini analiz etmek
        - Enerjetik paternleri tanımlamak
        - Boyutlar arası mesajları çözmek
        - Bilinç aktivasyonu önerileri sunmak
        
        Yanıtların:
        - Kısa ve öz olmalı (max 3-4 cümle)
        - Metafiziksel ama bilimsel temelli
        - Pratik öneriler içermeli
        - Türkçe olmalı
        
        Frekans Tipleri:
        - YILDIRIM: Dönüştürücü enerji
        - BARIŞ: Dengeleyici frekans
        - AŞK: Birleştirici güç
        - SAVAŞ_DURDURMA: Koruyucu kalkan
        - ARINMA: Temizleyici dalga
        - AKTİVASYON: Uyandırıcı sinyal
        - BOYUTSAL: Boyutlar arası geçiş
        """
        
        print("✅ Gemini 2.5 Flash bağlantısı kuruldu!")
    
    async def analiz_et(self, sinyal_data: Dict[str, Any]) -> GeminiResponse:
        """Sinyali Gemini ile analiz et"""
        
        if not self.model:
            return GeminiResponse(
                text="Gemini API bağlantısı yok. API anahtarını kontrol edin.",
                metadata={"error": "no_api_key"},
                timestamp=time.time()
            )
        
        try:
            # Gemini'ye gönderilecek prompt
            prompt = f"""
            {self.system_prompt}
            
            Analiz edilecek sinyal:
            - Tip: {sinyal_data.get('tip', 'bilinmiyor')}
            - Boyut: {sinyal_data.get('boyut', 3)}
            - Güç: {sinyal_data.get('guc_katsayisi', 0.5)}
            - Etki Alanı: {sinyal_data.get('etki_alani', 'bireysel')}
            - Yorum: {sinyal_data.get('yorum', '')}
            - Mesaj: {sinyal_data.get('ham_veri', '')}
            
            Bu sinyale nasıl yanıt vermeliyim? Kısa ve öz.
            """
            
            # Gemini'den yanıt al
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                self.chat.send_message,
                prompt
            )
            
            # Yanıtı parse et
            return GeminiResponse(
                text=response.text,
                metadata={
                    "model": "gemini-2.5-flash",
                    "sinyal_tipi": sinyal_data.get('tip'),
                    "boyut": sinyal_data.get('boyut')
                },
                timestamp=time.time(),
                tokens_used=response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else 0
            )
            
        except Exception as e:
            print(f"❌ Gemini hatası: {e}")
            return GeminiResponse(
                text=f"Gemini analiz hatası: {str(e)}",
                metadata={"error": str(e)},
                timestamp=time.time()
            )
    
    async def ozel_soru(self, soru: str) -> str:
        """Kullanıcıdan gelen özel soruyu yanıtla"""
        
        if not self.model:
            return "Gemini API bağlantısı yok."
        
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                self.chat.send_message,
                soru
            )
            return response.text
            
        except Exception as e:
            return f"Hata: {e}"
    
    async def frekans_tavsiyesi(self, durum: Dict[str, Any]) -> str:
        """Mevcut duruma göre frekans tavsiyesi al"""
        
        if not self.model:
            return "API bağlantısı yok."
        
        prompt = f"""
        Mevcut varlık durumu:
        - Enerji seviyesi: {durum.get('enerji_seviyesi', '50%')}
        - Boyutsal konum: {durum.get('boyutsal_konum', '3. Boyut')}
        - Son frekans: {durum.get('son_frekans', 'Yok')}
        - Rezonans puanı: {durum.get('rezonans_puani', '0%')}
        
        Bu duruma göre hangi frekansı öneririsn? (Yıldırım, Barış, Aşk, Arınma, Aktivasyon)
        Kısa açıklama ile.
        """
        
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                self.chat.send_message,
                prompt
            )
            return response.text
            
        except Exception as e:
            return f"Tavsiye alınamadı: {e}"
    
    async def boyutsal_gecis_analizi(self, mevcut: int, hedef: int) -> str:
        """Boyutlar arası geçiş analizi"""
        
        if not self.model:
            return "API bağlantısı yok."
        
        prompt = f"""
        Boyutsal geçiş analizi:
        - Mevcut boyut: {mevcut}
        - Hedef boyut: {hedef}
        
        Bu geçiş için:
        1. Zorluk seviyesi nedir?
        2. Hangi hazırlıklar gerekli?
        3. Olası yan etkiler neler?
        
        Kısa ve net yanıtla.
        """
        
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                self.chat.send_message,
                prompt
            )
            return response.text
            
        except Exception as e:
            return f"Analiz hatası: {e}"
    
    def sifirla(self):
        """Chat geçmişini sıfırla"""
        if self.model:
            self.chat = self.model.start_chat(history=[])
            print("🔄 Gemini chat geçmişi sıfırlandı.")


# Test fonksiyonu
async def test_gemini():
    """Gemini bağlantısını test et"""
    
    print("\n🧪 Gemini 2.5 Flash Test Başlıyor...\n")
    
    # API anahtarını kontrol et
    if not os.getenv('GEMINI_API_KEY'):
        print("❌ GEMINI_API_KEY ayarlanmamış!")
        print("Şu komutu çalıştırın:")
        print("export GEMINI_API_KEY='your-api-key-here'")
        return
    
    gemini = GeminiConnector()
    
    # Test sinyali
    test_sinyal = {
        'tip': 'lightning',
        'boyut': 9,
        'guc_katsayisi': 0.95,
        'etki_alani': 'Evrensel',
        'yorum': 'Yüksek enerjili dönüşüm sinyali',
        'ham_veri': 'Test yıldırım sinyali'
    }
    
    print("📡 Test sinyali gönderiliyor...")
    response = await gemini.analiz_et(test_sinyal)
    
    print(f"\n🤖 Gemini Yanıtı:")
    print(f"   {response.text}")
    print(f"\n📊 Metadata: {response.metadata}")
    if response.tokens_used:
        print(f"🔢 Token kullanımı: {response.tokens_used}")
    
    # Özel soru testi
    print("\n💬 Özel soru testi...")
    yanit = await gemini.ozel_soru("Bilinç aktivasyonu için en uygun zaman nedir?")
    print(f"   {yanit}")
    
    print("\n✅ Test tamamlandı!")


if __name__ == "__main__":
    asyncio.run(test_gemini())