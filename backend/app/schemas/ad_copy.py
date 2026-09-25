from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AdCopyBase(BaseModel):
    primary_copy: Optional[str] = None
    headline: Optional[str] = None
    description: Optional[str] = None
    cta: Optional[str] = None
    variation_1_copy: Optional[str] = None
    variation_1_headline: Optional[str] = None
    variation_1_description: Optional[str] = None
    variation_1_cta: Optional[str] = None
    variation_2_copy: Optional[str] = None
    variation_2_headline: Optional[str] = None
    variation_2_description: Optional[str] = None
    variation_2_cta: Optional[str] = None


class AdCopyCreate(AdCopyBase):
    campaign_id: int


class AdCopyResponse(AdCopyBase):
    id: int
    campaign_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
        
    @classmethod
    def from_orm(cls, obj):
        # Handle any ORM-specific conversions if needed
        return cls(**obj.__dict__)


class AdCopyGenerationRequest(BaseModel):
    campaign_id: int
