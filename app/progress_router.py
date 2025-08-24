from fastapi import APIRouter, Depends, HTTPException
from app.models import ProgressLog, User
from app.auth import get_current_user
from datetime import date

router = APIRouter(prefix="/progress", tags=["progress"])

@router.post("/")
async def log_progress(log: ProgressLog, current_user: User = Depends(get_current_user)):
    # log = ProgressLog(user_id=current_user.id, date=date, notes=notes)
    if not current_user.id:
        raise ValueError("no user id")

    log.user_id = current_user.id
    await log.insert()
    return log

@router.get("/")
async def list_progress(current_user: User = Depends(get_current_user)):
    return await ProgressLog.find(ProgressLog.user_id == current_user.id).to_list()

@router.put("/{log_id}")
async def update_progress(log_id: str, notes: str, current_user: User = Depends(get_current_user)):
    log = await ProgressLog.get(log_id)
    if not log or log.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Log not found")
    await log.save()
    return log

@router.delete("/{log_id}")
async def delete_progress(log_id: str, current_user: User = Depends(get_current_user)):
    log = await ProgressLog.get(log_id)
    if not log or log.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Log not found")
    await log.delete()
    return {"message": "Progress log deleted"}
