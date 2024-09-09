import boto3
import random
import string

from config.config import Config

class Gateway():
    
    def __init__(self):
        self.lambda_target = None
        self.lambda_function = None
        self.api_gateway = None
        self.api_gateway_create = None
        self.endpoint = None

        self.id_num = "".join(random.choices(string.digits, k=7))

        self.protocol_type = "HTTP"
        self.version = "1.0"

        # Load environment variables
        self.config = Config()
        self.config.load()

    def create_client(self) -> None:
        self.api_gateway = boto3.client( "apigatewayv2",
                                         aws_access_key_id=self.config.ACCESS_KEY,
                                         aws_secret_access_key=self.config.SECRET_KEY,
                                         region_name=self.config.REGION
                                       )
        print("\n    [INFO] Create AWS API Gateway client. \n")

    def get_lambda_function(self, function_name: str) -> None:
        
        lambda_client = boto3.client( "lambda",
                                      aws_access_key_id=self.config.ACCESS_KEY,
                                      aws_secret_access_key=self.config.SECRET_KEY,
                                      region_name=self.config.REGION
                                    )

        self.lambda_function= lambda_client.get_function(FunctionName=function_name)
        self.lambda_target= self.lambda_function["Configuration"]["FunctionArn"]

        print("\n    [INFO] Get lambda function. \n")
        print(self.lambda_function)

    def create_api(self, api_name : str) -> None:
        print(f"\n    [INFO] Create API with name {api_name} \n")
        self.api_gateway_create = self.api_gateway.create_api( Name=api_name,
                                                          ProtocolType=self.protocol_type,
                                                          Version=self.version,
                                                          RouteKey="ANY /", # This will create an API with a single route for all methods
                                                          Target=self.lambda_target,
        )
        self.endpoint = self.api_gateway_create["ApiEndpoint"]

        print(f'\n    [INFO] Check API Endpoint : {self.endpoint} \n')

    def set_permissions(self, function_name: str) -> None:
        print(f"\n    [INFO] Set lambda function permissions for API.\n")
        lambda_client = boto3.client( "lambda",
                                      aws_access_key_id=self.config.ACCESS_KEY,
                                      aws_secret_access_key=self.config.SECRET_KEY,
                                      region_name=self.config.REGION
                                    )
        
        api_gateway_permissions = lambda_client.add_permission( FunctionName=function_name,
                                                                       StatementId="api-gateway-permission-statement-" + self.id_num,
                                                                       Action="lambda:InvokeFunction",
                                                                       Principal="apigateway.amazonaws.com",
                                                                     )
        
    def create_route(self, HTTP_method: str, route_key: str ) -> None:
        print(f"\n    [INFO] Create a route for API \n")
        print("\n           > HTTP method : " + HTTP_method)
        print("\n           > Route : " + route_key)
        
        # Create an integration between the API Gateway and the Lambda function
        integration_response = self.api_gateway.create_integration(
            ApiId=self.api_gateway_create["ApiId"],
            IntegrationType="AWS_PROXY",
            IntegrationMethod= HTTP_method, 
            IntegrationUri=self.lambda_target,
            PayloadFormatVersion="2.0",
        )

        # Create a route for the POST method
        route_response = self.api_gateway.create_route(
            ApiId=self.api_gateway_create["ApiId"],
            RouteKey= route_key,  
            Target=f"integrations/{integration_response['IntegrationId']}",
        )


    def see_all_gateways(self):
        response = self.api_gateway.get_apis(MaxResults="2000")

        print(f"\n    [INFO] See all apis associated to the account id \n")
        print(f"\n           > APIs : \n")
        for api in response["Items"]:
            print(f"             - {api['Name']} ({api['ApiEndpoint']})")
    
    def cleanup(self, api_name: str) -> None:

        if(self.api_gateway):
            response = self.api_gateway.get_apis(MaxResults="2000")
            api_gateway_id = None

            for item in response["Items"]:
                if item["Name"] == api_name:
                    api_gateway_id = item["ApiId"]
                    break

            # Delete the API Gateway
            if api_gateway_id:
                self.api_gateway.delete_api(ApiId=api_gateway_id)
                print(f"\n    [INFO] API Gateway '{api_name}' deleted successfully. \n")
            else:
                print(f"\n    [INFO] API Gateway '{api_name}' not found. \n")
        else:
            print(f"\n    [INFO] No gateway to delete. \n")