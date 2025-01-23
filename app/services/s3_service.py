import boto3
from botocore.exceptions import NoCredentialsError
import os

YANDEX_BUCKET_NAME = os.getenv('YANDEX_BUCKET_NAME')
YANDEX_ENDPOINT = os.getenv('YANDEX_ENDPOINT')
VALID_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('YANDEX_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('YANDEX_SECRET_KEY'),
    endpoint_url=YANDEX_ENDPOINT
)

def count_obj(bucket: str=YANDEX_BUCKET_NAME, extensions: set=VALID_EXTENSIONS) -> int:
    """
    Count the number of objects in an S3 bucket folder with the specified file extensions.

    :param bucket: The name of the S3 bucket.
    :param extensions: A set of file extensions to filter the files by.

    :returns: The number of objects in the specified bucket that match the extensions.
    """
    count = 0
    paginator = s3_client.get_paginator('list_objects_v2')
    
    # Iterate through paginated results from the bucket
    for page in paginator.paginate(Bucket=bucket):
        if 'Contents' in page:
            # Check each file's extension
            for obj in page['Contents']:
                key = obj['Key']
                if any(key.endswith(ext) for ext in extensions):
                    count += 1
    return count

def list_files(offset: int = 0, limit: int = 12) -> dict:
    """
    Retrieve a specific range of image files from the S3 bucket.

    :param offset: The starting index of files to retrieve.
    :param limit: The maximum number of files to return.

    :returns: A dictionary containing 'files' (list of file paths).
    """
    try:
        # Set a full list of files
        paginator = s3_client.get_paginator('list_objects_v2')
        all_files = []

        for page in paginator.paginate(Bucket=YANDEX_BUCKET_NAME):
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    if key.endswith(tuple(VALID_EXTENSIONS)):
                        all_files.append(key)

        # Sort files by int values in names
        sorted_files = sorted(all_files, key=lambda x: int(x.split('.')[0]))

        # Return files only from the specified range
        return {
            "files": sorted_files[offset:offset + limit],
        }
    except Exception as e:
        print(f"Error listing files: {e}")
        return {"files": []}

def download_file(file_key: str) -> bytes:
    """
    Download an image file from the S3 bucket.

    :param file_key: The key (path) of the file to download in the S3 bucket.

    :returns: The content of the file as bytes, or None if an error occurred.
    """
    try:
        file_obj = s3_client.get_object(Bucket=YANDEX_BUCKET_NAME, Key=file_key)
        return file_obj['Body'].read()
    except Exception as e:
        # Handle exceptions during file download
        print(f"Error downloading file: {e}")
        return None
