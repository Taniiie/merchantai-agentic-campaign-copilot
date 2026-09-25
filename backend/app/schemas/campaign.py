from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any, Union
from datetime import datetime
import json


class CampaignBase(BaseModel):
    objective: Optional[str] = None
    target_audience: Optional[str] = None
    audience_characteristics: Optional[Union[Dict[str, Any], str]] = None
    budget_allocation: Optional[float] = Field(None, ge=0)
    duration_days: Optional[int] = Field(None, ge=1)
    reasoning: Optional[str] = None
    
    @field_validator('audience_characteristics', mode='before')
    @classmethod
    def parse_audience_characteristics(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return {}
        return v


class CampaignCreate(CampaignBase):
    merchant_id: int


class CampaignUpdate(CampaignBase):
    pass


class CampaignResponse(CampaignBase):
    id: int
    merchant_id: int
    status: str
    readiness_status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class CampaignPlanRequest(BaseModel):
    merchant_id: int


class CampaignPlanResponse(BaseModel):
    objective: str
    target_audience: str
    audience_characteristics: Dict[str, Any]
    budget_allocation: float
    duration_days: int
    reasoning: str
