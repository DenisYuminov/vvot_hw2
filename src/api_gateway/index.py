import base64
from pathlib import Path
from util.environment import PHOTOS_BUCKET, FACES_BUCKET
from util.constants import (
    STORAGE_PREFIX,
    MISSING_PARAMETER_ERROR_MESSAGE,
    FILE_NOT_FOUND_ERROR_MESSAGE,
    ERROR_READING_FILE_ERROR_MESSAGE
)


def handler(event, context):
    # Получение параметров запроса
    query_params = event.get('queryStringParameters', {})

    face_id = query_params.get('face')
    photo_id = query_params.get('original_photo')

    # Проверка наличия обязательных параметров
    if not face_id and not photo_id:
        return {
            'statusCode': 400,
            'body': MISSING_PARAMETER_ERROR_MESSAGE,
        }

    # Формирование пути к файлу в зависимости от наличия face_id или photo_id
    if face_id:
        file_path = Path(STORAGE_PREFIX, FACES_BUCKET, face_id)
    else:
        file_path = Path(STORAGE_PREFIX, PHOTOS_BUCKET, photo_id)

    # Проверка существования файла
    if not file_path.exists():
        return {
            'statusCode': 404,
            'body': FILE_NOT_FOUND_ERROR_MESSAGE,
        }

    # Чтение файла и обработка ошибок
    try:
        with open(file_path, "rb") as file:
            file_bytes = file.read()
    except Exception:
        return {
            'statusCode': 500,
            'body': ERROR_READING_FILE_ERROR_MESSAGE,
        }

    # Возвращение изображения в виде base64
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'image/jpeg'},
        'body': base64.b64encode(file_bytes).decode("utf-8"),
        'isBase64Encoded': True,
    }
