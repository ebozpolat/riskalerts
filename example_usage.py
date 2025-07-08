#!/usr/bin/env python3
"""
Example usage of the Lark Webhook Client
"""

from lark_webhook import LarkWebhookClient
import json


def example_usage():
    """Demonstrate different ways to use the Lark webhook client"""
    
    # Replace with your actual webhook URL
    webhook_url = "https://open.larksuite.com/open-apis/bot/v2/hook/YOUR_WEBHOOK_TOKEN"
    
    # Initialize client
    client = LarkWebhookClient(webhook_url)
    
    print("=== Lark Webhook Examples ===\n")
    
    # Example 1: Simple text message (equivalent to your curl command)
    print("1. Sending simple text message...")
    result = client.send_text_message("request example")
    print(f"Result: {result}\n")
    
    # Example 2: Custom text message
    print("2. Sending custom text message...")
    result = client.send_text_message("Hello from Python! 🐍")
    print(f"Result: {result}\n")
    
    # Example 3: Rich text message
    print("3. Sending rich text message...")
    rich_content = [
        [
            {"tag": "text", "text": "This is a "},
            {"tag": "text", "text": "bold", "style": ["bold"]},
            {"tag": "text", "text": " message with "},
            {"tag": "a", "text": "a link", "href": "https://www.larksuite.com/"}
        ]
    ]
    result = client.send_rich_text_message("Rich Text Example", rich_content)
    print(f"Result: {result}\n")
    
    # Example 4: Card message (interactive)
    print("4. Sending card message...")
    card_content = {
        "config": {
            "wide_screen_mode": True
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "content": "**Hello World!**\nThis is a card message.",
                    "tag": "lark_md"
                }
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "content": "Click Me",
                            "tag": "plain_text"
                        },
                        "type": "primary"
                    }
                ]
            }
        ]
    }
    result = client.send_card_message(card_content)
    print(f"Result: {result}\n")


if __name__ == "__main__":
    example_usage()
