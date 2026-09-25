from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    merchant_id = Column(Integer, ForeignKey("merchants.id"), nullable=False)
    objective = Column(Text, nullable=True)
    target_audience = Column(Text, nullable=True)
    audience_characteristics = Column(Text, nullable=True)  # JSON string
    budget_allocation = Column(Float, nullable=True)
    duration_days = Column(Integer, nullable=True)
    reasoning = Column(Text, nullable=True)
    status = Column(String(50), default="draft")  # draft, ready, approved
    readiness_status = Column(String(50), default="needs_attention")  # ready, needs_attention
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    ad_copy = relationship("AdCopy", back_populates="campaign", uselist=False)
    creative_brief = relationship("CreativeBrief", back_populates="campaign", uselist=False)
    validation_issues = relationship("ValidationIssue", back_populates="campaign")
