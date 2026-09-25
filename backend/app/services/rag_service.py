from typing import List, Dict, Any, Optional
import json
import os
from app.config import settings


class RAGService:
    """Simple RAG service using local knowledge base"""
    
    def __init__(self):
        self.knowledge_base_path = settings.knowledge_base_path
        self.knowledge_base = self._load_knowledge_base()
    
    def _load_knowledge_base(self) -> Dict[str, str]:
        """Load knowledge base from markdown files"""
        knowledge = {}
        
        # Ensure knowledge base directory exists
        os.makedirs(self.knowledge_base_path, exist_ok=True)
        
        # Create default knowledge base files if they don't exist
        self._create_default_knowledge_base()
        
        # Load knowledge from files
        files = os.listdir(self.knowledge_base_path)
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(self.knowledge_base_path, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    knowledge[file.replace('.md', '')] = f.read()
        
        return knowledge
    
    def _create_default_knowledge_base(self):
        """Create default knowledge base files"""
        
        # Campaign Objectives
        campaign_objectives = """# Campaign Objectives

## Brand Awareness
- Best for new businesses or product launches
- Focus on reach and impressions
- Suitable for: Fashion, lifestyle, food & beverage
- Metrics: Reach, impressions, brand recall

## Lead Generation
- Best for service-based businesses
- Focus on collecting contact information
- Suitable for: Real estate, education, professional services
- Metrics: Form submissions, cost per lead

## Sales/Conversion
- Best for e-commerce and retail
- Focus on driving purchases
- Suitable for: E-commerce, retail, D2C brands
- Metrics: Conversion rate, ROAS, cost per acquisition

## Website Traffic
- Best for content-driven businesses
- Focus on getting users to visit website
- Suitable for: Blogs, news sites, content platforms
- Metrics: Click-through rate, bounce rate, time on site

## App Install
- Best for mobile-first businesses
- Focus on getting app downloads
- Suitable for: Mobile apps, games, utilities
- Metrics: Install rate, cost per install
"""
        
        # Audience Segmentation
        audience_segmentation = """# Audience Segmentation

## Demographic Segmentation
- Age: Group by age ranges (18-24, 25-34, 35-44, 45+)
- Gender: Male, female, or all
- Location: Geographic targeting (city, region, country)
- Income: Economic segments (low, medium, high)
- Education: Educational qualification levels

## Psychographic Segmentation
- Interests: Hobbies, passions, activities
- Values: Beliefs, lifestyle preferences
- Personality: Traits, behaviors
- Life stage: Student, parent, professional, retired

## Behavioral Segmentation
- Purchase behavior: Buying patterns, frequency
- Brand loyalty: New customers vs. repeat customers
- User status: Active, inactive, potential users
- Engagement: How they interact with content

## Lookalike Audiences
- Based on existing customers
- Similar characteristics to your best customers
- Higher conversion potential
- Requires minimum customer data

## Custom Audiences
- Website visitors
- Email subscribers
- Social media engagers
- Past customers
"""
        
        # Ad Copy Best Practices
        ad_copy_principles = """# Ad Copy Best Practices

## Headline Principles
- Keep it under 25 characters for mobile
- Use power words: "Discover", "Transform", "Unlock"
- Include numbers when possible
- Address pain points or desires
- Create urgency or curiosity

## Description Principles
- Focus on benefits, not features
- Use clear, simple language
- Include social proof (reviews, testimonials)
- Add relevant hashtags
- Keep it under 125 characters for optimal display

## CTA Best Practices
- Use action verbs: "Shop Now", "Learn More", "Sign Up"
- Create urgency: "Limited Time", "Today Only"
- Be specific about what happens next
- Use first-person when appropriate
- Test different CTAs for performance

## Tone Guidelines
- Match brand voice (professional, casual, playful)
- Be authentic and transparent
- Avoid overly promotional language
- Use inclusive language
- Consider cultural context

## A/B Testing
- Test one variable at a time
- Test headlines, descriptions, CTAs separately
- Run tests for minimum 1-2 weeks
- Statistical significance requires adequate sample size
- Document learnings for future campaigns
"""
        
        # Budget Allocation
        budget_allocation = """# Budget Allocation

## Platform Allocation
- Facebook/Instagram: 40-60% (visual platforms)
- Google Search: 20-30% (intent-based)
- YouTube: 10-20% (video content)
- Display/Programmatic: 5-10% (awareness)

## Campaign Type Allocation
- Awareness campaigns: 30-40% of budget
- Consideration campaigns: 30-40% of budget
- Conversion campaigns: 20-30% of budget
- Retention campaigns: 10% of budget

## Budget Optimization
- Start with test budget (10-20% of total)
- Scale winning campaigns
- Pause underperforming ads
- Reallocate budget weekly
- Consider seasonality

## Minimum Viable Budget
- Facebook/Instagram: ₹5,000-10,000/month
- Google Search: ₹3,000-5,000/month
- Combined test: ₹10,000-15,000/month

## ROI Considerations
- Track cost per acquisition (CPA)
- Monitor return on ad spend (ROAS)
- Consider customer lifetime value (CLV)
- Factor in organic amplification
"""
        
        # Write files
        files = {
            'campaign_objectives.md': campaign_objectives,
            'audience_segmentation.md': audience_segmentation,
            'ad_copy_principles.md': ad_copy_principles,
            'budget_allocation.md': budget_allocation
        }
        
        for filename, content in files.items():
            file_path = os.path.join(self.knowledge_base_path, filename)
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
    
    def retrieve(
        self, 
        query: str, 
        top_k: int = 3,
        context: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant knowledge based on query
        For MVP, using simple keyword matching (can be upgraded to vector search)
        """
        query_lower = query.lower()
        results = []
        
        # Simple keyword matching for MVP
        for topic, content in self.knowledge_base.items():
            content_lower = content.lower()
            
            # Calculate simple relevance score
            score = 0
            query_words = query_lower.split()
            
            for word in query_words:
                if word in content_lower:
                    score += content_lower.count(word)
            
            if score > 0:
                results.append({
                    "topic": topic,
                    "content": content,
                    "score": score
                })
        
        # Sort by score and return top_k
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
    
    def get_context_for_campaign_planning(self, merchant_info: Dict[str, Any]) -> str:
        """Get relevant knowledge for campaign planning"""
        business_type = merchant_info.get("business_type", "").lower()
        marketing_goal = merchant_info.get("marketing_goal", "").lower()
        
        # Build query based on merchant info
        query = f"{business_type} {marketing_goal} campaign"
        
        relevant_docs = self.retrieve(query, top_k=2)
        
        context = "\n\n".join([
            f"## {doc['topic']}\n{doc['content']}" 
            for doc in relevant_docs
        ])
        
        return context if context else "General marketing best practices apply."
    
    def get_context_for_ad_copy(self, merchant_info: Dict[str, Any]) -> str:
        """Get relevant knowledge for ad copy generation"""
        business_type = merchant_info.get("business_type", "").lower()
        
        query = f"{business_type} ad copy principles"
        
        relevant_docs = self.retrieve(query, top_k=2)
        
        context = "\n\n".join([
            f"## {doc['topic']}\n{doc['content']}" 
            for doc in relevant_docs
        ])
        
        return context if context else "Follow general ad copy best practices."
    
    def get_context_for_creative_brief(self, merchant_info: Dict[str, Any]) -> str:
        """Get relevant knowledge for creative brief generation"""
        business_type = merchant_info.get("business_type", "").lower()
        
        query = f"{business_type} creative brief visual concept"
        
        relevant_docs = self.retrieve(query, top_k=2)
        
        context = "\n\n".join([
            f"## {doc['topic']}\n{doc['content']}" 
            for doc in relevant_docs
        ])
        
        return context if context else "Focus on visual storytelling and brand consistency."


# Singleton instance
rag_service = RAGService()
