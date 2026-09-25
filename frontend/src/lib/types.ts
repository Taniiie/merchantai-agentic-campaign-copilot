// Merchant Types
export interface Merchant {
  id?: number;
  business_name: string;
  business_type: string;
  location: string;
  product_service: string;
  target_customers?: string;
  marketing_goal?: string;
  campaign_budget?: number;
  promotion_offer?: string;
  preferred_platform?: string;
  onboarding_complete?: number;
  created_at?: string;
  updated_at?: string;
}

export interface OnboardingValidation {
  is_complete: boolean;
  completion_percentage: number;
  missing_fields: string[];
  next_step: string;
}

// Campaign Types
export interface Campaign {
  id?: number;
  merchant_id: number;
  objective?: string;
  target_audience?: string;
  audience_characteristics?: any;
  budget_allocation?: number;
  duration_days?: number;
  reasoning?: string;
  status?: string;
  readiness_status?: string;
  created_at?: string;
  updated_at?: string;
}

export interface CampaignPlan {
  objective: string;
  target_audience: string;
  audience_characteristics: any;
  budget_allocation: any;
  duration_days: number;
  reasoning: string;
}

// Ad Copy Types
export interface AdCopy {
  id?: number;
  campaign_id: number;
  primary_copy?: string;
  headline?: string;
  description?: string;
  cta?: string;
  variation_1_copy?: string;
  variation_1_headline?: string;
  variation_1_description?: string;
  variation_1_cta?: string;
  variation_2_copy?: string;
  variation_2_headline?: string;
  variation_2_description?: string;
  variation_2_cta?: string;
  created_at?: string;
}

// Creative Brief Types
export interface CreativeBrief {
  id?: number;
  campaign_id: number;
  visual_concept?: string;
  scene_direction?: string;
  headline_placement?: string;
  tone?: string;
  suggested_imagery?: any;
  suggested_format?: string;
  key_selling_point?: string;
  created_at?: string;
}

// Validation Types
export interface ValidationResult {
  is_ready: boolean;
  readiness_status: string;
  issues: ValidationIssue[];
  total_issues: number;
  error_count: number;
  warning_count: number;
}

export interface ValidationIssue {
  field: string;
  severity: string;
  message: string;
}

// API Response Types
export interface AgentResponse {
  stage: string;
  message: string;
  next_stage: string;
  [key: string]: any;
}
