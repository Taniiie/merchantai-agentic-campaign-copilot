from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class Merchant(Base):
    __tablename__ = "merchants"
    
    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String(255), nullable=False)
    business_type = Column(String(100), nullable=False)
    location = Column(String(255), nullable=False)
    product_service = Column(Text, nullable=False)
    target_customers = Column(Text, nullable=True)
    marketing_goal = Column(Text, nullable=True)
    campaign_budget = Column(Float, nullable=True)
    promotion_offer = Column(Text, nullable=True)
    preferred_platform = Column(String(100), nullable=True)
    onboarding_complete = Column(Integer, default=0)  # 0-100 percentage
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
