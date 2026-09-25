'use client';

import { useState } from 'react';
import OnboardingForm from '@/components/onboarding/OnboardingForm';
import Dashboard from '@/components/dashboard/Dashboard';
import { Merchant } from '@/lib/types';

type ViewState = 'landing' | 'onboarding' | 'dashboard';

export default function Home() {
  const [viewState, setViewState] = useState<ViewState>('landing');
  const [merchant, setMerchant] = useState<Merchant | null>(null);

  const handleStartOnboarding = () => {
    setViewState('onboarding');
  };

  const handleOnboardingComplete = (completedMerchant: Merchant) => {
    setMerchant(completedMerchant);
    setViewState('dashboard');
  };

  const handleBackToLanding = () => {
    setViewState('landing');
    setMerchant(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {viewState === 'landing' && (
        <LandingPage onStartOnboarding={handleStartOnboarding} />
      )}
      
      {viewState === 'onboarding' && (
        <OnboardingForm 
          onComplete={handleOnboardingComplete}
          onCancel={handleBackToLanding}
        />
      )}
      
      {viewState === 'dashboard' && merchant && (
        <Dashboard 
          merchant={merchant}
          onBack={handleBackToLanding}
        />
      )}
    </div>
  );
}

function LandingPage({ onStartOnboarding }: { onStartOnboarding: () => void }) {
  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="max-w-4xl w-full">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-slate-900 mb-4">
            MerchantAI
          </h1>
          <p className="text-xl text-slate-600 mb-2">
            Agentic SMB Marketing & Onboarding Copilot
          </p>
          <p className="text-slate-500">
            AI-powered campaign planning and creative generation for small businesses
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <h2 className="text-2xl font-semibold text-slate-800 mb-6">
            How It Works
          </h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">📝</span>
              </div>
              <h3 className="font-semibold text-slate-800 mb-2">1. Onboarding</h3>
              <p className="text-slate-600 text-sm">
                Share your business details and marketing goals
              </p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🤖</span>
              </div>
              <h3 className="font-semibold text-slate-800 mb-2">2. AI Planning</h3>
              <p className="text-slate-600 text-sm">
                Our AI agent creates your campaign strategy
              </p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🚀</span>
              </div>
              <h3 className="font-semibold text-slate-800 mb-2">3. Launch Ready</h3>
              <p className="text-slate-600 text-sm">
                Get ad copy, creative briefs, and readiness validation
              </p>
            </div>
          </div>
        </div>

        <div className="text-center">
          <button
            onClick={onStartOnboarding}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-4 px-8 rounded-lg text-lg transition-colors shadow-lg"
          >
            Get Started
          </button>
        </div>

        <div className="mt-8 text-center text-slate-500 text-sm">
          <p>Demo Mode Active - No API Key Required</p>
        </div>
      </div>
    </div>
  );
}
