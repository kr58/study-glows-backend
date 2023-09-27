from django.conf import settings
import boto3


def upload_to_s3(file, folder=""):
    bucket = settings.AWS_STORAGE_BUCKET_NAME
    key = 'media/' + folder + "+".join([f.strip() for f in file.name.split(" ")])
    session = boto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    s3 = session.client('s3')
    try:
        s3.put_object(Bucket=bucket, Key=key, Body=file.read(), Metadata={'Content-Type': file.content_type})
        url = f'https://{bucket}.s3.amazonaws.com/{key}'
        return url
    except Exception as e:
        print(e)
        return e