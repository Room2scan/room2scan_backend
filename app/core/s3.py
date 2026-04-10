import os
import boto3
from dotenv import load_dotenv

# .env 로드
load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

def upload_to_s3(file, filename):
    s3.upload_fileobj(file, BUCKET_NAME, filename)
    return f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{filename}"

def delete_from_s3(file_url: str):
    key = file_url.split(".com/")[-1]

    s3.delete_object(
        Bucket=BUCKET_NAME,
        Key=key
    )