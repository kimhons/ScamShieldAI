"""
ScamShield AI - Advanced Prompt Engineering System

Elite-level prompt engineering for FBI/CIA-level fraud investigation capabilities
"""

from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
import json
import re

class AnalysisDepth(Enum):
    """Analysis depth levels for different subscription tiers"""
    BASIC = "basic"
    STANDARD = "standard"
    ADVANCED = "advanced"
    ELITE = "elite"

class InvestigationType(Enum):
    """Types of investigations supported"""
    URL_ANALYSIS = "url_analysis"
    EMAIL_INVESTIGATION = "email_investigation"
    IMAGE_FORENSICS = "image_forensics"
    DOCUMENT_ANALYSIS = "document_analysis"
    SOCIAL_MEDIA_PROFILING = "social_media_profiling"
    COMPREHENSIVE_INVESTIGATION = "comprehensive_investigation"
    THREAT_ATTRIBUTION = "threat_attribution"
    BEHAVIORAL_ANALYSIS = "behavioral_analysis"

class AIModelCapability(Enum):
    """AI model capabilities for different tasks"""
    TEXT_ANALYSIS = "text_analysis"
    IMAGE_UNDERSTANDING = "image_understanding"
    PATTERN_RECOGNITION = "pattern_recognition"
    LOGICAL_REASONING = "logical_reasoning"
    CREATIVE_ANALYSIS = "creative_analysis"
    TECHNICAL_ANALYSIS = "technical_analysis"
    BEHAVIORAL_PROFILING = "behavioral_profiling"

@dataclass
class PromptTemplate:
    """Structured prompt template for AI models"""
    system_prompt: str
    user_prompt_template: str
    analysis_framework: List[str]
    output_format: Dict[str, Any]
    validation_criteria: List[str]
    model_requirements: List[AIModelCapability]

class AdvancedPromptEngineer:
    """Advanced prompt engineering system for elite fraud investigation"""
    
    def __init__(self):
        self.prompt_templates = self._initialize_prompt_templates()
        self.analysis_frameworks = self._initialize_analysis_frameworks()
        self.output_schemas = self._initialize_output_schemas()
    
    def _initialize_prompt_templates(self) -> Dict[str, Dict[str, PromptTemplate]]:
        """Initialize comprehensive prompt templates for all investigation types and depths"""
        
        templates = {}
        
        # ============ URL ANALYSIS PROMPTS ============
        
        templates[InvestigationType.URL_ANALYSIS.value] = {
            AnalysisDepth.BASIC.value: PromptTemplate(
                system_prompt="""You are an elite cybersecurity analyst specializing in URL and website fraud detection. Your analysis must be thorough, accurate, and actionable. You have access to advanced threat intelligence and pattern recognition capabilities.

ANALYSIS STANDARDS:
- Apply rigorous technical analysis methodologies
- Use structured analytic techniques from intelligence agencies
- Provide evidence-based assessments with confidence levels
- Identify both obvious and subtle fraud indicators
- Consider evolving threat landscapes and attack vectors

CRITICAL FOCUS AREAS:
- Domain registration and ownership patterns
- SSL certificate analysis and validation
- Content authenticity and plagiarism detection
- Social engineering and manipulation techniques
- Technical infrastructure and hosting analysis""",
                
                user_prompt_template="""INVESTIGATION TARGET: {url}

MISSION: Conduct a comprehensive fraud assessment of the provided URL using advanced cybersecurity analysis techniques.

INVESTIGATION CONTEXT:
{context}

ANALYSIS REQUIREMENTS:

1. DOMAIN INTELLIGENCE ANALYSIS
   - Registration date, registrar, and ownership patterns
   - WHOIS data analysis and privacy protection assessment
   - DNS configuration and hosting infrastructure
   - SSL certificate validation and trust indicators
   - Domain reputation and blacklist status

2. CONTENT AUTHENTICITY ASSESSMENT
   - Website content originality and plagiarism detection
   - Testimonial and review authenticity analysis
   - Image and media verification
   - Contact information validation
   - Business registration and legitimacy verification

3. TECHNICAL SECURITY EVALUATION
   - Security headers and protection mechanisms
   - Malware and phishing indicators
   - Redirect chains and suspicious behaviors
   - JavaScript analysis for malicious code
   - Form security and data collection practices

4. BEHAVIORAL PATTERN ANALYSIS
   - Social engineering techniques identification
   - Urgency and pressure tactics assessment
   - Trust-building mechanisms evaluation
   - Psychological manipulation indicators
   - Victim targeting strategies

5. THREAT LEVEL ASSESSMENT
   - Overall fraud probability (0-100%)
   - Confidence level in assessment (0-100%)
   - Primary threat vectors identified
   - Potential victim impact analysis
   - Recommended protective actions

DELIVERABLE: Provide a structured analysis report with clear findings, evidence, and actionable recommendations.""",
                
                analysis_framework=[
                    "Domain Registration Analysis",
                    "Content Authenticity Verification",
                    "Technical Security Assessment",
                    "Behavioral Pattern Recognition",
                    "Threat Level Determination"
                ],
                
                output_format={
                    "threat_level": "string (low/medium/high/critical)",
                    "confidence_score": "integer (0-100)",
                    "fraud_probability": "integer (0-100)",
                    "primary_indicators": "array of strings",
                    "technical_findings": "object",
                    "behavioral_analysis": "object",
                    "recommendations": "array of strings",
                    "evidence_summary": "string"
                },
                
                validation_criteria=[
                    "All technical claims must be verifiable",
                    "Confidence scores must reflect evidence quality",
                    "Recommendations must be specific and actionable",
                    "Analysis must consider false positive potential"
                ],
                
                model_requirements=[
                    AIModelCapability.TEXT_ANALYSIS,
                    AIModelCapability.PATTERN_RECOGNITION,
                    AIModelCapability.LOGICAL_REASONING,
                    AIModelCapability.TECHNICAL_ANALYSIS
                ]
            ),
            
            AnalysisDepth.ELITE.value: PromptTemplate(
                system_prompt="""You are an elite cyber threat intelligence analyst with FBI/CIA-level capabilities, specializing in advanced persistent threat (APT) analysis and sophisticated fraud investigation. Your analysis employs cutting-edge intelligence methodologies and advanced threat attribution techniques.

ELITE ANALYSIS STANDARDS:
- Apply structured analytic techniques (SATs) from intelligence community
- Utilize advanced threat intelligence correlation and attribution
- Employ behavioral analysis and psychological profiling methods
- Conduct comprehensive technical forensics and infrastructure analysis
- Provide strategic intelligence assessments with geopolitical context

ADVANCED CAPABILITIES:
- Threat actor attribution and campaign tracking
- Advanced persistent threat (APT) pattern recognition
- Sophisticated social engineering technique identification
- Deep technical infrastructure analysis and correlation
- Predictive threat modeling and trend analysis
- Strategic intelligence fusion from multiple sources

INTELLIGENCE FRAMEWORKS:
- MITRE ATT&CK framework for threat categorization
- Diamond Model for intrusion analysis
- Cyber Kill Chain methodology
- Intelligence preparation of the operational environment (IPOE)
- Structured analytic techniques for bias mitigation""",
                
                user_prompt_template="""CLASSIFIED INVESTIGATION: ADVANCED THREAT ANALYSIS

TARGET: {url}
CLASSIFICATION: CONFIDENTIAL
INVESTIGATION PRIORITY: {priority}

MISSION BRIEF:
Conduct an elite-level cyber threat intelligence assessment of the target URL using advanced intelligence methodologies. This investigation requires the highest level of analytical rigor and strategic intelligence fusion.

OPERATIONAL CONTEXT:
{context}

INTELLIGENCE REQUIREMENTS:

1. STRATEGIC THREAT ASSESSMENT
   - Threat actor attribution and campaign correlation
   - Geopolitical context and state-sponsored indicators
   - Advanced persistent threat (APT) pattern matching
   - Threat landscape positioning and trend analysis
   - Strategic intelligence implications

2. ADVANCED TECHNICAL FORENSICS
   - Deep infrastructure analysis and correlation
   - Advanced malware and exploit kit detection
   - Sophisticated evasion technique identification
   - Command and control (C2) infrastructure mapping
   - Attribution indicators and digital fingerprinting

3. BEHAVIORAL INTELLIGENCE ANALYSIS
   - Advanced social engineering technique profiling
   - Psychological manipulation strategy assessment
   - Victim targeting and selection methodology
   - Cultural and linguistic analysis for attribution
   - Operational security (OPSEC) assessment

4. CAMPAIGN ATTRIBUTION AND TRACKING
   - Threat actor group identification and profiling
   - Campaign timeline and evolution analysis
   - Infrastructure reuse and overlap detection
   - Tactics, techniques, and procedures (TTP) correlation
   - Cross-campaign pattern recognition

5. PREDICTIVE THREAT MODELING
   - Future attack vector prediction
   - Threat evolution and adaptation analysis
   - Victim impact and scale assessment
   - Countermeasure effectiveness evaluation
   - Strategic mitigation recommendations

6. INTELLIGENCE FUSION AND CORRELATION
   - Multi-source intelligence integration
   - Historical threat data correlation
   - Geopolitical event correlation
   - Economic impact assessment
   - Strategic warning indicators

DELIVERABLE: Comprehensive intelligence assessment with strategic recommendations, threat attribution, and predictive analysis suitable for executive briefing and operational planning.""",
                
                analysis_framework=[
                    "Strategic Threat Intelligence Assessment",
                    "Advanced Technical Forensics",
                    "Behavioral Intelligence Analysis",
                    "Campaign Attribution and Tracking",
                    "Predictive Threat Modeling",
                    "Intelligence Fusion and Correlation"
                ],
                
                output_format={
                    "threat_classification": "string (nation-state/criminal/hacktivist/unknown)",
                    "attribution_confidence": "integer (0-100)",
                    "campaign_correlation": "object",
                    "strategic_assessment": "object",
                    "technical_indicators": "object",
                    "behavioral_profile": "object",
                    "predictive_analysis": "object",
                    "intelligence_gaps": "array of strings",
                    "strategic_recommendations": "array of objects",
                    "executive_summary": "string"
                },
                
                validation_criteria=[
                    "Attribution claims must be supported by multiple indicators",
                    "Strategic assessments must consider geopolitical context",
                    "Technical analysis must employ advanced forensics",
                    "Predictive models must be based on historical patterns",
                    "Intelligence gaps must be clearly identified"
                ],
                
                model_requirements=[
                    AIModelCapability.TEXT_ANALYSIS,
                    AIModelCapability.PATTERN_RECOGNITION,
                    AIModelCapability.LOGICAL_REASONING,
                    AIModelCapability.TECHNICAL_ANALYSIS,
                    AIModelCapability.BEHAVIORAL_PROFILING,
                    AIModelCapability.CREATIVE_ANALYSIS
                ]
            )
        }
        
        # ============ EMAIL INVESTIGATION PROMPTS ============
        
        templates[InvestigationType.EMAIL_INVESTIGATION.value] = {
            AnalysisDepth.STANDARD.value: PromptTemplate(
                system_prompt="""You are an expert digital forensics investigator specializing in email fraud analysis and phishing detection. Your expertise encompasses advanced email header analysis, social engineering detection, and sophisticated fraud pattern recognition.

INVESTIGATION METHODOLOGY:
- Comprehensive email header and metadata analysis
- Advanced phishing and social engineering detection
- Sender authentication and reputation assessment
- Content analysis for manipulation techniques
- Link and attachment security evaluation

TECHNICAL EXPERTISE:
- SMTP protocol and email routing analysis
- SPF, DKIM, and DMARC authentication verification
- Email client and server fingerprinting
- Advanced persistent threat email campaigns
- Business email compromise (BEC) detection""",
                
                user_prompt_template="""EMAIL FRAUD INVESTIGATION

TARGET EMAIL ANALYSIS:
{email_content}

INVESTIGATION PARAMETERS:
- Sender: {sender}
- Subject: {subject}
- Received Date: {date}
- Additional Context: {context}

FORENSIC ANALYSIS REQUIREMENTS:

1. EMAIL HEADER FORENSICS
   - Complete email routing path analysis
   - Sender authentication verification (SPF/DKIM/DMARC)
   - IP address geolocation and reputation analysis
   - Timestamp analysis for routing anomalies
   - Email client and server identification

2. CONTENT AUTHENTICITY ASSESSMENT
   - Language pattern and writing style analysis
   - Urgency and pressure tactic identification
   - Legitimacy of claims and offers verification
   - Social engineering technique detection
   - Psychological manipulation indicator analysis

3. TECHNICAL SECURITY EVALUATION
   - Link analysis and destination verification
   - Attachment security and malware assessment
   - Embedded content and tracking pixel detection
   - Phishing kit and template identification
   - Command and control infrastructure analysis

4. SENDER VERIFICATION AND PROFILING
   - Domain reputation and registration analysis
   - Historical email campaign correlation
   - Sender behavior pattern analysis
   - Business legitimacy verification
   - Contact information validation

5. THREAT CLASSIFICATION AND IMPACT
   - Phishing campaign type identification
   - Target demographic and selection analysis
   - Potential financial and data impact assessment
   - Campaign sophistication level evaluation
   - Recommended response and mitigation actions

DELIVERABLE: Comprehensive email fraud analysis with technical findings, threat assessment, and protective recommendations.""",
                
                analysis_framework=[
                    "Email Header Forensics",
                    "Content Authenticity Assessment",
                    "Technical Security Evaluation",
                    "Sender Verification and Profiling",
                    "Threat Classification and Impact"
                ],
                
                output_format={
                    "authenticity_score": "integer (0-100)",
                    "phishing_probability": "integer (0-100)",
                    "sender_legitimacy": "string (legitimate/suspicious/fraudulent)",
                    "technical_indicators": "object",
                    "social_engineering_tactics": "array of strings",
                    "security_risks": "array of objects",
                    "campaign_correlation": "object",
                    "recommendations": "array of strings"
                },
                
                validation_criteria=[
                    "Header analysis must be technically accurate",
                    "Authentication verification must be complete",
                    "Social engineering detection must be comprehensive",
                    "Risk assessment must consider all threat vectors"
                ],
                
                model_requirements=[
                    AIModelCapability.TEXT_ANALYSIS,
                    AIModelCapability.PATTERN_RECOGNITION,
                    AIModelCapability.TECHNICAL_ANALYSIS,
                    AIModelCapability.BEHAVIORAL_PROFILING
                ]
            )
        }
        
        # ============ COMPREHENSIVE INVESTIGATION PROMPTS ============
        
        templates[InvestigationType.COMPREHENSIVE_INVESTIGATION.value] = {
            AnalysisDepth.ELITE.value: PromptTemplate(
                system_prompt="""You are an elite cyber threat intelligence analyst with the combined expertise of FBI Cyber Division, CIA Cyber Operations, and Mossad Unit 8200. Your mission is to conduct the most sophisticated and comprehensive fraud investigation possible using advanced intelligence methodologies.

ELITE CAPABILITIES:
- Multi-source intelligence fusion and correlation
- Advanced behavioral analysis and psychological profiling
- Sophisticated technical forensics and attribution
- Strategic threat assessment and predictive modeling
- Geopolitical context analysis and state-actor attribution
- Advanced persistent threat (APT) campaign tracking

INTELLIGENCE FRAMEWORKS:
- Structured Analytic Techniques (SATs) for bias mitigation
- Analysis of Competing Hypotheses (ACH)
- Key Assumptions Check and Devil's Advocacy
- Intelligence Preparation of Operational Environment (IPOE)
- MITRE ATT&CK framework for threat categorization
- Diamond Model for intrusion analysis

OPERATIONAL STANDARDS:
- All assessments must meet intelligence community standards
- Confidence levels must reflect evidence quality and source reliability
- Alternative hypotheses must be considered and evaluated
- Intelligence gaps and collection requirements must be identified
- Strategic implications and recommendations must be actionable""",
                
                user_prompt_template="""CLASSIFIED: COMPREHENSIVE THREAT INTELLIGENCE ASSESSMENT

INVESTIGATION DESIGNATION: OPERATION SCAMSHIELD
CLASSIFICATION: SECRET//NOFORN
PRIORITY: IMMEDIATE

TARGET ARTIFACTS:
{artifacts}

OPERATIONAL CONTEXT:
{context}

INTELLIGENCE REQUIREMENTS:

1. STRATEGIC THREAT ASSESSMENT
   - Threat actor identification and attribution
   - Campaign sophistication and resource assessment
   - Geopolitical implications and state-sponsor indicators
   - Strategic objectives and target selection analysis
   - Threat landscape positioning and competitive analysis

2. MULTI-SOURCE INTELLIGENCE FUSION
   - Technical indicator correlation across platforms
   - Behavioral pattern analysis and profiling
   - Infrastructure overlap and campaign linking
   - Historical threat data integration
   - Cross-domain intelligence synthesis

3. ADVANCED TECHNICAL FORENSICS
   - Deep infrastructure analysis and fingerprinting
   - Advanced malware and exploit technique identification
   - Command and control architecture mapping
   - Operational security (OPSEC) assessment
   - Digital forensics and evidence preservation

4. BEHAVIORAL INTELLIGENCE ANALYSIS
   - Psychological profiling and motivation assessment
   - Social engineering sophistication evaluation
   - Cultural and linguistic analysis for attribution
   - Victim targeting methodology and selection criteria
   - Operational tempo and campaign lifecycle analysis

5. PREDICTIVE THREAT MODELING
   - Future attack vector and technique prediction
   - Campaign evolution and adaptation analysis
   - Threat actor capability development assessment
   - Victim impact scaling and propagation modeling
   - Countermeasure effectiveness evaluation

6. STRATEGIC INTELLIGENCE ASSESSMENT
   - Economic impact and financial motivation analysis
   - Regulatory and legal implications assessment
   - Industry-specific threat landscape evaluation
   - Supply chain and third-party risk analysis
   - Strategic warning indicators and early detection

7. ATTRIBUTION AND CAMPAIGN TRACKING
   - Threat actor group identification and profiling
   - Campaign timeline reconstruction and analysis
   - Infrastructure reuse and overlap detection
   - Tactics, techniques, and procedures (TTP) evolution
   - Cross-campaign pattern recognition and correlation

8. INTELLIGENCE GAPS AND COLLECTION REQUIREMENTS
   - Critical information gaps identification
   - Additional collection requirements specification
   - Source reliability and credibility assessment
   - Alternative hypothesis development and testing
   - Confidence level justification and evidence quality

ANALYTICAL STANDARDS:
- Apply structured analytic techniques to mitigate cognitive bias
- Consider alternative hypotheses and competing explanations
- Assess source reliability and information credibility
- Identify assumptions and test their validity
- Provide confidence levels with clear justification

DELIVERABLE: Comprehensive intelligence assessment suitable for executive briefing, operational planning, and strategic decision-making. Include executive summary, detailed findings, strategic recommendations, and intelligence collection requirements.""",
                
                analysis_framework=[
                    "Strategic Threat Assessment",
                    "Multi-Source Intelligence Fusion",
                    "Advanced Technical Forensics",
                    "Behavioral Intelligence Analysis",
                    "Predictive Threat Modeling",
                    "Strategic Intelligence Assessment",
                    "Attribution and Campaign Tracking",
                    "Intelligence Gaps and Collection Requirements"
                ],
                
                output_format={
                    "executive_summary": "string",
                    "threat_classification": "object",
                    "attribution_assessment": "object",
                    "technical_analysis": "object",
                    "behavioral_profile": "object",
                    "strategic_implications": "object",
                    "predictive_analysis": "object",
                    "intelligence_gaps": "array of objects",
                    "collection_requirements": "array of objects",
                    "strategic_recommendations": "array of objects",
                    "confidence_assessment": "object",
                    "alternative_hypotheses": "array of objects"
                },
                
                validation_criteria=[
                    "Analysis must employ structured analytic techniques",
                    "Attribution must be supported by multiple independent indicators",
                    "Confidence levels must reflect evidence quality and source reliability",
                    "Alternative hypotheses must be considered and evaluated",
                    "Strategic recommendations must be actionable and prioritized",
                    "Intelligence gaps must be clearly identified with collection requirements"
                ],
                
                model_requirements=[
                    AIModelCapability.TEXT_ANALYSIS,
                    AIModelCapability.PATTERN_RECOGNITION,
                    AIModelCapability.LOGICAL_REASONING,
                    AIModelCapability.TECHNICAL_ANALYSIS,
                    AIModelCapability.BEHAVIORAL_PROFILING,
                    AIModelCapability.CREATIVE_ANALYSIS
                ]
            )
        }
        
        return templates
    
    def _initialize_analysis_frameworks(self) -> Dict[str, List[str]]:
        """Initialize structured analysis frameworks for different investigation types"""
        
        return {
            "cyber_threat_intelligence": [
                "Threat Actor Identification and Profiling",
                "Campaign Attribution and Tracking",
                "Infrastructure Analysis and Correlation",
                "Tactics, Techniques, and Procedures (TTP) Analysis",
                "Victim Targeting and Selection Analysis",
                "Operational Security (OPSEC) Assessment",
                "Predictive Threat Modeling",
                "Strategic Intelligence Implications"
            ],
            
            "fraud_investigation": [
                "Entity Verification and Legitimacy Assessment",
                "Financial Motivation and Benefit Analysis",
                "Social Engineering Technique Identification",
                "Victim Impact and Scale Assessment",
                "Evidence Collection and Preservation",
                "Legal and Regulatory Implications",
                "Preventive Measures and Countermeasures",
                "Law Enforcement Coordination Requirements"
            ],
            
            "behavioral_analysis": [
                "Psychological Profiling and Motivation Assessment",
                "Communication Pattern and Style Analysis",
                "Social Engineering Sophistication Evaluation",
                "Cultural and Linguistic Indicators",
                "Operational Tempo and Timeline Analysis",
                "Decision-Making Process Evaluation",
                "Risk Tolerance and Capability Assessment",
                "Adaptation and Learning Pattern Recognition"
            ],
            
            "technical_forensics": [
                "Digital Infrastructure Analysis",
                "Network Architecture and Topology Mapping",
                "Security Control Assessment and Bypass Techniques",
                "Malware and Exploit Analysis",
                "Data Exfiltration and Communication Channels",
                "Persistence Mechanisms and Backdoor Analysis",
                "Anti-Forensics and Evasion Techniques",
                "Digital Evidence Preservation and Chain of Custody"
            ]
        }
    
    def _initialize_output_schemas(self) -> Dict[str, Dict[str, Any]]:
        """Initialize structured output schemas for consistent reporting"""
        
        return {
            "threat_assessment": {
                "threat_level": {
                    "type": "string",
                    "enum": ["low", "medium", "high", "critical"],
                    "description": "Overall threat level assessment"
                },
                "confidence_score": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 100,
                    "description": "Confidence level in the assessment (0-100%)"
                },
                "fraud_probability": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 100,
                    "description": "Probability that the target is fraudulent (0-100%)"
                },
                "primary_indicators": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Primary fraud indicators identified"
                }
            },
            
            "technical_analysis": {
                "infrastructure_assessment": {
                    "type": "object",
                    "properties": {
                        "domain_analysis": {"type": "object"},
                        "hosting_analysis": {"type": "object"},
                        "security_assessment": {"type": "object"},
                        "malware_indicators": {"type": "array"}
                    }
                },
                "network_analysis": {
                    "type": "object",
                    "properties": {
                        "ip_reputation": {"type": "object"},
                        "dns_analysis": {"type": "object"},
                        "ssl_assessment": {"type": "object"},
                        "traffic_patterns": {"type": "object"}
                    }
                }
            },
            
            "behavioral_analysis": {
                "social_engineering": {
                    "type": "object",
                    "properties": {
                        "techniques_identified": {"type": "array"},
                        "sophistication_level": {"type": "string"},
                        "target_demographics": {"type": "object"},
                        "psychological_tactics": {"type": "array"}
                    }
                },
                "communication_patterns": {
                    "type": "object",
                    "properties": {
                        "language_analysis": {"type": "object"},
                        "urgency_indicators": {"type": "array"},
                        "trust_building_methods": {"type": "array"},
                        "manipulation_techniques": {"type": "array"}
                    }
                }
            },
            
            "strategic_assessment": {
                "attribution": {
                    "type": "object",
                    "properties": {
                        "threat_actor_type": {"type": "string"},
                        "sophistication_level": {"type": "string"},
                        "resource_assessment": {"type": "object"},
                        "motivation_analysis": {"type": "object"}
                    }
                },
                "campaign_analysis": {
                    "type": "object",
                    "properties": {
                        "campaign_type": {"type": "string"},
                        "target_selection": {"type": "object"},
                        "operational_timeline": {"type": "object"},
                        "success_indicators": {"type": "array"}
                    }
                }
            }
        }
    
    def generate_investigation_prompt(
        self,
        investigation_type: InvestigationType,
        analysis_depth: AnalysisDepth,
        artifacts: List[Dict[str, Any]],
        context: Optional[str] = None,
        priority: str = "standard"
    ) -> Tuple[str, str, Dict[str, Any]]:
        """Generate optimized prompts for specific investigation requirements"""
        
        # Get prompt template
        template = self.prompt_templates.get(investigation_type.value, {}).get(analysis_depth.value)
        
        if not template:
            # Fallback to basic template
            template = self.prompt_templates[InvestigationType.URL_ANALYSIS.value][AnalysisDepth.BASIC.value]
        
        # Format artifacts for prompt
        artifact_text = self._format_artifacts_for_prompt(artifacts)
        
        # Format user prompt
        user_prompt = template.user_prompt_template.format(
            artifacts=artifact_text,
            context=context or "Standard fraud investigation request",
            priority=priority,
            url=artifacts[0].get('content', '') if artifacts and artifacts[0].get('type') == 'url' else '',
            email_content=artifacts[0].get('content', '') if artifacts and artifacts[0].get('type') == 'email' else '',
            sender=artifacts[0].get('metadata', {}).get('sender', '') if artifacts else '',
            subject=artifacts[0].get('metadata', {}).get('subject', '') if artifacts else '',
            date=artifacts[0].get('metadata', {}).get('date', '') if artifacts else ''
        )
        
        return template.system_prompt, user_prompt, template.output_format
    
    def _format_artifacts_for_prompt(self, artifacts: List[Dict[str, Any]]) -> str:
        """Format artifacts for inclusion in prompts"""
        
        formatted_artifacts = []
        
        for i, artifact in enumerate(artifacts, 1):
            artifact_type = artifact.get('type', 'unknown')
            content = artifact.get('content', '')
            metadata = artifact.get('metadata', {})
            
            formatted_artifact = f"ARTIFACT {i}: {artifact_type.upper()}\n"
            
            if artifact_type == 'url':
                formatted_artifact += f"URL: {content}\n"
            elif artifact_type == 'email':
                formatted_artifact += f"EMAIL CONTENT:\n{content}\n"
                if metadata:
                    formatted_artifact += f"METADATA: {json.dumps(metadata, indent=2)}\n"
            elif artifact_type == 'image':
                formatted_artifact += f"IMAGE: {content}\n"
                formatted_artifact += f"DESCRIPTION: {metadata.get('description', 'No description provided')}\n"
            elif artifact_type == 'document':
                formatted_artifact += f"DOCUMENT CONTENT:\n{content}\n"
                formatted_artifact += f"FILENAME: {metadata.get('filename', 'Unknown')}\n"
            else:
                formatted_artifact += f"CONTENT:\n{content}\n"
            
            formatted_artifacts.append(formatted_artifact)
        
        return "\n\n".join(formatted_artifacts)
    
    def get_model_requirements(
        self,
        investigation_type: InvestigationType,
        analysis_depth: AnalysisDepth
    ) -> List[AIModelCapability]:
        """Get AI model capability requirements for specific investigation"""
        
        template = self.prompt_templates.get(investigation_type.value, {}).get(analysis_depth.value)
        
        if template:
            return template.model_requirements
        
        # Default requirements
        return [
            AIModelCapability.TEXT_ANALYSIS,
            AIModelCapability.PATTERN_RECOGNITION,
            AIModelCapability.LOGICAL_REASONING
        ]
    
    def validate_analysis_output(
        self,
        output: Dict[str, Any],
        investigation_type: InvestigationType,
        analysis_depth: AnalysisDepth
    ) -> Tuple[bool, List[str]]:
        """Validate AI analysis output against quality criteria"""
        
        template = self.prompt_templates.get(investigation_type.value, {}).get(analysis_depth.value)
        
        if not template:
            return True, []
        
        validation_errors = []
        
        # Check required fields
        required_fields = template.output_format.keys()
        for field in required_fields:
            if field not in output:
                validation_errors.append(f"Missing required field: {field}")
        
        # Validate confidence scores
        if 'confidence_score' in output:
            confidence = output['confidence_score']
            if not isinstance(confidence, int) or confidence < 0 or confidence > 100:
                validation_errors.append("Confidence score must be an integer between 0 and 100")
        
        # Validate threat levels
        if 'threat_level' in output:
            valid_levels = ['low', 'medium', 'high', 'critical']
            if output['threat_level'] not in valid_levels:
                validation_errors.append(f"Threat level must be one of: {valid_levels}")
        
        # Check for empty critical fields
        critical_fields = ['executive_summary', 'recommendations', 'primary_indicators']
        for field in critical_fields:
            if field in output and not output[field]:
                validation_errors.append(f"Critical field '{field}' cannot be empty")
        
        return len(validation_errors) == 0, validation_errors
    
    def optimize_prompt_for_model(
        self,
        system_prompt: str,
        user_prompt: str,
        model_name: str,
        max_tokens: int = 4000
    ) -> Tuple[str, str]:
        """Optimize prompts for specific AI models"""
        
        # Model-specific optimizations
        if 'gpt-4' in model_name.lower():
            # GPT-4 optimizations
            system_prompt = self._optimize_for_gpt4(system_prompt)
            user_prompt = self._optimize_for_gpt4(user_prompt)
        
        elif 'claude' in model_name.lower():
            # Claude optimizations
            system_prompt = self._optimize_for_claude(system_prompt)
            user_prompt = self._optimize_for_claude(user_prompt)
        
        elif 'gemini' in model_name.lower():
            # Gemini optimizations
            system_prompt = self._optimize_for_gemini(system_prompt)
            user_prompt = self._optimize_for_gemini(user_prompt)
        
        elif 'deepseek' in model_name.lower():
            # DeepSeek optimizations
            system_prompt = self._optimize_for_deepseek(system_prompt)
            user_prompt = self._optimize_for_deepseek(user_prompt)
        
        # Token limit optimization
        if max_tokens:
            system_prompt, user_prompt = self._optimize_for_token_limit(
                system_prompt, user_prompt, max_tokens
            )
        
        return system_prompt, user_prompt
    
    def _optimize_for_gpt4(self, prompt: str) -> str:
        """Optimize prompts for GPT-4 models"""
        # GPT-4 responds well to structured, detailed prompts
        # Add explicit reasoning instructions
        if "ANALYSIS REQUIREMENTS:" in prompt:
            prompt = prompt.replace(
                "ANALYSIS REQUIREMENTS:",
                "ANALYSIS REQUIREMENTS:\nThink step by step and provide detailed reasoning for each conclusion.\n"
            )
        return prompt
    
    def _optimize_for_claude(self, prompt: str) -> str:
        """Optimize prompts for Claude models"""
        # Claude prefers clear structure and explicit instructions
        # Add thinking tags for better reasoning
        if "DELIVERABLE:" in prompt:
            prompt = prompt.replace(
                "DELIVERABLE:",
                "Before providing your final analysis, think through each step carefully.\n\nDELIVERABLE:"
            )
        return prompt
    
    def _optimize_for_gemini(self, prompt: str) -> str:
        """Optimize prompts for Gemini models"""
        # Gemini works well with conversational, detailed prompts
        # Add context emphasis
        if "INVESTIGATION" in prompt:
            prompt = "Please conduct a thorough and detailed investigation as requested.\n\n" + prompt
        return prompt
    
    def _optimize_for_deepseek(self, prompt: str) -> str:
        """Optimize prompts for DeepSeek models"""
        # DeepSeek excels at reasoning and technical analysis
        # Emphasize logical reasoning
        if "ANALYSIS" in prompt:
            prompt = prompt.replace(
                "ANALYSIS",
                "LOGICAL ANALYSIS (apply rigorous reasoning)"
            )
        return prompt
    
    def _optimize_for_token_limit(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int
    ) -> Tuple[str, str]:
        """Optimize prompts to fit within token limits"""
        
        # Rough token estimation (1 token ≈ 4 characters)
        total_chars = len(system_prompt) + len(user_prompt)
        estimated_tokens = total_chars // 4
        
        if estimated_tokens <= max_tokens:
            return system_prompt, user_prompt
        
        # Reduce prompt length while preserving critical information
        reduction_ratio = max_tokens / estimated_tokens
        
        # Prioritize user prompt over system prompt for reduction
        if reduction_ratio < 0.8:
            # Significant reduction needed
            system_prompt = self._compress_prompt(system_prompt, 0.7)
            user_prompt = self._compress_prompt(user_prompt, 0.9)
        else:
            # Minor reduction needed
            user_prompt = self._compress_prompt(user_prompt, reduction_ratio)
        
        return system_prompt, user_prompt
    
    def _compress_prompt(self, prompt: str, ratio: float) -> str:
        """Compress prompt while preserving essential information"""
        
        lines = prompt.split('\n')
        target_lines = int(len(lines) * ratio)
        
        # Preserve critical sections
        critical_keywords = [
            'REQUIREMENTS:', 'DELIVERABLE:', 'ANALYSIS:', 'INVESTIGATION:',
            'MISSION:', 'OBJECTIVE:', 'CRITICAL:', 'IMPORTANT:'
        ]
        
        critical_lines = []
        other_lines = []
        
        for line in lines:
            if any(keyword in line for keyword in critical_keywords):
                critical_lines.append(line)
            else:
                other_lines.append(line)
        
        # Keep all critical lines and reduce other lines
        remaining_slots = target_lines - len(critical_lines)
        if remaining_slots > 0:
            selected_other_lines = other_lines[:remaining_slots]
        else:
            selected_other_lines = []
        
        return '\n'.join(critical_lines + selected_other_lines)

# ============ PROMPT OPTIMIZATION UTILITIES ============

class PromptOptimizer:
    """Utility class for advanced prompt optimization"""
    
    @staticmethod
    def enhance_reasoning_capability(prompt: str) -> str:
        """Enhance prompt to improve AI reasoning capabilities"""
        
        reasoning_enhancers = [
            "Think step by step and show your reasoning process.",
            "Consider multiple perspectives and alternative explanations.",
            "Provide evidence for each conclusion you reach.",
            "Identify any assumptions you are making.",
            "Explain your confidence level for each assessment."
        ]
        
        # Add reasoning enhancers to the prompt
        enhanced_prompt = prompt + "\n\nREASONING INSTRUCTIONS:\n"
        enhanced_prompt += "\n".join(f"- {enhancer}" for enhancer in reasoning_enhancers)
        
        return enhanced_prompt
    
    @staticmethod
    def add_bias_mitigation(prompt: str) -> str:
        """Add bias mitigation instructions to prompts"""
        
        bias_mitigation = """
BIAS MITIGATION REQUIREMENTS:
- Consider alternative hypotheses and explanations
- Avoid confirmation bias by seeking disconfirming evidence
- Question initial assumptions and first impressions
- Consider cultural and contextual factors that might influence interpretation
- Acknowledge uncertainty and limitations in available information
- Provide balanced analysis that considers multiple viewpoints
"""
        
        return prompt + bias_mitigation
    
    @staticmethod
    def add_quality_assurance(prompt: str) -> str:
        """Add quality assurance requirements to prompts"""
        
        qa_requirements = """
QUALITY ASSURANCE STANDARDS:
- All claims must be supported by evidence from the provided artifacts
- Confidence levels must accurately reflect the strength of evidence
- Recommendations must be specific, actionable, and prioritized
- Technical analysis must be accurate and verifiable
- Language must be professional and appropriate for the intended audience
- Analysis must be comprehensive yet concise and well-organized
"""
        
        return prompt + qa_requirements

# ============ SPECIALIZED PROMPT GENERATORS ============

class SpecializedPromptGenerator:
    """Generator for specialized investigation prompts"""
    
    @staticmethod
    def generate_threat_attribution_prompt(artifacts: List[Dict[str, Any]], context: str) -> str:
        """Generate specialized prompt for threat attribution analysis"""
        
        return f"""CLASSIFIED: THREAT ATTRIBUTION ANALYSIS

MISSION: Conduct advanced threat actor attribution analysis using intelligence community methodologies.

TARGET ARTIFACTS:
{SpecializedPromptGenerator._format_artifacts(artifacts)}

OPERATIONAL CONTEXT:
{context}

ATTRIBUTION ANALYSIS REQUIREMENTS:

1. THREAT ACTOR PROFILING
   - Sophistication level assessment (script kiddie/criminal/nation-state)
   - Resource and capability evaluation
   - Operational security (OPSEC) assessment
   - Historical campaign correlation

2. TECHNICAL ATTRIBUTION INDICATORS
   - Infrastructure overlap and reuse patterns
   - Tool and technique fingerprinting
   - Code similarity and development patterns
   - Operational timing and geographic indicators

3. BEHAVIORAL ATTRIBUTION ANALYSIS
   - Language and cultural indicators
   - Target selection methodology
   - Operational tempo and patterns
   - Motivation and objective assessment

4. CAMPAIGN CORRELATION
   - Historical threat data correlation
   - Cross-campaign pattern recognition
   - Infrastructure timeline analysis
   - Victim overlap and targeting patterns

DELIVERABLE: Comprehensive threat attribution assessment with confidence levels and supporting evidence."""
    
    @staticmethod
    def generate_predictive_analysis_prompt(artifacts: List[Dict[str, Any]], context: str) -> str:
        """Generate specialized prompt for predictive threat analysis"""
        
        return f"""INTELLIGENCE ASSESSMENT: PREDICTIVE THREAT ANALYSIS

MISSION: Conduct predictive threat modeling and future attack vector analysis.

CURRENT THREAT INDICATORS:
{SpecializedPromptGenerator._format_artifacts(artifacts)}

ANALYSIS CONTEXT:
{context}

PREDICTIVE ANALYSIS REQUIREMENTS:

1. THREAT EVOLUTION MODELING
   - Campaign adaptation and learning patterns
   - Technique sophistication progression
   - Infrastructure evolution and migration
   - Countermeasure adaptation analysis

2. FUTURE ATTACK VECTOR PREDICTION
   - Likely next-phase attack methods
   - Target expansion and selection evolution
   - Technology adoption and exploitation trends
   - Seasonal and temporal pattern analysis

3. IMPACT SCALING ASSESSMENT
   - Victim population growth modeling
   - Financial impact progression analysis
   - Geographic expansion patterns
   - Industry sector targeting evolution

4. COUNTERMEASURE EFFECTIVENESS EVALUATION
   - Current protection gap analysis
   - Defensive measure bypass probability
   - Detection evasion technique prediction
   - Mitigation strategy effectiveness assessment

DELIVERABLE: Predictive threat assessment with timeline projections and strategic recommendations."""
    
    @staticmethod
    def _format_artifacts(artifacts: List[Dict[str, Any]]) -> str:
        """Format artifacts for specialized prompts"""
        formatted = []
        for i, artifact in enumerate(artifacts, 1):
            formatted.append(f"ARTIFACT {i}: {artifact.get('type', 'unknown').upper()}")
            formatted.append(f"Content: {artifact.get('content', '')[:500]}...")
            if artifact.get('metadata'):
                formatted.append(f"Metadata: {json.dumps(artifact['metadata'], indent=2)}")
            formatted.append("")
        return "\n".join(formatted)

# ============ PROMPT TEMPLATE REGISTRY ============

class PromptTemplateRegistry:
    """Registry for managing and versioning prompt templates"""
    
    def __init__(self):
        self.templates = {}
        self.versions = {}
    
    def register_template(
        self,
        template_id: str,
        template: PromptTemplate,
        version: str = "1.0"
    ):
        """Register a new prompt template"""
        if template_id not in self.templates:
            self.templates[template_id] = {}
            self.versions[template_id] = []
        
        self.templates[template_id][version] = template
        self.versions[template_id].append(version)
    
    def get_template(
        self,
        template_id: str,
        version: Optional[str] = None
    ) -> Optional[PromptTemplate]:
        """Get a prompt template by ID and version"""
        if template_id not in self.templates:
            return None
        
        if version is None:
            # Get latest version
            latest_version = max(self.versions[template_id])
            return self.templates[template_id][latest_version]
        
        return self.templates[template_id].get(version)
    
    def list_templates(self) -> List[str]:
        """List all available template IDs"""
        return list(self.templates.keys())
    
    def get_template_versions(self, template_id: str) -> List[str]:
        """Get all versions of a template"""
        return self.versions.get(template_id, [])

# Initialize global prompt engineer instance
prompt_engineer = AdvancedPromptEngineer()
prompt_optimizer = PromptOptimizer()
specialized_generator = SpecializedPromptGenerator()
template_registry = PromptTemplateRegistry()

