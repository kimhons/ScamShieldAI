#!/usr/bin/env python3
"""
Test script for Companies House API integration
"""

import asyncio
import sys
import os

# Add the backend source to Python path
sys.path.append('/home/ubuntu/scamshield-ai-platform/backend/src')

from api_integration.companies_house_integration import CompaniesHouseIntegration

async def test_companies_house_api():
    """Test Companies House API with the provided key"""
    
    print("🏢 Testing Companies House API Integration for ScamShield AI")
    print("=" * 60)
    
    try:
        async with CompaniesHouseIntegration() as api:
            
            # Test 1: Company search
            print("\n🔍 Test 1: Company Search (Apple)")
            print("-" * 40)
            search_result = await api.search_companies("Apple", items_per_page=5)
            
            if "error" in search_result:
                print(f"❌ Company search failed: {search_result['error']}")
            else:
                print(f"✅ Company search successful!")
                analysis = search_result.get('analysis', {})
                print(f"   Total results: {search_result.get('total_results', 0)}")
                print(f"   Exact matches: {analysis.get('exact_matches', 0)}")
                print(f"   Active companies: {analysis.get('active_companies', 0)}")
                print(f"   Dissolved companies: {analysis.get('dissolved_companies', 0)}")
                
                # Show first few companies
                for i, company in enumerate(search_result.get('items', [])[:3]):
                    print(f"   Company {i+1}: {company.get('title', 'N/A')} ({company.get('company_number', 'N/A')})")
            
            # Test 2: Company profile (using Marks & Spencer as a known UK company)
            print("\n🏢 Test 2: Company Profile (Marks & Spencer - 00006245)")
            print("-" * 40)
            profile_result = await api.get_company_profile("00006245")
            
            if "error" in profile_result:
                print(f"❌ Company profile failed: {profile_result['error']}")
            else:
                print(f"✅ Company profile successful!")
                company_data = profile_result.get('company_data', {})
                analysis = profile_result.get('analysis', {})
                print(f"   Company: {company_data.get('company_name', 'N/A')}")
                print(f"   Status: {analysis.get('company_status', 'N/A')}")
                print(f"   Type: {analysis.get('company_type', 'N/A')}")
                print(f"   Incorporation: {analysis.get('incorporation_date', 'N/A')}")
                print(f"   Risk Level: {analysis.get('risk_level', 'N/A')}")
                print(f"   Risk Factors: {len(analysis.get('risk_factors', []))}")
            
            # Test 3: Company officers
            print("\n👥 Test 3: Company Officers (Marks & Spencer)")
            print("-" * 40)
            officers_result = await api.get_company_officers("00006245")
            
            if "error" in officers_result:
                print(f"❌ Company officers failed: {officers_result['error']}")
            else:
                print(f"✅ Company officers successful!")
                analysis = officers_result.get('analysis', {})
                print(f"   Total officers: {analysis.get('total_officers', 0)}")
                print(f"   Active officers: {analysis.get('active_officers', 0)}")
                print(f"   Directors: {analysis.get('director_count', 0)}")
                print(f"   Secretaries: {analysis.get('secretary_count', 0)}")
                print(f"   Risk factors: {len(analysis.get('risk_factors', []))}")
            
            # Test 4: Filing history
            print("\n📄 Test 4: Filing History (Marks & Spencer)")
            print("-" * 40)
            filing_result = await api.get_company_filing_history("00006245")
            
            if "error" in filing_result:
                print(f"❌ Filing history failed: {filing_result['error']}")
            else:
                print(f"✅ Filing history successful!")
                analysis = filing_result.get('analysis', {})
                print(f"   Total filings: {analysis.get('total_filings', 0)}")
                print(f"   Recent filings: {analysis.get('recent_filings', 0)}")
                print(f"   Compliance status: {analysis.get('compliance_status', 'N/A')}")
                print(f"   Risk factors: {len(analysis.get('risk_factors', []))}")
            
            # Test 5: Officer search
            print("\n👤 Test 5: Officer Search (John Smith)")
            print("-" * 40)
            officer_search_result = await api.search_officers("John Smith", items_per_page=5)
            
            if "error" in officer_search_result:
                print(f"❌ Officer search failed: {officer_search_result['error']}")
            else:
                print(f"✅ Officer search successful!")
                analysis = officer_search_result.get('analysis', {})
                print(f"   Total matches: {officer_search_result.get('total_results', 0)}")
                print(f"   Active appointments: {analysis.get('active_appointments', 0)}")
                print(f"   Resigned appointments: {analysis.get('resigned_appointments', 0)}")
                print(f"   Companies involved: {len(analysis.get('companies_involved', []))}")
            
            # Test 6: Comprehensive company investigation
            print("\n🔍 Test 6: Comprehensive Company Investigation")
            print("-" * 40)
            target_data = {
                "company_name": "Apple",
                "company_number": "00006245"
            }
            
            comprehensive_result = await api.comprehensive_company_investigation(target_data)
            
            if "error" in comprehensive_result:
                print(f"❌ Comprehensive investigation failed: {comprehensive_result['error']}")
            else:
                print(f"✅ Comprehensive investigation successful!")
                analysis = comprehensive_result.get('comprehensive_analysis', {})
                print(f"   Overall Risk Level: {analysis.get('overall_risk_level', 'N/A')}")
                print(f"   Legitimacy Score: {analysis.get('legitimacy_score', 0):.2f}")
                print(f"   Corporate Risk Factors: {len(analysis.get('corporate_risk_factors', []))}")
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
            print(f"   Rate limit: {status['rate_limit']} per {status['rate_window_minutes']} minutes")
            print(f"   Total cost: £{status['total_cost']}")
            print(f"   Status: {status['status']}")
            
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("🎯 Companies House API Integration Test Complete!")

if __name__ == "__main__":
    asyncio.run(test_companies_house_api())

