from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, description="Minimum 8 characters")
    full_name: str = Field(min_length=1)
    organization_name: str = Field(min_length=1)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthUserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    department: str
    organization_id: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    user: AuthUserResponse
