from fastapi import APIRouter, HTTPException
from app.models import Exercise

router = APIRouter(prefix="/exercises", tags=["exercises"])

@router.post("/")
async def create_exercise(exercise :  Exercise):
    # exercise = Exercise(exercise_name=name, muscle_group=muscle_group, equipment=equipment, difficulty=difficulty)
    await exercise.insert()
    return exercise

@router.get("/")
async def list_exercises():
    return await Exercise.find_all().to_list()

@router.get("/{exercise_id}")
async def get_exercise(exercise_id: str):
    exercise = await Exercise.get(exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise
