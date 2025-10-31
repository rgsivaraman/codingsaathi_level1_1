from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Agent Schemas
class AgentBase(BaseModel):
    name: str
    description: Optional[str] = None
    code: str
    tags: Optional[str] = None
    is_public: bool = True


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    code: Optional[str] = None
    tags: Optional[str] = None
    is_public: Optional[bool] = None
    version: Optional[str] = None


class AgentResponse(AgentBase):
    id: int
    creator_id: int
    parent_id: Optional[int] = None
    version: str
    is_active: bool
    usage_count: int
    created_at: datetime
    updated_at: datetime
    average_rating: Optional[float] = None
    creator_username: Optional[str] = None

    class Config:
        from_attributes = True


class AgentExecuteRequest(BaseModel):
    agent_id: int
    input_data: dict = {}


class AgentExecuteResponse(BaseModel):
    success: bool
    output: Optional[str] = None
    error: Optional[str] = None


# Rating Schemas
class RatingCreate(BaseModel):
    agent_id: int
    rating: float = Field(..., ge=1, le=5)


class RatingResponse(BaseModel):
    id: int
    agent_id: int
    user_id: int
    rating: float
    created_at: datetime

    class Config:
        from_attributes = True


# Review Schemas
class ReviewCreate(BaseModel):
    agent_id: int
    comment: str


class ReviewUpdate(BaseModel):
    comment: str


class ReviewResponse(BaseModel):
    id: int
    agent_id: int
    user_id: int
    comment: str
    created_at: datetime
    updated_at: datetime
    username: Optional[str] = None

    class Config:
        from_attributes = True


# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
