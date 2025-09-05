#!/usr/bin/env python3
"""
Test script for Alpha Vantage API integration
"""

import asyncio
import sys
import os

# Add the backend source to Python path
sys.path.append('/home/ubuntu/scamshield-ai-platform/backend/src')

from api_integration.alphavantage_integration import AlphaVantageIntegration

async def test_alphavantage_api():
    """Test Alpha Vantage API with the provided key"""
    
    print("💰 Testing Alpha Vantage API Integration for ScamShield AI")
    print("=" * 60)
    
    try:
        async with AlphaVantageIntegration() as api:
            
            # Test 1: Stock quote lookup
            print("\n📈 Test 1: Stock Quote Lookup (AAPL)")
            print("-" * 40)
            stock_result = await api.get_stock_quote("AAPL")
            
            if "error" in stock_result:
                print(f"❌ Stock quote failed: {stock_result['error']}")
            else:
                print(f"✅ Stock quote successful!")
                quote_data = stock_result.get('quote_data', {})
                analysis = stock_result.get('analysis', {})
                print(f"   Symbol: AAPL")
                print(f"   Current Price: ${analysis.get('current_price', 'N/A')}")
                print(f"   Change %: {analysis.get('change_percent', 'N/A')}%")
                print(f"   Volume: {analysis.get('volume', 'N/A'):,}")
                print(f"   Market Status: {analysis.get('market_status', 'N/A')}")
            
            # Test 2: Company overview
            print("\n🏢 Test 2: Company Overview (AAPL)")
            print("-" * 40)
            company_result = await api.get_company_overview("AAPL")
            
            if "error" in company_result:
                print(f"❌ Company overview failed: {company_result['error']}")
            else:
                print(f"✅ Company overview successful!")
                company_data = company_result.get('company_data', {})
                analysis = company_result.get('analysis', {})
                print(f"   Company: {company_data.get('Name', 'N/A')}")
                print(f"   Sector: {analysis.get('sector', 'N/A')}")
                print(f"   Market Cap: ${analysis.get('market_cap', 'N/A'):,}")
                print(f"   Risk Level: {analysis.get('risk_level', 'N/A')}")
                print(f"   Risk Factors: {len(analysis.get('risk_factors', []))}")
            
            # Test 3: Symbol search
            print("\n🔍 Test 3: Symbol Search (Apple)")
            print("-" * 40)
            search_result = await api.search_symbol("Apple")
            
            if "error" in search_result:
                print(f"❌ Symbol search failed: {search_result['error']}")
            else:
                print(f"✅ Symbol search successful!")
                matches = search_result.get('matches', [])
                analysis = search_result.get('analysis', {})
                print(f"   Total matches: {analysis.get('total_matches', 0)}")
                print(f"   Exact matches: {analysis.get('exact_matches', 0)}")
                print(f"   Regions: {', '.join(analysis.get('regions', []))}")
                
                # Show first few matches
                for i, match in enumerate(matches[:3]):
                    print(f"   Match {i+1}: {match.get('1. symbol', 'N/A')} - {match.get('2. name', 'N/A')}")
            
            # Test 4: Forex rate
            print("\n💱 Test 4: Forex Rate (USD to EUR)")
            print("-" * 40)
            forex_result = await api.get_forex_rate("USD", "EUR")
            
            if "error" in forex_result:
                print(f"❌ Forex rate failed: {forex_result['error']}")
            else:
                print(f"✅ Forex rate successful!")
                rate_data = forex_result.get('rate_data', {})
                analysis = forex_result.get('analysis', {})
                print(f"   Exchange Rate: {analysis.get('exchange_rate', 'N/A')}")
                print(f"   Bid Price: {analysis.get('bid_price', 'N/A')}")
                print(f"   Ask Price: {analysis.get('ask_price', 'N/A')}")
                print(f"   Spread: {analysis.get('spread', 'N/A'):.4f}%")
            
            # Test 5: Crypto quote
            print("\n₿ Test 5: Crypto Quote (BTC to USD)")
            print("-" * 40)
            crypto_result = await api.get_crypto_quote("BTC", "USD")
            
            if "error" in crypto_result:
                print(f"❌ Crypto quote failed: {crypto_result['error']}")
            else:
                print(f"✅ Crypto quote successful!")
                rate_data = crypto_result.get('rate_data', {})
                analysis = crypto_result.get('analysis', {})
                print(f"   BTC Price: ${analysis.get('price', 'N/A'):,.2f}")
                print(f"   Volatility Risk: {analysis.get('volatility_risk', 'N/A')}")
                print(f"   Risk Indicators: {len(analysis.get('risk_indicators', []))}")
            
            # Test 6: Comprehensive financial investigation
            print("\n🔍 Test 6: Comprehensive Financial Investigation")
            print("-" * 40)
            target_data = {
                "company_name": "Apple",
                "stock_symbol": "AAPL",
                "currency_from": "USD",
                "currency_to": "EUR"
            }
            
            comprehensive_result = await api.comprehensive_financial_investigation(target_data)
            
            if "error" in comprehensive_result:
                print(f"❌ Comprehensive investigation failed: {comprehensive_result['error']}")
            else:
                print(f"✅ Comprehensive investigation successful!")
                analysis = comprehensive_result.get('comprehensive_analysis', {})
                print(f"   Overall Risk Level: {analysis.get('overall_risk_level', 'N/A')}")
                print(f"   Financial Risk Factors: {len(analysis.get('financial_risk_factors', []))}")
                print(f"   Recommendations: {len(analysis.get('recommendations', []))}")
                
                # Show recommendations
                for rec in analysis.get('recommendations', [])[:2]:
                    print(f"   • {rec}")
            
            # API Status Summary
            print("\n📊 API Status Summary")
            print("-" * 40)
            status = api.get_api_status()
            print(f"   API Name: {status['api_name']}")
            print(f"   Requests made: {status['requests_made']}")
            print(f"   Requests today: {status['requests_today']}")
            print(f"   Daily limit: {status['daily_limit']}")
            print(f"   Remaining requests: {status['remaining_requests']}")
            print(f"   Total cost: ${status['total_cost']}")
            print(f"   Status: {status['status']}")
            
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("🎯 Alpha Vantage API Integration Test Complete!")

if __name__ == "__main__":
    asyncio.run(test_alphavantage_api())

