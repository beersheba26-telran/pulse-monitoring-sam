"""Pulse values reducer Lambda.

Consumes pulse probe messages from SQS, stores pulses per device in DynamoDB,
and when the configured reduction period is reached, publishes a reduced pulse
probe to SNS and removes the stored item.
"""

from __future__ import annotations

import json
import os
from statistics import median
from typing import Any

import boto3
from boto3.dynamodb.conditions import Key 
from logger_config import logger


dynamodb = boto3.resource("dynamodb")
sns = boto3.client("sns")

TABLE_NAME = os.environ.get("REDUCING_DATA_TABLE_NAME", "")
TOPIC_ARN = os.environ.get("REDUCED_PULSE_VALUES_TOPIC_ARN", "")
REDUCING_PERIOD_SECONDS = int(os.environ.get("REDUCING_PERIOD_SECONDS", "3600"))


def get_device_item(table, device_id: str) -> dict[str, Any] | None:
    response = table.query(KeyConditionExpression=Key("device_id").eq(device_id), Limit=1)
    items = response.get("Items", [])
    item = None

    if items:
        item = items[0]

    return item


def store_new_device_item(table, device_id: str, pulse_value: int, create_at: int) -> None:
    table.put_item(
        Item={
            "device_id": device_id,
            "create_at": create_at,
            "pulse_values": [pulse_value],
        }
    )



def append_pulse_value(table, device_id: str, pulse_value: int) -> None:
    table.update_item(
        Key={"device_id": device_id},
        UpdateExpression="SET pulse_values = list_append(if_not_exists(pulse_values, :empty_list), :new_value)",
        ExpressionAttributeValues={
            ":empty_list": [],
            ":new_value": [pulse_value],
        },
    )



def publish_reduced_probe(payload: dict[str, Any], device_id: str, create_at: int) -> None:
    publish_kwargs = {
        "TopicArn": TOPIC_ARN,
        "Message": json.dumps(payload),
    }

    if TOPIC_ARN.endswith(".fifo"):
        publish_kwargs["MessageGroupId"] = device_id
        publish_kwargs["MessageDeduplicationId"] = f"{device_id}:{create_at}:{payload['timestamp']}"

    sns.publish(**publish_kwargs)



def reduce_device_item(table, device_id: str, pulse_values: list[int], create_at: int, last_probe_timestamp: int) -> None:
    reduced_payload = {
        "device_id": device_id,
        "min_pulse_value": min(pulse_values),
        "median_pulse_value": median(pulse_values),
        "max_pulse_value": max(pulse_values),
        "timestamp": last_probe_timestamp,
    }

    publish_reduced_probe(reduced_payload, device_id, create_at)
    table.delete_item(Key={"device_id": device_id})
    logger.debug("Published reduced values {}", reduced_payload)



def lambda_handler(event, context):
    """Process SQS pulse probes, update DynamoDB, and publish reduced values."""
    if not TABLE_NAME:
        raise RuntimeError("PULSE_TABLE_NAME is not set")
    if not TOPIC_ARN:
        raise RuntimeError("REDUCED_PULSE_VALUES_TOPIC_ARN is not set")

    table = dynamodb.Table(TABLE_NAME)
    records = event.get("Records", [])

    logger.debug("Received SQS records count={}", len(records))

    for record in records:
        body = record.get("body", "")
        message = json.loads(body)

        device_id = message.get("device_id")
        pulse_value = message.get("pulse")
        raw_timestamp = message.get("timestamp")

       

        device_id = str(device_id)
        pulse_value = int(pulse_value)
        probe_timestamp = int(raw_timestamp)

        item = get_device_item(table, device_id)

        if item is None:
            store_new_device_item(table, device_id, pulse_value, probe_timestamp)
            logger.debug(
                "Created device item {}",
                {"device_id": device_id, "create_at": probe_timestamp, "pulse": pulse_value},
            )
            continue

        create_at = int(item.get("create_at"))
        pulse_values = [int(value) for value in item.get("pulse_values", []) if value is not None]
        pulse_values.append(pulse_value)

        if probe_timestamp - create_at >= REDUCING_PERIOD_SECONDS:
            reduce_device_item(table, device_id, pulse_values, create_at, probe_timestamp)
            continue

        append_pulse_value(table, device_id, pulse_value)
        logger.debug(
            "Updated device item {}",
            {
                "device_id": device_id,
                "create_at": create_at,
                "pulse_values_count": len(pulse_values),
            },
        )
