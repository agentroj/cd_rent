
from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, Optional, Union, cast
from fastapi import APIRouter, HTTPException, FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient
from app.database.database import Borrower


router = APIRouter(
    prefix="/borrowers", tags=["Borrowers"], responses={404: {"borrowers": "Not found"}}
)

load_dotenv()
MONGODB_URL = os.getenv("MONGODB_URL")

# MongoDB client
client = AsyncIOMotorClient(MONGODB_URL)
db = client["cd_rent_system"]

# Define MongoDB collections
borrowers_collection = db["borrowers"]


# Borrowers CRUD operations
@router.post("/")
async def create_borrower(borrower: Borrower):
    await borrowers_collection.insert_one(borrower.dict())
    return borrower


@router.get("/{borrower_id}")
async def read_borrower(borrower_id: int):
    borrower = await borrowers_collection.find_one({"id": borrower_id})
    if not borrower:
        raise HTTPException(status_code=404, detail="Borrower not found")
    return Borrower(**borrower)


@router.delete("/{borrower_id}")
async def delete_borrower(borrower_id: int):
    result = await borrowers_collection.delete_one({"id": borrower_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Borrower not found")
    return {"message": f"Borrower {borrower_id} deleted successfully"}


@router.put("/{borrower_id}")
async def update_borrower(borrower_id: int, borrower: Borrower):
    existing_borrower = await borrowers_collection.find_one({"id": borrower_id})
    if not existing_borrower:
        raise HTTPException(status_code=404, detail="Borrower not found")

    # Update only the fields that are provided in the request
    updated_data = borrower.dict(exclude_unset=True)

    await borrowers_collection.update_one({"id": borrower_id}, {"$set": updated_data})

    return {**existing_borrower, **updated_data}
