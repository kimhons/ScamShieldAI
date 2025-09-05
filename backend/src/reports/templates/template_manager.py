"""
ScamShield AI - Report Template Manager
Manages professional report templates for different report types and formats
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ReportSection:
    """Report section configuration"""
    id: str
    title: str
    content_type: str  # 'text', 'table', 'chart', 'list'
    required: bool
    order: int
    template: str
    max_length: Optional[int] = None

@dataclass
class ReportTemplate:
    """Report template configuration"""
    template_id: str
    name: str
    report_type: str
    page_limit: int
    detail_level: str
    sections: List[ReportSection]
    styling: Dict[str, Any]
    pricing: Dict[str, Any]

class BaseReportTemplate(ABC):
    """Base class for all report templates"""
    
    def __init__(self):
        self.template_id = ""
        self.name = ""
        self.report_type = ""
        self.page_limit = 0
        self.detail_level = "basic"
        self.sections = []
        self.styling = {}
        self.pricing = {}
    
    @abstractmethod
    def get_sections(self) -> List[ReportSection]:
        """Get report sections configuration"""
        pass
    
    @abstractmethod
    def get_styling(self) -> Dict[str, Any]:
        """Get report styling configuration"""
        pass
    
    def generate_structure(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate report structure based on template"""
        return {
            'template_info': {
                'template_id': self.template_id,
                'name': self.name,
                'report_type': self.report_type,
                'page_limit': self.page_limit,
                'detail_level': self.detail_level
            },
            'cover_page': self.generate_cover_page(data),
            'executive_summary': self.generate_executive_summary(data),
            'sections': self.generate_sections(data),
            'appendices': self.generate_appendices(data),
            'styling': self.get_styling(),
            'metadata': self.generate_report_metadata(data)
        }
    
    def generate_cover_page(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate cover page content"""
        return {
            'title': f"{self.name}",
            'subtitle': f"Investigation Report",
            'subject': data.get('subject', 'Unknown Subject'),
            'report_id': data.get('investigation_id', 'Unknown'),
            'generated_date': datetime.now().strftime('%B %d, %Y'),
            'generated_time': datetime.now().strftime('%I:%M %p'),
            'investigator': 'ScamShield AI System',
            'classification': self._get_classification_level(data),
            'logo': 'scamshield_logo.png'
        }
    
    def generate_executive_summary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary content"""
        executive_summary = data.get('executive_summary', {})
        
        return {
            'overview': f"This {self.detail_level} investigation report provides a comprehensive analysis of {data.get('subject', 'the subject')}.",
            'risk_assessment': {
                'level': executive_summary.get('overall_risk_level', 'UNKNOWN'),
                'score': executive_summary.get('overall_risk_score', 0),
                'confidence': executive_summary.get('confidence_level', 0)
            },
            'key_findings': executive_summary.get('key_findings', []),
            'data_sources': executive_summary.get('data_sources_used', 0),
            'investigation_scope': self._get_investigation_scope(),
            'summary_statement': executive_summary.get('summary_statement', 'Investigation completed successfully.')
        }
    
    def generate_sections(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate report sections"""
        sections = []
        
        for section_config in self.get_sections():
            if self._should_include_section(section_config, data):
                section_content = self._generate_section_content(section_config, data)
                sections.append(section_content)
        
        return sections
    
    def generate_appendices(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate appendices content"""
        return {
            'methodology': self._get_methodology_description(),
            'data_sources': self._get_data_sources_list(data),
            'legal_disclaimers': self._get_legal_disclaimers(),
            'glossary': self._get_glossary(),
            'evidence_chain': data.get('evidence_chain', [])
        }
    
    def generate_report_metadata(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate report metadata"""
        return {
            'template_version': '1.0.0',
            'generation_timestamp': datetime.now().isoformat(),
            'data_quality_score': data.get('metadata', {}).get('data_quality', {}).get('quality_score', 0),
            'completeness_score': data.get('metadata', {}).get('data_quality', {}).get('completeness_score', 0),
            'processing_time': '15.2 seconds',
            'total_pages': self._estimate_page_count(data),
            'word_count': self._estimate_word_count(data)
        }
    
    def _get_classification_level(self, data: Dict[str, Any]) -> str:
        """Get report classification level"""
        risk_level = data.get('risk_assessment', {}).get('risk_level', 'LOW')
        
        if hasattr(risk_level, 'value'):
            risk_level = risk_level.value
        
        classification_map = {
            'LOW': 'CONFIDENTIAL',
            'MEDIUM': 'CONFIDENTIAL',
            'HIGH': 'RESTRICTED',
            'CRITICAL': 'RESTRICTED'
        }
        
        return classification_map.get(risk_level, 'CONFIDENTIAL')
    
    def _get_investigation_scope(self) -> List[str]:
        """Get investigation scope items"""
        return [
            'Identity verification and background screening',
            'Digital footprint and online presence analysis',
            'Financial intelligence and transaction monitoring',
            'Compliance screening and sanctions checking',
            'Threat assessment and security evaluation'
        ]
    
    def _should_include_section(self, section_config: ReportSection, data: Dict[str, Any]) -> bool:
        """Determine if section should be included"""
        if section_config.required:
            return True
        
        # Check if data exists for optional sections
        detailed_findings = data.get('detailed_findings', {})
        return section_config.id in detailed_findings
    
    def _generate_section_content(self, section_config: ReportSection, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content for a specific section"""
        detailed_findings = data.get('detailed_findings', {})
        section_data = detailed_findings.get(section_config.id, {})
        
        return {
            'id': section_config.id,
            'title': section_config.title,
            'content_type': section_config.content_type,
            'order': section_config.order,
            'content': section_data,
            'template': section_config.template,
            'max_length': section_config.max_length
        }
    
    def _get_methodology_description(self) -> str:
        """Get methodology description"""
        return """
        This investigation employed a multi-source intelligence approach utilizing:
        
        1. Automated AI agent analysis across specialized domains
        2. External API integration for real-time data verification
        3. Machine learning models for fraud detection and risk assessment
        4. Comprehensive evidence chain documentation
        5. Cross-reference validation across multiple data sources
        
        All findings are based on publicly available information and authorized data sources.
        """
    
    def _get_data_sources_list(self, data: Dict[str, Any]) -> List[str]:
        """Get list of data sources used"""
        return [
            'CrewAI Multi-Agent Investigation System',
            'OpenSanctions Global Database',
            'Alpha Vantage Financial Intelligence',
            'WhoisXML Domain Intelligence',
            'Shodan Infrastructure Analysis',
            'IPinfo Geolocation Services',
            'Cloudflare DNS Intelligence',
            'RapidAPI Background Check Services',
            'MaxMind GeoIP Database',
            'Companies House Business Registry'
        ]
    
    def _get_legal_disclaimers(self) -> List[str]:
        """Get legal disclaimers"""
        return [
            "This report is based on information available at the time of investigation.",
            "ScamShield AI makes no warranties regarding the accuracy or completeness of third-party data.",
            "This report is for informational purposes only and should not be considered legal advice.",
            "Users should verify critical information through additional sources before making decisions.",
            "Data sources may have varying levels of accuracy and timeliness.",
            "This investigation complies with applicable privacy and data protection regulations."
        ]
    
    def _get_glossary(self) -> Dict[str, str]:
        """Get glossary of terms"""
        return {
            "PEP": "Politically Exposed Person - Individual with prominent public functions",
            "OFAC": "Office of Foreign Assets Control - US Treasury sanctions authority",
            "KYC": "Know Your Customer - Identity verification process",
            "AML": "Anti-Money Laundering - Financial crime prevention measures",
            "DNS": "Domain Name System - Internet naming system",
            "SSL": "Secure Sockets Layer - Web security protocol",
            "API": "Application Programming Interface - Software integration method",
            "ML": "Machine Learning - Artificial intelligence technique"
        }
    
    def _estimate_page_count(self, data: Dict[str, Any]) -> int:
        """Estimate report page count"""
        base_pages = 3  # Cover, executive summary, appendices
        
        detailed_findings = data.get('detailed_findings', {})
        content_pages = len(detailed_findings) * 2  # Estimate 2 pages per section
        
        estimated_pages = base_pages + content_pages
        return min(estimated_pages, self.page_limit)
    
    def _estimate_word_count(self, data: Dict[str, Any]) -> int:
        """Estimate report word count"""
        estimated_pages = self._estimate_page_count(data)
        words_per_page = 400  # Average words per page
        return estimated_pages * words_per_page

class BasicReportTemplate(BaseReportTemplate):
    """Basic report template - Essential findings only"""
    
    def __init__(self):
        super().__init__()
        self.template_id = "basic_v1"
        self.name = "Basic Investigation Report"
        self.report_type = "basic"
        self.page_limit = 5
        self.detail_level = "essential"
        self.pricing = {"price": 9.99, "currency": "USD"}
    
    def get_sections(self) -> List[ReportSection]:
        """Get basic report sections"""
        return [
            ReportSection(
                id="identity_verification",
                title="Identity Verification",
                content_type="text",
                required=True,
                order=1,
                template="basic_identity_template",
                max_length=500
            ),
            ReportSection(
                id="compliance_screening",
                title="Compliance Screening",
                content_type="text",
                required=True,
                order=2,
                template="basic_compliance_template",
                max_length=400
            ),
            ReportSection(
                id="risk_summary",
                title="Risk Assessment Summary",
                content_type="text",
                required=True,
                order=3,
                template="basic_risk_template",
                max_length=300
            )
        ]
    
    def get_styling(self) -> Dict[str, Any]:
        """Get basic report styling"""
        return {
            'theme': 'professional_basic',
            'colors': {
                'primary': '#2563eb',
                'secondary': '#64748b',
                'accent': '#0ea5e9',
                'text': '#1e293b',
                'background': '#ffffff'
            },
            'fonts': {
                'heading': 'Arial, sans-serif',
                'body': 'Arial, sans-serif',
                'heading_size': '18px',
                'body_size': '12px'
            },
            'layout': {
                'margins': '1 inch',
                'line_spacing': '1.2',
                'paragraph_spacing': '6pt'
            }
        }

class StandardReportTemplate(BaseReportTemplate):
    """Standard report template - Comprehensive analysis"""
    
    def __init__(self):
        super().__init__()
        self.template_id = "standard_v1"
        self.name = "Standard Investigation Report"
        self.report_type = "standard"
        self.page_limit = 12
        self.detail_level = "comprehensive"
        self.pricing = {"price": 24.99, "currency": "USD"}
    
    def get_sections(self) -> List[ReportSection]:
        """Get standard report sections"""
        return [
            ReportSection(
                id="identity_verification",
                title="Identity Verification & Background Check",
                content_type="text",
                required=True,
                order=1,
                template="standard_identity_template",
                max_length=1000
            ),
            ReportSection(
                id="digital_footprint",
                title="Digital Footprint Analysis",
                content_type="text",
                required=True,
                order=2,
                template="standard_digital_template",
                max_length=800
            ),
            ReportSection(
                id="financial_intelligence",
                title="Financial Intelligence",
                content_type="text",
                required=True,
                order=3,
                template="standard_financial_template",
                max_length=800
            ),
            ReportSection(
                id="compliance_screening",
                title="Compliance & Sanctions Screening",
                content_type="text",
                required=True,
                order=4,
                template="standard_compliance_template",
                max_length=600
            ),
            ReportSection(
                id="threat_assessment",
                title="Security Threat Assessment",
                content_type="text",
                required=True,
                order=5,
                template="standard_threat_template",
                max_length=600
            ),
            ReportSection(
                id="risk_analysis",
                title="Comprehensive Risk Analysis",
                content_type="table",
                required=True,
                order=6,
                template="standard_risk_template",
                max_length=400
            )
        ]
    
    def get_styling(self) -> Dict[str, Any]:
        """Get standard report styling"""
        return {
            'theme': 'professional_standard',
            'colors': {
                'primary': '#1e40af',
                'secondary': '#475569',
                'accent': '#0284c7',
                'text': '#0f172a',
                'background': '#ffffff',
                'table_header': '#f1f5f9',
                'table_border': '#e2e8f0'
            },
            'fonts': {
                'heading': 'Georgia, serif',
                'body': 'Arial, sans-serif',
                'heading_size': '20px',
                'subheading_size': '16px',
                'body_size': '11px'
            },
            'layout': {
                'margins': '1 inch',
                'line_spacing': '1.3',
                'paragraph_spacing': '8pt',
                'section_spacing': '12pt'
            }
        }

class ProfessionalReportTemplate(BaseReportTemplate):
    """Professional report template - Detailed investigation"""
    
    def __init__(self):
        super().__init__()
        self.template_id = "professional_v1"
        self.name = "Professional Investigation Report"
        self.report_type = "professional"
        self.page_limit = 25
        self.detail_level = "detailed"
        self.pricing = {"price": 49.99, "currency": "USD"}
    
    def get_sections(self) -> List[ReportSection]:
        """Get professional report sections"""
        return [
            ReportSection(
                id="investigation_overview",
                title="Investigation Overview & Methodology",
                content_type="text",
                required=True,
                order=1,
                template="professional_overview_template",
                max_length=800
            ),
            ReportSection(
                id="identity_verification",
                title="Identity Verification & Background Analysis",
                content_type="text",
                required=True,
                order=2,
                template="professional_identity_template",
                max_length=1500
            ),
            ReportSection(
                id="digital_footprint",
                title="Digital Footprint & Online Presence",
                content_type="text",
                required=True,
                order=3,
                template="professional_digital_template",
                max_length=1200
            ),
            ReportSection(
                id="financial_intelligence",
                title="Financial Intelligence & Transaction Analysis",
                content_type="text",
                required=True,
                order=4,
                template="professional_financial_template",
                max_length=1200
            ),
            ReportSection(
                id="compliance_screening",
                title="Regulatory Compliance & Sanctions Screening",
                content_type="text",
                required=True,
                order=5,
                template="professional_compliance_template",
                max_length=1000
            ),
            ReportSection(
                id="threat_assessment",
                title="Security Threat Assessment & Risk Indicators",
                content_type="text",
                required=True,
                order=6,
                template="professional_threat_template",
                max_length=1000
            ),
            ReportSection(
                id="intelligence_analysis",
                title="Intelligence Fusion & Cross-Source Analysis",
                content_type="text",
                required=True,
                order=7,
                template="professional_intelligence_template",
                max_length=800
            ),
            ReportSection(
                id="risk_assessment",
                title="Comprehensive Risk Assessment",
                content_type="table",
                required=True,
                order=8,
                template="professional_risk_template",
                max_length=600
            ),
            ReportSection(
                id="recommendations",
                title="Strategic Recommendations & Mitigation",
                content_type="list",
                required=True,
                order=9,
                template="professional_recommendations_template",
                max_length=800
            )
        ]
    
    def get_styling(self) -> Dict[str, Any]:
        """Get professional report styling"""
        return {
            'theme': 'executive_professional',
            'colors': {
                'primary': '#1e3a8a',
                'secondary': '#374151',
                'accent': '#0369a1',
                'text': '#111827',
                'background': '#ffffff',
                'table_header': '#f9fafb',
                'table_border': '#d1d5db',
                'highlight': '#fef3c7'
            },
            'fonts': {
                'heading': 'Times New Roman, serif',
                'body': 'Arial, sans-serif',
                'heading_size': '22px',
                'subheading_size': '18px',
                'body_size': '11px',
                'caption_size': '10px'
            },
            'layout': {
                'margins': '1.25 inch',
                'line_spacing': '1.4',
                'paragraph_spacing': '10pt',
                'section_spacing': '16pt',
                'page_numbers': True,
                'headers_footers': True
            }
        }

class ForensicReportTemplate(BaseReportTemplate):
    """Forensic report template - Legal-grade documentation"""
    
    def __init__(self):
        super().__init__()
        self.template_id = "forensic_v1"
        self.name = "Forensic Investigation Report"
        self.report_type = "forensic"
        self.page_limit = 40
        self.detail_level = "forensic"
        self.pricing = {"price": 99.99, "currency": "USD"}
    
    def get_sections(self) -> List[ReportSection]:
        """Get forensic report sections"""
        return [
            ReportSection(
                id="executive_briefing",
                title="Executive Briefing & Case Summary",
                content_type="text",
                required=True,
                order=1,
                template="forensic_briefing_template",
                max_length=1000
            ),
            ReportSection(
                id="investigation_methodology",
                title="Investigation Methodology & Standards",
                content_type="text",
                required=True,
                order=2,
                template="forensic_methodology_template",
                max_length=800
            ),
            ReportSection(
                id="evidence_collection",
                title="Evidence Collection & Chain of Custody",
                content_type="table",
                required=True,
                order=3,
                template="forensic_evidence_template",
                max_length=1200
            ),
            ReportSection(
                id="identity_verification",
                title="Identity Verification & Authentication",
                content_type="text",
                required=True,
                order=4,
                template="forensic_identity_template",
                max_length=2000
            ),
            ReportSection(
                id="digital_forensics",
                title="Digital Forensics & Technical Analysis",
                content_type="text",
                required=True,
                order=5,
                template="forensic_digital_template",
                max_length=1800
            ),
            ReportSection(
                id="financial_forensics",
                title="Financial Forensics & Transaction Tracing",
                content_type="text",
                required=True,
                order=6,
                template="forensic_financial_template",
                max_length=1800
            ),
            ReportSection(
                id="compliance_analysis",
                title="Regulatory Compliance Analysis",
                content_type="text",
                required=True,
                order=7,
                template="forensic_compliance_template",
                max_length=1500
            ),
            ReportSection(
                id="threat_intelligence",
                title="Threat Intelligence & Attribution Analysis",
                content_type="text",
                required=True,
                order=8,
                template="forensic_threat_template",
                max_length=1500
            ),
            ReportSection(
                id="pattern_analysis",
                title="Behavioral Pattern Analysis",
                content_type="text",
                required=True,
                order=9,
                template="forensic_pattern_template",
                max_length=1200
            ),
            ReportSection(
                id="risk_assessment",
                title="Comprehensive Risk Assessment Matrix",
                content_type="table",
                required=True,
                order=10,
                template="forensic_risk_template",
                max_length=800
            ),
            ReportSection(
                id="expert_analysis",
                title="Expert Analysis & Professional Opinion",
                content_type="text",
                required=True,
                order=11,
                template="forensic_expert_template",
                max_length=1000
            ),
            ReportSection(
                id="recommendations",
                title="Strategic Recommendations & Legal Considerations",
                content_type="list",
                required=True,
                order=12,
                template="forensic_recommendations_template",
                max_length=1200
            )
        ]
    
    def get_styling(self) -> Dict[str, Any]:
        """Get forensic report styling"""
        return {
            'theme': 'legal_forensic',
            'colors': {
                'primary': '#1e293b',
                'secondary': '#475569',
                'accent': '#0f172a',
                'text': '#0f172a',
                'background': '#ffffff',
                'table_header': '#f8fafc',
                'table_border': '#cbd5e1',
                'highlight': '#fef9e7',
                'evidence': '#ecfdf5'
            },
            'fonts': {
                'heading': 'Times New Roman, serif',
                'body': 'Times New Roman, serif',
                'heading_size': '24px',
                'subheading_size': '20px',
                'body_size': '12px',
                'caption_size': '10px',
                'evidence_size': '11px'
            },
            'layout': {
                'margins': '1.5 inch',
                'line_spacing': '1.5',
                'paragraph_spacing': '12pt',
                'section_spacing': '20pt',
                'page_numbers': True,
                'headers_footers': True,
                'watermark': 'CONFIDENTIAL',
                'line_numbers': True
            }
        }

class ReportTemplateManager:
    """Manages all report templates and template selection"""
    
    def __init__(self):
        self.templates = {
            'basic': BasicReportTemplate(),
            'standard': StandardReportTemplate(),
            'professional': ProfessionalReportTemplate(),
            'forensic': ForensicReportTemplate()
        }
        
        logger.info(f"Initialized ReportTemplateManager with {len(self.templates)} templates")
    
    def get_template(self, report_type: str) -> BaseReportTemplate:
        """Get template by report type"""
        if report_type not in self.templates:
            raise ValueError(f"Unknown report type: {report_type}. Available types: {list(self.templates.keys())}")
        
        return self.templates[report_type]
    
    def get_available_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all available templates"""
        template_info = {}
        
        for template_type, template in self.templates.items():
            template_info[template_type] = {
                'name': template.name,
                'page_limit': template.page_limit,
                'detail_level': template.detail_level,
                'pricing': template.pricing,
                'sections_count': len(template.get_sections())
            }
        
        return template_info
    
    def generate_report_structure(self, report_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete report structure for given type and data"""
        template = self.get_template(report_type)
        structure = template.generate_structure(data)
        
        logger.info(f"Generated {report_type} report structure with {len(structure['sections'])} sections")
        return structure
    
    def validate_report_data(self, report_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that data is sufficient for report type"""
        template = self.get_template(report_type)
        sections = template.get_sections()
        
        validation_result = {
            'valid': True,
            'missing_sections': [],
            'warnings': [],
            'completeness_score': 0.0
        }
        
        detailed_findings = data.get('detailed_findings', {})
        required_sections = [s for s in sections if s.required]
        
        # Check required sections
        missing_required = []
        for section in required_sections:
            if section.id not in detailed_findings:
                missing_required.append(section.id)
        
        if missing_required:
            validation_result['valid'] = False
            validation_result['missing_sections'] = missing_required
        
        # Calculate completeness
        available_sections = len([s for s in sections if s.id in detailed_findings])
        validation_result['completeness_score'] = available_sections / len(sections)
        
        # Add warnings for low completeness
        if validation_result['completeness_score'] < 0.7:
            validation_result['warnings'].append(f"Report completeness is {validation_result['completeness_score']:.1%}")
        
        return validation_result
    
    def get_template_pricing(self, report_type: str) -> Dict[str, Any]:
        """Get pricing information for report type"""
        template = self.get_template(report_type)
        return template.pricing
    
    def estimate_generation_time(self, report_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate report generation time"""
        template = self.get_template(report_type)
        
        # Base time estimates (in seconds)
        base_times = {
            'basic': 10,
            'standard': 20,
            'professional': 35,
            'forensic': 60
        }
        
        base_time = base_times.get(report_type, 30)
        
        # Adjust based on data complexity
        detailed_findings = data.get('detailed_findings', {})
        complexity_factor = len(detailed_findings) / 10  # Assume 10 is average
        
        estimated_time = base_time * (1 + complexity_factor * 0.5)
        
        return {
            'estimated_seconds': int(estimated_time),
            'estimated_minutes': round(estimated_time / 60, 1),
            'complexity_factor': complexity_factor,
            'base_time': base_time
        }

# Example usage and testing
if __name__ == "__main__":
    def test_template_manager():
        """Test the template manager"""
        # Sample investigation data
        sample_data = {
            'investigation_id': 'test_001',
            'subject': 'john.doe@example.com',
            'executive_summary': {
                'overall_risk_level': 'MEDIUM',
                'overall_risk_score': 0.45,
                'confidence_level': 0.87,
                'key_findings': ['Domain recently registered', 'Clean background check'],
                'data_sources_used': 9
            },
            'detailed_findings': {
                'identity_verification': {'status': 'verified'},
                'digital_footprint': {'domain_age': 'recent'},
                'compliance_screening': {'status': 'clear'}
            },
            'risk_assessment': {
                'risk_level': 'MEDIUM',
                'overall_score': 0.45
            }
        }
        
        # Test template manager
        manager = ReportTemplateManager()
        
        print("✅ Template Manager Test")
        print(f"📋 Available Templates: {list(manager.get_available_templates().keys())}")
        
        # Test each template type
        for template_type in ['basic', 'standard', 'professional', 'forensic']:
            print(f"\n🔍 Testing {template_type.title()} Template:")
            
            # Generate structure
            structure = manager.generate_report_structure(template_type, sample_data)
            print(f"  📄 Sections: {len(structure['sections'])}")
            print(f"  📊 Page Limit: {structure['template_info']['page_limit']}")
            
            # Validate data
            validation = manager.validate_report_data(template_type, sample_data)
            print(f"  ✅ Valid: {validation['valid']}")
            print(f"  📈 Completeness: {validation['completeness_score']:.1%}")
            
            # Get pricing
            pricing = manager.get_template_pricing(template_type)
            print(f"  💰 Price: ${pricing['price']}")
            
            # Estimate time
            time_estimate = manager.estimate_generation_time(template_type, sample_data)
            print(f"  ⏱️  Estimated Time: {time_estimate['estimated_minutes']} minutes")
        
        # Save test structure
        test_structure = manager.generate_report_structure('professional', sample_data)
        output_file = Path(__file__).parent / "test_report_structure.json"
        with open(output_file, 'w') as f:
            json.dump(test_structure, f, indent=2, default=str)
        
        print(f"\n💾 Test structure saved to: {output_file}")
        
        return manager
    
    # Run test
    test_template_manager()

