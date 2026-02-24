import re
import os
import logging
import time
import json
import requests

from dotenv import load_dotenv

def send_disc_message(message: str):
    load_dotenv()
    webhook_url = os.getenv('WEBHOOK_URL')
    
    data = {
        "content": message,
        "username": "Job Agent Alert" 
    }
    
    response = requests.post(webhook_url, json=data)

    # Check the response status code
    if 200 <= response.status_code < 300:
        print(f"Webhook sent successfully! Status code: {response.status_code}")
    else:
        print(f"Failed to send webhook. Status code: {response.status_code}, response: {response.text}")

