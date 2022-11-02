import boto3
from dotenv import load_dotenv

load_dotenv('.env')



client = boto3.client(
    's3',
    aws_access_key_id='AKIAR4KXHPRAGZI7Z3UJ',
    aws_secret_access_key="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"
)


def post_to_s3(user, property, document_object, name):

    bucket_name="financial-forecast"
    response = client.upload_file(name, bucket_name, f"{user}/{property}/{document_object}")

    return response
    