from typing import Dict, Any, Optional
from app.services.ai_provider import get_ai_provider
from app.services.rag_service import rag_service
from app.tools.validation import ValidationTool


class AgentOrchestrator:
    """
    Main orchestrator that coordinates between different agents and tools.
    Implements a simple state machine to decide which agent/tool to use.
    """
    
    def __init__(self):
        self.ai_provider = get_ai_provider()
        self.validation_tool = ValidationTool()
        self.rag_service = rag_service
    
    async def process_merchant_input(
        self, 
        merchant_data: Dict[str, Any],
        current_stage: str = "onboarding"
    ) -> Dict[str, Any]:
        """
        Process merchant input through the appropriate workflow stage
        """
        if current_stage == "onboarding":
            return await self._handle_onboarding(merchant_data)
        elif current_stage == "campaign_planning":
            return await self._handle_campaign_planning(merchant_data)
        elif current_stage == "ad_copy_generation":
            return await self._handle_ad_copy_generation(merchant_data)
        elif current_stage == "creative_brief_generation":
            return await self._handle_creative_brief_generation(merchant_data)
        elif current_stage == "readiness_check":
            return await self._handle_readiness_check(merchant_data)
        else:
            return {"error": f"Unknown stage: {current_stage}"}
    
    async def _handle_onboarding(self, merchant_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle onboarding validation and guidance"""
        # Validate onboarding completeness
        validation = self.validation_tool.validate_merchant_onboarding(merchant_data)
        
        # Calculate completion percentage
        completion = self.validation_tool.calculate_onboarding_completion(merchant_data)
        
        # Generate guidance message
        if validation.is_complete:
            message = "✅ Onboarding complete! You can now proceed to campaign planning."
            next_stage = "campaign_planning"
        else:
            message = f"⚠️ Onboarding progress: {validation.completion_percentage}%\n\n"
            message += f"Missing information: {', '.join(validation.missing_fields)}\n\n"
            message += f"Next step: {validation.next_step}"
            next_stage = "onboarding"
        
        return {
            "stage": "onboarding",
            "validation": validation.dict(),
            "completion_percentage": completion,
            "message": message,
            "next_stage": next_stage,
            "merchant_data": merchant_data
        }
    
    async def _handle_campaign_planning(self, merchant_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle campaign planning with RAG context"""
        # Get RAG context
        rag_context = self.rag_service.get_context_for_campaign_planning(merchant_data)
        
        # Build prompt for campaign planning
        prompt = self._build_campaign_planning_prompt(merchant_data, rag_context)
        
        # Generate campaign plan
        system_prompt = "You are an expert digital marketing strategist. Create comprehensive campaign plans for small businesses."
        
        try:
            # Try structured generation first
            campaign_plan = await self.ai_provider.generate_structured(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.7
            )
        except Exception as e:
            # Fallback to text generation
            text_response = await self.ai_provider.generate_completion(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.7
            )
            campaign_plan = {"text_response": text_response}
        
        return {
            "stage": "campaign_planning",
            "campaign_plan": campaign_plan,
            "message": "Campaign plan generated successfully. Next: Generate ad copy.",
            "next_stage": "ad_copy_generation"
        }
    
    async def _handle_ad_copy_generation(self, merchant_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle ad copy generation with RAG context"""
        # Get RAG context
        rag_context = self.rag_service.get_context_for_ad_copy(merchant_data)
        
        # Build prompt for ad copy generation
        prompt = self._build_ad_copy_prompt(merchant_data, rag_context)
        
        # Generate ad copy
        system_prompt = "You are an expert copywriter specializing in digital advertising. Create compelling ad copy that drives action."
        
        try:
            # Try structured generation first
            ad_copy = await self.ai_provider.generate_structured(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.8
            )
        except Exception as e:
            # Fallback to text generation
            text_response = await self.ai_provider.generate_completion(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.8
            )
            ad_copy = {"text_response": text_response}
        
        return {
            "stage": "ad_copy_generation",
            "ad_copy": ad_copy,
            "message": "Ad copy generated successfully. Next: Generate creative brief.",
            "next_stage": "creative_brief_generation"
        }
    
    async def _handle_creative_brief_generation(self, merchant_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle creative brief generation with RAG context"""
        # Get RAG context
        rag_context = self.rag_service.get_context_for_creative_brief(merchant_data)
        
        # Build prompt for creative brief generation
        prompt = self._build_creative_brief_prompt(merchant_data, rag_context)
        
        # Generate creative brief
        system_prompt = "You are an expert creative director. Create detailed creative briefs that guide visual content creation."
        
        try:
            # Try structured generation first
            creative_brief = await self.ai_provider.generate_structured(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.7
            )
        except Exception as e:
            # Fallback to text generation
            text_response = await self.ai_provider.generate_completion(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.7
            )
            creative_brief = {"text_response": text_response}
        
        return {
            "stage": "creative_brief_generation",
            "creative_brief": creative_brief,
            "message": "Creative brief generated successfully. Next: Check campaign readiness.",
            "next_stage": "readiness_check"
        }
    
    async def _handle_readiness_check(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle campaign readiness validation"""
        # Validate campaign readiness
        validation = self.validation_tool.validate_campaign_readiness(campaign_data)
        
        # Generate message
        if validation["is_ready"]:
            message = "✅ Campaign is READY for review and approval!\n\nAll components have been validated."
        else:
            message = f"⚠️ Campaign needs attention ({validation['total_issues']} issues)\n\n"
            for issue in validation["issues"]:
                icon = "❌" if issue["severity"] == "error" else "⚠️"
                message += f"{icon} {issue['field']}: {issue['message']}\n"
        
        return {
            "stage": "readiness_check",
            "validation": validation,
            "message": message,
            "next_stage": "complete" if validation["is_ready"] else "ready_check"
        }
    
    def _build_campaign_planning_prompt(self, merchant_data: Dict[str, Any], rag_context: str) -> str:
        """Build prompt for campaign planning"""
        prompt = f"""Create a comprehensive digital marketing campaign plan for this business:

Business Information:
- Business Name: {merchant_data.get('business_name', 'Not specified')}
- Business Type: {merchant_data.get('business_type', 'Not specified')}
- Location: {merchant_data.get('location', 'Not specified')}
- Product/Service: {merchant_data.get('product_service', 'Not specified')}
- Target Customers: {merchant_data.get('target_customers', 'Not specified')}
- Marketing Goal: {merchant_data.get('marketing_goal', 'Not specified')}
- Campaign Budget: {merchant_data.get('campaign_budget', 'Not specified')}
- Preferred Platform: {merchant_data.get('preferred_platform', 'Not specified')}

Marketing Guidance (from knowledge base):
{rag_context}

Please provide:
1. Campaign objective (specific, measurable goal)
2. Target audience (detailed demographic and psychographic profile)
3. Audience characteristics (age range, gender, location, interests, behaviors)
4. Budget allocation (percentage breakdown by platform/campaign type)
5. Campaign duration (recommended number of days/weeks)
6. Reasoning (explain why these recommendations)

Return as JSON with these fields: objective, target_audience, audience_characteristics (as object), budget_allocation (as object), duration_days, reasoning."""
        
        return prompt
    
    def _build_ad_copy_prompt(self, merchant_data: Dict[str, Any], rag_context: str) -> str:
        """Build prompt for ad copy generation"""
        prompt = f"""Create compelling ad copy for this business:

Business Information:
- Business Name: {merchant_data.get('business_name', 'Not specified')}
- Business Type: {merchant_data.get('business_type', 'Not specified')}
- Product/Service: {merchant_data.get('product_service', 'Not specified')}
- Target Customers: {merchant_data.get('target_customers', 'Not specified')}
- Marketing Goal: {merchant_data.get('marketing_goal', 'Not specified')}
- Promotion/Offer: {merchant_data.get('promotion_offer', 'Not specified')}

Copywriting Guidance (from knowledge base):
{rag_context}

Please provide:
1. Primary ad copy (main body text)
2. Headline (catchy, under 25 characters)
3. Description (benefit-focused, under 125 characters)
4. CTA (call-to-action)
5. Variation 1 (alternative copy with headline, description, CTA)
6. Variation 2 (second alternative with headline, description, CTA)

Return as JSON with these fields: primary_copy, headline, description, cta, variation_1 (object with copy, headline, description, cta), variation_2 (object with copy, headline, description, cta)."""
        
        return prompt
    
    def _build_creative_brief_prompt(self, merchant_data: Dict[str, Any], rag_context: str) -> str:
        """Build prompt for creative brief generation"""
        prompt = f"""Create a detailed creative brief for this business:

Business Information:
- Business Name: {merchant_data.get('business_name', 'Not specified')}
- Business Type: {merchant_data.get('business_type', 'Not specified')}
- Product/Service: {merchant_data.get('product_service', 'Not specified')}
- Target Customers: {merchant_data.get('target_customers', 'Not specified')}
- Preferred Platform: {merchant_data.get('preferred_platform', 'Not specified')}

Creative Guidance (from knowledge base):
{rag_context}

Please provide:
1. Visual concept (overall creative direction)
2. Scene direction (what should be shown, setting, mood)
3. Headline placement (where text should appear)
4. Tone (emotional feel of the creative)
5. Suggested imagery (specific visual elements, as array)
6. Suggested format (aspect ratios, platform-specific)
7. Key selling point (main message to convey)

Return as JSON with these fields: visual_concept, scene_direction, headline_placement, tone, suggested_imagery (as array), suggested_format, key_selling_point."""
        
        return prompt


# Singleton instance
orchestrator = AgentOrchestrator()
