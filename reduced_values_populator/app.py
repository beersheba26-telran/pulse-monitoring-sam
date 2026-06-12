import json
import os
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError
import pymongo

from logger_config import logger


def get_secret() -> str:
    secret_name = os.environ["DB_CREDENTIALS_SECRET_ARN"]
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)
    except ClientError:
        raise

    return response["SecretString"]


def _resolve_db_credentials() -> tuple[str, str, str]:
    secret_value = get_secret()
    secret_obj = json.loads(secret_value)

    uri = secret_obj.get("MONGO_URI")
    db_name = secret_obj.get("MONGO_DB_NAME")
    collection_name = secret_obj.get("REDUCED_VALUES_COLLECTION")

    if not uri or not db_name or not collection_name:
        raise ValueError("Secret is missing one or more required MongoDB fields")

    return uri, db_name, collection_name


def _build_document(data: dict) -> dict:
    device_id = data["device_id"]
    pulse_value = data["pulse_value"] if "pulse_value" in data else data["median_pulse_value"]
    timestamp = data["timestamp"]


    date_utc_naive_iso = (
        datetime.fromtimestamp(int(timestamp), tz=timezone.utc)
        .replace(tzinfo=None)
        .isoformat(timespec="seconds")
    )

    return {
        "device_id": device_id,
        "pulse_value": pulse_value,
        "date": date_utc_naive_iso,
    }


URI, DB_NAME, COLLECTION_NAME = _resolve_db_credentials()
MONGO_CLIENT = pymongo.MongoClient(URI)
COLLECTION = MONGO_CLIENT[DB_NAME][COLLECTION_NAME]


def _process_record(record: dict) -> None:
    sns_message = record.get("Sns", {})
    body = sns_message.get("Message", "")

    try:
       data = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Received invalid SNS message JSON: {body}") from exc

    document = _build_document(data)
    COLLECTION.insert_one(document)
    logger.debug(f"Inserted reduced values document {document}")


def lambda_handler(event, context):
    records = event.get("Records", [])

    for record in records:
        _process_record(record)



