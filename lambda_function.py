from PIL import Image
from uuid import uuid4
from urllib.parse import unquote_plus
import os 
import sys
import boto3

# Define Image Size and s3 Client.
size = 256, 256
s3 = boto3.client('s3')

# Resize and Save image.
def resize_image(imagePath, resizedPath):
    # Open Image from ImagePath.
    with Image.open(imagePath) as image:
        # Resize and Save image to resizedPath.
        image.thumbnail(size)
        image.save(resizedPath)

def lambda_handler(event, context):
    # Iterate of event Data from S3 bucket.
    for record in event['Records']:
        # Read S3 Bucket name and Key(file name) from Record.
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])

        # Remove '/' from key(file name) then assign path variables for internal lambda environment.
        tempkey = key.replace('/', '')
        downloadPath = '/tmp/{}{}'.format(uuid4, tempkey)
        uploadPath = '/tmp/resized-256x256-{}'.format(tempkey)

        # Download file from Bucket into downloadPath, resize file, then Upload file to bucket from uploadPath.
        s3.download_file(bucket, key, downloadPath)
        resize_image(downloadPath, uploadPath)
        print("Resizing {}".format(key))
        s3.upload_file(uploadPath, '{}-resized'.format(bucket), key)
    
    print("Image(s) Resize Complete.")