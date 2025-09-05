import React, { useState } from 'react';
import './PricingSection.css';

const PricingSection = () => {
  const [selectedPlan, setSelectedPlan] = useState('professional');
  const [billingCycle, setBillingCycle] = useState('monthly');

  const pricingPlans = [
    {
      id: 'basic',
      name: 'Basic Report',
      price: 9.99,
      pages: '3-5 pages',
      description: 'Essential fraud investigation for quick risk assessment',
      features: [
        'Identity Verification',
        'Basic Digital Footprint Analysis',
        'Compliance Screening (Sanctions/PEP)',
        'Risk Assessment Summary',
        'PDF & HTML Export',
        '24-hour delivery',
        'Email support'
      ],
      color: '#28a745',
      popular: false,
      investigations: 'Perfect for individuals and small businesses'
    },
    {
      id: 'standard',
      name: 'Standard Report',
      price: 24.99,
      pages: '8-12 pages',
      description: 'Comprehensive analysis with detailed findings and strategic recommendations',
      features: [
        'Everything in Basic',
        'Advanced Digital Forensics',
        'Financial Intelligence Analysis',
        'Threat Assessment Matrix',
        'Strategic Recommendations',
        'All Export Formats (PDF, HTML, JSON, Word)',
        '12-hour delivery',
        'Priority email support',
        'Investigation methodology disclosure'
      ],
      color: '#007bff',
      popular: true,
      investigations: 'Ideal for business professionals and decision-makers'
    },
    {
      id: 'professional',
      name: 'Professional Report',
      price: 49.99,
      pages: '15-25 pages',
      description: 'Expert-level analysis with advanced risk modeling and detailed methodology',
      features: [
        'Everything in Standard',
        'Multi-Agent AI Investigation (8 specialized agents)',
        'Advanced Risk Modeling & Confidence Scoring',
        'Cross-Source Data Validation',
        'Detailed Evidence Chain Documentation',
        'Professional Formatting for Business Use',
        'API Integration Results (9+ data sources)',
        '6-hour delivery',
        'Phone & email support',
        'Custom investigation parameters'
      ],
      color: '#6f42c1',
      popular: false,
      investigations: 'Perfect for due diligence and risk management professionals'
    },
    {
      id: 'forensic',
      name: 'Forensic Report',
      price: 99.99,
      pages: '25-40 pages',
      description: 'Legal-grade documentation with complete evidence chain for court proceedings',
      features: [
        'Everything in Professional',
        'Legal-Grade Documentation Standards',
        'Complete Chain of Custody',
        'Expert Certification & Digital Signatures',
        'Regulatory Compliance (GDPR, CCPA)',
        'Court-Admissible Evidence Format',
        'Detailed Methodology & Source Attribution',
        'Quality Assurance Validation',
        '3-hour delivery',
        'Dedicated support specialist',
        'Expert witness consultation available'
      ],
      color: '#dc3545',
      popular: false,
      investigations: 'Essential for legal proceedings and regulatory compliance'
    }
  ];

  const handlePlanSelect = (planId) => {
    setSelectedPlan(planId);
  };

  const handleOrderNow = (plan) => {
    // In production, this would integrate with payment processor
    alert(`Starting ${plan.name} investigation for $${plan.price}. This would redirect to secure payment processing.`);
  };

  return (
    <section className="pricing-section" id="pricing">
      <div className="container">
        <div className="pricing-header">
          <h2>Professional Investigation Reports</h2>
          <p className="pricing-subtitle">
            Choose the investigation depth that matches your needs. All reports include our advanced AI analysis 
            and are delivered in multiple formats for maximum usability.
          </p>
          
          <div className="billing-toggle">
            <span className={billingCycle === 'monthly' ? 'active' : ''}>Per Investigation</span>
            <div className="toggle-switch">
              <input 
                type="checkbox" 
                id="billing-toggle"
                checked={billingCycle === 'annual'}
                onChange={(e) => setBillingCycle(e.target.checked ? 'annual' : 'monthly')}
              />
              <label htmlFor="billing-toggle"></label>
            </div>
            <span className={billingCycle === 'annual' ? 'active' : ''}>
              Bulk Packages <span className="discount-badge">Save 30%</span>
            </span>
          </div>
        </div>

        <div className="pricing-grid">
          {pricingPlans.map((plan) => (
            <div 
              key={plan.id}
              className={`pricing-card ${selectedPlan === plan.id ? 'selected' : ''} ${plan.popular ? 'popular' : ''}`}
              onClick={() => handlePlanSelect(plan.id)}
            >
              {plan.popular && <div className="popular-badge">Most Popular</div>}
              
              <div className="plan-header">
                <h3 className="plan-name">{plan.name}</h3>
                <div className="plan-price">
                  <span className="currency">$</span>
                  <span className="amount">{plan.price}</span>
                  <span className="period">per report</span>
                </div>
                <p className="plan-pages">{plan.pages}</p>
                <p className="plan-description">{plan.description}</p>
              </div>

              <div className="plan-features">
                <ul>
                  {plan.features.map((feature, index) => (
                    <li key={index}>
                      <span className="checkmark">✓</span>
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="plan-footer">
                <p className="plan-use-case">{plan.investigations}</p>
                <button 
                  className="cta-button"
                  style={{ backgroundColor: plan.color }}
                  onClick={(e) => {
                    e.stopPropagation();
                    handleOrderNow(plan);
                  }}
                >
                  Start Investigation
                </button>
              </div>
            </div>
          ))}
        </div>

        <div className="pricing-comparison">
          <h3>Why Choose ScamShield AI?</h3>
          <div className="comparison-grid">
            <div className="comparison-item">
              <div className="comparison-icon">🏢</div>
              <h4>Traditional Investigation Services</h4>
              <ul>
                <li>$500 - $5,000 per investigation</li>
                <li>2-4 weeks delivery time</li>
                <li>Limited data sources (2-3)</li>
                <li>Manual analysis prone to errors</li>
                <li>No standardized formatting</li>
              </ul>
            </div>
            <div className="comparison-item highlight">
              <div className="comparison-icon">🛡️</div>
              <h4>ScamShield AI</h4>
              <ul>
                <li>$9.99 - $99.99 per investigation</li>
                <li>3-24 hours delivery time</li>
                <li>9+ integrated data sources</li>
                <li>AI-powered multi-agent analysis</li>
                <li>Professional standardized reports</li>
              </ul>
            </div>
          </div>
          
          <div className="savings-calculator">
            <h4>Cost Savings Calculator</h4>
            <p>
              <strong>Traditional Service:</strong> $2,500 average per investigation<br/>
              <strong>ScamShield AI Professional:</strong> $49.99 per investigation<br/>
              <strong>Your Savings:</strong> <span className="savings-amount">$2,450.01 (98% cost reduction)</span>
            </p>
          </div>
        </div>

        <div className="pricing-faq">
          <h3>Frequently Asked Questions</h3>
          <div className="faq-grid">
            <div className="faq-item">
              <h4>What formats do I receive?</h4>
              <p>All reports include PDF and HTML formats. Standard tier and above also include JSON (for API integration) and Word (for editing) formats.</p>
            </div>
            <div className="faq-item">
              <h4>How quickly will I receive my report?</h4>
              <p>Delivery times range from 3 hours (Forensic) to 24 hours (Basic). Most Professional reports are delivered within 6 hours.</p>
            </div>
            <div className="faq-item">
              <h4>Are the reports legally admissible?</h4>
              <p>Professional and Forensic reports are formatted to legal standards. Forensic reports include complete chain of custody documentation suitable for court proceedings.</p>
            </div>
            <div className="faq-item">
              <h4>What data sources do you use?</h4>
              <p>We integrate 9+ premium data sources including sanctions databases, financial intelligence, domain analysis, and threat intelligence feeds.</p>
            </div>
            <div className="faq-item">
              <h4>Can I customize the investigation?</h4>
              <p>Professional and Forensic tiers allow custom investigation parameters. Contact our support team to discuss specific requirements.</p>
            </div>
            <div className="faq-item">
              <h4>Do you offer bulk discounts?</h4>
              <p>Yes! Bulk packages offer 30% savings for organizations conducting multiple investigations. Contact sales for enterprise pricing.</p>
            </div>
          </div>
        </div>

        <div className="pricing-cta">
          <h3>Ready to Start Your Investigation?</h3>
          <p>Join thousands of professionals who trust ScamShield AI for accurate, fast, and affordable fraud investigations.</p>
          <div className="cta-buttons">
            <button className="cta-primary">Start Free Trial</button>
            <button className="cta-secondary">Schedule Demo</button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default PricingSection;

