
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = os.getenv('FLASK_DEBUG', 'production') == 'development'
    MONGO_URI = os.getenv('DATABASE_URL', 'mongodb://localhost:27017/flask_db')
