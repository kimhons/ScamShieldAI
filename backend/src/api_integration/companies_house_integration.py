"""
Companies House API Integration for ScamShield AI
Provides access to UK company data, director information, and filing history
"""

import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import base64

class CompaniesHouseIntegration:
    """
    Companies House API integration for UK company intelligence and corporate fraud investigation
    """
    
    def __init__(self, api_key: str = "9e899963-34fb-4c3e-8377-cc881667d5b4"):
        self.api_key = api_key
        self.base_url = "https://api.company-information.service.gov.uk"
        self.session = None
        self.logger = logging.getLogger(__name__)
        
        # Request tracking
        self.requests_made = 0
        self.total_cost = 0.0
        
        # Rate limiting (600 requests per 5 minutes)
        self.rate_limit = 600
        self.rate_window = 300  # 5 minutes in seconds
        
    async def __aenter__(self):
        """Async context manager entry"""
        # Companies House uses Basic Auth with API key as username and empty password
        auth_string = f"{self.api_key}:"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
        
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Basic {auth_b64}",
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
    
    async def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make authenticated request to Companies House API"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            async with self.session.get(url, params=params) as response:
                self.requests_made += 1
                self.total_cost += 0.0  # Free API
                
                if response.status == 200:
                    data = await response.json()
                    self.logger.info(f"Companies House API request successful: {endpoint}")
                    return data
                elif response.status == 401:
                    self.logger.error("Companies House API authentication failed")
                    return {"error": "Authentication failed", "status": 401}
                elif response.status == 404:
                    self.logger.warning(f"Companies House API resource not found: {endpoint}")
                    return {"error": "Resource not found", "status": 404}
                elif response.status == 429:
                    self.logger.warning("Companies House API rate limit exceeded")
                    return {"error": "Rate limit exceeded", "status": 429}
                else:
                    error_text = await response.text()
                    self.logger.error(f"Companies House API error {response.status}: {error_text}")
                    return {"error": f"API error: {response.status}", "details": error_text}
                    
        except asyncio.TimeoutError:
            self.logger.error("Companies House API request timeout")
            return {"error": "Request timeout"}
        except Exception as e:
            self.logger.error(f"Companies House API request failed: {str(e)}")
            return {"error": f"Request failed: {str(e)}"}
    
    async def search_companies(self, query: str, items_per_page: int = 20) -> Dict:
        """
        Search for companies by name or number
        
        Args:
            query: Company name or number to search for
            items_per_page: Number of results per page (max 100)
            
        Returns:
            Dict containing search results and analysis
        """
        try:
            params = {
                "q": query,
                "items_per_page": min(items_per_page, 100)
            }
            
            endpoint = "/search/companies"
            result = await self._make_request(endpoint, params)
            
            if "error" in result:
                return result
            
            # Analyze search results
            analysis = self._analyze_company_search_results(result, query)
            
            return {
                "query": query,
                "total_results": result.get("total_results", 0),
                "items": result.get("items", []),
                "analysis": analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "api_cost": 0.0
            }
            
        except Exception as e:
            self.logger.error(f"Company search failed: {str(e)}")
            return {"error": f"Company search failed: {str(e)}"}
    
    async def get_company_profile(self, company_number: str) -> Dict:
        """
        Get detailed company profile information
        
        Args:
            company_number: Companies House company number
            
        Returns:
            Dict containing company profile and analysis
        """
        try:
            endpoint = f"/company/{company_number}"
            result = await self._make_request(endpoint)
            
            if "error" in result:
                return result
            
            # Analyze company profile
            analysis = self._analyze_company_profile(result, company_number)
            
            return {
                "company_number": company_number,
                "company_data": result,
                "analysis": analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "api_cost": 0.0
            }
            
        except Exception as e:
            self.logger.error(f"Company profile lookup failed: {str(e)}")
            return {"error": f"Company profile lookup failed: {str(e)}"}
    
    async def get_company_officers(self, company_number: str, items_per_page: int = 35) -> Dict:
        """
        Get company officers (directors, secretaries, etc.)
        
        Args:
            company_number: Companies House company number
            items_per_page: Number of officers per page (max 35)
            
        Returns:
            Dict containing officers data and analysis
        """
        try:
            params = {
                "items_per_page": min(items_per_page, 35)
            }
            
            endpoint = f"/company/{company_number}/officers"
            result = await self._make_request(endpoint, params)
            
            if "error" in result:
                return result
            
            # Analyze officers data
            analysis = self._analyze_company_officers(result, company_number)
            
            return {
                "company_number": company_number,
                "total_results": result.get("total_results", 0),
                "officers": result.get("items", []),
                "analysis": analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "api_cost": 0.0
            }
            
        except Exception as e:
            self.logger.error(f"Company officers lookup failed: {str(e)}")
            return {"error": f"Company officers lookup failed: {str(e)}"}
    
    async def get_company_filing_history(self, company_number: str, items_per_page: int = 25) -> Dict:
        """
        Get company filing history
        
        Args:
            company_number: Companies House company number
            items_per_page: Number of filings per page (max 100)
            
        Returns:
            Dict containing filing history and analysis
        """
        try:
            params = {
                "items_per_page": min(items_per_page, 100)
            }
            
            endpoint = f"/company/{company_number}/filing-history"
            result = await self._make_request(endpoint, params)
            
            if "error" in result:
                return result
            
            # Analyze filing history
            analysis = self._analyze_filing_history(result, company_number)
            
            return {
                "company_number": company_number,
                "total_results": result.get("total_results", 0),
                "filings": result.get("items", []),
                "analysis": analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "api_cost": 0.0
            }
            
        except Exception as e:
            self.logger.error(f"Filing history lookup failed: {str(e)}")
            return {"error": f"Filing history lookup failed: {str(e)}"}
    
    async def search_officers(self, query: str, items_per_page: int = 20) -> Dict:
        """
        Search for officers by name
        
        Args:
            query: Officer name to search for
            items_per_page: Number of results per page (max 50)
            
        Returns:
            Dict containing officer search results and analysis
        """
        try:
            params = {
                "q": query,
                "items_per_page": min(items_per_page, 50)
            }
            
            endpoint = "/search/officers"
            result = await self._make_request(endpoint, params)
            
            if "error" in result:
                return result
            
            # Analyze officer search results
            analysis = self._analyze_officer_search_results(result, query)
            
            return {
                "query": query,
                "total_results": result.get("total_results", 0),
                "officers": result.get("items", []),
                "analysis": analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "api_cost": 0.0
            }
            
        except Exception as e:
            self.logger.error(f"Officer search failed: {str(e)}")
            return {"error": f"Officer search failed: {str(e)}"}
    
    async def comprehensive_company_investigation(self, target_data: Dict) -> Dict:
        """
        Comprehensive company investigation using multiple data sources
        
        Args:
            target_data: Dict containing company name, number, officer names, etc.
            
        Returns:
            Dict containing comprehensive company analysis
        """
        try:
            results = {}
            
            # Company search
            if target_data.get("company_name"):
                results["company_search"] = await self.search_companies(target_data["company_name"])
            
            # Company profile analysis
            if target_data.get("company_number"):
                results["company_profile"] = await self.get_company_profile(target_data["company_number"])
                results["company_officers"] = await self.get_company_officers(target_data["company_number"])
                results["filing_history"] = await self.get_company_filing_history(target_data["company_number"])
            
            # Officer search
            if target_data.get("officer_name"):
                results["officer_search"] = await self.search_officers(target_data["officer_name"])
            
            # Comprehensive analysis
            comprehensive_analysis = self._analyze_comprehensive_company_results(results, target_data)
            
            return {
                "target_data": target_data,
                "individual_results": results,
                "comprehensive_analysis": comprehensive_analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "total_api_cost": 0.0
            }
            
        except Exception as e:
            self.logger.error(f"Comprehensive company investigation failed: {str(e)}")
            return {"error": f"Company investigation failed: {str(e)}"}
    
    def _analyze_company_search_results(self, results: Dict, query: str) -> Dict:
        """Analyze company search results for risk indicators"""
        try:
            analysis = {
                "total_matches": results.get("total_results", 0),
                "exact_matches": 0,
                "active_companies": 0,
                "dissolved_companies": 0,
                "risk_indicators": [],
                "company_types": []
            }
            
            for item in results.get("items", []):
                company_name = item.get("title", "").lower()
                company_status = item.get("company_status", "")
                company_type = item.get("company_type", "")
                
                # Check for exact matches
                if query.lower() in company_name:
                    analysis["exact_matches"] += 1
                
                # Count company statuses
                if company_status == "active":
                    analysis["active_companies"] += 1
                elif company_status in ["dissolved", "liquidation"]:
                    analysis["dissolved_companies"] += 1
                    analysis["risk_indicators"].append(f"Dissolved/liquidated company found: {item.get('title', '')}")
                
                # Collect company types
                if company_type and company_type not in analysis["company_types"]:
                    analysis["company_types"].append(company_type)
            
            # Risk assessment
            if analysis["dissolved_companies"] > analysis["active_companies"]:
                analysis["risk_indicators"].append("More dissolved companies than active ones")
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Company search analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_company_profile(self, company_data: Dict, company_number: str) -> Dict:
        """Analyze company profile for risk indicators"""
        try:
            analysis = {
                "company_status": company_data.get("company_status", "unknown"),
                "company_type": company_data.get("company_type", "unknown"),
                "incorporation_date": company_data.get("date_of_creation", ""),
                "risk_level": "LOW",
                "risk_factors": [],
                "business_activity": "unknown"
            }
            
            # Status analysis
            status = company_data.get("company_status", "").lower()
            if status in ["dissolved", "liquidation", "receivership"]:
                analysis["risk_factors"].append(f"Company status: {status}")
                analysis["risk_level"] = "HIGH"
            elif status in ["dormant", "voluntary-arrangement"]:
                analysis["risk_factors"].append(f"Company status: {status}")
                analysis["risk_level"] = "MEDIUM"
            
            # Age analysis
            incorporation_date = company_data.get("date_of_creation")
            if incorporation_date:
                try:
                    inc_date = datetime.strptime(incorporation_date, "%Y-%m-%d")
                    age_days = (datetime.utcnow() - inc_date).days
                    
                    if age_days < 90:  # Less than 3 months old
                        analysis["risk_factors"].append("Very new company (less than 3 months)")
                        analysis["risk_level"] = "MEDIUM"
                    elif age_days < 365:  # Less than 1 year old
                        analysis["risk_factors"].append("New company (less than 1 year)")
                        if analysis["risk_level"] == "LOW":
                            analysis["risk_level"] = "MEDIUM"
                except:
                    pass
            
            # Address analysis
            registered_office = company_data.get("registered_office_address", {})
            if registered_office:
                # Check for PO Box addresses (higher risk)
                address_line_1 = registered_office.get("address_line_1", "").lower()
                if "po box" in address_line_1 or "p.o. box" in address_line_1:
                    analysis["risk_factors"].append("Registered to PO Box address")
                    if analysis["risk_level"] == "LOW":
                        analysis["risk_level"] = "MEDIUM"
            
            # SIC codes analysis
            sic_codes = company_data.get("sic_codes", [])
            high_risk_sic_codes = ["64999", "82990", "70229"]  # Financial services, business support, management consultancy
            for sic_code in sic_codes:
                if sic_code in high_risk_sic_codes:
                    analysis["risk_factors"].append(f"High-risk SIC code: {sic_code}")
                    if analysis["risk_level"] == "LOW":
                        analysis["risk_level"] = "MEDIUM"
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Company profile analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_company_officers(self, officers_data: Dict, company_number: str) -> Dict:
        """Analyze company officers for risk indicators"""
        try:
            analysis = {
                "total_officers": officers_data.get("total_results", 0),
                "active_officers": 0,
                "resigned_officers": 0,
                "director_count": 0,
                "secretary_count": 0,
                "risk_factors": [],
                "officer_nationalities": []
            }
            
            for officer in officers_data.get("items", []):
                officer_role = officer.get("officer_role", "").lower()
                resigned_on = officer.get("resigned_on")
                nationality = officer.get("nationality")
                
                # Count by status
                if resigned_on:
                    analysis["resigned_officers"] += 1
                else:
                    analysis["active_officers"] += 1
                
                # Count by role
                if "director" in officer_role:
                    analysis["director_count"] += 1
                elif "secretary" in officer_role:
                    analysis["secretary_count"] += 1
                
                # Collect nationalities
                if nationality and nationality not in analysis["officer_nationalities"]:
                    analysis["officer_nationalities"].append(nationality)
            
            # Risk assessment
            if analysis["total_officers"] == 0:
                analysis["risk_factors"].append("No officers found")
            elif analysis["active_officers"] == 0:
                analysis["risk_factors"].append("No active officers")
            elif analysis["director_count"] == 0:
                analysis["risk_factors"].append("No directors found")
            
            if analysis["resigned_officers"] > analysis["active_officers"]:
                analysis["risk_factors"].append("More resigned officers than active ones")
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Officers analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_filing_history(self, filing_data: Dict, company_number: str) -> Dict:
        """Analyze company filing history for compliance indicators"""
        try:
            analysis = {
                "total_filings": filing_data.get("total_results", 0),
                "recent_filings": 0,
                "overdue_filings": 0,
                "filing_types": [],
                "compliance_status": "UNKNOWN",
                "risk_factors": []
            }
            
            current_date = datetime.utcnow()
            one_year_ago = current_date - timedelta(days=365)
            
            for filing in filing_data.get("items", []):
                filing_date_str = filing.get("date")
                filing_type = filing.get("type", "")
                
                # Count recent filings
                if filing_date_str:
                    try:
                        filing_date = datetime.strptime(filing_date_str, "%Y-%m-%d")
                        if filing_date >= one_year_ago:
                            analysis["recent_filings"] += 1
                    except:
                        pass
                
                # Collect filing types
                if filing_type and filing_type not in analysis["filing_types"]:
                    analysis["filing_types"].append(filing_type)
            
            # Compliance assessment
            if analysis["recent_filings"] == 0:
                analysis["risk_factors"].append("No recent filings in past year")
                analysis["compliance_status"] = "POOR"
            elif analysis["recent_filings"] < 2:
                analysis["risk_factors"].append("Very few recent filings")
                analysis["compliance_status"] = "MODERATE"
            else:
                analysis["compliance_status"] = "GOOD"
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Filing history analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_officer_search_results(self, results: Dict, query: str) -> Dict:
        """Analyze officer search results"""
        try:
            analysis = {
                "total_matches": results.get("total_results", 0),
                "active_appointments": 0,
                "resigned_appointments": 0,
                "companies_involved": [],
                "officer_roles": []
            }
            
            for officer in results.get("items", []):
                # Count appointments
                if officer.get("resigned_on"):
                    analysis["resigned_appointments"] += 1
                else:
                    analysis["active_appointments"] += 1
                
                # Collect companies
                company_name = officer.get("title", "")
                if company_name and company_name not in analysis["companies_involved"]:
                    analysis["companies_involved"].append(company_name)
                
                # Collect roles
                officer_role = officer.get("description", "")
                if officer_role and officer_role not in analysis["officer_roles"]:
                    analysis["officer_roles"].append(officer_role)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Officer search analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_comprehensive_company_results(self, results: Dict, target_data: Dict) -> Dict:
        """Analyze comprehensive company investigation results"""
        try:
            analysis = {
                "overall_risk_level": "LOW",
                "corporate_risk_factors": [],
                "compliance_indicators": [],
                "legitimacy_score": 0.0,
                "recommendations": []
            }
            
            risk_score = 0
            max_score = 100
            
            # Analyze individual results
            for result_type, result in results.items():
                if isinstance(result, dict) and not result.get("error"):
                    result_analysis = result.get("analysis", {})
                    
                    # Extract risk factors
                    risk_factors = result_analysis.get("risk_factors", [])
                    analysis["corporate_risk_factors"].extend(risk_factors)
                    
                    # Assess risk level
                    risk_level = result_analysis.get("risk_level", "LOW")
                    if risk_level == "HIGH":
                        risk_score += 30
                        analysis["overall_risk_level"] = "HIGH"
                    elif risk_level == "MEDIUM":
                        risk_score += 15
                        if analysis["overall_risk_level"] == "LOW":
                            analysis["overall_risk_level"] = "MEDIUM"
                    
                    # Compliance indicators
                    compliance_status = result_analysis.get("compliance_status")
                    if compliance_status:
                        analysis["compliance_indicators"].append(f"{result_type}: {compliance_status}")
            
            # Calculate legitimacy score
            analysis["legitimacy_score"] = max(0, (max_score - risk_score) / max_score)
            
            # Generate recommendations
            if analysis["overall_risk_level"] == "HIGH":
                analysis["recommendations"].append("High risk company - enhanced due diligence required")
                analysis["recommendations"].append("Verify company legitimacy through additional sources")
            elif analysis["overall_risk_level"] == "MEDIUM":
                analysis["recommendations"].append("Medium risk - additional verification recommended")
                analysis["recommendations"].append("Monitor company status and filing compliance")
            else:
                analysis["recommendations"].append("Low risk company - standard verification sufficient")
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Comprehensive company analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def get_api_status(self) -> Dict:
        """Get current API usage status"""
        return {
            "api_name": "Companies House",
            "requests_made": self.requests_made,
            "rate_limit": self.rate_limit,
            "rate_window_minutes": self.rate_window // 60,
            "total_cost": round(self.total_cost, 2),
            "status": "active" if self.api_key else "inactive"
        }

# Test function
async def test_companies_house_integration():
    """Test Companies House API integration"""
    async with CompaniesHouseIntegration() as api:
        print("Testing Companies House API integration...")
        
        # Test company search
        search_result = await api.search_companies("Apple", items_per_page=5)
        print(f"Company search result: {json.dumps(search_result, indent=2)}")
        
        # Test company profile (using a known UK company number)
        profile_result = await api.get_company_profile("00006245")  # Marks & Spencer
        print(f"Company profile: {json.dumps(profile_result, indent=2)}")
        
        # Test company officers
        officers_result = await api.get_company_officers("00006245")
        print(f"Company officers: {json.dumps(officers_result, indent=2)}")
        
        # Test comprehensive investigation
        target_data = {
            "company_name": "Apple",
            "company_number": "00006245"
        }
        comprehensive_result = await api.comprehensive_company_investigation(target_data)
        print(f"Comprehensive investigation: {json.dumps(comprehensive_result, indent=2)}")
        
        # Print API status
        status = api.get_api_status()
        print(f"API Status: {json.dumps(status, indent=2)}")

if __name__ == "__main__":
    asyncio.run(test_companies_house_integration())

