'use client';

import { useState } from 'react';
import { Merchant, OnboardingValidation } from '@/lib/types';
import { apiClient } from '@/lib/api';

interface OnboardingFormProps {
  onComplete: (merchant: Merchant) => void;
  onCancel: () => void;
}

export default function OnboardingForm({ onComplete, onCancel }: OnboardingFormProps) {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [validation, setValidation] = useState<OnboardingValidation | null>(null);
  const [merchant, setMerchant] = useState<Partial<Merchant>>({
    business_name: '',
    business_type: '',
    location: '',
    product_service: '',
    target_customers: '',
    marketing_goal: '',
    campaign_budget: undefined,
    promotion_offer: '',
    preferred_platform: '',
  });

  const businessTypes = [
    'Retail',
    'Restaurant/Food',
    'Services',
    'E-commerce',
    'Healthcare',
    'Education',
    'Real Estate',
    'Technology',
    'Fashion/Apparel',
    'Other'
  ];

  const platforms = [
    'Instagram',
    'Facebook',
    'Google',
    'YouTube',
    'LinkedIn',
    'Twitter',
    'Multiple Platforms'
  ];

  const handleInputChange = (field: keyof Merchant, value: string | number) => {
    setMerchant(prev => ({ ...prev, [field]: value }));
  };

  const validateCurrentStep = () => {
    if (step === 1) {
      return merchant.business_name && merchant.business_type && merchant.location && merchant.product_service;
    }
    return true;
  };

  const handleNext = async () => {
    if (!validateCurrentStep()) return;

    if (step < 3) {
      setStep(step + 1);
    } else {
      await handleSubmit();
    }
  };

  const handleBack = () => {
    if (step > 1) {
      setStep(step - 1);
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      // Create merchant
      const createdMerchant = await apiClient.createMerchant(merchant as Omit<Merchant, 'id' | 'onboarding_complete' | 'created_at' | 'updated_at'>);
      
      // Validate onboarding
      const validationResult = await apiClient.validateOnboarding(createdMerchant.id!);
      setValidation(validationResult);
      
      onComplete(createdMerchant);
    } catch (error) {
      console.error('Error creating merchant:', error);
      alert('Error creating merchant. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getProgressPercentage = () => {
    return Math.round((step / 3) * 100);
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-8">
      <div className="max-w-2xl w-full">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-slate-900 mb-2">
              Merchant Onboarding
            </h1>
            <p className="text-slate-600">
              Step {step} of 3
            </p>
            {/* Progress Bar */}
            <div className="mt-4 h-2 bg-slate-200 rounded-full overflow-hidden">
              <div 
                className="h-full bg-blue-600 transition-all duration-300"
                style={{ width: `${getProgressPercentage()}%` }}
              />
            </div>
          </div>

          {/* Step 1: Basic Information */}
          {step === 1 && (
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Business Name *
                </label>
                <input
                  type="text"
                  value={merchant.business_name}
                  onChange={(e) => handleInputChange('business_name', e.target.value)}
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter your business name"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Business Type *
                </label>
                <select
                  value={merchant.business_type}
                  onChange={(e) => handleInputChange('business_type', e.target.value)}
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Select business type</option>
                  {businessTypes.map(type => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Location *
                </label>
                <input
                  type="text"
                  value={merchant.location}
                  onChange={(e) => handleInputChange('location', e.target.value)}
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="City, State"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Product/Service Description *
                </label>
                <textarea
                  value={merchant.product_service}
                  onChange={(e) => handleInputChange('product_service', e.target.value)}
                  rows={4}
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Describe what you sell or the services you offer"
                />
              </div>
            </div>
          )}

          {/* Step 2: Target & Goals */}
          {step === 2 && (
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Target Customers
                </label>
                <textarea
                  value={merchant.target_customers}
                  onChange={(e) => handleInputChange('target_customers', e.target.value)}
                  rows={3}
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Who are your ideal customers? (age range, location, interests)"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Marketing Goal
                </label>
                <textarea
                  value={merchant.marketing_goal}
                  onChange={(e) => handleInputChange('marketing_goal', e.target.value)}
                  rows={3}
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="What do you want to achieve? (brand awareness, sales, leads)"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Campaign Budget (₹)
                </label>
                <input
                  type="number"
                  value={merchant.campaign_budget || ''}
                  onChange={(e) => handleInputChange('campaign_budget', parseFloat(e.target.value) || 0)}
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter your advertising budget"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Preferred Platform
                </label>
                <select
                  value={merchant.preferred_platform}
                  onChange={(e) => handleInputChange('preferred_platform', e.target.value)}
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Select platform</option>
                  {platforms.map(platform => (
                    <option key={platform} value={platform}>{platform}</option>
                  ))}
                </select>
              </div>
            </div>
          )}

          {/* Step 3: Additional Details */}
          {step === 3 && (
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Promotion/Offer (Optional)
                </label>
                <textarea
                  value={merchant.promotion_offer}
                  onChange={(e) => handleInputChange('promotion_offer', e.target.value)}
                  rows={3}
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Any special offers or promotions you want to highlight?"
                />
              </div>

              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h3 className="font-semibold text-blue-900 mb-2">Review Your Information</h3>
                <div className="space-y-2 text-sm text-blue-800">
                  <p><strong>Business:</strong> {merchant.business_name}</p>
                  <p><strong>Type:</strong> {merchant.business_type}</p>
                  <p><strong>Location:</strong> {merchant.location}</p>
                  <p><strong>Product/Service:</strong> {merchant.product_service}</p>
                  {merchant.target_customers && <p><strong>Target:</strong> {merchant.target_customers}</p>}
                  {merchant.marketing_goal && <p><strong>Goal:</strong> {merchant.marketing_goal}</p>}
                  {merchant.campaign_budget && <p><strong>Budget:</strong> ₹{merchant.campaign_budget}</p>}
                  {merchant.preferred_platform && <p><strong>Platform:</strong> {merchant.preferred_platform}</p>}
                </div>
              </div>

              {validation && (
                <div className={`rounded-lg p-4 ${validation.is_complete ? 'bg-green-50 border border-green-200' : 'bg-yellow-50 border border-yellow-200'}`}>
                  <p className={`font-semibold ${validation.is_complete ? 'text-green-900' : 'text-yellow-900'}`}>
                    {validation.is_complete ? '✅ Onboarding Complete!' : '⚠️ Additional Information Recommended'}
                  </p>
                  <p className={`text-sm mt-1 ${validation.is_complete ? 'text-green-800' : 'text-yellow-800'}`}>
                    Completion: {validation.completion_percentage}%
                  </p>
                  {!validation.is_complete && validation.missing_fields.length > 0 && (
                    <p className="text-sm text-yellow-800 mt-2">
                      Missing: {validation.missing_fields.join(', ')}
                    </p>
                  )}
                </div>
              )}
            </div>
          )}

          {/* Navigation Buttons */}
          <div className="flex justify-between mt-8">
            <button
              onClick={onCancel}
              className="px-6 py-3 border border-slate-300 rounded-lg text-slate-700 hover:bg-slate-50 transition-colors"
            >
              Cancel
            </button>
            
            <div className="flex gap-3">
              {step > 1 && (
                <button
                  onClick={handleBack}
                  className="px-6 py-3 border border-slate-300 rounded-lg text-slate-700 hover:bg-slate-50 transition-colors"
                >
                  Back
                </button>
              )}
              <button
                onClick={handleNext}
                disabled={loading || !validateCurrentStep()}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-slate-400 disabled:cursor-not-allowed"
              >
                {loading ? 'Processing...' : step === 3 ? 'Complete Onboarding' : 'Next'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
