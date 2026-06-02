import json

from logger_config import logger





def lambda_handler(event, context):
    """Event from SNS containing reduced pulse value data.

    The function prints the message from every SNS record in the batch.
    Each SNS message may contain a JSON payload with reduced values.
    """

    records = event.get("Records", [])

    for record in records:
        sns_message = record.get("Sns", {})
        body = sns_message.get("Message", "")

        try:
            message = json.loads(body)
        except json.JSONDecodeError:
            raise ValueError("Received SNS message", body)

        device_id = message.get("device_id")
        min_value = message.get("min_pulse_value")
        median_value = message.get("median_pulse_value")
        max_value = message.get("max_pulse_value")
        timestamp = message.get("timestamp")

        logger.debug(
            "Received reduced values {}",
            {
                "device_id": device_id,
                "min_pulse_value": min_value,
                "median_pulse_value": median_value,
                "max_pulse_value": max_value,
                "timestamp": timestamp,
            },
        )

   
        