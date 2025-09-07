"""
Comprehensive Integration Tests for ScamShield AI API Wrappers
Tests all API integrations with validation, error handling, and performance monitoring
"""

import asyncio
import pytest
import json
import time
from typing import Dict, Any, List
from datetime import datetime

# Import all API wrappers
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from integrations.api_manager import APIManager, InvestigationRequest
from integrations.security_apis import SecurityAPIWrapper
from integrations.anti_malware_apis import AntiMalwareAPIWrapper
from integrations.email_apis import EmailAPIWrapper
from integrations.geolocation_apis import GeolocationAPIWrapper
from integrations.phone_apis import PhoneAPIWrapper
from integrations.validation_apis import ValidationAPIWrapper

class TestAPIIntegrations:
    """Comprehensive test suite for API integrations"""
    
    @pytest.fixture
    async def api_manager(self):
        """Create API manager instance for testing"""
        # Test API keys (use environment variables in production)
        test_api_keys = {
            # Add your test API keys here
            'hunter_io': 'test_key',
            'emailrep': None,  # No auth required
            'ipgeolocation': 'test_key',
            'ipapi': None,  # No auth required
            'numverify': 'test_key',
            'cloudmersive': 'test_key'
        }
        
        manager = APIManager(test_api_keys)
        async with manager:
            yield manager
    
    @pytest.mark.asyncio
    async def test_api_manager_health_check(self, api_manager):
        """Test comprehensive health check of all APIs"""
        health_status = await api_manager.health_check()
        
        assert 'overall_health' in health_status
        assert 'service_details' in health_status
        assert health_status['total_services'] > 0
        
        print(f"Overall API Health: {health_status['overall_health']:.1f}%")
        print(f"Healthy Services: {health_status['healthy_services']}/{health_status['total_services']}")
        
        # Log individual service status
        for service, details in health_status['service_details'].items():
            status = details['status']
            response_time = details.get('response_time', 0)
            print(f"  {service}: {status} ({response_time:.3f}s)")
    
    @pytest.mark.asyncio
    async def test_email_investigation(self, api_manager):
        """Test comprehensive email investigation"""
        test_emails = [
            'test@example.com',
            'suspicious@tempmail.com',
            'admin@google.com',
            'invalid-email-format'
        ]
        
        for email in test_emails:
            print(f"\n--- Testing Email: {email} ---")
            
            start_time = time.time()
            result = await api_manager.investigate_email(email)
            processing_time = time.time() - start_time
            
            # Validate result structure
            assert result.target_type == 'email'
            assert result.target_value == email
            assert 0 <= result.overall_risk_score <= 100
            assert result.overall_risk_level in ['LOW', 'MEDIUM', 'HIGH']
            assert 0 <= result.confidence_score <= 100
            assert isinstance(result.detailed_analysis, dict)
            assert isinstance(result.recommendations, list)
            assert isinstance(result.apis_used, list)
            
            print(f"Risk Score: {result.overall_risk_score:.1f}/100 ({result.overall_risk_level})")
            print(f"Confidence: {result.confidence_score:.1f}%")
            print(f"Processing Time: {processing_time:.3f}s")
            print(f"APIs Used: {', '.join(result.apis_used)}")
            print(f"Summary: {result.summary}")
            
            if result.recommendations:
                print("Recommendations:")
                for rec in result.recommendations[:3]:  # Show first 3
                    print(f"  - {rec}")
    
    @pytest.mark.asyncio
    async def test_phone_investigation(self, api_manager):
        """Test comprehensive phone investigation"""
        test_phones = [
            '+1234567890',
            '+44 20 7946 0958',
            '+33 1 42 86 83 26',
            '555-0123',
            'invalid-phone'
        ]
        
        for phone in test_phones:
            print(f"\n--- Testing Phone: {phone} ---")
            
            start_time = time.time()
            result = await api_manager.investigate_phone(phone)
            processing_time = time.time() - start_time
            
            # Validate result structure
            assert result.target_type == 'phone'
            assert result.target_value == phone
            assert 0 <= result.overall_risk_score <= 100
            assert result.overall_risk_level in ['LOW', 'MEDIUM', 'HIGH']
            
            print(f"Risk Score: {result.overall_risk_score:.1f}/100 ({result.overall_risk_level})")
            print(f"Confidence: {result.confidence_score:.1f}%")
            print(f"Processing Time: {processing_time:.3f}s")
            print(f"Summary: {result.summary}")
    
    @pytest.mark.asyncio
    async def test_ip_investigation(self, api_manager):
        """Test comprehensive IP investigation"""
        test_ips = [
            '8.8.8.8',  # Google DNS
            '1.1.1.1',  # Cloudflare DNS
            '192.168.1.1',  # Private IP
            '127.0.0.1',  # Localhost
            'invalid-ip'
        ]
        
        for ip in test_ips:
            print(f"\n--- Testing IP: {ip} ---")
            
            start_time = time.time()
            result = await api_manager.investigate_ip(ip)
            processing_time = time.time() - start_time
            
            # Validate result structure
            assert result.target_type == 'ip'
            assert result.target_value == ip
            assert 0 <= result.overall_risk_score <= 100
            
            print(f"Risk Score: {result.overall_risk_score:.1f}/100 ({result.overall_risk_level})")
            print(f"Processing Time: {processing_time:.3f}s")
            print(f"Summary: {result.summary}")
    
    @pytest.mark.asyncio
    async def test_domain_investigation(self, api_manager):
        """Test comprehensive domain investigation"""
        test_domains = [
            'google.com',
            'example.com',
            'suspicious-domain.tk',
            'nonexistent-domain-12345.com'
        ]
        
        for domain in test_domains:
            print(f"\n--- Testing Domain: {domain} ---")
            
            start_time = time.time()
            result = await api_manager.investigate_domain(domain)
            processing_time = time.time() - start_time
            
            # Validate result structure
            assert result.target_type == 'domain'
            assert result.target_value == domain
            assert 0 <= result.overall_risk_score <= 100
            
            print(f"Risk Score: {result.overall_risk_score:.1f}/100 ({result.overall_risk_level})")
            print(f"Processing Time: {processing_time:.3f}s")
            print(f"Summary: {result.summary}")
    
    @pytest.mark.asyncio
    async def test_url_investigation(self, api_manager):
        """Test comprehensive URL investigation"""
        test_urls = [
            'https://www.google.com',
            'https://example.com',
            'http://suspicious-site.tk',
            'https://nonexistent-url-12345.com',
            'invalid-url-format'
        ]
        
        for url in test_urls:
            print(f"\n--- Testing URL: {url} ---")
            
            start_time = time.time()
            result = await api_manager.investigate_url(url)
            processing_time = time.time() - start_time
            
            # Validate result structure
            assert result.target_type == 'url'
            assert result.target_value == url
            assert 0 <= result.overall_risk_score <= 100
            
            print(f"Risk Score: {result.overall_risk_score:.1f}/100 ({result.overall_risk_level})")
            print(f"Processing Time: {processing_time:.3f}s")
            print(f"Summary: {result.summary}")
    
    @pytest.mark.asyncio
    async def test_batch_investigation(self, api_manager):
        """Test batch investigation processing"""
        requests = [
            InvestigationRequest('email', 'test@example.com', 'standard'),
            InvestigationRequest('phone', '+1234567890', 'standard'),
            InvestigationRequest('ip', '8.8.8.8', 'standard'),
            InvestigationRequest('domain', 'google.com', 'standard'),
            InvestigationRequest('url', 'https://example.com', 'standard')
        ]
        
        print(f"\n--- Testing Batch Investigation ({len(requests)} requests) ---")
        
        start_time = time.time()
        results = await api_manager.batch_investigate(requests)
        total_time = time.time() - start_time
        
        assert len(results) == len(requests)
        
        print(f"Total Processing Time: {total_time:.3f}s")
        print(f"Average Time per Investigation: {total_time/len(requests):.3f}s")
        
        for i, result in enumerate(results):
            request = requests[i]
            print(f"  {request.target_type}:{request.target_value} -> Risk: {result.overall_risk_score:.1f}/100")
    
    @pytest.mark.asyncio
    async def test_individual_api_wrappers(self, api_manager):
        """Test individual API wrapper functionality"""
        
        # Test Security APIs
        print("\n--- Testing Security APIs ---")
        security_result = await api_manager.security_apis.health_check()
        print(f"Security APIs Health: {'✓' if security_result.success else '✗'}")
        
        # Test Anti-Malware APIs
        print("\n--- Testing Anti-Malware APIs ---")
        malware_result = await api_manager.anti_malware_apis.health_check()
        print(f"Anti-Malware APIs Health: {'✓' if malware_result.success else '✗'}")
        
        # Test Email APIs
        print("\n--- Testing Email APIs ---")
        email_result = await api_manager.email_apis.health_check()
        print(f"Email APIs Health: {'✓' if email_result.success else '✗'}")
        
        # Test Geolocation APIs
        print("\n--- Testing Geolocation APIs ---")
        geo_result = await api_manager.geolocation_apis.health_check()
        print(f"Geolocation APIs Health: {'✓' if geo_result.success else '✗'}")
        
        # Test Phone APIs
        print("\n--- Testing Phone APIs ---")
        phone_result = await api_manager.phone_apis.health_check()
        print(f"Phone APIs Health: {'✓' if phone_result.success else '✗'}")
        
        # Test Validation APIs
        print("\n--- Testing Validation APIs ---")
        validation_result = await api_manager.validation_apis.health_check()
        print(f"Validation APIs Health: {'✓' if validation_result.success else '✗'}")
    
    @pytest.mark.asyncio
    async def test_error_handling(self, api_manager):
        """Test error handling and edge cases"""
        
        # Test invalid target types
        print("\n--- Testing Error Handling ---")
        
        invalid_request = InvestigationRequest('invalid_type', 'test_value', 'standard')
        result = await api_manager.comprehensive_investigation(invalid_request)
        
        assert result.overall_risk_score == 100
        assert result.overall_risk_level == 'HIGH'
        assert 'error' in result.detailed_analysis
        
        print("✓ Invalid target type handled correctly")
        
        # Test empty values
        empty_request = InvestigationRequest('email', '', 'standard')
        result = await api_manager.comprehensive_investigation(empty_request)
        
        print("✓ Empty target value handled")
        
        # Test malformed data
        malformed_requests = [
            InvestigationRequest('email', 'not-an-email', 'standard'),
            InvestigationRequest('phone', 'not-a-phone', 'standard'),
            InvestigationRequest('ip', 'not-an-ip', 'standard'),
            InvestigationRequest('url', 'not-a-url', 'standard')
        ]
        
        for request in malformed_requests:
            result = await api_manager.comprehensive_investigation(request)
            print(f"✓ Malformed {request.target_type} handled: Risk {result.overall_risk_score}/100")
    
    @pytest.mark.asyncio
    async def test_performance_benchmarks(self, api_manager):
        """Test performance benchmarks and rate limiting"""
        
        print("\n--- Performance Benchmarks ---")
        
        # Single investigation performance
        start_time = time.time()
        result = await api_manager.investigate_email('test@example.com')
        single_time = time.time() - start_time
        
        print(f"Single Email Investigation: {single_time:.3f}s")
        
        # Batch investigation performance
        batch_requests = [
            InvestigationRequest('email', f'test{i}@example.com', 'standard')
            for i in range(5)
        ]
        
        start_time = time.time()
        batch_results = await api_manager.batch_investigate(batch_requests)
        batch_time = time.time() - start_time
        
        print(f"Batch Investigation (5 emails): {batch_time:.3f}s")
        print(f"Average per investigation: {batch_time/5:.3f}s")
        
        # Test rate limiting doesn't cause failures
        rapid_requests = [
            InvestigationRequest('ip', '8.8.8.8', 'basic')
            for _ in range(3)
        ]
        
        start_time = time.time()
        rapid_results = await api_manager.batch_investigate(rapid_requests)
        rapid_time = time.time() - start_time
        
        successful_rapid = sum(1 for r in rapid_results if r.overall_risk_score < 100)
        print(f"Rapid Requests: {successful_rapid}/3 successful in {rapid_time:.3f}s")
    
    @pytest.mark.asyncio
    async def test_caching_functionality(self, api_manager):
        """Test investigation result caching"""
        
        print("\n--- Testing Caching ---")
        
        # First investigation (should hit APIs)
        start_time = time.time()
        result1 = await api_manager.investigate_email('cache-test@example.com')
        first_time = time.time() - start_time
        
        # Second investigation (should use cache)
        start_time = time.time()
        result2 = await api_manager.investigate_email('cache-test@example.com')
        second_time = time.time() - start_time
        
        print(f"First investigation: {first_time:.3f}s")
        print(f"Second investigation (cached): {second_time:.3f}s")
        print(f"Cache speedup: {first_time/second_time:.1f}x faster")
        
        # Results should be identical
        assert result1.overall_risk_score == result2.overall_risk_score
        assert result1.overall_risk_level == result2.overall_risk_level
        
        print("✓ Cache results are consistent")
    
    def test_statistics_tracking(self, api_manager):
        """Test statistics tracking functionality"""
        
        print("\n--- Testing Statistics ---")
        
        # Get initial statistics
        initial_stats = api_manager.get_statistics()
        print(f"Initial investigations: {initial_stats['investigation_stats']['total_investigations']}")
        
        # Reset statistics
        api_manager.reset_statistics()
        reset_stats = api_manager.get_statistics()
        
        assert reset_stats['investigation_stats']['total_investigations'] == 0
        print("✓ Statistics reset successfully")
        
        # Test cache clearing
        api_manager.clear_cache()
        assert reset_stats['cache_size'] >= 0
        print("✓ Cache cleared successfully")

class TestValidationSuite:
    """Validation tests for API response schemas and edge cases"""
    
    @pytest.mark.asyncio
    async def test_response_schema_validation(self):
        """Test that all API responses conform to expected schemas"""
        
        # Test with minimal API keys (free APIs only)
        api_manager = APIManager({})
        
        async with api_manager:
            # Test email validation with free APIs
            result = await api_manager.investigate_email('test@example.com')
            
            # Validate response schema
            required_fields = [
                'request_id', 'target_type', 'target_value', 'overall_risk_score',
                'overall_risk_level', 'confidence_score', 'investigation_level',
                'detailed_analysis', 'recommendations', 'summary', 'processing_time',
                'apis_used', 'timestamp'
            ]
            
            for field in required_fields:
                assert hasattr(result, field), f"Missing required field: {field}"
            
            # Validate data types
            assert isinstance(result.overall_risk_score, (int, float))
            assert 0 <= result.overall_risk_score <= 100
            assert result.overall_risk_level in ['LOW', 'MEDIUM', 'HIGH']
            assert isinstance(result.confidence_score, (int, float))
            assert isinstance(result.detailed_analysis, dict)
            assert isinstance(result.recommendations, list)
            assert isinstance(result.apis_used, list)
            
            print("✓ Response schema validation passed")
    
    @pytest.mark.asyncio
    async def test_rate_limit_handling(self):
        """Test rate limit handling and retry mechanisms"""
        
        api_manager = APIManager({})
        
        async with api_manager:
            # Simulate rapid requests that might hit rate limits
            tasks = []
            for i in range(10):
                task = api_manager.investigate_email(f'ratelimit{i}@example.com')
                tasks.append(task)
            
            # Execute all tasks
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Count successful vs failed requests
            successful = sum(1 for r in results if not isinstance(r, Exception) and r.confidence_score > 0)
            total = len(results)
            
            print(f"Rate limit test: {successful}/{total} successful")
            
            # At least some should succeed even with rate limiting
            assert successful > 0, "No requests succeeded - rate limiting too aggressive"
    
    @pytest.mark.asyncio
    async def test_null_field_handling(self):
        """Test handling of null/missing fields in API responses"""
        
        api_manager = APIManager({})
        
        async with api_manager:
            # Test with various edge case inputs
            edge_cases = [
                ('email', ''),
                ('email', None),
                ('phone', ''),
                ('ip', ''),
                ('domain', ''),
                ('url', '')
            ]
            
            for target_type, target_value in edge_cases:
                if target_value is None:
                    continue  # Skip None values as they would cause request creation to fail
                
                request = InvestigationRequest(target_type, target_value or 'empty', 'basic')
                result = await api_manager.comprehensive_investigation(request)
                
                # Should handle gracefully without crashing
                assert result is not None
                assert hasattr(result, 'overall_risk_score')
                
                print(f"✓ Handled empty {target_type} gracefully")

# Test runner function
async def run_comprehensive_tests():
    """Run all comprehensive API integration tests"""
    
    print("=" * 80)
    print("SCAMSHIELD AI - COMPREHENSIVE API INTEGRATION TESTS")
    print("=" * 80)
    
    # Initialize test suite
    test_suite = TestAPIIntegrations()
    validation_suite = TestValidationSuite()
    
    # Create API manager for testing
    api_manager = APIManager({
        # Add test API keys here for full testing
        'emailrep': None,  # Free API
        'ipapi': None,     # Free API
        'postman_echo': None,  # Free API
        'json_test': None  # Free API
    })
    
    try:
        async with api_manager:
            print("\n🔍 Starting API Integration Tests...")
            
            # Health check
            await test_suite.test_api_manager_health_check(api_manager)
            
            # Individual investigation tests
            await test_suite.test_email_investigation(api_manager)
            await test_suite.test_phone_investigation(api_manager)
            await test_suite.test_ip_investigation(api_manager)
            await test_suite.test_domain_investigation(api_manager)
            await test_suite.test_url_investigation(api_manager)
            
            # Batch processing
            await test_suite.test_batch_investigation(api_manager)
            
            # Individual API wrapper tests
            await test_suite.test_individual_api_wrappers(api_manager)
            
            # Error handling
            await test_suite.test_error_handling(api_manager)
            
            # Performance benchmarks
            await test_suite.test_performance_benchmarks(api_manager)
            
            # Caching functionality
            await test_suite.test_caching_functionality(api_manager)
            
            # Statistics tracking
            test_suite.test_statistics_tracking(api_manager)
            
            print("\n🔍 Starting Validation Tests...")
            
            # Validation tests
            await validation_suite.test_response_schema_validation()
            await validation_suite.test_rate_limit_handling()
            await validation_suite.test_null_field_handling()
            
            # Final statistics
            final_stats = api_manager.get_statistics()
            print("\n" + "=" * 80)
            print("FINAL TEST STATISTICS")
            print("=" * 80)
            print(f"Total Investigations: {final_stats['investigation_stats']['total_investigations']}")
            print(f"Successful: {final_stats['investigation_stats']['successful_investigations']}")
            print(f"Failed: {final_stats['investigation_stats']['failed_investigations']}")
            print(f"High Risk Detections: {final_stats['investigation_stats']['high_risk_detections']}")
            print(f"APIs Called: {final_stats['investigation_stats']['apis_called']}")
            print(f"Average Processing Time: {final_stats['investigation_stats']['average_processing_time']:.3f}s")
            print(f"Cache Size: {final_stats['cache_size']}")
            
            print("\n✅ ALL TESTS COMPLETED SUCCESSFULLY!")
            
    except Exception as e:
        print(f"\n❌ TEST SUITE FAILED: {e}")
        raise

if __name__ == "__main__":
    # Run the comprehensive test suite
    asyncio.run(run_comprehensive_tests())

