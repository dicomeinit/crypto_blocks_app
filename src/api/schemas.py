from pydantic import BaseModel, EmailStr


class BlockResponse(BaseModel):
    id: int
    currency_id: int
    currency_name: str
    provider_id: int
    provider_name: str
    block_number: int
    created_at: str
    stored_at: str

    class Config:
        from_attributes = True


class PaginatedBlockResponse(BaseModel):
    total: int
    limit: int
    offset: int
    results: list[BlockResponse]

    class Config:
        from_attributes = True


class ProviderResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str
