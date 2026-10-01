"""Pydantic models used to validate user input."""
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class UserInput(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    user_id: int = Field(..., ge=1)
    age: int = Field(..., ge=5, le=120)
    weight: float = Field(..., ge=20, le=400)
    goal: str = Field(..., min_length=2, max_length=200)
    intensity: Literal["low", "medium", "high"]

    @field_validator("username", "goal", mode="before")
    @classmethod
    def _strip(cls, v):
        return v.strip() if isinstance(v, str) else v

    @field_validator("intensity", mode="before")
    @classmethod
    def _lower(cls, v):
        return v.strip().lower() if isinstance(v, str) else v


class FeedbackRequest(BaseModel):
    user_id: int = Field(..., ge=1)
    feedback: str = Field(..., min_length=3, max_length=1000)

    @field_validator("feedback", mode="before")
    @classmethod
    def _strip(cls, v):
        return v.strip() if isinstance(v, str) else v
