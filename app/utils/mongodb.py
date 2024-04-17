from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient


load_dotenv()
MONGODB_URL = os.getenv("MONGODB_URL")

# MongoDB client
client = AsyncIOMotorClient(MONGODB_URL)
db = client["cd_rent_system"]

# Define MongoDB collections
borrowers_collection = db["borrowers"]
artists_collection = db["artists"]
cd_albums_collection = db["cd_albums"]
