#!/usr/bin/env python3
"""
Enhanced Risk Alert Simulator for Group Chat
Uses group chat specific features like mentions and rich formatting
"""

import time
from lark_group_chat import LarkGroupChatClient

# Your group chat webhook URL
WEBHOOK_URL = "https://open.larksuite.com/open-apis/bot/v2/hook/t-g206787iAEON7GKUSM3H7MEYKICF4OTYVUMQFNBX"

def simulate_group_risk_alerts():
    """Simulate risk alerts specifically designed for group chat"""
    
    client = LarkGroupChatClient(WEBHOOK_URL)
    
    print("🚨 Starting Group Chat Risk Alert Simulation...\n")
    
    # Scenario 1: Critical alert with @all mention
    print("Scenario 1: Critical price movement (mentions everyone)")
    result = client.send_urgent_alert(
        "CRITICAL PRICE MOVEMENT",
        "🚨 BTC/USDT paritesinde son 10 dakikada %12 artış tespit edildi!\n\n" +
        "📈 Mevcut Fiyat: $45,230\n" +
        "⚡ Değişim: +12.5%\n" +
        "🔥 Acil inceleme gerekli!"
    )
    print(f"Status: {'✅ Success' if result['success'] else '❌ Failed'}")
    time.sleep(3)
    
    # Scenario 2: Rich card alert for volume spike
    print("Scenario 2: Volume spike with rich card format")
    volume_details = {
        "Parite": "ETH/USDT",
        "Hacim Artışı": "%350",
        "24h Hacim": "$2.8B",
        "Ortalama Hacim": "$800M",
        "Durum": "Anormal Aktivite Tespit Edildi",
        "Önerilen Aksiyon": "Manuel İnceleme"
    }
    result = client.send_rich_alert_card("Volume Spike Alert", volume_details, "high")
    print(f"Status: {'✅ Success' if result['success'] else '❌ Failed'}")
    time.sleep(3)
    
    # Scenario 3: Spread alert with medium urgency
    print("Scenario 3: Spread alert with medium urgency")
    spread_details = {
        "Parite": "XRP/USDT", 
        "Spread": "%6.2",
        "Normal Spread": "%0.8",
        "Artış Oranı": "%675",
        "Likidite Durumu": "Düşük",
        "Risk Seviyesi": "ORTA"
    }
    result = client.send_rich_alert_card("Spread Genişlemesi", spread_details, "medium")
    print(f"Status: {'✅ Success' if result['success'] else '❌ Failed'}")
    time.sleep(3)
    
    # Scenario 4: Wash trading detection
    print("Scenario 4: Wash trading detection alert")
    result = client.send_urgent_alert(
        "WASH TRADING ŞÜPHESİ",
        "⚠️ Kullanıcı ID: A7829 için anormal işlem paterni tespit edildi.\n\n" +
        "🔍 Tespit Edilen Aktiviteler:\n" +
        "• Aynı fiyattan sürekli alım-satım\n" +
        "• Kısa süre aralıklarında büyük hacimler\n" +
        "• Spread'i etkileyecek düzeyde işlemler\n\n" +
        "📋 Compliance ekibi bilgilendirildi.",
        mention_all=False  # Don't mention everyone for this type of alert
    )
    print(f"Status: {'✅ Success' if result['success'] else '❌ Failed'}")
    time.sleep(3)
    
    # Scenario 5: Multiple alerts summary
    print("Scenario 5: Daily alert summary")
    daily_alerts = [
        {
            "type": "Fiyat Uyarısı",
            "message": "BTC/USDT +12% (5 dakika)",
            "time": "14:30:15"
        },
        {
            "type": "Hacim Uyarısı", 
            "message": "ETH/USDT hacim %350 artış",
            "time": "14:32:42"
        },
        {
            "type": "Spread Uyarısı",
            "message": "XRP/USDT spread %6.2'ye yükseldi",
            "time": "14:35:18"
        },
        {
            "type": "Wash Trading",
            "message": "Kullanıcı A7829 şüpheli aktivite",
            "time": "14:38:55"
        },
        {
            "type": "Likidite Uyarısı",
            "message": "DOGE/USDT düşük likidite",
            "time": "14:42:33"
        }
    ]
    
    result = client.send_group_summary(daily_alerts)
    print(f"Status: {'✅ Success' if result['success'] else '❌ Failed'}")
    time.sleep(2)
    
    # Scenario 6: System status update
    print("Scenario 6: System status update")
    system_details = {
        "Sistem Durumu": "Aktif",
        "Monitör Edilen Pariteler": "47",
        "Aktif Uyarılar": "12",
        "Son Güncelleme": "14:45:22",
        "CPU Kullanımı": "%23",
        "Bellek Kullanımı": "%67",
        "Ağ Gecikmesi": "12ms"
    }
    result = client.send_rich_alert_card("Risk Sistemi Durumu", system_details, "low")
    print(f"Status: {'✅ Success' if result['success'] else '❌ Failed'}")
    
    print("\n✅ Group chat risk alert simulation completed!")

def send_custom_group_alert(alert_type: str, message: str, urgency: str = "medium"):
    """
    Send a custom alert to the group chat
    
    Args:
        alert_type: Type of alert
        message: Alert message
        urgency: Alert urgency level (high, medium, low)
    """
    client = LarkGroupChatClient(WEBHOOK_URL)
    
    if urgency == "high":
        result = client.send_urgent_alert(alert_type, message)
    else:
        result = client.send_text_message(f"📊 **{alert_type}**\n\n{message}")
    
    return result

def send_trading_summary():
    """Send end-of-day trading summary to group"""
    
    client = LarkGroupChatClient(WEBHOOK_URL)
    
    summary_details = {
        "Toplam İşlem Hacmi": "$45.2M",
        "En Aktif Parite": "BTC/USDT",
        "Günlük Kar/Zarar": "+$12,450",
        "Risk Uyarıları": "23",
        "Kritik Uyarılar": "3",
        "Sistem Uptime": "%99.8",
        "Ortalama Spread": "%0.12"
    }
    
    result = client.send_rich_alert_card("Günlük Trading Özeti", summary_details, "low")
    
    if result['success']:
        print("✅ Daily summary sent to group chat!")
    else:
        print(f"❌ Failed to send summary: {result['error']}")

if __name__ == "__main__":
    # Run the group chat simulation
    simulate_group_risk_alerts()
    
    print("\n" + "="*60)
    print("Sending daily trading summary...")
    
    # Send daily summary
    send_trading_summary()
    
    print("\n" + "="*60)
    print("Example of custom alert...")
    
    # Example custom alert
    custom_result = send_custom_group_alert(
        "MARKET MANIPULATION DETECTED",
        "🔍 ALGO/USDT paritesinde koordineli alım-satım aktivitesi tespit edildi.\n\n" +
        "Şüpheli hesaplar compliance ekibine yönlendirildi.",
        "high"
    )
    print(f"Custom alert status: {'✅ Success' if custom_result['success'] else '❌ Failed'}")
