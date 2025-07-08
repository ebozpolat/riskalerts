#!/usr/bin/env python3
"""
Enhanced Lark Webhook Client with Group Chat Features
Supports group mentions, user mentions, and group-specific formatting
"""

import requests
import json
import sys
from typing import Dict, Any, Optional, List


class LarkGroupChatClient:
    """Enhanced client for sending messages to Lark group chats via webhook API"""
    
    def __init__(self, webhook_url: str):
        """
        Initialize the Lark group chat client
        
        Args:
            webhook_url: The complete webhook URL from Lark group chat
        """
        self.webhook_url = webhook_url
        self.headers = {
            'Content-Type': 'application/json'
        }
    
    def send_text_message(self, text: str) -> Dict[str, Any]:
        """
        Send a text message to the group chat
        
        Args:
            text: The text message to send
            
        Returns:
            Response from the API
        """
        payload = {
            "msg_type": "text",
            "content": {
                "text": text
            }
        }
        
        return self._make_request(payload)
    
    def send_message_with_mentions(self, text: str, user_ids: List[str] = None, mention_all: bool = False) -> Dict[str, Any]:
        """
        Send a message with user mentions to the group chat
        
        Args:
            text: The text message to send
            user_ids: List of user IDs to mention (optional)
            mention_all: Whether to mention all users in the group
            
        Returns:
            Response from the API
        """
        # Build mention text
        mention_text = ""
        if mention_all:
            mention_text = "<at user_id=\"all\">所有人</at> "
        elif user_ids:
            for user_id in user_ids:
                mention_text += f"<at user_id=\"{user_id}\">@user</at> "
        
        full_text = mention_text + text
        
        payload = {
            "msg_type": "text",
            "content": {
                "text": full_text
            }
        }
        
        return self._make_request(payload)
    
    def send_urgent_alert(self, title: str, message: str, mention_all: bool = True) -> Dict[str, Any]:
        """
        Send an urgent alert with @all mention and formatting
        
        Args:
            title: Alert title
            message: Alert message
            mention_all: Whether to mention all users (default: True)
            
        Returns:
            Response from the API
        """
        alert_text = f"🚨 **{title}** 🚨\n\n{message}"
        
        if mention_all:
            alert_text = "<at user_id=\"all\">所有人</at> " + alert_text
        
        payload = {
            "msg_type": "text",
            "content": {
                "text": alert_text
            }
        }
        
        return self._make_request(payload)
    
    def send_rich_alert_card(self, title: str, details: Dict[str, str], urgency: str = "high") -> Dict[str, Any]:
        """
        Send a rich card alert suitable for group chats
        
        Args:
            title: Alert title
            details: Dictionary of detail fields
            urgency: Alert urgency level (high, medium, low)
            
        Returns:
            Response from the API
        """
        # Color coding based on urgency
        color_map = {
            "high": "red",
            "medium": "orange", 
            "low": "blue"
        }
        
        # Build card elements
        elements = []
        
        # Title with urgency indicator
        urgency_emoji = "🚨" if urgency == "high" else "⚠️" if urgency == "medium" else "ℹ️"
        elements.append({
            "tag": "div",
            "text": {
                "content": f"{urgency_emoji} **{title}**",
                "tag": "lark_md"
            }
        })
        
        # Add details
        for key, value in details.items():
            elements.append({
                "tag": "div",
                "text": {
                    "content": f"**{key}:** {value}",
                    "tag": "lark_md"
                }
            })
        
        # Add timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elements.append({
            "tag": "div",
            "text": {
                "content": f"**Zaman:** {timestamp}",
                "tag": "lark_md"
            }
        })
        
        # Add action buttons for high urgency
        if urgency == "high":
            elements.append({
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "content": "Acil Müdahale",
                            "tag": "plain_text"
                        },
                        "type": "danger"
                    },
                    {
                        "tag": "button", 
                        "text": {
                            "content": "Detayları Gör",
                            "tag": "plain_text"
                        },
                        "type": "primary"
                    }
                ]
            })
        
        card_content = {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "title": {
                    "content": f"{urgency_emoji} Risk Management Alert",
                    "tag": "plain_text"
                },
                "template": color_map.get(urgency, "blue")
            },
            "elements": elements
        }
        
        payload = {
            "msg_type": "interactive",
            "card": card_content
        }
        
        return self._make_request(payload)
    
    def send_group_summary(self, alerts: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Send a summary of multiple alerts to the group
        
        Args:
            alerts: List of alert dictionaries with 'type', 'message', 'time' keys
            
        Returns:
            Response from the API
        """
        summary_text = "📊 **Risk Alert Summary**\n\n"
        
        for i, alert in enumerate(alerts, 1):
            alert_type = alert.get('type', 'Unknown')
            message = alert.get('message', 'No message')
            time = alert.get('time', 'Unknown time')
            
            summary_text += f"{i}. **{alert_type}**\n"
            summary_text += f"   {message}\n"
            summary_text += f"   ⏰ {time}\n\n"
        
        summary_text += f"Total Alerts: {len(alerts)}"
        
        payload = {
            "msg_type": "text",
            "content": {
                "text": summary_text
            }
        }
        
        return self._make_request(payload)
    
    def _make_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make the actual HTTP request to Lark API
        
        Args:
            payload: The JSON payload to send
            
        Returns:
            Response data or error information
        """
        try:
            response = requests.post(
                self.webhook_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            # Check if request was successful
            response.raise_for_status()
            
            # Parse response
            response_data = response.json()
            
            return {
                'success': True,
                'status_code': response.status_code,
                'data': response_data
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'status_code': getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
            }
        except json.JSONDecodeError as e:
            return {
                'success': False,
                'error': f'Failed to parse JSON response: {str(e)}',
                'status_code': response.status_code if 'response' in locals() else None
            }


def main():
    """Demo function showing group chat features"""
    
    # Replace with your actual webhook URL
    webhook_url = "https://open.larksuite.com/open-apis/bot/v2/hook/t-g206787iAEON7GKUSM3H7MEYKICF4OTYVUMQFNBX"
    
    # Initialize group chat client
    client = LarkGroupChatClient(webhook_url)
    
    print("=== Group Chat Alert Examples ===\n")
    
    # Example 1: Simple group message
    print("1. Sending simple group message...")
    result = client.send_text_message("📊 Daily trading summary ready for review.")
    print(f"Result: {result['success']}\n")
    
    # Example 2: Urgent alert with @all mention
    print("2. Sending urgent alert with @all mention...")
    result = client.send_urgent_alert(
        "CRITICAL PRICE MOVEMENT", 
        "BTC/USDT has moved +15% in the last 5 minutes. Immediate attention required!"
    )
    print(f"Result: {result['success']}\n")
    
    # Example 3: Rich card alert
    print("3. Sending rich card alert...")
    alert_details = {
        "Parite": "BTC/USDT",
        "Fiyat Değişimi": "+12.5%",
        "Mevcut Fiyat": "$45,230",
        "Hacim": "$1.2B",
        "Risk Seviyesi": "YÜKSEK"
    }
    result = client.send_rich_alert_card("Price Surge Detected", alert_details, "high")
    print(f"Result: {result['success']}\n")
    
    # Example 4: Alert summary
    print("4. Sending alert summary...")
    alerts = [
        {"type": "Price Alert", "message": "BTC +12%", "time": "14:30"},
        {"type": "Volume Alert", "message": "ETH volume spike", "time": "14:32"},
        {"type": "Spread Alert", "message": "XRP spread widening", "time": "14:35"}
    ]
    result = client.send_group_summary(alerts)
    print(f"Result: {result['success']}\n")


if __name__ == "__main__":
    main()
