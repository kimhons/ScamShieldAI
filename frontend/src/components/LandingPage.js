import React, { useState } from 'react';
import PricingSection from './PricingSection';
import './LandingPage.css';

const LandingPage = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
    setIsMenuOpen(false);
  };

  return (
    <div className="landing-page">
      {/* Navigation */}
      <nav className="navbar">
        <div className="nav-container">
          <div className="nav-logo">
            <span className="logo-icon">🛡️</span>
            <span className="logo-text">ScamShield AI</span>
          </div>
          
          <div className={`nav-menu ${isMenuOpen ? 'active' : ''}`}>
            <a href="#home" onClick={() => scrollToSection('home')}>Home</a>
            <a href="#features" onClick={() => scrollToSection('features')}>Features</a>
            <a href="#pricing" onClick={() => scrollToSection('pricing')}>Pricing</a>
            <a href="#demo" onClick={() => scrollToSection('demo')}>Demo</a>
            <a href="#contact" onClick={() => scrollToSection('contact')}>Contact</a>
            <button className="nav-cta">Start Investigation</button>
          </div>
          
          <div className="nav-toggle" onClick={() => setIsMenuOpen(!isMenuOpen)}>
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section id="home" className="hero-section">
        <div className="hero-container">
          <div className="hero-content">
            <h1 className="hero-title">
              Advanced AI-Powered
              <span className="gradient-text"> Fraud Investigation</span>
            </h1>
            <p className="hero-subtitle">
              Professional-grade investigation reports in hours, not weeks. 
              Our multi-agent AI system delivers comprehensive fraud analysis 
              at 98% less cost than traditional services.
            </p>
            
            <div className="hero-stats">
              <div className="stat-item">
                <div className="stat-number">98%</div>
                <div className="stat-label">Cost Reduction</div>
              </div>
              <div className="stat-item">
                <div className="stat-number">3-24hrs</div>
                <div className="stat-label">Delivery Time</div>
              </div>
              <div className="stat-item">
                <div className="stat-number">9+</div>
                <div className="stat-label">Data Sources</div>
              </div>
              <div className="stat-item">
                <div className="stat-number">8</div>
                <div className="stat-label">AI Agents</div>
              </div>
            </div>
            
            <div className="hero-cta">
              <button className="cta-primary" onClick={() => scrollToSection('pricing')}>
                Start Investigation
              </button>
              <button className="cta-secondary" onClick={() => scrollToSection('demo')}>
                Watch Demo
              </button>
            </div>
            
            <div className="hero-trust">
              <p>Trusted by professionals worldwide</p>
              <div className="trust-badges">
                <span className="trust-badge">🏢 Enterprise Ready</span>
                <span className="trust-badge">⚖️ Legal Grade</span>
                <span className="trust-badge">🔒 SOC 2 Compliant</span>
              </div>
            </div>
          </div>
          
          <div className="hero-visual">
            <div className="dashboard-preview">
              <div className="preview-header">
                <div className="preview-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <div className="preview-title">ScamShield AI Dashboard</div>
              </div>
              <div className="preview-content">
                <div className="preview-section">
                  <div className="section-title">🔍 Active Investigation</div>
                  <div className="investigation-item">
                    <div className="investigation-subject">suspicious-crypto-exchange.ml</div>
                    <div className="investigation-status risk-high">HIGH RISK</div>
                  </div>
                  <div className="progress-bar">
                    <div className="progress-fill" style={{width: '87%'}}></div>
                  </div>
                  <div className="progress-text">87% Complete - 8 agents deployed</div>
                </div>
                
                <div className="preview-section">
                  <div className="section-title">📊 Recent Findings</div>
                  <div className="findings-list">
                    <div className="finding-item">
                      <span className="finding-icon">⚠️</span>
                      <span>Domain registered 18 days ago</span>
                    </div>
                    <div className="finding-item">
                      <span className="finding-icon">🚫</span>
                      <span>No business registration found</span>
                    </div>
                    <div className="finding-item">
                      <span className="finding-icon">✅</span>
                      <span>No sanctions matches</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="features-section">
        <div className="container">
          <div className="section-header">
            <h2>Why Choose ScamShield AI?</h2>
            <p>Advanced multi-agent investigation system with professional-grade reporting</p>
          </div>
          
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🤖</div>
              <h3>8 Specialized AI Agents</h3>
              <p>FBI, CIA, MI6, and Mossad-inspired investigation methodologies working in parallel to analyze every aspect of potential fraud.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">🔍</div>
              <h3>9+ Premium Data Sources</h3>
              <p>Integrated access to sanctions databases, financial intelligence, domain analysis, and threat intelligence feeds.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h3>Professional Reports</h3>
              <p>Legal-grade documentation suitable for court proceedings, business decisions, and regulatory compliance.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">⚡</div>
              <h3>Lightning Fast</h3>
              <p>Complete investigations in 3-24 hours vs. weeks for traditional services. Real-time progress tracking.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">💰</div>
              <h3>98% Cost Reduction</h3>
              <p>$9.99-$99.99 per investigation vs. $500-$5,000 for traditional investigation services.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">🔒</div>
              <h3>Enterprise Security</h3>
              <p>SOC 2 compliant with end-to-end encryption, audit trails, and complete data protection.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <PricingSection />

      {/* Demo Section */}
      <section id="demo" className="demo-section">
        <div className="container">
          <div className="section-header">
            <h2>See ScamShield AI in Action</h2>
            <p>Watch how our multi-agent system conducts a comprehensive fraud investigation</p>
          </div>
          
          <div className="demo-container">
            <div className="demo-video">
              <div className="video-placeholder">
                <div className="play-button">▶️</div>
                <div className="video-title">ScamShield AI Investigation Demo</div>
                <div className="video-duration">3:45</div>
              </div>
            </div>
            
            <div className="demo-features">
              <h3>What You'll See:</h3>
              <ul>
                <li>✅ Real-time multi-agent deployment</li>
                <li>✅ Live data source integration</li>
                <li>✅ AI-powered risk assessment</li>
                <li>✅ Professional report generation</li>
                <li>✅ Multi-format export capabilities</li>
              </ul>
              
              <div className="demo-cta">
                <button className="cta-primary">Try Free Investigation</button>
                <p className="demo-note">No credit card required • 5-minute setup</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="testimonials-section">
        <div className="container">
          <div className="section-header">
            <h2>Trusted by Professionals Worldwide</h2>
            <p>See what our customers say about ScamShield AI</p>
          </div>
          
          <div className="testimonials-grid">
            <div className="testimonial-card">
              <div className="testimonial-content">
                "ScamShield AI reduced our investigation time from weeks to hours. The professional reports are court-ready and have saved us thousands in legal fees."
              </div>
              <div className="testimonial-author">
                <div className="author-info">
                  <div className="author-name">Sarah Chen</div>
                  <div className="author-title">Legal Counsel, TechCorp</div>
                </div>
              </div>
            </div>
            
            <div className="testimonial-card">
              <div className="testimonial-content">
                "The multi-agent analysis is incredibly thorough. We've caught fraud attempts that would have cost us millions. ROI was immediate."
              </div>
              <div className="testimonial-author">
                <div className="author-info">
                  <div className="author-name">Michael Rodriguez</div>
                  <div className="author-title">Risk Manager, Global Finance</div>
                </div>
              </div>
            </div>
            
            <div className="testimonial-card">
              <div className="testimonial-content">
                "As a private investigator, ScamShield AI has revolutionized my practice. I can handle 10x more cases with better accuracy."
              </div>
              <div className="testimonial-author">
                <div className="author-info">
                  <div className="author-name">Jennifer Walsh</div>
                  <div className="author-title">Licensed Private Investigator</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="contact-section">
        <div className="container">
          <div className="contact-content">
            <div className="contact-info">
              <h2>Ready to Get Started?</h2>
              <p>Join thousands of professionals who trust ScamShield AI for accurate, fast, and affordable fraud investigations.</p>
              
              <div className="contact-stats">
                <div className="contact-stat">
                  <div className="stat-number">10,000+</div>
                  <div className="stat-label">Investigations Completed</div>
                </div>
                <div className="contact-stat">
                  <div className="stat-number">99.2%</div>
                  <div className="stat-label">Customer Satisfaction</div>
                </div>
                <div className="contact-stat">
                  <div className="stat-number">24/7</div>
                  <div className="stat-label">Support Available</div>
                </div>
              </div>
              
              <div className="contact-methods">
                <div className="contact-method">
                  <span className="method-icon">📧</span>
                  <span>support@scamshield.ai</span>
                </div>
                <div className="contact-method">
                  <span className="method-icon">📞</span>
                  <span>1-800-SCAM-SHIELD</span>
                </div>
                <div className="contact-method">
                  <span className="method-icon">💬</span>
                  <span>Live Chat Available</span>
                </div>
              </div>
            </div>
            
            <div className="contact-form">
              <h3>Start Your Investigation</h3>
              <form>
                <div className="form-group">
                  <label>Investigation Type</label>
                  <select>
                    <option>Domain/Website Investigation</option>
                    <option>Email/Identity Verification</option>
                    <option>Business/Company Analysis</option>
                    <option>Cryptocurrency Investigation</option>
                    <option>Comprehensive Investigation</option>
                  </select>
                </div>
                
                <div className="form-group">
                  <label>Subject to Investigate</label>
                  <input type="text" placeholder="Enter domain, email, or company name" />
                </div>
                
                <div className="form-group">
                  <label>Report Tier</label>
                  <select>
                    <option>Basic Report ($9.99)</option>
                    <option>Standard Report ($24.99)</option>
                    <option>Professional Report ($49.99)</option>
                    <option>Forensic Report ($99.99)</option>
                  </select>
                </div>
                
                <div className="form-group">
                  <label>Your Email</label>
                  <input type="email" placeholder="your@email.com" />
                </div>
                
                <button type="submit" className="form-submit">
                  Start Investigation Now
                </button>
                
                <p className="form-note">
                  Secure payment • Instant delivery • 100% satisfaction guarantee
                </p>
              </form>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-section">
              <div className="footer-logo">
                <span className="logo-icon">🛡️</span>
                <span className="logo-text">ScamShield AI</span>
              </div>
              <p>Advanced AI-powered fraud investigation platform trusted by professionals worldwide.</p>
            </div>
            
            <div className="footer-section">
              <h4>Services</h4>
              <ul>
                <li><a href="#pricing">Investigation Reports</a></li>
                <li><a href="#features">Multi-Agent Analysis</a></li>
                <li><a href="#demo">API Integration</a></li>
                <li><a href="#contact">Enterprise Solutions</a></li>
              </ul>
            </div>
            
            <div className="footer-section">
              <h4>Company</h4>
              <ul>
                <li><a href="#about">About Us</a></li>
                <li><a href="#careers">Careers</a></li>
                <li><a href="#press">Press</a></li>
                <li><a href="#partners">Partners</a></li>
              </ul>
            </div>
            
            <div className="footer-section">
              <h4>Legal</h4>
              <ul>
                <li><a href="#privacy">Privacy Policy</a></li>
                <li><a href="#terms">Terms of Service</a></li>
                <li><a href="#compliance">Compliance</a></li>
                <li><a href="#security">Security</a></li>
              </ul>
            </div>
          </div>
          
          <div className="footer-bottom">
            <p>&copy; 2025 ScamShield AI. All rights reserved.</p>
            <div className="footer-social">
              <a href="#twitter">Twitter</a>
              <a href="#linkedin">LinkedIn</a>
              <a href="#github">GitHub</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;

