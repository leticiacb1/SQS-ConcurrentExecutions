import boto3
import os

def lambda_handler(event, context):
    # Create an SQS client
    sqs = boto3.client("sqs")

    # Define the queue URL
    queue_url = os.environ.get("DESTINATION_SQS_URL")

    # Define the message to send
    message_body = "I can send messages to SQS!"

    # Send message to the queue
    response = sqs.send_message(QueueUrl=queue_url, MessageBody=message_body)
    return response