from json import loads
from api.yandex_cloud import get_original_photo, upload_face, get_face_uid
from api.face_cutter import cut_face
from api.ydb import save_relation, get_db_session

def handler(event, context):
    queue_message_body = event["messages"][0]["details"]["message"]["body"]
    message = loads(queue_message_body)

    original_photo_id, face_coordinates = message["original_photo_id"], message["face_coordinates"]
    original_photo = get_original_photo(original_photo_id)
    
    face = cut_face(original_photo, face_coordinates)
    face_id = get_face_uid()

    db_session = get_db_session()

    save_relation(db_session, original_photo_id, face_id)
    upload_face(face, face_id)

    return {
        "statusCode": 200,
    }