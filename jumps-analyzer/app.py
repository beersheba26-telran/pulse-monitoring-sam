"""Pulse values reducer Lambda.

Consumes pulse probe messages from SQS, stores pulses per device in DynamoDB,
and when the configured reduction period is reached, publishes a reduced pulse
probe to SNS and removes the stored item.
"""

from __future__ import annotations

import json
import os
from time import time
from typing import Any

import boto3
from boto3.dynamodb.conditions import Key 
from logger_config import logger


dynamodb = boto3.resource("dynamodb")
sns = boto3.client("sns")

TABLE_NAME = os.environ.get("LAST_PULSE_VALUES_TABLE_NAME", "")
TOPIC_ARN = os.environ.get("PULSE_JUMPS_TOPIC_ARN", "")
JUMP_THRESHOLD_PERCENT = int(os.environ.get("JUMP_THRESHOLD_PERCENT", "40"))

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
            "last_value": pulse_value,
        }
    )



def update_last_pulse_value(table, device_id: str, pulse_value: int) -> None:
    table.update_item(
        Key={"device_id": device_id},
        UpdateExpression="SET last_value = :new_value, create_at = :create_at",
        ExpressionAttributeValues={
            ":new_value": pulse_value,
            ":create_at": int(time()),
        },
    )



def publish_jump_probe(payload: dict[str, Any]) -> None:
    publish_kwargs = {
        "TopicArn": TOPIC_ARN,
        "Message": json.dumps(payload),
    }

    if TOPIC_ARN.endswith(".fifo"):
        publish_kwargs["MessageGroupId"] = payload["device_id"]
        publish_kwargs["MessageDeduplicationId"] = f"{payload['device_id']}:{payload['timestamp']}"

    sns.publish(**publish_kwargs)



def create_jump_probe(table, device_id: str, previous_pulse_value: int, current_pulse_value: int, last_probe_timestamp: int) -> None:
    jump_payload = {
        "device_id": device_id,
        "previous_pulse_value": previous_pulse_value,
        "current_pulse_value": current_pulse_value,
        "timestamp": last_probe_timestamp,
    }

    publish_jump_probe(jump_payload)
    
    logger.debug("Published jump probe {}", jump_payload)

def _is_jump(previous_pulse_value: int, current_pulse_value: int) -> bool:
    
    change_percent = abs(current_pulse_value - previous_pulse_value) / previous_pulse_value * 100
    return change_percent > JUMP_THRESHOLD_PERCENT

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
        probe_timestamp = message.get("timestamp")
       

        device_id = str(device_id)
        pulse_value = int(pulse_value)
        probe_timestamp = int(probe_timestamp)
        item = get_device_item(table, device_id)

        if item is None:
            store_new_device_item(table, device_id, pulse_value, probe_timestamp)
            logger.debug(
                "Created device item {}",
                {"device_id": device_id, "create_at": probe_timestamp, "pulse": pulse_value},
            )
            continue

        previous_pulse_value = int(item["last_value"])

        if(_is_jump(previous_pulse_value, pulse_value)):
            create_jump_probe(table, device_id, previous_pulse_value, pulse_value, probe_timestamp)

        update_last_pulse_value(table, device_id, pulse_value)
        logger.debug(
            "Updated device item {}",
            {
                "device_id": device_id,
                "last_value": previous_pulse_value,
            },
        )
