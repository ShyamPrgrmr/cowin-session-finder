import boto3
import json

with open('config.json') as json_file:
    config = json.load(json_file)
    email = config['config_email']

def verify_email_identity():
    ses_client = boto3.client("ses", region_name="ap-south-1")
    response = ses_client.verify_email_identity(
        EmailAddress=email
    )
    print(response)