
from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, Optional, Union, cast
from fastapi import APIRouter, HTTPException, FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient
from app.database.database import Borrower, CDAlbum, Artist


router = APIRouter(
    prefix="/rent", tags=["Rent"], responses={404: {"rent": "Not found"}}
)

load_dotenv()
MONGODB_URL = os.getenv("MONGODB_URL")

# MongoDB client
client = AsyncIOMotorClient(MONGODB_URL)
db = client["cd_rent_system"]

# Define MongoDB collections
borrowers_collection = db["borrowers"]


@router.put("/{borrower_id}")
async def rent_cd_album_to_borrower(borrower_id: int, cd_id: int):
    await borrowers_collection.update_one({"id": borrower_id}, {"$addToSet": {"borrowed_cd_albums": cd_id}})
    return {"message": f"CD album {cd_id} rented to borrower {borrower_id}"}


@router.delete("/{borrower_id}")
async def return_cd_album_from_borrower(borrower_id: int, cd_id: int):
    await borrowers_collection.update_one({"id": borrower_id}, {"$pull": {"borrowed_cd_albums": cd_id}})
    return {"message": f"CD album {cd_id} returned from borrower {borrower_id}"}
