import boto3
from json import dumps
from util.environment import MESSAGE_QUEUE_URL, ACCESS_KEY, SECRET_KEY
from util.constants import SERVICE_NAME, ENDPOINT_URL, REGION_NAME

def send_message_to_queue(message):
    client = boto3.client(
        service_name=SERVICE_NAME,
        endpoint_url=ENDPOINT_URL,
        region_name=REGION_NAME,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )

    client.send_message(
        QueueUrl=MESSAGE_QUEUE_URL,
        MessageBody=dumps(message),
    )