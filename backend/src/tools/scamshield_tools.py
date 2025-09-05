"""
ScamShield AI - CrewAI Tool Integrations

This module provides CrewAI-compatible tools that integrate with ScamShield's
existing API services for comprehensive fraud investigation capabilities.
"""

from crewai.tools import BaseTool
from typing import Type, Optional, Dict, Any
from pydantic import BaseModel, Field
import json
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Tool Input Models
class DomainLookupInput(BaseModel):
    domain: str = Field(description="Domain name to analyze (e.g., example.com)")

class IPScanInput(BaseModel):
    ip_address: str = Field(description="IP address to scan (e.g., 192.168.1.1)")

class EmailAnalysisInput(BaseModel):
    email: str = Field(description="Email address to investigate")

class SanctionsCheckInput(BaseModel):
    entity: str = Field(description="Entity name or identifier to screen")

class CryptoAnalysisInput(BaseModel):
    address: str = Field(description="Cryptocurrency address to analyze")

class SSLAnalysisInput(BaseModel):
    domain: str = Field(description="Domain for SSL certificate analysis")

# WhoisXML API Tool
class WhoisDomainLookupTool(BaseTool):
    name: str = "whois_domain_lookup"
    description: str = """
    Perform comprehensive WHOIS lookup on domain names to gather registration
    information, contact details, and administrative data for fraud investigation.
    """
    args_schema: Type[BaseModel] = DomainLookupInput
    
    def _run(self, domain: str) -> str:
        """Execute WHOIS lookup using WhoisXML API integration"""
        try:
            # Import ScamShield WhoisXML integration
            from ..api_integration.whoisxml_integration import WhoisXMLIntegration
            
            whois_client = WhoisXMLIntegration()
            result = whois_client.lookup_domain(domain)
            
            # Format result for CrewAI consumption
            formatted_result = {
                "domain": domain,
                "whois_data": result,
                "analysis_timestamp": whois_client.get_timestamp(),
                "data_source": "WhoisXML API"
            }
            
            logger.info(f"WHOIS lookup completed for domain: {domain}")
            return json.dumps(formatted_result, indent=2)
            
        except Exception as e:
            logger.error(f"WHOIS lookup failed for {domain}: {str(e)}")
            return json.dumps({
                "error": f"WHOIS lookup failed: {str(e)}",
                "domain": domain,
                "status": "failed"
            })

# Shodan API Tool
class ShodanNetworkScanTool(BaseTool):
    name: str = "shodan_network_scan"
    description: str = """
    Scan IP addresses using Shodan to gather network intelligence, open ports,
    services, and infrastructure information for cyber investigation.
    """
    args_schema: Type[BaseModel] = IPScanInput
    
    def _run(self, ip_address: str) -> str:
        """Execute Shodan scan using ScamShield integration"""
        try:
            from ..api_integration.shodan_integration import ShodanIntegration
            
            shodan_client = ShodanIntegration()
            result = shodan_client.scan_ip(ip_address)
            
            formatted_result = {
                "ip_address": ip_address,
                "scan_results": result,
                "analysis_timestamp": shodan_client.get_timestamp(),
                "data_source": "Shodan API"
            }
            
            logger.info(f"Shodan scan completed for IP: {ip_address}")
            return json.dumps(formatted_result, indent=2)
            
        except Exception as e:
            logger.error(f"Shodan scan failed for {ip_address}: {str(e)}")
            return json.dumps({
                "error": f"Shodan scan failed: {str(e)}",
                "ip_address": ip_address,
                "status": "failed"
            })

# OpenSanctions API Tool
class SanctionsScreeningTool(BaseTool):
    name: str = "sanctions_screening"
    description: str = """
    Screen entities against international sanctions lists including OFAC, EU,
    UK, and other regulatory databases for compliance investigation.
    """
    args_schema: Type[BaseModel] = SanctionsCheckInput
    
    def _run(self, entity: str) -> str:
        """Execute sanctions screening using OpenSanctions integration"""
        try:
            from ..api_integration.opensanctions_integration import OpenSanctionsIntegration
            
            sanctions_client = OpenSanctionsIntegration()
            result = sanctions_client.screen_entity(entity)
            
            formatted_result = {
                "entity": entity,
                "sanctions_results": result,
                "analysis_timestamp": sanctions_client.get_timestamp(),
                "data_source": "OpenSanctions API"
            }
            
            logger.info(f"Sanctions screening completed for entity: {entity}")
            return json.dumps(formatted_result, indent=2)
            
        except Exception as e:
            logger.error(f"Sanctions screening failed for {entity}: {str(e)}")
            return json.dumps({
                "error": f"Sanctions screening failed: {str(e)}",
                "entity": entity,
                "status": "failed"
            })

# IPinfo API Tool
class IPGeolocationTool(BaseTool):
    name: str = "ip_geolocation"
    description: str = """
    Get detailed geolocation and network information for IP addresses
    including country, region, ISP, and threat intelligence data.
    """
    args_schema: Type[BaseModel] = IPScanInput
    
    def _run(self, ip_address: str) -> str:
        """Execute IP geolocation using IPinfo integration"""
        try:
            from ..api_integration.ipinfo_integration import IPinfoIntegration
            
            ipinfo_client = IPinfoIntegration()
            result = ipinfo_client.lookup_ip(ip_address)
            
            formatted_result = {
                "ip_address": ip_address,
                "geolocation_data": result,
                "analysis_timestamp": ipinfo_client.get_timestamp(),
                "data_source": "IPinfo API"
            }
            
            logger.info(f"IP geolocation completed for: {ip_address}")
            return json.dumps(formatted_result, indent=2)
            
        except Exception as e:
            logger.error(f"IP geolocation failed for {ip_address}: {str(e)}")
            return json.dumps({
                "error": f"IP geolocation failed: {str(e)}",
                "ip_address": ip_address,
                "status": "failed"
            })

# Cloudflare API Tool
class DNSAnalysisTool(BaseTool):
    name: str = "dns_analysis"
    description: str = """
    Perform comprehensive DNS analysis including record examination,
    security assessment, and infrastructure mapping for domain investigation.
    """
    args_schema: Type[BaseModel] = DomainLookupInput
    
    def _run(self, domain: str) -> str:
        """Execute DNS analysis using Cloudflare integration"""
        try:
            from ..api_integration.cloudflare_integration import CloudflareIntegration
            
            cloudflare_client = CloudflareIntegration()
            result = cloudflare_client.analyze_domain(domain)
            
            formatted_result = {
                "domain": domain,
                "dns_analysis": result,
                "analysis_timestamp": cloudflare_client.get_timestamp(),
                "data_source": "Cloudflare API"
            }
            
            logger.info(f"DNS analysis completed for domain: {domain}")
            return json.dumps(formatted_result, indent=2)
            
        except Exception as e:
            logger.error(f"DNS analysis failed for {domain}: {str(e)}")
            return json.dumps({
                "error": f"DNS analysis failed: {str(e)}",
                "domain": domain,
                "status": "failed"
            })

# SSL Certificate Analysis Tool
class SSLCertificateAnalysisTool(BaseTool):
    name: str = "ssl_certificate_analysis"
    description: str = """
    Analyze SSL certificates for domains including validity, trust chain,
    security configuration, and certificate authority information.
    """
    args_schema: Type[BaseModel] = SSLAnalysisInput
    
    def _run(self, domain: str) -> str:
        """Execute SSL certificate analysis"""
        try:
            # This would integrate with SSL analysis service
            # For now, implementing basic SSL check
            import ssl
            import socket
            from datetime import datetime
            
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
            
            formatted_result = {
                "domain": domain,
                "ssl_certificate": {
                    "subject": dict(x[0] for x in cert['subject']),
                    "issuer": dict(x[0] for x in cert['issuer']),
                    "version": cert['version'],
                    "serial_number": cert['serialNumber'],
                    "not_before": cert['notBefore'],
                    "not_after": cert['notAfter'],
                    "signature_algorithm": cert.get('signatureAlgorithm', 'Unknown')
                },
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "data_source": "SSL Certificate Analysis"
            }
            
            logger.info(f"SSL analysis completed for domain: {domain}")
            return json.dumps(formatted_result, indent=2)
            
        except Exception as e:
            logger.error(f"SSL analysis failed for {domain}: {str(e)}")
            return json.dumps({
                "error": f"SSL analysis failed: {str(e)}",
                "domain": domain,
                "status": "failed"
            })

# Alpha Vantage Financial Tool
class FinancialIntelligenceTool(BaseTool):
    name: str = "financial_intelligence"
    description: str = """
    Gather financial intelligence including market data, company information,
    and financial indicators for comprehensive financial investigation.
    """
    args_schema: Type[BaseModel] = SanctionsCheckInput
    
    def _run(self, entity: str) -> str:
        """Execute financial intelligence gathering"""
        try:
            from ..api_integration.alphavantage_integration import AlphaVantageIntegration
            
            av_client = AlphaVantageIntegration()
            result = av_client.get_company_overview(entity)
            
            formatted_result = {
                "entity": entity,
                "financial_data": result,
                "analysis_timestamp": av_client.get_timestamp(),
                "data_source": "Alpha Vantage API"
            }
            
            logger.info(f"Financial intelligence completed for entity: {entity}")
            return json.dumps(formatted_result, indent=2)
            
        except Exception as e:
            logger.error(f"Financial intelligence failed for {entity}: {str(e)}")
            return json.dumps({
                "error": f"Financial intelligence failed: {str(e)}",
                "entity": entity,
                "status": "failed"
            })

# Cryptocurrency Analysis Tool (Placeholder for future integration)
class BlockchainAnalysisTool(BaseTool):
    name: str = "blockchain_analysis"
    description: str = """
    Analyze cryptocurrency addresses and transactions for risk assessment,
    compliance screening, and illicit activity detection.
    """
    args_schema: Type[BaseModel] = CryptoAnalysisInput
    
    def _run(self, address: str) -> str:
        """Execute blockchain analysis (placeholder implementation)"""
        try:
            # This would integrate with cryptocurrency analysis APIs
            # For now, implementing basic structure
            formatted_result = {
                "address": address,
                "blockchain_analysis": {
                    "address_type": "Unknown",
                    "risk_score": 0,
                    "transaction_count": 0,
                    "total_received": 0,
                    "total_sent": 0,
                    "first_seen": None,
                    "last_seen": None
                },
                "analysis_timestamp": "2024-01-01T00:00:00Z",
                "data_source": "Blockchain Analysis (Placeholder)"
            }
            
            logger.info(f"Blockchain analysis completed for address: {address}")
            return json.dumps(formatted_result, indent=2)
            
        except Exception as e:
            logger.error(f"Blockchain analysis failed for {address}: {str(e)}")
            return json.dumps({
                "error": f"Blockchain analysis failed: {str(e)}",
                "address": address,
                "status": "failed"
            })

# Email Analysis Tool (Placeholder)
class EmailHeaderAnalysisTool(BaseTool):
    name: str = "email_header_analysis"
    description: str = """
    Analyze email headers for authenticity, routing information,
    and fraud indicators including SPF, DKIM, and DMARC validation.
    """
    args_schema: Type[BaseModel] = EmailAnalysisInput
    
    def _run(self, email: str) -> str:
        """Execute email header analysis (placeholder implementation)"""
        try:
            # This would integrate with email analysis services
            formatted_result = {
                "email": email,
                "header_analysis": {
                    "domain": email.split('@')[1] if '@' in email else None,
                    "spf_status": "Unknown",
                    "dkim_status": "Unknown",
                    "dmarc_status": "Unknown",
                    "reputation_score": 0,
                    "fraud_indicators": []
                },
                "analysis_timestamp": "2024-01-01T00:00:00Z",
                "data_source": "Email Analysis (Placeholder)"
            }
            
            logger.info(f"Email analysis completed for: {email}")
            return json.dumps(formatted_result, indent=2)
            
        except Exception as e:
            logger.error(f"Email analysis failed for {email}: {str(e)}")
            return json.dumps({
                "error": f"Email analysis failed: {str(e)}",
                "email": email,
                "status": "failed"
            })

# Tool Registry
SCAMSHIELD_TOOLS = {
    "whois_domain_lookup": WhoisDomainLookupTool(),
    "shodan_network_scan": ShodanNetworkScanTool(),
    "sanctions_screening": SanctionsScreeningTool(),
    "ip_geolocation": IPGeolocationTool(),
    "dns_analysis": DNSAnalysisTool(),
    "ssl_certificate_analysis": SSLCertificateAnalysisTool(),
    "financial_intelligence": FinancialIntelligenceTool(),
    "blockchain_analysis": BlockchainAnalysisTool(),
    "email_header_analysis": EmailHeaderAnalysisTool()
}

def get_tool(tool_name: str) -> Optional[BaseTool]:
    """Get a specific tool by name"""
    return SCAMSHIELD_TOOLS.get(tool_name)

def get_all_tools() -> Dict[str, BaseTool]:
    """Get all available tools"""
    return SCAMSHIELD_TOOLS

def get_tools_for_agent(agent_type: str) -> list:
    """Get recommended tools for specific agent types"""
    tool_mappings = {
        "fbi_cyber": [
            "whois_domain_lookup",
            "shodan_network_scan", 
            "dns_analysis",
            "ssl_certificate_analysis"
        ],
        "cia_intelligence": [
            "sanctions_screening",
            "financial_intelligence",
            "ip_geolocation"
        ],
        "mi6_signals": [
            "dns_analysis",
            "ip_geolocation",
            "ssl_certificate_analysis"
        ],
        "mossad_counterintel": [
            "sanctions_screening",
            "financial_intelligence",
            "blockchain_analysis"
        ],
        "crypto_specialist": [
            "blockchain_analysis",
            "sanctions_screening"
        ],
        "email_specialist": [
            "email_header_analysis",
            "dns_analysis"
        ]
    }
    
    tool_names = tool_mappings.get(agent_type, [])
    return [SCAMSHIELD_TOOLS[name] for name in tool_names if name in SCAMSHIELD_TOOLS]

