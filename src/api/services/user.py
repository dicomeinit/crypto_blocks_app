from datetime import datetime, timedelta
from typing import Optional

from asgiref.sync import sync_to_async
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from django.contrib.auth import get_user_model
from django.db import transaction
from django.conf import settings
from pydantic import EmailStr


# Constants
ALGORITHM = "HS256"
# Setup
oauth2_scheme = HTTPBearer()
User = get_user_model()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


# Database operations
@sync_to_async
def check_user_exists(username: str, email: str) -> tuple[bool, str]:
    if User.objects.filter(username=username).exists():
        return True, "Username already registered"
    if User.objects.filter(email=email).exists():
        return True, "Email already registered"
    return False, ""


@sync_to_async
def create_user(username: str, email: EmailStr, password: str) -> User:
    with transaction.atomic():
        return User.objects.create_user(
            username=username, email=email, password=password, is_active=False
        )


@sync_to_async
def get_user_by_id(user_id: int) -> Optional[User]:
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


@sync_to_async
def get_user_by_username(username: str) -> Optional[User]:
    return User.objects.filter(username=username).first()


@sync_to_async
def get_user_for_token(username: str) -> Optional[User]:
    return User.objects.filter(username=username).first()


# User operations
@sync_to_async
def activate_user(user: User) -> User:
    user.is_active = True
    user.save()
    return user


@sync_to_async
def verify_password(user: User, password: str) -> bool:
    return user.check_password(password)


# Authentication middleware
async def get_current_user(token=Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token.credentials, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_for_token(username)
    if user is None:
        raise credentials_exception

    return user
