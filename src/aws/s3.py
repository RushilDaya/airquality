import boto3
from src.config import AWS_PROFILE

def upload_file_to_s3(
        bucket: str,
        file_contents :str,
        file_name: str,
):
    boto3_session = boto3.Session(profile_name=AWS_PROFILE)
    s3 = boto3_session.resource('s3')
    response = s3.Bucket(bucket).put_object(Key=file_name, Body=file_contents, ContentType='text/html')
    return response
    
    