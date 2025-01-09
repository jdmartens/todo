from pydantic_settings import BaseSettings

class AWSConfig(BaseSettings):
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str = "us-east-2"

    class Config:
        env_file = ".env"

aws_config = AWSConfig()