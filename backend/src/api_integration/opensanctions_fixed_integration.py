"""
Corrected OpenSanctions API Integration for ScamShield AI
Based on official API documentation at https://api.opensanctions.org/
"""

import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

class OpenSanctionsIntegration:
    """
    Corrected OpenSanctions API integration for compliance screening and sanctions checking
    """
    
    def __init__(self, api_key: str = "579928de8a52db1706c5235975ba23b9"):
        self.api_key = api_key
        self.base_url = "https://api.opensanctions.org"
        self.session = None
        self.logger = logging.getLogger(__name__)
        
        # Request tracking
        self.requests_made = 0
        self.total_cost = 0.0
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.api_key}",
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
    
    async def _make_request(self, endpoint: str, method: str = "GET", params: Dict = None, data: Dict = None) -> Dict:
        """Make authenticated request to OpenSanctions API"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method == "GET":
                async with self.session.get(url, params=params) as response:
                    return await self._process_response(response, endpoint)
            elif method == "POST":
                async with self.session.post(url, params=params, json=data) as response:
                    return await self._process_response(response, endpoint)
                    
        except asyncio.TimeoutError:
            self.logger.error("OpenSanctions API request timeout")
            return {"error": "Request timeout"}
        except Exception as e:
            self.logger.error(f"OpenSanctions API request failed: {str(e)}")
            return {"error": f"Request failed: {str(e)}"}
    
    async def _process_response(self, response, endpoint: str) -> Dict:
        """Process API response"""
        self.requests_made += 1
        self.total_cost += 0.01  # Estimated cost per request
        
        if response.status == 200:
            data = await response.json()
            self.logger.info(f"OpenSanctions API request successful: {endpoint}")
            return data
        elif response.status == 401:
            self.logger.error("OpenSanctions API authentication failed")
            return {"error": "Authentication failed", "status": 401}
        elif response.status == 429:
            self.logger.warning("OpenSanctions API rate limit exceeded")
            return {"error": "Rate limit exceeded", "status": 429}
        else:
            error_text = await response.text()
            self.logger.error(f"OpenSanctions API error {response.status}: {error_text}")
            return {"error": f"API error: {response.status}", "details": error_text}
    
    async def search_entities(self, query: str, dataset: str = "default", limit: int = 10) -> Dict:
        """
        Search for entities using text-based search
        
        Args:
            query: Search term (name, company, etc.)
            dataset: Dataset scope (default, sanctions, peps, etc.)
            limit: Maximum number of results
            
        Returns:
            Dict containing search results and analysis
        """
        try:
            params = {
                "q": query,
                "limit": limit
            }
            
            endpoint = f"/search/{dataset}"
            result = await self._make_request(endpoint, params=params)
            
            if "error" in result:
                return result
            
            # Process and analyze results
            analysis = self._analyze_search_results(result, query)
            
            return {
                "query": query,
                "dataset": dataset,
                "total_results": result.get("total", 0),
                "results": result.get("results", []),
                "analysis": analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "api_cost": 0.01
            }
            
        except Exception as e:
            self.logger.error(f"Entity search failed: {str(e)}")
            return {"error": f"Search failed: {str(e)}"}
    
    async def match_entity(self, entity_data: Dict, dataset: str = "sanctions", threshold: float = 0.7) -> Dict:
        """
        Match an entity against the database using structured data
        
        Args:
            entity_data: Structured entity data (name, birthDate, nationality, etc.)
            dataset: Dataset scope to match against
            threshold: Score threshold for matches
            
        Returns:
            Dict containing match results
        """
        try:
            # Prepare query data
            query_data = {
                "queries": {
                    "target": entity_data
                }
            }
            
            params = {
                "threshold": threshold,
                "limit": 10
            }
            
            endpoint = f"/match/{dataset}"
            result = await self._make_request(endpoint, method="POST", params=params, data=query_data)
            
            if "error" in result:
                return result
            
            # Extract results for our target
            target_results = result.get("responses", {}).get("target", {})
            matches = target_results.get("results", [])
            
            # Analyze matches
            analysis = self._analyze_match_results(matches, entity_data)
            
            return {
                "entity_data": entity_data,
                "dataset": dataset,
                "threshold": threshold,
                "matches": matches,
                "analysis": analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "api_cost": 0.01
            }
            
        except Exception as e:
            self.logger.error(f"Entity matching failed: {str(e)}")
            return {"error": f"Matching failed: {str(e)}"}
    
    async def check_sanctions(self, name: str, country: str = None, birth_date: str = None) -> Dict:
        """
        Check if an individual or entity is on sanctions lists
        
        Args:
            name: Full name or entity name
            country: Optional country/nationality
            birth_date: Optional birth date (YYYY-MM-DD format)
            
        Returns:
            Dict containing sanctions check results
        """
        try:
            # Prepare entity data for matching
            entity_data = {
                "schema": "Person",
                "properties": {
                    "name": [name]
                }
            }
            
            if country:
                entity_data["properties"]["nationality"] = [country]
            
            if birth_date:
                entity_data["properties"]["birthDate"] = [birth_date]
            
            # Match against sanctions dataset
            result = await self.match_entity(entity_data, dataset="sanctions", threshold=0.6)
            
            if "error" in result:
                return result
            
            # Analyze for sanctions matches
            sanctions_analysis = self._analyze_sanctions_matches(result, name)
            
            return {
                "name": name,
                "country": country,
                "birth_date": birth_date,
                "sanctions_found": sanctions_analysis["has_sanctions"],
                "risk_level": sanctions_analysis["risk_level"],
                "matches": sanctions_analysis["matches"],
                "analysis": sanctions_analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "api_cost": 0.01
            }
            
        except Exception as e:
            self.logger.error(f"Sanctions check failed: {str(e)}")
            return {"error": f"Sanctions check failed: {str(e)}"}
    
    async def check_pep_status(self, name: str, country: str = None) -> Dict:
        """
        Check if an individual is a Politically Exposed Person (PEP)
        
        Args:
            name: Full name
            country: Optional country/nationality
            
        Returns:
            Dict containing PEP check results
        """
        try:
            # Prepare entity data for matching
            entity_data = {
                "schema": "Person",
                "properties": {
                    "name": [name]
                }
            }
            
            if country:
                entity_data["properties"]["nationality"] = [country]
            
            # Match against PEPs dataset
            result = await self.match_entity(entity_data, dataset="peps", threshold=0.7)
            
            if "error" in result:
                return result
            
            # Analyze for PEP matches
            pep_analysis = self._analyze_pep_matches(result, name)
            
            return {
                "name": name,
                "country": country,
                "is_pep": pep_analysis["is_pep"],
                "risk_level": pep_analysis["risk_level"],
                "matches": pep_analysis["matches"],
                "analysis": pep_analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "api_cost": 0.01
            }
            
        except Exception as e:
            self.logger.error(f"PEP check failed: {str(e)}")
            return {"error": f"PEP check failed: {str(e)}"}
    
    async def comprehensive_compliance_check(self, target_data: Dict) -> Dict:
        """
        Comprehensive compliance screening using multiple checks
        
        Args:
            target_data: Dict containing name, company, country, birth_date, etc.
            
        Returns:
            Dict containing comprehensive compliance analysis
        """
        try:
            results = {}
            
            # Individual sanctions check
            if target_data.get("name"):
                results["sanctions_check"] = await self.check_sanctions(
                    target_data["name"], 
                    target_data.get("country"),
                    target_data.get("birth_date")
                )
            
            # PEP check
            if target_data.get("name"):
                results["pep_check"] = await self.check_pep_status(
                    target_data["name"],
                    target_data.get("country")
                )
            
            # Company sanctions check
            if target_data.get("company"):
                company_entity = {
                    "schema": "Organization",
                    "properties": {
                        "name": [target_data["company"]]
                    }
                }
                if target_data.get("country"):
                    company_entity["properties"]["country"] = [target_data["country"]]
                
                results["company_sanctions"] = await self.match_entity(
                    company_entity, 
                    dataset="sanctions", 
                    threshold=0.7
                )
            
            # Comprehensive analysis
            comprehensive_analysis = self._analyze_comprehensive_results(results, target_data)
            
            return {
                "target_data": target_data,
                "individual_results": results,
                "comprehensive_analysis": comprehensive_analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "total_api_cost": len(results) * 0.01
            }
            
        except Exception as e:
            self.logger.error(f"Comprehensive compliance check failed: {str(e)}")
            return {"error": f"Comprehensive check failed: {str(e)}"}
    
    def _analyze_search_results(self, results: Dict, query: str) -> Dict:
        """Analyze search results for risk indicators"""
        try:
            analysis = {
                "total_matches": results.get("total", 0),
                "high_risk_matches": 0,
                "sanctions_matches": 0,
                "pep_matches": 0,
                "risk_indicators": [],
                "confidence_score": 0.0
            }
            
            for result in results.get("results", []):
                # Check datasets
                datasets = result.get("datasets", [])
                
                # Check for sanctions
                if any("sanction" in dataset.lower() for dataset in datasets):
                    analysis["sanctions_matches"] += 1
                    analysis["high_risk_matches"] += 1
                    analysis["risk_indicators"].append("Sanctions list match")
                
                # Check for PEP status
                if any("pep" in dataset.lower() for dataset in datasets):
                    analysis["pep_matches"] += 1
                    analysis["risk_indicators"].append("PEP (Politically Exposed Person)")
                
                # Calculate confidence based on score
                score = result.get("score", 0)
                analysis["confidence_score"] = max(analysis["confidence_score"], score)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Search results analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_match_results(self, matches: List[Dict], entity_data: Dict) -> Dict:
        """Analyze match results for risk assessment"""
        try:
            analysis = {
                "total_matches": len(matches),
                "high_confidence_matches": 0,
                "risk_level": "LOW",
                "risk_factors": [],
                "best_match_score": 0.0
            }
            
            for match in matches:
                score = match.get("score", 0)
                analysis["best_match_score"] = max(analysis["best_match_score"], score)
                
                if score > 0.8:
                    analysis["high_confidence_matches"] += 1
                
                # Check for risk factors
                datasets = match.get("datasets", [])
                for dataset in datasets:
                    if "sanction" in dataset.lower():
                        analysis["risk_factors"].append(f"Sanctions: {dataset}")
                        analysis["risk_level"] = "CRITICAL"
                    elif "pep" in dataset.lower():
                        analysis["risk_factors"].append(f"PEP: {dataset}")
                        if analysis["risk_level"] == "LOW":
                            analysis["risk_level"] = "HIGH"
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Match analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_sanctions_matches(self, result: Dict, name: str) -> Dict:
        """Analyze results specifically for sanctions matches"""
        try:
            matches = result.get("matches", [])
            analysis = result.get("analysis", {})
            
            sanctions_analysis = {
                "has_sanctions": analysis.get("risk_level") == "CRITICAL",
                "risk_level": analysis.get("risk_level", "LOW"),
                "matches": [],
                "confidence_scores": []
            }
            
            for match in matches:
                score = match.get("score", 0)
                if score > 0.6:  # Only include reasonable matches
                    match_info = {
                        "name": match.get("caption", ""),
                        "score": score,
                        "datasets": match.get("datasets", []),
                        "risk_factors": []
                    }
                    
                    # Check datasets for sanctions
                    for dataset in match.get("datasets", []):
                        if "sanction" in dataset.lower():
                            match_info["risk_factors"].append(f"Sanctions: {dataset}")
                    
                    if match_info["risk_factors"]:
                        sanctions_analysis["matches"].append(match_info)
                        sanctions_analysis["confidence_scores"].append(score)
            
            return sanctions_analysis
            
        except Exception as e:
            self.logger.error(f"Sanctions analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_pep_matches(self, result: Dict, name: str) -> Dict:
        """Analyze results specifically for PEP matches"""
        try:
            matches = result.get("matches", [])
            
            pep_analysis = {
                "is_pep": False,
                "risk_level": "LOW",
                "matches": [],
                "confidence_scores": []
            }
            
            for match in matches:
                score = match.get("score", 0)
                if score > 0.7:  # Higher threshold for PEP matches
                    pep_analysis["is_pep"] = True
                    pep_analysis["risk_level"] = "HIGH"
                    
                    match_info = {
                        "name": match.get("caption", ""),
                        "score": score,
                        "datasets": match.get("datasets", []),
                        "positions": []
                    }
                    
                    pep_analysis["matches"].append(match_info)
                    pep_analysis["confidence_scores"].append(score)
            
            return pep_analysis
            
        except Exception as e:
            self.logger.error(f"PEP analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_comprehensive_results(self, results: Dict, target_data: Dict) -> Dict:
        """Analyze comprehensive compliance check results"""
        try:
            analysis = {
                "overall_risk_level": "LOW",
                "critical_findings": [],
                "high_risk_findings": [],
                "medium_risk_findings": [],
                "compliance_status": "CLEAR",
                "recommendations": []
            }
            
            # Analyze individual results
            for check_type, result in results.items():
                if isinstance(result, dict) and not result.get("error"):
                    risk_level = result.get("analysis", {}).get("risk_level", "LOW")
                    
                    if risk_level == "CRITICAL" or result.get("sanctions_found"):
                        analysis["critical_findings"].append({
                            "type": check_type,
                            "details": result
                        })
                        analysis["overall_risk_level"] = "CRITICAL"
                        analysis["compliance_status"] = "BLOCKED"
                    
                    elif risk_level == "HIGH" or result.get("is_pep"):
                        analysis["high_risk_findings"].append({
                            "type": check_type,
                            "details": result
                        })
                        if analysis["overall_risk_level"] not in ["CRITICAL"]:
                            analysis["overall_risk_level"] = "HIGH"
                            analysis["compliance_status"] = "REVIEW_REQUIRED"
                    
                    elif risk_level == "MEDIUM":
                        analysis["medium_risk_findings"].append({
                            "type": check_type,
                            "details": result
                        })
                        if analysis["overall_risk_level"] == "LOW":
                            analysis["overall_risk_level"] = "MEDIUM"
                            analysis["compliance_status"] = "ENHANCED_DUE_DILIGENCE"
            
            # Generate recommendations
            if analysis["overall_risk_level"] == "CRITICAL":
                analysis["recommendations"].append("IMMEDIATE ACTION: Do not proceed with transaction")
                analysis["recommendations"].append("Report to compliance team immediately")
            elif analysis["overall_risk_level"] == "HIGH":
                analysis["recommendations"].append("Enhanced due diligence required")
                analysis["recommendations"].append("Senior management approval needed")
            elif analysis["overall_risk_level"] == "MEDIUM":
                analysis["recommendations"].append("Additional verification recommended")
                analysis["recommendations"].append("Document decision rationale")
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Comprehensive analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def get_api_status(self) -> Dict:
        """Get current API usage status"""
        return {
            "api_name": "OpenSanctions",
            "requests_made": self.requests_made,
            "total_cost": round(self.total_cost, 2),
            "average_cost_per_request": round(self.total_cost / max(self.requests_made, 1), 4),
            "status": "active" if self.api_key else "inactive"
        }

# Test function
async def test_corrected_opensanctions():
    """Test corrected OpenSanctions API integration"""
    async with OpenSanctionsIntegration() as api:
        print("🔍 Testing Corrected OpenSanctions API Integration")
        print("=" * 50)
        
        # Test 1: Search for a known sanctioned entity
        print("\n📋 Test 1: Search for Sanctioned Entity")
        print("-" * 30)
        search_result = await api.search_entities("Putin", dataset="sanctions", limit=3)
        print(f"Search result: {json.dumps(search_result, indent=2)}")
        
        # Test 2: Match entity against sanctions
        print("\n🚨 Test 2: Entity Matching")
        print("-" * 30)
        entity_data = {
            "schema": "Person",
            "properties": {
                "name": ["Vladimir Putin"],
                "nationality": ["ru"]
            }
        }
        match_result = await api.match_entity(entity_data, dataset="sanctions")
        print(f"Match result: {json.dumps(match_result, indent=2)}")
        
        # Test 3: Comprehensive compliance check
        print("\n🔍 Test 3: Comprehensive Check")
        print("-" * 30)
        target_data = {
            "name": "Vladimir Putin",
            "country": "RU"
        }
        comprehensive_result = await api.comprehensive_compliance_check(target_data)
        print(f"Comprehensive result: {json.dumps(comprehensive_result, indent=2)}")
        
        # Print API status
        status = api.get_api_status()
        print(f"\n📊 API Status: {json.dumps(status, indent=2)}")

if __name__ == "__main__":
    asyncio.run(test_corrected_opensanctions())

