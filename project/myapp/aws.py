import boto3

def upload_to_s3(file_path, bucket_name):
    s3 = boto3.client('s3')
    with open(file_path, 'rb') as f:
        s3.upload_fileobj(f, bucket_name, file_path.split('/')[-1])