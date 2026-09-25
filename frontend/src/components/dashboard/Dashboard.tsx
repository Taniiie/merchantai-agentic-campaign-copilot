'use client';

import { useState, useEffect } from 'react';
import { Merchant, Campaign, CampaignPlan, AdCopy, CreativeBrief, AgentResponse } from '@/lib/types';
import { apiClient } from '@/lib/api';

interface DashboardProps {
  merchant: Merchant;
  onBack: () => void;
}

export default function Dashboard({ merchant, onBack }: DashboardProps) {
  const [loading, setLoading] = useState(false);
  const [currentStage, setCurrentStage] = useState<'planning' | 'generating' | 'ready'>('planning');
  const [campaign, setCampaign] = useState<Campaign | null>(null);
  const [campaignPlan, setCampaignPlan] = useState<CampaignPlan | null>(null);
  const [adCopy, setAdCopy] = useState<AdCopy | null>(null);
  const [creativeBrief, setCreativeBrief] = useState<CreativeBrief | null>(null);
  const [readinessResult, setReadinessResult] = useState<AgentResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handlePlanCampaign = async () => {
    setLoading(true);
    setError(null);
    try {
      const plan = await apiClient.planCampaign(merchant.id!);
      setCampaignPlan(plan);
      
      // Create campaign with the plan
      const newCampaign = await apiClient.createCampaign({
        merchant_id: merchant.id!,
        objective: plan.objective,
        target_audience: plan.target_audience,
        audience_characteristics: plan.audience_characteristics,
        budget_allocation: typeof plan.budget_allocation === 'object' ? Object.values(plan.budget_allocation).reduce((a: number, b: number) => a + b, 0) : plan.budget_allocation,
        duration_days: plan.duration_days,
        reasoning: plan.reasoning
      });
      
      setCampaign(newCampaign);
      setCurrentStage('generating');
    } catch (err) {
      setError('Failed to generate campaign plan. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateAdCopy = async () => {
    if (!campaign) return;
    
    setLoading(true);
    setError(null);
    try {
      const copy = await apiClient.generateAdCopy(campaign.id!);
      setAdCopy(copy);
    } catch (err) {
      setError('Failed to generate ad copy. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateCreativeBrief = async () => {
    if (!campaign) return;
    
    setLoading(true);
    setError(null);
    try {
      const brief = await apiClient.generateCreativeBrief(campaign.id!);
      setCreativeBrief(brief);
    } catch (err) {
      setError('Failed to generate creative brief. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCheckReadiness = async () => {
    if (!campaign) return;
    
    setLoading(true);
    setError(null);
    try {
      const result = await apiClient.checkCampaignReadiness(campaign.id!);
      setReadinessResult(result);
      
      if (result.validation?.is_ready) {
        setCurrentStage('ready');
      }
    } catch (err) {
      setError('Failed to check campaign readiness. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateAll = async () => {
    setLoading(true);
    setError(null);
    try {
      // Step 1: Plan campaign and create campaign record
      const plan = await apiClient.planCampaign(merchant.id!);
      setCampaignPlan(plan);
      
      const newCampaign = await apiClient.createCampaign({
        merchant_id: merchant.id!,
        objective: plan.objective,
        target_audience: plan.target_audience,
        audience_characteristics: plan.audience_characteristics,
        budget_allocation: typeof plan.budget_allocation === 'object' ? Object.values(plan.budget_allocation).reduce((a: number, b: number) => a + b, 0) : plan.budget_allocation,
        duration_days: plan.duration_days,
        reasoning: plan.reasoning
      });
      
      setCampaign(newCampaign);
      setCurrentStage('generating');
      
      // Step 2: Generate ad copy
      const copy = await apiClient.generateAdCopy(newCampaign.id!);
      setAdCopy(copy);
      
      // Step 3: Generate creative brief
      const brief = await apiClient.generateCreativeBrief(newCampaign.id!);
      setCreativeBrief(brief);
      
      // Step 4: Check readiness
      const result = await apiClient.checkCampaignReadiness(newCampaign.id!);
      setReadinessResult(result);
      
      if (result.validation?.is_ready) {
        setCurrentStage('ready');
      }
    } catch (err) {
      console.error('Error in generate all flow:', err);
      setError('Failed to complete campaign generation. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getStageColor = (stage: string) => {
    switch (stage) {
      case 'planning': return 'bg-blue-100 text-blue-800';
      case 'generating': return 'bg-purple-100 text-purple-800';
      case 'ready': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="min-h-screen px-4 py-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">Campaign Dashboard</h1>
            <p className="text-slate-600 mt-1">{merchant.business_name}</p>
          </div>
          <button
            onClick={onBack}
            className="px-4 py-2 border border-slate-300 rounded-lg text-slate-700 hover:bg-slate-50 transition-colors"
          >
            Back to Home
          </button>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <p className="text-red-800">{error}</p>
          </div>
        )}

        {/* Stage Indicator */}
        <div className="bg-white rounded-xl shadow-md p-6 mb-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className={`px-4 py-2 rounded-full font-medium ${getStageColor(currentStage)}`}>
                {currentStage === 'planning' && 'Campaign Planning'}
                {currentStage === 'generating' && 'Generating Content'}
                {currentStage === 'ready' && 'Ready to Launch'}
              </div>
              <div className="text-slate-600">
                {currentStage === 'planning' && 'Plan your campaign strategy'}
                {currentStage === 'generating' && 'Generate ad copy and creative briefs'}
                {currentStage === 'ready' && 'Campaign is ready for review'}
              </div>
            </div>
            <div className="text-slate-500 text-sm">
              Onboarding: {merchant.onboarding_complete || 0}% complete
            </div>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Left Column - Actions */}
          <div className="lg:col-span-1 space-y-6">
            {/* Action Buttons */}
            <div className="bg-white rounded-xl shadow-md p-6">
              <h2 className="text-lg font-semibold text-slate-900 mb-4">Campaign Actions</h2>
              <div className="space-y-3">
                {!campaignPlan && (
                  <button
                    onClick={handlePlanCampaign}
                    disabled={loading}
                    className="w-full px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-slate-400"
                  >
                    {loading ? 'Planning...' : 'Plan Campaign'}
                  </button>
                )}
                
                {campaignPlan && !adCopy && (
                  <button
                    onClick={handleGenerateAdCopy}
                    disabled={loading}
                    className="w-full px-4 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors disabled:bg-slate-400"
                  >
                    {loading ? 'Generating...' : 'Generate Ad Copy'}
                  </button>
                )}
                
                {adCopy && !creativeBrief && (
                  <button
                    onClick={handleGenerateCreativeBrief}
                    disabled={loading}
                    className="w-full px-4 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors disabled:bg-slate-400"
                  >
                    {loading ? 'Generating...' : 'Generate Creative Brief'}
                  </button>
                )}
                
                {creativeBrief && !readinessResult && (
                  <button
                    onClick={handleCheckReadiness}
                    disabled={loading}
                    className="w-full px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors disabled:bg-slate-400"
                  >
                    {loading ? 'Checking...' : 'Check Readiness'}
                  </button>
                )}

                {!campaignPlan && (
                  <button
                    onClick={handleGenerateAll}
                    disabled={loading}
                    className="w-full px-4 py-3 bg-slate-800 text-white rounded-lg hover:bg-slate-900 transition-colors disabled:bg-slate-400"
                  >
                    {loading ? 'Processing...' : 'Generate All (Auto)'}
                  </button>
                )}
              </div>
            </div>

            {/* Merchant Profile */}
            <div className="bg-white rounded-xl shadow-md p-6">
              <h2 className="text-lg font-semibold text-slate-900 mb-4">Business Profile</h2>
              <div className="space-y-3 text-sm">
                <div>
                  <span className="text-slate-500">Business Type:</span>
                  <span className="ml-2 text-slate-900">{merchant.business_type}</span>
                </div>
                <div>
                  <span className="text-slate-500">Location:</span>
                  <span className="ml-2 text-slate-900">{merchant.location}</span>
                </div>
                <div>
                  <span className="text-slate-500">Product/Service:</span>
                  <span className="ml-2 text-slate-900">{merchant.product_service}</span>
                </div>
                {merchant.target_customers && (
                  <div>
                    <span className="text-slate-500">Target Customers:</span>
                    <span className="ml-2 text-slate-900">{merchant.target_customers}</span>
                  </div>
                )}
                {merchant.marketing_goal && (
                  <div>
                    <span className="text-slate-500">Marketing Goal:</span>
                    <span className="ml-2 text-slate-900">{merchant.marketing_goal}</span>
                  </div>
                )}
                {merchant.campaign_budget && (
                  <div>
                    <span className="text-slate-500">Budget:</span>
                    <span className="ml-2 text-slate-900">₹{merchant.campaign_budget}</span>
                  </div>
                )}
                {merchant.preferred_platform && (
                  <div>
                    <span className="text-slate-500">Platform:</span>
                    <span className="ml-2 text-slate-900">{merchant.preferred_platform}</span>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Right Column - Results */}
          <div className="lg:col-span-2 space-y-6">
            {/* Campaign Plan */}
            {campaignPlan && (
              <div className="bg-white rounded-xl shadow-md p-6">
                <h2 className="text-lg font-semibold text-slate-900 mb-4">Campaign Plan</h2>
                <div className="space-y-4">
                  <div>
                    <h3 className="font-medium text-slate-700 mb-1">Objective</h3>
                    <p className="text-slate-600">{campaignPlan.objective}</p>
                  </div>
                  <div>
                    <h3 className="font-medium text-slate-700 mb-1">Target Audience</h3>
                    <p className="text-slate-600">{campaignPlan.target_audience}</p>
                  </div>
                  <div>
                    <h3 className="font-medium text-slate-700 mb-1">Audience Characteristics</h3>
                    <div className="bg-slate-50 rounded-lg p-3 text-sm">
                      <pre className="text-slate-600 whitespace-pre-wrap">
                        {JSON.stringify(campaignPlan.audience_characteristics, null, 2)}
                      </pre>
                    </div>
                  </div>
                  <div>
                    <h3 className="font-medium text-slate-700 mb-1">Budget Allocation</h3>
                    <div className="bg-slate-50 rounded-lg p-3 text-sm">
                      <pre className="text-slate-600 whitespace-pre-wrap">
                        {JSON.stringify(campaignPlan.budget_allocation, null, 2)}
                      </pre>
                    </div>
                  </div>
                  <div>
                    <h3 className="font-medium text-slate-700 mb-1">Duration</h3>
                    <p className="text-slate-600">{campaignPlan.duration_days} days</p>
                  </div>
                  <div>
                    <h3 className="font-medium text-slate-700 mb-1">Reasoning</h3>
                    <p className="text-slate-600">{campaignPlan.reasoning}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Ad Copy */}
            {adCopy && (
              <div className="bg-white rounded-xl shadow-md p-6">
                <h2 className="text-lg font-semibold text-slate-900 mb-4">Ad Copy</h2>
                <div className="space-y-4">
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <h3 className="font-medium text-blue-900 mb-2">Primary Copy</h3>
                    <p className="text-blue-800 mb-2">{adCopy.headline}</p>
                    <p className="text-blue-700 text-sm">{adCopy.description}</p>
                    <p className="text-blue-900 font-medium mt-2">{adCopy.cta}</p>
                  </div>
                  
                  {adCopy.variation_1_copy && (
                    <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                      <h3 className="font-medium text-purple-900 mb-2">Variation 1</h3>
                      <p className="text-purple-800 mb-2">{adCopy.variation_1_headline}</p>
                      <p className="text-purple-700 text-sm">{adCopy.variation_1_description}</p>
                      <p className="text-purple-900 font-medium mt-2">{adCopy.variation_1_cta}</p>
                    </div>
                  )}
                  
                  {adCopy.variation_2_copy && (
                    <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                      <h3 className="font-medium text-green-900 mb-2">Variation 2</h3>
                      <p className="text-green-800 mb-2">{adCopy.variation_2_headline}</p>
                      <p className="text-green-700 text-sm">{adCopy.variation_2_description}</p>
                      <p className="text-green-900 font-medium mt-2">{adCopy.variation_2_cta}</p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Creative Brief */}
            {creativeBrief && (
              <div className="bg-white rounded-xl shadow-md p-6">
                <h2 className="text-lg font-semibold text-slate-900 mb-4">Creative Brief</h2>
                <div className="space-y-4">
                  <div>
                    <h3 className="font-medium text-slate-700 mb-1">Visual Concept</h3>
                    <p className="text-slate-600">{creativeBrief.visual_concept}</p>
                  </div>
                  <div>
                    <h3 className="font-medium text-slate-700 mb-1">Scene Direction</h3>
                    <p className="text-slate-600">{creativeBrief.scene_direction}</p>
                  </div>
                  <div>
                    <h3 className="font-medium text-slate-700 mb-1">Headline Placement</h3>
                    <p className="text-slate-600">{creativeBrief.headline_placement}</p>
                  </div>
                  <div>
                    <h3 className="font-medium text-slate-700 mb-1">Tone</h3>
                    <p className="text-slate-600">{creativeBrief.tone}</p>
                  </div>
                  <div>
                    <h3 className="font-medium text-slate-700 mb-1">Suggested Imagery</h3>
                    <div className="bg-slate-50 rounded-lg p-3 text-sm">
                      <pre className="text-slate-600 whitespace-pre-wrap">
                        {typeof creativeBrief.suggested_imagery === 'string' 
                          ? creativeBrief.suggested_imagery 
                          : JSON.stringify(creativeBrief.suggested_imagery, null, 2)}
                      </pre>
                    </div>
                  </div>
                  <div>
                    <h3 className="font-medium text-slate-700 mb-1">Suggested Format</h3>
                    <p className="text-slate-600">{creativeBrief.suggested_format}</p>
                  </div>
                  <div>
                    <h3 className="font-medium text-slate-700 mb-1">Key Selling Point</h3>
                    <p className="text-slate-600">{creativeBrief.key_selling_point}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Readiness Result */}
            {readinessResult && (
              <div className={`rounded-xl shadow-md p-6 ${readinessResult.validation?.is_ready ? 'bg-green-50 border-2 border-green-200' : 'bg-yellow-50 border-2 border-yellow-200'}`}>
                <h2 className={`text-lg font-semibold mb-4 ${readinessResult.validation?.is_ready ? 'text-green-900' : 'text-yellow-900'}`}>
                  {readinessResult.validation?.is_ready ? '✅ Campaign Ready' : '⚠️ Campaign Needs Attention'}
                </h2>
                <p className={`mb-4 ${readinessResult.validation?.is_ready ? 'text-green-800' : 'text-yellow-800'}`}>
                  {readinessResult.message}
                </p>
                
                {readinessResult.validation?.issues && readinessResult.validation.issues.length > 0 && (
                  <div className="space-y-2">
                    {readinessResult.validation.issues.map((issue, index) => (
                      <div key={index} className={`p-3 rounded-lg ${issue.severity === 'error' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'}`}>
                        <span className="font-medium">{issue.field}:</span> {issue.message}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Empty State */}
            {!campaignPlan && !adCopy && !creativeBrief && !readinessResult && (
              <div className="bg-white rounded-xl shadow-md p-12 text-center">
                <div className="text-6xl mb-4">🎯</div>
                <h3 className="text-xl font-semibold text-slate-900 mb-2">Ready to Plan Your Campaign</h3>
                <p className="text-slate-600">
                  Click "Plan Campaign" to get started with AI-powered campaign planning
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
