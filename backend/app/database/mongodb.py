import motor.motor_asyncio
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = "fateverse"

# Async client for FastAPI
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client[DATABASE_NAME]

# Collections
users = db.users
fortune_history = db.fortune_history
tarot_cards = db.tarot_cards
zodiac_data = db.zodiac_data
daily_fortunes = db.daily_fortunes

# Indexes
async def create_indexes():
    # User indexes
    await users.create_index("email", unique=True)
    await users.create_index("created_at")
    
    # Fortune history indexes
    await fortune_history.create_index([("user_id", 1), ("created_at", -1)])
    await fortune_history.create_index("type")
    
    # Daily fortune index
    await daily_fortunes.create_index("fortune_date", unique=True)

# Database initialization
async def init_db():
    try:
        await create_indexes()
        print("Database indexes created successfully")
    except Exception as e:
        print(f"Error creating database indexes: {e}")

# Helper functions
async def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")