from typing import Dict, Any, List
from app.schemas.merchant import OnboardingValidation


class ValidationTool:
    """Tool for validating merchant information and campaign readiness"""
    
    @staticmethod
    def validate_merchant_onboarding(merchant_data: Dict[str, Any]) -> OnboardingValidation:
        """
        Validate merchant onboarding completeness
        Returns validation status with missing fields
        """
        required_fields = {
            "business_name": "Business name",
            "business_type": "Business type/category",
            "location": "Business location",
            "product_service": "Product or service description"
        }
        
        recommended_fields = {
            "target_customers": "Target customers",
            "marketing_goal": "Marketing goal",
            "campaign_budget": "Campaign budget",
            "preferred_platform": "Preferred advertising platform"
        }
        
        missing_required = []
        missing_recommended = []
        
        # Check required fields
        for field, display_name in required_fields.items():
            if not merchant_data.get(field) or str(merchant_data.get(field)).strip() == "":
                missing_required.append(display_name)
        
        # Check recommended fields
        for field, display_name in recommended_fields.items():
            if not merchant_data.get(field) or str(merchant_data.get(field)).strip() == "":
                missing_recommended.append(display_name)
        
        # Calculate completion percentage
        total_fields = len(required_fields) + len(recommended_fields)
        completed_fields = total_fields - len(missing_required) - len(missing_recommended)
        completion_percentage = int((completed_fields / total_fields) * 100)
        
        # Determine if complete
        is_complete = len(missing_required) == 0
        
        # Generate next step message
        if missing_required:
            next_step = f"Please provide: {', '.join(missing_required)}"
        elif missing_recommended:
            next_step = f"For better results, please provide: {', '.join(missing_recommended)}"
        else:
            next_step = "Onboarding complete! You can proceed to campaign planning."
        
        all_missing = missing_required + missing_recommended
        
        return OnboardingValidation(
            is_complete=is_complete,
            completion_percentage=completion_percentage,
            missing_fields=all_missing,
            next_step=next_step
        )
    
    @staticmethod
    def validate_campaign_readiness(campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate campaign readiness
        Returns validation status with specific issues
        """
        issues = []
        
        # Check campaign objective
        if not campaign_data.get("objective") or str(campaign_data.get("objective")).strip() == "":
            issues.append({
                "field": "objective",
                "severity": "error",
                "message": "Campaign objective is required"
            })
        
        # Check target audience
        if not campaign_data.get("target_audience") or str(campaign_data.get("target_audience")).strip() == "":
            issues.append({
                "field": "target_audience",
                "severity": "error",
                "message": "Target audience is required"
            })
        
        # Check budget
        if not campaign_data.get("budget_allocation"):
            issues.append({
                "field": "budget_allocation",
                "severity": "warning",
                "message": "Budget allocation is recommended"
            })
        
        # Check ad copy
        if not campaign_data.get("ad_copy") or not campaign_data.get("ad_copy").get("primary_copy"):
            issues.append({
                "field": "ad_copy",
                "severity": "error",
                "message": "Ad copy is required"
            })
        
        # Check creative brief
        if not campaign_data.get("creative_brief") or not campaign_data.get("creative_brief").get("visual_concept"):
            issues.append({
                "field": "creative_brief",
                "severity": "error",
                "message": "Creative brief is required"
            })
        
        # Determine readiness
        error_issues = [i for i in issues if i["severity"] == "error"]
        is_ready = len(error_issues) == 0
        
        return {
            "is_ready": is_ready,
            "readiness_status": "ready" if is_ready else "needs_attention",
            "issues": issues,
            "total_issues": len(issues),
            "error_count": len(error_issues),
            "warning_count": len([i for i in issues if i["severity"] == "warning"])
        }
    
    @staticmethod
    def calculate_onboarding_completion(merchant_data: Dict[str, Any]) -> int:
        """Calculate onboarding completion percentage"""
        fields = [
            "business_name",
            "business_type", 
            "location",
            "product_service",
            "target_customers",
            "marketing_goal",
            "campaign_budget",
            "preferred_platform"
        ]
        
        completed = sum(1 for field in fields if merchant_data.get(field) and str(merchant_data.get(field)).strip() != "")
        
        return int((completed / len(fields)) * 100)
