import json

from logger_config import logger






def lambda_handler(event, context):
    """Event from SNS containing jumps pulse value data.

    The function prints the message from every SNS record in the batch.
    Each SNS message may contain a JSON payload with jumps values.
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
        previous_pulse_value = message.get("previous_pulse_value")
        current_pulse_value = message.get("current_pulse_value")
        timestamp = message.get("timestamp")

        logger.debug(
            "Received reduced values {}",
            {
                "device_id": device_id,
                "previous_pulse_value": previous_pulse_value,
                "current_pulse_value": current_pulse_value,
                "timestamp": timestamp,
            },
        )

   
        