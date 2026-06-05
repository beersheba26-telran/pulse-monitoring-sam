import json
import os
import time

import boto3
from botocore.exceptions import ClientError

from logger_config import logger


MAX_INVOKE_RETRIES = 3
THROTTLING_ERROR_CODES = {"TooManyRequestsException", "ThrottlingException"}
LAMBDA_CLIENT = boto3.client("lambda")
SNS_CLIENT = boto3.client("sns")
STALE_TIME_SECONDS = int(os.environ.get("STALE_TIME_SECONDS", 3600))
device_data_cache = {
    # device_id: {"data": dict, "timestamp": int}
}
def _publish_abnormal_pulse_event(device_id: str, median_pulse_value: int, timestamp: int, normal_range_center: int, deviation_percent_threshold: int) -> None:
    event_payload = {
        "device_id": device_id,
        "median_pulse_value": median_pulse_value,
        "timestamp": timestamp,
        "normal_range_center": normal_range_center,
        "deviation_percent_threshold": deviation_percent_threshold,
    }
    SNS_CLIENT.publish(
        TopicArn=os.environ["ABNORMAL_PULSE_TOPIC_ARN"],
        Message=json.dumps(event_payload),
    )
    logger.debug(f"Published abnormal pulse event {event_payload}" )
def _is_abnormal_pulse(median_pulse_value: int, normal_range_center:int, deviation_percent_threshold:int) -> bool:
    deviation_percent = abs(median_pulse_value - normal_range_center) / normal_range_center * 100
    return deviation_percent > deviation_percent_threshold
def _invoke_data_provider(device_id: str) -> dict:
    """Invoke the data provider Lambda function with the given device_id and return its response."""
    for attempt in range(1, MAX_INVOKE_RETRIES + 1):
        try:
            response = LAMBDA_CLIENT.invoke(
                FunctionName=os.environ["DATA_PROVIDER_FUNCTION_NAME"],
                InvocationType="RequestResponse",
                Payload=json.dumps({"device_id": device_id}),
            )
            payload = response["Payload"].read()
            return json.loads(payload)
        except ClientError as error:
            error_code = error.response.get("Error", {}).get("Code")
            if error_code not in THROTTLING_ERROR_CODES or attempt == MAX_INVOKE_RETRIES:
                raise

            backoff_seconds = attempt
            logger.warning(
                f"Lambda invoke throttled for device_id={device_id} on attempt {attempt}/{MAX_INVOKE_RETRIES}; retrying in {backoff_seconds}s"
            )
            time.sleep(backoff_seconds)

def _get_device_data(device_id: str) -> dict:
    """cache functionality
       if the device data was fetched less than STALE_TIME_SECONDS 
         ago, return cached data, otherwise invoke data provider Lambda to get fresh data
    """
    if device_id in device_data_cache and time.time() - device_data_cache[device_id]["timestamp"] < STALE_TIME_SECONDS:
        
        logger.debug(f"Using cached data for device_id={device_id}")
        response =  device_data_cache[device_id]["data"]
    else:
        response = _invoke_data_provider(device_id)
        device_data_cache[device_id] = {"data": response, "timestamp": time.time()}
        logger.debug(f"Fetched fresh data for device_id={device_id} and updated cache")
    return response

def _process_record(body: str) -> None:
    """Process a single SNS message body containing reduced pulse data."""
    bodyDict = json.loads(body)
    device_id = bodyDict["device_id"]
    median_pulse_value = bodyDict["median_pulse_value"]
    timestamp = bodyDict["timestamp"]
    logger.debug(
        f"Processing reduced pulse data {bodyDict}",
    )
    try:
        provider_response = _get_device_data(device_id)
    except ClientError as error:
        error_code = error.response.get("Error", {}).get("Code")
        logger.error(
            f"Failed to invoke data provider for device_id={device_id} with error code {error_code}"
        )
        raise

    logger.debug(f"Received data provider response {provider_response}")
    normal_range_center = (provider_response["min_value"] + provider_response["max_value"]) // 2
    deviation_percent_threshold = provider_response["deviation_percent_threshold"]
    if _is_abnormal_pulse(median_pulse_value, normal_range_center, deviation_percent_threshold):
        logger.debug(f"Abnormal pulse detected for device_id={device_id}")
        _publish_abnormal_pulse_event(device_id, median_pulse_value, timestamp, normal_range_center, deviation_percent_threshold) 
def lambda_handler(event, _):
    """receive event from SNS containing reduced pulse data of following format:
    {
        "device_id": "string",
        "median_pulse_value": int,
        
    }
    directly invoke data provider Lamda passing device_id
    invoked function returns approate to the device_id data of following fomat
    {min_value:int, max_value:int, deviation_percent_threshold:int}
    where deviation_percent_threshold means the percentage of deviation medium value
    from( min_value + max_value)//2 that is considered as abnormal pulse value
    """
    records = event.get("Records", [])
    for record in records:
        sns_message = record.get("Sns", {})
        body = sns_message.get("Message", "")
        logger.debug("Received SNS message {}", body)
        _process_record(body)
        
        
        