from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class ValidationIssue(Base):
    __tablename__ = "validation_issues"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    issue_type = Column(String(50), nullable=False)  # missing_field, inconsistent_data, validation_error
    field_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(20), default="warning")  # info, warning, error
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    campaign = relationship("Campaign", back_populates="validation_issues")
