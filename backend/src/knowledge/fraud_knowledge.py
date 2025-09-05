"""
ScamShield AI - Fraud Knowledge Management System

This module implements the knowledge management system for ScamShield investigations
including fraud patterns, threat intelligence, and investigation methodologies.
"""

from crewai.knowledge import Knowledge
from typing import Dict, List, Any, Optional
import json
import os
import logging
from datetime import datetime
import yaml

# Configure logging
logger = logging.getLogger(__name__)

class ScamShieldFraudKnowledge:
    """
    Comprehensive knowledge management system for fraud investigation
    with pattern recognition, threat intelligence, and methodology storage.
    """
    
    def __init__(self, knowledge_directory: str = "./knowledge"):
        """
        Initialize the fraud knowledge system
        
        Args:
            knowledge_directory: Directory containing knowledge sources
        """
        self.knowledge_directory = knowledge_directory
        
        # Ensure knowledge directories exist
        self._create_knowledge_directories()
        
        # Initialize knowledge sources
        self.knowledge_sources = [
            f"{knowledge_directory}/fraud_patterns.json",
            f"{knowledge_directory}/threat_intelligence/",
            f"{knowledge_directory}/investigation_methodologies/",
            f"{knowledge_directory}/regulatory_compliance/",
            f"{knowledge_directory}/case_studies/"
        ]
        
        # Initialize CrewAI Knowledge system
        self.knowledge_system = Knowledge(
            sources=self.knowledge_sources
        )
        
        # Load fraud patterns
        self.fraud_patterns = self._load_fraud_patterns()
        
        # Load investigation methodologies
        self.methodologies = self._load_methodologies()
        
        # Load threat intelligence
        self.threat_intelligence = self._load_threat_intelligence()
        
        logger.info("ScamShield Fraud Knowledge system initialized")
    
    def _create_knowledge_directories(self):
        """Create necessary knowledge directories"""
        directories = [
            self.knowledge_directory,
            f"{self.knowledge_directory}/threat_intelligence",
            f"{self.knowledge_directory}/investigation_methodologies",
            f"{self.knowledge_directory}/regulatory_compliance",
            f"{self.knowledge_directory}/case_studies",
            f"{self.knowledge_directory}/patterns"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def _load_fraud_patterns(self) -> Dict[str, Any]:
        """Load fraud patterns from knowledge base"""
        patterns_file = f"{self.knowledge_directory}/fraud_patterns.json"
        
        try:
            if os.path.exists(patterns_file):
                with open(patterns_file, 'r') as f:
                    patterns = json.load(f)
                logger.info(f"Loaded {len(patterns)} fraud patterns")
                return patterns
            else:
                # Create default fraud patterns
                default_patterns = self._create_default_fraud_patterns()
                self._save_fraud_patterns(default_patterns)
                return default_patterns
                
        except Exception as e:
            logger.error(f"Failed to load fraud patterns: {str(e)}")
            return {}
    
    def _create_default_fraud_patterns(self) -> Dict[str, Any]:
        """Create default fraud patterns for initial knowledge base"""
        return {
            "domain_patterns": {
                "suspicious_tlds": [
                    ".tk", ".ml", ".ga", ".cf", ".top", ".click", ".download",
                    ".stream", ".science", ".racing", ".review", ".faith"
                ],
                "suspicious_keywords": [
                    "bank", "paypal", "amazon", "microsoft", "apple", "google",
                    "secure", "verify", "update", "suspended", "urgent", "limited"
                ],
                "registration_anomalies": [
                    "recent_registration",
                    "privacy_protection",
                    "bulk_registration",
                    "suspicious_registrar"
                ],
                "dns_indicators": [
                    "fast_flux",
                    "domain_generation_algorithm",
                    "suspicious_nameservers",
                    "short_ttl"
                ]
            },
            "email_patterns": {
                "spoofing_indicators": [
                    "display_name_spoofing",
                    "domain_spoofing",
                    "homograph_attack",
                    "subdomain_spoofing"
                ],
                "phishing_keywords": [
                    "verify", "confirm", "update", "suspended", "expired",
                    "click here", "urgent", "immediate action", "limited time"
                ],
                "header_anomalies": [
                    "missing_spf",
                    "dkim_failure",
                    "dmarc_failure",
                    "suspicious_routing"
                ]
            },
            "financial_patterns": {
                "money_laundering_indicators": [
                    "rapid_movement",
                    "structuring",
                    "shell_companies",
                    "high_risk_jurisdictions"
                ],
                "sanctions_evasion": [
                    "name_variations",
                    "beneficial_ownership_obscuring",
                    "front_companies",
                    "cryptocurrency_mixing"
                ],
                "fraud_schemes": [
                    "advance_fee_fraud",
                    "investment_fraud",
                    "romance_scam",
                    "business_email_compromise"
                ]
            },
            "cryptocurrency_patterns": {
                "mixing_services": [
                    "tornado_cash",
                    "bitcoin_mixer",
                    "privacy_coins",
                    "tumbling_services"
                ],
                "illicit_indicators": [
                    "darknet_markets",
                    "ransomware_payments",
                    "exchange_hacks",
                    "sanctions_evasion"
                ],
                "risk_factors": [
                    "high_volume_transactions",
                    "rapid_conversion",
                    "multiple_exchanges",
                    "privacy_focused_wallets"
                ]
            }
        }
    
    def _save_fraud_patterns(self, patterns: Dict[str, Any]):
        """Save fraud patterns to knowledge base"""
        patterns_file = f"{self.knowledge_directory}/fraud_patterns.json"
        
        try:
            with open(patterns_file, 'w') as f:
                json.dump(patterns, f, indent=2)
            logger.info("Fraud patterns saved to knowledge base")
            
        except Exception as e:
            logger.error(f"Failed to save fraud patterns: {str(e)}")
    
    def _load_methodologies(self) -> Dict[str, Any]:
        """Load investigation methodologies"""
        methodologies_dir = f"{self.knowledge_directory}/investigation_methodologies"
        methodologies = {}
        
        try:
            # Load FBI methodologies
            fbi_file = f"{methodologies_dir}/fbi_cyber_methods.yaml"
            if not os.path.exists(fbi_file):
                self._create_fbi_methodologies(fbi_file)
            
            with open(fbi_file, 'r') as f:
                methodologies['fbi_cyber'] = yaml.safe_load(f)
            
            # Load CIA methodologies
            cia_file = f"{methodologies_dir}/cia_intelligence_methods.yaml"
            if not os.path.exists(cia_file):
                self._create_cia_methodologies(cia_file)
            
            with open(cia_file, 'r') as f:
                methodologies['cia_intelligence'] = yaml.safe_load(f)
            
            # Load MI6 methodologies
            mi6_file = f"{methodologies_dir}/mi6_signals_methods.yaml"
            if not os.path.exists(mi6_file):
                self._create_mi6_methodologies(mi6_file)
            
            with open(mi6_file, 'r') as f:
                methodologies['mi6_signals'] = yaml.safe_load(f)
            
            # Load Mossad methodologies
            mossad_file = f"{methodologies_dir}/mossad_counterintel_methods.yaml"
            if not os.path.exists(mossad_file):
                self._create_mossad_methodologies(mossad_file)
            
            with open(mossad_file, 'r') as f:
                methodologies['mossad_counterintel'] = yaml.safe_load(f)
            
            logger.info("Investigation methodologies loaded")
            return methodologies
            
        except Exception as e:
            logger.error(f"Failed to load methodologies: {str(e)}")
            return {}
    
    def _create_fbi_methodologies(self, file_path: str):
        """Create FBI cyber investigation methodologies"""
        fbi_methods = {
            "digital_forensics": {
                "evidence_collection": [
                    "disk_imaging",
                    "memory_acquisition",
                    "network_traffic_capture",
                    "mobile_device_extraction"
                ],
                "analysis_techniques": [
                    "file_system_analysis",
                    "registry_analysis",
                    "log_file_examination",
                    "malware_analysis"
                ],
                "attribution_methods": [
                    "behavioral_analysis",
                    "code_similarity",
                    "infrastructure_mapping",
                    "opsec_failures"
                ]
            },
            "network_investigation": {
                "reconnaissance": [
                    "passive_dns_analysis",
                    "whois_investigation",
                    "certificate_transparency",
                    "infrastructure_mapping"
                ],
                "active_investigation": [
                    "port_scanning",
                    "service_enumeration",
                    "vulnerability_assessment",
                    "honeypot_deployment"
                ]
            }
        }
        
        with open(file_path, 'w') as f:
            yaml.dump(fbi_methods, f, default_flow_style=False)
    
    def _create_cia_methodologies(self, file_path: str):
        """Create CIA intelligence methodologies"""
        cia_methods = {
            "intelligence_analysis": {
                "collection_methods": [
                    "humint_sources",
                    "sigint_intercepts",
                    "osint_gathering",
                    "financial_intelligence"
                ],
                "analysis_frameworks": [
                    "structured_analytic_techniques",
                    "competing_hypotheses",
                    "devil_advocacy",
                    "red_team_analysis"
                ],
                "assessment_criteria": [
                    "source_reliability",
                    "information_credibility",
                    "confidence_levels",
                    "uncertainty_factors"
                ]
            },
            "strategic_assessment": {
                "threat_modeling": [
                    "actor_profiling",
                    "capability_assessment",
                    "intent_analysis",
                    "opportunity_evaluation"
                ],
                "geopolitical_context": [
                    "regional_dynamics",
                    "economic_factors",
                    "political_stability",
                    "alliance_structures"
                ]
            }
        }
        
        with open(file_path, 'w') as f:
            yaml.dump(cia_methods, f, default_flow_style=False)
    
    def _create_mi6_methodologies(self, file_path: str):
        """Create MI6 signals intelligence methodologies"""
        mi6_methods = {
            "signals_intelligence": {
                "collection_techniques": [
                    "communication_intercepts",
                    "metadata_analysis",
                    "traffic_analysis",
                    "pattern_recognition"
                ],
                "analysis_methods": [
                    "linguistic_analysis",
                    "cryptographic_analysis",
                    "network_analysis",
                    "behavioral_patterns"
                ],
                "gchq_methods": [
                    "bulk_collection",
                    "targeted_intercepts",
                    "computer_network_exploitation",
                    "cryptanalysis"
                ]
            },
            "strategic_intelligence": {
                "assessment_frameworks": [
                    "threat_landscape_analysis",
                    "capability_development",
                    "strategic_warning",
                    "policy_support"
                ]
            }
        }
        
        with open(file_path, 'w') as f:
            yaml.dump(mi6_methods, f, default_flow_style=False)
    
    def _create_mossad_methodologies(self, file_path: str):
        """Create Mossad counterintelligence methodologies"""
        mossad_methods = {
            "counterintelligence": {
                "threat_identification": [
                    "adversary_profiling",
                    "operational_security",
                    "penetration_testing",
                    "insider_threat_detection"
                ],
                "analysis_techniques": [
                    "behavioral_analysis",
                    "pattern_recognition",
                    "anomaly_detection",
                    "risk_assessment"
                ],
                "attribution_methods": [
                    "tactical_fingerprinting",
                    "operational_patterns",
                    "resource_analysis",
                    "capability_assessment"
                ]
            },
            "strategic_counterintelligence": {
                "threat_assessment": [
                    "state_actor_analysis",
                    "non_state_threats",
                    "hybrid_warfare",
                    "asymmetric_threats"
                ]
            }
        }
        
        with open(file_path, 'w') as f:
            yaml.dump(mossad_methods, f, default_flow_style=False)
    
    def _load_threat_intelligence(self) -> Dict[str, Any]:
        """Load threat intelligence data"""
        threat_intel_dir = f"{self.knowledge_directory}/threat_intelligence"
        threat_intel = {}
        
        try:
            # Load threat actor profiles
            actors_file = f"{threat_intel_dir}/threat_actors.json"
            if not os.path.exists(actors_file):
                self._create_threat_actors(actors_file)
            
            with open(actors_file, 'r') as f:
                threat_intel['actors'] = json.load(f)
            
            # Load TTPs (Tactics, Techniques, Procedures)
            ttps_file = f"{threat_intel_dir}/ttps.json"
            if not os.path.exists(ttps_file):
                self._create_ttps(ttps_file)
            
            with open(ttps_file, 'r') as f:
                threat_intel['ttps'] = json.load(f)
            
            logger.info("Threat intelligence loaded")
            return threat_intel
            
        except Exception as e:
            logger.error(f"Failed to load threat intelligence: {str(e)}")
            return {}
    
    def _create_threat_actors(self, file_path: str):
        """Create threat actor profiles"""
        threat_actors = {
            "apt_groups": {
                "apt1": {
                    "name": "Comment Crew",
                    "origin": "China",
                    "targets": ["intellectual_property", "government", "military"],
                    "techniques": ["spear_phishing", "custom_malware", "lateral_movement"]
                },
                "apt28": {
                    "name": "Fancy Bear",
                    "origin": "Russia",
                    "targets": ["government", "military", "political"],
                    "techniques": ["spear_phishing", "zero_day_exploits", "credential_harvesting"]
                }
            },
            "cybercriminal_groups": {
                "lazarus": {
                    "name": "Lazarus Group",
                    "origin": "North Korea",
                    "targets": ["financial", "cryptocurrency", "entertainment"],
                    "techniques": ["banking_trojans", "ransomware", "supply_chain_attacks"]
                }
            },
            "fraud_networks": {
                "romance_scammers": {
                    "origin": "West Africa",
                    "targets": ["individuals", "dating_platforms"],
                    "techniques": ["social_engineering", "identity_theft", "money_mules"]
                }
            }
        }
        
        with open(file_path, 'w') as f:
            json.dump(threat_actors, f, indent=2)
    
    def _create_ttps(self, file_path: str):
        """Create TTPs (Tactics, Techniques, Procedures) database"""
        ttps = {
            "initial_access": {
                "spear_phishing": {
                    "description": "Targeted phishing emails to specific individuals",
                    "indicators": ["suspicious_attachments", "spoofed_domains", "social_engineering"],
                    "mitigations": ["email_filtering", "user_training", "attachment_sandboxing"]
                },
                "supply_chain_compromise": {
                    "description": "Compromise of software supply chain",
                    "indicators": ["unauthorized_code", "suspicious_updates", "certificate_anomalies"],
                    "mitigations": ["code_signing", "update_verification", "vendor_assessment"]
                }
            },
            "persistence": {
                "registry_modification": {
                    "description": "Modification of Windows registry for persistence",
                    "indicators": ["registry_changes", "startup_modifications", "service_creation"],
                    "mitigations": ["registry_monitoring", "application_whitelisting", "privilege_restriction"]
                }
            },
            "command_and_control": {
                "domain_generation_algorithm": {
                    "description": "Algorithmic generation of C2 domains",
                    "indicators": ["dga_domains", "periodic_dns_queries", "suspicious_traffic_patterns"],
                    "mitigations": ["dns_monitoring", "dga_detection", "network_segmentation"]
                }
            }
        }
        
        with open(file_path, 'w') as f:
            json.dump(ttps, f, indent=2)
    
    def get_fraud_patterns(self, pattern_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Get fraud patterns by type
        
        Args:
            pattern_type: Specific pattern type to retrieve
            
        Returns:
            Fraud patterns matching the criteria
        """
        if pattern_type and pattern_type in self.fraud_patterns:
            return {pattern_type: self.fraud_patterns[pattern_type]}
        return self.fraud_patterns
    
    def get_investigation_methodology(self, agent_type: str) -> Dict[str, Any]:
        """
        Get investigation methodology for specific agent type
        
        Args:
            agent_type: Type of agent (fbi_cyber, cia_intelligence, etc.)
            
        Returns:
            Investigation methodology for the agent
        """
        return self.methodologies.get(agent_type, {})
    
    def get_threat_intelligence(self, threat_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Get threat intelligence data
        
        Args:
            threat_type: Specific threat type to retrieve
            
        Returns:
            Threat intelligence matching the criteria
        """
        if threat_type and threat_type in self.threat_intelligence:
            return {threat_type: self.threat_intelligence[threat_type]}
        return self.threat_intelligence
    
    def add_fraud_pattern(self, 
                         pattern_type: str,
                         pattern_name: str,
                         pattern_data: Dict[str, Any]) -> bool:
        """
        Add new fraud pattern to knowledge base
        
        Args:
            pattern_type: Type of fraud pattern
            pattern_name: Name of the pattern
            pattern_data: Pattern data and indicators
            
        Returns:
            Success status of the operation
        """
        try:
            if pattern_type not in self.fraud_patterns:
                self.fraud_patterns[pattern_type] = {}
            
            self.fraud_patterns[pattern_type][pattern_name] = {
                "data": pattern_data,
                "created": datetime.utcnow().isoformat(),
                "usage_count": 0
            }
            
            # Save updated patterns
            self._save_fraud_patterns(self.fraud_patterns)
            
            logger.info(f"Added fraud pattern: {pattern_type}/{pattern_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add fraud pattern: {str(e)}")
            return False
    
    def update_pattern_usage(self, pattern_type: str, pattern_name: str) -> bool:
        """
        Update usage count for a fraud pattern
        
        Args:
            pattern_type: Type of fraud pattern
            pattern_name: Name of the pattern
            
        Returns:
            Success status of the operation
        """
        try:
            if (pattern_type in self.fraud_patterns and 
                pattern_name in self.fraud_patterns[pattern_type]):
                
                current_count = self.fraud_patterns[pattern_type][pattern_name].get("usage_count", 0)
                self.fraud_patterns[pattern_type][pattern_name]["usage_count"] = current_count + 1
                
                # Save updated patterns
                self._save_fraud_patterns(self.fraud_patterns)
                
                logger.info(f"Updated usage count for pattern: {pattern_type}/{pattern_name}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to update pattern usage: {str(e)}")
            return False
    
    def search_knowledge(self, query: str, knowledge_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search knowledge base for relevant information
        
        Args:
            query: Search query
            knowledge_type: Specific type of knowledge to search
            
        Returns:
            List of relevant knowledge items
        """
        try:
            results = []
            
            # Search fraud patterns
            if not knowledge_type or knowledge_type == "patterns":
                for pattern_type, patterns in self.fraud_patterns.items():
                    for pattern_name, pattern_data in patterns.items():
                        if query.lower() in pattern_name.lower() or query.lower() in str(pattern_data).lower():
                            results.append({
                                "type": "fraud_pattern",
                                "category": pattern_type,
                                "name": pattern_name,
                                "data": pattern_data
                            })
            
            # Search methodologies
            if not knowledge_type or knowledge_type == "methodologies":
                for agent_type, methods in self.methodologies.items():
                    if query.lower() in str(methods).lower():
                        results.append({
                            "type": "methodology",
                            "agent_type": agent_type,
                            "data": methods
                        })
            
            # Search threat intelligence
            if not knowledge_type or knowledge_type == "threat_intel":
                for intel_type, intel_data in self.threat_intelligence.items():
                    if query.lower() in str(intel_data).lower():
                        results.append({
                            "type": "threat_intelligence",
                            "category": intel_type,
                            "data": intel_data
                        })
            
            logger.info(f"Found {len(results)} knowledge items for query: {query}")
            return results
            
        except Exception as e:
            logger.error(f"Failed to search knowledge: {str(e)}")
            return []

# Factory function for easy knowledge system creation
def create_fraud_knowledge(knowledge_directory: str = "./knowledge") -> ScamShieldFraudKnowledge:
    """
    Factory function to create fraud knowledge system
    
    Args:
        knowledge_directory: Directory for knowledge sources
        
    Returns:
        Configured fraud knowledge system
    """
    return ScamShieldFraudKnowledge(knowledge_directory)

# Global knowledge instance (singleton pattern)
_global_knowledge_instance = None

def get_global_knowledge() -> ScamShieldFraudKnowledge:
    """
    Get global knowledge instance (singleton)
    
    Returns:
        Global fraud knowledge system
    """
    global _global_knowledge_instance
    if _global_knowledge_instance is None:
        _global_knowledge_instance = create_fraud_knowledge()
    return _global_knowledge_instance

