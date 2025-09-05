import React, { useState } from 'react';
import './BackgroundCheckPanel.css';

const BackgroundCheckPanel = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    state: '',
    zipCode: ''
  });

  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      // Simulate API call for demo
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      // Mock response data
      const mockResults = {
        personData: formData,
        riskScore: 15.2,
        confidenceLevel: 'High',
        dataSources: ['TruePeopleSearch', 'Address Verification Service', 'Phone Carrier Database', 'Email Verification Service', 'Social Media Search', 'Criminal Records Database', 'OpenSanctions'],
        identityVerification: {
          identityFound: true,
          nameMatch: 'exact',
          ageRange: '30-35',
          knownAddresses: 2,
          knownPhoneNumbers: 1,
          relativesFound: 3,
          verificationScore: 0.92
        },
        addressHistory: [
          {
            address: `${formData.address}, ${formData.city}, ${formData.state} ${formData.zipCode}`,
            residencePeriod: '2021-2024',
            verificationStatus: 'verified',
            propertyType: 'apartment',
            ownershipStatus: 'renter'
          },
          {
            address: '456 Oak Avenue, Previous City, NY 67890',
            residencePeriod: '2019-2021',
            verificationStatus: 'verified',
            propertyType: 'single_family',
            ownershipStatus: 'owner'
          }
        ],
        phoneVerification: {
          phoneNumber: formData.phone,
          carrier: 'T-Mobile',
          lineType: 'mobile',
          location: 'New York, NY',
          isValid: true,
          isActive: true,
          verificationScore: 0.88
        },
        emailVerification: {
          emailAddress: formData.email,
          domain: formData.email.split('@')[1] || 'example.com',
          isValid: true,
          isDeliverable: true,
          isDisposable: false,
          domainReputation: 'good',
          breachCount: 0,
          verificationScore: 0.85
        },
        socialMediaProfiles: [
          {
            platform: 'LinkedIn',
            username: `${formData.firstName.toLowerCase()}.${formData.lastName.toLowerCase()}`,
            verificationStatus: 'verified',
            activityLevel: 'active',
            professionalInfo: {
              currentJob: 'Marketing Manager',
              company: 'Digital Solutions Inc',
              location: 'New York, NY'
            }
          }
        ],
        criminalRecords: {
          recordsFound: false,
          searchStates: ['NY', 'NJ', 'CT'],
          federalSearch: true,
          sexOffenderCheck: true,
          warrantCheck: true
        },
        investigationTimestamp: new Date().toISOString()
      };

      setResults(mockResults);
    } catch (err) {
      setError('Failed to perform background check. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const getRiskLevelColor = (score) => {
    if (score < 20) return '#10B981'; // Green
    if (score < 50) return '#F59E0B'; // Yellow
    if (score < 80) return '#EF4444'; // Red
    return '#DC2626'; // Dark Red
  };

  const getRiskLevelText = (score) => {
    if (score < 20) return 'Low Risk';
    if (score < 50) return 'Medium Risk';
    if (score < 80) return 'High Risk';
    return 'Critical Risk';
  };

  return (
    <div className="background-check-panel">
      <div className="panel-header">
        <h2>🔍 Background Check Investigation</h2>
        <p>Comprehensive identity verification and background screening</p>
      </div>

      {!results ? (
        <form onSubmit={handleSubmit} className="background-check-form">
          <div className="form-section">
            <h3>Personal Information</h3>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="firstName">First Name *</label>
                <input
                  type="text"
                  id="firstName"
                  name="firstName"
                  value={formData.firstName}
                  onChange={handleInputChange}
                  required
                  placeholder="Enter first name"
                />
              </div>
              <div className="form-group">
                <label htmlFor="lastName">Last Name *</label>
                <input
                  type="text"
                  id="lastName"
                  name="lastName"
                  value={formData.lastName}
                  onChange={handleInputChange}
                  required
                  placeholder="Enter last name"
                />
              </div>
            </div>
          </div>

          <div className="form-section">
            <h3>Contact Information</h3>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="email">Email Address</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  placeholder="Enter email address"
                />
              </div>
              <div className="form-group">
                <label htmlFor="phone">Phone Number</label>
                <input
                  type="tel"
                  id="phone"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                  placeholder="(555) 123-4567"
                />
              </div>
            </div>
          </div>

          <div className="form-section">
            <h3>Address Information</h3>
            <div className="form-group">
              <label htmlFor="address">Street Address</label>
              <input
                type="text"
                id="address"
                name="address"
                value={formData.address}
                onChange={handleInputChange}
                placeholder="123 Main Street"
              />
            </div>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="city">City</label>
                <input
                  type="text"
                  id="city"
                  name="city"
                  value={formData.city}
                  onChange={handleInputChange}
                  placeholder="New York"
                />
              </div>
              <div className="form-group">
                <label htmlFor="state">State</label>
                <input
                  type="text"
                  id="state"
                  name="state"
                  value={formData.state}
                  onChange={handleInputChange}
                  placeholder="NY"
                  maxLength="2"
                />
              </div>
              <div className="form-group">
                <label htmlFor="zipCode">ZIP Code</label>
                <input
                  type="text"
                  id="zipCode"
                  name="zipCode"
                  value={formData.zipCode}
                  onChange={handleInputChange}
                  placeholder="10001"
                />
              </div>
            </div>
          </div>

          {error && (
            <div className="error-message">
              ❌ {error}
            </div>
          )}

          <button 
            type="submit" 
            className="submit-button"
            disabled={isLoading || !formData.firstName || !formData.lastName}
          >
            {isLoading ? (
              <>
                <div className="spinner"></div>
                Performing Background Check...
              </>
            ) : (
              'Start Background Check'
            )}
          </button>
        </form>
      ) : (
        <div className="results-container">
          <div className="results-header">
            <h3>📋 Background Check Report</h3>
            <button 
              onClick={() => setResults(null)}
              className="new-search-button"
            >
              New Search
            </button>
          </div>

          <div className="subject-info">
            <h4>Subject Information</h4>
            <p><strong>Name:</strong> {results.personData.firstName} {results.personData.lastName}</p>
            <p><strong>Email:</strong> {results.personData.email}</p>
            <p><strong>Phone:</strong> {results.personData.phone}</p>
            <p><strong>Investigation Date:</strong> {new Date(results.investigationTimestamp).toLocaleString()}</p>
          </div>

          <div className="risk-assessment">
            <h4>🎯 Risk Assessment</h4>
            <div className="risk-score">
              <div className="risk-meter">
                <div 
                  className="risk-fill"
                  style={{ 
                    width: `${results.riskScore}%`,
                    backgroundColor: getRiskLevelColor(results.riskScore)
                  }}
                ></div>
              </div>
              <div className="risk-details">
                <span className="risk-number">{results.riskScore.toFixed(1)}/100</span>
                <span 
                  className="risk-level"
                  style={{ color: getRiskLevelColor(results.riskScore) }}
                >
                  {getRiskLevelText(results.riskScore)}
                </span>
              </div>
            </div>
            <p><strong>Confidence Level:</strong> {results.confidenceLevel}</p>
            <p><strong>Data Sources:</strong> {results.dataSources.join(', ')}</p>
          </div>

          <div className="verification-sections">
            <div className="verification-section">
              <h4>✅ Identity Verification</h4>
              <div className="verification-grid">
                <div className="verification-item">
                  <span className="label">Identity Found:</span>
                  <span className={`value ${results.identityVerification.identityFound ? 'success' : 'warning'}`}>
                    {results.identityVerification.identityFound ? 'Yes' : 'No'}
                  </span>
                </div>
                <div className="verification-item">
                  <span className="label">Name Match:</span>
                  <span className="value">{results.identityVerification.nameMatch}</span>
                </div>
                <div className="verification-item">
                  <span className="label">Age Range:</span>
                  <span className="value">{results.identityVerification.ageRange}</span>
                </div>
                <div className="verification-item">
                  <span className="label">Verification Score:</span>
                  <span className="value">{(results.identityVerification.verificationScore * 100).toFixed(0)}%</span>
                </div>
              </div>
            </div>

            <div className="verification-section">
              <h4>🏠 Address History</h4>
              {results.addressHistory.map((address, index) => (
                <div key={index} className="address-item">
                  <div className="address-main">{address.address}</div>
                  <div className="address-details">
                    <span>Period: {address.residencePeriod}</span>
                    <span>Status: {address.verificationStatus}</span>
                    <span>Type: {address.propertyType}</span>
                  </div>
                </div>
              ))}
            </div>

            <div className="verification-section">
              <h4>📱 Phone Verification</h4>
              <div className="verification-grid">
                <div className="verification-item">
                  <span className="label">Valid:</span>
                  <span className={`value ${results.phoneVerification.isValid ? 'success' : 'warning'}`}>
                    {results.phoneVerification.isValid ? 'Yes' : 'No'}
                  </span>
                </div>
                <div className="verification-item">
                  <span className="label">Carrier:</span>
                  <span className="value">{results.phoneVerification.carrier}</span>
                </div>
                <div className="verification-item">
                  <span className="label">Type:</span>
                  <span className="value">{results.phoneVerification.lineType}</span>
                </div>
                <div className="verification-item">
                  <span className="label">Location:</span>
                  <span className="value">{results.phoneVerification.location}</span>
                </div>
              </div>
            </div>

            <div className="verification-section">
              <h4>📧 Email Verification</h4>
              <div className="verification-grid">
                <div className="verification-item">
                  <span className="label">Valid:</span>
                  <span className={`value ${results.emailVerification.isValid ? 'success' : 'warning'}`}>
                    {results.emailVerification.isValid ? 'Yes' : 'No'}
                  </span>
                </div>
                <div className="verification-item">
                  <span className="label">Deliverable:</span>
                  <span className={`value ${results.emailVerification.isDeliverable ? 'success' : 'warning'}`}>
                    {results.emailVerification.isDeliverable ? 'Yes' : 'No'}
                  </span>
                </div>
                <div className="verification-item">
                  <span className="label">Domain:</span>
                  <span className="value">{results.emailVerification.domain}</span>
                </div>
                <div className="verification-item">
                  <span className="label">Reputation:</span>
                  <span className="value">{results.emailVerification.domainReputation}</span>
                </div>
              </div>
            </div>

            <div className="verification-section">
              <h4>📱 Social Media Profiles</h4>
              {results.socialMediaProfiles.map((profile, index) => (
                <div key={index} className="social-profile">
                  <div className="profile-header">
                    <strong>{profile.platform}</strong>
                    <span className={`status ${profile.verificationStatus}`}>
                      {profile.verificationStatus}
                    </span>
                  </div>
                  <div className="profile-details">
                    <p>Username: {profile.username}</p>
                    <p>Activity: {profile.activityLevel}</p>
                    {profile.professionalInfo && (
                      <p>Current Role: {profile.professionalInfo.currentJob} at {profile.professionalInfo.company}</p>
                    )}
                  </div>
                </div>
              ))}
            </div>

            <div className="verification-section">
              <h4>⚖️ Criminal Records</h4>
              <div className="verification-grid">
                <div className="verification-item">
                  <span className="label">Records Found:</span>
                  <span className={`value ${results.criminalRecords.recordsFound ? 'warning' : 'success'}`}>
                    {results.criminalRecords.recordsFound ? 'Yes' : 'No'}
                  </span>
                </div>
                <div className="verification-item">
                  <span className="label">States Searched:</span>
                  <span className="value">{results.criminalRecords.searchStates.join(', ')}</span>
                </div>
                <div className="verification-item">
                  <span className="label">Federal Search:</span>
                  <span className="value">{results.criminalRecords.federalSearch ? 'Yes' : 'No'}</span>
                </div>
                <div className="verification-item">
                  <span className="label">Sex Offender Check:</span>
                  <span className="value">{results.criminalRecords.sexOffenderCheck ? 'Yes' : 'No'}</span>
                </div>
              </div>
            </div>
          </div>

          <div className="report-actions">
            <button className="download-button">
              📄 Download PDF Report
            </button>
            <button className="share-button">
              📤 Share Report
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default BackgroundCheckPanel;

