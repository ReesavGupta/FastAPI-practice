import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from beanie import init_beanie
from app.models import User, Exercise, WorkoutPlan, ProgressLog, NutritionLog

load_dotenv()

client : AsyncIOMotorClient | None = None

async def init_db():
    global client

    client = AsyncIOMotorClient(os.getenv("MONGO_DB_URI"))

    if not client:
        raise ValueError("There was no client initialized for the database")
        return
        
    db_name = os.getenv("MONGO_DB_DATABASE")
    
    if not db_name:
        raise ValueError("MONGO_DB_DATABASE environment variable is not set")
        
    database = client.get_database(db_name)

    await init_beanie(database=database, document_models=[User, Exercise, WorkoutPlan, ProgressLog, NutritionLog]) #type:ignore 