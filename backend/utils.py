from backend.config import ENCRYPTION_KEY
from cryptography.fernet import Fernet
f = Fernet(ENCRYPTION_KEY.encode())


def encrypt_token(token: str) -> str:
    return f.encrypt(token.encode()).decode()

def decrypt_token(token: str) -> str:
    return f.decrypt(token.encode()).decode()