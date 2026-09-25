import { Merchant, OnboardingValidation, Campaign, CampaignPlan, AdCopy, CreativeBrief, ValidationResult, AgentResponse } from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  // Merchant Endpoints
  async createMerchant(merchant: Omit<Merchant, 'id' | 'onboarding_complete' | 'created_at' | 'updated_at'>): Promise<Merchant> {
    return this.request<Merchant>('/api/merchants/', {
      method: 'POST',
      body: JSON.stringify(merchant),
    });
  }

  async getMerchant(merchantId: number): Promise<Merchant> {
    return this.request<Merchant>(`/api/merchants/${merchantId}`);
  }

  async updateMerchant(merchantId: number, merchant: Omit<Merchant, 'id' | 'onboarding_complete' | 'created_at' | 'updated_at'>): Promise<Merchant> {
    return this.request<Merchant>(`/api/merchants/${merchantId}`, {
      method: 'PUT',
      body: JSON.stringify(merchant),
    });
  }

  async validateOnboarding(merchantId: number): Promise<OnboardingValidation> {
    return this.request<OnboardingValidation>(`/api/merchants/${merchantId}/validate-onboarding`, {
      method: 'POST',
    });
  }

  async processMerchantStage(merchantId: number, stage: string): Promise<AgentResponse> {
    return this.request<AgentResponse>(`/api/merchants/${merchantId}/process?stage=${stage}`, {
      method: 'POST',
    });
  }

  // Campaign Endpoints
  async createCampaign(campaign: Omit<Campaign, 'id' | 'status' | 'readiness_status' | 'created_at' | 'updated_at'>): Promise<Campaign> {
    return this.request<Campaign>('/api/campaigns/', {
      method: 'POST',
      body: JSON.stringify(campaign),
    });
  }

  async getCampaign(campaignId: number): Promise<Campaign> {
    return this.request<Campaign>(`/api/campaigns/${campaignId}`);
  }

  async planCampaign(merchantId: number): Promise<CampaignPlan> {
    return this.request<CampaignPlan>('/api/campaigns/plan', {
      method: 'POST',
      body: JSON.stringify({ merchant_id: merchantId }),
    });
  }

  async generateAdCopy(campaignId: number): Promise<AdCopy> {
    return this.request<AdCopy>(`/api/campaigns/${campaignId}/generate-ad-copy`, {
      method: 'POST',
    });
  }

  async generateCreativeBrief(campaignId: number): Promise<CreativeBrief> {
    return this.request<CreativeBrief>(`/api/campaigns/${campaignId}/generate-creative-brief`, {
      method: 'POST',
    });
  }

  async checkCampaignReadiness(campaignId: number): Promise<AgentResponse> {
    return this.request<AgentResponse>(`/api/campaigns/${campaignId}/check-readiness`, {
      method: 'POST',
    });
  }
}

export const apiClient = new ApiClient(API_BASE_URL);
