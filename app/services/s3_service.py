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

def list_files(offset: int = 0, limit: int = 12, object_keys: list = None) -> dict:
    """
    Retrieve a specific range of image files from the S3 bucket.

    :param offset: The starting index of files to retrieve.
    :param limit: The maximum number of files to return.
    :param object_keys: The set of file keys to retrieve. If None, retrieves all files.

    :returns: A dictionary containing 'files' (list of file paths).
    """
    all_files = []
    count_obj = 0

    try:
        if object_keys is not None:
            if not object_keys:
                return {"files": [], "total": 0}
            # Check and collect only the existing files from the provided keys
            for key in object_keys:
                try:
                    s3_client.head_object(Bucket=YANDEX_BUCKET_NAME, Key=key)
                    if key.endswith(tuple(VALID_EXTENSIONS)):
                        all_files.append(key)
                        count_obj += 1
                except s3_client.exceptions.ClientError as e:
                    if e.response['Error']['Code'] == '404':
                        print(f"File not found: {key}")
                    else:
                        raise
        else:
            # Fetch all files from the bucket if no specific keys are provided
            paginator = s3_client.get_paginator('list_objects_v2')

            for page in paginator.paginate(Bucket=YANDEX_BUCKET_NAME):
                if 'Contents' in page:
                    for obj in page['Contents']:
                        key = obj['Key']
                        if key.endswith(tuple(VALID_EXTENSIONS)):
                            all_files.append(key)
                            count_obj += 1

        # Sort files by int values in names (assumes the name format supports this)
        sorted_files = sorted(all_files, key=lambda x: int(x.split('.')[0]))

        # Return files only from the specified range
        return {
            "files": sorted_files[offset:offset + limit],
            "total": count_obj
        }
    except Exception as e:
        print(f"Error listing files: {e}")
        return {"files": [], "total": 0}

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
