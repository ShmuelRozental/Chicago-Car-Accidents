import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/TrafficAccidentsDB')
