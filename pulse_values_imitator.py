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
    DURATION_SECONDS,
    INTERVAL_SECONDS,
    DEVICES,
    GROUPS,
    DELTA_PERCENT_RANGES,
    SNS_TOPIC_ARN,
)


sns = boto3.client("sns")


def epoch_seconds() -> int:
    return int(time.time())


def random_chance(probability_percent: int) -> bool:
    """Return True with the given integer percentage chance (0..100)."""
    if not 0 <= probability_percent <= 100:
        raise ValueError("probability_percent must be between 0 and 100")
    return random.randint(1, 100) <= probability_percent

def get_random_delta_percent(percent_ranges_thresholds: tuple[int, int, int, int]) -> int:
    """Return a random delta percent based on the defined ranges and their probabilities."""
    rand_percent = random.randint(1, 100)
    for i, threshold in enumerate(percent_ranges_thresholds):
        if rand_percent <= threshold:
            return random.randint(*DELTA_PERCENT_RANGES[i])
    raise ValueError("Invalid delta_percent_ranges configuration")


def get_random_delta(current_pulse: int, group_info: dict) -> int:
    delta_percent = get_random_delta_percent(group_info["percent_ranges_thresholds"])
    delta = int(current_pulse * delta_percent / 100)
    if not random_chance(group_info["prob_incr"]):
        delta = -delta
    return delta
        
def get_next_pulse_value(current_pulse: int, group_info: dict) -> int:
    delta = 0
    if random_chance(group_info["prob_change"]):
        delta = get_random_delta(current_pulse, group_info)
    new_pulse = current_pulse + delta
    return max(group_info["pulse_min"], min(group_info["pulse_max"], new_pulse))

def get_pulse_value(device_id: str) -> int:
    device_info = DEVICES[device_id]
    group_info = GROUPS[device_info["group"]]
    if not device_info["current_pulse"]:
        # Initial pulse value for the device
        pulse = random.randint(group_info["first_pulse_range"][0], group_info["first_pulse_range"][1])
        device_info["current_pulse"] = pulse
    else:
        pulse = get_next_pulse_value(device_info["current_pulse"], group_info)
        device_info["current_pulse"] = pulse
    return pulse
    
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
def run_imitator(
    duration_seconds: int,
    interval_seconds: float,
    topic_arn: str,
) -> None:
    ids = list(DEVICES.keys())
    start = time.monotonic()
    sent_count = 0

    while True:
        elapsed = time.monotonic() - start
        if elapsed >= duration_seconds:
            break

        for current_device in ids:
            payload = {
                "device_id": current_device,
                "pulse": get_pulse_value(current_device),
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
        duration_seconds=DURATION_SECONDS,
        interval_seconds=INTERVAL_SECONDS,
        topic_arn=SNS_TOPIC_ARN,
    )