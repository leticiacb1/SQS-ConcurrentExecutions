import boto3
from config.config import Config

class SQS():

    def __init__(self):
        self.sqs_client = None
        self.queue_url = None

        self.visibility_timeout = 60    # Timeout in seconds before the message becomes visible again
        self.wait_time_seconds = 20     # Wait up to 20 seconds for a message to be available


        self.config = Config()
        self.config.load()

    def create_client(self) -> None:        
        self.sqs_client = boto3.client( "sqs",
                                    aws_access_key_id= self.config.ACCESS_KEY,
                                    aws_secret_access_key=self.config.SECRET_KEY,
                                    region_name=self.config.REGION,
                                )
                        
        print("\n    [INFO] Create a Amazon Simple Queue Service (SQS) client. \n")

    def create_queue(self, queue_name: str, delay_seconds: str = "0", menssage_rentention_period: str = "3600") -> None:
        response = self.sqs_client.create_queue( QueueName=queue_name,
                                                 Attributes={
                                                    "DelaySeconds": delay_seconds,
                                                    "MessageRetentionPeriod": menssage_rentention_period, # seconds
                                                 },
                                                )

        # Get the queue URL
        self.queue_url = response["QueueUrl"]
        print("\n    [INFO] SQS queue created with URL" + self.queue_url)

    def check_queue(self) -> None:  

        # Get the attributes of the SQS queue
        response = self.sqs_client.get_queue_attributes(QueueUrl=self.queue_url, AttributeNames=["All"])

        # Extract the desired attributes from the response
        attributes = response["Attributes"]
        approximate_message_count = attributes["ApproximateNumberOfMessages"]
        approximate_message_not_visible_count = attributes["ApproximateNumberOfMessagesNotVisible"]

        print("\n    [INFO] Approximate number of visible messages:" + approximate_message_count)
        print("\n    [INFO] Approximate number of messages not visible:" + approximate_message_not_visible_count)

    def send_message(self, message: str) -> None:
        # Send a message to the SQS queue
        response = self.sqs_client.send_message(
            QueueUrl=self.queue_url, 
            MessageBody=message,
        )

        # Get the message ID from the response
        message_id = response["MessageId"]
        print("\n    [INFO] Message sent with ID:" + message_id)

    def read_messages(self, num_messages :int = 1) -> None:

        print("\n    [INFO] Reading all messages ...")

        # Receive messages from the SQS queue
        response = self.sqs_client.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=num_messages,
            VisibilityTimeout=self.visibility_timeout,  
            WaitTimeSeconds=self.wait_time_seconds,
        )

        # Process received messages
        messages = response.get("Messages", [])
        for message in messages:
            message_text = message["Body"]

            # Print the message
            print(f"\n           > Received message: {message_text}")

            # Delete the processed message from the SQS queue
            self.sqs_client.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=message["ReceiptHandle"],
            )

    def cleanup(self) -> None:
        if(self.sqs_client):
            print(f"\n    [INFO] Delete queue with URL = {self.queue_url}. \n")
            self.sqs_client.delete_queue(QueueUrl=self.queue_url)
        else:
            print(f"\n    [INFO] No queue with URL = {self.queue_url} to delete. \n")