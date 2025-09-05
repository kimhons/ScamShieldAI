import React, { useState, useEffect } from 'react';
import './NewPricingSection.css';

const NewPricingSection = () => {
  const [pricingData, setPricingData] = useState(null);
  const [selectedTier, setSelectedTier] = useState('professional');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch pricing data from API
    fetchPricingData();
  }, []);

  const fetchPricingData = async () => {
    try {
      // In production, this would call the actual API
      // For now, using the same data structure as our Flask API
      const mockPricingData = {
        success: true,
        pricing_model: 'per_report',
        currency: 'USD',
        tiers: {
          basic: {
            price: 9.99,
            name: 'Basic Report',
            pages: '3-5 pages',
            description: 'Essential fraud investigation for quick risk assessment',
            delivery_time: '24 hours',
            features: [
              'Identity Verification',
              'Basic Digital Footprint Analysis', 
              'Compliance Screening (Sanctions/PEP)',
              'Risk Assessment Summary',
              'PDF & HTML Export',
              '24-hour delivery',
              'Email support'
            ]
          },
          standard: {
            price: 24.99,
            name: 'Standard Report',
            pages: '8-12 pages',
            description: 'Comprehensive analysis with detailed findings and strategic recommendations',
            delivery_time: '12 hours',
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
            ]
          },
          professional: {
            price: 49.99,
            name: 'Professional Report',
            pages: '15-25 pages',
            description: 'Expert-level analysis with advanced risk modeling and detailed methodology',
            delivery_time: '6 hours',
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
            ]
          },
          forensic: {
            price: 99.99,
            name: 'Forensic Report',
            pages: '25-40 pages',
            description: 'Legal-grade documentation with complete evidence chain for court proceedings',
            delivery_time: '3 hours',
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
            ]
          }
        },
        comparison: {
          traditional_services: {
            price_range: '$500 - $5,000',
            delivery_time: '2-4 weeks',
            data_sources: '2-3',
            format_options: 'PDF only'
          },
          scamshield_ai: {
            price_range: '$9.99 - $99.99',
            delivery_time: '3-24 hours',
            data_sources: '9+',
            format_options: 'PDF, HTML, JSON, Word'
          },
          savings: '98% cost reduction'
        }
      };
      
      setPricingData(mockPricingData);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching pricing data:', error);
      setLoading(false);
    }
  };

  const handleSelectTier = (tierKey) => {
    setSelectedTier(tierKey);
  };

  const handleOrderNow = (tierKey) => {
    // In production, this would redirect to order form
    window.location.href = `/order?tier=${tierKey}`;
  };

  if (loading) {
    return (
      <div className="pricing-section loading">
        <div className="loading-spinner">Loading pricing information...</div>
      </div>
    );
  }

  if (!pricingData) {
    return (
      <div className="pricing-section error">
        <div className="error-message">Unable to load pricing information</div>
      </div>
    );
  }

  const { tiers, comparison } = pricingData;

  return (
    <section className="pricing-section" id="pricing">
      <div className="container">
        {/* Header */}
        <div className="pricing-header">
          <h2 className="section-title">Professional Investigation Reports</h2>
          <p className="section-subtitle">
            Choose the perfect report tier for your investigation needs. 
            Pay only for what you need, when you need it.
          </p>
          
          {/* Cost Comparison Banner */}
          <div className="cost-comparison">
            <div className="comparison-item traditional">
              <h4>Traditional Services</h4>
              <div className="price-range">{comparison.traditional_services.price_range}</div>
              <div className="details">
                <span>⏱ {comparison.traditional_services.delivery_time}</span>
                <span>📊 {comparison.traditional_services.data_sources} data sources</span>
                <span>📄 {comparison.traditional_services.format_options}</span>
              </div>
            </div>
            
            <div className="vs-divider">
              <span>VS</span>
            </div>
            
            <div className="comparison-item scamshield">
              <h4>ScamShield AI</h4>
              <div className="price-range">{comparison.scamshield_ai.price_range}</div>
              <div className="details">
                <span>⚡ {comparison.scamshield_ai.delivery_time}</span>
                <span>🔗 {comparison.scamshield_ai.data_sources} data sources</span>
                <span>📋 {comparison.scamshield_ai.format_options}</span>
              </div>
              <div className="savings-badge">{comparison.savings}</div>
            </div>
          </div>
        </div>

        {/* Pricing Tiers */}
        <div className="pricing-tiers">
          {Object.entries(tiers).map(([tierKey, tier]) => (
            <div 
              key={tierKey}
              className={`pricing-card ${tierKey} ${selectedTier === tierKey ? 'selected' : ''} ${tierKey === 'professional' ? 'popular' : ''}`}
              onClick={() => handleSelectTier(tierKey)}
            >
              {tierKey === 'professional' && (
                <div className="popular-badge">Most Popular</div>
              )}
              
              <div className="card-header">
                <h3 className="tier-name">{tier.name}</h3>
                <div className="tier-price">
                  <span className="currency">$</span>
                  <span className="amount">{tier.price}</span>
                  <span className="period">per report</span>
                </div>
                <p className="tier-description">{tier.description}</p>
              </div>

              <div className="card-body">
                <div className="tier-details">
                  <div className="detail-item">
                    <span className="icon">📄</span>
                    <span>{tier.pages}</span>
                  </div>
                  <div className="detail-item">
                    <span className="icon">⏱</span>
                    <span>{tier.delivery_time}</span>
                  </div>
                </div>

                <div className="features-list">
                  {tier.features.map((feature, index) => (
                    <div key={index} className="feature-item">
                      <span className="check-icon">✓</span>
                      <span>{feature}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="card-footer">
                <button 
                  className={`order-button ${tierKey}`}
                  onClick={(e) => {
                    e.stopPropagation();
                    handleOrderNow(tierKey);
                  }}
                >
                  Order {tier.name}
                </button>
                <div className="money-back">30-day money-back guarantee</div>
              </div>
            </div>
          ))}
        </div>

        {/* Features Comparison Table */}
        <div className="features-comparison">
          <h3>Detailed Feature Comparison</h3>
          <div className="comparison-table">
            <table>
              <thead>
                <tr>
                  <th>Feature</th>
                  <th>Basic</th>
                  <th>Standard</th>
                  <th>Professional</th>
                  <th>Forensic</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Identity Verification</td>
                  <td>✓</td>
                  <td>✓</td>
                  <td>✓</td>
                  <td>✓</td>
                </tr>
                <tr>
                  <td>Digital Footprint Analysis</td>
                  <td>Basic</td>
                  <td>Advanced</td>
                  <td>Expert</td>
                  <td>Forensic</td>
                </tr>
                <tr>
                  <td>AI Agents Deployed</td>
                  <td>2</td>
                  <td>4</td>
                  <td>8</td>
                  <td>8</td>
                </tr>
                <tr>
                  <td>Data Sources</td>
                  <td>3</td>
                  <td>6</td>
                  <td>9+</td>
                  <td>9+</td>
                </tr>
                <tr>
                  <td>Export Formats</td>
                  <td>PDF, HTML</td>
                  <td>All Formats</td>
                  <td>All Formats</td>
                  <td>All Formats</td>
                </tr>
                <tr>
                  <td>Legal Documentation</td>
                  <td>-</td>
                  <td>-</td>
                  <td>Business Grade</td>
                  <td>Court Ready</td>
                </tr>
                <tr>
                  <td>Support Level</td>
                  <td>Email</td>
                  <td>Priority Email</td>
                  <td>Phone & Email</td>
                  <td>Dedicated Specialist</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* FAQ Section */}
        <div className="pricing-faq">
          <h3>Frequently Asked Questions</h3>
          <div className="faq-grid">
            <div className="faq-item">
              <h4>How does per-report pricing work?</h4>
              <p>You pay only for the investigations you need. No monthly subscriptions, no hidden fees. Order a report, pay once, receive professional results.</p>
            </div>
            <div className="faq-item">
              <h4>What's included in each report?</h4>
              <p>Each report includes comprehensive analysis, risk assessment, evidence documentation, and professional formatting. Higher tiers include more data sources and detailed analysis.</p>
            </div>
            <div className="faq-item">
              <h4>How fast will I receive my report?</h4>
              <p>Delivery times range from 3-24 hours depending on the tier selected. Most reports are delivered within 6 hours.</p>
            </div>
            <div className="faq-item">
              <h4>Are reports suitable for legal use?</h4>
              <p>Professional and Forensic tiers provide business and legal-grade documentation with complete evidence chains and expert certification.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default NewPricingSection;

