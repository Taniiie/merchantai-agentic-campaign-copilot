from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
import json
from app.database import get_db
from app.models.campaign import Campaign
from app.models.ad_copy import AdCopy
from app.models.creative_brief import CreativeBrief
from app.models.validation_issue import ValidationIssue
from app.schemas.campaign import CampaignCreate, CampaignResponse, CampaignPlanRequest, CampaignPlanResponse
from app.schemas.ad_copy import AdCopyCreate, AdCopyResponse, AdCopyGenerationRequest
from app.schemas.creative_brief import CreativeBriefCreate, CreativeBriefResponse, CreativeBriefGenerationRequest
from app.agents.orchestrator import orchestrator

router = APIRouter(prefix="/api/campaigns", tags=["campaigns"])


@router.post("/", response_model=CampaignResponse)
async def create_campaign(campaign: CampaignCreate, db: Session = Depends(get_db)):
    """Create a new campaign"""
    # Convert dict to JSON string for database storage
    campaign_data = campaign.dict()
    if isinstance(campaign_data.get('audience_characteristics'), dict):
        campaign_data['audience_characteristics'] = json.dumps(campaign_data['audience_characteristics'])
    
    db_campaign = Campaign(**campaign_data)
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign


@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """Get campaign by ID"""
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


@router.post("/plan", response_model=CampaignPlanResponse)
async def plan_campaign(request: CampaignPlanRequest, db: Session = Depends(get_db)):
    """Generate campaign plan using AI agent"""
    from app.models.merchant import Merchant
    
    merchant = db.query(Merchant).filter(Merchant.id == request.merchant_id).first()
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
    
    result = await orchestrator.process_merchant_input(merchant_dict, current_stage="campaign_planning")
    
    # Extract structured data
    campaign_plan = result.get("campaign_plan", {})
    
    # Create campaign with generated plan
    budget_alloc = campaign_plan.get("budget_allocation")
    if isinstance(budget_alloc, dict):
        budget_value = budget_alloc.get("total", merchant.campaign_budget)
    else:
        budget_value = budget_alloc if budget_alloc else merchant.campaign_budget
    
    db_campaign = Campaign(
        merchant_id=request.merchant_id,
        objective=campaign_plan.get("objective"),
        target_audience=campaign_plan.get("target_audience"),
        audience_characteristics=json.dumps(campaign_plan.get("audience_characteristics", {})),
        budget_allocation=budget_value,
        duration_days=campaign_plan.get("duration_days", 30),
        reasoning=campaign_plan.get("reasoning"),
        status="draft",
        readiness_status="needs_attention"
    )
    
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    
    return CampaignPlanResponse(
        objective=db_campaign.objective or "",
        target_audience=db_campaign.target_audience or "",
        audience_characteristics=campaign_plan.get("audience_characteristics", {}),
        budget_allocation=db_campaign.budget_allocation or 0,
        duration_days=db_campaign.duration_days or 0,
        reasoning=db_campaign.reasoning or ""
    )


@router.post("/{campaign_id}/generate-ad-copy", response_model=AdCopyResponse)
async def generate_ad_copy(campaign_id: int, db: Session = Depends(get_db)):
    """Generate ad copy using AI agent"""
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    from app.models.merchant import Merchant
    merchant = db.query(Merchant).filter(Merchant.id == campaign.merchant_id).first()
    
    merchant_dict = {
        "business_name": merchant.business_name,
        "business_type": merchant.business_type,
        "location": merchant.location,
        "product_service": merchant.product_service,
        "target_customers": merchant.target_customers,
        "marketing_goal": merchant.marketing_goal,
        "campaign_budget": merchant.campaign_budget,
        "preferred_platform": merchant.preferred_platform,
        "promotion_offer": merchant.promotion_offer
    }
    
    result = await orchestrator.process_merchant_input(merchant_dict, current_stage="ad_copy_generation")
    
    # Extract structured data
    ad_copy_data = result.get("ad_copy", {})
    
    # Create or update ad copy
    existing_ad_copy = db.query(AdCopy).filter(AdCopy.campaign_id == campaign_id).first()
    
    if existing_ad_copy:
        existing_ad_copy.primary_copy = ad_copy_data.get("primary_copy")
        existing_ad_copy.headline = ad_copy_data.get("headline")
        existing_ad_copy.description = ad_copy_data.get("description")
        existing_ad_copy.cta = ad_copy_data.get("cta")
        
        if "variation_1" in ad_copy_data:
            existing_ad_copy.variation_1_copy = ad_copy_data["variation_1"].get("copy")
            existing_ad_copy.variation_1_headline = ad_copy_data["variation_1"].get("headline")
            existing_ad_copy.variation_1_description = ad_copy_data["variation_1"].get("description")
            existing_ad_copy.variation_1_cta = ad_copy_data["variation_1"].get("cta")
        
        if "variation_2" in ad_copy_data:
            existing_ad_copy.variation_2_copy = ad_copy_data["variation_2"].get("copy")
            existing_ad_copy.variation_2_headline = ad_copy_data["variation_2"].get("headline")
            existing_ad_copy.variation_2_description = ad_copy_data["variation_2"].get("description")
            existing_ad_copy.variation_2_cta = ad_copy_data["variation_2"].get("cta")
        
        db.commit()
        db.refresh(existing_ad_copy)
        return existing_ad_copy
    else:
        db_ad_copy = AdCopy(
            campaign_id=campaign_id,
            primary_copy=ad_copy_data.get("primary_copy"),
            headline=ad_copy_data.get("headline"),
            description=ad_copy_data.get("description"),
            cta=ad_copy_data.get("cta"),
            variation_1_copy=ad_copy_data.get("variation_1", {}).get("copy"),
            variation_1_headline=ad_copy_data.get("variation_1", {}).get("headline"),
            variation_1_description=ad_copy_data.get("variation_1", {}).get("description"),
            variation_1_cta=ad_copy_data.get("variation_1", {}).get("cta"),
            variation_2_copy=ad_copy_data.get("variation_2", {}).get("copy"),
            variation_2_headline=ad_copy_data.get("variation_2", {}).get("headline"),
            variation_2_description=ad_copy_data.get("variation_2", {}).get("description"),
            variation_2_cta=ad_copy_data.get("variation_2", {}).get("cta")
        )
        db.add(db_ad_copy)
        db.commit()
        db.refresh(db_ad_copy)
        return db_ad_copy


@router.post("/{campaign_id}/generate-creative-brief", response_model=CreativeBriefResponse)
async def generate_creative_brief(campaign_id: int, db: Session = Depends(get_db)):
    """Generate creative brief using AI agent"""
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    from app.models.merchant import Merchant
    merchant = db.query(Merchant).filter(Merchant.id == campaign.merchant_id).first()
    
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
    
    result = await orchestrator.process_merchant_input(merchant_dict, current_stage="creative_brief_generation")
    
    # Extract structured data
    creative_brief_data = result.get("creative_brief", {})
    
    # Create or update creative brief
    existing_brief = db.query(CreativeBrief).filter(CreativeBrief.campaign_id == campaign_id).first()
    
    if existing_brief:
        existing_brief.visual_concept = creative_brief_data.get("visual_concept")
        existing_brief.scene_direction = creative_brief_data.get("scene_direction")
        existing_brief.headline_placement = creative_brief_data.get("headline_placement")
        existing_brief.tone = creative_brief_data.get("tone")
        imagery_data = creative_brief_data.get("suggested_imagery", [])
        if isinstance(imagery_data, dict):
            existing_brief.suggested_imagery = json.dumps(imagery_data)
        elif isinstance(imagery_data, list):
            existing_brief.suggested_imagery = json.dumps({"scenes": imagery_data})
        else:
            existing_brief.suggested_imagery = json.dumps([])
        existing_brief.suggested_format = creative_brief_data.get("suggested_format")
        existing_brief.key_selling_point = creative_brief_data.get("key_selling_point")
        
        db.commit()
        db.refresh(existing_brief)
        return existing_brief
    else:
        imagery_data = creative_brief_data.get("suggested_imagery", [])
        if isinstance(imagery_data, dict):
            imagery_json = json.dumps(imagery_data)
        elif isinstance(imagery_data, list):
            imagery_json = json.dumps({"scenes": imagery_data})
        else:
            imagery_json = json.dumps([])
            
        db_brief = CreativeBrief(
            campaign_id=campaign_id,
            visual_concept=creative_brief_data.get("visual_concept"),
            scene_direction=creative_brief_data.get("scene_direction"),
            headline_placement=creative_brief_data.get("headline_placement"),
            tone=creative_brief_data.get("tone"),
            suggested_imagery=imagery_json,
            suggested_format=creative_brief_data.get("suggested_format"),
            key_selling_point=creative_brief_data.get("key_selling_point")
        )
        db.add(db_brief)
        db.commit()
        db.refresh(db_brief)
        return db_brief


@router.post("/{campaign_id}/check-readiness")
async def check_campaign_readiness(campaign_id: int, db: Session = Depends(get_db)):
    """Check campaign readiness and validate all components"""
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Get all campaign components
    ad_copy = db.query(AdCopy).filter(AdCopy.campaign_id == campaign_id).first()
    creative_brief = db.query(CreativeBrief).filter(CreativeBrief.campaign_id == campaign_id).first()
    
    # Build campaign data for validation
    campaign_data = {
        "objective": campaign.objective,
        "target_audience": campaign.target_audience,
        "budget_allocation": campaign.budget_allocation,
        "ad_copy": {
            "primary_copy": ad_copy.primary_copy if ad_copy else None
        } if ad_copy else None,
        "creative_brief": {
            "visual_concept": creative_brief.visual_concept if creative_brief else None
        } if creative_brief else None
    }
    
    # Run validation
    result = await orchestrator.process_merchant_input(campaign_data, current_stage="readiness_check")
    
    validation = result.get("validation", {})
    
    # Update campaign status
    campaign.readiness_status = validation.get("readiness_status", "needs_attention")
    if validation.get("is_ready"):
        campaign.status = "ready"
    
    # Clear old validation issues
    db.query(ValidationIssue).filter(ValidationIssue.campaign_id == campaign_id).delete()
    
    # Create new validation issues
    for issue in validation.get("issues", []):
        db_issue = ValidationIssue(
            campaign_id=campaign_id,
            issue_type=issue.get("severity", "warning"),
            field_name=issue.get("field"),
            description=issue.get("message"),
            severity=issue.get("severity", "warning")
        )
        db.add(db_issue)
    
    db.commit()
    
    return result
