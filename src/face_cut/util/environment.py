from os import getenv

PHOTOS_BUCKET = getenv("PHOTOS_BUCKET")
FACES_BUCKET = getenv("FACES_BUCKET")
ACCESS_KEY = getenv("ACCESS_KEY")
SECRET_KEY = getenv("SECRET_KEY")

# YDB

YDB_ENDPOINT = getenv("YDB_ENDPOINT")
YDB_PATH = getenv("YDB_PATH")