import os   
from dotenv import load_dotenv   

load_dotenv()  

CLIENT_ID = os.getenv("CLIENT_ID")   
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
FRONTEND_URL = os.getenv("FRONTEND_URL")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
