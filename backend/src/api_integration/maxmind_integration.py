"""
MaxMind GeoIP2 API Integration for ScamShield AI
Provides access to geolocation, ISP, and IP intelligence data
"""

import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import base64

class MaxMindIntegration:
    """
    MaxMind GeoIP2 API integration for geolocation and IP intelligence
    """
    
    def __init__(self, account_id: str = "1195683", license_key: str = "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"):
        self.account_id = account_id
        self.license_key = license_key
        self.base_url = "https://geoip.maxmind.com/geoip/v2.1"
        self.session = None
        self.logger = logging.getLogger(__name__)
        
        # Request tracking
        self.requests_made = 0
        self.total_cost = 0.0
        
        # Rate limiting (1000 requests per day for free tier)
        self.daily_limit = 1000
        self.requests_today = 0
        self.last_reset = datetime.utcnow().date()
        
    async def __aenter__(self):
        """Async context manager entry"""
        # MaxMind uses Basic Auth with account_id as username and license_key as password
        auth_string = f"{self.account_id}:{self.license_key}"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
        
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Basic {auth_b64}",
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
    
    def _check_rate_limit(self) -> bool:
        """Check if we're within rate limits"""
        current_date = datetime.utcnow().date()
        
        # Reset daily counter if new day
        if current_date > self.last_reset:
            self.requests_today = 0
            self.last_reset = current_date
        
        return self.requests_today < self.daily_limit
    
    async def _make_request(self, endpoint: str) -> Dict:
        """Make authenticated request to MaxMind API"""
        try:
            # Check rate limits
            if not self._check_rate_limit():
                return {
                    "error": "Daily rate limit exceeded",
                    "limit": self.daily_limit,
                    "requests_today": self.requests_today
                }
            
            url = f"{self.base_url}{endpoint}"
            
            async with self.session.get(url) as response:
                self.requests_made += 1
                self.requests_today += 1
                self.total_cost += 0.0  # Free tier
                
                if response.status == 200:
                    data = await response.json()
                    self.logger.info(f"MaxMind API request successful: {endpoint}")
                    return data
                elif response.status == 401:
                    self.logger.error("MaxMind API authentication failed")
                    return {"error": "Authentication failed", "status": 401}
                elif response.status == 404:
                    self.logger.warning(f"MaxMind API IP not found: {endpoint}")
                    return {"error": "IP address not found", "status": 404}
                elif response.status == 429:
                    self.logger.warning("MaxMind API rate limit exceeded")
                    return {"error": "Rate limit exceeded", "status": 429}
                else:
                    error_text = await response.text()
                    self.logger.error(f"MaxMind API error {response.status}: {error_text}")
                    return {"error": f"API error: {response.status}", "details": error_text}
                    
        except asyncio.TimeoutError:
            self.logger.error("MaxMind API request timeout")
            return {"error": "Request timeout"}
        except Exception as e:
            self.logger.error(f"MaxMind API request failed: {str(e)}")
            return {"error": f"Request failed: {str(e)}"}
    
    async def get_city_data(self, ip_address: str) -> Dict:
        """
        Get city-level geolocation data for an IP address
        
        Args:
            ip_address: IP address to lookup
            
        Returns:
            Dict containing city data and analysis
        """
        try:
            endpoint = f"/city/{ip_address}"
            result = await self._make_request(endpoint)
            
            if "error" in result:
                return result
            
            # Analyze city data
            analysis = self._analyze_city_data(result, ip_address)
            
            return {
                "ip_address": ip_address,
                "city_data": result,
                "analysis": analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "api_cost": 0.0
            }
            
        except Exception as e:
            self.logger.error(f"City data lookup failed: {str(e)}")
            return {"error": f"City lookup failed: {str(e)}"}
    
    async def get_country_data(self, ip_address: str) -> Dict:
        """
        Get country-level geolocation data for an IP address
        
        Args:
            ip_address: IP address to lookup
            
        Returns:
            Dict containing country data and analysis
        """
        try:
            endpoint = f"/country/{ip_address}"
            result = await self._make_request(endpoint)
            
            if "error" in result:
                return result
            
            # Analyze country data
            analysis = self._analyze_country_data(result, ip_address)
            
            return {
                "ip_address": ip_address,
                "country_data": result,
                "analysis": analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "api_cost": 0.0
            }
            
        except Exception as e:
            self.logger.error(f"Country data lookup failed: {str(e)}")
            return {"error": f"Country lookup failed: {str(e)}"}
    
    async def get_insights_data(self, ip_address: str) -> Dict:
        """
        Get insights data for an IP address (anonymizer, hosting provider, etc.)
        
        Args:
            ip_address: IP address to lookup
            
        Returns:
            Dict containing insights data and analysis
        """
        try:
            endpoint = f"/insights/{ip_address}"
            result = await self._make_request(endpoint)
            
            if "error" in result:
                return result
            
            # Analyze insights data
            analysis = self._analyze_insights_data(result, ip_address)
            
            return {
                "ip_address": ip_address,
                "insights_data": result,
                "analysis": analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "api_cost": 0.0
            }
            
        except Exception as e:
            self.logger.error(f"Insights data lookup failed: {str(e)}")
            return {"error": f"Insights lookup failed: {str(e)}"}
    
    async def comprehensive_ip_investigation(self, ip_address: str) -> Dict:
        """
        Comprehensive IP investigation using multiple MaxMind data sources
        
        Args:
            ip_address: IP address to investigate
            
        Returns:
            Dict containing comprehensive IP analysis
        """
        try:
            results = {}
            
            # Get city data (includes most comprehensive information)
            results["city_data"] = await self.get_city_data(ip_address)
            
            # Get country data (lighter weight)
            results["country_data"] = await self.get_country_data(ip_address)
            
            # Get insights data (security-focused)
            results["insights_data"] = await self.get_insights_data(ip_address)
            
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
    
    def _analyze_city_data(self, city_data: Dict, ip_address: str) -> Dict:
        """Analyze city data for risk indicators"""
        try:
            analysis = {
                "location": {},
                "isp_info": {},
                "risk_indicators": [],
                "accuracy_radius": 0,
                "timezone": "unknown"
            }
            
            # Extract location information
            city = city_data.get("city", {})
            country = city_data.get("country", {})
            location = city_data.get("location", {})
            
            analysis["location"] = {
                "city": city.get("names", {}).get("en", "Unknown"),
                "country": country.get("names", {}).get("en", "Unknown"),
                "country_code": country.get("iso_code", ""),
                "latitude": location.get("latitude"),
                "longitude": location.get("longitude"),
                "accuracy_radius": location.get("accuracy_radius", 0)
            }
            
            analysis["accuracy_radius"] = location.get("accuracy_radius", 0)
            analysis["timezone"] = location.get("time_zone", "unknown")
            
            # ISP information
            traits = city_data.get("traits", {})
            analysis["isp_info"] = {
                "is_anonymous_proxy": traits.get("is_anonymous_proxy", False),
                "is_satellite_provider": traits.get("is_satellite_provider", False),
                "user_type": traits.get("user_type", "unknown")
            }
            
            # Risk assessment
            if traits.get("is_anonymous_proxy", False):
                analysis["risk_indicators"].append("Anonymous proxy detected")
            
            if traits.get("is_satellite_provider", False):
                analysis["risk_indicators"].append("Satellite internet provider")
            
            if analysis["accuracy_radius"] > 1000:
                analysis["risk_indicators"].append(f"Low location accuracy (radius: {analysis['accuracy_radius']}km)")
            
            # High-risk countries (example list)
            high_risk_countries = ["CN", "RU", "KP", "IR"]
            if country.get("iso_code") in high_risk_countries:
                analysis["risk_indicators"].append(f"High-risk country: {country.get('names', {}).get('en', '')}")
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"City data analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_country_data(self, country_data: Dict, ip_address: str) -> Dict:
        """Analyze country data for risk indicators"""
        try:
            analysis = {
                "country_info": {},
                "risk_level": "LOW",
                "risk_factors": []
            }
            
            # Extract country information
            country = country_data.get("country", {})
            continent = country_data.get("continent", {})
            
            analysis["country_info"] = {
                "country": country.get("names", {}).get("en", "Unknown"),
                "country_code": country.get("iso_code", ""),
                "continent": continent.get("names", {}).get("en", "Unknown"),
                "continent_code": continent.get("code", "")
            }
            
            # Risk assessment based on country
            country_code = country.get("iso_code", "")
            
            # High-risk countries
            high_risk_countries = ["CN", "RU", "KP", "IR", "SY"]
            if country_code in high_risk_countries:
                analysis["risk_level"] = "HIGH"
                analysis["risk_factors"].append(f"High-risk country: {country.get('names', {}).get('en', '')}")
            
            # Medium-risk countries
            medium_risk_countries = ["PK", "BD", "NG", "ID"]
            if country_code in medium_risk_countries:
                analysis["risk_level"] = "MEDIUM"
                analysis["risk_factors"].append(f"Medium-risk country: {country.get('names', {}).get('en', '')}")
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Country data analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_insights_data(self, insights_data: Dict, ip_address: str) -> Dict:
        """Analyze insights data for security indicators"""
        try:
            analysis = {
                "security_indicators": [],
                "anonymizer_status": False,
                "hosting_provider": False,
                "risk_score": 0,
                "user_type": "unknown"
            }
            
            # Extract traits
            traits = insights_data.get("traits", {})
            
            # Anonymizer detection
            if traits.get("is_anonymous_proxy", False):
                analysis["anonymizer_status"] = True
                analysis["security_indicators"].append("Anonymous proxy detected")
                analysis["risk_score"] += 30
            
            if traits.get("is_tor_exit_node", False):
                analysis["security_indicators"].append("Tor exit node detected")
                analysis["risk_score"] += 40
            
            # Hosting provider detection
            if traits.get("is_hosting_provider", False):
                analysis["hosting_provider"] = True
                analysis["security_indicators"].append("Hosting provider IP")
                analysis["risk_score"] += 20
            
            # User type analysis
            user_type = traits.get("user_type", "")
            analysis["user_type"] = user_type
            
            if user_type == "hosting":
                analysis["security_indicators"].append("Hosting/datacenter IP")
                analysis["risk_score"] += 15
            elif user_type == "cellular":
                analysis["security_indicators"].append("Mobile/cellular IP")
            elif user_type == "dialup":
                analysis["security_indicators"].append("Dial-up connection")
            
            # ISP information
            isp = insights_data.get("isp", {})
            if isp:
                isp_name = isp.get("name", "")
                if "vpn" in isp_name.lower() or "proxy" in isp_name.lower():
                    analysis["security_indicators"].append(f"VPN/Proxy ISP: {isp_name}")
                    analysis["risk_score"] += 25
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Insights data analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_comprehensive_ip_results(self, results: Dict, ip_address: str) -> Dict:
        """Analyze comprehensive IP investigation results"""
        try:
            analysis = {
                "overall_risk_level": "LOW",
                "risk_score": 0,
                "location_summary": {},
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
                    risk_factors = result_analysis.get("risk_factors", [])
                    security_indicators = result_analysis.get("security_indicators", [])
                    
                    analysis["risk_factors"].extend(risk_indicators)
                    analysis["risk_factors"].extend(risk_factors)
                    analysis["risk_factors"].extend(security_indicators)
                    
                    # Accumulate risk scores
                    risk_score = result_analysis.get("risk_score", 0)
                    total_risk_score += risk_score
                    
                    # Extract location summary
                    if result_type == "city_data":
                        location_info = result_analysis.get("location", {})
                        analysis["location_summary"] = location_info
                    
                    # Extract security summary
                    if result_type == "insights_data":
                        analysis["security_summary"] = {
                            "anonymizer_status": result_analysis.get("anonymizer_status", False),
                            "hosting_provider": result_analysis.get("hosting_provider", False),
                            "user_type": result_analysis.get("user_type", "unknown")
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
            "api_name": "MaxMind GeoIP2",
            "account_id": self.account_id,
            "requests_made": self.requests_made,
            "requests_today": self.requests_today,
            "daily_limit": self.daily_limit,
            "remaining_requests": self.daily_limit - self.requests_today,
            "total_cost": round(self.total_cost, 2),
            "status": "active" if self.license_key else "inactive"
        }

# Test function
async def test_maxmind_integration():
    """Test MaxMind API integration"""
    async with MaxMindIntegration() as api:
        print("Testing MaxMind GeoIP2 API integration...")
        
        # Test with a known IP address (Google DNS)
        test_ip = "8.8.8.8"
        
        # Test city data
        city_result = await api.get_city_data(test_ip)
        print(f"City data result: {json.dumps(city_result, indent=2)}")
        
        # Test country data
        country_result = await api.get_country_data(test_ip)
        print(f"Country data: {json.dumps(country_result, indent=2)}")
        
        # Test insights data
        insights_result = await api.get_insights_data(test_ip)
        print(f"Insights data: {json.dumps(insights_result, indent=2)}")
        
        # Test comprehensive investigation
        comprehensive_result = await api.comprehensive_ip_investigation(test_ip)
        print(f"Comprehensive investigation: {json.dumps(comprehensive_result, indent=2)}")
        
        # Print API status
        status = api.get_api_status()
        print(f"API Status: {json.dumps(status, indent=2)}")

if __name__ == "__main__":
    asyncio.run(test_maxmind_integration())

