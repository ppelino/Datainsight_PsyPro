from datetime import datetime
from typing import Dict

from pydantic import BaseModel, ConfigDict


# ==== USER ====


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: datetime

    # Pydantic v2: habilita .from_orm() / from_attributes
    model_config = ConfigDict(from_attributes=True)


# ==== CAMPANHAS ====


class CampaignCreate(BaseModel):
    company_name: str
    title: str
    description: str | None = None


class CampaignOut(BaseModel):
    id: int
    company_name: str
    title: str
    description: str | None = None
    created_at: datetime

    # Também vem direto do SQLAlchemy -> .from_orm()
    model_config = ConfigDict(from_attributes=True)


class SummaryOut(BaseModel):
    campaign: CampaignOut
    averages: Dict[str, float]
