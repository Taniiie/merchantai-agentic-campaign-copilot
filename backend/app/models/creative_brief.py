from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class CreativeBrief(Base):
    __tablename__ = "creative_briefs"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    visual_concept = Column(Text, nullable=True)
    scene_direction = Column(Text, nullable=True)
    headline_placement = Column(Text, nullable=True)
    tone = Column(Text, nullable=True)
    suggested_imagery = Column(Text, nullable=True)  # JSON string (can be array or object)
    suggested_format = Column(Text, nullable=True)
    key_selling_point = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    campaign = relationship("Campaign", back_populates="creative_brief")
