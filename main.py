from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import init_db
from app.user_router import router as user_router
from app.auth_router import router as auth_router
from app.excercise_router import router as exercise_router
from app.workout_router import router as workout_router
from app.progress_router import router as progress_router
from app.nutrition_router import router as nutrition_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

# Routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(exercise_router)
app.include_router(workout_router)
app.include_router(progress_router)
app.include_router(nutrition_router)

@app.get("/")
async def root():
    return {"message": "Fitness Tracker API"}
