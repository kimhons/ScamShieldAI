#!/usr/bin/env python3
"""
Test script for IPinfo API integration
"""

import asyncio
import sys
import os

# Add the backend source to Python path
sys.path.append('/home/ubuntu/scamshield-ai-platform/backend/src')

from api_integration.ipinfo_integration import IPinfoIntegration

async def test_ipinfo_api():
    """Test IPinfo API with the provided token"""
    
    print("🌐 Testing IPinfo API Integration for ScamShield AI")
    print("=" * 60)
    
    try:
        async with IPinfoIntegration() as api:
            
            # Test IPs for different scenarios
            test_ips = [
                ("8.8.8.8", "Google DNS - US"),
                ("1.1.1.1", "Cloudflare DNS - US")
            ]
            
            for ip, description in test_ips:
                print(f"\n🔍 Testing IP: {ip} ({description})")
                print("-" * 50)
                
                # Test 1: Full IP info
                print(f"\n📍 Test 1: Full IP Info for {ip}")
                print("-" * 30)
                ip_result = await api.get_ip_info(ip)
                
                if "error" in ip_result:
                    print(f"❌ Full IP info failed: {ip_result['error']}")
                else:
                    print(f"✅ Full IP info successful!")
                    analysis = ip_result.get('analysis', {})
                    location = analysis.get('location', {})
                    network = analysis.get('network_info', {})
                    
                    print(f"   IP: {location.get('ip', 'N/A')}")
                    print(f"   Location: {location.get('city', 'N/A')}, {location.get('region', 'N/A')}, {location.get('country', 'N/A')}")
                    print(f"   Coordinates: {location.get('coordinates', 'N/A')}")
                    print(f"   Timezone: {location.get('timezone', 'N/A')}")
                    print(f"   ASN: {network.get('asn', 'N/A')}")
                    print(f"   AS Name: {network.get('as_name', 'N/A')}")
                    print(f"   ISP: {network.get('isp', 'N/A')}")
                    print(f"   Privacy indicators: {len(analysis.get('privacy_indicators', []))}")
                    print(f"   Hosting indicators: {len(analysis.get('hosting_indicators', []))}")
                
                # Test 2: Lite IP info
                print(f"\n🔍 Test 2: Lite IP Info for {ip}")
                print("-" * 30)
                lite_result = await api.get_ip_lite(ip)
                
                if "error" in lite_result:
                    print(f"❌ Lite IP info failed: {lite_result['error']}")
                else:
                    print(f"✅ Lite IP info successful!")
                    analysis = lite_result.get('analysis', {})
                    basic_location = analysis.get('basic_location', {})
                    basic_network = analysis.get('basic_network', {})
                    
                    print(f"   Country: {basic_location.get('country', 'N/A')} ({basic_location.get('country_code', 'N/A')})")
                    print(f"   Continent: {basic_location.get('continent', 'N/A')} ({basic_location.get('continent_code', 'N/A')})")
                    print(f"   ASN: {basic_network.get('asn', 'N/A')}")
                    print(f"   AS Name: {basic_network.get('as_name', 'N/A')}")
                    print(f"   Risk Level: {analysis.get('risk_level', 'N/A')}")
                
                # Test 3: ASN lookup (if available)
                if lite_result.get('analysis', {}).get('basic_network', {}).get('asn'):
                    asn = lite_result['analysis']['basic_network']['asn']
                    print(f"\n🏢 Test 3: ASN Info for {asn}")
                    print("-" * 30)
                    asn_result = await api.get_asn_info(asn)
                    
                    if "error" in asn_result:
                        print(f"❌ ASN info failed: {asn_result['error']}")
                    else:
                        print(f"✅ ASN info successful!")
                        analysis = asn_result.get('analysis', {})
                        asn_info = analysis.get('asn_info', {})
                        
                        print(f"   ASN: {asn_info.get('asn', 'N/A')}")
                        print(f"   Name: {asn_info.get('name', 'N/A')}")
                        print(f"   Domain: {asn_info.get('domain', 'N/A')}")
                        print(f"   Type: {asn_info.get('type', 'N/A')}")
                        print(f"   Network Type: {analysis.get('network_type', 'N/A')}")
                        print(f"   Risk Indicators: {len(analysis.get('risk_indicators', []))}")
                
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
                    network_summary = analysis.get('network_summary', {})
                    security_summary = analysis.get('security_summary', {})
                    
                    print(f"   Overall Risk Level: {analysis.get('overall_risk_level', 'N/A')}")
                    print(f"   Risk Score: {analysis.get('risk_score', 0)}/100")
                    print(f"   Location: {location_summary.get('city', 'N/A')}, {location_summary.get('country', 'N/A')}")
                    print(f"   ASN: {network_summary.get('asn', 'N/A')}")
                    print(f"   Privacy Services: {security_summary.get('privacy_services', False)}")
                    print(f"   Hosting Provider: {security_summary.get('hosting_provider', False)}")
                    print(f"   Anonymization: {security_summary.get('anonymization_detected', False)}")
                    print(f"   Risk Factors: {len(analysis.get('risk_factors', []))}")
                    print(f"   Recommendations: {len(analysis.get('recommendations', []))}")
                    
                    # Show first recommendation
                    recommendations = analysis.get('recommendations', [])
                    if recommendations:
                        print(f"   • {recommendations[0]}")
                
                print("\n" + "=" * 50)
                
                # Only test first IP to avoid rate limits during testing
                break
            
            # Test 5: Batch lookup
            print(f"\n📊 Test 5: Batch IP Lookup")
            print("-" * 30)
            batch_ips = ["8.8.8.8", "1.1.1.1", "208.67.222.222"]
            batch_result = await api.batch_ip_lookup(batch_ips)
            
            if "error" in batch_result:
                print(f"❌ Batch lookup failed: {batch_result['error']}")
            else:
                print(f"✅ Batch lookup successful!")
                batch_analysis = batch_result.get('batch_analysis', {})
                
                print(f"   Total IPs: {batch_analysis.get('total_ips', 0)}")
                print(f"   Successful: {batch_analysis.get('successful_lookups', 0)}")
                print(f"   Failed: {batch_analysis.get('failed_lookups', 0)}")
                print(f"   Countries: {list(batch_analysis.get('country_distribution', {}).keys())}")
                print(f"   Risk Summary: {batch_analysis.get('risk_summary', {})}")
            
            # API Status Summary
            print("\n📊 API Status Summary")
            print("-" * 40)
            status = api.get_api_status()
            print(f"   API Name: {status['api_name']}")
            print(f"   Requests made: {status['requests_made']}")
            print(f"   Requests this month: {status['requests_this_month']}")
            print(f"   Monthly limit: {status['monthly_limit']}")
            print(f"   Remaining requests: {status['remaining_requests']}")
            print(f"   Total cost: ${status['total_cost']}")
            print(f"   Status: {status['status']}")
            
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("🎯 IPinfo API Integration Test Complete!")

if __name__ == "__main__":
    asyncio.run(test_ipinfo_api())

