from pydantic import BaseModel, field_validator
from typing import Optional, Dict, Any, Union, List
from datetime import datetime
import json


class CreativeBriefBase(BaseModel):
    visual_concept: Optional[str] = None
    scene_direction: Optional[str] = None
    headline_placement: Optional[str] = None
    tone: Optional[str] = None
    suggested_imagery: Optional[Union[Dict[str, Any], str, List[str]]] = None
    suggested_format: Optional[str] = None
    key_selling_point: Optional[str] = None
    
    @field_validator('suggested_imagery', mode='before')
    @classmethod
    def parse_suggested_imagery(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        # If it's already a list or dict, return as is
        return v


class CreativeBriefCreate(CreativeBriefBase):
    campaign_id: int


class CreativeBriefResponse(CreativeBriefBase):
    id: int
    campaign_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class CreativeBriefGenerationRequest(BaseModel):
    campaign_id: int
