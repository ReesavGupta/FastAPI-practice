from fastapi import APIRouter, Depends, HTTPException
from app.models import WorkoutPlan, User
from app.auth import get_current_user

router = APIRouter(prefix="/workouts", tags=["workouts"])

@router.post("/")
async def create_workout(plan_name: str, current_user: User = Depends(get_current_user)):
    if not current_user.id:
        return
    workout = WorkoutPlan(user_id=current_user.id, plan_name=plan_name)
    if not  workout:
        raise ValueError("No workout created")
    await workout.insert()
    return workout

@router.get("/")
async def list_workouts(current_user: User = Depends(get_current_user)):
    return await WorkoutPlan.find(WorkoutPlan.user_id == current_user.id).to_list()

@router.put("/{workout_id}")
async def update_workout(workout_id: str, plan_name: str, current_user: User = Depends(get_current_user)):
    workout = await WorkoutPlan.get(workout_id)
    if not workout or workout.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Workout not found")
    workout.plan_name = plan_name
    await workout.save()
    return workout

@router.delete("/{workout_id}")
async def delete_workout(workout_id: str, current_user: User = Depends(get_current_user)):
    workout = await WorkoutPlan.get(workout_id)
    if not workout or workout.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Workout not found")
    await workout.delete()
    return {"message": "Workout deleted"}
