from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.models.documents import UserRole


class UserProfileResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    department: str
    organization_id: str
    created_at: datetime


class UpdateProfileRequest(BaseModel):
    full_name: str | None = Field(None, min_length=1)
    department: str | None = None


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)


class SessionItemResponse(BaseModel):
    id: str
    user_agent: str
    created_at: datetime
    expires_at: datetime
    is_current: bool = False


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str = Field(min_length=1)
    role: UserRole
    department: str = ""


class UpdateUserRoleRequest(BaseModel):
    role: UserRole


class DeleteAccountRequest(BaseModel):
    confirm_text: str = Field(description="Must equal 'DELETE'")
