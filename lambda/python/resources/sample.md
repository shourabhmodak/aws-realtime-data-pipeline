# AWS Lambda to convert md to HTML 

This tutorial will show you how you can use AWS Lambda to convert
 a markdown file into HTML as soon as the file lands on an S3 bucket.
We will be implementing a simple transform that renders markdown
in `Text` fields to HTML which would be triggered by a S3 add object event.

What is Lambda:
 - a service from Amazon that lets you run code in response to events
 - no servers to manage, continuous scaling 


## Steps:

1. Sign in to the [AWS Console]
2. Select "Lambda" from the "Services" section of the top menu.
3. Select "Create a new lambda" 
4. Select Python 3.6
5. Copy and paste the code into Lambda console