from json import loads
from api.telegram import send_message, send_photo
from util.constants import GET_FACE, FIND
from util.constants import ERROR_MESSAGE, NO_UNRECOGNIZED_FACES_MESSAGE, NO_PHOTOS_WITH, INTERNAL_ERROR
from util.environment import API_GW_URL
from api.ydb import get_unrecognized_face_id, get_all_original_photos_with, save_name, get_processing_face_id, set_is_processing, get_db_session

def handler(event, context):
    update = loads(event["body"])
    message = update.get("message")

    if message:
        handle_message(message)
    
    return {
        "statusCode": 200,
    }

def handle_message(message):
    text = message.get("text")

    db_session = get_db_session()

    # Пользователь отправил команду `/getface`
    if text == GET_FACE:
        try:
            unrecognized_face_id = get_unrecognized_face_id(db_session)
            set_is_processing(db_session, unrecognized_face_id, True)
            photo_url = f"{API_GW_URL}?face={unrecognized_face_id}"
            send_photo(photo_url, message)
        except Exception as e:
            send_message(NO_UNRECOGNIZED_FACES_MESSAGE, message)
        
        return {
            "statusCode": 200
        }
    
    # Пользователь в ответ на фото с лицом человека, полученное после команды `/getface`, отправил текст с именем этого человека
    elif text and (not text.startswith("/")) and (message.get("reply_to_message")):
        try:
            face_id = get_processing_face_id(db_session)
            save_name(db_session, text, face_id)
            set_is_processing(db_session, face_id, False)
        except Exception as e:
            send_message(INTERNAL_ERROR, message)

        return {
            "statusCode": 200
        }

    # Пользователь отправил команду `/find xyz`, где `xyz` - имя человека, фотографии с которым нужно найти
    elif text.startswith(FIND):
        name = text[(len(FIND) + 1):]
        original_photos_with = get_all_original_photos_with(db_session, name)

        if original_photos_with:
            for original in original_photos_with:
                send_photo(f"{API_GW_URL}?original_photo={original}", message)
        else:
            send_message(f"{NO_PHOTOS_WITH} '{name}'", message)
        
        return {
            "statusCode": 200
        }
    
    # Пользователь отправил неподдерживаемую ботом команду
    else:
        send_message(ERROR_MESSAGE, message)
        
        return {
            "statusCode": 200
        }
