import boto3
import os

s3 = boto3.client(
   "s3",
   aws_access_key_id=os.getenv("s3_access_key_id"),
   aws_secret_access_key=os.getenv("s3_secret_access_key")
)
bucket_name = os.getenv("s3_bucket_name")
upload_folder = os.getenv('s3_upload_folder')


def upload_file_to_s3(file_path):
    """
    Uploads a file into S3 bucket
    """
    file_name = file_path.split("/")[-1]
    s3_file_key = f"{upload_folder}{file_name}"

    with open(file_path, "rb") as f:
        s3.upload_fileobj(
            f,
            bucket_name,
            s3_file_key
        )


def list_s3_files():
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=upload_folder)

    files = map(lambda x: x["Key"], response["Contents"])

    return(list(files))
