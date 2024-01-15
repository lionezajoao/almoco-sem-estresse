from pydantic import BaseModel
from typing import Optional, List

class UserBase(BaseModel):
    email: str

class UserLogin(UserBase):
    password: str

class UserCreate(UserBase):
    name: str
    password: str
    role: str