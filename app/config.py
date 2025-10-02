# database configuration
import os
from dotenv import load_dotenv

# Load env
load_dotenv()

# Database config
class Config:
    SQLALCHEMY_DATABASE_URI= os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS= False
