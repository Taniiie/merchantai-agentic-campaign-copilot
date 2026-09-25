from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import json
from app.config import settings


class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    async def generate_completion(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Generate text completion"""
        pass
    
    @abstractmethod
    async def generate_structured(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        schema: Optional[Dict[str, Any]] = None,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Generate structured output"""
        pass


class DemoAIProvider(AIProvider):
    """Demo mode provider with deterministic mock responses"""
    
    async def generate_completion(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Generate deterministic mock responses based on prompt context"""
        
        # Analyze prompt to determine context
        prompt_lower = prompt.lower()
        
        if "onboarding" in prompt_lower or "missing" in prompt_lower:
            return self._generate_onboarding_response(prompt)
        elif "campaign" in prompt_lower and "plan" in prompt_lower:
            return self._generate_campaign_plan_response(prompt)
        elif "ad copy" in prompt_lower or "copy" in prompt_lower:
            return self._generate_ad_copy_response(prompt)
        elif "creative brief" in prompt_lower or "creative" in prompt_lower:
            return self._generate_creative_brief_response(prompt)
        elif "validation" in prompt_lower or "readiness" in prompt_lower:
            return self._generate_validation_response(prompt)
        else:
            return "I understand your request. Let me help you with that."
    
    async def generate_structured(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        schema: Optional[Dict[str, Any]] = None,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Generate structured mock responses"""
        
        prompt_lower = prompt.lower()
        
        if "campaign" in prompt_lower and "plan" in prompt_lower:
            return self._generate_structured_campaign_plan(prompt)
        elif "ad copy" in prompt_lower:
            return self._generate_structured_ad_copy(prompt)
        elif "creative brief" in prompt_lower:
            return self._generate_structured_creative_brief(prompt)
        elif "validation" in prompt_lower or "readiness" in prompt_lower:
            return self._generate_structured_validation(prompt)
        else:
            return {"status": "success", "message": "Request processed"}
    
    def _generate_onboarding_response(self, prompt: str) -> str:
        """Generate onboarding validation response"""
        return """Based on the information provided, I need a few more details to complete your onboarding:

1. Target customers - Who are you trying to reach? (age range, location, interests)
2. Marketing goal - What do you want to achieve? (brand awareness, sales, leads)
3. Campaign budget - What's your advertising budget?
4. Preferred platform - Where do you want to advertise? (Instagram, Facebook, Google)

Once you provide these details, I can create a comprehensive campaign plan for you."""
    
    def _generate_campaign_plan_response(self, prompt: str) -> str:
        """Generate campaign planning response"""
        return """Based on your business information, here's my recommended campaign plan:

**Campaign Objective:** Brand Awareness & Customer Acquisition

**Target Audience:** 
- Women aged 22-40 in your local area
- Interested in fashion, ethnic wear, and festive shopping
- Lookalike audience based on your existing customers

**Budget Allocation:** 
- 60% for Instagram/Facebook ads
- 30% for Google Search ads
- 10% for retargeting

**Duration:** 4-6 weeks to build momentum and see results

**Reasoning:** Your business category benefits from visual platforms like Instagram. The demographic aligns with your target customers. A mix of awareness and conversion-focused ads will help build brand recognition while driving sales."""
    
    def _generate_ad_copy_response(self, prompt: str) -> str:
        """Generate ad copy response"""
        return """Here are the ad copy variations:

**Primary Copy:**
Transform your festive look with our exquisite ethnic wear collection. Handcrafted with love, designed for the modern woman who celebrates tradition in style.

**Headline:** Elevate Your Festive Style

**Description:** Discover our curated collection of ethnic wear - from elegant sarees to stunning lehengas. Perfect for Diwali, weddings, and special occasions.

**CTA:** Shop Now

**Variation 1:**
Make every celebration memorable with our ethnic wear. Traditional craftsmanship meets contemporary design.

**Headline:** Tradition Meets Elegance

**Description:** Explore our handpicked ethnic wear collection. Quality fabrics, intricate designs, and perfect fits for every occasion.

**CTA:** Explore Collection

**Variation 2:**
Your search for the perfect ethnic wear ends here. Premium quality, authentic designs, and unbeatable prices.

**Headline:** Festive Fashion Awaits

**Description:** From casual ethnic wear to wedding-ready ensembles, find everything you need. New arrivals added weekly.

**CTA:** Discover Now"""
    
    def _generate_creative_brief_response(self, prompt: str) -> str:
        """Generate creative brief response"""
        return """**Creative Brief:**

**Visual Concept:** Warm, inviting, and festive. Show women of different ages wearing your ethnic wear in celebratory settings.

**Scene Direction:** 
- Outdoor location with natural lighting (garden, courtyard, or festival setting)
- Candid moments of women laughing, celebrating, or posing
- Mix of close-up details (fabric, embroidery) and full-length shots

**Headline Placement:** Top third of the image, overlaid with subtle shadow for readability

**Tone:** Celebratory, elegant, inclusive, and premium

**Suggested Imagery:**
- Women in traditional festive settings
- Close-ups of fabric details and embroidery
- Product flat lays with festive props
- Lifestyle shots showing the clothing in use

**Suggested Format:** 1:1 square for Instagram, 4:5 portrait for Facebook, 16:9 for YouTube

**Key Selling Point:** Authentic ethnic wear that blends tradition with modern style"""
    
    def _generate_validation_response(self, prompt: str) -> str:
        """Generate validation response"""
        return """**Campaign Readiness Check:**

✅ Merchant Information: Complete
✅ Campaign Objective: Defined
✅ Target Audience: Specified
✅ Budget Allocation: Recommended
✅ Ad Copy: Generated
✅ Creative Brief: Created

**Status: READY**

Your campaign is ready for review and approval. All required components are in place and validated."""
    
    def _generate_structured_campaign_plan(self, prompt: str) -> Dict[str, Any]:
        """Generate structured campaign plan"""
        return {
            "objective": "Brand Awareness & Customer Acquisition",
            "target_audience": "Women aged 22-40 in local area interested in fashion and ethnic wear",
            "audience_characteristics": {
                "age_range": "22-40",
                "gender": "Female",
                "location": "Local area (within 10km)",
                "interests": ["Fashion", "Ethnic Wear", "Festive Shopping", "Weddings"],
                "behaviors": ["Engaged with fashion content", "Previous purchasers"]
            },
            "budget_allocation": {
                "instagram_facebook": 60,
                "google_search": 30,
                "retargeting": 10
            },
            "duration_days": 30,
            "reasoning": "Visual platforms like Instagram align with fashion/ethnic wear. Target demographic matches typical customers. Mixed strategy balances awareness and conversion."
        }
    
    def _generate_structured_ad_copy(self, prompt: str) -> Dict[str, Any]:
        """Generate structured ad copy"""
        return {
            "primary_copy": "Transform your festive look with our exquisite ethnic wear collection. Handcrafted with love, designed for the modern woman who celebrates tradition in style.",
            "headline": "Elevate Your Festive Style",
            "description": "Discover our curated collection of ethnic wear - from elegant sarees to stunning lehengas. Perfect for Diwali, weddings, and special occasions.",
            "cta": "Shop Now",
            "variation_1": {
                "copy": "Make every celebration memorable with our ethnic wear. Traditional craftsmanship meets contemporary design.",
                "headline": "Tradition Meets Elegance",
                "description": "Explore our handpicked ethnic wear collection. Quality fabrics, intricate designs, and perfect fits for every occasion.",
                "cta": "Explore Collection"
            },
            "variation_2": {
                "copy": "Your search for the perfect ethnic wear ends here. Premium quality, authentic designs, and unbeatable prices.",
                "headline": "Festive Fashion Awaits",
                "description": "From casual ethnic wear to wedding-ready ensembles, find everything you need. New arrivals added weekly.",
                "cta": "Discover Now"
            }
        }
    
    def _generate_structured_creative_brief(self, prompt: str) -> Dict[str, Any]:
        """Generate structured creative brief"""
        return {
            "visual_concept": "Warm, inviting, and festive. Show women of different ages wearing ethnic wear in celebratory settings.",
            "scene_direction": "Outdoor location with natural lighting. Candid moments of women celebrating. Mix of close-up details and full-length shots.",
            "headline_placement": "Top third of the image, overlaid with subtle shadow for readability",
            "tone": "Celebratory, elegant, inclusive, and premium",
            "suggested_imagery": {
                "main_scenes": [
                    "Women in traditional festive settings",
                    "Close-ups of fabric details and embroidery",
                    "Product flat lays with festive props",
                    "Lifestyle shots showing clothing in use"
                ],
                "style_notes": "Natural lighting, authentic moments, diverse models"
            },
            "suggested_format": "1:1 square for Instagram, 4:5 portrait for Facebook, 16:9 for YouTube",
            "key_selling_point": "Authentic ethnic wear that blends tradition with modern style"
        }
    
    def _generate_structured_validation(self, prompt: str) -> Dict[str, Any]:
        """Generate structured validation"""
        return {
            "is_ready": True,
            "readiness_status": "ready",
            "validated_components": [
                "merchant_information",
                "campaign_objective",
                "target_audience",
                "budget_allocation",
                "ad_copy",
                "creative_brief"
            ],
            "issues": [],
            "recommendations": [
                "Review campaign objective for alignment with business goals",
                "Test ad copy with small audience before full launch",
                "Consider A/B testing different creative variations"
            ]
        }


class OpenAIProvider(AIProvider):
    """OpenAI provider implementation"""
    
    def __init__(self):
        try:
            import openai
            self.client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
        except ImportError:
            raise ImportError("OpenAI package not installed. Install with: pip install openai")
    
    async def generate_completion(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = await self.client.chat.completions.create(
            model=settings.llm_model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
    
    async def generate_structured(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        schema: Optional[Dict[str, Any]] = None,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        if schema:
            messages.append({
                "role": "system", 
                "content": f"Respond with valid JSON matching this schema: {json.dumps(schema)}"
            })
        
        response = await self.client.chat.completions.create(
            model=settings.llm_model_name,
            messages=messages,
            temperature=temperature,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)


class AnthropicProvider(AIProvider):
    """Anthropic provider implementation"""
    
    def __init__(self):
        try:
            import anthropic
            self.client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
        except ImportError:
            raise ImportError("Anthropic package not installed. Install with: pip install anthropic")
    
    async def generate_completion(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        messages = [{"role": "user", "content": prompt}]
        
        response = await self.client.messages.create(
            model=settings.llm_model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt or "",
            messages=messages
        )
        
        return response.content[0].text
    
    async def generate_structured(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        schema: Optional[Dict[str, Any]] = None,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        full_prompt = prompt
        if schema:
            full_prompt += f"\n\nRespond with valid JSON matching this schema: {json.dumps(schema)}"
        
        messages = [{"role": "user", "content": full_prompt}]
        
        response = await self.client.messages.create(
            model=settings.llm_model_name,
            max_tokens=2000,
            temperature=temperature,
            system=system_prompt or "",
            messages=messages
        )
        
        return json.loads(response.content[0].text)


def get_ai_provider() -> AIProvider:
    """Factory function to get the configured AI provider"""
    provider_type = settings.ai_provider.lower()
    
    if provider_type == "demo":
        return DemoAIProvider()
    elif provider_type == "openai":
        return OpenAIProvider()
    elif provider_type == "anthropic":
        return AnthropicProvider()
    else:
        print(f"Unknown provider {provider_type}, falling back to demo mode")
        return DemoAIProvider()
