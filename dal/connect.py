from pymongo import MongoClient
from config import Config

class Database:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client['TrafficAccidentsDB']

    def get_db(self):
        return self.db

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def close(self):
        self.client.close()


database = Database()