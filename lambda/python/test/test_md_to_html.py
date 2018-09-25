import boto3
from md_to_html import lambda_handler

s3_client = boto3.client('s3')


def test_md_to_html():
    s3_bucket = 'aws-demo-smodak'
    test_event = {
        "Records": [
            {
                "eventVersion": "2.0",
                "eventTime": "1970-01-01T00:00:00.000Z",
                "requestParameters": {
                    "sourceIPAddress": "127.0.0.1"
                },
                "s3": {
                    "configurationId": "testConfigRule",
                    "object": {
                        "eTag": "0123456789abcdef0123456789abcdef",
                        "sequencer": "0A1B2C3D4E5F678901",
                        "key": "lambda/sample.md",
                        "size": 1024
                    },
                    "bucket": {
                        "arn": "arn:aws:s3:::mybucket",
                        "name": "aws-demo-smodak",
                        "ownerIdentity": {
                            "principalId": "EXAMPLE"
                        }
                    },
                    "s3SchemaVersion": "1.0"
                },
                "responseElements": {
                    "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH",
                    "x-amz-request-id": "EXAMPLE123456789"
                },
                "awsRegion": "us-west-2",
                "eventName": "ObjectCreated:Put",
                "userIdentity": {
                    "principalId": "EXAMPLE"
                },
                "eventSource": "aws:s3"
            }
        ]
    }

    lambda_handler(test_event, '')

    keys = 0
    html_key = ''
    for key in s3_client.list_objects(Bucket=s3_bucket)['Contents']:
        keys = keys + 1
        print(key['Key'])
        if key['Key'].endswith(".html"):
            html_key = key['Key']

    assert (keys == 3)
    assert (html_key == 'lambda/sample.html')
