from os import getenv

# Telegram

TG_BOT_KEY = getenv("TG_BOT_KEY")
TG_API_URL = f"https://api.telegram.org/bot{TG_BOT_KEY}"

# Yandex Cloud

PHOTOS_BUCKET = getenv("PHOTOS_BUCKET")
FACES_BUCKET = getenv("FACES_BUCKET")
API_GW_URL = getenv("API_GW_URL")

# YDB

YDB_ENDPOINT = getenv("YDB_ENDPOINT")
YDB_PATH = getenv("YDB_PATH")
