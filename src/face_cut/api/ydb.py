import ydb
import ydb.iam
from util.environment import YDB_ENDPOINT, YDB_PATH

def get_db_session():
    db_driver = ydb.Driver(
        endpoint=f"grpcs://{YDB_ENDPOINT}",
        database=YDB_PATH,
        credentials=ydb.iam.MetadataUrlCredentials(),
    )
    db_driver.wait(fail_fast=True, timeout=30)
    db_client = ydb.TableClient(db_driver)
    
    return db_client.session().create()

def save_relation(session, original_photo_id, face_id):
    query = f"INSERT INTO photos (photo_id, face_id, is_processing) VALUES ('{original_photo_id}', '{face_id}', FALSE)"
    session.transaction().execute(query, commit_tx=True)