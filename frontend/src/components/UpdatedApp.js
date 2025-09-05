import React, { useState } from 'react';
import './UpdatedApp.css';
import NewPricingSection from './NewPricingSection';
import InvestigationOrderForm from './InvestigationOrderForm';

const UpdatedApp = () => {
  const [currentPage, setCurrentPage] = useState('home');

  const navigateTo = (page) => {
    setCurrentPage(page);
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'order':
        return <InvestigationOrderForm />;
      case 'pricing':
        return <NewPricingSection />;
      default:
        return <HomePage navigateTo={navigateTo} />;
    }
  };

  return (
    <div className="updated-app">
      {currentPage === 'home' && (
        <Navigation navigateTo={navigateTo} />
      )}
      {renderPage()}
      {currentPage === 'home' && (
        <Footer navigateTo={navigateTo} />
      )}
    </div>
  );
};

const Navigation = ({ navigateTo }) => {
  return (
    <nav className="navigation">
      <div className="nav-container">
        <div className="nav-brand">
          <span className="brand-icon">🛡️</span>
          <span className="brand-name">ScamShield AI</span>
        </div>
        <div className="nav-links">
          <a href="#features" className="nav-link">Features</a>
          <a href="#pricing" className="nav-link">Pricing</a>
          <a href="#about" className="nav-link">About</a>
          <button 
            className="nav-cta"
            onClick={() => navigateTo('order')}
          >
            Start Investigation
          </button>
        </div>
      </div>
    </nav>
  );
};

const HomePage = ({ navigateTo }) => {
  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-container">
          <div className="hero-content">
            <h1 className="hero-title">
              Professional Fraud Investigation
              <span className="highlight"> Powered by AI</span>
            </h1>
            <p className="hero-subtitle">
              Get expert-level fraud investigation reports in hours, not weeks. 
              Our 8 specialized AI agents analyze 9+ data sources to deliver 
              professional-grade results at 98% less cost than traditional services.
            </p>
            <div className="hero-stats">
              <div className="stat">
                <div className="stat-number">98%</div>
                <div className="stat-label">Cost Reduction</div>
              </div>
              <div className="stat">
                <div className="stat-number">3-24h</div>
                <div className="stat-label">Delivery Time</div>
              </div>
              <div className="stat">
                <div className="stat-number">9+</div>
                <div className="stat-label">Data Sources</div>
              </div>
              <div className="stat">
                <div className="stat-number">8</div>
                <div className="stat-label">AI Agents</div>
              </div>
            </div>
            <div className="hero-actions">
              <button 
                className="primary-button"
                onClick={() => navigateTo('order')}
              >
                Start Investigation Now
              </button>
              <button 
                className="secondary-button"
                onClick={() => navigateTo('pricing')}
              >
                View Pricing
              </button>
            </div>
            <div className="trust-indicators">
              <span>🔒 Bank-level Security</span>
              <span>⚡ Instant Results</span>
              <span>💰 30-day Guarantee</span>
            </div>
          </div>
          <div className="hero-visual">
            <div className="investigation-demo">
              <div className="demo-header">
                <span className="demo-title">Live Investigation</span>
                <span className="demo-status">🟢 Active</span>
              </div>
              <div className="demo-agents">
                <div className="agent-item">
                  <span className="agent-icon">🕵️</span>
                  <span className="agent-name">FBI Cyber Agent</span>
                  <span className="agent-status">Analyzing...</span>
                </div>
                <div className="agent-item">
                  <span className="agent-icon">🔍</span>
                  <span className="agent-name">CIA Intelligence</span>
                  <span className="agent-status">Complete ✓</span>
                </div>
                <div className="agent-item">
                  <span className="agent-icon">🌐</span>
                  <span className="agent-name">MI6 Signals</span>
                  <span className="agent-status">Processing...</span>
                </div>
                <div className="agent-item">
                  <span className="agent-icon">🛡️</span>
                  <span className="agent-name">Mossad Counter-Intel</span>
                  <span className="agent-status">Queued</span>
                </div>
              </div>
              <div className="demo-progress">
                <div className="progress-bar">
                  <div className="progress-fill" style={{width: '67%'}}></div>
                </div>
                <span className="progress-text">67% Complete</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="features-section">
        <div className="container">
          <div className="section-header">
            <h2>Advanced AI Investigation Capabilities</h2>
            <p>Our multi-agent system delivers comprehensive fraud analysis using cutting-edge AI technology</p>
          </div>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🤖</div>
              <h3>8 Specialized AI Agents</h3>
              <p>FBI, CIA, MI6, and Mossad-inspired methodologies working in parallel to analyze every aspect of potential fraud</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🔗</div>
              <h3>9+ Data Sources</h3>
              <p>OpenSanctions, WhoisXML, Shodan, Alpha Vantage, Companies House, and more for comprehensive intelligence</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h3>Professional Reports</h3>
              <p>Legal-grade documentation suitable for court proceedings, business decisions, and regulatory compliance</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">⚡</div>
              <h3>Real-time Processing</h3>
              <p>Advanced parallel processing delivers results in 3-24 hours instead of weeks required by traditional services</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🎯</div>
              <h3>Multi-format Export</h3>
              <p>Receive reports in PDF, HTML, JSON, and Word formats for maximum compatibility and usability</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🔒</div>
              <h3>Enterprise Security</h3>
              <p>Bank-level encryption, GDPR compliance, and secure data handling protect your sensitive investigations</p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <NewPricingSection />

      {/* Comparison Section */}
      <section className="comparison-section">
        <div className="container">
          <div className="section-header">
            <h2>Why Choose ScamShield AI?</h2>
            <p>See how we compare to traditional investigation services</p>
          </div>
          <div className="comparison-table">
            <div className="comparison-header">
              <div className="comparison-item">
                <h3>Feature</h3>
              </div>
              <div className="comparison-item traditional">
                <h3>Traditional Services</h3>
              </div>
              <div className="comparison-item scamshield">
                <h3>ScamShield AI</h3>
              </div>
            </div>
            <div className="comparison-row">
              <div className="comparison-item">Cost per Investigation</div>
              <div className="comparison-item traditional">$500 - $5,000</div>
              <div className="comparison-item scamshield">$9.99 - $99.99</div>
            </div>
            <div className="comparison-row">
              <div className="comparison-item">Delivery Time</div>
              <div className="comparison-item traditional">2-4 weeks</div>
              <div className="comparison-item scamshield">3-24 hours</div>
            </div>
            <div className="comparison-row">
              <div className="comparison-item">Data Sources</div>
              <div className="comparison-item traditional">2-3 sources</div>
              <div className="comparison-item scamshield">9+ sources</div>
            </div>
            <div className="comparison-row">
              <div className="comparison-item">Report Formats</div>
              <div className="comparison-item traditional">PDF only</div>
              <div className="comparison-item scamshield">PDF, HTML, JSON, Word</div>
            </div>
            <div className="comparison-row">
              <div className="comparison-item">AI Enhancement</div>
              <div className="comparison-item traditional">Manual analysis</div>
              <div className="comparison-item scamshield">8 AI agents</div>
            </div>
            <div className="comparison-row">
              <div className="comparison-item">Availability</div>
              <div className="comparison-item traditional">Business hours</div>
              <div className="comparison-item scamshield">24/7 automated</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="container">
          <div className="cta-content">
            <h2>Ready to Revolutionize Your Fraud Investigation?</h2>
            <p>Join thousands of professionals who trust ScamShield AI for accurate, fast, and affordable fraud detection</p>
            <div className="cta-actions">
              <button 
                className="primary-button large"
                onClick={() => navigateTo('order')}
              >
                Start Your Investigation
              </button>
              <div className="cta-guarantee">
                30-day money-back guarantee • No setup fees • Instant delivery
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

const Footer = ({ navigateTo }) => {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-brand">
            <div className="brand">
              <span className="brand-icon">🛡️</span>
              <span className="brand-name">ScamShield AI</span>
            </div>
            <p>Professional fraud investigation powered by advanced AI technology</p>
          </div>
          <div className="footer-links">
            <div className="link-group">
              <h4>Services</h4>
              <a href="#" onClick={() => navigateTo('order')}>Domain Investigation</a>
              <a href="#" onClick={() => navigateTo('order')}>Email Analysis</a>
              <a href="#" onClick={() => navigateTo('order')}>Background Checks</a>
              <a href="#" onClick={() => navigateTo('order')}>Business Verification</a>
            </div>
            <div className="link-group">
              <h4>Company</h4>
              <a href="#">About Us</a>
              <a href="#">Contact</a>
              <a href="#">Privacy Policy</a>
              <a href="#">Terms of Service</a>
            </div>
            <div className="link-group">
              <h4>Support</h4>
              <a href="#">Help Center</a>
              <a href="#">API Documentation</a>
              <a href="#">Status Page</a>
              <a href="#">Security</a>
            </div>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; 2024 ScamShield AI. All rights reserved.</p>
          <div className="footer-badges">
            <span>🔒 SOC 2 Compliant</span>
            <span>🛡️ GDPR Ready</span>
            <span>⚡ 99.9% Uptime</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default UpdatedApp;

