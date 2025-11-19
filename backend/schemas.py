from pydantic import BaseModel, EmailStr
from typing import List, Dict
from datetime import datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True


class CampaignCreate(BaseModel):
    company_name: str
    title: str
    description: str | None = None


class CampaignOut(BaseModel):
    id: int
    company_name: str
    title: str
    description: str | None
    status: str
    created_at: datetime

    class Config:
        orm_mode = True


class SummaryOut(BaseModel):
    campaign: CampaignOut
    averages: Dict[str, float]
