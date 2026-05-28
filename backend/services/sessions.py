import secrets
import time
import logging
from backend.services.db import delete_session_items, write_session, get_access_token_from_table, get_refresh_token_from_table
from backend.utils import encrypt_token
logger = logging.getLogger(__name__)



def create_session(access_token: str, refresh_token: str):
    session_id = generate_session_id()
    try:
        save_session(session_id, access_token, refresh_token)
        return session_id
    except Exception:
        logger.exception("Failed to create session")
        return None

def generate_session_id():
    return secrets.token_urlsafe(32)


def update_session(session_id: str, access_token: str, refresh_token: str):
    
    try:
        save_session(session_id, access_token, refresh_token)
        return session_id
    except Exception:
        logger.exception("Failed to update session")
        return None
    
def delete_session(session_id: str):
    try:
        delete_session_items(session_id)
    except Exception:
        logger.exception("Failed to delete session")
        raise

def get_access_token_from_session(session_id: str):
    return get_access_token_from_table(session_id)

def get_refresh_token_from_session(session_id: str):
    return get_refresh_token_from_table(session_id)


def save_session(session_id: str, access_token: str, refresh_token: str):
    expiration = int(time.time()) + (14 * 24 * 3600)  #14 days
    encrypted_access_token = encrypt_token(access_token)
    encrypted_refresh_token = encrypt_token(refresh_token)
    write_session(session_id, encrypted_access_token, encrypted_refresh_token, expiration)
    