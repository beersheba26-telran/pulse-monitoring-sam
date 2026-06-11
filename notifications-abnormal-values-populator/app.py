import json
import os
from datetime import datetime, timezone
from uuid import uuid4

import boto3
from botocore.exceptions import ClientError
import psycopg

from logger_config import logger

"""Notifications abnormal values populator Lambda.

Receives SNS abnormal values events and stores notification rows in PostgreSQL table
`notifications` using severity mapping by deviation of medium value from normal center value percentage:
- 60% - 70%: MINOR
- 71% - 90%: MAJOR
- >90%: CRITICAL
"""

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


def _resolve_db_uri() -> str:
	secret_value = get_secret()
	secret_obj = json.loads(secret_value)

	uri = secret_obj.get("URI")
	if not uri:
		raise ValueError("Secret is missing required URI field")

	return uri


MAJOR_THRESHOLD_PERCENT = int(os.environ.get("ABNORMAL_VALUES_MAJOR_THRESHOLD_PERCENT", "70"))
CRITICAL_THRESHOLD_PERCENT = int(os.environ.get("ABNORMAL_VALUES_CRITICAL_THRESHOLD_PERCENT", "90"))


def _to_severity(normal_central_value: int, medium_value: int) -> str:
	severity = "MINOR"
	deviation_percent = abs(medium_value - normal_central_value) / normal_central_value * 100
	if deviation_percent > CRITICAL_THRESHOLD_PERCENT:
		severity = "CRITICAL"
	elif deviation_percent > MAJOR_THRESHOLD_PERCENT:
		severity = "MAJOR"

	return severity


def _build_notification(payload: dict) -> dict:
	device_id = payload["device_id"]
	normal_central_value = payload["normal_range_center"]
	median_value = payload["median_pulse_value"]
	timestamp = payload["timestamp"]
	logger.debug(f"Building notification payload for device_id={device_id}, normal_central_value={normal_central_value}, median_value={median_value}, timestamp={timestamp}")

	severity = _to_severity(normal_central_value, median_value)
	created_at = datetime.fromtimestamp(timestamp, tz=timezone.utc)
	text = (
		f"Abnormal Pulse value detected for device {device_id}: "
		f"{normal_central_value} -> {median_value}."
	)

	return {
		"id": uuid4().hex,
		"created_at": created_at,
		"type": "ABNORMAL_PULSE",
		"status": "CREATED",
		"severity": severity,
		"text": text,
		"device_id": device_id,
	}


URI = _resolve_db_uri()


def _insert_notification(notification: dict) -> None:
	query = """
		INSERT INTO notifications (id, created_at, type, status, severity, text, device_id)
		VALUES (%s, %s, %s, %s, %s, %s, %s)
	"""

	try:
		with psycopg.connect(URI) as connection:
			with connection.cursor() as cursor:
				cursor.execute(
					query,
					(
						notification["id"],
						notification["created_at"],
						notification["type"],
						notification["status"],
						notification["severity"],
						notification["text"],
						notification["device_id"],
					),
				)
			connection.commit()
		logger.debug(f"Inserted notification id={notification['id']} for device_id={notification['device_id']}")
	except Exception:
		logger.error(f"Failed to insert notification id={notification['id']} for device_id={notification['device_id']}")
		raise

def _process_record(record: dict) -> None:
	sns_message = record.get("Sns", {})
	body = sns_message.get("Message", "")
	logger.debug(f"Processing SNS record with body length={len(body)}")

	try:
		payload = json.loads(body)
	except json.JSONDecodeError as exc:
		logger.error(f"Received invalid SNS message JSON: {body}")
		raise ValueError(f"Received invalid SNS message JSON: {body}") from exc

	try:
		notification = _build_notification(payload)
		_insert_notification(notification)
		logger.debug(f"Successfully processed notification id={notification['id']}")
	except Exception:
		logger.error(f"Failed processing SNS record payload={payload}")
		raise


def lambda_handler(event, context):
	records = event.get("Records", [])
	logger.debug(f"Received records count={len(records)}")
	for record in records:
		_process_record(record)