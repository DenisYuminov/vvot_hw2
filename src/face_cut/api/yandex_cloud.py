from PIL import Image
from pathlib import Path
from uuid import uuid4
from util.environment import FACES_BUCKET, PHOTOS_BUCKET
from util.constants import STORAGE_PREFIX

def get_original_photo(original_photo_id):
    photo_path = Path(STORAGE_PREFIX, PHOTOS_BUCKET, original_photo_id)
    with Image.open(photo_path) as image:
        image.load()
    
    return image

def get_face_uid():
    return f"{uuid4()}.jpg" 

def upload_face(face, face_id):
    face_path = Path(STORAGE_PREFIX, FACES_BUCKET, face_id)
    face.save(face_path)