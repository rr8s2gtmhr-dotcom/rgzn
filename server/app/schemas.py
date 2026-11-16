from typing import Any, Generic, TypeVar, Optional, List
from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    code: int = 0
    message: str = "success"
    data: Optional[T] = None


class PageResult(BaseModel, Generic[T]):
    list: List[T]
    total: int
    pageNum: int = 1
    pageSize: int = 10


class LoginRequest(BaseModel):
    userName: str
    password: str


class SettingRequest(BaseModel):
    settings: dict
