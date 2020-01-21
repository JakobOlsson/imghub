from os import getenv
import redis

SESSION_KEY = getenv('SESSION_KEY')
SESSION_TYPE = getenv('SESSION_TYPE')
SESSION_REDIS = redis.from_url(getenv('SESSION_REDIS'))

# S3BUCKET
AWS_ACCESS_KEY_ID = getenv('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = getenv('AWS_SECRET_ACCESS_KEY', '')
# for aws this is https://s3.<region>.amazonaws.com/
# or https://s3.amazonaws.com/
S3_API_ENDPOINT = getenv('S3_API_ENDPOINT', 'http://localhost:9000')

# Name of the bucket
S3_BUCKET_NAME = getenv('S3_BUCKET', 'images')
# Prefix (folder) in the Bucket
S3_PREFIX = getenv("S3_PREFIX", 'images')
# Full url for the bucket, custom dns name if for instance,
# fronted by CloudFront.
# Remember to include https or http if it is secure or not
S3_FULL_URL = f'{S3_API_ENDPOINT}/{S3_BUCKET_NAME}' if getenv('S3_FULL_URL', "") == "" else getenv('S3_FULL_URL')
