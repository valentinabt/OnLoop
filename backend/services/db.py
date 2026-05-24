import boto3
import logging
from backend.config import DYNAMODB_TABLE_NAME, DYNAMODB_REFRESH_TABLE_NAME
from backend.utils import decrypt_token

logger = logging.getLogger(__name__)
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table(DYNAMODB_TABLE_NAME)
refresh_table = dynamodb.Table(DYNAMODB_REFRESH_TABLE_NAME)



def delete_session_items(session_id: str):

    dynamodb.meta.client.transact_write(Items=[
         {
            'Delete': {
            'TableName': DYNAMODB_TABLE_NAME,
            'Key': {'session_id': {'S': session_id}}
             }
        },
        {
            'Delete': {
            'TableName': DYNAMODB_REFRESH_TABLE_NAME,
            'Key': {'session_id': {'S': session_id}}
            }
        }
        ])
    

def write_session(session_id: str, encrypted_access_token: str, encrypted_refresh_token: str, expiration):
    dynamodb.meta.client.transact_write(Items=[
            {
                'Put': {
                    'TableName': DYNAMODB_TABLE_NAME,
                    'Item': {
                        'session_id': {'S': session_id},
                        'access_token': {'S': encrypted_access_token},
                        'ttl': {'N': str(expiration)}
                    }
                }
            },
            {
                'Put': {
                    'TableName': DYNAMODB_REFRESH_TABLE_NAME,
                    'Item': {
                        'session_id': {'S': session_id},
                        'refresh_token': {'S': encrypted_refresh_token}
                    }
                }
            }
        ])

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
    return get_item_from_table(table, session_id, 'access_token')


def get_refresh_token_from_table(session_id: str):
     return get_item_from_table(refresh_table, session_id, 'refresh_token')

