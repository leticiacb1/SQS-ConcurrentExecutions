from dataclass.compress import CompressFile
from dataclass.lambda_function import LambdaFunction
from dataclass.queue import SQS

import concurrent.futures
import boto3
import time
import io

def multiple_simultaneous_calls(num_executions: int, function_name: str, lambda_client: boto3.client) -> None:
    try:
        print(f"\n    [INFO] Call lambda function {function_name}() {num_executions} times.\n")
        # Create a thread pool executor with the desired number of threads
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_executions) as executor:
            # List to store the future objects
            futures = []

            # Submit the Lambda invocations to the executor
            for _ in range(num_executions):
                future = executor.submit(
                    lambda_client.invoke,
                    FunctionName=function_name,
                    InvocationType="RequestResponse",
                )
                futures.append(future)

            # Process the results as they become available
            for future in concurrent.futures.as_completed(futures):
                print("-" * 40)
                response = future.result()
                payload = response["Payload"]
                txt = io.BytesIO(payload.read()).read().decode("utf-8")
                print(f"\n           > Response:\n{txt}\n")

    except Exception as e:
        print(f"\n    [ERROR] An error occurred in multiple_simultaneous_calls(): \n {e}")


if __name__ == "__main__":
    # Variaveis
    username = "leticiacb1"     

    message = "I love Python"
    queue_name = "message_queue_" + username
    
    try: 
        # Instances
        sqs = SQS()

        # Create Queue for handle messages
        sqs.create_client()
        sqs.create_queue(queue_name= queue_name)
        sqs.check_queue()
        sqs.send_message(message=message)
        sqs.read_messages()

    except Exception as e:
        print(f"\n    [ERROR] An error occurred: \n {e}")
    finally:
        # Cleaning:
        sqs.cleanup()