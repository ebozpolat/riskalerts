#!/usr/bin/env python3
"""
Lark (Feishu) Webhook API Client
Script to send messages to Lark via webhook API
"""

import requests
import json
import sys
from typing import Dict, Any, Optional


class LarkWebhookClient:
    """Client for sending messages to Lark via webhook API"""
    
    def __init__(self, webhook_url: str):
        """
        Initialize the Lark webhook client
        
        Args:
            webhook_url: The complete webhook URL from Lark
        """
        self.webhook_url = webhook_url
        self.headers = {
            'Content-Type': 'application/json'
        }
    
    def send_text_message(self, text: str) -> Dict[str, Any]:
        """
        Send a text message to Lark
        
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
    
    def send_rich_text_message(self, title: str, content: list) -> Dict[str, Any]:
        """
        Send a rich text message to Lark
        
        Args:
            title: Title of the message
            content: List of rich text elements
            
        Returns:
            Response from the API
        """
        payload = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": title,
                        "content": content
                    }
                }
            }
        }
        
        return self._make_request(payload)
    
    def send_card_message(self, card_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a card message to Lark
        
        Args:
            card_content: Card content structure
            
        Returns:
            Response from the API
        """
        payload = {
            "msg_type": "interactive",
            "card": card_content
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
    """Main function to demonstrate usage"""
    
    # Replace with your actual webhook URL
    webhook_url = "https://open.larksuite.com/open-apis/bot/v2/hook/****"
    
    # Check if webhook URL is provided as command line argument
    if len(sys.argv) > 1:
        webhook_url = sys.argv[1]
    
    # Check if webhook URL is still placeholder
    if "****" in webhook_url:
        print("Error: Please replace the webhook URL with your actual Lark webhook URL")
        print("Usage: python lark_webhook.py <webhook_url> [message]")
        sys.exit(1)
    
    # Initialize client
    client = LarkWebhookClient(webhook_url)
    
    # Get message from command line or use default
    message = "request example"
    if len(sys.argv) > 2:
        message = sys.argv[2]
    
    # Send the message
    print(f"Sending message: '{message}'")
    result = client.send_text_message(message)
    
    # Print result
    if result['success']:
        print("✅ Message sent successfully!")
        print(f"Status Code: {result['status_code']}")
        print(f"Response: {json.dumps(result['data'], indent=2)}")
    else:
        print("❌ Failed to send message!")
        print(f"Error: {result['error']}")
        if result['status_code']:
            print(f"Status Code: {result['status_code']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
