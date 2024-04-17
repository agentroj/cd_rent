from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient


class Borrower(BaseModel):
    id: int
    name: str
    address: str
    contact_number: str
    borrowed_cd_albums: list = []


class Artist(BaseModel):
    id: int
    name: str
    country: str
    genre: str
    cd_albums: list = []


class CDAlbum(BaseModel):
    id: int
    title: str
    artist_id: int
