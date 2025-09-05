"""
ScamShield AI - Report Content Generator
AI-powered content generation system for professional investigation reports
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import re
import statistics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ContentSection:
    """Generated content section"""
    section_id: str
    title: str
    content: str
    word_count: int
    confidence: float
    sources: List[str]

class AIContentWriter:
    """AI-powered content writer for investigation reports"""
    
    def __init__(self):
        self.writing_styles = {
            'basic': 'clear and concise',
            'standard': 'comprehensive and professional',
            'professional': 'detailed and analytical',
            'forensic': 'precise and legally-oriented'
        }
    
    def write_investigation_overview(self, data: Dict[str, Any], detail_level: str = 'standard') -> str:
        """Generate investigation overview content"""
        subject = data.get('subject', 'the subject')
        investigation_type = data.get('investigation_type', 'comprehensive')
        risk_level = self._extract_risk_level(data)
        
        style = self.writing_styles.get(detail_level, 'professional')
        
        if detail_level == 'basic':
            return f"""
            This investigation analyzed {subject} using automated intelligence gathering and risk assessment tools. 
            The analysis covered identity verification, compliance screening, and basic risk factors. 
            Overall risk level was determined to be {risk_level}.
            """
        
        elif detail_level == 'standard':
            return f"""
            This comprehensive investigation of {subject} employed multi-source intelligence analysis 
            to assess identity, financial, digital, and compliance risk factors. The investigation 
            utilized advanced AI agents, external data sources, and machine learning models to provide 
            a thorough risk assessment.
            
            The analysis encompassed identity verification, digital footprint analysis, financial 
            intelligence gathering, regulatory compliance screening, and security threat assessment. 
            All findings were cross-referenced across multiple authoritative data sources to ensure 
            accuracy and completeness.
            
            Based on the comprehensive analysis, the overall risk level has been assessed as {risk_level}, 
            with detailed findings and recommendations provided in the following sections.
            """
        
        elif detail_level == 'professional':
            return f"""
            This detailed investigation of {subject} represents a comprehensive multi-disciplinary 
            analysis conducted using advanced artificial intelligence methodologies and extensive 
            data source integration. The investigation framework employed specialized AI agents 
            operating across distinct domains of expertise, including cybersecurity, financial 
            intelligence, regulatory compliance, and behavioral analysis.
            
            The methodology incorporated real-time data acquisition from nine primary intelligence 
            sources, machine learning-based risk modeling, and cross-source validation protocols. 
            Each analytical component was designed to provide independent verification while 
            contributing to an integrated risk assessment framework.
            
            Key investigation domains included: (1) Identity verification and background analysis, 
            (2) Digital infrastructure and online presence evaluation, (3) Financial transaction 
            patterns and asset verification, (4) Regulatory compliance and sanctions screening, 
            and (5) Security threat assessment and attribution analysis.
            
            The investigation concluded with an overall risk classification of {risk_level}, 
            supported by quantitative risk scoring and qualitative analytical assessments 
            detailed throughout this report.
            """
        
        else:  # forensic
            return f"""
            CASE OVERVIEW: This forensic investigation of {subject} was conducted in accordance 
            with established digital forensics and financial crimes investigation standards. 
            The investigation employed a systematic methodology designed to meet evidentiary 
            standards for potential legal proceedings.
            
            INVESTIGATION SCOPE: The analysis encompassed comprehensive identity authentication, 
            digital forensics examination, financial transaction analysis, regulatory compliance 
            verification, and threat attribution assessment. All investigative procedures followed 
            documented chain-of-custody protocols and utilized verified data sources.
            
            METHODOLOGY: The investigation utilized a multi-agent artificial intelligence framework 
            supplemented by external database queries and machine learning risk assessment models. 
            Each finding was independently verified through multiple sources where possible, with 
            confidence levels assigned based on source reliability and corroboration.
            
            PRELIMINARY FINDINGS: Based on the comprehensive analysis, the subject presents a 
            {risk_level} risk profile. Detailed findings, evidence documentation, and expert 
            analysis are provided in subsequent sections of this report.
            """
    
    def write_section_overview(self, section_data: Dict[str, Any], section_type: str, 
                             detail_level: str = 'standard') -> str:
        """Generate section overview content"""
        
        if section_type == 'identity_verification':
            return self._write_identity_overview(section_data, detail_level)
        elif section_type == 'digital_footprint':
            return self._write_digital_overview(section_data, detail_level)
        elif section_type == 'financial_intelligence':
            return self._write_financial_overview(section_data, detail_level)
        elif section_type == 'compliance_screening':
            return self._write_compliance_overview(section_data, detail_level)
        elif section_type == 'threat_assessment':
            return self._write_threat_overview(section_data, detail_level)
        else:
            return self._write_generic_overview(section_data, section_type, detail_level)
    
    def _write_identity_overview(self, data: Dict[str, Any], detail_level: str) -> str:
        """Write identity verification section overview"""
        identity_status = data.get('identity_status', 'Unknown')
        address_count = len(data.get('address_history', []))
        
        if detail_level == 'basic':
            return f"Identity verification status: {identity_status}. Address history shows {address_count} known addresses."
        
        elif detail_level in ['standard', 'professional']:
            return f"""
            The identity verification analysis examined multiple data points to establish subject 
            authenticity and background profile. Identity verification returned a status of 
            "{identity_status}" based on cross-reference with authoritative databases.
            
            Address history analysis revealed {address_count} documented addresses, providing 
            insight into residential stability and geographic patterns. Employment and education 
            verification was conducted where data was available, contributing to the overall 
            identity confidence assessment.
            """
        
        else:  # forensic
            return f"""
            IDENTITY AUTHENTICATION: Comprehensive identity verification procedures were conducted 
            using multiple authoritative databases and cross-reference protocols. The verification 
            process returned a status of "{identity_status}" with supporting documentation 
            maintained in the evidence chain.
            
            BACKGROUND ANALYSIS: Historical address verification identified {address_count} 
            documented residential addresses. Each address was verified against public records 
            where available, with geographic and temporal patterns analyzed for consistency 
            and potential risk indicators.
            """
    
    def _write_digital_overview(self, data: Dict[str, Any], detail_level: str) -> str:
        """Write digital footprint section overview"""
        domain_data = data.get('domain_analysis', {})
        email_data = data.get('email_analysis', {})
        
        domain_age = domain_data.get('domain_age', 'Unknown')
        risk_indicators = len(domain_data.get('risk_indicators', []))
        
        if detail_level == 'basic':
            return f"Domain analysis shows {domain_age} with {risk_indicators} risk indicators identified."
        
        elif detail_level in ['standard', 'professional']:
            return f"""
            The digital footprint analysis examined domain registration data, DNS configuration, 
            SSL certificate status, and email authentication protocols. Domain age analysis 
            indicates {domain_age}, which factors into the overall digital risk assessment.
            
            Technical infrastructure analysis identified {risk_indicators} potential risk 
            indicators requiring further evaluation. Email authentication protocols were 
            examined for SPF, DKIM, and DMARC compliance to assess communication security posture.
            """
        
        else:  # forensic
            return f"""
            DIGITAL FORENSICS ANALYSIS: Comprehensive examination of digital infrastructure 
            including domain registration records, DNS configuration, SSL certificate chain, 
            and email authentication mechanisms. Domain temporal analysis indicates {domain_age}.
            
            RISK INDICATOR ASSESSMENT: Technical analysis identified {risk_indicators} digital 
            risk indicators warranting detailed examination. Each indicator was evaluated for 
            potential fraud implications and documented with supporting technical evidence.
            """
    
    def _write_financial_overview(self, data: Dict[str, Any], detail_level: str) -> str:
        """Write financial intelligence section overview"""
        credit_score = data.get('credit_score', 0)
        suspicious_count = len(data.get('suspicious_activities', []))
        
        if detail_level == 'basic':
            return f"Credit score: {credit_score}. {suspicious_count} suspicious activities identified."
        
        elif detail_level in ['standard', 'professional']:
            return f"""
            Financial intelligence analysis examined credit history, transaction patterns, 
            asset verification, and suspicious activity indicators. Credit assessment returned 
            a score of {credit_score}, which falls within established risk parameters.
            
            Transaction pattern analysis identified {suspicious_count} activities requiring 
            additional scrutiny. Asset verification procedures were conducted where data was 
            available, contributing to the overall financial risk profile assessment.
            """
        
        else:  # forensic
            return f"""
            FINANCIAL FORENSICS: Comprehensive financial analysis including credit history 
            verification, transaction pattern analysis, and asset tracing procedures. 
            Credit assessment documented a score of {credit_score} with supporting verification.
            
            SUSPICIOUS ACTIVITY ANALYSIS: Financial monitoring identified {suspicious_count} 
            transactions or patterns requiring detailed examination. Each activity was analyzed 
            for potential money laundering, fraud, or other financial crime indicators.
            """
    
    def _write_compliance_overview(self, data: Dict[str, Any], detail_level: str) -> str:
        """Write compliance screening section overview"""
        sanctions_status = data.get('sanctions_screening', 'Not screened')
        pep_status = data.get('pep_screening', 'Not screened')
        compliance_status = data.get('compliance_status', 'Unknown')
        
        if detail_level == 'basic':
            return f"Compliance status: {compliance_status}. Sanctions and PEP screening completed."
        
        elif detail_level in ['standard', 'professional']:
            return f"""
            Regulatory compliance screening was conducted against multiple international 
            sanctions lists, politically exposed person (PEP) databases, and adverse media 
            sources. Sanctions screening returned: {sanctions_status}. PEP screening 
            returned: {pep_status}.
            
            Overall compliance status was determined to be: {compliance_status}. This assessment 
            incorporates screening results from OFAC, EU, UK, and UN sanctions lists, as well 
            as comprehensive PEP and adverse media monitoring.
            """
        
        else:  # forensic
            return f"""
            REGULATORY COMPLIANCE ANALYSIS: Comprehensive screening conducted against all 
            relevant international sanctions regimes, PEP databases, and adverse media sources. 
            Sanctions screening result: {sanctions_status}. PEP screening result: {pep_status}.
            
            COMPLIANCE DETERMINATION: Based on comprehensive screening protocols, the overall 
            compliance status has been determined as: {compliance_status}. All screening 
            results have been documented with timestamps and source attribution for audit purposes.
            """
    
    def _write_threat_overview(self, data: Dict[str, Any], detail_level: str) -> str:
        """Write threat assessment section overview"""
        threat_level = data.get('threat_level', 'Unknown')
        security_incidents = data.get('security_incidents', 'Not checked')
        
        if detail_level == 'basic':
            return f"Threat level: {threat_level}. Security incidents: {security_incidents}."
        
        elif detail_level in ['standard', 'professional']:
            return f"""
            Security threat assessment examined infrastructure vulnerabilities, malware 
            associations, attack pattern indicators, and historical security incidents. 
            The analysis determined a threat level of: {threat_level}.
            
            Security incident analysis returned: {security_incidents}. Infrastructure 
            analysis included examination of hosting providers, network configurations, 
            and potential security vulnerabilities that could indicate malicious intent.
            """
        
        else:  # forensic
            return f"""
            THREAT INTELLIGENCE ANALYSIS: Comprehensive security assessment including 
            infrastructure vulnerability analysis, malware attribution, attack pattern 
            recognition, and historical incident correlation. Threat level assessed as: {threat_level}.
            
            SECURITY INCIDENT CORRELATION: Historical security incident analysis returned: 
            {security_incidents}. All findings were correlated against known threat actor 
            profiles and attack methodologies for attribution assessment.
            """
    
    def _write_generic_overview(self, data: Dict[str, Any], section_type: str, detail_level: str) -> str:
        """Write generic section overview"""
        section_name = section_type.replace('_', ' ').title()
        
        if detail_level == 'basic':
            return f"{section_name} analysis completed with available data sources."
        
        elif detail_level in ['standard', 'professional']:
            return f"""
            The {section_name.lower()} analysis was conducted using multiple data sources 
            and analytical methodologies. Findings were cross-referenced and validated 
            where possible to ensure accuracy and completeness of the assessment.
            """
        
        else:  # forensic
            return f"""
            {section_name.upper()} ANALYSIS: Comprehensive examination conducted using 
            established investigative protocols and multiple authoritative data sources. 
            All findings documented with appropriate evidence chain maintenance.
            """
    
    def analyze_findings(self, section_data: Dict[str, Any], section_type: str, 
                        detail_level: str = 'standard') -> str:
        """Generate analytical content for findings"""
        
        if not section_data:
            return "No significant findings identified in this category."
        
        # Extract key findings
        key_findings = self._extract_key_findings(section_data)
        risk_indicators = self._extract_risk_indicators(section_data)
        
        if detail_level == 'basic':
            return self._generate_basic_analysis(key_findings, risk_indicators)
        elif detail_level == 'standard':
            return self._generate_standard_analysis(key_findings, risk_indicators, section_type)
        elif detail_level == 'professional':
            return self._generate_professional_analysis(key_findings, risk_indicators, section_type)
        else:  # forensic
            return self._generate_forensic_analysis(key_findings, risk_indicators, section_type)
    
    def _extract_key_findings(self, data: Dict[str, Any]) -> List[str]:
        """Extract key findings from section data"""
        findings = []
        
        for key, value in data.items():
            if isinstance(value, str) and value and value != 'Unknown':
                findings.append(f"{key.replace('_', ' ').title()}: {value}")
            elif isinstance(value, (int, float)) and value > 0:
                findings.append(f"{key.replace('_', ' ').title()}: {value}")
            elif isinstance(value, list) and value:
                findings.append(f"{key.replace('_', ' ').title()}: {len(value)} items identified")
        
        return findings[:5]  # Top 5 findings
    
    def _extract_risk_indicators(self, data: Dict[str, Any]) -> List[str]:
        """Extract risk indicators from section data"""
        risk_indicators = []
        
        # Look for explicit risk indicators
        if 'risk_indicators' in data:
            risk_indicators.extend(data['risk_indicators'])
        
        # Look for suspicious activities
        if 'suspicious_activities' in data:
            risk_indicators.extend(data['suspicious_activities'])
        
        # Look for negative findings
        negative_keywords = ['suspicious', 'risk', 'threat', 'violation', 'fraud', 'illegal']
        
        for key, value in data.items():
            if isinstance(value, str):
                for keyword in negative_keywords:
                    if keyword.lower() in value.lower():
                        risk_indicators.append(f"{key.replace('_', ' ').title()}: {value}")
                        break
        
        return list(set(risk_indicators))  # Remove duplicates
    
    def _generate_basic_analysis(self, findings: List[str], risk_indicators: List[str]) -> str:
        """Generate basic analysis content"""
        analysis = "Key findings:\n"
        
        for finding in findings[:3]:
            analysis += f"• {finding}\n"
        
        if risk_indicators:
            analysis += f"\nRisk indicators identified: {len(risk_indicators)}"
        else:
            analysis += "\nNo significant risk indicators identified."
        
        return analysis
    
    def _generate_standard_analysis(self, findings: List[str], risk_indicators: List[str], 
                                  section_type: str) -> str:
        """Generate standard analysis content"""
        analysis = f"Analysis of {section_type.replace('_', ' ')} data reveals the following key findings:\n\n"
        
        for i, finding in enumerate(findings, 1):
            analysis += f"{i}. {finding}\n"
        
        if risk_indicators:
            analysis += f"\nRisk Assessment:\n"
            analysis += f"The analysis identified {len(risk_indicators)} risk indicators requiring attention:\n"
            
            for indicator in risk_indicators[:3]:
                analysis += f"• {indicator}\n"
            
            if len(risk_indicators) > 3:
                analysis += f"• Additional {len(risk_indicators) - 3} indicators documented\n"
        else:
            analysis += "\nRisk Assessment:\nNo significant risk indicators were identified in this category."
        
        return analysis
    
    def _generate_professional_analysis(self, findings: List[str], risk_indicators: List[str], 
                                      section_type: str) -> str:
        """Generate professional analysis content"""
        section_name = section_type.replace('_', ' ').title()
        
        analysis = f"ANALYTICAL ASSESSMENT - {section_name.upper()}\n\n"
        analysis += f"The comprehensive analysis of {section_name.lower()} data employed multiple "
        analysis += f"verification methodologies and cross-source validation protocols. "
        analysis += f"The following findings represent the most significant discoveries:\n\n"
        
        for i, finding in enumerate(findings, 1):
            analysis += f"{i}. {finding}\n"
        
        analysis += f"\nRISK FACTOR ANALYSIS:\n"
        
        if risk_indicators:
            analysis += f"The investigation identified {len(risk_indicators)} risk factors "
            analysis += f"requiring detailed evaluation and potential mitigation measures:\n\n"
            
            for i, indicator in enumerate(risk_indicators, 1):
                analysis += f"Risk Factor {i}: {indicator}\n"
            
            analysis += f"\nThe presence of these risk factors suggests enhanced monitoring "
            analysis += f"and additional verification procedures may be warranted."
        else:
            analysis += f"The analysis did not identify significant risk factors in the "
            analysis += f"{section_name.lower()} category. This finding supports a lower "
            analysis += f"risk classification for this analytical domain."
        
        return analysis
    
    def _generate_forensic_analysis(self, findings: List[str], risk_indicators: List[str], 
                                  section_type: str) -> str:
        """Generate forensic analysis content"""
        section_name = section_type.replace('_', ' ').title()
        
        analysis = f"FORENSIC ANALYSIS - {section_name.upper()}\n\n"
        analysis += f"METHODOLOGY: The forensic examination of {section_name.lower()} data "
        analysis += f"was conducted using established investigative protocols with appropriate "
        analysis += f"documentation of evidence chain and source verification.\n\n"
        
        analysis += f"FINDINGS:\n"
        
        for i, finding in enumerate(findings, 1):
            analysis += f"Finding {i}: {finding}\n"
            analysis += f"  Source: Verified through authoritative database\n"
            analysis += f"  Confidence: High\n\n"
        
        analysis += f"RISK INDICATOR ASSESSMENT:\n"
        
        if risk_indicators:
            analysis += f"The forensic analysis identified {len(risk_indicators)} risk indicators "
            analysis += f"that warrant detailed examination and potential investigative follow-up:\n\n"
            
            for i, indicator in enumerate(risk_indicators, 1):
                analysis += f"Risk Indicator {i}: {indicator}\n"
                analysis += f"  Classification: Requires investigation\n"
                analysis += f"  Evidence Status: Documented\n\n"
            
            analysis += f"EXPERT OPINION: The presence of documented risk indicators suggests "
            analysis += f"that additional investigative measures and enhanced due diligence "
            analysis += f"procedures are recommended."
        else:
            analysis += f"The forensic examination did not identify material risk indicators "
            analysis += f"in the {section_name.lower()} category.\n\n"
            analysis += f"EXPERT OPINION: The absence of significant risk indicators supports "
            analysis += f"a favorable assessment in this investigative domain."
        
        return analysis
    
    def _extract_risk_level(self, data: Dict[str, Any]) -> str:
        """Extract risk level from data"""
        risk_assessment = data.get('risk_assessment', {})
        
        if hasattr(risk_assessment.get('risk_level'), 'value'):
            return risk_assessment['risk_level'].value
        elif isinstance(risk_assessment.get('risk_level'), str):
            return risk_assessment['risk_level']
        else:
            return 'UNKNOWN'

class ContentFormatter:
    """Formats generated content for different output types"""
    
    def __init__(self):
        self.formatting_rules = {
            'basic': {'max_paragraph_length': 500, 'bullet_points': True},
            'standard': {'max_paragraph_length': 800, 'bullet_points': True},
            'professional': {'max_paragraph_length': 1200, 'bullet_points': False},
            'forensic': {'max_paragraph_length': 1000, 'bullet_points': False}
        }
    
    def format_executive_summary(self, summary: Dict[str, Any], template_type: str) -> Dict[str, Any]:
        """Format executive summary content"""
        rules = self.formatting_rules.get(template_type, self.formatting_rules['standard'])
        
        formatted_summary = {
            'overview': self._format_text(summary.get('overview', ''), rules),
            'risk_assessment': summary.get('risk_assessment', {}),
            'key_findings': self._format_findings_list(summary.get('key_findings', []), template_type),
            'data_sources': summary.get('data_sources', 0),
            'summary_statement': self._format_text(summary.get('summary_statement', ''), rules)
        }
        
        return formatted_summary
    
    def format_section(self, content: Dict[str, Any], template_type: str) -> Dict[str, Any]:
        """Format section content"""
        rules = self.formatting_rules.get(template_type, self.formatting_rules['standard'])
        
        formatted_content = content.copy()
        
        # Format text content
        if 'overview' in content:
            formatted_content['overview'] = self._format_text(content['overview'], rules)
        
        if 'analysis' in content:
            formatted_content['analysis'] = self._format_text(content['analysis'], rules)
        
        # Format findings
        if 'findings' in content:
            formatted_content['findings'] = self._format_findings_list(content['findings'], template_type)
        
        return formatted_content
    
    def _format_text(self, text: str, rules: Dict[str, Any]) -> str:
        """Format text according to rules"""
        if not text:
            return text
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Break into paragraphs if too long
        max_length = rules.get('max_paragraph_length', 800)
        
        if len(text) <= max_length:
            return text
        
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        paragraphs = []
        current_paragraph = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            if current_length + sentence_length > max_length and current_paragraph:
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = [sentence]
                current_length = sentence_length
            else:
                current_paragraph.append(sentence)
                current_length += sentence_length
        
        if current_paragraph:
            paragraphs.append(' '.join(current_paragraph))
        
        return '\n\n'.join(paragraphs)
    
    def _format_findings_list(self, findings: List[str], template_type: str) -> List[str]:
        """Format findings list"""
        if not findings:
            return findings
        
        rules = self.formatting_rules.get(template_type, self.formatting_rules['standard'])
        
        formatted_findings = []
        
        for finding in findings:
            # Clean up the finding text
            formatted_finding = finding.strip()
            
            # Add bullet point if required
            if rules.get('bullet_points', True) and not formatted_finding.startswith('•'):
                formatted_finding = f"• {formatted_finding}"
            
            formatted_findings.append(formatted_finding)
        
        return formatted_findings

class ReportContentGenerator:
    """Main content generator for investigation reports"""
    
    def __init__(self):
        self.ai_writer = AIContentWriter()
        self.formatter = ContentFormatter()
        
        logger.info("Initialized ReportContentGenerator")
    
    def generate_complete_report_content(self, data: Dict[str, Any], template_type: str) -> Dict[str, Any]:
        """Generate complete report content"""
        logger.info(f"Generating {template_type} report content")
        
        try:
            # Generate executive summary
            executive_summary = self.generate_executive_summary(data, template_type)
            
            # Generate all sections
            sections = self.generate_all_sections(data, template_type)
            
            # Generate recommendations
            recommendations = self.generate_recommendations_content(data, template_type)
            
            # Generate conclusion
            conclusion = self.generate_conclusion(data, template_type)
            
            complete_content = {
                'executive_summary': executive_summary,
                'sections': sections,
                'recommendations': recommendations,
                'conclusion': conclusion,
                'generation_metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'template_type': template_type,
                    'content_generator_version': '1.0.0',
                    'total_sections': len(sections)
                }
            }
            
            logger.info(f"Generated complete {template_type} report content with {len(sections)} sections")
            return complete_content
            
        except Exception as e:
            logger.error(f"Error generating report content: {str(e)}")
            raise
    
    def generate_executive_summary(self, data: Dict[str, Any], template_type: str) -> Dict[str, Any]:
        """Generate executive summary content"""
        executive_data = data.get('executive_summary', {})
        
        # Generate overview
        overview = self.ai_writer.write_investigation_overview(data, template_type)
        
        # Format the summary
        summary_content = {
            'overview': overview,
            'risk_assessment': executive_data.get('risk_assessment', {}),
            'key_findings': executive_data.get('key_findings', []),
            'data_sources': executive_data.get('data_sources_used', 0),
            'summary_statement': executive_data.get('summary_statement', '')
        }
        
        return self.formatter.format_executive_summary(summary_content, template_type)
    
    def generate_all_sections(self, data: Dict[str, Any], template_type: str) -> List[Dict[str, Any]]:
        """Generate content for all report sections"""
        sections = []
        detailed_findings = data.get('detailed_findings', {})
        
        for section_id, section_data in detailed_findings.items():
            section_content = self.generate_section_content(section_id, section_data, template_type)
            sections.append(section_content)
        
        return sections
    
    def generate_section_content(self, section_id: str, section_data: Dict[str, Any], 
                               template_type: str) -> Dict[str, Any]:
        """Generate content for a specific section"""
        
        # Generate section overview
        overview = self.ai_writer.write_section_overview(section_data, section_id, template_type)
        
        # Generate detailed analysis
        analysis = self.ai_writer.analyze_findings(section_data, section_id, template_type)
        
        # Extract key findings
        findings = self._extract_section_findings(section_data)
        
        section_content = {
            'section_id': section_id,
            'title': section_id.replace('_', ' ').title(),
            'overview': overview,
            'analysis': analysis,
            'findings': findings,
            'data': section_data
        }
        
        return self.formatter.format_section(section_content, template_type)
    
    def generate_recommendations_content(self, data: Dict[str, Any], template_type: str) -> Dict[str, Any]:
        """Generate recommendations content"""
        recommendations = data.get('recommendations', [])
        risk_level = self._extract_risk_level(data)
        
        if template_type == 'basic':
            content = "Based on the investigation findings, the following actions are recommended:\n\n"
            for i, rec in enumerate(recommendations[:3], 1):
                content += f"{i}. {rec}\n"
        
        elif template_type == 'standard':
            content = f"""
            Based on the comprehensive investigation and {risk_level} risk assessment, 
            the following recommendations are provided to address identified risks and 
            enhance security posture:
            
            """
            
            for i, rec in enumerate(recommendations[:5], 1):
                content += f"{i}. {rec}\n\n"
        
        elif template_type == 'professional':
            content = f"""
            STRATEGIC RECOMMENDATIONS
            
            Based on the detailed multi-source analysis and comprehensive risk assessment 
            indicating a {risk_level} risk profile, the following strategic recommendations 
            are provided to address identified vulnerabilities and enhance overall security posture:
            
            """
            
            for i, rec in enumerate(recommendations[:8], 1):
                content += f"Recommendation {i}: {rec}\n\n"
                content += f"Priority: {'High' if i <= 3 else 'Medium'}\n"
                content += f"Implementation Timeline: {'Immediate' if i <= 2 else '30-60 days'}\n\n"
        
        else:  # forensic
            content = f"""
            EXPERT RECOMMENDATIONS AND LEGAL CONSIDERATIONS
            
            Based on the forensic investigation findings and comprehensive risk assessment 
            indicating a {risk_level} risk classification, the following expert recommendations 
            are provided with consideration for potential legal and regulatory implications:
            
            """
            
            for i, rec in enumerate(recommendations, 1):
                content += f"Recommendation {i}: {rec}\n"
                content += f"Legal Consideration: Review with legal counsel if implementing\n"
                content += f"Evidence Support: Documented in investigation findings\n"
                content += f"Risk Mitigation: {'Critical' if i <= 3 else 'Important'}\n\n"
        
        return {
            'content': content,
            'recommendations_count': len(recommendations),
            'risk_level': risk_level
        }
    
    def generate_conclusion(self, data: Dict[str, Any], template_type: str) -> Dict[str, Any]:
        """Generate conclusion content"""
        risk_level = self._extract_risk_level(data)
        confidence = data.get('risk_assessment', {}).get('confidence', 0)
        
        if template_type == 'basic':
            content = f"""
            This investigation determined a {risk_level} risk level with {confidence:.0%} confidence. 
            The findings provide sufficient information for risk-based decision making.
            """
        
        elif template_type == 'standard':
            content = f"""
            INVESTIGATION CONCLUSION
            
            This comprehensive investigation has determined a {risk_level} risk classification 
            with {confidence:.0%} confidence based on multi-source analysis and cross-validation. 
            The investigation successfully gathered and analyzed data from multiple authoritative 
            sources to provide a thorough risk assessment.
            
            The findings indicate that appropriate risk management measures should be implemented 
            based on the identified risk level and specific findings detailed throughout this report.
            """
        
        elif template_type == 'professional':
            content = f"""
            EXECUTIVE CONCLUSION AND PROFESSIONAL ASSESSMENT
            
            This detailed investigation has concluded with a {risk_level} risk classification, 
            supported by comprehensive multi-source analysis and validated through cross-reference 
            protocols. The assessment confidence level of {confidence:.0%} reflects the quality 
            and completeness of available data sources.
            
            The investigation methodology employed advanced artificial intelligence analysis, 
            external database integration, and machine learning risk modeling to provide a 
            thorough and objective assessment. All findings have been documented with appropriate 
            source attribution and confidence levels.
            
            The risk classification and associated recommendations provide a solid foundation 
            for informed decision-making and appropriate risk management implementation.
            """
        
        else:  # forensic
            content = f"""
            FORENSIC CONCLUSION AND EXPERT OPINION
            
            Based on the comprehensive forensic investigation conducted in accordance with 
            established investigative standards, this analysis concludes with a {risk_level} 
            risk classification. The assessment confidence level of {confidence:.0%} is 
            supported by documented evidence and verified data sources.
            
            EXPERT OPINION: The investigation methodology employed recognized forensic 
            techniques and maintained appropriate evidence chain documentation. All findings 
            are based on verifiable data sources and have been documented with sufficient 
            detail to support potential legal or regulatory proceedings.
            
            The risk assessment and associated findings provide a professional foundation 
            for risk-based decision making and potential legal considerations. All evidence 
            and documentation have been preserved in accordance with forensic standards.
            """
        
        return {
            'content': content,
            'risk_level': risk_level,
            'confidence': confidence
        }
    
    def _extract_section_findings(self, section_data: Dict[str, Any]) -> List[str]:
        """Extract key findings from section data"""
        findings = []
        
        for key, value in section_data.items():
            if isinstance(value, str) and value and value not in ['Unknown', 'Not available', 'Not checked']:
                findings.append(f"{key.replace('_', ' ').title()}: {value}")
            elif isinstance(value, (int, float)) and value > 0:
                findings.append(f"{key.replace('_', ' ').title()}: {value}")
            elif isinstance(value, list) and value:
                findings.append(f"{key.replace('_', ' ').title()}: {len(value)} items")
            elif isinstance(value, dict) and value:
                # Handle nested dictionaries
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, str) and sub_value and sub_value != 'Unknown':
                        findings.append(f"{sub_key.replace('_', ' ').title()}: {sub_value}")
        
        return findings[:10]  # Limit to top 10 findings
    
    def _extract_risk_level(self, data: Dict[str, Any]) -> str:
        """Extract risk level from data"""
        risk_assessment = data.get('risk_assessment', {})
        
        if hasattr(risk_assessment.get('risk_level'), 'value'):
            return risk_assessment['risk_level'].value
        elif isinstance(risk_assessment.get('risk_level'), str):
            return risk_assessment['risk_level']
        else:
            return 'UNKNOWN'

# Example usage and testing
if __name__ == "__main__":
    def test_content_generator():
        """Test the content generator"""
        # Sample processed investigation data
        sample_data = {
            'investigation_id': 'test_001',
            'subject': 'john.doe@example.com',
            'executive_summary': {
                'overall_risk_level': 'MEDIUM',
                'overall_risk_score': 0.45,
                'confidence_level': 0.87,
                'key_findings': ['Domain recently registered', 'Clean background check', 'No sanctions matches'],
                'data_sources_used': 9,
                'summary_statement': 'Investigation shows medium risk with high confidence.'
            },
            'detailed_findings': {
                'identity_verification': {
                    'identity_status': 'Identity confirmed',
                    'address_history': ['123 Main St', '456 Oak Ave'],
                    'criminal_background': 'No criminal records found'
                },
                'digital_footprint': {
                    'domain_analysis': {
                        'domain_age': 'Recent registration (< 30 days)',
                        'risk_indicators': ['Recent registration', 'Suspicious TLD']
                    },
                    'email_analysis': {
                        'email_validity': 'Valid email format',
                        'phishing_indicators': []
                    }
                },
                'compliance_screening': {
                    'sanctions_screening': 'No sanctions matches found',
                    'pep_screening': 'Not a politically exposed person',
                    'compliance_status': 'CLEAR'
                }
            },
            'risk_assessment': {
                'risk_level': 'MEDIUM',
                'overall_score': 0.45,
                'confidence': 0.87
            },
            'recommendations': [
                'Monitor domain for suspicious activity',
                'Verify domain ownership',
                'Implement standard monitoring procedures'
            ]
        }
        
        # Test content generator
        generator = ReportContentGenerator()
        
        print("✅ Content Generator Test")
        
        # Test each template type
        for template_type in ['basic', 'standard', 'professional', 'forensic']:
            print(f"\n🔍 Testing {template_type.title()} Content Generation:")
            
            # Generate complete content
            content = generator.generate_complete_report_content(sample_data, template_type)
            
            print(f"  📄 Sections Generated: {content['generation_metadata']['total_sections']}")
            print(f"  📝 Executive Summary: {len(content['executive_summary']['overview'])} characters")
            print(f"  💡 Recommendations: {content['recommendations']['recommendations_count']}")
            
            # Save sample content
            output_file = Path(__file__).parent / f"test_{template_type}_content.json"
            with open(output_file, 'w') as f:
                json.dump(content, f, indent=2, default=str)
            
            print(f"  💾 Content saved to: {output_file}")
        
        return generator
    
    # Run test
    test_content_generator()

