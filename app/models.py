from beanie import Document, Indexed, Link, PydanticObjectId
from pydantic import EmailStr, Field
from typing import Optional, List
from datetime import datetime, date

class User(Document):
    username: Indexed(str, unique=True)   # type: ignore
    email: Indexed(EmailStr, unique=True) # type: ignore
    password: str
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    fitness_goals: Optional[str] = None
    medical_conditions: Optional[str] = None
    activity_level: Optional[str] = None

    class Settings:
        name = "users"


class Exercise(Document):
    exercise_name: str
    category: Optional[str] = None
    equipment_needed: Optional[str] = None
    difficulty: Optional[str] = None
    instructions: Optional[str] = None
    target_muscles: Optional[List[str]] = None

    class Settings:
        name = "exercises"


class WorkoutPlan(Document):
    user_id: PydanticObjectId         # link to user
    plan_name: str
    difficulty_level: Optional[str] = None
    duration: Optional[int] = None
    target_muscle_groups: Optional[List[str]] = None
    exercises_list: List[Link[Exercise]] = Field(default_factory=list)

    class Settings:
        name = "workout_plans"


class ProgressLog(Document):
    user_id: PydanticObjectId
    workout_id: Optional[PydanticObjectId] = None
    date: datetime
    exercises_completed: int
    sets: int
    reps: int
    weights: Optional[float] = None
    duration: Optional[int] = None
    calories_burned: Optional[float] = None

    class Settings:
        name = "progress_logs"


class NutritionLog(Document):
    user_id: PydanticObjectId
    date: date
    meals: Optional[str] = None
    calories: Optional[int] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fats: Optional[float] = None

    class Settings:
        name = "nutrition_logs"