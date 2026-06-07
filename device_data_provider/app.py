import os
import json

import boto3
from botocore.exceptions import ClientError
import psycopg
from logger_config import logger
def get_secret():
    secret_name = os.environ["DB_CREDENTIALS_SECRET_ARN"]
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    return secret


def _resolve_db_credentials() -> tuple[str, str]:
    secret_value = get_secret()
    try:
        secret_obj = json.loads(secret_value)
        logger.debug(f"the keys of the secret object are {list(secret_obj.keys())}")
        URI = secret_obj.get("URI")
        logger.debug(f"the URI value from the secret is {URI[:30]}...")  # log only the beginning of the URI for security reasons
       
    except json.JSONDecodeError:
        logger.debug("Secret value is not a JSON object, using default user and secret value as password.")
        pass

    return URI


URI= _resolve_db_credentials()

def lambda_handler(event, context):
    """even of direct invocation with device_id value
    it returns payload
    {
        min_value: int,
        max_value: int,
        deviation_percent_threshold: int
    }
    """
    device_id = event["device_id"]
    query = """
        SELECT
            g.min_value,
            g.max_value,
            g.deviation_percent_threshold
        FROM devices d
        JOIN patients p ON p.id = d.patient_id
        JOIN groups g ON g.id = p.grop_id
        WHERE d.id = %s
    """

    with psycopg.connect(URI) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (device_id,))
            row = cursor.fetchone()

    if row is None:
        raise ValueError(f"No configuration found for device_id={device_id}")

    min_value, max_value, deviation_percent_threshold = row
    logger.debug(f"Queried configuration for device_id={device_id}: min_value={min_value}, max_value={max_value}, deviation_percent_threshold={deviation_percent_threshold}")
    return {
        "min_value": int(min_value),
        "max_value": int(max_value),
        "deviation_percent_threshold": int(deviation_percent_threshold),
    }
    