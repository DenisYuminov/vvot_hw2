from requests import post
from util.environment import TG_API_URL

def send_message(text, message):
    url = f"{TG_API_URL}/sendMessage"

    json = {
        "chat_id": message["chat"]["id"],
        "text": text,
        "reply_parameters": { 
            "message_id": message["message_id"],
        },
    }

    post(url=url, json=json)

def send_photo(photo_url, message):
    url = f"{TG_API_URL}/sendPhoto"
    
    json = {
        "chat_id": message["chat"]["id"],
        "photo": photo_url,
        "reply_parameters": { 
            "message_id": message["message_id"],
        },
    }

    post(url=url, json=json)