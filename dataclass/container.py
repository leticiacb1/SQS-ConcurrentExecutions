import boto3
from config.config import Config

class ContainerRegistry():

    def __init__(self):
        self.ecr_client = None
        self.repository_arn = None
        self.repository_uri = None

        self.config = Config()
        self.config.load()

    def create_client(self) -> None:
        self.ecr_client = boto3.client("ecr",
                                        aws_access_key_id=self.config.ACCESS_KEY,
                                        aws_secret_access_key=self.config.SECRET_KEY,
                                        region_name=self.config.REGION
                                       )
        print("\n    [INFO] Create AWS Elastic Container Registry client. \n")

    def create_repository(self, repository_name: str) -> None:
        response = self.ecr_client.create_repository(repositoryName=repository_name,
                                                     imageScanningConfiguration={"scanOnPush": True},
                                                     imageTagMutability="MUTABLE",
                                                    )
        self.repository_arn = response['repository']['repositoryArn']
        self.repository_uri = response['repository']['repositoryUri']

        print(f"\n    [INFO] Create a ECR repository with name {repository_name}. \n")
        print("\n           > Repository Arn : " + self.repository_arn)
        print("\n           > Repository Uri : " + self.repository_uri)

    def cleanup(self, repository_name: str) -> None:
        if(self.ecr_client):
            print(f"\n    [INFO] Deleting all images in repository {repository_name}. \n")
            image_ids = self.ecr_client.list_images(repositoryName=repository_name)['imageIds']
            if(len(image_ids) > 0):
                self.ecr_client.batch_delete_image(
                    repositoryName=repository_name,
                    imageIds=image_ids
                )

            print(f"\n    [INFO] Delete repository {repository_name}. \n")
            self.ecr_client.delete_repository(repositoryName=repository_name)
        else:
            print(f"\n    [INFO] No repository {repository_name} to delete. \n")