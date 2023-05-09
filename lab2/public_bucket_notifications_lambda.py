import boto3
from botocore.exceptions import ClientError
import json
import os

def policy_notifier(bucket_name, s3, annotation):
    try:
        sns = boto3.client(''sns'')
        subject = "Potential compliance violation in the bucket: " + bucket_name
        message = "Potential compliance violation in the bucket: " + bucket_name + ", reason: " + annotation
        response = sns.publish(
            TopicArn = os.environ[''TOPIC_ARN''],
            Subject = subject,
            Message = message
        )
    except ClientError as e:
        print("No bucket policy found; no alert sent.")
def lambda_handler(event, context):
    s3 = boto3.client(''s3'')
    evaluations = event[''detail''][''requestParameters''][''evaluations'']
    for el in evaluations:
        if el.get("annotation"):
             annotation = el["annotation"]
             bucket_name = el["complianceResourceId"]
             policy_notifier(bucket_name, s3, annotation)
    return 0  # done