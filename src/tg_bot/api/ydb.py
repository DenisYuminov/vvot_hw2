import ydb
import ydb.iam
from util.environment import YDB_ENDPOINT, YDB_PATH


def get_db_session():
    """Создает и возвращает сессию для работы с YDB."""
    db_driver = ydb.Driver(
        endpoint=f"grpcs://{YDB_ENDPOINT}",
        database=YDB_PATH,
        credentials=ydb.iam.MetadataUrlCredentials(),
    )

    # Ожидание подключения с таймаутом 30 секунд
    db_driver.wait(fail_fast=True, timeout=30)

    # Создание клиента и сессии
    db_client = ydb.TableClient(db_driver)
    return db_client.session().create()


def get_unrecognized_face_id(session):
    """Возвращает ID нераспознанного лица, если таковое существует."""
    query = """
    SELECT face_id
    FROM photos
    WHERE face_name IS NULL AND is_processing = TRUE
    LIMIT 1
    """
    unrecognized_face = session.transaction().execute(query)[0].rows

    # Если есть лица в процессе обработки, возвращаем их ID
    if unrecognized_face:
        return unrecognized_face[0]["face_id"].decode("utf-8")

    # Если нет лиц в процессе обработки, выбираем просто нераспознанные
    query = "SELECT face_id FROM photos WHERE face_name IS NULL LIMIT 1"
    unrecognized_face = session.transaction().execute(query)[0].rows[0]
    return unrecognized_face["face_id"].decode("utf-8")


def get_processing_face_id(session):
    """Возвращает ID лица, которое в данный момент обрабатывается."""
    query = """
    SELECT face_id
    FROM photos
    WHERE face_name IS NULL AND is_processing = TRUE
    LIMIT 1
    """
    processing_face = session.transaction().execute(query)[0].rows[0]

    # Если лицо найдено, возвращаем его ID
    if processing_face:
        return processing_face["face_id"].decode("utf-8")
    else:
        raise Exception("No processing face found")


def set_is_processing(session, face_id, is_processing):
    """Обновляет статус 'is_processing' для указанного лица."""
    query = f"""
    UPDATE photos
    SET is_processing = {is_processing}
    WHERE face_id = '{face_id}'
    """
    session.transaction().execute(query, commit_tx=True)


def get_all_original_photos_with(session, name):
    """Возвращает список ID всех оригинальных фото для указанного имени лица."""
    query = f"SELECT photo_id FROM photos WHERE face_name = '{name}'"
    all_photos_with = session.transaction().execute(query)[0].rows

    # Возвращаем список photo_id, если они есть
    return [row["photo_id"].decode("utf-8") for row in all_photos_with] if all_photos_with else []


def save_name(session, name, face_id):
    """Сохраняет имя для указанного face_id."""
    query = f"""
    UPDATE photos
    SET face_name = '{name}'
    WHERE face_id = '{face_id}'
    """
    session.transaction().execute(query, commit_tx=True)
