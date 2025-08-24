from fastapi import APIRouter, Depends, HTTPException
from app.models import NutritionLog, User
from app.auth import get_current_user
from datetime import date

router = APIRouter(prefix="/nutrition", tags=["nutrition"])

@router.post("/")
async def create_nutrition_log(date: date, calories: int, protein: int, carbs: int, fat: int, current_user: User = Depends(get_current_user)):
    if current_user.id:
        log = NutritionLog(user_id=current_user.id, date=date, calories=calories, protein=protein, carbs=carbs)
        await log.insert()
        return log
    else: 
        raise ValueError("something went wrong")

@router.get("/")
async def list_nutrition_logs(current_user: User = Depends(get_current_user)):
    return await NutritionLog.find(NutritionLog.user_id == current_user.id).to_list()

@router.put("/{log_id}")
async def update_nutrition_log(log_id: str, calories: int, protein: int, carbs: int, fat: int, current_user: User = Depends(get_current_user)):
    log = await NutritionLog.get(log_id)
    if not log or log.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Nutrition log not found")
    log.calories, log.protein, log.carbs = calories, protein, carbs
    await log.save()
    return log

@router.delete("/{log_id}")
async def delete_nutrition_log(log_id: str, current_user: User = Depends(get_current_user)):
    log = await NutritionLog.get(log_id)
    if not log or log.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Nutrition log not found")
    await log.delete()
    return {"message": "Nutrition log deleted"}
