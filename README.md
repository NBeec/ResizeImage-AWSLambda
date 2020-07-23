# Resizing Images with AWS Lambda, Based on S3 Events.
This is some sample code that is used to resized images that are uploaded to an S3 Bucket. This is the source code that is used in the YouTube video [**Here!**](https://youtu.be/lZyg0hdKXio). The video walks you through what Serverless code is, What AWS Lambda is, and A full breakdown of how to get it working.

---

This code sample is based on the AWS code that you can find in their Documentation. [Here!](https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example-deployment-pkg.html). You will have to compile this code into a v-env zip file for it to be used with AWS Lambda, this can also be found on their documentation.

---

**This code uses the verify=False flag with the Boto3.client, this is not optimal/secure and should not be used in production**
