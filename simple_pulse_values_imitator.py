"""Simple pulse values imitator.

Generates pulse probe payloads and publishes them directly to SNS FIFO.

Defaults follow README requirements:
- 5 devices
- random pulse value in [60, 200]
- duration 5 minutes
- every second, each device sends one probe
"""

from __future__ import annotations

import json
import random
import time
from typing import Iterable
from logger_config import logger    
import boto3

from pulse_imitator_config import (
    DEVICE_COUNT,
    DURATION_SECONDS,
    INTERVAL_SECONDS,
    PULSE_MAX,
    PULSE_MIN,
    SNS_TOPIC_ARN,
)


sns = boto3.client("sns")


def epoch_seconds() -> int:
    return int(time.time())


def publish_probe(topic_arn: str, payload: dict, device_id: str) -> str:
    publish_kwargs = {
        "TopicArn": topic_arn,
        "Message": json.dumps(payload),
    }

    if topic_arn.endswith(".fifo"):
        publish_kwargs["MessageGroupId"] = device_id
        publish_kwargs["MessageDeduplicationId"] = f"{device_id}:{payload['timestamp']}:{payload['pulse']}"

    response = sns.publish(**publish_kwargs)
    return response["MessageId"]


def device_ids(count: int) -> Iterable[str]:
    for index in range(1, count + 1):
        yield f"device-{index}"


def run_imitator(
    device_count: int,
    duration_seconds: int,
    interval_seconds: float,
    pulse_min: int,
    pulse_max: int,
    topic_arn: str,
) -> None:
    ids = list(device_ids(device_count))
    start = time.monotonic()
    sent_count = 0

    while True:
        elapsed = time.monotonic() - start
        if elapsed >= duration_seconds:
            break

        for current_device in ids:
            payload = {
                "device_id": current_device,
                "pulse": random.randint(pulse_min, pulse_max),
                "timestamp": epoch_seconds(),
            }
            message_id = publish_probe(topic_arn, payload, current_device)
            sent_count += 1

            logger.debug(
                f"[{payload['timestamp']}] sent={sent_count} "
                f"device={payload['device_id']} pulse={payload['pulse']} "
                f"message_id={message_id}"
            )

        time.sleep(interval_seconds)

    print(
        f"Finished. total_sent={sent_count} "
        f"duration_seconds={duration_seconds}"
    )


if __name__ == "__main__":
    run_imitator(
        device_count=DEVICE_COUNT,
        duration_seconds=DURATION_SECONDS,
        interval_seconds=INTERVAL_SECONDS,
        pulse_min=PULSE_MIN,
        pulse_max=PULSE_MAX,
        topic_arn=SNS_TOPIC_ARN,
    )