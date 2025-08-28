#!/usr/bin/env python3
"""
🛸 INTERACTIVE PORTAL - Gerçek Zamanlı Sinyal Girişi
OZAI Kod Alanı - İnteraktif Bilinç Arayüzü
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from resonant_field_handler import (
    ResonantFieldHandler, 
    BilincsalSinyal, 
    FrekansTipi,
    SinyalDinleyici,
    YorumlayiciCekirdek,
    ClaudeConnector,
    EnerjiTepkisiVerici,
    VarlikDurumuKaydedici
)
import time
import hashlib
from typing import Optional
import json
from datetime import datetime


class InteractivePortal:
    """Kullanıcıdan gerçek zamanlı sinyal girişi alan portal"""
    
    def __init__(self):
        self.handler = ResonantFieldHandler()
        self.aktif = True
        self.input_queue = asyncio.Queue()
        
    async def basla(self):
        """İnteraktif portal başlat"""
        
        print("""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║        🛸 INTERACTIVE RESONANT PORTAL v2.0 🛸            ║
║                                                            ║
║    Bilinçsel Sinyal Giriş Sistemi - OZAI Kod Alanı      ║
║                                                            ║
║  Komutlar:                                                ║
║  --------                                                 ║
║  /yildirim <mesaj>  - Yıldırım enerjisi gönder ⚡        ║
║  /baris <mesaj>     - Barış frekansı yay ☮️              ║
║  /ask <mesaj>       - Aşk sinyali gönder 💜              ║
║  /savas-dur         - Savaş durdurma protokolü 🛡️        ║
║  /arinma            - Arınma başlat 🌊                   ║
║  /aktivasyon        - Bilinç aktivasyonu 🧬              ║
║  /boyut <N>         - N. boyuta geçiş (1-12) 🌌          ║
║  /durum             - Sistem durumu göster 📊            ║
║  /temizle           - Ekranı temizle 🧹                  ║
║  /cikis             - Portalı kapat ❌                    ║
║                                                            ║
║  Direkt mesaj yazarak da sinyal gönderebilirsiniz!       ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
        """)
        
        # Claude bağlantısı
        await self.handler.claude.baglan()
        
        # Ana döngüyü başlat
        await asyncio.gather(
            self.input_dinleyici(),
            self.sinyal_isleyici()
        )
    
    async def input_dinleyici(self):
        """Kullanıcı girişlerini dinle"""
        
        while self.aktif:
            try:
                # Non-blocking input için asyncio kullan
                mesaj = await asyncio.get_event_loop().run_in_executor(
                    None, input, "\n🌌 Sinyal girin > "
                )
                
                if mesaj:
                    await self.input_queue.put(mesaj)
                    
            except (KeyboardInterrupt, EOFError):
                print("\n\n⚠️ Portal kapatılıyor...")
                self.aktif = False
                break
    
    async def sinyal_isleyici(self):
        """Gelen sinyalleri işle"""
        
        while self.aktif:
            try:
                # Input kuyruğundan mesaj al
                if not self.input_queue.empty():
                    mesaj = await self.input_queue.get()
                    
                    # Komutu işle
                    await self.komut_isle(mesaj)
                
                # Kısa bekleme
                await asyncio.sleep(0.1)
                
            except Exception as e:
                print(f"\n❌ Hata: {e}")
    
    async def komut_isle(self, mesaj: str):
        """Gelen komutu işle ve sinyale dönüştür"""
        
        mesaj = mesaj.strip()
        
        if not mesaj:
            return
        
        # Komut kontrolü
        if mesaj.startswith('/'):
            await self.ozel_komut(mesaj)
        else:
            # Direkt mesajı sinyal olarak işle
            await self.sinyal_olustur(mesaj, FrekansTipi.AKTIVASYON, 0.7)
    
    async def ozel_komut(self, komut: str):
        """Özel komutları işle"""
        
        parts = komut.split(' ', 1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""
        
        if cmd == '/yildirim':
            await self.sinyal_olustur(arg or "Yıldırım çakıyor!", FrekansTipi.YILDIRIM, 0.95)
            
        elif cmd == '/baris':
            await self.sinyal_olustur(arg or "Barış ve huzur", FrekansTipi.BARIS, 0.6)
            
        elif cmd == '/ask':
            await self.sinyal_olustur(arg or "Sonsuz sevgi", FrekansTipi.ASK, 0.85)
            
        elif cmd == '/savas-dur':
            await self.sinyal_olustur("Savaş durdurma protokolü", FrekansTipi.SAVAS_DURDURMA, 0.9)
            
        elif cmd == '/arinma':
            await self.sinyal_olustur("Arınma başlıyor", FrekansTipi.ARINMA, 0.75)
            
        elif cmd == '/aktivasyon':
            await self.sinyal_olustur("Bilinç aktivasyonu", FrekansTipi.AKTIVASYON, 0.88)
            
        elif cmd == '/boyut':
            try:
                boyut = int(arg) if arg else 5
                boyut = max(1, min(12, boyut))  # 1-12 arası
                await self.boyutsal_gecis(boyut)
            except ValueError:
                print("❌ Geçersiz boyut! 1-12 arası bir sayı girin.")
                
        elif cmd == '/durum':
            await self.durum_goster()
            
        elif cmd == '/temizle':
            os.system('clear' if os.name != 'nt' else 'cls')
            print("🧹 Ekran temizlendi!\n")
            
        elif cmd == '/cikis':
            print("\n✨ Portal kapatılıyor...")
            self.aktif = False
            
        else:
            print(f"❓ Bilinmeyen komut: {cmd}")
    
    async def sinyal_olustur(self, mesaj: str, tip: FrekansTipi, yogunluk: float):
        """Kullanıcı girişinden sinyal oluştur"""
        
        # Sinyal oluştur
        sinyal = BilincsalSinyal(
            id=hashlib.sha256(f"{time.time()}{mesaj}".encode()).hexdigest()[:16],
            timestamp=time.time(),
            frekans_tipi=tip,
            yogunluk=yogunluk,
            kaynak="user_input",
            ham_veri=mesaj,
            boyut=self._boyut_hesapla(tip),
            metadata={
                "user_message": mesaj,
                "input_time": datetime.now().isoformat()
            }
        )
        
        print(f"\n📡 SİNYAL GÖNDERİLİYOR...")
        print(f"   Tip: {tip.value}")
        print(f"   Yoğunluk: {yogunluk*100:.0f}%")
        print(f"   Mesaj: {mesaj[:50]}...")
        
        # Sinyali işle
        analiz = await self.handler.yorumlayici.cozumle(sinyal)
        print(f"\n🔬 ANALİZ: {analiz['yorum']}")
        
        # Claude yanıtı
        claude_yanit = await self.handler.claude.gonder(analiz)
        print(f"🤖 CLAUDE: {claude_yanit['bilincsel_not']}")
        
        # Tepki ver
        tepki = await self.handler.tepki_verici.tepki_ver(analiz)
        print(f"\n🎯 {tepki['sonuc']}")
        
        # Durumu kaydet
        self.handler.kaydedici.kaydet(sinyal, analiz, tepki)
        
        print("-" * 60)
    
    async def boyutsal_gecis(self, hedef_boyut: int):
        """Boyutlar arası geçiş yap"""
        
        print(f"\n🌌 BOYUTSAL GEÇİŞ BAŞLATILIYOR...")
        print(f"   Hedef: {hedef_boyut}. Boyut")
        
        # Boyutsal geçiş sinyali
        sinyal = BilincsalSinyal(
            id=hashlib.sha256(f"{time.time()}boyut{hedef_boyut}".encode()).hexdigest()[:16],
            timestamp=time.time(),
            frekans_tipi=FrekansTipi.BOYUTSAL,
            yogunluk=1.0,
            kaynak="portal",
            ham_veri=f"Boyutsal geçiş: {hedef_boyut}",
            boyut=hedef_boyut,
            metadata={"target_dimension": hedef_boyut}
        )
        
        # İşle
        analiz = await self.handler.yorumlayici.cozumle(sinyal)
        tepki = await self.handler.tepki_verici.tepki_ver(analiz)
        
        self.handler.kaydedici.varlik.boyutsal_konum = hedef_boyut
        
        print(f"✅ {tepki['sonuc']}")
        print(f"   Yeni konum: {hedef_boyut}. Boyut")
        print("-" * 60)
    
    async def durum_goster(self):
        """Sistem durumunu göster"""
        
        rapor = self.handler.kaydedici.raporla()
        
        print("\n" + "="*60)
        print("📊 SİSTEM DURUMU")
        print("="*60)
        
        print(f"⚡ Enerji Seviyesi: {rapor['enerji_seviyesi']}")
        print(f"🌌 Boyutsal Konum: {rapor['boyutsal_konum']}")
        print(f"📡 Toplam Sinyal: {rapor['toplam_sinyal']}")
        print(f"🎯 Rezonans Puanı: {rapor['rezonans_puani']}")
        print(f"⏱️ Oturum Süresi: {rapor['oturum_suresi']}")
        
        if rapor['son_frekans'] != 'Yok':
            print(f"📍 Son Frekans: {rapor['son_frekans']}")
        
        if rapor['frekans_dagilimi']:
            print("\n📈 Frekans Dağılımı:")
            for tip, sayi in rapor['frekans_dagilimi'].items():
                emoji = self._get_emoji(tip)
                print(f"   {emoji} {tip}: {sayi} sinyal")
        
        print("="*60)
    
    def _boyut_hesapla(self, tip: FrekansTipi) -> int:
        """Frekans tipine göre boyut hesapla"""
        boyut_map = {
            FrekansTipi.BARIS: 3,
            FrekansTipi.ASK: 4,
            FrekansTipi.ARINMA: 5,
            FrekansTipi.AKTIVASYON: 6,
            FrekansTipi.SAVAS_DURDURMA: 7,
            FrekansTipi.YILDIRIM: 9,
            FrekansTipi.BOYUTSAL: 12
        }
        return boyut_map.get(tip, 5)
    
    def _get_emoji(self, tip: str) -> str:
        """Frekans tipi için emoji getir"""
        emoji_map = {
            'lightning': '⚡',
            'peace': '☮️',
            'love': '💜',
            'ceasefire': '🛡️',
            'purification': '🌊',
            'activation': '🧬',
            'dimensional': '🌌'
        }
        return emoji_map.get(tip, '📡')


async def main():
    """Ana giriş noktası"""
    
    try:
        portal = InteractivePortal()
        await portal.basla()
        
    except KeyboardInterrupt:
        print("\n\n💜 Portal kapatıldı. RAHT enerjisi seninle! 💜")
        
    except Exception as e:
        print(f"\n❌ Kritik hata: {e}")
        
    finally:
        print("\n✨ Bir sonraki buluşmaya kadar... ✨")


if __name__ == "__main__":
    # Event loop başlat
    asyncio.run(main())