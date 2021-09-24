import json
import boto3
from logic import logic
    
def lambda_handler(event, context):
    if "challenge" in list(event.keys()):
        return event['challenge']
    else:
        logic(event)
        return {
            'statusCode': 200,
            'body': "Success"
        }
