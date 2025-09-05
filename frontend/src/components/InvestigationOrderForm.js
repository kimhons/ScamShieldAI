import React, { useState, useEffect } from 'react';
import './InvestigationOrderForm.css';

const InvestigationOrderForm = () => {
  const [formData, setFormData] = useState({
    subject: '',
    investigation_type: 'comprehensive',
    report_tier: 'professional',
    customer_email: '',
    customer_name: '',
    urgency: 'standard',
    special_instructions: ''
  });
  
  const [quote, setQuote] = useState(null);
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(1); // 1: Form, 2: Quote, 3: Payment, 4: Confirmation

  const investigationTypes = {
    domain: {
      name: 'Domain/Website Investigation',
      description: 'Comprehensive analysis of suspicious websites and domains',
      icon: '🌐',
      examples: 'suspicious-site.com, phishing-bank.net'
    },
    email: {
      name: 'Email Investigation',
      description: 'Advanced email header and content analysis for fraud detection',
      icon: '📧',
      examples: 'suspicious@domain.com, phishing email headers'
    },
    person: {
      name: 'Background Check',
      description: 'Professional background verification and identity analysis',
      icon: '👤',
      examples: 'John Doe, suspicious individual name'
    },
    company: {
      name: 'Business Investigation',
      description: 'Corporate due diligence and business verification',
      icon: '🏢',
      examples: 'Suspicious Corp LLC, fake business name'
    },
    crypto: {
      name: 'Cryptocurrency Investigation',
      description: 'Blockchain analysis and cryptocurrency compliance screening',
      icon: '₿',
      examples: 'Bitcoin address, Ethereum wallet'
    },
    comprehensive: {
      name: 'Comprehensive Investigation',
      description: 'Full multi-source investigation using all available methods',
      icon: '🔍',
      examples: 'Any suspicious entity requiring full analysis'
    }
  };

  const reportTiers = {
    basic: {
      name: 'Basic Report',
      price: 9.99,
      delivery: '24 hours',
      description: 'Essential fraud investigation for quick risk assessment'
    },
    standard: {
      name: 'Standard Report',
      price: 24.99,
      delivery: '12 hours',
      description: 'Comprehensive analysis with detailed findings'
    },
    professional: {
      name: 'Professional Report',
      price: 49.99,
      delivery: '6 hours',
      description: 'Expert-level analysis with advanced risk modeling'
    },
    forensic: {
      name: 'Forensic Report',
      price: 99.99,
      delivery: '3 hours',
      description: 'Legal-grade documentation for court proceedings'
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const generateQuote = async () => {
    setLoading(true);
    try {
      // In production, this would call the actual API
      const mockQuote = {
        quote_id: 'QT-' + Math.random().toString(36).substr(2, 9).toUpperCase(),
        subject: formData.subject,
        investigation_type: investigationTypes[formData.investigation_type],
        report_tier: reportTiers[formData.report_tier],
        total_price: reportTiers[formData.report_tier].price,
        estimated_delivery: reportTiers[formData.report_tier].delivery,
        valid_until: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
        includes: getIncludedFeatures(formData.report_tier),
        urgency_fee: formData.urgency === 'rush' ? reportTiers[formData.report_tier].price * 0.5 : 0
      };
      
      if (formData.urgency === 'rush') {
        mockQuote.total_price += mockQuote.urgency_fee;
        mockQuote.estimated_delivery = getUrgentDelivery(formData.report_tier);
      }
      
      setQuote(mockQuote);
      setStep(2);
    } catch (error) {
      console.error('Error generating quote:', error);
      alert('Error generating quote. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getIncludedFeatures = (tier) => {
    const features = {
      basic: [
        'Identity Verification',
        'Basic Digital Footprint Analysis',
        'Compliance Screening',
        'PDF & HTML Export'
      ],
      standard: [
        'Everything in Basic',
        'Advanced Digital Forensics',
        'Financial Intelligence Analysis',
        'All Export Formats',
        'Priority Support'
      ],
      professional: [
        'Everything in Standard',
        'Multi-Agent AI Investigation',
        'Advanced Risk Modeling',
        'Professional Formatting',
        'Phone Support'
      ],
      forensic: [
        'Everything in Professional',
        'Legal-Grade Documentation',
        'Expert Certification',
        'Court-Admissible Format',
        'Dedicated Specialist'
      ]
    };
    return features[tier] || features.basic;
  };

  const getUrgentDelivery = (tier) => {
    const urgentTimes = {
      basic: '12 hours',
      standard: '6 hours',
      professional: '3 hours',
      forensic: '90 minutes'
    };
    return urgentTimes[tier] || '12 hours';
  };

  const proceedToPayment = () => {
    setStep(3);
    // In production, this would integrate with Stripe/PayPal
    setTimeout(() => {
      setStep(4);
    }, 2000);
  };

  const validateForm = () => {
    return formData.subject && formData.customer_email && formData.customer_name;
  };

  if (step === 4) {
    return (
      <div className="order-form-container">
        <div className="confirmation-screen">
          <div className="success-icon">✅</div>
          <h2>Investigation Order Confirmed!</h2>
          <div className="confirmation-details">
            <p><strong>Order ID:</strong> {quote?.quote_id}</p>
            <p><strong>Subject:</strong> {formData.subject}</p>
            <p><strong>Report Type:</strong> {quote?.report_tier.name}</p>
            <p><strong>Total Paid:</strong> ${quote?.total_price}</p>
            <p><strong>Estimated Delivery:</strong> {quote?.estimated_delivery}</p>
          </div>
          <div className="next-steps">
            <h3>What happens next?</h3>
            <ul>
              <li>Our AI agents will begin investigating immediately</li>
              <li>You'll receive progress updates via email</li>
              <li>Your professional report will be delivered within {quote?.estimated_delivery}</li>
              <li>All reports include our 30-day money-back guarantee</li>
            </ul>
          </div>
          <button 
            className="track-button"
            onClick={() => window.location.href = '/track'}
          >
            Track Investigation Progress
          </button>
        </div>
      </div>
    );
  }

  if (step === 3) {
    return (
      <div className="order-form-container">
        <div className="payment-screen">
          <h2>Secure Payment</h2>
          <div className="payment-summary">
            <div className="summary-item">
              <span>Investigation:</span>
              <span>{formData.subject}</span>
            </div>
            <div className="summary-item">
              <span>Report Type:</span>
              <span>{quote?.report_tier.name}</span>
            </div>
            <div className="summary-item">
              <span>Base Price:</span>
              <span>${reportTiers[formData.report_tier].price}</span>
            </div>
            {formData.urgency === 'rush' && (
              <div className="summary-item">
                <span>Rush Fee (50%):</span>
                <span>${quote?.urgency_fee}</span>
              </div>
            )}
            <div className="summary-item total">
              <span>Total:</span>
              <span>${quote?.total_price}</span>
            </div>
          </div>
          
          <div className="payment-methods">
            <div className="payment-method active">
              <span className="icon">💳</span>
              <span>Credit Card</span>
            </div>
            <div className="payment-method">
              <span className="icon">🅿️</span>
              <span>PayPal</span>
            </div>
          </div>
          
          <div className="payment-form">
            <div className="form-group">
              <label>Card Number</label>
              <input type="text" placeholder="1234 5678 9012 3456" />
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Expiry</label>
                <input type="text" placeholder="MM/YY" />
              </div>
              <div className="form-group">
                <label>CVC</label>
                <input type="text" placeholder="123" />
              </div>
            </div>
          </div>
          
          <button 
            className="pay-button"
            onClick={proceedToPayment}
          >
            Pay ${quote?.total_price} Securely
          </button>
          
          <div className="security-badges">
            <span>🔒 256-bit SSL Encryption</span>
            <span>🛡️ PCI DSS Compliant</span>
            <span>💰 30-day Money Back Guarantee</span>
          </div>
        </div>
      </div>
    );
  }

  if (step === 2) {
    return (
      <div className="order-form-container">
        <div className="quote-screen">
          <h2>Investigation Quote</h2>
          <div className="quote-details">
            <div className="quote-header">
              <div className="quote-id">Quote #{quote?.quote_id}</div>
              <div className="valid-until">Valid until: {new Date(quote?.valid_until).toLocaleDateString()}</div>
            </div>
            
            <div className="investigation-summary">
              <h3>Investigation Details</h3>
              <div className="summary-grid">
                <div className="summary-item">
                  <span className="label">Subject:</span>
                  <span className="value">{formData.subject}</span>
                </div>
                <div className="summary-item">
                  <span className="label">Type:</span>
                  <span className="value">{quote?.investigation_type.name}</span>
                </div>
                <div className="summary-item">
                  <span className="label">Report Tier:</span>
                  <span className="value">{quote?.report_tier.name}</span>
                </div>
                <div className="summary-item">
                  <span className="label">Delivery:</span>
                  <span className="value">{quote?.estimated_delivery}</span>
                </div>
              </div>
            </div>
            
            <div className="included-features">
              <h3>What's Included</h3>
              <ul>
                {quote?.includes.map((feature, index) => (
                  <li key={index}>{feature}</li>
                ))}
              </ul>
            </div>
            
            <div className="pricing-breakdown">
              <div className="price-item">
                <span>Base Price:</span>
                <span>${reportTiers[formData.report_tier].price}</span>
              </div>
              {formData.urgency === 'rush' && (
                <div className="price-item">
                  <span>Rush Processing (50%):</span>
                  <span>${quote?.urgency_fee}</span>
                </div>
              )}
              <div className="price-item total">
                <span>Total:</span>
                <span>${quote?.total_price}</span>
              </div>
            </div>
            
            <div className="quote-actions">
              <button 
                className="back-button"
                onClick={() => setStep(1)}
              >
                ← Modify Order
              </button>
              <button 
                className="proceed-button"
                onClick={proceedToPayment}
              >
                Proceed to Payment →
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="order-form-container">
      <div className="order-form">
        <div className="form-header">
          <h2>Order Professional Investigation</h2>
          <p>Get expert fraud investigation results in hours, not weeks</p>
        </div>

        <form onSubmit={(e) => { e.preventDefault(); generateQuote(); }}>
          {/* Investigation Subject */}
          <div className="form-section">
            <h3>What would you like to investigate?</h3>
            <div className="form-group">
              <label htmlFor="subject">Investigation Subject *</label>
              <input
                type="text"
                id="subject"
                name="subject"
                value={formData.subject}
                onChange={handleInputChange}
                placeholder="Enter domain, email, person name, company, etc."
                required
              />
              <div className="help-text">
                Examples: suspicious-site.com, john.doe@email.com, "Fake Company LLC"
              </div>
            </div>
          </div>

          {/* Investigation Type */}
          <div className="form-section">
            <h3>Investigation Type</h3>
            <div className="investigation-types">
              {Object.entries(investigationTypes).map(([key, type]) => (
                <div 
                  key={key}
                  className={`investigation-type ${formData.investigation_type === key ? 'selected' : ''}`}
                  onClick={() => setFormData(prev => ({ ...prev, investigation_type: key }))}
                >
                  <div className="type-icon">{type.icon}</div>
                  <div className="type-content">
                    <h4>{type.name}</h4>
                    <p>{type.description}</p>
                    <div className="examples">Examples: {type.examples}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Report Tier */}
          <div className="form-section">
            <h3>Report Tier</h3>
            <div className="report-tiers">
              {Object.entries(reportTiers).map(([key, tier]) => (
                <div 
                  key={key}
                  className={`report-tier ${formData.report_tier === key ? 'selected' : ''} ${key === 'professional' ? 'recommended' : ''}`}
                  onClick={() => setFormData(prev => ({ ...prev, report_tier: key }))}
                >
                  {key === 'professional' && <div className="recommended-badge">Recommended</div>}
                  <h4>{tier.name}</h4>
                  <div className="tier-price">${tier.price}</div>
                  <div className="tier-delivery">{tier.delivery}</div>
                  <p>{tier.description}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Customer Information */}
          <div className="form-section">
            <h3>Contact Information</h3>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="customer_name">Full Name *</label>
                <input
                  type="text"
                  id="customer_name"
                  name="customer_name"
                  value={formData.customer_name}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="customer_email">Email Address *</label>
                <input
                  type="email"
                  id="customer_email"
                  name="customer_email"
                  value={formData.customer_email}
                  onChange={handleInputChange}
                  required
                />
              </div>
            </div>
          </div>

          {/* Urgency */}
          <div className="form-section">
            <h3>Delivery Urgency</h3>
            <div className="urgency-options">
              <div 
                className={`urgency-option ${formData.urgency === 'standard' ? 'selected' : ''}`}
                onClick={() => setFormData(prev => ({ ...prev, urgency: 'standard' }))}
              >
                <h4>Standard</h4>
                <p>Normal processing time</p>
                <div className="urgency-price">No additional fee</div>
              </div>
              <div 
                className={`urgency-option ${formData.urgency === 'rush' ? 'selected' : ''}`}
                onClick={() => setFormData(prev => ({ ...prev, urgency: 'rush' }))}
              >
                <h4>Rush Processing</h4>
                <p>50% faster delivery</p>
                <div className="urgency-price">+50% fee</div>
              </div>
            </div>
          </div>

          {/* Special Instructions */}
          <div className="form-section">
            <h3>Special Instructions (Optional)</h3>
            <div className="form-group">
              <label htmlFor="special_instructions">Additional Details</label>
              <textarea
                id="special_instructions"
                name="special_instructions"
                value={formData.special_instructions}
                onChange={handleInputChange}
                placeholder="Any specific areas of focus or additional context..."
                rows="4"
              />
            </div>
          </div>

          {/* Submit Button */}
          <div className="form-actions">
            <button 
              type="submit" 
              className="get-quote-button"
              disabled={!validateForm() || loading}
            >
              {loading ? 'Generating Quote...' : 'Get Quote & Proceed'}
            </button>
            <div className="guarantee-text">
              30-day money-back guarantee • Secure payment • Professional results
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default InvestigationOrderForm;

