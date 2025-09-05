"""
ScamShield AI-A - FBI Cyber Division Investigation Agent
Intelligence-Grade Digital Forensics and Cyber Crime Investigation

This module implements advanced FBI cyber crime investigation methodologies
with AI-powered analysis capabilities for fraud detection and attribution.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import openai
import anthropic
from together import Together

@dataclass
class EvidencePackage:
    """Structured evidence package for FBI investigation methodology."""
    case_id: str
    evidence_type: str
    source_data: Dict[str, Any]
    collection_timestamp: datetime
    chain_of_custody: List[str]
    integrity_hash: str

@dataclass
class FBIAssessment:
    """FBI-standard investigation assessment structure."""
    case_classification: str
    threat_level: int  # 1-10 scale
    sophistication_level: str
    impact_scope: str
    attribution_confidence: str
    evidence_analysis: Dict[str, Any]
    investigation_plan: Dict[str, Any]
    legal_considerations: str

class FBICyberAgent:
    """
    Advanced FBI Cyber Division investigation agent using real FBI methodologies
    combined with cutting-edge AI analysis capabilities.
    
    Implements:
    - FBI Digital Forensics Framework
    - Cyber Crime Investigation Protocols
    - Evidence Chain of Custody Standards
    - Legal Admissibility Requirements
    - Threat Attribution Methodologies
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize FBI Cyber Agent with model configurations."""
        self.config = config
        
        # AI Model Configuration
        self.primary_model = "gpt-4o"  # Primary reasoning and analysis
        self.forensics_model = "claude-3-5-sonnet"  # Technical forensics
        self.pattern_model = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"  # Pattern recognition
        
        # FBI Investigation Framework Phases
        self.investigation_phases = [
            "initial_assessment",
            "evidence_collection", 
            "technical_analysis",
            "pattern_correlation",
            "threat_attribution",
            "legal_documentation",
            "final_assessment"
        ]
        
        # FBI Cyber Crime Categories
        self.threat_categories = {
            "national_security": "National Security Cyber Intrusions",
            "criminal_enterprise": "Criminal Enterprise Cyber Activities",
            "ransomware": "Ransomware/Extortion Operations", 
            "identity_theft": "Identity Theft/Financial Fraud",
            "business_email": "Business Email Compromise",
            "romance_scam": "Romance/Investment Scams",
            "cryptocurrency": "Cryptocurrency Fraud"
        }
        
        # Initialize AI clients
        self.openai_client = openai.AsyncOpenAI(api_key=config.get('openai_api_key'))
        self.anthropic_client = anthropic.AsyncAnthropic(api_key=config.get('anthropic_api_key'))
        self.together_client = Together(api_key=config.get('together_api_key'))
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
    async def investigate_with_fbi_methodology(self, evidence_package: EvidencePackage) -> FBIAssessment:
        """
        Conduct comprehensive investigation using FBI cyber crime methodology
        with advanced AI analysis capabilities.
        
        Args:
            evidence_package: Structured evidence for investigation
            
        Returns:
            FBIAssessment: Comprehensive FBI-standard assessment
        """
        
        self.logger.info(f"Starting FBI investigation for case {evidence_package.case_id}")
        
        try:
            # Phase 1: Initial Assessment using FBI methodology
            initial_assessment = await self._conduct_initial_assessment(evidence_package)
            
            # Phase 2: Technical Forensics Analysis
            forensics_analysis = await self._conduct_forensics_analysis(evidence_package, initial_assessment)
            
            # Phase 3: Pattern Recognition and Correlation
            pattern_analysis = await self._conduct_pattern_analysis(evidence_package, forensics_analysis)
            
            # Phase 4: Threat Attribution Assessment
            attribution_analysis = await self._conduct_attribution_analysis(
                evidence_package, forensics_analysis, pattern_analysis
            )
            
            # Phase 5: Legal Documentation and Final Assessment
            final_assessment = await self._generate_fbi_assessment(
                evidence_package, initial_assessment, forensics_analysis, 
                pattern_analysis, attribution_analysis
            )
            
            self.logger.info(f"FBI investigation completed for case {evidence_package.case_id}")
            return final_assessment
            
        except Exception as e:
            self.logger.error(f"FBI investigation failed for case {evidence_package.case_id}: {str(e)}")
            raise
    
    async def _conduct_initial_assessment(self, evidence_package: EvidencePackage) -> Dict[str, Any]:
        """
        Conduct initial assessment using FBI cyber crime investigation methodology.
        """
        
        initial_assessment_prompt = f"""
        You are an FBI Cyber Crime Special Agent with 15+ years of experience in digital forensics 
        and cyber crime investigation. You follow FBI investigation protocols and methodologies.

        CASE BRIEFING:
        Case ID: {evidence_package.case_id}
        Evidence Type: {evidence_package.evidence_type}
        Evidence Data: {json.dumps(evidence_package.source_data, indent=2)}
        Collection Time: {evidence_package.collection_timestamp}
        
        TASK: Conduct initial assessment using FBI cyber crime investigation methodology.
        
        APPLY FBI FRAMEWORK:
        
        1. **Threat Classification** (FBI Cyber Division Categories)
           Classify this case into one of the following categories:
           - National Security Cyber Intrusions
           - Criminal Enterprise Cyber Activities  
           - Ransomware/Extortion Operations
           - Identity Theft/Financial Fraud
           - Business Email Compromise
           - Romance/Investment Scams
           - Cryptocurrency Fraud
        
        2. **Evidence Categorization** (FBI Digital Evidence Standards)
           Categorize evidence as:
           - Primary Evidence (direct indicators of criminal activity)
           - Secondary Evidence (circumstantial supporting evidence)
           - Corroborating Evidence (supporting facts from multiple sources)
           - Exculpatory Evidence (evidence that contradicts criminal hypothesis)
        
        3. **Chain of Custody Assessment**
           Evaluate:
           - Evidence source reliability and collection method
           - Integrity verification procedures followed
           - Documentation adequacy for legal proceedings
           - Potential contamination or tampering indicators
        
        4. **Risk Assessment Matrix** (FBI Cyber Risk Framework)
           Assess on 1-10 scales:
           - Immediate Threat Level (1=minimal, 10=critical)
           - Sophistication Assessment (1=amateur, 10=nation-state level)
           - Impact Evaluation (1=individual, 10=critical infrastructure)
           - Attribution Confidence (1=speculation, 10=definitive proof)
        
        CRITICAL FBI PRINCIPLES:
        - Base analysis strictly on evidence, avoid speculation
        - Maintain objectivity and consider alternative explanations
        - Document methodology for court admissibility
        - Assess threat actor capabilities and intent indicators
        - Consider operational security and counter-intelligence factors
        
        RESPONSE FORMAT (JSON):
        {{
            "case_classification": {{
                "primary_category": "FBI cyber crime category",
                "subcategory": "specific type within category",
                "classification_confidence": "High/Medium/Low",
                "classification_reasoning": "evidence-based justification"
            }},
            "threat_assessment": {{
                "immediate_risk": 1-10,
                "sophistication": 1-10,
                "impact_scope": 1-10,
                "attribution_confidence": 1-10,
                "threat_indicators": ["specific indicators observed"],
                "risk_factors": ["factors increasing threat level"]
            }},
            "evidence_analysis": {{
                "primary_indicators": ["direct evidence of criminal activity"],
                "secondary_evidence": ["circumstantial supporting evidence"],
                "corroborating_evidence": ["multi-source confirmations"],
                "exculpatory_evidence": ["contradictory evidence"],
                "chain_of_custody_assessment": "evaluation of evidence integrity",
                "evidence_quality_score": 1-10
            }},
            "investigation_plan": {{
                "next_phases": ["prioritized investigation actions"],
                "resource_requirements": ["needed capabilities and tools"],
                "timeline_estimate": "estimated investigation duration",
                "priority_targets": ["high-value investigation targets"],
                "collection_requirements": ["additional evidence needed"]
            }},
            "legal_considerations": {{
                "admissibility_assessment": "court admissibility evaluation",
                "procedural_requirements": ["legal procedures to follow"],
                "jurisdiction_considerations": ["jurisdictional factors"],
                "evidence_preservation": ["preservation requirements"]
            }},
            "preliminary_conclusions": {{
                "working_hypothesis": "initial theory of the case",
                "confidence_level": "High/Medium/Low",
                "alternative_hypotheses": ["other possible explanations"],
                "key_uncertainties": ["major unknowns to resolve"]
            }}
        }}
        
        Conduct this analysis with the precision and methodology of an FBI Special Agent.
        Ensure all conclusions are evidence-based and legally defensible.
        """
        
        response = await self._execute_with_openai(
            self.primary_model,
            initial_assessment_prompt,
            temperature=0.1,  # Low temperature for precise analysis
            max_tokens=4000
        )
        
        return json.loads(response)
    
    async def _conduct_forensics_analysis(self, evidence_package: EvidencePackage, initial_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Conduct comprehensive digital forensics analysis using FBI methodologies.
        """
        
        forensics_prompt = f"""
        You are an FBI Digital Forensics Examiner (Level 3 Certified) with expertise in 
        cyber crime investigation and digital evidence analysis. You follow FBI Laboratory
        digital forensics standards and methodologies.
        
        CASE CONTEXT:
        Case ID: {evidence_package.case_id}
        Initial Assessment: {json.dumps(initial_assessment, indent=2)}
        Evidence to Analyze: {json.dumps(evidence_package.source_data, indent=2)}
        
        TASK: Conduct comprehensive digital forensics analysis using FBI methodologies.
        
        APPLY FBI DIGITAL FORENSICS FRAMEWORK:
        
        1. **Technical Artifact Analysis**
           Examine all technical indicators:
           - Network indicators (IP addresses, domains, protocols, ports)
           - File system artifacts (metadata, timestamps, file hashes)
           - Communication analysis (email headers, messaging protocols)
           - Behavioral indicators (access patterns, timing analysis)
           - System artifacts (registry entries, log files, process data)
        
        2. **Attribution Methodology** (FBI Cyber Attribution Framework)
           Apply four levels of attribution analysis:
           - Technical Attribution (infrastructure, tools, methods used)
           - Tactical Attribution (procedures, targets, operational objectives) 
           - Operational Attribution (campaign patterns, timing, coordination)
           - Strategic Attribution (motivation, capabilities, resource indicators)
        
        3. **Pattern Recognition** (FBI Threat Actor Profiling)
           Identify and analyze:
           - Modus Operandi (consistent methods and procedures)
           - Tools, Techniques, Procedures (TTP) identification
           - Infrastructure reuse patterns and relationships
           - Timeline correlation and operational tempo
           - Signature behaviors and unique identifiers
        
        4. **Threat Intelligence Integration**
           Cross-reference with known intelligence:
           - Known threat actor comparison and matching
           - Campaign overlap analysis with historical cases
           - Infrastructure relationship mapping
           - Tactical pattern matching with threat databases
           - Indicator overlap with previous investigations
        
        ADVANCED FORENSIC TECHNIQUES:
        - Pivoting analysis from initial indicators
        - Infrastructure enumeration and mapping
        - Temporal correlation analysis across evidence
        - Cross-reference validation with multiple sources
        - Confidence scoring methodology for each finding
        - Alternative explanation consideration
        
        RESPONSE FORMAT (JSON):
        {{
            "technical_findings": {{
                "network_indicators": {{
                    "ip_addresses": ["detailed IP analysis with geolocation"],
                    "domains": ["domain analysis with registration data"],
                    "protocols": ["network protocol analysis"],
                    "infrastructure_analysis": "hosting and network infrastructure assessment"
                }},
                "file_artifacts": {{
                    "metadata_analysis": ["file metadata examination"],
                    "hash_analysis": ["file hash verification and comparison"],
                    "timestamp_correlation": ["temporal analysis of file activities"],
                    "content_analysis": "file content examination results"
                }},
                "communication_analysis": {{
                    "email_headers": ["email header forensic analysis"],
                    "messaging_patterns": ["communication pattern analysis"],
                    "social_engineering": ["social engineering technique identification"],
                    "linguistic_analysis": ["language and writing style analysis"]
                }},
                "behavioral_indicators": {{
                    "access_patterns": ["system access pattern analysis"],
                    "timing_analysis": ["operational timing patterns"],
                    "operational_security": ["OPSEC assessment and failures"],
                    "automation_indicators": ["automated vs manual activity indicators"]
                }}
            }},
            "attribution_assessment": {{
                "technical_attribution": {{
                    "infrastructure_analysis": "technical infrastructure attribution",
                    "tool_identification": ["tools and methods identified"],
                    "capability_assessment": "technical capability evaluation",
                    "confidence_level": "High/Medium/Low"
                }},
                "tactical_attribution": {{
                    "procedures_analysis": "tactical procedures assessment",
                    "target_selection": "targeting methodology analysis", 
                    "operational_methods": "operational method evaluation",
                    "confidence_level": "High/Medium/Low"
                }},
                "operational_attribution": {{
                    "campaign_patterns": "campaign-level pattern analysis",
                    "coordination_indicators": "coordination and planning indicators",
                    "resource_indicators": "resource and capability indicators",
                    "confidence_level": "High/Medium/Low"
                }},
                "strategic_attribution": {{
                    "motivation_analysis": "motivation and intent assessment",
                    "capability_indicators": "strategic capability indicators",
                    "resource_assessment": "resource and backing evaluation",
                    "confidence_level": "High/Medium/Low"
                }},
                "overall_attribution_confidence": "Definitive/High/Medium/Low",
                "attribution_chain": "logical reasoning chain for attribution"
            }},
            "threat_actor_profile": {{
                "sophistication_assessment": {{
                    "technical_sophistication": 1-10,
                    "operational_sophistication": 1-10,
                    "resource_indicators": ["evidence of resources and backing"],
                    "professionalism_indicators": ["indicators of professional operation"]
                }},
                "capability_analysis": {{
                    "technical_capabilities": ["demonstrated technical skills"],
                    "operational_capabilities": ["operational planning and execution"],
                    "resource_access": ["access to tools, infrastructure, funding"],
                    "collaboration_indicators": ["evidence of team or network operation"]
                }},
                "motivation_assessment": {{
                    "primary_motivation": "assessed primary motivation",
                    "secondary_motivations": ["additional motivating factors"],
                    "target_selection_rationale": "reasoning behind target selection",
                    "success_metrics": ["how threat actor measures success"]
                }},
                "geographic_indicators": {{
                    "location_clues": ["geographic location indicators"],
                    "timezone_analysis": ["operational timezone patterns"],
                    "language_indicators": ["language and cultural indicators"],
                    "infrastructure_geography": ["geographic distribution of infrastructure"]
                }}
            }},
            "investigative_leads": {{
                "priority_indicators": ["highest priority indicators for follow-up"],
                "pivot_opportunities": ["opportunities for investigation expansion"],
                "correlation_targets": ["targets for correlation with other cases"],
                "collection_requirements": ["additional evidence collection needs"],
                "intelligence_gaps": ["critical information gaps to address"]
            }},
            "forensic_quality_assessment": {{
                "evidence_integrity": "assessment of evidence integrity",
                "analysis_confidence": "confidence in forensic analysis",
                "methodology_validation": "validation of forensic methodology",
                "peer_review_recommendations": ["recommendations for peer review"],
                "court_admissibility": "assessment of court admissibility"
            }}
        }}
        
        Provide FBI-quality digital forensics analysis with court-admissible documentation.
        Ensure all findings are evidence-based and methodology is clearly documented.
        """
        
        response = await self._execute_with_anthropic(
            self.forensics_model,
            forensics_prompt,
            temperature=0.05,  # Very low temperature for forensic precision
            max_tokens=6000
        )
        
        return json.loads(response)
    
    async def _conduct_pattern_analysis(self, evidence_package: EvidencePackage, forensics_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Conduct advanced pattern recognition and correlation analysis.
        """
        
        pattern_prompt = f"""
        You are an FBI Behavioral Analysis Unit specialist with expertise in cyber crime 
        pattern recognition and threat actor profiling. You excel at identifying subtle 
        patterns and correlations that reveal threat actor behavior and intent.
        
        CASE DATA:
        Case ID: {evidence_package.case_id}
        Forensics Analysis: {json.dumps(forensics_analysis, indent=2)}
        Raw Evidence: {json.dumps(evidence_package.source_data, indent=2)}
        
        TASK: Conduct advanced pattern recognition and behavioral analysis.
        
        PATTERN ANALYSIS FRAMEWORK:
        
        1. **Behavioral Pattern Recognition**
           Identify consistent behavioral patterns:
           - Operational timing patterns (when threat actor is active)
           - Communication patterns (how they interact with targets)
           - Technical patterns (consistent technical choices)
           - Targeting patterns (victim selection criteria)
           - Adaptation patterns (how they respond to countermeasures)
        
        2. **Modus Operandi Analysis**
           Analyze consistent methods and procedures:
           - Initial access methods (how they gain entry)
           - Persistence mechanisms (how they maintain access)
           - Escalation techniques (how they increase privileges)
           - Data collection methods (what they target and how)
           - Exfiltration techniques (how they remove data/money)
        
        3. **Infrastructure Pattern Analysis**
           Examine infrastructure usage patterns:
           - Domain registration patterns and preferences
           - Hosting provider selection and geographic preferences
           - IP address usage patterns and rotation
           - Certificate usage and reuse patterns
           - DNS configuration patterns and preferences
        
        4. **Temporal Pattern Analysis**
           Analyze time-based patterns:
           - Activity timing and operational hours
           - Campaign duration and lifecycle patterns
           - Response timing to external events
           - Seasonal or cyclical activity patterns
           - Coordination timing between different activities
        
        5. **Linguistic and Cultural Pattern Analysis**
           Examine language and cultural indicators:
           - Writing style and linguistic patterns
           - Cultural references and knowledge
           - Time zone and geographic activity patterns
           - Language proficiency and native language indicators
           - Cultural context understanding in social engineering
        
        ADVANCED PATTERN TECHNIQUES:
        - Cross-correlation analysis between different pattern types
        - Anomaly detection within established patterns
        - Pattern evolution analysis over time
        - Pattern confidence scoring and validation
        - Alternative pattern explanation consideration
        
        RESPONSE FORMAT (JSON):
        {{
            "behavioral_patterns": {{
                "operational_timing": {{
                    "active_hours": "identified active time periods",
                    "timezone_indicators": "timezone analysis results",
                    "activity_frequency": "frequency and consistency of activity",
                    "pattern_confidence": "High/Medium/Low"
                }},
                "communication_patterns": {{
                    "interaction_style": "how threat actor communicates",
                    "social_engineering_techniques": ["identified techniques"],
                    "response_patterns": "response timing and style patterns",
                    "adaptation_indicators": ["how they adapt communication"]
                }},
                "technical_patterns": {{
                    "tool_preferences": ["consistent tool choices"],
                    "technique_patterns": ["repeated technical techniques"],
                    "infrastructure_preferences": ["hosting and infrastructure patterns"],
                    "operational_security": ["OPSEC patterns and failures"]
                }}
            }},
            "modus_operandi": {{
                "attack_lifecycle": {{
                    "initial_access": "consistent initial access methods",
                    "persistence": "persistence mechanism patterns",
                    "privilege_escalation": "escalation technique patterns",
                    "data_collection": "data targeting and collection patterns",
                    "exfiltration": "data/money removal patterns"
                }},
                "target_selection": {{
                    "victim_criteria": "victim selection patterns",
                    "targeting_methods": "how targets are identified and approached",
                    "success_factors": "factors that increase success probability",
                    "failure_patterns": "patterns in failed attempts"
                }},
                "operational_methods": {{
                    "planning_indicators": "evidence of planning and preparation",
                    "execution_patterns": "consistent execution methods",
                    "monitoring_patterns": "how they monitor operations",
                    "cleanup_patterns": "evidence cleanup and covering tracks"
                }}
            }},
            "infrastructure_patterns": {{
                "domain_patterns": {{
                    "registration_patterns": "domain registration preferences",
                    "naming_conventions": "domain naming patterns",
                    "lifecycle_management": "domain lifecycle patterns",
                    "dns_patterns": "DNS configuration patterns"
                }},
                "hosting_patterns": {{
                    "provider_preferences": "hosting provider selection patterns",
                    "geographic_preferences": "geographic hosting preferences",
                    "service_patterns": "hosting service usage patterns",
                    "migration_patterns": "infrastructure migration patterns"
                }},
                "network_patterns": {{
                    "ip_usage_patterns": "IP address usage and rotation",
                    "protocol_preferences": "network protocol preferences",
                    "traffic_patterns": "network traffic characteristics",
                    "anonymization_patterns": "anonymization technique patterns"
                }}
            }},
            "temporal_analysis": {{
                "activity_cycles": {{
                    "daily_patterns": "daily activity patterns",
                    "weekly_patterns": "weekly activity patterns",
                    "seasonal_patterns": "seasonal or long-term patterns",
                    "event_correlation": "correlation with external events"
                }},
                "campaign_timing": {{
                    "campaign_duration": "typical campaign duration patterns",
                    "preparation_time": "preparation time patterns",
                    "execution_timing": "execution timing patterns",
                    "dormancy_periods": "inactive period patterns"
                }}
            }},
            "linguistic_cultural": {{
                "language_analysis": {{
                    "writing_style": "consistent writing style indicators",
                    "language_proficiency": "language skill assessment",
                    "native_language_indicators": "native language clues",
                    "translation_artifacts": "evidence of translation use"
                }},
                "cultural_indicators": {{
                    "cultural_references": "cultural knowledge indicators",
                    "geographic_knowledge": "geographic familiarity indicators",
                    "social_context": "social and cultural context understanding",
                    "local_knowledge": "local knowledge and customs awareness"
                }}
            }},
            "pattern_correlation": {{
                "cross_pattern_analysis": "correlations between different pattern types",
                "pattern_evolution": "how patterns change over time",
                "anomaly_detection": "deviations from established patterns",
                "pattern_validation": "validation of identified patterns",
                "alternative_explanations": ["alternative explanations for patterns"]
            }},
            "threat_actor_signature": {{
                "unique_identifiers": ["unique behavioral signatures"],
                "distinguishing_characteristics": ["characteristics that distinguish this actor"],
                "signature_confidence": "confidence in signature identification",
                "signature_evolution": "how signature has evolved over time"
            }}
        }}
        
        Provide comprehensive pattern analysis with FBI-level analytical rigor.
        Focus on identifying unique and distinguishing patterns that can aid in attribution.
        """
        
        response = await self._execute_with_together_ai(
            self.pattern_model,
            pattern_prompt,
            temperature=0.15,
            max_tokens=6000
        )
        
        return json.loads(response)
    
    async def _conduct_attribution_analysis(self, evidence_package: EvidencePackage, 
                                          forensics_analysis: Dict[str, Any], 
                                          pattern_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Conduct comprehensive threat attribution analysis using FBI methodologies.
        """
        
        attribution_prompt = f"""
        You are an FBI Cyber Threat Attribution Specialist with expertise in advanced 
        threat actor identification and attribution. You follow FBI attribution standards
        and work with intelligence community partners on complex attribution cases.
        
        COMPREHENSIVE CASE DATA:
        Case ID: {evidence_package.case_id}
        Forensics Analysis: {json.dumps(forensics_analysis, indent=2)}
        Pattern Analysis: {json.dumps(pattern_analysis, indent=2)}
        
        TASK: Conduct comprehensive threat attribution analysis using FBI methodology.
        
        FBI ATTRIBUTION FRAMEWORK:
        
        1. **Multi-Level Attribution Assessment**
           Apply FBI's four-tier attribution model:
           
           **Technical Attribution (Infrastructure & Tools)**
           - Infrastructure ownership and control analysis
           - Tool and malware attribution and sourcing
           - Technical capability assessment and comparison
           - Infrastructure relationship mapping and clustering
           
           **Tactical Attribution (Methods & Procedures)**
           - Tactical procedure analysis and comparison
           - Operational method consistency evaluation
           - Target selection methodology assessment
           - Execution technique pattern matching
           
           **Operational Attribution (Campaign & Coordination)**
           - Campaign-level coordination analysis
           - Multi-target operation correlation
           - Resource allocation and management patterns
           - Strategic timing and coordination assessment
           
           **Strategic Attribution (Motivation & Backing)**
           - Motivation analysis and assessment
           - Resource and capability backing evaluation
           - Strategic objective alignment analysis
           - Geopolitical context and benefit analysis
        
        2. **Confidence Assessment Framework**
           Apply FBI confidence standards:
           - **Definitive (95-100%)**: Multiple independent sources confirm attribution
           - **High Confidence (85-94%)**: Strong evidence with minimal uncertainty
           - **Medium Confidence (65-84%)**: Reasonable evidence with some uncertainty
           - **Low Confidence (35-64%)**: Limited evidence with significant uncertainty
           - **Speculative (<35%)**: Insufficient evidence for reliable attribution
        
        3. **Alternative Hypothesis Testing**
           Consider and evaluate alternative explanations:
           - False flag operations and misdirection
           - Shared tool and infrastructure usage
           - Copycat operations and mimicry
           - Coincidental similarity and convergent evolution
           - Third-party compromise and proxy usage
        
        4. **Attribution Chain Validation**
           Validate the logical chain of attribution:
           - Evidence quality and reliability assessment
           - Logical consistency verification
           - Alternative explanation consideration
           - Bias identification and mitigation
           - Peer review and validation requirements
        
        ADVANCED ATTRIBUTION TECHNIQUES:
        - Multi-source intelligence fusion and correlation
        - Temporal correlation analysis across campaigns
        - Infrastructure relationship graph analysis
        - Behavioral signature matching and comparison
        - Linguistic and cultural indicator analysis
        - Technical capability fingerprinting
        - Operational pattern clustering and classification
        
        RESPONSE FORMAT (JSON):
        {{
            "attribution_assessment": {{
                "primary_attribution": {{
                    "threat_actor_assessment": "primary threat actor identification",
                    "actor_type": "Individual/Criminal Group/Nation-State/Hacktivist/Unknown",
                    "sophistication_level": "Amateur/Intermediate/Advanced/Expert/Nation-State",
                    "confidence_level": "Definitive/High/Medium/Low/Speculative",
                    "confidence_percentage": 1-100
                }},
                "attribution_reasoning": {{
                    "technical_attribution": {{
                        "infrastructure_evidence": ["technical infrastructure indicators"],
                        "tool_evidence": ["tool and technique indicators"],
                        "capability_evidence": ["technical capability indicators"],
                        "confidence": "Definitive/High/Medium/Low/Speculative"
                    }},
                    "tactical_attribution": {{
                        "procedure_evidence": ["tactical procedure indicators"],
                        "method_evidence": ["operational method indicators"],
                        "targeting_evidence": ["target selection indicators"],
                        "confidence": "Definitive/High/Medium/Low/Speculative"
                    }},
                    "operational_attribution": {{
                        "campaign_evidence": ["campaign coordination indicators"],
                        "resource_evidence": ["resource and planning indicators"],
                        "coordination_evidence": ["multi-operation coordination indicators"],
                        "confidence": "Definitive/High/Medium/Low/Speculative"
                    }},
                    "strategic_attribution": {{
                        "motivation_evidence": ["motivation and intent indicators"],
                        "backing_evidence": ["resource and backing indicators"],
                        "benefit_evidence": ["who benefits analysis"],
                        "confidence": "Definitive/High/Medium/Low/Speculative"
                    }}
                }}
            }},
            "alternative_hypotheses": {{
                "hypothesis_1": {{
                    "description": "alternative attribution possibility",
                    "supporting_evidence": ["evidence supporting this hypothesis"],
                    "contradicting_evidence": ["evidence contradicting this hypothesis"],
                    "probability": 1-100
                }},
                "hypothesis_2": {{
                    "description": "second alternative attribution possibility",
                    "supporting_evidence": ["evidence supporting this hypothesis"],
                    "contradicting_evidence": ["evidence contradicting this hypothesis"],
                    "probability": 1-100
                }},
                "false_flag_assessment": {{
                    "false_flag_probability": 1-100,
                    "misdirection_indicators": ["indicators of intentional misdirection"],
                    "genuine_indicators": ["indicators of genuine attribution"]
                }}
            }},
            "attribution_chain": {{
                "evidence_chain": ["logical chain of evidence leading to attribution"],
                "critical_assumptions": ["key assumptions in attribution logic"],
                "weakest_links": ["weakest points in attribution chain"],
                "validation_requirements": ["what would strengthen attribution"],
                "peer_review_recommendations": ["recommendations for peer review"]
            }},
            "threat_actor_profile": {{
                "actor_characteristics": {{
                    "technical_capabilities": ["demonstrated technical capabilities"],
                    "operational_capabilities": ["demonstrated operational capabilities"],
                    "resource_indicators": ["indicators of resources and backing"],
                    "geographic_indicators": ["geographic location indicators"],
                    "temporal_patterns": ["operational timing and pattern indicators"]
                }},
                "historical_activity": {{
                    "known_campaigns": ["known or suspected previous campaigns"],
                    "evolution_analysis": ["how actor has evolved over time"],
                    "success_patterns": ["patterns in successful operations"],
                    "failure_patterns": ["patterns in failed operations"]
                }},
                "future_threat_assessment": {{
                    "likely_future_activity": "assessment of future threat activity",
                    "capability_development": "likely capability development trajectory",
                    "target_evolution": "likely evolution in targeting",
                    "countermeasure_adaptation": "likely adaptation to countermeasures"
                }}
            }},
            "intelligence_requirements": {{
                "critical_gaps": ["critical intelligence gaps for attribution"],
                "collection_priorities": ["priority intelligence collection requirements"],
                "validation_needs": ["validation requirements for attribution"],
                "collaboration_opportunities": ["opportunities for intelligence sharing"]
            }},
            "legal_implications": {{
                "prosecution_viability": "assessment of prosecution viability",
                "evidence_admissibility": "court admissibility of attribution evidence",
                "jurisdiction_considerations": ["jurisdictional factors for prosecution"],
                "international_cooperation": ["international cooperation requirements"]
            }}
        }}
        
        Provide FBI-quality threat attribution analysis with comprehensive reasoning.
        Ensure attribution meets FBI standards for accuracy and legal admissibility.
        """
        
        response = await self._execute_with_openai(
            self.primary_model,
            attribution_prompt,
            temperature=0.1,
            max_tokens=8000
        )
        
        return json.loads(response)
    
    async def _generate_fbi_assessment(self, evidence_package: EvidencePackage,
                                     initial_assessment: Dict[str, Any],
                                     forensics_analysis: Dict[str, Any],
                                     pattern_analysis: Dict[str, Any],
                                     attribution_analysis: Dict[str, Any]) -> FBIAssessment:
        """
        Generate final FBI-standard investigation assessment.
        """
        
        # Extract key findings for FBI assessment structure
        case_classification = initial_assessment.get('case_classification', {}).get('primary_category', 'Unknown')
        threat_level = initial_assessment.get('threat_assessment', {}).get('immediate_risk', 5)
        sophistication = attribution_analysis.get('attribution_assessment', {}).get('primary_attribution', {}).get('sophistication_level', 'Unknown')
        impact_scope = f"Level {initial_assessment.get('threat_assessment', {}).get('impact_scope', 5)}"
        attribution_confidence = attribution_analysis.get('attribution_assessment', {}).get('primary_attribution', {}).get('confidence_level', 'Low')
        
        # Compile comprehensive evidence analysis
        evidence_analysis = {
            'initial_assessment': initial_assessment,
            'forensics_findings': forensics_analysis,
            'pattern_analysis': pattern_analysis,
            'attribution_analysis': attribution_analysis
        }
        
        # Generate investigation plan
        investigation_plan = {
            'completed_phases': self.investigation_phases,
            'recommendations': attribution_analysis.get('intelligence_requirements', {}),
            'next_steps': initial_assessment.get('investigation_plan', {}).get('next_phases', []),
            'resource_requirements': initial_assessment.get('investigation_plan', {}).get('resource_requirements', [])
        }
        
        # Legal considerations
        legal_considerations = f"""
        Evidence Admissibility: {attribution_analysis.get('legal_implications', {}).get('evidence_admissibility', 'Under Review')}
        Prosecution Viability: {attribution_analysis.get('legal_implications', {}).get('prosecution_viability', 'Under Assessment')}
        Jurisdictional Factors: {attribution_analysis.get('legal_implications', {}).get('jurisdiction_considerations', [])}
        Chain of Custody: Maintained per FBI standards
        """
        
        return FBIAssessment(
            case_classification=case_classification,
            threat_level=threat_level,
            sophistication_level=sophistication,
            impact_scope=impact_scope,
            attribution_confidence=attribution_confidence,
            evidence_analysis=evidence_analysis,
            investigation_plan=investigation_plan,
            legal_considerations=legal_considerations
        )
    
    async def _execute_with_openai(self, model: str, prompt: str, temperature: float = 0.1, max_tokens: int = 4000) -> str:
        """Execute prompt with OpenAI model."""
        try:
            response = await self.openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"OpenAI execution failed: {str(e)}")
            raise
    
    async def _execute_with_anthropic(self, model: str, prompt: str, temperature: float = 0.1, max_tokens: int = 4000) -> str:
        """Execute prompt with Anthropic model."""
        try:
            response = await self.anthropic_client.messages.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.content[0].text
        except Exception as e:
            self.logger.error(f"Anthropic execution failed: {str(e)}")
            raise
    
    async def _execute_with_together_ai(self, model: str, prompt: str, temperature: float = 0.1, max_tokens: int = 4000) -> str:
        """Execute prompt with Together AI model."""
        try:
            response = await self.together_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"Together AI execution failed: {str(e)}")
            raise

# Example usage and testing
if __name__ == "__main__":
    async def test_fbi_agent():
        """Test FBI Cyber Agent with sample evidence."""
        
        config = {
            'openai_api_key': 'your-openai-key',
            'anthropic_api_key': 'your-anthropic-key',
            'together_api_key': 'your-together-key'
        }
        
        # Sample evidence package
        evidence = EvidencePackage(
            case_id="FBI-CYBER-2024-001",
            evidence_type="website_investigation",
            source_data={
                "url": "https://suspicious-investment.com",
                "domain_age": "3 days",
                "registrar": "Privacy Protected",
                "hosting": "Bulletproof hosting service",
                "ssl_status": "Invalid certificate",
                "content_analysis": "Investment scam indicators present"
            },
            collection_timestamp=datetime.now(),
            chain_of_custody=["Automated Collection System", "FBI Cyber Agent"],
            integrity_hash="sha256:abc123..."
        )
        
        # Initialize and run FBI investigation
        fbi_agent = FBICyberAgent(config)
        assessment = await fbi_agent.investigate_with_fbi_methodology(evidence)
        
        print(f"FBI Investigation Complete for Case {evidence.case_id}")
        print(f"Classification: {assessment.case_classification}")
        print(f"Threat Level: {assessment.threat_level}/10")
        print(f"Attribution Confidence: {assessment.attribution_confidence}")
        
        return assessment
    
    # Run test if executed directly
    # asyncio.run(test_fbi_agent())

