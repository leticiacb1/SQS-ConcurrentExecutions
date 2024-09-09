import os
from dotenv import load_dotenv

class Config():

    def __init__(self):
        
        self.ACCESS_KEY = None
        self.SECRET_KEY = None
        self.REGION     = None
        self.ACCOUNT_ID = None
        self.ROLE_ARN   = None

        self.env_filename = '.env'

    def load(self) -> None:
        '''
        Read .env and export variables used in project
        '''

        load_dotenv(os.path.join(os.path.dirname(__file__), self.env_filename))
        
        self.ACCESS_KEY =  os.getenv("AWS_ACCESS_KEY_ID")
        self.SECRET_KEY =  os.getenv("AWS_SECRET_ACCESS_KEY")
        self.REGION     = os.getenv("AWS_REGION")
        self.ACCOUNT_ID = os.getenv("AWS_ACCOUNT_ID")
        self.ROLE_ARN   = os.getenv("AWS_LAMBDA_ROLE_ARN")

        print("\n    [INFO] Environment variables loaded successfully.\n")
        print("\n           > ACCESS_KEY : " + self.ACCESS_KEY)
        print("\n           > SECRET_KEY : " + self.SECRET_KEY)
        print("\n           > REGION : " + self.REGION)
        print("\n           > ACCOUNT_ID : " + self.ACCOUNT_ID)
        print("\n           > ROLE_ARN : " + self.ROLE_ARN + "\n")