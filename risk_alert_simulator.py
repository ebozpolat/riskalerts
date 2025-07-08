#!/usr/bin/env python3
"""
Enhanced Cryptocurrency Risk Alert Simulator for Lark Group Chat
Uses LarkGroupChatClient for group chat features like mentions and rich cards
"""

import time
from lark_group_chat import LarkGroupChatClient

# Lark Group Chat Webhook URL - Replace with your actual webhook URL
WEBHOOK_URL = "https://open.larksuite.com/open-apis/bot/v2/hook/t-g206787iAEON7GKUSM3H7MEYKICF4OTYVUMQFNBX"

def send_lark_alert(client, message, mention_all=False):
    """
    Send alert message to Lark group chat using the enhanced client

    Args:
        client: Instance of LarkGroupChatClient
        message: Alert message to send
        mention_all: Whether to mention all users in the group
    """
    if mention_all:
        result = client.send_urgent_alert("Risk Alert", message, mention_all=True)
    else:
        result = client.send_text_message(message)

    if result['success']:
        print(f"✅ Alert sent successfully: {message[:50]}...")
    else:
        print(f"❌ Failed to send alert: {result['error']}")


def simulate_risk_conditions():
    """Simulate various cryptocurrency risk conditions with group chat features"""

    client = LarkGroupChatClient(WEBHOOK_URL)

    print("🚨 Starting Risk Alert Simulation with Group Chat Features...\n")

    # Scenario 1: Price surge with mention all
    print("Scenario 1: Price surge alert with @all mention")
    send_lark_alert(client, "🚨 BTC/USDT paritesinde son 10 dakikada %12 artış tespit edildi!", mention_all=True)
    time.sleep(2)

    # Scenario 2: Volume spike with rich card
    print("Scenario 2: Volume spike with rich card")
    volume_details = {
        "Parite": "ETH/USDT",
        "Hacim Artışı": "%350",
        "24h Hacim": "$2.8B",
        "Ortalama Hacim": "$800M",
        "Durum": "Anormal Aktivite Tespit Edildi",
        "Önerilen Aksiyon": "Manuel İnceleme"
    }
    result = client.send_rich_alert_card("Volume Spike Alert", volume_details, "high")
    if result['success']:
        print("✅ Volume spike alert sent successfully!")
    else:
        print(f"❌ Failed to send volume spike alert: {result['error']}")
    time.sleep(2)

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
    if result['success']:
        print("✅ Spread alert sent successfully!")
    else:
        print(f"❌ Failed to send spread alert: {result['error']}")
    time.sleep(2)

    # Scenario 4: Wash trading detection without mention all
    print("Scenario 4: Wash trading detection alert")
    send_lark_alert(client, "⚠️ Kullanıcı A'nın işlemleri wash trading şüphesi yaratıyor.", mention_all=False)
    time.sleep(2)

    # Scenario 5: Liquidation alert with mention all
    print("Scenario 5: Liquidation alert with @all mention")
    send_lark_alert(client, "💥 Son 5 dakikada $2.5M değerinde pozisyon tasfiye edildi!", mention_all=True)
    time.sleep(2)

    # Scenario 6: Market manipulation alert")
    print("Scenario 6: Market manipulation alert")
    send_lark_alert(client, "🔍 DOGE/USDT'de anormal işlem paterni tespit edildi. Manuel inceleme gerekli.")
    time.sleep(2)

    # Scenario 7: System alert with rich card
    print("Scenario 7: System alert with rich card")
    system_details = {
        "Sistem Durumu": "Aktif",
        "Monitör Edilen Pariteler": "47",
        "Aktif Uyarılar": "12",
        "Son Güncelleme": "14:45:22",
        "CPU Kullanımı": "%23",
        "Bellek Kullanımı": "%67",
        "Ağ Gecikmesi": "12ms"
    }
    result = client.send_rich_alert_card("Risk Yönetim Sistemi Durumu", system_details, "low")
    if result['success']:
        print("✅ System alert sent successfully!")
    else:
        print(f"❌ Failed to send system alert: {result['error']}")

    print("\n✅ Risk alert simulation with group chat features completed!")


if __name__ == "__main__":
    simulate_risk_conditions()
