import os   
from dotenv import load_dotenv   

load_dotenv()  

CLIENT_ID = os.getenv("CLIENT_ID")   
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
FRONTEND_URL = os.getenv("FRONTEND_URL")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
