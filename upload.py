import boto3
import os

s3 = boto3.client(
   "s3",
   aws_access_key_id=os.getenv("s3_key"),
   aws_secret_access_key=os.getenv("s3_secret")
)
bucket_name = os.getenv("s3_bucket")


def upload_file_to_s3(file_path):
    """
    xoxo
    """
    file_name = file_path.split("/")[-1]

    with open(file_path, "rb") as f:
        s3.upload_fileobj(
            f,
            bucket_name,
            file_name,
            ExtraArgs={
                "ContentType": "jpg/jpeg"
            }
        )
