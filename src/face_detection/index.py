from pathlib import Path
from api.yandex_cloud import send_message_to_queue
from api.face_detector import get_faces_coordinates
from util.environment import PHOTOS_BUCKET
from util.constants import STORAGE_PREFIX

def handler(event, context):
    original_photo_id = event["messages"][0]["details"]["object_id"]

    photo_path = Path(STORAGE_PREFIX, PHOTOS_BUCKET, original_photo_id)
    faces_coordinates = get_faces_coordinates(photo_path)

    for face in faces_coordinates:
        queue_message_body = {
            "original_photo_id": original_photo_id,
            "face_coordinates": face,
        }

        send_message_to_queue(queue_message_body)

    return {
        "statusCode": 200,
    }