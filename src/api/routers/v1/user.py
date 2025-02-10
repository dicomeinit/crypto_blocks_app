from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from django.contrib.auth import get_user_model

from api.schemas import UserCreate, UserResponse, Token, LoginRequest
from api.services.user import (
    check_user_exists,
    create_user,
    get_user_by_id,
    activate_user,
    get_current_user,
    verify_password,
    create_access_token,
    get_user_by_username,
)


ACCESS_TOKEN_EXPIRE_MINUTES = 60
oauth2_scheme = HTTPBearer()
router = APIRouter(prefix="/api/v1/users", tags=["users"])
User = get_user_model()


# API Endpoints
@router.post("/register/", response_model=UserResponse)
async def register_user(user_data: UserCreate):
    exists, error_message = await check_user_exists(user_data.username, user_data.email)
    if exists:
        raise HTTPException(status_code=400, detail=error_message)

    user = await create_user(
        username=user_data.username, email=user_data.email, password=user_data.password
    )

    return UserResponse(
        id=user.id, email=user.email, username=user.username, is_active=user.is_active
    )


@router.post("/approve/{user_id}/", response_model=UserResponse)
async def approve_user(user_id: int):
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = await activate_user(user)
    return UserResponse(
        id=updated_user.id,
        email=updated_user.email,
        username=updated_user.username,
        is_active=updated_user.is_active,
    )


@router.post("/login/", response_model=Token)
async def login(login_data: LoginRequest):
    user = await get_user_by_username(login_data.username)
    if not user or not await verify_password(user, login_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not active",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token)


@router.get("/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        is_active=current_user.is_active,
    )
