
from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, Optional, Union, cast
from fastapi import APIRouter, HTTPException, FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os, logging
from motor.motor_asyncio import AsyncIOMotorClient
from app.database.database import Artist


router = APIRouter(
    prefix="/artists", tags=["Artists"], responses={404: {"artists": "Not found"}}
)

load_dotenv()
MONGODB_URL = os.getenv("MONGODB_URL")

# MongoDB client
client = AsyncIOMotorClient(MONGODB_URL)
db = client["cd_rent_system"]

# Define MongoDB collections
artists_collection = db["artists"]


# Artists CRUD operations
@router.get("/")
async def get_artists():
    all_artists = []
    logging.warning(artists_collection)
    async for artist in artists_collection.find():
        artist['_id'] = str(artist['_id'])  # Convert ObjectId to string
        all_artists.append(artist)
    return all_artists


@router.get("/{artist_id}")
async def get_artist(artist_id: int):
    artist = await artists_collection.find_one({"id": artist_id})
    artist['_id'] = str(artist['_id'])
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist


@router.post("/")
async def create_artist(artist: Artist):
    await artists_collection.insert_one(artist.dict())
    return artist


@router.put("/{artist_id}")
async def update_artist(artist_id: int, artist: Artist):
    existing_artist = await artists_collection.find_one({"id": artist_id})
    if not existing_artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    # Update only the fields that are provided in the request
    updated_data = artist.dict(exclude_unset=True)

    await artists_collection.update_one({"id": artist_id}, {"$set": updated_data})

    return {**existing_artist, **updated_data}


@router.delete("/{artist_id}")
async def delete_artist(artist_id: int):
    result = await artists_collection.delete_one({"id": artist_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Artist not found")
    return {"message": f"Artist {artist_id} deleted successfully"}
