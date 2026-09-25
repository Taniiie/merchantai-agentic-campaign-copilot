from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.database import get_db
from app.models.merchant import Merchant
from app.schemas.merchant import MerchantCreate, MerchantResponse, OnboardingValidation
from app.agents.orchestrator import orchestrator
from app.tools.validation import ValidationTool

router = APIRouter(prefix="/api/merchants", tags=["merchants"])


@router.post("/", response_model=MerchantResponse)
async def create_merchant(merchant: MerchantCreate, db: Session = Depends(get_db)):
    """Create a new merchant"""
    db_merchant = Merchant(**merchant.dict())
    db.add(db_merchant)
    db.commit()
    db.refresh(db_merchant)
    return db_merchant


@router.get("/{merchant_id}", response_model=MerchantResponse)
async def get_merchant(merchant_id: int, db: Session = Depends(get_db)):
    """Get merchant by ID"""
    merchant = db.query(Merchant).filter(Merchant.id == merchant_id).first()
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")
    return merchant


@router.put("/{merchant_id}", response_model=MerchantResponse)
async def update_merchant(merchant_id: int, merchant_update: MerchantCreate, db: Session = Depends(get_db)):
    """Update merchant information"""
    merchant = db.query(Merchant).filter(Merchant.id == merchant_id).first()
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    for field, value in merchant_update.dict().items():
        setattr(merchant, field, value)
    
    # Update completion percentage
    validation_tool = ValidationTool()
    merchant.onboarding_complete = validation_tool.calculate_onboarding_completion(merchant_update.dict())
    
    db.commit()
    db.refresh(merchant)
    return merchant


@router.post("/{merchant_id}/validate-onboarding", response_model=OnboardingValidation)
async def validate_onboarding(merchant_id: int, db: Session = Depends(get_db)):
    """Validate merchant onboarding status"""
    merchant = db.query(Merchant).filter(Merchant.id == merchant_id).first()
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    validation_tool = ValidationTool()
    merchant_dict = {
        "business_name": merchant.business_name,
        "business_type": merchant.business_type,
        "location": merchant.location,
        "product_service": merchant.product_service,
        "target_customers": merchant.target_customers,
        "marketing_goal": merchant.marketing_goal,
        "campaign_budget": merchant.campaign_budget,
        "preferred_platform": merchant.preferred_platform
    }
    
    validation = validation_tool.validate_merchant_onboarding(merchant_dict)
    
    # Update merchant completion
    merchant.onboarding_complete = validation.completion_percentage
    db.commit()
    
    return validation


@router.post("/{merchant_id}/process")
async def process_merchant_stage(merchant_id: int, stage: str, db: Session = Depends(get_db)):
    """Process merchant through the agent workflow"""
    merchant = db.query(Merchant).filter(Merchant.id == merchant_id).first()
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    merchant_dict = {
        "business_name": merchant.business_name,
        "business_type": merchant.business_type,
        "location": merchant.location,
        "product_service": merchant.product_service,
        "target_customers": merchant.target_customers,
        "marketing_goal": merchant.marketing_goal,
        "campaign_budget": merchant.campaign_budget,
        "preferred_platform": merchant.preferred_platform
    }
    
    result = await orchestrator.process_merchant_input(merchant_dict, current_stage=stage)
    
    return result
