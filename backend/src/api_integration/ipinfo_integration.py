"""
IPinfo API Integration for ScamShield AI
Provides access to IP geolocation, ASN, and network intelligence data
"""

import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json

class IPinfoIntegration:
    """
    IPinfo API integration for IP intelligence and geolocation
    """
    
    def __init__(self, api_token: str = "73a9372cc469a8"):
        self.api_token = api_token
        self.base_url = "https://api.ipinfo.io"
        self.session = None
        self.logger = logging.getLogger(__name__)
        
        # Request tracking
        self.requests_made = 0
        self.total_cost = 0.0
        
        # Rate limiting (50,000 requests per month for free tier)
        self.monthly_limit = 50000
        self.requests_this_month = 0
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            headers={
                "Accept": "application/json",
                "User-Agent": "ScamShield-AI/1.0"
            },
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make authenticated request to IPinfo API"""
        try:
            if params is None:
                params = {}
            
            # Add token to parameters
            params["token"] = self.api_token
            
            url = f"{self.base_url}{endpoint}"
            
            async with self.session.get(url, params=params) as response:
                self.requests_made += 1
                self.requests_this_month += 1
                self.total_cost += 0.0  # Free tier
                
                if response.status == 200:
                    data = await response.json()
                    self.logger.info(f"IPinfo API request successful: {endpoint}")
                    return data
                elif response.status == 401:
                    self.logger.error("IPinfo API authentication failed")
                    return {"error": "Authentication failed", "status": 401}
                elif response.status == 403:
                    self.logger.error("IPinfo API access forbidden")
                    return {"error": "Access forbidden", "status": 403}
                elif response.status == 429:
                    self.logger.warning("IPinfo API rate limit exceeded")
                    return {"error": "Rate limit exceeded", "status": 429}
                else:
                    error_text = await response.text()
                    self.logger.error(f"IPinfo API error {response.status}: {error_text}")
                    return {"error": f"API error: {response.status}", "details": error_text}
                    
        except asyncio.TimeoutError:
            self.logger.error("IPinfo API request timeout")
            return {"error": "Request timeout"}
        except Exception as e:
            self.logger.error(f"IPinfo API request failed: {str(e)}")
            return {"error": f"Request failed: {str(e)}"}
    
    async def get_ip_info(self, ip_address: str) -> Dict:
        """
        Get comprehensive IP information
        
        Args:
            ip_address: IP address to lookup
            
        Returns:
            Dict containing IP information and analysis
        """
        try:
            endpoint = f"/{ip_address}"
            result = await self._make_request(endpoint)
            
            if "error" in result:
                return result
            
            # Analyze IP data
            analysis = self._analyze_ip_data(result, ip_address)
            
            return {
                "ip_address": ip_address,
                "ip_data": result,
                "analysis": analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "api_cost": 0.0
            }
            
        except Exception as e:
            self.logger.error(f"IP info lookup failed: {str(e)}")
            return {"error": f"IP lookup failed: {str(e)}"}
    
    async def get_ip_lite(self, ip_address: str) -> Dict:
        """
        Get lite IP information (reduced data set)
        
        Args:
            ip_address: IP address to lookup
            
        Returns:
            Dict containing lite IP information and analysis
        """
        try:
            endpoint = f"/lite/{ip_address}"
            result = await self._make_request(endpoint)
            
            if "error" in result:
                return result
            
            # Analyze lite IP data
            analysis = self._analyze_lite_ip_data(result, ip_address)
            
            return {
                "ip_address": ip_address,
                "lite_data": result,
                "analysis": analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "api_cost": 0.0
            }
            
        except Exception as e:
            self.logger.error(f"IP lite lookup failed: {str(e)}")
            return {"error": f"IP lite lookup failed: {str(e)}"}
    
    async def get_asn_info(self, asn: str) -> Dict:
        """
        Get ASN (Autonomous System Number) information
        
        Args:
            asn: ASN to lookup (e.g., "AS15169")
            
        Returns:
            Dict containing ASN information and analysis
        """
        try:
            endpoint = f"/{asn}"
            result = await self._make_request(endpoint)
            
            if "error" in result:
                return result
            
            # Analyze ASN data
            analysis = self._analyze_asn_data(result, asn)
            
            return {
                "asn": asn,
                "asn_data": result,
                "analysis": analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "api_cost": 0.0
            }
            
        except Exception as e:
            self.logger.error(f"ASN lookup failed: {str(e)}")
            return {"error": f"ASN lookup failed: {str(e)}"}
    
    async def batch_ip_lookup(self, ip_addresses: List[str]) -> Dict:
        """
        Batch lookup multiple IP addresses
        
        Args:
            ip_addresses: List of IP addresses to lookup
            
        Returns:
            Dict containing batch results and analysis
        """
        try:
            results = {}
            
            # Process IPs in batches to respect rate limits
            for ip in ip_addresses[:10]:  # Limit to 10 IPs per batch
                ip_result = await self.get_ip_lite(ip)  # Use lite for batch processing
                results[ip] = ip_result
                
                # Small delay to avoid rate limiting
                await asyncio.sleep(0.1)
            
            # Analyze batch results
            batch_analysis = self._analyze_batch_results(results)
            
            return {
                "ip_addresses": ip_addresses,
                "individual_results": results,
                "batch_analysis": batch_analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "total_api_cost": 0.0
            }
            
        except Exception as e:
            self.logger.error(f"Batch IP lookup failed: {str(e)}")
            return {"error": f"Batch lookup failed: {str(e)}"}
    
    async def comprehensive_ip_investigation(self, ip_address: str) -> Dict:
        """
        Comprehensive IP investigation using multiple IPinfo endpoints
        
        Args:
            ip_address: IP address to investigate
            
        Returns:
            Dict containing comprehensive IP analysis
        """
        try:
            results = {}
            
            # Get full IP information
            results["full_data"] = await self.get_ip_info(ip_address)
            
            # Get lite data for comparison
            results["lite_data"] = await self.get_ip_lite(ip_address)
            
            # If we have ASN information, get ASN details
            full_data = results["full_data"].get("ip_data", {})
            asn = full_data.get("asn")
            if asn:
                results["asn_data"] = await self.get_asn_info(asn)
            
            # Comprehensive analysis
            comprehensive_analysis = self._analyze_comprehensive_ip_results(results, ip_address)
            
            return {
                "ip_address": ip_address,
                "individual_results": results,
                "comprehensive_analysis": comprehensive_analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "total_api_cost": 0.0
            }
            
        except Exception as e:
            self.logger.error(f"Comprehensive IP investigation failed: {str(e)}")
            return {"error": f"IP investigation failed: {str(e)}"}
    
    def _analyze_ip_data(self, ip_data: Dict, ip_address: str) -> Dict:
        """Analyze full IP data for risk indicators"""
        try:
            analysis = {
                "location": {},
                "network_info": {},
                "risk_indicators": [],
                "privacy_indicators": [],
                "hosting_indicators": []
            }
            
            # Extract location information
            analysis["location"] = {
                "ip": ip_data.get("ip", ip_address),
                "city": ip_data.get("city", "Unknown"),
                "region": ip_data.get("region", "Unknown"),
                "country": ip_data.get("country", "Unknown"),
                "country_code": ip_data.get("country_code", ""),
                "postal": ip_data.get("postal", ""),
                "timezone": ip_data.get("timezone", "Unknown"),
                "coordinates": ip_data.get("loc", "Unknown")
            }
            
            # Extract network information
            analysis["network_info"] = {
                "asn": ip_data.get("asn", "Unknown"),
                "as_name": ip_data.get("as_name", "Unknown"),
                "as_domain": ip_data.get("as_domain", "Unknown"),
                "isp": ip_data.get("isp", "Unknown"),
                "org": ip_data.get("org", "Unknown")
            }
            
            # Privacy and security analysis
            privacy = ip_data.get("privacy", {})
            if privacy:
                if privacy.get("vpn", False):
                    analysis["privacy_indicators"].append("VPN detected")
                if privacy.get("proxy", False):
                    analysis["privacy_indicators"].append("Proxy detected")
                if privacy.get("tor", False):
                    analysis["privacy_indicators"].append("Tor exit node detected")
                if privacy.get("relay", False):
                    analysis["privacy_indicators"].append("Relay detected")
                if privacy.get("hosting", False):
                    analysis["hosting_indicators"].append("Hosting provider detected")
                if privacy.get("service", ""):
                    analysis["privacy_indicators"].append(f"Privacy service: {privacy['service']}")
            
            # Company information analysis
            company = ip_data.get("company", {})
            if company:
                company_name = company.get("name", "")
                company_domain = company.get("domain", "")
                company_type = company.get("type", "")
                
                if company_type == "hosting":
                    analysis["hosting_indicators"].append(f"Hosting company: {company_name}")
                elif company_type == "isp":
                    analysis["network_info"]["company_type"] = "ISP"
                
                # Check for suspicious company names
                suspicious_keywords = ["vpn", "proxy", "anonymous", "privacy", "secure"]
                if any(keyword in company_name.lower() for keyword in suspicious_keywords):
                    analysis["privacy_indicators"].append(f"Suspicious company: {company_name}")
            
            # Abuse information
            abuse = ip_data.get("abuse", {})
            if abuse:
                analysis["network_info"]["abuse_contact"] = abuse.get("email", "Unknown")
                analysis["network_info"]["abuse_name"] = abuse.get("name", "Unknown")
                analysis["network_info"]["abuse_phone"] = abuse.get("phone", "Unknown")
            
            # Domains information
            domains = ip_data.get("domains", {})
            if domains:
                total_domains = domains.get("total", 0)
                if total_domains > 1000:
                    analysis["hosting_indicators"].append(f"High domain count: {total_domains} domains")
                elif total_domains > 100:
                    analysis["hosting_indicators"].append(f"Medium domain count: {total_domains} domains")
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"IP data analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_lite_ip_data(self, lite_data: Dict, ip_address: str) -> Dict:
        """Analyze lite IP data for basic risk indicators"""
        try:
            analysis = {
                "basic_location": {},
                "basic_network": {},
                "risk_level": "LOW"
            }
            
            # Extract basic information
            analysis["basic_location"] = {
                "country": lite_data.get("country", "Unknown"),
                "country_code": lite_data.get("country_code", ""),
                "continent": lite_data.get("continent", "Unknown"),
                "continent_code": lite_data.get("continent_code", "")
            }
            
            analysis["basic_network"] = {
                "asn": lite_data.get("asn", "Unknown"),
                "as_name": lite_data.get("as_name", "Unknown"),
                "as_domain": lite_data.get("as_domain", "Unknown")
            }
            
            # Basic risk assessment
            country_code = lite_data.get("country_code", "")
            high_risk_countries = ["CN", "RU", "KP", "IR", "SY"]
            
            if country_code in high_risk_countries:
                analysis["risk_level"] = "HIGH"
            
            # Check ASN for hosting providers
            as_name = lite_data.get("as_name", "").lower()
            hosting_keywords = ["hosting", "cloud", "server", "datacenter", "digital ocean", "aws", "azure"]
            if any(keyword in as_name for keyword in hosting_keywords):
                analysis["risk_level"] = "MEDIUM" if analysis["risk_level"] == "LOW" else analysis["risk_level"]
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Lite IP data analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_asn_data(self, asn_data: Dict, asn: str) -> Dict:
        """Analyze ASN data for network intelligence"""
        try:
            analysis = {
                "asn_info": {},
                "network_type": "unknown",
                "risk_indicators": []
            }
            
            # Extract ASN information
            analysis["asn_info"] = {
                "asn": asn_data.get("asn", asn),
                "name": asn_data.get("name", "Unknown"),
                "domain": asn_data.get("domain", "Unknown"),
                "route": asn_data.get("route", "Unknown"),
                "type": asn_data.get("type", "Unknown")
            }
            
            # Determine network type
            asn_type = asn_data.get("type", "").lower()
            asn_name = asn_data.get("name", "").lower()
            
            if "hosting" in asn_type or "hosting" in asn_name:
                analysis["network_type"] = "hosting"
                analysis["risk_indicators"].append("Hosting provider ASN")
            elif "isp" in asn_type or "internet" in asn_name:
                analysis["network_type"] = "isp"
            elif "education" in asn_type or "university" in asn_name:
                analysis["network_type"] = "education"
            elif "government" in asn_type or "gov" in asn_name:
                analysis["network_type"] = "government"
            
            # Check for VPN/Proxy indicators
            vpn_keywords = ["vpn", "proxy", "anonymous", "privacy", "secure"]
            if any(keyword in asn_name for keyword in vpn_keywords):
                analysis["risk_indicators"].append("VPN/Proxy ASN detected")
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"ASN data analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_batch_results(self, batch_results: Dict) -> Dict:
        """Analyze batch IP lookup results"""
        try:
            analysis = {
                "total_ips": len(batch_results),
                "successful_lookups": 0,
                "failed_lookups": 0,
                "country_distribution": {},
                "asn_distribution": {},
                "risk_summary": {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
            }
            
            for ip, result in batch_results.items():
                if "error" in result:
                    analysis["failed_lookups"] += 1
                    continue
                
                analysis["successful_lookups"] += 1
                
                # Extract data from result
                result_analysis = result.get("analysis", {})
                basic_location = result_analysis.get("basic_location", {})
                basic_network = result_analysis.get("basic_network", {})
                risk_level = result_analysis.get("risk_level", "LOW")
                
                # Country distribution
                country = basic_location.get("country", "Unknown")
                analysis["country_distribution"][country] = analysis["country_distribution"].get(country, 0) + 1
                
                # ASN distribution
                asn = basic_network.get("asn", "Unknown")
                analysis["asn_distribution"][asn] = analysis["asn_distribution"].get(asn, 0) + 1
                
                # Risk summary
                analysis["risk_summary"][risk_level] += 1
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Batch results analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_comprehensive_ip_results(self, results: Dict, ip_address: str) -> Dict:
        """Analyze comprehensive IP investigation results"""
        try:
            analysis = {
                "overall_risk_level": "LOW",
                "risk_score": 0,
                "location_summary": {},
                "network_summary": {},
                "security_summary": {},
                "risk_factors": [],
                "recommendations": []
            }
            
            total_risk_score = 0
            
            # Analyze individual results
            for result_type, result in results.items():
                if isinstance(result, dict) and not result.get("error"):
                    result_analysis = result.get("analysis", {})
                    
                    # Extract risk factors
                    risk_indicators = result_analysis.get("risk_indicators", [])
                    privacy_indicators = result_analysis.get("privacy_indicators", [])
                    hosting_indicators = result_analysis.get("hosting_indicators", [])
                    
                    analysis["risk_factors"].extend(risk_indicators)
                    analysis["risk_factors"].extend(privacy_indicators)
                    analysis["risk_factors"].extend(hosting_indicators)
                    
                    # Calculate risk score
                    risk_score = len(risk_indicators) * 15 + len(privacy_indicators) * 20 + len(hosting_indicators) * 10
                    total_risk_score += risk_score
                    
                    # Extract summaries
                    if result_type == "full_data":
                        location_info = result_analysis.get("location", {})
                        network_info = result_analysis.get("network_info", {})
                        
                        analysis["location_summary"] = location_info
                        analysis["network_summary"] = network_info
                        
                        # Security summary
                        analysis["security_summary"] = {
                            "privacy_services": len(privacy_indicators) > 0,
                            "hosting_provider": len(hosting_indicators) > 0,
                            "anonymization_detected": any("vpn" in factor.lower() or "proxy" in factor.lower() or "tor" in factor.lower() for factor in analysis["risk_factors"])
                        }
            
            # Calculate overall risk level
            analysis["risk_score"] = min(total_risk_score, 100)
            
            if total_risk_score >= 60:
                analysis["overall_risk_level"] = "HIGH"
            elif total_risk_score >= 30:
                analysis["overall_risk_level"] = "MEDIUM"
            else:
                analysis["overall_risk_level"] = "LOW"
            
            # Generate recommendations
            if analysis["overall_risk_level"] == "HIGH":
                analysis["recommendations"].append("High-risk IP - enhanced verification required")
                analysis["recommendations"].append("Consider blocking or flagging this IP address")
            elif analysis["overall_risk_level"] == "MEDIUM":
                analysis["recommendations"].append("Medium-risk IP - additional monitoring recommended")
                analysis["recommendations"].append("Verify user identity through additional means")
            else:
                analysis["recommendations"].append("Low-risk IP - standard processing acceptable")
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Comprehensive IP analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def get_api_status(self) -> Dict:
        """Get current API usage status"""
        return {
            "api_name": "IPinfo",
            "requests_made": self.requests_made,
            "requests_this_month": self.requests_this_month,
            "monthly_limit": self.monthly_limit,
            "remaining_requests": self.monthly_limit - self.requests_this_month,
            "total_cost": round(self.total_cost, 2),
            "status": "active" if self.api_token else "inactive"
        }

# Test function
async def test_ipinfo_integration():
    """Test IPinfo API integration"""
    async with IPinfoIntegration() as api:
        print("Testing IPinfo API integration...")
        
        # Test with a known IP address (Google DNS)
        test_ip = "8.8.8.8"
        
        # Test full IP info
        ip_result = await api.get_ip_info(test_ip)
        print(f"IP info result: {json.dumps(ip_result, indent=2)}")
        
        # Test lite IP info
        lite_result = await api.get_ip_lite(test_ip)
        print(f"Lite IP info: {json.dumps(lite_result, indent=2)}")
        
        # Test ASN lookup
        asn_result = await api.get_asn_info("AS15169")
        print(f"ASN info: {json.dumps(asn_result, indent=2)}")
        
        # Test comprehensive investigation
        comprehensive_result = await api.comprehensive_ip_investigation(test_ip)
        print(f"Comprehensive investigation: {json.dumps(comprehensive_result, indent=2)}")
        
        # Print API status
        status = api.get_api_status()
        print(f"API Status: {json.dumps(status, indent=2)}")

if __name__ == "__main__":
    asyncio.run(test_ipinfo_integration())

