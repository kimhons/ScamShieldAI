#!/usr/bin/env python3
"""
Test script for OpenSanctions API integration
"""

import asyncio
import sys
import os

# Add the backend source to Python path
sys.path.append('/home/ubuntu/scamshield-ai-platform/backend/src')

from api_integration.opensanctions_integration import OpenSanctionsIntegration

async def test_opensanctions_api():
    """Test OpenSanctions API with the provided key"""
    
    print("🔍 Testing OpenSanctions API Integration for ScamShield AI")
    print("=" * 60)
    
    try:
        async with OpenSanctionsIntegration() as api:
            
            # Test 1: Basic entity search
            print("\n📋 Test 1: Basic Entity Search")
            print("-" * 30)
            search_result = await api.search_entity("Putin", limit=3)
            
            if "error" in search_result:
                print(f"❌ Search failed: {search_result['error']}")
            else:
                print(f"✅ Search successful!")
                print(f"   Total results: {search_result.get('total_results', 0)}")
                print(f"   API cost: ${search_result.get('api_cost', 0)}")
                
                # Show first result if available
                if search_result.get('results'):
                    first_result = search_result['results'][0]
                    print(f"   First match: {first_result.get('caption', 'N/A')}")
            
            # Test 2: Sanctions check for a known entity
            print("\n🚨 Test 2: Sanctions Check")
            print("-" * 30)
            sanctions_result = await api.check_sanctions("Vladimir Putin", "RU")
            
            if "error" in sanctions_result:
                print(f"❌ Sanctions check failed: {sanctions_result['error']}")
            else:
                print(f"✅ Sanctions check successful!")
                print(f"   Sanctions found: {sanctions_result.get('sanctions_found', False)}")
                print(f"   Risk level: {sanctions_result.get('risk_level', 'UNKNOWN')}")
                print(f"   PEP status: {sanctions_result.get('pep_status', False)}")
                print(f"   Matches found: {len(sanctions_result.get('matches', []))}")
            
            # Test 3: Clean entity check
            print("\n✅ Test 3: Clean Entity Check")
            print("-" * 30)
            clean_result = await api.check_sanctions("John Smith", "US")
            
            if "error" in clean_result:
                print(f"❌ Clean check failed: {clean_result['error']}")
            else:
                print(f"✅ Clean check successful!")
                print(f"   Sanctions found: {clean_result.get('sanctions_found', False)}")
                print(f"   Risk level: {clean_result.get('risk_level', 'UNKNOWN')}")
                print(f"   Matches found: {len(clean_result.get('matches', []))}")
            
            # Test 4: Comprehensive compliance check
            print("\n🔍 Test 4: Comprehensive Compliance Check")
            print("-" * 30)
            target_data = {
                "name": "Vladimir Putin",
                "country": "RU",
                "company": "Russian Federation Government"
            }
            
            comprehensive_result = await api.comprehensive_compliance_check(target_data)
            
            if "error" in comprehensive_result:
                print(f"❌ Comprehensive check failed: {comprehensive_result['error']}")
            else:
                print(f"✅ Comprehensive check successful!")
                analysis = comprehensive_result.get('comprehensive_analysis', {})
                print(f"   Overall risk level: {analysis.get('overall_risk_level', 'UNKNOWN')}")
                print(f"   Compliance status: {analysis.get('compliance_status', 'UNKNOWN')}")
                print(f"   Critical findings: {len(analysis.get('critical_findings', []))}")
                print(f"   Total API cost: ${comprehensive_result.get('total_api_cost', 0)}")
            
            # API Status Summary
            print("\n📊 API Status Summary")
            print("-" * 30)
            status = api.get_api_status()
            print(f"   API Name: {status['api_name']}")
            print(f"   Requests made: {status['requests_made']}")
            print(f"   Total cost: ${status['total_cost']}")
            print(f"   Avg cost per request: ${status['average_cost_per_request']}")
            print(f"   Status: {status['status']}")
            
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("🎯 OpenSanctions API Integration Test Complete!")

if __name__ == "__main__":
    asyncio.run(test_opensanctions_api())

