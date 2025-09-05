"""
Cloudflare API Integration for ScamShield AI
Provides access to DNS data, security settings, and traffic analytics for security intelligence
"""

import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json

class CloudflareIntegration:
    """
    Cloudflare API integration for security intelligence and DNS analysis
    """
    
    def __init__(self, api_token: str = "jt5q1YjcVGJ2NRSn-5qAmMikuCXDS5ZFm-6hBl3G"):
        self.api_token = api_token
        self.base_url = "https://api.cloudflare.com/client/v4"
        self.session = None
        self.logger = logging.getLogger(__name__)
        
        # Request tracking
        self.requests_made = 0
        self.total_cost = 0.0
        
        # Rate limiting (1200 requests per 5 minutes)
        self.rate_limit = 1200
        self.rate_window = 300  # 5 minutes in seconds
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json",
                "User-Agent": "ScamShield-AI/1.0"
            },
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def _make_request(self, endpoint: str, params: Dict = None, method: str = "GET") -> Dict:
        """Make authenticated request to Cloudflare API"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method.upper() == "GET":
                async with self.session.get(url, params=params) as response:
                    return await self._process_response(response, endpoint)
            elif method.upper() == "POST":
                async with self.session.post(url, json=params) as response:
                    return await self._process_response(response, endpoint)
            else:
                return {"error": f"Unsupported HTTP method: {method}"}
                    
        except asyncio.TimeoutError:
            self.logger.error("Cloudflare API request timeout")
            return {"error": "Request timeout"}
        except Exception as e:
            self.logger.error(f"Cloudflare API request failed: {str(e)}")
            return {"error": f"Request failed: {str(e)}"}
    
    async def _process_response(self, response, endpoint: str) -> Dict:
        """Process Cloudflare API response"""
        self.requests_made += 1
        self.total_cost += 0.0  # Free API
        
        if response.status == 200:
            data = await response.json()
            
            if data.get("success", False):
                self.logger.info(f"Cloudflare API request successful: {endpoint}")
                return data
            else:
                errors = data.get("errors", [])
                error_msg = "; ".join([err.get("message", "Unknown error") for err in errors])
                self.logger.error(f"Cloudflare API error: {error_msg}")
                return {"error": error_msg, "cloudflare_errors": errors}
        elif response.status == 401:
            self.logger.error("Cloudflare API authentication failed")
            return {"error": "Authentication failed", "status": 401}
        elif response.status == 403:
            self.logger.error("Cloudflare API access forbidden")
            return {"error": "Access forbidden", "status": 403}
        elif response.status == 429:
            self.logger.warning("Cloudflare API rate limit exceeded")
            return {"error": "Rate limit exceeded", "status": 429}
        else:
            error_text = await response.text()
            self.logger.error(f"Cloudflare API error {response.status}: {error_text}")
            return {"error": f"API error: {response.status}", "details": error_text}
    
    async def verify_token(self) -> Dict:
        """
        Verify API token status and permissions
        
        Returns:
            Dict containing token verification results
        """
        try:
            endpoint = "/user/tokens/verify"
            result = await self._make_request(endpoint)
            
            if "error" in result:
                return result
            
            token_info = result.get("result", {})
            
            return {
                "token_valid": True,
                "token_id": token_info.get("id"),
                "status": token_info.get("status"),
                "expires_on": token_info.get("expires_on"),
                "verification_time": datetime.utcnow().isoformat(),
                "api_cost": 0.0
            }
            
        except Exception as e:
            self.logger.error(f"Token verification failed: {str(e)}")
            return {"error": f"Token verification failed: {str(e)}"}
    
    async def list_zones(self, name: str = None, status: str = "active") -> Dict:
        """
        List Cloudflare zones (domains)
        
        Args:
            name: Filter by zone name (domain)
            status: Filter by zone status (active, pending, etc.)
            
        Returns:
            Dict containing zones and analysis
        """
        try:
            params = {"status": status}
            if name:
                params["name"] = name
            
            endpoint = "/zones"
            result = await self._make_request(endpoint, params)
            
            if "error" in result:
                return result
            
            zones = result.get("result", [])
            
            # Analyze zones
            analysis = self._analyze_zones(zones)
            
            return {
                "zones": zones,
                "total_zones": len(zones),
                "analysis": analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "api_cost": 0.0
            }
            
        except Exception as e:
            self.logger.error(f"Zone listing failed: {str(e)}")
            return {"error": f"Zone listing failed: {str(e)}"}
    
    async def get_zone_dns_records(self, zone_id: str, record_type: str = None, name: str = None) -> Dict:
        """
        Get DNS records for a zone
        
        Args:
            zone_id: Cloudflare zone ID
            record_type: Filter by record type (A, AAAA, CNAME, MX, etc.)
            name: Filter by record name
            
        Returns:
            Dict containing DNS records and analysis
        """
        try:
            params = {}
            if record_type:
                params["type"] = record_type
            if name:
                params["name"] = name
            
            endpoint = f"/zones/{zone_id}/dns_records"
            result = await self._make_request(endpoint, params)
            
            if "error" in result:
                return result
            
            dns_records = result.get("result", [])
            
            # Analyze DNS records
            analysis = self._analyze_dns_records(dns_records, zone_id)
            
            return {
                "zone_id": zone_id,
                "dns_records": dns_records,
                "total_records": len(dns_records),
                "analysis": analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "api_cost": 0.0
            }
            
        except Exception as e:
            self.logger.error(f"DNS records lookup failed: {str(e)}")
            return {"error": f"DNS records lookup failed: {str(e)}"}
    
    async def get_zone_security_settings(self, zone_id: str) -> Dict:
        """
        Get security settings for a zone
        
        Args:
            zone_id: Cloudflare zone ID
            
        Returns:
            Dict containing security settings and analysis
        """
        try:
            # Get multiple security settings
            security_settings = {}
            
            # Security level
            endpoint = f"/zones/{zone_id}/settings/security_level"
            result = await self._make_request(endpoint)
            if "error" not in result:
                security_settings["security_level"] = result.get("result", {})
            
            # SSL settings
            endpoint = f"/zones/{zone_id}/settings/ssl"
            result = await self._make_request(endpoint)
            if "error" not in result:
                security_settings["ssl"] = result.get("result", {})
            
            # Always use HTTPS
            endpoint = f"/zones/{zone_id}/settings/always_use_https"
            result = await self._make_request(endpoint)
            if "error" not in result:
                security_settings["always_use_https"] = result.get("result", {})
            
            # Bot fight mode
            endpoint = f"/zones/{zone_id}/settings/bot_fight_mode"
            result = await self._make_request(endpoint)
            if "error" not in result:
                security_settings["bot_fight_mode"] = result.get("result", {})
            
            # Analyze security settings
            analysis = self._analyze_security_settings(security_settings, zone_id)
            
            return {
                "zone_id": zone_id,
                "security_settings": security_settings,
                "analysis": analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "api_cost": 0.0
            }
            
        except Exception as e:
            self.logger.error(f"Security settings lookup failed: {str(e)}")
            return {"error": f"Security settings lookup failed: {str(e)}"}
    
    async def get_zone_analytics(self, zone_id: str, since: str = None, until: str = None) -> Dict:
        """
        Get analytics data for a zone
        
        Args:
            zone_id: Cloudflare zone ID
            since: Start date (ISO format)
            until: End date (ISO format)
            
        Returns:
            Dict containing analytics and analysis
        """
        try:
            params = {}
            if since:
                params["since"] = since
            if until:
                params["until"] = until
            
            endpoint = f"/zones/{zone_id}/analytics/dashboard"
            result = await self._make_request(endpoint, params)
            
            if "error" in result:
                return result
            
            analytics = result.get("result", {})
            
            # Analyze analytics data
            analysis = self._analyze_analytics(analytics, zone_id)
            
            return {
                "zone_id": zone_id,
                "analytics": analytics,
                "analysis": analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "api_cost": 0.0
            }
            
        except Exception as e:
            self.logger.error(f"Analytics lookup failed: {str(e)}")
            return {"error": f"Analytics lookup failed: {str(e)}"}
    
    async def comprehensive_domain_investigation(self, domain: str) -> Dict:
        """
        Comprehensive domain investigation using Cloudflare data
        
        Args:
            domain: Domain name to investigate
            
        Returns:
            Dict containing comprehensive domain analysis
        """
        try:
            results = {}
            
            # Get zone information
            zones_result = await self.list_zones(name=domain)
            if "error" not in zones_result and zones_result.get("zones"):
                zone = zones_result["zones"][0]
                zone_id = zone["id"]
                
                results["zone_info"] = zone
                
                # Get DNS records
                results["dns_records"] = await self.get_zone_dns_records(zone_id)
                
                # Get security settings
                results["security_settings"] = await self.get_zone_security_settings(zone_id)
                
                # Get analytics (last 7 days)
                since = (datetime.utcnow() - timedelta(days=7)).isoformat()
                results["analytics"] = await self.get_zone_analytics(zone_id, since=since)
            else:
                results["zone_info"] = {"error": "Domain not found in Cloudflare"}
            
            # Comprehensive analysis
            comprehensive_analysis = self._analyze_comprehensive_domain_results(results, domain)
            
            return {
                "domain": domain,
                "individual_results": results,
                "comprehensive_analysis": comprehensive_analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "total_api_cost": 0.0
            }
            
        except Exception as e:
            self.logger.error(f"Comprehensive domain investigation failed: {str(e)}")
            return {"error": f"Domain investigation failed: {str(e)}"}
    
    def _analyze_zones(self, zones: List[Dict]) -> Dict:
        """Analyze zones for security indicators"""
        try:
            analysis = {
                "total_zones": len(zones),
                "active_zones": 0,
                "paused_zones": 0,
                "plan_types": [],
                "security_indicators": []
            }
            
            for zone in zones:
                status = zone.get("status", "")
                plan = zone.get("plan", {}).get("name", "")
                
                if status == "active":
                    analysis["active_zones"] += 1
                elif status == "paused":
                    analysis["paused_zones"] += 1
                    analysis["security_indicators"].append(f"Paused zone: {zone.get('name', '')}")
                
                if plan and plan not in analysis["plan_types"]:
                    analysis["plan_types"].append(plan)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Zone analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_dns_records(self, dns_records: List[Dict], zone_id: str) -> Dict:
        """Analyze DNS records for security indicators"""
        try:
            analysis = {
                "total_records": len(dns_records),
                "record_types": {},
                "security_indicators": [],
                "suspicious_patterns": []
            }
            
            for record in dns_records:
                record_type = record.get("type", "")
                content = record.get("content", "")
                name = record.get("name", "")
                
                # Count record types
                analysis["record_types"][record_type] = analysis["record_types"].get(record_type, 0) + 1
                
                # Check for suspicious patterns
                if record_type == "A" and content.startswith("127."):
                    analysis["suspicious_patterns"].append(f"Localhost A record: {name}")
                
                if record_type == "CNAME" and "bit.ly" in content:
                    analysis["suspicious_patterns"].append(f"URL shortener CNAME: {name}")
                
                if record_type == "TXT" and "v=spf1" in content and "~all" not in content and "-all" not in content:
                    analysis["security_indicators"].append("Weak SPF record configuration")
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"DNS records analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_security_settings(self, security_settings: Dict, zone_id: str) -> Dict:
        """Analyze security settings for risk assessment"""
        try:
            analysis = {
                "security_score": 0,
                "security_strengths": [],
                "security_weaknesses": [],
                "recommendations": []
            }
            
            max_score = 100
            
            # SSL analysis
            ssl_setting = security_settings.get("ssl", {}).get("value", "")
            if ssl_setting == "strict":
                analysis["security_score"] += 30
                analysis["security_strengths"].append("Strict SSL enabled")
            elif ssl_setting == "full":
                analysis["security_score"] += 20
                analysis["security_strengths"].append("Full SSL enabled")
            elif ssl_setting == "flexible":
                analysis["security_score"] += 10
                analysis["security_weaknesses"].append("Flexible SSL (less secure)")
            else:
                analysis["security_weaknesses"].append("SSL not properly configured")
                analysis["recommendations"].append("Enable strict SSL")
            
            # Always use HTTPS
            always_https = security_settings.get("always_use_https", {}).get("value", "")
            if always_https == "on":
                analysis["security_score"] += 20
                analysis["security_strengths"].append("Always use HTTPS enabled")
            else:
                analysis["security_weaknesses"].append("Always use HTTPS disabled")
                analysis["recommendations"].append("Enable always use HTTPS")
            
            # Security level
            security_level = security_settings.get("security_level", {}).get("value", "")
            if security_level == "high":
                analysis["security_score"] += 25
                analysis["security_strengths"].append("High security level")
            elif security_level == "medium":
                analysis["security_score"] += 15
                analysis["security_strengths"].append("Medium security level")
            elif security_level == "low":
                analysis["security_score"] += 5
                analysis["security_weaknesses"].append("Low security level")
            
            # Bot fight mode
            bot_fight = security_settings.get("bot_fight_mode", {}).get("value", "")
            if bot_fight == "on":
                analysis["security_score"] += 25
                analysis["security_strengths"].append("Bot fight mode enabled")
            else:
                analysis["security_weaknesses"].append("Bot fight mode disabled")
                analysis["recommendations"].append("Enable bot fight mode")
            
            # Calculate final score
            analysis["security_score"] = min(analysis["security_score"], max_score)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Security settings analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_analytics(self, analytics: Dict, zone_id: str) -> Dict:
        """Analyze traffic analytics for patterns"""
        try:
            analysis = {
                "traffic_patterns": {},
                "security_events": {},
                "anomalies": []
            }
            
            # Analyze totals
            totals = analytics.get("totals", {})
            
            requests = totals.get("requests", {}).get("all", 0)
            bandwidth = totals.get("bandwidth", {}).get("all", 0)
            threats = totals.get("threats", {}).get("all", 0)
            
            analysis["traffic_patterns"]["total_requests"] = requests
            analysis["traffic_patterns"]["total_bandwidth"] = bandwidth
            analysis["security_events"]["total_threats"] = threats
            
            # Calculate threat ratio
            if requests > 0:
                threat_ratio = (threats / requests) * 100
                analysis["security_events"]["threat_ratio"] = threat_ratio
                
                if threat_ratio > 10:
                    analysis["anomalies"].append(f"High threat ratio: {threat_ratio:.2f}%")
                elif threat_ratio > 5:
                    analysis["anomalies"].append(f"Elevated threat ratio: {threat_ratio:.2f}%")
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Analytics analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_comprehensive_domain_results(self, results: Dict, domain: str) -> Dict:
        """Analyze comprehensive domain investigation results"""
        try:
            analysis = {
                "overall_risk_level": "LOW",
                "security_score": 0,
                "risk_factors": [],
                "security_strengths": [],
                "recommendations": []
            }
            
            # Analyze individual results
            for result_type, result in results.items():
                if isinstance(result, dict) and not result.get("error"):
                    result_analysis = result.get("analysis", {})
                    
                    # Security settings analysis
                    if result_type == "security_settings":
                        security_score = result_analysis.get("security_score", 0)
                        analysis["security_score"] = security_score
                        
                        analysis["security_strengths"].extend(result_analysis.get("security_strengths", []))
                        analysis["risk_factors"].extend(result_analysis.get("security_weaknesses", []))
                        analysis["recommendations"].extend(result_analysis.get("recommendations", []))
                        
                        if security_score < 50:
                            analysis["overall_risk_level"] = "HIGH"
                        elif security_score < 75:
                            analysis["overall_risk_level"] = "MEDIUM"
                    
                    # DNS analysis
                    if result_type == "dns_records":
                        suspicious_patterns = result_analysis.get("suspicious_patterns", [])
                        security_indicators = result_analysis.get("security_indicators", [])
                        
                        analysis["risk_factors"].extend(suspicious_patterns)
                        analysis["risk_factors"].extend(security_indicators)
                        
                        if suspicious_patterns:
                            if analysis["overall_risk_level"] == "LOW":
                                analysis["overall_risk_level"] = "MEDIUM"
                    
                    # Analytics analysis
                    if result_type == "analytics":
                        anomalies = result_analysis.get("anomalies", [])
                        analysis["risk_factors"].extend(anomalies)
                        
                        if anomalies:
                            if analysis["overall_risk_level"] == "LOW":
                                analysis["overall_risk_level"] = "MEDIUM"
            
            # Generate final recommendations
            if analysis["overall_risk_level"] == "HIGH":
                analysis["recommendations"].insert(0, "High risk domain - enhanced monitoring recommended")
            elif analysis["overall_risk_level"] == "MEDIUM":
                analysis["recommendations"].insert(0, "Medium risk domain - additional verification recommended")
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Comprehensive domain analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def get_api_status(self) -> Dict:
        """Get current API usage status"""
        return {
            "api_name": "Cloudflare",
            "requests_made": self.requests_made,
            "rate_limit": self.rate_limit,
            "rate_window_minutes": self.rate_window // 60,
            "total_cost": round(self.total_cost, 2),
            "status": "active" if self.api_token else "inactive"
        }

# Test function
async def test_cloudflare_integration():
    """Test Cloudflare API integration"""
    async with CloudflareIntegration() as api:
        print("Testing Cloudflare API integration...")
        
        # Test token verification
        verify_result = await api.verify_token()
        print(f"Token verification: {json.dumps(verify_result, indent=2)}")
        
        # Test zone listing
        zones_result = await api.list_zones()
        print(f"Zones: {json.dumps(zones_result, indent=2)}")
        
        # If we have zones, test additional features
        if zones_result.get("zones"):
            zone_id = zones_result["zones"][0]["id"]
            domain = zones_result["zones"][0]["name"]
            
            # Test DNS records
            dns_result = await api.get_zone_dns_records(zone_id)
            print(f"DNS records: {json.dumps(dns_result, indent=2)}")
            
            # Test comprehensive investigation
            comprehensive_result = await api.comprehensive_domain_investigation(domain)
            print(f"Comprehensive investigation: {json.dumps(comprehensive_result, indent=2)}")
        
        # Print API status
        status = api.get_api_status()
        print(f"API Status: {json.dumps(status, indent=2)}")

if __name__ == "__main__":
    asyncio.run(test_cloudflare_integration())

