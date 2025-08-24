from app.models import User
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, Depends, status
from app.auth import hash_password, create_access_token, verify_password, get_current_user

router = APIRouter(prefix="/auth")

@router.post("/register")
async def register(username: str, email: str, password: str):
    existing_user = await User.find_one(User.username == username)

    if existing_user:
        raise HTTPException(status_code=400, detail="user already exist")

    user = User(username=username, email=email, password=hash_password(password))
    await user.insert()
    return {"message": "User registered successfully"}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.find_one(User.username == form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user