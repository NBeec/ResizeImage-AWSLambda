# Needed for s3 commands.
import boto3

import os
import sys
import uuid
from urllib.parse import unquote_plus

# Used for resize_image.
from PIL import Image
import PIL.Image

print("Lambda S3 Function Start.")

# Define Image Size and s3 Client.
size = 256, 256
s3 = boto3.client('s3', verify=False)

# Resize and Save image.
def resize_image(imagePath, resizedPath):
    print("Resize Function called.")
    # Open Image from ImagePath.
    with Image.open(imagePath) as image:
        # Resize and Save image to resizedPath.
        image.thumbnail(size)
        image.save(resizedPath)

def lambda_handler(event, context):
    print("Lambda handler called.")
    # Iterate of event Data from S3 bucket.
    for record in event['Records']:
        # Read S3 Bucket name and Key(file name) from Record.
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        print("Loop started for {} in Bucket {}".format(key, bucket))
        
        # Remove '/' from key(file name) then assign path variables for internal lambda environment.
        tempkey = key.replace('/', '')
        downloadPath = '/tmp/{}{}'.format(uuid.uuid4(), tempkey)
        uploadPath = '/tmp/resized-{}'.format(tempkey)

        # Download file from Bucket into downloadPath, resize file, then Upload file to bucket from uploadPath.
        s3.download_file(bucket, key, downloadPath)
        resize_image(downloadPath, uploadPath)
        print("Resizing {}".format(key))
        s3.upload_file(uploadPath, os.environ['UploadBucket'], "Resized-256x256-" + key)
    
    print("Image(s) Resize Complete.")
