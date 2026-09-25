from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MerchantBase(BaseModel):
    business_name: str = Field(..., min_length=1, max_length=255)
    business_type: str = Field(..., min_length=1, max_length=100)
    location: str = Field(..., min_length=1, max_length=255)
    product_service: str = Field(..., min_length=1)
    target_customers: Optional[str] = None
    marketing_goal: Optional[str] = None
    campaign_budget: Optional[float] = Field(None, ge=0)
    promotion_offer: Optional[str] = None
    preferred_platform: Optional[str] = None


class MerchantCreate(MerchantBase):
    pass


class MerchantUpdate(MerchantBase):
    pass


class MerchantResponse(MerchantBase):
    id: int
    onboarding_complete: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class OnboardingValidation(BaseModel):
    is_complete: bool
    completion_percentage: int
    missing_fields: list[str]
    next_step: str
