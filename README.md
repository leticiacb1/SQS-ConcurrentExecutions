### 🆚️ SQS - Concurrent Executions in Lambda Function

AWS Lambda imposes several quotas that can impact the design and deployment of your functions:

One of these quotas is the _Concurrency Limits_

* **Concurrency Limits:**

By default, there is a limit on the number of concurrent executions of Lambda functions, typically set to 1,000 concurrent executions per region, though this can be increased by request.

> It is the responsibility of the client or the invoker of the Lambda function to handle rate limiting and retries

To handle rate limiting and retries effectively, you can implement error handling and retry mechanisms in your application code.

Another option is to use **queues**, such as **Amazon Simple Queue Service (SQS)**.

This project create a lambda function that is activated whenever new messages arrive in a queue.The lambda function will receive a batch of messages and, after processing them, will send them to a new queue.

```bash
     _____________________            _____________           ___________________________
    |                     |          |             |         |                           |
    |  Origin SQS Queue   |   ---->  |    Lambda   |  ---->  |  Destinantion SQS Queue   |
    |_____________________|          |_____________|         |___________________________|

```

#### 📌 Run the project

* **Dependencies** 

Install **AWS CLI**, [click here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

```bash
# Configure credentials
$ aws configure --profile mlops
AWS Access Key ID [None]: ????????????
AWS Secret Access Key [None]: ????????????????????????????????
Default region name [None]: us-east-2
Default output format [None]:

# Set profile in each terminal you will use
$ export AWS_PROFILE=mlops

# List the names of lambda functions associated with your account:
$ aws lambda list-functions --query "Functions[*].FunctionName" --output text
```
<br>

Create a `venv` and install dependencies:

```bash
    # Create environment
    python3 -m venv venv  

    # Activate environment
    source venv/bin/activate

    # Install dependencies
    pip install -r requirements.txt
``` 

Create a `.env` file inside `config/` folder with user and password of RabbitMQ:

```bash
    # .env content'
    AWS_ACCESS_KEY_ID="XXXXXXXXXXXXXX"
    AWS_SECRET_ACCESS_KEY="aaaaaaaaaaaaaaaaaaaaaaaaaaa"
    AWS_REGION="xx-xxxx-2"
    AWS_LAMBDA_ROLE_ARN="arn:xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
``` 

* **Run the project** 

Run the file `limit_executions_example.py` to see the concurrent execution of the lambda function, and how it works when the limit of calls exceeds the configured limit for the lambda function.

```bash
   # Lambda function on file lambda_proc.py
    python3 limit_executions_example.py
```

> **Handle Rate Limiting**
> In file `limit_executions_example.py` change the  `num_executions` variable value for a number greater than the `concurrent_executions_limit` and see what happens when the limit of executions is reached.


Run the file sqs_example to see a example of **Amazon Simple Queue Service (SQS)** in action:

```bash
    python3 one_sqs_example.py
```

To see how lambda and sqs interact to build a sistem to handle rate limiting and retries, run :

```bash
    # Lambda function on file lambda_send_sqs.py
    python3 main.py
```

<br>
@2024, Insper. 9° Semester,  Computer Engineering.
<br>

_Machine Learning Ops & Interviews Discipline_