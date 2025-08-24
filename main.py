from fastapi import FastAPI
from app.db import init_db
from contextlib import asynccontextmanager
from app.user_router import router as user_router
from app.auth_router import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Fitness Tracker API"}