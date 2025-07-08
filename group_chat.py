# Group Chat Alert Setup Guide

## How to Send Alerts to Lark Group Chat

### Method 1: Group Webhook (Recommended - What you're using)

Your current webhook URL is already configured for a group chat. Here's how to optimize it:

#### Current Setup:
```python
WEBHOOK_URL = "https://open.larksuite.com/open-apis/bot/v2/hook/t-g206787iAEON7GKUSM3H7MEYKICF4OTYVUMQFNBX"
```

This webhook sends messages directly to the group chat where it was created.

### Method 2: Enhanced Group Features

Use the new `LarkGroupChatClient` for advanced group features:

```python
from lark_group_chat import LarkGroupChatClient

client = LarkGroupChatClient(WEBHOOK_URL)

# Send urgent alert with @all mention
client.send_urgent_alert("CRITICAL ALERT", "Message here")

# Send rich formatted card
details = {"Parite": "BTC/USDT", "Değişim": "+12%"}
client.send_rich_alert_card("Price Alert", details, "high")
```

## Group Chat Features Available:

### 1. **@All Mentions**
```python
# Mentions everyone in the group
client.send_urgent_alert("URGENT", "Critical message", mention_all=True)
```

### 2. **Rich Card Alerts**
```python
# Professional looking cards with color coding
alert_details = {
    "Parite": "BTC/USDT",
    "Fiyat": "$45,230", 
    "Değişim": "+12.5%",
    "Risk": "YÜKSEK"
}
client.send_rich_alert_card("Price Alert", alert_details, "high")
```

### 3. **Alert Summaries**
```python
# Send multiple alerts as a summary
alerts = [
    {"type": "Price Alert", "message": "BTC +12%", "time": "14:30"},
    {"type": "Volume Alert", "message": "ETH spike", "time": "14:32"}
]
client.send_group_summary(alerts)
```

### 4. **Urgency Levels**
- **High**: Red cards with action buttons, @all mentions
- **Medium**: Orange cards, no mentions
- **Low**: Blue cards for informational updates

## Setup Instructions:

### Step 1: Verify Group Webhook
Your webhook is already set up for a group. To confirm:
1. Go to your Lark group chat
2. Check if messages from your webhook appear there
3. If yes, you're all set!

### Step 2: Install Enhanced Client
```bash
pip install requests
```

### Step 3: Use Group Features
```python
# Run the enhanced group alerts
python group_risk_alerts.py
```

## Group Chat Best Practices:

### 1. **Alert Hierarchy**
- 🚨 **Critical**: Use @all mentions, red cards
- ⚠️ **Warning**: Orange cards, no mentions
- ℹ️ **Info**: Blue cards, summary format

### 2. **Message Formatting**
```python
# Good: Clear, structured alerts
client.send_urgent_alert(
    "PRICE SURGE DETECTED",
    "🚨 BTC/USDT: +12% in 10 minutes\n" +
    "📈 Current: $45,230\n" +
    "⚡ Action: Review positions"
)

# Avoid: Plain, unclear messages
client.send_text_message("btc up")
```

### 3. **Timing**
```python
import time

# Add delays between multiple alerts
client.send_urgent_alert("Alert 1", "Message 1")
time.sleep(2)  # Wait 2 seconds
client.send_urgent_alert("Alert 2", "Message 2")
```

### 4. **Group Etiquette**
- Use @all sparingly (only for critical alerts)
- Group similar alerts into summaries
- Use rich cards for important information
- Include timestamps and context

## Advanced Group Features:

### 1. **Conditional Mentions**
```python
# Only mention everyone for high-risk alerts
def send_smart_alert(message, risk_level):
    if risk_level == "critical":
        client.send_urgent_alert("CRITICAL", message, mention_all=True)
    else:
        client.send_text_message(f"📊 {message}")
```

### 2. **Alert Batching**
```python
# Collect alerts and send as batch
alerts_batch = []
# ... collect alerts ...
client.send_group_summary(alerts_batch)
```

### 3. **Interactive Cards**
Rich cards can include action buttons for immediate response.

## Troubleshooting:

### Issue: Messages not appearing in group
- **Solution**: Verify webhook URL is from the correct group
- **Check**: Group settings allow webhook messages

### Issue: @all mentions not working
- **Solution**: Ensure bot has mention permissions in group
- **Alternative**: Use text-based mentions

### Issue: Cards not displaying properly
- **Solution**: Check JSON structure, use simple text as fallback

## Example Usage:

```bash
# Run group chat simulation
python group_risk_alerts.py

# This will send:
# 1. Critical alert with @all mention
# 2. Rich volume spike card
# 3. Medium urgency spread alert  
# 4. Wash trading detection
# 5. Daily alert summary
# 6. System status update
```

Your current webhook URL is already configured for group chat, so all these features will work immediately!
