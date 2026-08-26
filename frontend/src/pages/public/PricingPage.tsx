import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Check } from 'lucide-react';
import './PricingPage.css';

export const PricingPage: React.FC = () => {
  const navigate = useNavigate();
  const [annual, setAnnual] = useState<boolean>(false);
  const [selectedPlan, setSelectedPlan] = useState<'free' | 'pro' | 'enterprise'>('pro');
  const [hoveredPlan, setHoveredPlan] = useState<'free' | 'pro' | 'enterprise' | null>(null);

  const activePlan = hoveredPlan || selectedPlan;

  return (
    <div className="pricing-page-wrapper">
      <div className="pricing-container">
        {/* ── Header ───────────────────────────────────────────────────────── */}
        <div className="pricing-header">
          <h1>Simple and Affordable Pricing Plans</h1>
          <p>
            Start tracking and improving your finance management
          </p>

          {/* Segmented Billing Toggle */}
          <div className="pricing-toggle-wrapper">
            <button
              type="button"
              onClick={() => setAnnual(false)}
              className={`pricing-toggle-btn ${!annual ? 'active' : ''}`}
            >
              Monthly
            </button>
            <button
              type="button"
              onClick={() => setAnnual(true)}
              className={`pricing-toggle-btn ${annual ? 'active' : ''}`}
            >
              Annual
              <span className="pricing-save-badge">Save 20%</span>
            </button>
          </div>
        </div>

        {/* ── 3-Column Finament Glassmorphic Grid (Dynamic Active Selection) ── */}
        <div className="pricing-grid">
          {/* Card 1: Free */}
          <div
            className={`finament-card ${activePlan === 'free' ? 'active' : ''}`}
            onMouseEnter={() => setHoveredPlan('free')}
            onMouseLeave={() => setHoveredPlan(null)}
            onClick={() => setSelectedPlan('free')}
          >
            <div className="finament-card-header">
              <span className="finament-title">Free</span>
            </div>

            <div className="finament-price-block">
              <span className="finament-price">$0,00</span>
              <span className="finament-period">/month</span>
            </div>

            <div className="finament-desc">
              Great for trying out FinGuard and for tiny teams
            </div>

            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                navigate('/signup');
              }}
              className={activePlan === 'free' ? 'finament-btn-featured' : 'finament-btn-neutral'}
            >
              Start for Free
            </button>

            <div className="finament-divider">
              <span className="finament-divider-line" />
              <span className="finament-divider-label">FEATURES</span>
              <span className="finament-divider-line" />
            </div>

            <div className="finament-features">
              <div className="finament-feature-row">
                <span className="finament-check-icon">
                  <Check size={11} strokeWidth={3} />
                </span>
                <span>Account Aggregation</span>
              </div>
              <div className="finament-feature-row">
                <span className="finament-check-icon">
                  <Check size={11} strokeWidth={3} />
                </span>
                <span>Expense Tracking</span>
              </div>
              <div className="finament-feature-row">
                <span className="finament-check-icon">
                  <Check size={11} strokeWidth={3} />
                </span>
                <span>Budgeting Tools</span>
              </div>
              <div className="finament-feature-row">
                <span className="finament-check-icon">
                  <Check size={11} strokeWidth={3} />
                </span>
                <span>Transaction Insights</span>
              </div>
              <div className="finament-feature-row">
                <span className="finament-check-icon">
                  <Check size={11} strokeWidth={3} />
                </span>
                <span>Basic Security</span>
              </div>
            </div>
          </div>

          {/* Card 2: Professional */}
          <div
            className={`finament-card ${activePlan === 'pro' ? 'active' : ''}`}
            onMouseEnter={() => setHoveredPlan('pro')}
            onMouseLeave={() => setHoveredPlan(null)}
            onClick={() => setSelectedPlan('pro')}
          >
            <div className="finament-card-header">
              <span className="finament-title">Professional</span>
              <span className="finament-popular-badge">Most Popular</span>
            </div>

            <div className="finament-price-block">
              <span className="finament-price">{annual ? '$78,00' : '$98,00'}</span>
              <span className="finament-period">/month</span>
            </div>

            <div className="finament-desc">
              Best for growing startups and growth companies
            </div>

            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                navigate('/signup');
              }}
              className={activePlan === 'pro' ? 'finament-btn-featured' : 'finament-btn-neutral'}
            >
              Sign Up with Professional
            </button>

            <div className="finament-divider">
              <span className="finament-divider-line" />
              <span className="finament-divider-label">FEATURES</span>
              <span className="finament-divider-line" />
            </div>

            <div className="finament-features">
              <div className="finament-feature-row">
                <span className="finament-check-icon">
                  <Check size={11} strokeWidth={3} />
                </span>
                <span>Everything in Free</span>
              </div>
              <div className="finament-feature-row">
                <span className="finament-check-icon">
                  <Check size={11} strokeWidth={3} />
                </span>
                <span>Customizable Dashboards</span>
              </div>
              <div className="finament-feature-row">
                <span className="finament-check-icon">
                  <Check size={11} strokeWidth={3} />
                </span>
                <span>Advanced Budgeting</span>
              </div>
              <div className="finament-feature-row">
                <span className="finament-check-icon">
                  <Check size={11} strokeWidth={3} />
                </span>
                <span>Investment Tracking</span>
              </div>
              <div className="finament-feature-row">
                <span className="finament-check-icon">
                  <Check size={11} strokeWidth={3} />
                </span>
                <span>Enhanced Security</span>
              </div>
            </div>
          </div>

          {/* Card 3: Enterprise */}
          <div
            className={`finament-card ${activePlan === 'enterprise' ? 'active' : ''}`}
            onMouseEnter={() => setHoveredPlan('enterprise')}
            onMouseLeave={() => setHoveredPlan(null)}
            onClick={() => setSelectedPlan('enterprise')}
          >
            <div className="finament-card-header">
              <span className="finament-title">Enterprise</span>
            </div>

            <div className="finament-price-block">
              <span className="finament-price">{annual ? '$128,00' : '$160,00'}</span>
              <span className="finament-period">/month</span>
            </div>

            <div className="finament-desc">
              Best for large companies and teams requiring high security
            </div>

            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                navigate('/signup');
              }}
              className={activePlan === 'enterprise' ? 'finament-btn-featured' : 'finament-btn-neutral'}
            >
              Sign Up with Enterprise
            </button>

            <div className="finament-divider">
              <span className="finament-divider-line" />
              <span className="finament-divider-label">FEATURES</span>
              <span className="finament-divider-line" />
            </div>

            <div className="finament-features">
              <div className="finament-feature-row">
                <span className="finament-check-icon">
                  <Check size={11} strokeWidth={3} />
                </span>
                <span>Financial Planning Tools</span>
              </div>
              <div className="finament-feature-row">
                <span className="finament-check-icon">
                  <Check size={11} strokeWidth={3} />
                </span>
                <span>Priority Support</span>
              </div>
              <div className="finament-feature-row">
                <span className="finament-check-icon">
                  <Check size={11} strokeWidth={3} />
                </span>
                <span>Premium Widgets</span>
              </div>
              <div className="finament-feature-row">
                <span className="finament-check-icon">
                  <Check size={11} strokeWidth={3} />
                </span>
                <span>Advanced Security</span>
              </div>
              <div className="finament-feature-row">
                <span className="finament-check-icon">
                  <Check size={11} strokeWidth={3} />
                </span>
                <span>Integration with 3rd-Party Services</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
