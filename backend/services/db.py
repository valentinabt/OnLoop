import boto3
import logging
from backend import config
from backend.utils import decrypt_token


logger = logging.getLogger(__name__)
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')


def get_table():
    return dynamodb.Table(config.DYNAMODB_TABLE_NAME)


def delete_session_items(session_id: str):
    try:
        get_table().delete_item(Key={'session_id': session_id})
    except Exception:
        logger.exception("DynamoDB delete_session failed")
        raise 

def write_session(session_id: str, encrypted_access_token: str, encrypted_refresh_token: str, expiration):
    try:
        get_table().put_item(Item={
            'session_id': session_id,
            'access_token': encrypted_access_token,
            'refresh_token': encrypted_refresh_token,
            'ttl': expiration
        })
    except Exception:
        logger.exception("DynamoDB write_session failed")
        raise

def get_item_from_table(table_ref, session_id: str, field: str):
    try:
        response = table_ref.get_item(Key={'session_id': session_id})
    except Exception:
        logger.exception("DynamoDB get_item failed")
        return None
    item = response.get('Item')
    if not item:
        return None
    return decrypt_token(item[field])

def get_access_token_from_table(session_id: str):
    return get_item_from_table(get_table(), session_id, 'access_token')


def get_refresh_token_from_table(session_id: str):
     return get_item_from_table(get_table(), session_id, 'refresh_token')

