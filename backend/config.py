import os   
from dotenv import load_dotenv   

load_dotenv()  

CLIENT_ID = os.getenv("CLIENT_ID")   
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
FRONTEND_URL = os.getenv("FRONTEND_URL")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
