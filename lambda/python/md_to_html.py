import boto3
import jinja2
import markdown

# Instantiate S3 client
s3_client = boto3.client('s3')

# HTML style template
TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.0/css/bootstrap-combined.min.css" rel="stylesheet">
    <style>
        body {
            font-family: sans-serif;
        }
        code, pre {
            font-family: monospace;
        }
        h1 code,
        h2 code,
        h3 code,
        h4 code,
        h5 code,
        h6 code {
            font-size: inherit;
        }
    </style>
</head>
<body>
<div class="container">
{{content}}
</div>
</body>
</html>
"""


def lambda_handler(event, context):

    for record in event['Records']:
        # Extract bucket and key information from S3 PutObject event
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        output_key = '{}.html'.format(key[:key.rfind('.md')])

        # Read Markdown file content from S3 bucket
        response = s3_client.get_object(Bucket=bucket, Key=key)
        md_content = response['Body'].read().decode('utf-8')
        print("MD " + md_content)

        # Convert Markdown content to HTML
        extensions = ['extra', 'smarty']
        html_content = markdown.markdown(md_content, extensions=extensions, output_format='html5')
        html_content_fmt = jinja2.Template(TEMPLATE).render(content=html_content)
        print("HTML " + html_content_fmt)

        # Encode content before uploading
        encoded_html = html_content_fmt.encode("utf-8")
        # Upload HTML content to S3 bucket
        s3_client.put_object(Bucket=bucket, Key=output_key, Body=encoded_html)
