import json
import boto3

sns = boto3.client('sns')

TOPIC_ARN = 'arn:aws:sns:us-east-1:356627769333:cloud-trail-tamper'

def lambda_handler(event, context):

    detail = event.get('detail', {})

    event_name = detail.get('eventName', 'Unknown')
    user = detail.get('userIdentity', {}).get('userName', 'Unknown')
    source_ip = detail.get('sourceIPAddress', 'Unknown')

    message = f"""
CloudTrail Tampering Attempt Detected

Event Name: {event_name}
User: {user}
Source IP: {source_ip}

Potential defense evasion attempt detected.
"""

    sns.publish(
        TopicArn= TOPIC_ARN,
        Subject='AWS Security Alert - CloudTrail Tampering',
        Message=message
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Alert sent')
    }