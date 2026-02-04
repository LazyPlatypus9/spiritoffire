from typing import List

from app import logger
from pymongo import MongoClient
from pymongo.database import Database

class MongoDatabase:
    def __init__(self, username: str, password: str, host: str, port: str):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.client = None

    def get_client(self):
        mongo_uri: List[str] = ["mongodb://"]

        if self.username and self.password:
            logger.info("Using secure connection for Mongo...")
            mongo_uri.append(f"{self.username}:{self.password}@")
        else:
            logger.warning("Using insecure connection for Mongo!!")

        mongo_uri.append(f"{self.host}:{self.port}")

        return MongoClient(''.join(mongo_uri))
    
    def get_database(self, name: str) -> Database:
        if not self.client:
            self.client = self.get_client()
        
        return self.client[name]