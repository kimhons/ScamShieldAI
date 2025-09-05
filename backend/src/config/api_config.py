"""
Centralized API Configuration for ScamShield AI
Manages all API keys and endpoints with placeholder support
"""

import os
from typing import Dict, Optional

class APIConfig:
    """
    Centralized API configuration management
    """
    
    def __init__(self):
        # API Keys - Can be set via environment variables or updated later
        self.api_keys = {
            # Core Intelligence APIs
            "rapidapi": os.getenv("RAPIDAPI_KEY", "c566ad06fcmsh7498d2bd141cec0p1e63e2jsnabd7069fe4aa"),
            "shodan": os.getenv("SHODAN_KEY", "KyNvhxEDtk2XUjHOFSrIyvbu28bB4vt3"),
            "whoisxml": os.getenv("WHOISXML_KEY", "at_Nr3kOpLxqAYPudfWbqY3wZfCQJyIL"),
            "opensanctions": os.getenv("OPENSANCTIONS_KEY", "579928de8a52db1706c5235975ba23b9"),
            "alpha_vantage": os.getenv("ALPHA_VANTAGE_KEY", "14X3TK5E9HJIO3SD"),
            "cloudflare": os.getenv("CLOUDFLARE_TOKEN", "jt5q1YjcVGJ2NRSn-5qAmMikuCXDS5ZFm-6hBl3G"),
            "ipinfo": os.getenv("IPINFO_TOKEN", "73a9372cc469a8"),
            "maxmind_account": os.getenv("MAXMIND_ACCOUNT", "1195683"),
            "maxmind_license": os.getenv("MAXMIND_LICENSE", "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"),
            "companies_house": os.getenv("COMPANIES_HOUSE_KEY", "9e899963-34fb-4c3e-8377-cc881667d5b4"),
            
            # Future API Keys (Placeholders)
            "virustotal": os.getenv("VIRUSTOTAL_KEY", "PLACEHOLDER_VIRUSTOTAL_KEY"),
            "hunter_io": os.getenv("HUNTER_IO_KEY", "PLACEHOLDER_HUNTER_IO_KEY"),
            "twitter": os.getenv("TWITTER_BEARER_TOKEN", "PLACEHOLDER_TWITTER_TOKEN"),
            "censys_id": os.getenv("CENSYS_ID", "PLACEHOLDER_CENSYS_ID"),
            "censys_secret": os.getenv("CENSYS_SECRET", "PLACEHOLDER_CENSYS_SECRET"),
        }
        
        # API Endpoints
        self.endpoints = {
            "rapidapi": "https://rapidapi.com/hub",
            "shodan": "https://api.shodan.io",
            "whoisxml": "https://www.whoisxmlapi.com/whoisserver/WhoisService",
            "opensanctions": "https://api.opensanctions.org",
            "alpha_vantage": "https://www.alphavantage.co/query",
            "cloudflare": "https://api.cloudflare.com/client/v4",
            "ipinfo": "https://api.ipinfo.io",
            "maxmind": "https://geolite.info/geoip/v2.1",
            "companies_house": "https://api.company-information.service.gov.uk",
            "virustotal": "https://www.virustotal.com/vtapi/v2",
            "hunter_io": "https://api.hunter.io/v2",
            "twitter": "https://api.twitter.com/2",
            "censys": "https://search.censys.io/api/v2",
        }
        
        # Demo mode flag
        self.demo_mode = os.getenv("DEMO_MODE", "true").lower() == "true"
        
    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a service"""
        return self.api_keys.get(service)
    
    def set_api_key(self, service: str, key: str) -> None:
        """Set API key for a service"""
        self.api_keys[service] = key
        
    def get_endpoint(self, service: str) -> Optional[str]:
        """Get endpoint URL for a service"""
        return self.endpoints.get(service)
    
    def is_api_configured(self, service: str) -> bool:
        """Check if API is properly configured"""
        key = self.get_api_key(service)
        return key is not None and not key.startswith("PLACEHOLDER_")
    
    def get_configured_apis(self) -> Dict[str, bool]:
        """Get status of all APIs"""
        return {
            service: self.is_api_configured(service)
            for service in self.api_keys.keys()
        }
    
    def enable_demo_mode(self) -> None:
        """Enable demo mode with mock data"""
        self.demo_mode = True
        
    def disable_demo_mode(self) -> None:
        """Disable demo mode to use real APIs"""
        self.demo_mode = False
    
    def is_demo_mode(self) -> bool:
        """Check if demo mode is enabled"""
        return self.demo_mode

# Global configuration instance
api_config = APIConfig()

