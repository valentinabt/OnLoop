import boto3
import secrets
import time


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('toptify-sessions')

def create_session(access_token: str):
    session_id = generate_session_id()
    expiration = int(time.time()) + 3600
    table.put_item(Item={
        'session_id': session_id,
        'access_token': access_token,
        'ttl': expiration
    })
    return session_id

def get_token_from_session(session_id: str):
    response = table.get_item(Key={'session_id': session_id})
    item = response.get('Item')
    if not item:
        return None
    return item['access_token']

def delete_session(session_id: str):
    table.delete_item(Key={'session_id': session_id})

def generate_session_id():
    return secrets.token_urlsafe(8)
