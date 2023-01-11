from __future__ import annotations
from pydantic import BaseModel
from . import models

__all__ = ["TokenData", "User"]


class User(BaseModel):
    user_id: int
    user_type: str
    user_info: models.Admin | models.Technician

    class Config:
        arbitrary_types_allowed = True


class TokenData(BaseModel):
    username: str | None = None
    id: str | None = None
    user_type: str | None = None
