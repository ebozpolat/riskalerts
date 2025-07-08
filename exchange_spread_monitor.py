#!/usr/bin/env python3
""" 
Cross-Exchange Spread and Price Difference Monitor with Lark Alerts
"""

import time
import requests
from lark_group_chat import LarkGroupChatClient

WEBHOOK_URL = "https://open.larksuite.com/open-apis/bot/v2/hook/5E2YcUz9UFWMOEE7QKt4oMtiQBqeUBLi"

SPREAD_THRESHOLD = 0.5  # USD
PRICE_DIFF_THRESHOLD_PCT = 1.0  # Percent
CHECK_INTERVAL_SEC = 300  # 5 minutes


def fetch_binance_price(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/ticker/bookTicker?symbol={symbol}"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
        return {
            "exchange": "Binance",
            "symbol": symbol,
            "bid": float(data["bidPrice"]),
            "ask": float(data["askPrice"]),
            "spread": float(data["askPrice"]) - float(data["bidPrice"])
        }
    except Exception as e:
        return {"exchange": "Binance", "error": str(e)}


def fetch_gateio_price(symbol="BTC_USDT"):
    url = "https://api.gate.io/api/v4/spot/tickers"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        tickers = res.json()
        for ticker in tickers:
            if ticker["currency_pair"] == symbol:
                return {
                    "exchange": "Gate.io",
                    "symbol": symbol,
                    "bid": float(ticker["highest_bid"]),
                    "ask": float(ticker["lowest_ask"]),
                    "spread": float(ticker["lowest_ask"]) - float(ticker["highest_bid"]),
                    "volume_usdt": float(ticker["quote_volume"]),
                    "price_change_24h": float(ticker["change_percentage"])
                }
        return {"exchange": "Gate.io", "error": f"{symbol} not found"}
    except Exception as e:
        return {"exchange": "Gate.io", "error": str(e)}


def send_alert(client, pair, bnb_data, gate_data):
    # Calculate price difference percentage
    if "error" in bnb_data or "error" in gate_data:
        print(f"Error in data for {pair}: Binance: {bnb_data.get('error')}, Gate.io: {gate_data.get('error')}")
        return

    price_diff = abs(bnb_data["bid"] - gate_data["bid"])
    avg_price = (bnb_data["bid"] + gate_data["bid"]) / 2
    price_diff_pct = (price_diff / avg_price) * 100

    alerts = []

    if bnb_data["spread"] > SPREAD_THRESHOLD:
        alerts.append(f"Binance spread is high: ${bnb_data['spread']:.4f}")
    if gate_data["spread"] > SPREAD_THRESHOLD:
        alerts.append(f"Gate.io spread is high: ${gate_data['spread']:.4f}")
    if price_diff_pct > PRICE_DIFF_THRESHOLD_PCT:
        alerts.append(f"Price difference between exchanges is {price_diff_pct:.2f}%")

    if not alerts:
        print(f"No alerts for {pair}. Spread and price difference within thresholds.")
        return

    # Compose alert message
    alert_text = f"🚨 Arbitrage Alert for {pair} 🚨\n\n"
    alert_text += f"Binance Bid: ${bnb_data['bid']:.2f}, Ask: ${bnb_data['ask']:.2f}, Spread: ${bnb_data['spread']:.4f}\n"
    alert_text += f"Gate.io Bid: ${gate_data['bid']:.2f}, Ask: ${gate_data['ask']:.2f}, Spread: ${gate_data['spread']:.4f}\n\n"
    alert_text += "\n".join(alerts)

    # Send rich card alert
    card_details = {
        "Binance Bid": f"${bnb_data['bid']:.2f}",
        "Binance Ask": f"${bnb_data['ask']:.2f}",
        "Binance Spread": f"${bnb_data['spread']:.4f}",
        "Gate.io Bid": f"${gate_data['bid']:.2f}",
        "Gate.io Ask": f"${gate_data['ask']:.2f}",
        "Gate.io Spread": f"${gate_data['spread']:.4f}",
        "Price Diff %": f"{price_diff_pct:.2f}%",
        "Volume (Gate.io)": f"${gate_data.get('volume_usdt', 0):,.2f}",
        "24h Change (Gate.io)": f"{gate_data.get('price_change_24h', 0):.2f}%"
    }

    result = client.send_rich_alert_card(f"Arbitrage Alert: {pair}", card_details, "high")
    if result['success']:
        print(f"✅ Alert sent for {pair}")
    else:
        print(f"❌ Failed to send alert for {pair}: {result['error']}")


def monitor_pairs(pairs):
    client = LarkGroupChatClient(WEBHOOK_URL)
    while True:
        for bnb_sym, gate_sym in pairs:
            bnb_data = fetch_binance_price(bnb_sym)
            gate_data = fetch_gateio_price(gate_sym)
            send_alert(client, bnb_sym, bnb_data, gate_data)
        print(f"Waiting {CHECK_INTERVAL_SEC} seconds before next check...")
        time.sleep(CHECK_INTERVAL_SEC)


if __name__ == "__main__":
    pairs = [("BTCUSDT", "BTC_USDT"), ("ETHUSDT", "ETH_USDT"), ("XRPUSDT", "XRP_USDT")]
    monitor_pairs(pairs)
