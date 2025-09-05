"""
ScamShield AI - Investigation Data Processor
Processes and validates investigation data for report generation
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import statistics
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RiskLevel(Enum):
    """Risk level enumeration"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ComplianceStatus(Enum):
    """Compliance status enumeration"""
    CLEAR = "CLEAR"
    REVIEW = "REVIEW"
    BLOCKED = "BLOCKED"

@dataclass
class ValidationResult:
    """Data validation result"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    completeness_score: float
    quality_score: float

@dataclass
class RiskAssessment:
    """Comprehensive risk assessment"""
    overall_score: float
    risk_level: RiskLevel
    confidence: float
    risk_factors: Dict[str, float]
    risk_indicators: List[str]
    mitigation_recommendations: List[str]

@dataclass
class EvidenceItem:
    """Evidence chain item"""
    source: str
    data_type: str
    finding: str
    confidence: float
    timestamp: datetime
    verification_status: str

@dataclass
class ProcessedInvestigationData:
    """Processed and validated investigation data"""
    investigation_id: str
    subject: str
    executive_summary: Dict[str, Any]
    risk_assessment: RiskAssessment
    detailed_findings: Dict[str, Any]
    evidence_chain: List[EvidenceItem]
    recommendations: List[str]
    compliance_status: ComplianceStatus
    metadata: Dict[str, Any]
    processed_at: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['processed_at'] = self.processed_at.isoformat()
        data['risk_assessment']['risk_level'] = self.risk_assessment.risk_level.value
        data['compliance_status'] = self.compliance_status.value
        
        # Convert evidence chain
        evidence_list = []
        for evidence in self.evidence_chain:
            evidence_dict = asdict(evidence)
            evidence_dict['timestamp'] = evidence.timestamp.isoformat()
            evidence_list.append(evidence_dict)
        data['evidence_chain'] = evidence_list
        
        return data

class DataValidator:
    """Validates investigation data quality and completeness"""
    
    def __init__(self):
        self.required_fields = {
            'crew_results': ['domain_analysis', 'email_analysis', 'background_check'],
            'api_responses': ['opensanctions', 'whoisxml', 'rapidapi'],
            'ml_predictions': ['overall_risk_score'],
            'metadata': ['investigation_id', 'subject']
        }
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate investigation data"""
        errors = []
        warnings = []
        
        # Check required fields
        for section, fields in self.required_fields.items():
            if section not in data:
                errors.append(f"Missing required section: {section}")
                continue
            
            for field in fields:
                if field not in data[section]:
                    errors.append(f"Missing required field: {section}.{field}")
        
        # Validate data quality
        quality_issues = self._validate_data_quality(data)
        warnings.extend(quality_issues)
        
        # Calculate scores
        completeness_score = self._calculate_completeness(data)
        quality_score = self._calculate_quality(data)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            completeness_score=completeness_score,
            quality_score=quality_score
        )
    
    def _validate_data_quality(self, data: Dict[str, Any]) -> List[str]:
        """Validate data quality issues"""
        warnings = []
        
        # Check API response success rates
        api_responses = data.get('api_responses', {})
        failed_apis = [api for api, response in api_responses.items() 
                      if response.get('status') != 'success']
        
        if failed_apis:
            warnings.append(f"Failed API calls: {', '.join(failed_apis)}")
        
        # Check ML prediction confidence
        ml_predictions = data.get('ml_predictions', {})
        low_confidence_predictions = []
        
        for prediction_type, prediction in ml_predictions.items():
            if isinstance(prediction, dict) and 'prediction' in prediction:
                confidence = prediction['prediction'].get('confidence', 0)
                if confidence < 0.7:
                    low_confidence_predictions.append(prediction_type)
        
        if low_confidence_predictions:
            warnings.append(f"Low confidence ML predictions: {', '.join(low_confidence_predictions)}")
        
        return warnings
    
    def _calculate_completeness(self, data: Dict[str, Any]) -> float:
        """Calculate data completeness score"""
        total_fields = 0
        present_fields = 0
        
        for section, fields in self.required_fields.items():
            total_fields += len(fields)
            if section in data:
                for field in fields:
                    if field in data[section]:
                        present_fields += 1
        
        return present_fields / total_fields if total_fields > 0 else 0.0
    
    def _calculate_quality(self, data: Dict[str, Any]) -> float:
        """Calculate data quality score"""
        quality_factors = []
        
        # API success rate
        api_responses = data.get('api_responses', {})
        if api_responses:
            successful_apis = sum(1 for response in api_responses.values() 
                                if response.get('status') == 'success')
            api_success_rate = successful_apis / len(api_responses)
            quality_factors.append(api_success_rate)
        
        # ML confidence average
        ml_predictions = data.get('ml_predictions', {})
        if ml_predictions:
            confidences = []
            for prediction in ml_predictions.values():
                if isinstance(prediction, dict) and 'prediction' in prediction:
                    confidence = prediction['prediction'].get('confidence', 0)
                    confidences.append(confidence)
            
            if confidences:
                avg_confidence = statistics.mean(confidences)
                quality_factors.append(avg_confidence)
        
        # Data freshness (assume recent data is higher quality)
        metadata = data.get('metadata', {})
        collection_time = metadata.get('collection_timestamp')
        if collection_time:
            # Simple freshness score (1.0 for recent data)
            quality_factors.append(0.95)  # Assume good freshness
        
        return statistics.mean(quality_factors) if quality_factors else 0.5

class RiskScorer:
    """Calculates comprehensive risk scores and assessments"""
    
    def __init__(self):
        self.risk_weights = {
            'identity_risk': 0.25,
            'financial_risk': 0.30,
            'digital_risk': 0.20,
            'compliance_risk': 0.15,
            'threat_risk': 0.10
        }
    
    def calculate_comprehensive_risk_assessment(self, data: Dict[str, Any]) -> RiskAssessment:
        """Calculate comprehensive risk assessment"""
        
        # Calculate individual risk factors
        risk_factors = {
            'identity_risk': self.score_identity_risk(data),
            'financial_risk': self.score_financial_risk(data),
            'digital_risk': self.score_digital_risk(data),
            'compliance_risk': self.score_compliance_risk(data),
            'threat_risk': self.score_threat_risk(data)
        }
        
        # Calculate weighted overall score
        overall_score = self.calculate_weighted_score(risk_factors)
        
        # Determine risk level
        risk_level = self.determine_risk_level(overall_score)
        
        # Calculate confidence
        confidence = self.calculate_confidence(data)
        
        # Identify risk indicators
        risk_indicators = self.identify_risk_indicators(data, risk_factors)
        
        # Generate recommendations
        recommendations = self.generate_mitigation_recommendations(risk_factors, risk_level)
        
        return RiskAssessment(
            overall_score=overall_score,
            risk_level=risk_level,
            confidence=confidence,
            risk_factors=risk_factors,
            risk_indicators=risk_indicators,
            mitigation_recommendations=recommendations
        )
    
    def score_identity_risk(self, data: Dict[str, Any]) -> float:
        """Score identity-related risk factors"""
        risk_score = 0.0
        
        # Background check results
        background_results = data.get('crew_results', {}).get('background_check', {})
        findings = background_results.get('findings', {})
        
        # Identity verification
        if findings.get('identity_verification') != 'Identity confirmed':
            risk_score += 0.3
        
        # Criminal background
        criminal_bg = findings.get('criminal_background', '')
        if 'criminal records found' in criminal_bg.lower():
            risk_score += 0.4
        
        # Address history
        address_history = findings.get('address_history', [])
        if len(address_history) == 0:
            risk_score += 0.2
        elif len(address_history) > 10:  # Too many addresses might be suspicious
            risk_score += 0.1
        
        # Social media presence
        social_media = findings.get('social_media_presence', '')
        if 'no social media' in social_media.lower():
            risk_score += 0.1
        
        return min(risk_score, 1.0)
    
    def score_financial_risk(self, data: Dict[str, Any]) -> float:
        """Score financial-related risk factors"""
        risk_score = 0.0
        
        # Financial crew results
        financial_results = data.get('crew_results', {}).get('financial_analysis', {})
        findings = financial_results.get('findings', {})
        
        # Credit score
        credit_score = findings.get('credit_score', 0)
        if credit_score < 600:
            risk_score += 0.4
        elif credit_score < 700:
            risk_score += 0.2
        
        # Suspicious activities
        suspicious_activities = findings.get('suspicious_activities', [])
        risk_score += len(suspicious_activities) * 0.2
        
        # Transaction patterns
        transaction_patterns = findings.get('transaction_patterns', '')
        if 'suspicious' in transaction_patterns.lower():
            risk_score += 0.3
        
        # ML financial risk score
        ml_financial = data.get('ml_predictions', {}).get('financial_risk_score', {})
        if 'prediction' in ml_financial:
            ml_risk = ml_financial['prediction'].get('risk_probability', 0)
            risk_score += ml_risk * 0.5
        
        return min(risk_score, 1.0)
    
    def score_digital_risk(self, data: Dict[str, Any]) -> float:
        """Score digital footprint-related risk factors"""
        risk_score = 0.0
        
        # Domain analysis
        domain_results = data.get('crew_results', {}).get('domain_analysis', {})
        domain_findings = domain_results.get('findings', {})
        
        # Domain age
        domain_age = domain_findings.get('domain_age', '')
        if 'recent registration' in domain_age.lower():
            risk_score += 0.3
        
        # Risk indicators
        risk_indicators = domain_findings.get('risk_indicators', [])
        risk_score += len(risk_indicators) * 0.1
        
        # Email analysis
        email_results = data.get('crew_results', {}).get('email_analysis', {})
        email_findings = email_results.get('findings', {})
        
        # Phishing indicators
        phishing_indicators = email_findings.get('phishing_indicators', [])
        risk_score += len(phishing_indicators) * 0.15
        
        # ML domain risk score
        ml_domain = data.get('ml_predictions', {}).get('domain_fraud_score', {})
        if 'prediction' in ml_domain:
            ml_risk = ml_domain['prediction'].get('fraud_probability', 0)
            risk_score += ml_risk * 0.4
        
        return min(risk_score, 1.0)
    
    def score_compliance_risk(self, data: Dict[str, Any]) -> float:
        """Score compliance-related risk factors"""
        risk_score = 0.0
        
        # Compliance screening results
        compliance_results = data.get('crew_results', {}).get('compliance_screening', {})
        findings = compliance_results.get('findings', {})
        
        # Sanctions screening
        sanctions_status = findings.get('sanctions_screening', '')
        if 'matches found' in sanctions_status.lower():
            risk_score += 0.8
        
        # PEP screening
        pep_status = findings.get('pep_screening', '')
        if 'politically exposed person' in pep_status.lower():
            risk_score += 0.6
        
        # Watchlist screening
        watchlist_status = findings.get('watchlist_screening', '')
        if 'matches' in watchlist_status.lower():
            risk_score += 0.7
        
        # Adverse media
        adverse_media = findings.get('adverse_media', '')
        if 'negative media' in adverse_media.lower():
            risk_score += 0.4
        
        # OpenSanctions API results
        opensanctions_data = data.get('api_responses', {}).get('opensanctions', {})
        if opensanctions_data.get('status') == 'success':
            sanctions_data = opensanctions_data.get('data', {})
            total_matches = sanctions_data.get('total_matches', 0)
            if total_matches > 0:
                risk_score += min(total_matches * 0.3, 0.9)
        
        return min(risk_score, 1.0)
    
    def score_threat_risk(self, data: Dict[str, Any]) -> float:
        """Score security threat-related risk factors"""
        risk_score = 0.0
        
        # Threat assessment results
        threat_results = data.get('crew_results', {}).get('threat_assessment', {})
        findings = threat_results.get('findings', {})
        
        # Threat level
        threat_level = findings.get('threat_level', 'LOW')
        if threat_level == 'HIGH':
            risk_score += 0.8
        elif threat_level == 'MEDIUM':
            risk_score += 0.5
        
        # Security incidents
        security_incidents = findings.get('security_incidents', '')
        if 'incidents found' in security_incidents.lower():
            risk_score += 0.6
        
        # Malware associations
        malware_associations = findings.get('malware_associations', '')
        if 'malware connections' in malware_associations.lower():
            risk_score += 0.7
        
        # Shodan infrastructure analysis
        shodan_data = data.get('api_responses', {}).get('shodan', {})
        if shodan_data.get('status') == 'success':
            shodan_findings = shodan_data.get('data', {})
            vulnerabilities = shodan_findings.get('vulnerabilities', [])
            risk_score += len(vulnerabilities) * 0.2
        
        return min(risk_score, 1.0)
    
    def calculate_weighted_score(self, risk_factors: Dict[str, float]) -> float:
        """Calculate weighted overall risk score"""
        weighted_score = 0.0
        
        for factor, score in risk_factors.items():
            weight = self.risk_weights.get(factor, 0.0)
            weighted_score += score * weight
        
        return min(weighted_score, 1.0)
    
    def determine_risk_level(self, overall_score: float) -> RiskLevel:
        """Determine risk level from overall score"""
        if overall_score >= 0.8:
            return RiskLevel.CRITICAL
        elif overall_score >= 0.6:
            return RiskLevel.HIGH
        elif overall_score >= 0.3:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def calculate_confidence(self, data: Dict[str, Any]) -> float:
        """Calculate confidence in risk assessment"""
        confidence_factors = []
        
        # Data completeness
        validator = DataValidator()
        validation_result = validator.validate(data)
        confidence_factors.append(validation_result.completeness_score)
        confidence_factors.append(validation_result.quality_score)
        
        # ML prediction confidence
        ml_predictions = data.get('ml_predictions', {})
        ml_confidences = []
        
        for prediction in ml_predictions.values():
            if isinstance(prediction, dict) and 'prediction' in prediction:
                confidence = prediction['prediction'].get('confidence', 0)
                ml_confidences.append(confidence)
        
        if ml_confidences:
            avg_ml_confidence = statistics.mean(ml_confidences)
            confidence_factors.append(avg_ml_confidence)
        
        # API success rate
        api_responses = data.get('api_responses', {})
        if api_responses:
            successful_apis = sum(1 for response in api_responses.values() 
                                if response.get('status') == 'success')
            api_success_rate = successful_apis / len(api_responses)
            confidence_factors.append(api_success_rate)
        
        return statistics.mean(confidence_factors) if confidence_factors else 0.5
    
    def identify_risk_indicators(self, data: Dict[str, Any], risk_factors: Dict[str, float]) -> List[str]:
        """Identify specific risk indicators"""
        indicators = []
        
        # High-risk factors
        for factor, score in risk_factors.items():
            if score >= 0.6:
                indicators.append(f"High {factor.replace('_', ' ')}: {score:.2f}")
        
        # Specific findings
        crew_results = data.get('crew_results', {})
        
        # Domain risk indicators
        domain_results = crew_results.get('domain_analysis', {})
        domain_risk_indicators = domain_results.get('findings', {}).get('risk_indicators', [])
        indicators.extend(domain_risk_indicators)
        
        # Email phishing indicators
        email_results = crew_results.get('email_analysis', {})
        phishing_indicators = email_results.get('findings', {}).get('phishing_indicators', [])
        indicators.extend(phishing_indicators)
        
        # Financial suspicious activities
        financial_results = crew_results.get('financial_analysis', {})
        suspicious_activities = financial_results.get('findings', {}).get('suspicious_activities', [])
        indicators.extend(suspicious_activities)
        
        return list(set(indicators))  # Remove duplicates
    
    def generate_mitigation_recommendations(self, risk_factors: Dict[str, float], 
                                          risk_level: RiskLevel) -> List[str]:
        """Generate risk mitigation recommendations"""
        recommendations = []
        
        if risk_level == RiskLevel.CRITICAL:
            recommendations.append("IMMEDIATE ACTION REQUIRED: Block all transactions and escalate to security team")
            recommendations.append("Conduct enhanced due diligence investigation")
            recommendations.append("Report to relevant regulatory authorities if required")
        
        elif risk_level == RiskLevel.HIGH:
            recommendations.append("Enhanced monitoring and verification required")
            recommendations.append("Require additional documentation before proceeding")
            recommendations.append("Consider transaction limits and enhanced controls")
        
        elif risk_level == RiskLevel.MEDIUM:
            recommendations.append("Implement additional verification steps")
            recommendations.append("Monitor for suspicious activity patterns")
            recommendations.append("Consider periodic re-evaluation")
        
        else:  # LOW risk
            recommendations.append("Standard monitoring procedures sufficient")
            recommendations.append("Proceed with normal business relationship")
            recommendations.append("Schedule routine periodic review")
        
        # Specific recommendations based on risk factors
        if risk_factors.get('identity_risk', 0) >= 0.5:
            recommendations.append("Verify identity through additional documentation")
            recommendations.append("Conduct enhanced background screening")
        
        if risk_factors.get('financial_risk', 0) >= 0.5:
            recommendations.append("Review financial history and credit reports")
            recommendations.append("Implement transaction monitoring controls")
        
        if risk_factors.get('compliance_risk', 0) >= 0.5:
            recommendations.append("Conduct enhanced sanctions and PEP screening")
            recommendations.append("Review adverse media and regulatory actions")
        
        return recommendations

class EvidenceChainBuilder:
    """Builds comprehensive evidence chain for investigations"""
    
    def build_evidence_chain(self, data: Dict[str, Any]) -> List[EvidenceItem]:
        """Build complete evidence chain from investigation data"""
        evidence_chain = []
        
        # CrewAI agent evidence
        crew_results = data.get('crew_results', {})
        for agent_type, results in crew_results.items():
            evidence_items = self._extract_crew_evidence(agent_type, results)
            evidence_chain.extend(evidence_items)
        
        # API response evidence
        api_responses = data.get('api_responses', {})
        for api_name, response in api_responses.items():
            evidence_items = self._extract_api_evidence(api_name, response)
            evidence_chain.extend(evidence_items)
        
        # ML prediction evidence
        ml_predictions = data.get('ml_predictions', {})
        for prediction_type, prediction in ml_predictions.items():
            evidence_items = self._extract_ml_evidence(prediction_type, prediction)
            evidence_chain.extend(evidence_items)
        
        # Sort by timestamp
        evidence_chain.sort(key=lambda x: x.timestamp, reverse=True)
        
        return evidence_chain
    
    def _extract_crew_evidence(self, agent_type: str, results: Dict[str, Any]) -> List[EvidenceItem]:
        """Extract evidence from CrewAI agent results"""
        evidence_items = []
        
        if not results:
            return evidence_items
        
        findings = results.get('findings', {})
        risk_assessment = results.get('risk_assessment', {})
        
        # Main finding
        agent_name = results.get('agent', agent_type.replace('_', ' ').title())
        risk_level = risk_assessment.get('level', 'UNKNOWN')
        confidence = risk_assessment.get('confidence', 0.5)
        
        evidence_items.append(EvidenceItem(
            source=f"CrewAI {agent_name}",
            data_type="Agent Analysis",
            finding=f"Risk Level: {risk_level}",
            confidence=confidence,
            timestamp=datetime.now(),
            verification_status="AI Analysis"
        ))
        
        # Specific findings
        for key, value in findings.items():
            if isinstance(value, (str, int, float)) and value:
                evidence_items.append(EvidenceItem(
                    source=f"CrewAI {agent_name}",
                    data_type=key.replace('_', ' ').title(),
                    finding=str(value),
                    confidence=confidence,
                    timestamp=datetime.now(),
                    verification_status="AI Analysis"
                ))
        
        return evidence_items
    
    def _extract_api_evidence(self, api_name: str, response: Dict[str, Any]) -> List[EvidenceItem]:
        """Extract evidence from API responses"""
        evidence_items = []
        
        if response.get('status') != 'success':
            return evidence_items
        
        api_data = response.get('data', {})
        
        # API-specific evidence extraction
        if api_name == 'opensanctions':
            sanctions_matches = api_data.get('sanctions_matches', [])
            pep_matches = api_data.get('pep_matches', [])
            
            if sanctions_matches:
                evidence_items.append(EvidenceItem(
                    source="OpenSanctions API",
                    data_type="Sanctions Screening",
                    finding=f"Found {len(sanctions_matches)} sanctions matches",
                    confidence=0.95,
                    timestamp=datetime.now(),
                    verification_status="External Database"
                ))
            
            if pep_matches:
                evidence_items.append(EvidenceItem(
                    source="OpenSanctions API",
                    data_type="PEP Screening",
                    finding=f"Found {len(pep_matches)} PEP matches",
                    confidence=0.95,
                    timestamp=datetime.now(),
                    verification_status="External Database"
                ))
        
        elif api_name == 'whoisxml':
            domain_info = api_data.get('domain_info', {})
            if domain_info:
                creation_date = domain_info.get('creation_date')
                registrar = domain_info.get('registrar')
                
                if creation_date:
                    evidence_items.append(EvidenceItem(
                        source="WhoisXML API",
                        data_type="Domain Registration",
                        finding=f"Domain created: {creation_date}, Registrar: {registrar}",
                        confidence=0.90,
                        timestamp=datetime.now(),
                        verification_status="Registry Data"
                    ))
        
        elif api_name == 'shodan':
            host_info = api_data.get('host_info', {})
            vulnerabilities = api_data.get('vulnerabilities', [])
            
            if host_info:
                country = host_info.get('country')
                organization = host_info.get('organization')
                
                evidence_items.append(EvidenceItem(
                    source="Shodan API",
                    data_type="Infrastructure Analysis",
                    finding=f"Host location: {country}, Organization: {organization}",
                    confidence=0.85,
                    timestamp=datetime.now(),
                    verification_status="Network Scan"
                ))
            
            if vulnerabilities:
                evidence_items.append(EvidenceItem(
                    source="Shodan API",
                    data_type="Security Vulnerabilities",
                    finding=f"Found {len(vulnerabilities)} vulnerabilities",
                    confidence=0.90,
                    timestamp=datetime.now(),
                    verification_status="Security Scan"
                ))
        
        return evidence_items
    
    def _extract_ml_evidence(self, prediction_type: str, prediction: Dict[str, Any]) -> List[EvidenceItem]:
        """Extract evidence from ML predictions"""
        evidence_items = []
        
        if 'prediction' not in prediction:
            return evidence_items
        
        pred_data = prediction['prediction']
        model_name = prediction.get('model', prediction_type.replace('_', ' ').title())
        
        fraud_prob = pred_data.get('fraud_probability') or pred_data.get('risk_probability', 0)
        risk_level = pred_data.get('risk_level', 'UNKNOWN')
        confidence = pred_data.get('confidence', 0.5)
        
        evidence_items.append(EvidenceItem(
            source=f"ML Model: {model_name}",
            data_type="Machine Learning Prediction",
            finding=f"Risk Level: {risk_level}, Probability: {fraud_prob:.2f}",
            confidence=confidence,
            timestamp=datetime.now(),
            verification_status="AI Prediction"
        ))
        
        return evidence_items

class ReportDataProcessor:
    """Main data processor for investigation reports"""
    
    def __init__(self):
        self.validator = DataValidator()
        self.risk_scorer = RiskScorer()
        self.evidence_builder = EvidenceChainBuilder()
    
    def process_investigation_data(self, raw_data: Dict[str, Any]) -> ProcessedInvestigationData:
        """Process and validate all investigation data"""
        logger.info(f"Processing investigation data for {raw_data.get('investigation_id', 'unknown')}")
        
        try:
            # Validate data
            validation_result = self.validator.validate(raw_data)
            if not validation_result.is_valid:
                logger.warning(f"Data validation issues: {validation_result.errors}")
            
            # Calculate risk assessment
            risk_assessment = self.risk_scorer.calculate_comprehensive_risk_assessment(raw_data)
            
            # Build evidence chain
            evidence_chain = self.evidence_builder.build_evidence_chain(raw_data)
            
            # Generate executive summary
            executive_summary = self.generate_executive_summary(raw_data, risk_assessment)
            
            # Structure detailed findings
            detailed_findings = self.structure_detailed_findings(raw_data)
            
            # Generate recommendations
            recommendations = self.generate_recommendations(raw_data, risk_assessment)
            
            # Determine compliance status
            compliance_status = self.determine_compliance_status(risk_assessment)
            
            # Generate processing metadata
            metadata = self.generate_processing_metadata(raw_data, validation_result)
            
            # Create processed data object
            processed_data = ProcessedInvestigationData(
                investigation_id=raw_data.get('investigation_id', 'unknown'),
                subject=raw_data.get('subject', 'unknown'),
                executive_summary=executive_summary,
                risk_assessment=risk_assessment,
                detailed_findings=detailed_findings,
                evidence_chain=evidence_chain,
                recommendations=recommendations,
                compliance_status=compliance_status,
                metadata=metadata,
                processed_at=datetime.now()
            )
            
            logger.info(f"Data processing completed for {processed_data.investigation_id}")
            return processed_data
            
        except Exception as e:
            logger.error(f"Error processing investigation data: {str(e)}")
            raise
    
    def generate_executive_summary(self, raw_data: Dict[str, Any], 
                                 risk_assessment: RiskAssessment) -> Dict[str, Any]:
        """Generate executive summary"""
        subject = raw_data.get('subject', 'Unknown')
        investigation_type = raw_data.get('investigation_type', 'comprehensive')
        
        # Key findings from crew results
        key_findings = []
        crew_results = raw_data.get('crew_results', {})
        
        for agent_type, results in crew_results.items():
            if results and 'risk_assessment' in results:
                agent_risk = results['risk_assessment'].get('level', 'LOW')
                if agent_risk in ['HIGH', 'CRITICAL']:
                    agent_name = agent_type.replace('_', ' ').title()
                    key_findings.append(f"{agent_name}: {agent_risk} risk identified")
        
        # Data source summary
        api_responses = raw_data.get('api_responses', {})
        successful_apis = [api for api, response in api_responses.items() 
                          if response.get('status') == 'success']
        
        return {
            'subject': subject,
            'investigation_type': investigation_type.title(),
            'overall_risk_level': risk_assessment.risk_level.value,
            'overall_risk_score': risk_assessment.overall_score,
            'confidence_level': risk_assessment.confidence,
            'key_findings': key_findings[:5],  # Top 5 findings
            'data_sources_used': len(successful_apis),
            'investigation_date': datetime.now().strftime('%Y-%m-%d'),
            'summary_statement': self._generate_summary_statement(risk_assessment)
        }
    
    def _generate_summary_statement(self, risk_assessment: RiskAssessment) -> str:
        """Generate natural language summary statement"""
        risk_level = risk_assessment.risk_level.value
        confidence = risk_assessment.confidence
        
        if risk_level == 'CRITICAL':
            return f"Investigation reveals CRITICAL risk factors with {confidence:.0%} confidence. Immediate action required."
        elif risk_level == 'HIGH':
            return f"Investigation identifies HIGH risk profile with {confidence:.0%} confidence. Enhanced due diligence recommended."
        elif risk_level == 'MEDIUM':
            return f"Investigation shows MEDIUM risk indicators with {confidence:.0%} confidence. Additional verification suggested."
        else:
            return f"Investigation indicates LOW risk profile with {confidence:.0%} confidence. Standard procedures sufficient."
    
    def structure_detailed_findings(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Structure detailed findings by category"""
        detailed_findings = {
            'identity_verification': self._extract_identity_findings(raw_data),
            'digital_footprint': self._extract_digital_findings(raw_data),
            'financial_intelligence': self._extract_financial_findings(raw_data),
            'compliance_screening': self._extract_compliance_findings(raw_data),
            'threat_assessment': self._extract_threat_findings(raw_data),
            'background_check': self._extract_background_findings(raw_data)
        }
        
        return detailed_findings
    
    def _extract_identity_findings(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract identity verification findings"""
        background_results = raw_data.get('crew_results', {}).get('background_check', {})
        findings = background_results.get('findings', {})
        
        return {
            'identity_status': findings.get('identity_verification', 'Unknown'),
            'address_history': findings.get('address_history', []),
            'employment_history': findings.get('employment_history', 'Not available'),
            'education_verification': findings.get('education_verification', 'Not verified'),
            'social_media_presence': findings.get('social_media_presence', 'Not found'),
            'public_records': findings.get('public_records', {})
        }
    
    def _extract_digital_findings(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract digital footprint findings"""
        domain_results = raw_data.get('crew_results', {}).get('domain_analysis', {})
        email_results = raw_data.get('crew_results', {}).get('email_analysis', {})
        
        domain_findings = domain_results.get('findings', {})
        email_findings = email_results.get('findings', {})
        
        return {
            'domain_analysis': {
                'domain_age': domain_findings.get('domain_age', 'Unknown'),
                'ssl_certificate': domain_findings.get('ssl_certificate', 'Not checked'),
                'dns_configuration': domain_findings.get('dns_configuration', 'Unknown'),
                'reputation_score': domain_findings.get('reputation_score', 0),
                'risk_indicators': domain_findings.get('risk_indicators', [])
            },
            'email_analysis': {
                'email_validity': email_findings.get('email_validity', 'Unknown'),
                'domain_verification': email_findings.get('domain_verification', 'Not verified'),
                'authentication_status': email_findings.get('header_analysis', {}).get('authentication_results', 'Unknown'),
                'phishing_indicators': email_findings.get('phishing_indicators', [])
            }
        }
    
    def _extract_financial_findings(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract financial intelligence findings"""
        financial_results = raw_data.get('crew_results', {}).get('financial_analysis', {})
        findings = financial_results.get('findings', {})
        
        return {
            'credit_score': findings.get('credit_score', 0),
            'financial_history': findings.get('financial_history', 'Unknown'),
            'transaction_patterns': findings.get('transaction_patterns', 'Unknown'),
            'suspicious_activities': findings.get('suspicious_activities', []),
            'asset_verification': findings.get('asset_verification', {})
        }
    
    def _extract_compliance_findings(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract compliance screening findings"""
        compliance_results = raw_data.get('crew_results', {}).get('compliance_screening', {})
        findings = compliance_results.get('findings', {})
        
        # Also check OpenSanctions API results
        opensanctions_data = raw_data.get('api_responses', {}).get('opensanctions', {})
        sanctions_data = opensanctions_data.get('data', {}) if opensanctions_data.get('status') == 'success' else {}
        
        return {
            'sanctions_screening': findings.get('sanctions_screening', 'Not screened'),
            'pep_screening': findings.get('pep_screening', 'Not screened'),
            'watchlist_screening': findings.get('watchlist_screening', 'Not screened'),
            'adverse_media': findings.get('adverse_media', 'Not checked'),
            'compliance_status': findings.get('compliance_status', 'Unknown'),
            'external_sanctions_matches': sanctions_data.get('total_matches', 0),
            'screening_databases': findings.get('screening_databases', [])
        }
    
    def _extract_threat_findings(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract threat assessment findings"""
        threat_results = raw_data.get('crew_results', {}).get('threat_assessment', {})
        findings = threat_results.get('findings', {})
        
        return {
            'threat_level': findings.get('threat_level', 'Unknown'),
            'security_incidents': findings.get('security_incidents', 'Not checked'),
            'malware_associations': findings.get('malware_associations', 'Not found'),
            'infrastructure_analysis': findings.get('infrastructure_analysis', {}),
            'vulnerabilities': []  # Will be populated from Shodan data
        }
    
    def _extract_background_findings(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract background check findings"""
        background_results = raw_data.get('crew_results', {}).get('background_check', {})
        findings = background_results.get('findings', {})
        
        return {
            'criminal_background': findings.get('criminal_background', 'Not checked'),
            'employment_verification': findings.get('employment_history', 'Not verified'),
            'education_verification': findings.get('education_verification', 'Not verified'),
            'reference_checks': 'Not performed',  # Future enhancement
            'professional_licenses': 'Not checked'  # Future enhancement
        }
    
    def generate_recommendations(self, raw_data: Dict[str, Any], 
                               risk_assessment: RiskAssessment) -> List[str]:
        """Generate comprehensive recommendations"""
        recommendations = []
        
        # Add risk-based recommendations
        recommendations.extend(risk_assessment.mitigation_recommendations)
        
        # Add specific recommendations based on findings
        crew_results = raw_data.get('crew_results', {})
        
        for agent_type, results in crew_results.items():
            if results and 'recommendations' in results:
                agent_recommendations = results['recommendations']
                if isinstance(agent_recommendations, list):
                    recommendations.extend(agent_recommendations)
        
        # Remove duplicates and limit to top recommendations
        unique_recommendations = list(dict.fromkeys(recommendations))
        return unique_recommendations[:10]  # Top 10 recommendations
    
    def determine_compliance_status(self, risk_assessment: RiskAssessment) -> ComplianceStatus:
        """Determine overall compliance status"""
        risk_level = risk_assessment.risk_level
        compliance_risk = risk_assessment.risk_factors.get('compliance_risk', 0)
        
        if risk_level == RiskLevel.CRITICAL or compliance_risk >= 0.8:
            return ComplianceStatus.BLOCKED
        elif risk_level == RiskLevel.HIGH or compliance_risk >= 0.5:
            return ComplianceStatus.REVIEW
        else:
            return ComplianceStatus.CLEAR
    
    def generate_processing_metadata(self, raw_data: Dict[str, Any], 
                                   validation_result: ValidationResult) -> Dict[str, Any]:
        """Generate processing metadata"""
        return {
            'processing_timestamp': datetime.now().isoformat(),
            'data_quality': {
                'completeness_score': validation_result.completeness_score,
                'quality_score': validation_result.quality_score,
                'validation_errors': len(validation_result.errors),
                'validation_warnings': len(validation_result.warnings)
            },
            'data_sources': {
                'crew_agents': len(raw_data.get('crew_results', {})),
                'api_responses': len(raw_data.get('api_responses', {})),
                'ml_predictions': len(raw_data.get('ml_predictions', {}))
            },
            'processing_version': '1.0.0',
            'processor': 'ScamShield AI Report Engine'
        }

# Example usage and testing
if __name__ == "__main__":
    def test_data_processor():
        """Test the data processor"""
        # Sample raw investigation data
        sample_data = {
            'investigation_id': 'test_001',
            'subject': 'john.doe@example.com',
            'investigation_type': 'comprehensive',
            'crew_results': {
                'domain_analysis': {
                    'agent': 'Domain Specialist',
                    'findings': {
                        'domain_age': 'Recent registration (< 30 days)',
                        'risk_indicators': ['Recent registration', 'Suspicious TLD']
                    },
                    'risk_assessment': {'level': 'MEDIUM', 'confidence': 0.85}
                },
                'background_check': {
                    'agent': 'Background Specialist',
                    'findings': {
                        'identity_verification': 'Identity confirmed',
                        'criminal_background': 'No criminal records found'
                    },
                    'risk_assessment': {'level': 'LOW', 'confidence': 0.92}
                }
            },
            'api_responses': {
                'opensanctions': {
                    'status': 'success',
                    'data': {'total_matches': 0}
                }
            },
            'ml_predictions': {
                'overall_risk_score': {
                    'prediction': {
                        'risk_probability': 0.25,
                        'risk_level': 'LOW',
                        'confidence': 0.87
                    }
                }
            },
            'metadata': {
                'investigation_id': 'test_001',
                'subject': 'john.doe@example.com'
            }
        }
        
        # Process the data
        processor = ReportDataProcessor()
        processed_data = processor.process_investigation_data(sample_data)
        
        print("✅ Data Processing Test Complete")
        print(f"📊 Risk Level: {processed_data.risk_assessment.risk_level.value}")
        print(f"🎯 Risk Score: {processed_data.risk_assessment.overall_score:.2f}")
        print(f"🔍 Evidence Items: {len(processed_data.evidence_chain)}")
        print(f"📋 Recommendations: {len(processed_data.recommendations)}")
        print(f"✅ Compliance Status: {processed_data.compliance_status.value}")
        
        # Save processed data
        from pathlib import Path
        output_file = Path(__file__).parent / "test_processed_data.json"
        with open(output_file, 'w') as f:
            json.dump(processed_data.to_dict(), f, indent=2)
        
        print(f"💾 Processed data saved to: {output_file}")
        
        return processed_data
    
    # Run test
    test_data_processor()

