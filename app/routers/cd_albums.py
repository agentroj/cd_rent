
from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, Optional, Union, cast
from fastapi import APIRouter, HTTPException, FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient
from app.database.database import CDAlbum


router = APIRouter(
    prefix="/cd_album", tags=["CD Albums"], responses={404: {"cd_album": "Not found"}}
)

load_dotenv()
MONGODB_URL = os.getenv("MONGODB_URL")

# MongoDB client
client = AsyncIOMotorClient(MONGODB_URL)
db = client["cd_rent_system"]

# Define MongoDB collections
cd_albums_collection = db["cd_album"]
artists_collection = db["artists"]


# CD Albums CRUD operations
@router.get("/")
async def get_cd_albums():
    all_cd_albums = []
    async for cd_album in cd_albums_collection.find():
        cd_album['_id'] = str(cd_album['_id'])
        all_cd_albums.append(cd_album)
    return all_cd_albums


@router.get("/{cd_album_id}")
async def get_cd_album(cd_album_id: int):
    cd_album = await cd_albums_collection.find_one({"id": cd_album_id})
    cd_album['_id'] = str(cd_album['_id'])
    if not cd_album:
        raise HTTPException(status_code=404, detail="CD Album not found")
    return cd_album


@router.post("/cd-albums/")
async def create_cd_album(cd_album: CDAlbum):
    # Check if the artist_id exists in the artists table
    artist = await artists_collection.find_one({"id": cd_album.artist_id})
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    # Insert the CD album into the CD albums collection
    await cd_albums_collection.insert_one(cd_album.dict())
    
    # Update the corresponding artist's cd_albums field
    await artists_collection.update_one({"id": cd_album.artist_id}, {"$addToSet": {"cd_albums": cd_album.id}})
    
    return cd_album

@router.put("/cd-albums/{cd_album_id}")
async def update_cd_album(cd_album_id: int, cd_album: CDAlbum):
    existing_cd_album = await cd_albums_collection.find_one({"id": cd_album_id})
    if not existing_cd_album:
        raise HTTPException(status_code=404, detail="CD Album not found")

    # Check if the artist_id exists in the artists table
    artist = await artists_collection.find_one({"id": cd_album.artist_id})
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    # Update only the fields that are provided in the request
    updated_data = cd_album.dict(exclude_unset=True)

    await cd_albums_collection.update_one({"id": cd_album_id}, {"$set": updated_data})

    # No need to update artist's cd_albums field here, as artist_id is not being modified
    
    return {**existing_cd_album, **updated_data}

@router.delete("/cd-albums/{cd_album_id}")
async def delete_cd_album(cd_album_id: int):
    existing_cd_album = await cd_albums_collection.find_one({"id": cd_album_id})
    if not existing_cd_album:
        raise HTTPException(status_code=404, detail="CD Album not found")

    # Remove CD album from CD albums collection
    await cd_albums_collection.delete_one({"id": cd_album_id})
    
    # Remove CD album from corresponding artist's cd_albums field
    await artists_collection.update_one({"id": existing_cd_album['artist_id']}, {"$pull": {"cd_albums": cd_album_id}})

    return {"message": f"CD Album {cd_album_id} deleted successfully"}

# Similar endpoints for CD albums CRUD operations...
