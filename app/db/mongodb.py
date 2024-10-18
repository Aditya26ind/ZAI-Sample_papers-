# app/db/mongodb.py
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]

mongodb = MongoDB(uri=os.getenv("MONGODB_URI"), db_name="SamplePaper")