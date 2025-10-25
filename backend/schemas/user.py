from pydantic import BaseModel, EmailStr, Field

class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=72, description="Password must be between 6 and 72 characters")

class SigninRequest(BaseModel):
    email: EmailStr
    password: str = Field(max_length=72, description="Password must not exceed 72 characters")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserRead(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
