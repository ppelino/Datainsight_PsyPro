from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict


# =======================
# USER
# =======================

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =======================
# CAMPANHAS
# =======================

class CampaignCreate(BaseModel):
    company_name: str
    title: str
    description: Optional[str] = None


class CampaignOut(BaseModel):
    id: int
    company_name: str
    title: str
    description: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SummaryOut(BaseModel):
    campaign: CampaignOut
    averages: Dict[str, float]


# =======================
# SURVEY PÚBLICO
# =======================

class AnswerIn(BaseModel):
    dimension: str     # Ex.: "Demandas"
    score: int         # 1 a 5


class PublicSurveyIn(BaseModel):
    campaign_id: int
    answers: List[AnswerIn]
