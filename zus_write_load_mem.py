import boto3
import pickle
from io import BytesIO

with open('AWS_S3_KEY.txt') as f:
    s3_key = f.read().strip()

key1 = s3_key.splitlines()[0]
key2 = s3_key.splitlines()[1]

# Configure Boto3 with AWS credentials
aws_region = 'ap-southeast-1'
s3 = boto3.client('s3',
                  aws_access_key_id=key1,
                  aws_secret_access_key=key2,
                  region_name=aws_region)

# Specify the S3 bucket and file name
bucket_name = 'zusbot-memory-storage'


def write_memory(memory, file_name):
    # Convert the variable to bytes using pickle and BytesIO
    file_bytes = BytesIO()
    pickle.dump(memory, file_bytes)
    file_bytes.seek(0)
    # Upload the file to Amazon S3
    s3.upload_fileobj(file_bytes, bucket_name, file_name)


def load_memory(file_name):
    try:
        # Download the file from Amazon S3
        response = s3.get_object(Bucket=bucket_name, Key=file_name)
        data = response['Body'].read()

        # Load the variable from the downloaded data
        memory = pickle.loads(data)
        return memory

    except Exception as e:
        print("Error: ", str(e))