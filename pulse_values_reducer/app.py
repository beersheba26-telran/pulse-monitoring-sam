import json



def lambda_handler(event, context):
    """event from SQS FIFO contaning pulse probe data
    It just prints out the received message body from SQS FIFO queue
    """
    print("Received message ", event['Records'][0]['body'])

   
        