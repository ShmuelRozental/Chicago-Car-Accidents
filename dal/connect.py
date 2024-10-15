from pymongo import MongoClient
from ..config import Config
from threading import Lock

class Database:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the MongoDB client with connection pooling."""
        try:
            self.client = MongoClient(
                Config.MONGO_URI,
                maxPoolSize=100,
                minPoolSize=10,
                serverSelectionTimeoutMS=5000
            )
            self.db = self.client['TrafficAccidentsDB']
            print("Database connected successfully.")
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            raise

    def get_collection(self, collection_name):
        """Return a MongoDB collection."""
        return self.db[collection_name]

    def drop_collection(self, collection_name):
        """drop a MongoDB collection. """
        self.db[collection_name].drop()


    def get_all_collection(self):
        """Return all collection"""
        return self.db.list_collection_names()

    def close(self):
        """Close the MongoDB client connection."""
        self.client.close()


database = Database()