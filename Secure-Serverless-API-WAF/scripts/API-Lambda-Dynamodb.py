import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('login-activity')

def lambda_handler(event, context):
    
    print("EVENT:", json.dumps(event))  # Debug log
    
    # Extract IP (FIXED)
    ip = event['requestContext']['http']['sourceIp']
    
    # Parse body safely
    body = json.loads(event.get('body', '{}'))
    username = body.get('username', 'unknown')

    table.put_item(
        Item={
            'username': username,
            'timestamp': str(datetime.utcnow()),
            'ip': ip
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({
            "message": "Login recorded",
            "ip": ip
        })
    }