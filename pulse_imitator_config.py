"""Configuration for the simple pulse values imitator."""

SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:246814138873:pulse-events.fifo"
DEVICE_COUNT = 5
DURATION_SECONDS = 5 * 60
INTERVAL_SECONDS = 1.0
PULSE_MIN = 60
PULSE_MAX = 200