from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class AdCopy(Base):
    __tablename__ = "ad_copies"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    primary_copy = Column(Text, nullable=True)
    headline = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    cta = Column(Text, nullable=True)
    variation_1_copy = Column(Text, nullable=True)
    variation_1_headline = Column(Text, nullable=True)
    variation_1_description = Column(Text, nullable=True)
    variation_1_cta = Column(Text, nullable=True)
    variation_2_copy = Column(Text, nullable=True)
    variation_2_headline = Column(Text, nullable=True)
    variation_2_description = Column(Text, nullable=True)
    variation_2_cta = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    campaign = relationship("Campaign", back_populates="ad_copy")
