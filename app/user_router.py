from fastapi import APIRouter
from app.models import User

router = APIRouter(prefix="/users")

@router.get("/")
async def list_users():
    users = await User.find_all().to_list()
    return users

@router.post("/")
async def create_user(user: User):
    await user.insert()
    return {"message": "User created", "user_id": str(user.id)}