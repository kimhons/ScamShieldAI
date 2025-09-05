"""
Alpha Vantage API Integration for ScamShield AI
Provides access to financial market data, stocks, forex, crypto, and economic indicators
"""

import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json

class AlphaVantageIntegration:
    """
    Alpha Vantage API integration for financial intelligence and market data
    """
    
    def __init__(self, api_key: str = "14X3TK5E9HJIO3SD"):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
        self.session = None
        self.logger = logging.getLogger(__name__)
        
        # Request tracking
        self.requests_made = 0
        self.total_cost = 0.0
        
        # Rate limiting (500 requests per day for free tier)
        self.daily_limit = 500
        self.requests_today = 0
        self.last_reset = datetime.utcnow().date()
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
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
    
    async def _make_request(self, params: Dict) -> Dict:
        """Make authenticated request to Alpha Vantage API"""
        try:
            # Check rate limits
            if not self._check_rate_limit():
                return {
                    "error": "Daily rate limit exceeded",
                    "limit": self.daily_limit,
                    "requests_today": self.requests_today
                }
            
            # Add API key to parameters
            params["apikey"] = self.api_key
            
            async with self.session.get(self.base_url, params=params) as response:
                self.requests_made += 1
                self.requests_today += 1
                self.total_cost += 0.0  # Free tier
                
                if response.status == 200:
                    data = await response.json()
                    
                    # Check for API error messages
                    if "Error Message" in data:
                        self.logger.error(f"Alpha Vantage API error: {data['Error Message']}")
                        return {"error": data["Error Message"]}
                    
                    if "Note" in data:
                        self.logger.warning(f"Alpha Vantage API note: {data['Note']}")
                        return {"error": "Rate limit exceeded", "note": data["Note"]}
                    
                    self.logger.info("Alpha Vantage API request successful")
                    return data
                else:
                    error_text = await response.text()
                    self.logger.error(f"Alpha Vantage API error {response.status}: {error_text}")
                    return {"error": f"API error: {response.status}", "details": error_text}
                    
        except asyncio.TimeoutError:
            self.logger.error("Alpha Vantage API request timeout")
            return {"error": "Request timeout"}
        except Exception as e:
            self.logger.error(f"Alpha Vantage API request failed: {str(e)}")
            return {"error": f"Request failed: {str(e)}"}
    
    async def get_stock_quote(self, symbol: str) -> Dict:
        """
        Get real-time stock quote
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'MSFT')
            
        Returns:
            Dict containing stock quote data and analysis
        """
        try:
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": symbol
            }
            
            result = await self._make_request(params)
            
            if "error" in result:
                return result
            
            # Extract quote data
            quote_data = result.get("Global Quote", {})
            
            if not quote_data:
                return {"error": "No quote data found", "symbol": symbol}
            
            # Analyze quote data
            analysis = self._analyze_stock_quote(quote_data, symbol)
            
            return {
                "symbol": symbol,
                "quote_data": quote_data,
                "analysis": analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "api_cost": 0.0
            }
            
        except Exception as e:
            self.logger.error(f"Stock quote lookup failed: {str(e)}")
            return {"error": f"Quote lookup failed: {str(e)}"}
    
    async def get_company_overview(self, symbol: str) -> Dict:
        """
        Get comprehensive company overview
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dict containing company overview and analysis
        """
        try:
            params = {
                "function": "OVERVIEW",
                "symbol": symbol
            }
            
            result = await self._make_request(params)
            
            if "error" in result:
                return result
            
            # Analyze company data
            analysis = self._analyze_company_overview(result, symbol)
            
            return {
                "symbol": symbol,
                "company_data": result,
                "analysis": analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "api_cost": 0.0
            }
            
        except Exception as e:
            self.logger.error(f"Company overview lookup failed: {str(e)}")
            return {"error": f"Company lookup failed: {str(e)}"}
    
    async def search_symbol(self, keywords: str) -> Dict:
        """
        Search for stock symbols by company name or keywords
        
        Args:
            keywords: Search keywords (company name, etc.)
            
        Returns:
            Dict containing search results and analysis
        """
        try:
            params = {
                "function": "SYMBOL_SEARCH",
                "keywords": keywords
            }
            
            result = await self._make_request(params)
            
            if "error" in result:
                return result
            
            # Extract search results
            matches = result.get("bestMatches", [])
            
            # Analyze search results
            analysis = self._analyze_symbol_search(matches, keywords)
            
            return {
                "keywords": keywords,
                "matches": matches,
                "analysis": analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "api_cost": 0.0
            }
            
        except Exception as e:
            self.logger.error(f"Symbol search failed: {str(e)}")
            return {"error": f"Symbol search failed: {str(e)}"}
    
    async def get_forex_rate(self, from_currency: str, to_currency: str) -> Dict:
        """
        Get real-time forex exchange rate
        
        Args:
            from_currency: Source currency (e.g., 'USD')
            to_currency: Target currency (e.g., 'EUR')
            
        Returns:
            Dict containing forex rate and analysis
        """
        try:
            params = {
                "function": "CURRENCY_EXCHANGE_RATE",
                "from_currency": from_currency,
                "to_currency": to_currency
            }
            
            result = await self._make_request(params)
            
            if "error" in result:
                return result
            
            # Extract exchange rate data
            rate_data = result.get("Realtime Currency Exchange Rate", {})
            
            if not rate_data:
                return {"error": "No exchange rate data found"}
            
            # Analyze forex data
            analysis = self._analyze_forex_rate(rate_data, from_currency, to_currency)
            
            return {
                "from_currency": from_currency,
                "to_currency": to_currency,
                "rate_data": rate_data,
                "analysis": analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "api_cost": 0.0
            }
            
        except Exception as e:
            self.logger.error(f"Forex rate lookup failed: {str(e)}")
            return {"error": f"Forex lookup failed: {str(e)}"}
    
    async def get_crypto_quote(self, symbol: str, market: str = "USD") -> Dict:
        """
        Get cryptocurrency quote
        
        Args:
            symbol: Crypto symbol (e.g., 'BTC', 'ETH')
            market: Market currency (default: 'USD')
            
        Returns:
            Dict containing crypto quote and analysis
        """
        try:
            params = {
                "function": "CURRENCY_EXCHANGE_RATE",
                "from_currency": symbol,
                "to_currency": market
            }
            
            result = await self._make_request(params)
            
            if "error" in result:
                return result
            
            # Extract crypto rate data
            rate_data = result.get("Realtime Currency Exchange Rate", {})
            
            if not rate_data:
                return {"error": "No crypto data found"}
            
            # Analyze crypto data
            analysis = self._analyze_crypto_quote(rate_data, symbol, market)
            
            return {
                "symbol": symbol,
                "market": market,
                "rate_data": rate_data,
                "analysis": analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "api_cost": 0.0
            }
            
        except Exception as e:
            self.logger.error(f"Crypto quote lookup failed: {str(e)}")
            return {"error": f"Crypto lookup failed: {str(e)}"}
    
    async def comprehensive_financial_investigation(self, target_data: Dict) -> Dict:
        """
        Comprehensive financial investigation using multiple data sources
        
        Args:
            target_data: Dict containing company names, symbols, currencies, etc.
            
        Returns:
            Dict containing comprehensive financial analysis
        """
        try:
            results = {}
            
            # Company symbol search
            if target_data.get("company_name"):
                results["symbol_search"] = await self.search_symbol(target_data["company_name"])
            
            # Stock quote analysis
            if target_data.get("stock_symbol"):
                results["stock_quote"] = await self.get_stock_quote(target_data["stock_symbol"])
                results["company_overview"] = await self.get_company_overview(target_data["stock_symbol"])
            
            # Forex analysis
            if target_data.get("currency_from") and target_data.get("currency_to"):
                results["forex_rate"] = await self.get_forex_rate(
                    target_data["currency_from"],
                    target_data["currency_to"]
                )
            
            # Crypto analysis
            if target_data.get("crypto_symbol"):
                results["crypto_quote"] = await self.get_crypto_quote(
                    target_data["crypto_symbol"],
                    target_data.get("crypto_market", "USD")
                )
            
            # Comprehensive analysis
            comprehensive_analysis = self._analyze_comprehensive_financial_results(results, target_data)
            
            return {
                "target_data": target_data,
                "individual_results": results,
                "comprehensive_analysis": comprehensive_analysis,
                "timestamp": datetime.utcnow().isoformat(),
                "total_api_cost": 0.0
            }
            
        except Exception as e:
            self.logger.error(f"Comprehensive financial investigation failed: {str(e)}")
            return {"error": f"Financial investigation failed: {str(e)}"}
    
    def _analyze_stock_quote(self, quote_data: Dict, symbol: str) -> Dict:
        """Analyze stock quote data for risk indicators"""
        try:
            analysis = {
                "current_price": 0.0,
                "change_percent": 0.0,
                "volume": 0,
                "risk_indicators": [],
                "market_status": "UNKNOWN"
            }
            
            # Extract key metrics
            price = float(quote_data.get("05. price", 0))
            change_percent = float(quote_data.get("10. change percent", "0%").replace("%", ""))
            volume = int(quote_data.get("06. volume", 0))
            
            analysis["current_price"] = price
            analysis["change_percent"] = change_percent
            analysis["volume"] = volume
            
            # Risk assessment
            if abs(change_percent) > 10:
                analysis["risk_indicators"].append("High volatility (>10% daily change)")
                analysis["market_status"] = "HIGH_VOLATILITY"
            elif abs(change_percent) > 5:
                analysis["risk_indicators"].append("Moderate volatility (>5% daily change)")
                analysis["market_status"] = "MODERATE_VOLATILITY"
            else:
                analysis["market_status"] = "STABLE"
            
            if volume == 0:
                analysis["risk_indicators"].append("No trading volume")
                analysis["market_status"] = "ILLIQUID"
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Stock quote analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_company_overview(self, company_data: Dict, symbol: str) -> Dict:
        """Analyze company overview data"""
        try:
            analysis = {
                "market_cap": 0,
                "sector": "Unknown",
                "risk_level": "LOW",
                "risk_factors": [],
                "financial_health": "UNKNOWN"
            }
            
            # Extract key metrics
            market_cap = company_data.get("MarketCapitalization", "0")
            sector = company_data.get("Sector", "Unknown")
            pe_ratio = company_data.get("PERatio", "N/A")
            
            analysis["sector"] = sector
            
            # Market cap analysis
            try:
                market_cap_value = float(market_cap)
                analysis["market_cap"] = market_cap_value
                
                if market_cap_value < 300000000:  # < $300M
                    analysis["risk_factors"].append("Small cap company (higher risk)")
                    analysis["risk_level"] = "HIGH"
                elif market_cap_value < 2000000000:  # < $2B
                    analysis["risk_factors"].append("Mid cap company (moderate risk)")
                    analysis["risk_level"] = "MEDIUM"
            except:
                analysis["risk_factors"].append("Market cap data unavailable")
            
            # PE ratio analysis
            try:
                if pe_ratio != "N/A" and pe_ratio != "-":
                    pe_value = float(pe_ratio)
                    if pe_value > 30:
                        analysis["risk_factors"].append("High P/E ratio (potentially overvalued)")
                    elif pe_value < 0:
                        analysis["risk_factors"].append("Negative P/E ratio (company losing money)")
                        analysis["financial_health"] = "POOR"
            except:
                pass
            
            # Sector risk assessment
            high_risk_sectors = ["Biotechnology", "Cryptocurrency", "Cannabis"]
            if sector in high_risk_sectors:
                analysis["risk_factors"].append(f"High-risk sector: {sector}")
                analysis["risk_level"] = "HIGH"
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Company analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_symbol_search(self, matches: List[Dict], keywords: str) -> Dict:
        """Analyze symbol search results"""
        try:
            analysis = {
                "total_matches": len(matches),
                "exact_matches": 0,
                "regions": [],
                "match_types": []
            }
            
            for match in matches:
                name = match.get("2. name", "").lower()
                region = match.get("4. region", "")
                match_type = match.get("3. type", "")
                
                # Check for exact name matches
                if keywords.lower() in name:
                    analysis["exact_matches"] += 1
                
                # Collect regions and types
                if region and region not in analysis["regions"]:
                    analysis["regions"].append(region)
                
                if match_type and match_type not in analysis["match_types"]:
                    analysis["match_types"].append(match_type)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Symbol search analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_forex_rate(self, rate_data: Dict, from_currency: str, to_currency: str) -> Dict:
        """Analyze forex rate data"""
        try:
            analysis = {
                "exchange_rate": 0.0,
                "bid_price": 0.0,
                "ask_price": 0.0,
                "spread": 0.0,
                "risk_indicators": []
            }
            
            # Extract rate data
            rate = float(rate_data.get("5. Exchange Rate", 0))
            bid = float(rate_data.get("8. Bid Price", 0))
            ask = float(rate_data.get("9. Ask Price", 0))
            
            analysis["exchange_rate"] = rate
            analysis["bid_price"] = bid
            analysis["ask_price"] = ask
            
            # Calculate spread
            if bid > 0 and ask > 0:
                spread = ((ask - bid) / bid) * 100
                analysis["spread"] = spread
                
                if spread > 1.0:
                    analysis["risk_indicators"].append("High spread (>1%)")
                elif spread > 0.5:
                    analysis["risk_indicators"].append("Moderate spread (>0.5%)")
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Forex analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_crypto_quote(self, rate_data: Dict, symbol: str, market: str) -> Dict:
        """Analyze cryptocurrency quote data"""
        try:
            analysis = {
                "price": 0.0,
                "bid_price": 0.0,
                "ask_price": 0.0,
                "volatility_risk": "UNKNOWN",
                "risk_indicators": []
            }
            
            # Extract crypto data
            price = float(rate_data.get("5. Exchange Rate", 0))
            bid = float(rate_data.get("8. Bid Price", 0))
            ask = float(rate_data.get("9. Ask Price", 0))
            
            analysis["price"] = price
            analysis["bid_price"] = bid
            analysis["ask_price"] = ask
            
            # Crypto-specific risk assessment
            analysis["risk_indicators"].append("Cryptocurrency - high volatility asset")
            analysis["volatility_risk"] = "HIGH"
            
            # Calculate spread
            if bid > 0 and ask > 0:
                spread = ((ask - bid) / bid) * 100
                if spread > 2.0:
                    analysis["risk_indicators"].append("Very high spread (>2%)")
                elif spread > 1.0:
                    analysis["risk_indicators"].append("High spread (>1%)")
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Crypto analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_comprehensive_financial_results(self, results: Dict, target_data: Dict) -> Dict:
        """Analyze comprehensive financial investigation results"""
        try:
            analysis = {
                "overall_risk_level": "LOW",
                "financial_risk_factors": [],
                "market_indicators": [],
                "compliance_flags": [],
                "recommendations": []
            }
            
            # Analyze individual results
            for result_type, result in results.items():
                if isinstance(result, dict) and not result.get("error"):
                    result_analysis = result.get("analysis", {})
                    
                    # Extract risk factors
                    risk_factors = result_analysis.get("risk_factors", [])
                    risk_indicators = result_analysis.get("risk_indicators", [])
                    
                    analysis["financial_risk_factors"].extend(risk_factors)
                    analysis["financial_risk_factors"].extend(risk_indicators)
                    
                    # Assess overall risk level
                    risk_level = result_analysis.get("risk_level", "LOW")
                    if risk_level == "HIGH":
                        analysis["overall_risk_level"] = "HIGH"
                    elif risk_level == "MEDIUM" and analysis["overall_risk_level"] == "LOW":
                        analysis["overall_risk_level"] = "MEDIUM"
            
            # Generate recommendations
            if analysis["overall_risk_level"] == "HIGH":
                analysis["recommendations"].append("Enhanced due diligence required")
                analysis["recommendations"].append("Consider additional financial verification")
            elif analysis["overall_risk_level"] == "MEDIUM":
                analysis["recommendations"].append("Monitor financial indicators")
                analysis["recommendations"].append("Verify company financial health")
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Comprehensive financial analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def get_api_status(self) -> Dict:
        """Get current API usage status"""
        return {
            "api_name": "Alpha Vantage",
            "requests_made": self.requests_made,
            "requests_today": self.requests_today,
            "daily_limit": self.daily_limit,
            "remaining_requests": self.daily_limit - self.requests_today,
            "total_cost": round(self.total_cost, 2),
            "status": "active" if self.api_key else "inactive"
        }

# Test function
async def test_alphavantage_integration():
    """Test Alpha Vantage API integration"""
    async with AlphaVantageIntegration() as api:
        print("Testing Alpha Vantage API integration...")
        
        # Test stock quote
        stock_result = await api.get_stock_quote("AAPL")
        print(f"Stock quote result: {json.dumps(stock_result, indent=2)}")
        
        # Test company overview
        company_result = await api.get_company_overview("AAPL")
        print(f"Company overview: {json.dumps(company_result, indent=2)}")
        
        # Test symbol search
        search_result = await api.search_symbol("Apple")
        print(f"Symbol search: {json.dumps(search_result, indent=2)}")
        
        # Test forex rate
        forex_result = await api.get_forex_rate("USD", "EUR")
        print(f"Forex rate: {json.dumps(forex_result, indent=2)}")
        
        # Test comprehensive investigation
        target_data = {
            "company_name": "Apple",
            "stock_symbol": "AAPL",
            "currency_from": "USD",
            "currency_to": "EUR"
        }
        comprehensive_result = await api.comprehensive_financial_investigation(target_data)
        print(f"Comprehensive investigation: {json.dumps(comprehensive_result, indent=2)}")
        
        # Print API status
        status = api.get_api_status()
        print(f"API Status: {json.dumps(status, indent=2)}")

if __name__ == "__main__":
    asyncio.run(test_alphavantage_integration())

