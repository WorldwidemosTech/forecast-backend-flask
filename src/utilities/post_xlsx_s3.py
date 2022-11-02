import json
import pymongo
import boto3
from dotenv import load_dotenv

load_dotenv('.env')



client = boto3.client(
    's3',
    aws_access_key_id='AKIAR4KXHPRAGZI7Z3UJ',
    aws_secret_access_key="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"
)


def post_to_s3(document_object):

    bucket_name="financial-forecast"

    client.put_object(Bucket=bucket_name, Key="diego/zoi-residencial/")

    response = client.upload_file("forecast.xlsx", bucket_name, document_object)
    
    return response
    