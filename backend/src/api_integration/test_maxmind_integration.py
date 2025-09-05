#!/usr/bin/env python3
"""
Test script for MaxMind GeoIP2 API integration
"""

import asyncio
import sys
import os

# Add the backend source to Python path
sys.path.append('/home/ubuntu/scamshield-ai-platform/backend/src')

from api_integration.maxmind_integration import MaxMindIntegration

async def test_maxmind_api():
    """Test MaxMind GeoIP2 API with the provided credentials"""
    
    print("🌍 Testing MaxMind GeoIP2 API Integration for ScamShield AI")
    print("=" * 60)
    
    try:
        async with MaxMindIntegration() as api:
            
            # Test IPs for different scenarios
            test_ips = [
                ("8.8.8.8", "Google DNS - US"),
                ("1.1.1.1", "Cloudflare DNS - US"),
                ("208.67.222.222", "OpenDNS - US")
            ]
            
            for ip, description in test_ips:
                print(f"\n🔍 Testing IP: {ip} ({description})")
                print("-" * 50)
                
                # Test 1: City data
                print(f"\n📍 Test 1: City Data for {ip}")
                print("-" * 30)
                city_result = await api.get_city_data(ip)
                
                if "error" in city_result:
                    print(f"❌ City data failed: {city_result['error']}")
                else:
                    print(f"✅ City data successful!")
                    analysis = city_result.get('analysis', {})
                    location = analysis.get('location', {})
                    print(f"   City: {location.get('city', 'N/A')}")
                    print(f"   Country: {location.get('country', 'N/A')} ({location.get('country_code', 'N/A')})")
                    print(f"   Coordinates: {location.get('latitude', 'N/A')}, {location.get('longitude', 'N/A')}")
                    print(f"   Accuracy: {location.get('accuracy_radius', 'N/A')} km")
                    print(f"   Timezone: {analysis.get('timezone', 'N/A')}")
                    print(f"   Risk indicators: {len(analysis.get('risk_indicators', []))}")
                
                # Test 2: Country data
                print(f"\n🌎 Test 2: Country Data for {ip}")
                print("-" * 30)
                country_result = await api.get_country_data(ip)
                
                if "error" in country_result:
                    print(f"❌ Country data failed: {country_result['error']}")
                else:
                    print(f"✅ Country data successful!")
                    analysis = country_result.get('analysis', {})
                    country_info = analysis.get('country_info', {})
                    print(f"   Country: {country_info.get('country', 'N/A')} ({country_info.get('country_code', 'N/A')})")
                    print(f"   Continent: {country_info.get('continent', 'N/A')} ({country_info.get('continent_code', 'N/A')})")
                    print(f"   Risk level: {analysis.get('risk_level', 'N/A')}")
                    print(f"   Risk factors: {len(analysis.get('risk_factors', []))}")
                
                # Test 3: Insights data
                print(f"\n🔒 Test 3: Insights Data for {ip}")
                print("-" * 30)
                insights_result = await api.get_insights_data(ip)
                
                if "error" in insights_result:
                    print(f"❌ Insights data failed: {insights_result['error']}")
                else:
                    print(f"✅ Insights data successful!")
                    analysis = insights_result.get('analysis', {})
                    print(f"   Anonymizer: {analysis.get('anonymizer_status', False)}")
                    print(f"   Hosting provider: {analysis.get('hosting_provider', False)}")
                    print(f"   User type: {analysis.get('user_type', 'N/A')}")
                    print(f"   Risk score: {analysis.get('risk_score', 0)}/100")
                    print(f"   Security indicators: {len(analysis.get('security_indicators', []))}")
                
                # Test 4: Comprehensive investigation
                print(f"\n🔍 Test 4: Comprehensive Investigation for {ip}")
                print("-" * 30)
                comprehensive_result = await api.comprehensive_ip_investigation(ip)
                
                if "error" in comprehensive_result:
                    print(f"❌ Comprehensive investigation failed: {comprehensive_result['error']}")
                else:
                    print(f"✅ Comprehensive investigation successful!")
                    analysis = comprehensive_result.get('comprehensive_analysis', {})
                    location_summary = analysis.get('location_summary', {})
                    security_summary = analysis.get('security_summary', {})
                    
                    print(f"   Overall Risk Level: {analysis.get('overall_risk_level', 'N/A')}")
                    print(f"   Risk Score: {analysis.get('risk_score', 0)}/100")
                    print(f"   Location: {location_summary.get('city', 'N/A')}, {location_summary.get('country', 'N/A')}")
                    print(f"   Anonymizer: {security_summary.get('anonymizer_status', False)}")
                    print(f"   Hosting Provider: {security_summary.get('hosting_provider', False)}")
                    print(f"   Risk Factors: {len(analysis.get('risk_factors', []))}")
                    print(f"   Recommendations: {len(analysis.get('recommendations', []))}")
                    
                    # Show first recommendation
                    recommendations = analysis.get('recommendations', [])
                    if recommendations:
                        print(f"   • {recommendations[0]}")
                
                print("\n" + "=" * 50)
                
                # Only test first IP to avoid rate limits during testing
                break
            
            # API Status Summary
            print("\n📊 API Status Summary")
            print("-" * 40)
            status = api.get_api_status()
            print(f"   API Name: {status['api_name']}")
            print(f"   Account ID: {status['account_id']}")
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
    print("🎯 MaxMind GeoIP2 API Integration Test Complete!")

if __name__ == "__main__":
    asyncio.run(test_maxmind_api())

