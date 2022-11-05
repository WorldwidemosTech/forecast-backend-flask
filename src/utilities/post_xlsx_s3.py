import boto3
from dotenv import load_dotenv
import os

load_dotenv('.env')

# TODO: change aws keys to env variables

SECRET_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

client = boto3.client(
    's3',
    aws_access_key_id=SECRET_KEY_ID,
    aws_secret_access_key=SECRET_ACCESS_KEY
)


def post_to_s3(file, user_id, property_id, filename):

    bucket_name="financial-forecast"
    response = client.put_object(Bucket=bucket_name, Key=f"{user_id}/{property_id}/{filename}.xlsx", Body=file)
    
    return response
    