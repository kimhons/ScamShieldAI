#!/usr/bin/env python3
"""
Test script for Cloudflare API integration
"""

import asyncio
import sys
import os

# Add the backend source to Python path
sys.path.append('/home/ubuntu/scamshield-ai-platform/backend/src')

from api_integration.cloudflare_integration import CloudflareIntegration

async def test_cloudflare_api():
    """Test Cloudflare API with the provided token"""
    
    print("☁️ Testing Cloudflare API Integration for ScamShield AI")
    print("=" * 60)
    
    try:
        async with CloudflareIntegration() as api:
            
            # Test 1: Token verification
            print("\n🔑 Test 1: Token Verification")
            print("-" * 40)
            verify_result = await api.verify_token()
            
            if "error" in verify_result:
                print(f"❌ Token verification failed: {verify_result['error']}")
                return
            else:
                print(f"✅ Token verification successful!")
                print(f"   Token ID: {verify_result.get('token_id', 'N/A')}")
                print(f"   Status: {verify_result.get('status', 'N/A')}")
                print(f"   Expires: {verify_result.get('expires_on', 'N/A')}")
            
            # Test 2: List zones
            print("\n🌐 Test 2: List Zones")
            print("-" * 40)
            zones_result = await api.list_zones()
            
            if "error" in zones_result:
                print(f"❌ Zone listing failed: {zones_result['error']}")
            else:
                print(f"✅ Zone listing successful!")
                analysis = zones_result.get('analysis', {})
                print(f"   Total zones: {zones_result.get('total_zones', 0)}")
                print(f"   Active zones: {analysis.get('active_zones', 0)}")
                print(f"   Paused zones: {analysis.get('paused_zones', 0)}")
                print(f"   Plan types: {', '.join(analysis.get('plan_types', []))}")
                
                # Show first few zones
                for i, zone in enumerate(zones_result.get('zones', [])[:3]):
                    print(f"   Zone {i+1}: {zone.get('name', 'N/A')} ({zone.get('status', 'N/A')})")
            
            # Test 3: DNS records (if we have zones)
            zones = zones_result.get('zones', [])
            if zones:
                zone = zones[0]
                zone_id = zone['id']
                domain = zone['name']
                
                print(f"\n📋 Test 3: DNS Records ({domain})")
                print("-" * 40)
                dns_result = await api.get_zone_dns_records(zone_id)
                
                if "error" in dns_result:
                    print(f"❌ DNS records failed: {dns_result['error']}")
                else:
                    print(f"✅ DNS records successful!")
                    analysis = dns_result.get('analysis', {})
                    print(f"   Total records: {dns_result.get('total_records', 0)}")
                    print(f"   Record types: {analysis.get('record_types', {})}")
                    print(f"   Security indicators: {len(analysis.get('security_indicators', []))}")
                    print(f"   Suspicious patterns: {len(analysis.get('suspicious_patterns', []))}")
                
                # Test 4: Security settings
                print(f"\n🔒 Test 4: Security Settings ({domain})")
                print("-" * 40)
                security_result = await api.get_zone_security_settings(zone_id)
                
                if "error" in security_result:
                    print(f"❌ Security settings failed: {security_result['error']}")
                else:
                    print(f"✅ Security settings successful!")
                    analysis = security_result.get('analysis', {})
                    print(f"   Security score: {analysis.get('security_score', 0)}/100")
                    print(f"   Security strengths: {len(analysis.get('security_strengths', []))}")
                    print(f"   Security weaknesses: {len(analysis.get('security_weaknesses', []))}")
                    print(f"   Recommendations: {len(analysis.get('recommendations', []))}")
                
                # Test 5: Analytics
                print(f"\n📊 Test 5: Analytics ({domain})")
                print("-" * 40)
                analytics_result = await api.get_zone_analytics(zone_id)
                
                if "error" in analytics_result:
                    print(f"❌ Analytics failed: {analytics_result['error']}")
                else:
                    print(f"✅ Analytics successful!")
                    analysis = analytics_result.get('analysis', {})
                    traffic = analysis.get('traffic_patterns', {})
                    security = analysis.get('security_events', {})
                    print(f"   Total requests: {traffic.get('total_requests', 0):,}")
                    print(f"   Total bandwidth: {traffic.get('total_bandwidth', 0):,}")
                    print(f"   Total threats: {security.get('total_threats', 0):,}")
                    print(f"   Threat ratio: {security.get('threat_ratio', 0):.2f}%")
                
                # Test 6: Comprehensive domain investigation
                print(f"\n🔍 Test 6: Comprehensive Domain Investigation ({domain})")
                print("-" * 40)
                comprehensive_result = await api.comprehensive_domain_investigation(domain)
                
                if "error" in comprehensive_result:
                    print(f"❌ Comprehensive investigation failed: {comprehensive_result['error']}")
                else:
                    print(f"✅ Comprehensive investigation successful!")
                    analysis = comprehensive_result.get('comprehensive_analysis', {})
                    print(f"   Overall Risk Level: {analysis.get('overall_risk_level', 'N/A')}")
                    print(f"   Security Score: {analysis.get('security_score', 0)}/100")
                    print(f"   Risk Factors: {len(analysis.get('risk_factors', []))}")
                    print(f"   Security Strengths: {len(analysis.get('security_strengths', []))}")
                    print(f"   Recommendations: {len(analysis.get('recommendations', []))}")
                    
                    # Show some recommendations
                    for rec in analysis.get('recommendations', [])[:3]:
                        print(f"   • {rec}")
            else:
                print("\n⚠️ No zones found - skipping zone-specific tests")
            
            # API Status Summary
            print("\n📊 API Status Summary")
            print("-" * 40)
            status = api.get_api_status()
            print(f"   API Name: {status['api_name']}")
            print(f"   Requests made: {status['requests_made']}")
            print(f"   Rate limit: {status['rate_limit']} per {status['rate_window_minutes']} minutes")
            print(f"   Total cost: ${status['total_cost']}")
            print(f"   Status: {status['status']}")
            
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("🎯 Cloudflare API Integration Test Complete!")

if __name__ == "__main__":
    asyncio.run(test_cloudflare_api())

