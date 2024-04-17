from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

import os
from motor.motor_asyncio import AsyncIOMotorClient

from app.utils import mongodb
from app.routers import (
    artists,
    borrowers,
    cd_albums,
    rent
)
load_dotenv()

# Load environment variables
DEBUG = os.getenv("DEBUG")


app = FastAPI()


FRONTEND_ENV = os.environ.get("FRONTEND_ENV", "")
# Define allowed origins for CORS
origins = [FRONTEND_ENV, "http://localhost:3000"]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(artists.router)
app.include_router(borrowers.router)
app.include_router(cd_albums.router)
app.include_router(rent.router)


@app.get("/")
async def root():
    return {"message": "Hello World!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8080, reload=bool(DEBUG))
