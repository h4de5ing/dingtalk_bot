import hmac
import hashlib
import base64
import urllib.parse
import requests
import time
import os

def generate_sign(timestamp, secret):
    string_to_sign = f'{timestamp}\n{secret}'
    hmac_code = hmac.new(secret.encode('utf-8'), string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()
    sign = base64.b64encode(hmac_code).decode('utf-8')
    return sign

def send_dingtalk_message(webhook_url, content, secret):
    timestamp = str(round(time.time() * 1000))
    sign = generate_sign(timestamp, secret)
    headers = {
        'Content-Type': 'application/json',
    }
    params = {
        'timestamp': timestamp,
        'sign': sign
    }
    data = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    response = requests.post(webhook_url, json=data, params=params, headers=headers)
    return response.status_code == 200

if __name__ == "__main__":
    webhook_url = os.environ.get('DINGTALK_WEBHOOK')
    secret = os.environ.get('DINGTALK_SECRET')
    content = "这是一条来自GitHub Actions的带签名消息。"
    if send_dingtalk_message(webhook_url, content, secret):
        print("DingTalk message sent successfully!")
    else:
        print("Failed to send DingTalk message.")