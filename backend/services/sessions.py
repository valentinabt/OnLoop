
import secrets
import time
import logging
from backend.config import ENCRYPTION_KEY
from cryptography.fernet import Fernet
from db import delete_session_items, write_session, get_item_from_table , get_access_token_from_table, get_refresh_token_from_table

logger = logging.getLogger(__name__)
f = Fernet(ENCRYPTION_KEY.encode())


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

def encrypt_token(token: str) -> str:
    return f.encrypt(token.encode()).decode()

def decrypt_token(token: str) -> str:
    return f.decrypt(token.encode()).decode()

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
    expiration = int(time.time()) + 3600
    encrypted_access_token = encrypt_token(access_token)
    encrypted_refresh_token = encrypt_token(refresh_token)
    write_session(session_id, encrypted_access_token, encrypted_refresh_token, expiration)
    