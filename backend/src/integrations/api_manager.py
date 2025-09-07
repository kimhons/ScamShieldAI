"""
Unified API Manager for ScamShield AI
Orchestrates all API integrations and provides centralized management
"""

import asyncio
import json
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging

from .base_api import APIResponse
from .security_apis import SecurityAPIWrapper
from .anti_malware_apis import AntiMalwareAPIWrapper
from .email_apis import EmailAPIWrapper
from .geolocation_apis import GeolocationAPIWrapper
from .phone_apis import PhoneAPIWrapper
from .validation_apis import ValidationAPIWrapper

logger = logging.getLogger(__name__)

@dataclass
class InvestigationRequest:
    """Standardized investigation request format"""
    target_type: str  # 'email', 'phone', 'ip', 'domain', 'url', 'comprehensive'
    target_value: str
    investigation_level: str = 'standard'  # 'basic', 'standard', 'professional', 'forensic'
    additional_data: Dict[str, Any] = None
    client_id: str = None
    request_id: str = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.additional_data is None:
            self.additional_data = {}
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()

@dataclass
class InvestigationResult:
    """Standardized investigation result format"""
    request_id: str
    target_type: str
    target_value: str
    overall_risk_score: float
    overall_risk_level: str
    confidence_score: float
    investigation_level: str
    detailed_analysis: Dict[str, Any]
    recommendations: List[str]
    summary: str
    processing_time: float
    apis_used: List[str]
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        result = asdict(self)
        result['timestamp'] = self.timestamp.isoformat()
        return result

class APIManager:
    """Unified API Manager for all ScamShield integrations"""
    
    def __init__(self, api_keys: Dict[str, str] = None):
        """Initialize API Manager with all service wrappers"""
        self.api_keys = api_keys or {}
        
        # Initialize all API wrappers
        self.security_apis = SecurityAPIWrapper(api_keys)
        self.anti_malware_apis = AntiMalwareAPIWrapper(api_keys)
        self.email_apis = EmailAPIWrapper(api_keys)
        self.geolocation_apis = GeolocationAPIWrapper(api_keys)
        self.phone_apis = PhoneAPIWrapper(api_keys)
        self.validation_apis = ValidationAPIWrapper(api_keys)
        
        # API wrapper registry
        self.api_wrappers = {
            'security': self.security_apis,
            'anti_malware': self.anti_malware_apis,
            'email': self.email_apis,
            'geolocation': self.geolocation_apis,
            'phone': self.phone_apis,
            'validation': self.validation_apis
        }
        
        # Investigation statistics
        self.stats = {
            'total_investigations': 0,
            'successful_investigations': 0,
            'failed_investigations': 0,
            'high_risk_detections': 0,
            'apis_called': 0,
            'average_processing_time': 0.0,
            'last_reset': datetime.utcnow()
        }
        
        # Investigation cache
        self.investigation_cache = {}
        self.cache_ttl = 3600  # 1 hour
    
    async def __aenter__(self):
        """Async context manager entry"""
        # Initialize all API wrapper sessions
        for wrapper in self.api_wrappers.values():
            await wrapper.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        # Close all API wrapper sessions
        for wrapper in self.api_wrappers.values():
            await wrapper.__aexit__(exc_type, exc_val, exc_tb)
    
    async def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check of all API services"""
        health_results = {}
        
        for service_name, wrapper in self.api_wrappers.items():
            try:
                result = await wrapper.health_check()
                health_results[service_name] = {
                    'status': 'healthy' if result.success else 'unhealthy',
                    'details': result.data,
                    'response_time': result.response_time
                }
            except Exception as e:
                health_results[service_name] = {
                    'status': 'error',
                    'error': str(e),
                    'response_time': 0.0
                }
        
        # Calculate overall health
        healthy_services = sum(1 for h in health_results.values() if h['status'] == 'healthy')
        total_services = len(health_results)
        overall_health = (healthy_services / total_services) * 100 if total_services > 0 else 0
        
        return {
            'overall_health': overall_health,
            'healthy_services': healthy_services,
            'total_services': total_services,
            'service_details': health_results,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _generate_cache_key(self, request: InvestigationRequest) -> str:
        """Generate cache key for investigation request"""
        key_data = f"{request.target_type}:{request.target_value}:{request.investigation_level}"
        return key_data
    
    def _get_cached_result(self, cache_key: str) -> Optional[InvestigationResult]:
        """Get cached investigation result if still valid"""
        if cache_key in self.investigation_cache:
            cached_data, timestamp = self.investigation_cache[cache_key]
            if datetime.utcnow() - timestamp < timedelta(seconds=self.cache_ttl):
                return cached_data
            else:
                # Remove expired cache entry
                del self.investigation_cache[cache_key]
        return None
    
    def _cache_result(self, cache_key: str, result: InvestigationResult):
        """Cache investigation result"""
        self.investigation_cache[cache_key] = (result, datetime.utcnow())
    
    async def investigate_email(self, email: str, investigation_level: str = 'standard') -> InvestigationResult:
        """Comprehensive email investigation"""
        start_time = datetime.utcnow()
        apis_used = []
        
        try:
            # Email validation and analysis
            email_result = await self.email_apis.comprehensive_email_analysis(email)
            apis_used.append('email_validation')
            
            # Security reputation check
            security_result = await self.security_apis.check_email_reputation(email)
            apis_used.append('email_security')
            
            # Extract domain for additional checks
            domain = email.split('@')[1] if '@' in email else ''
            domain_result = None
            if domain:
                domain_result = await self.security_apis.check_domain_reputation(domain)
                apis_used.append('domain_security')
            
            # Combine results
            detailed_analysis = {
                'email_analysis': email_result.data if email_result.success else None,
                'security_analysis': security_result.data if security_result.success else None,
                'domain_analysis': domain_result.data if domain_result and domain_result.success else None
            }
            
            # Calculate overall risk score
            risk_scores = []
            if email_result.success and 'overall_risk_score' in email_result.data:
                risk_scores.append(email_result.data['overall_risk_score'])
            if security_result.success and 'risk_score' in security_result.data:
                risk_scores.append(security_result.data['risk_score'])
            if domain_result and domain_result.success and 'risk_score' in domain_result.data:
                risk_scores.append(domain_result.data['risk_score'])
            
            overall_risk = max(risk_scores) if risk_scores else 50
            overall_risk_level = 'HIGH' if overall_risk > 70 else 'MEDIUM' if overall_risk > 30 else 'LOW'
            
            # Calculate confidence score
            successful_apis = sum(1 for result in [email_result, security_result, domain_result] if result and result.success)
            confidence_score = (successful_apis / 3) * 100
            
            # Generate recommendations
            recommendations = []
            for analysis in detailed_analysis.values():
                if analysis and 'recommendations' in analysis:
                    recommendations.extend(analysis['recommendations'])
                elif analysis and 'recommendation' in analysis:
                    recommendations.append(analysis['recommendation'])
            
            # Generate summary
            summary = f"Email {email} analysis: Risk {overall_risk:.1f}/100 ({overall_risk_level})"
            if detailed_analysis['email_analysis'] and 'summary' in detailed_analysis['email_analysis']:
                summary += f" | {detailed_analysis['email_analysis']['summary']}"
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return InvestigationResult(
                request_id=f"email_{int(start_time.timestamp())}",
                target_type='email',
                target_value=email,
                overall_risk_score=overall_risk,
                overall_risk_level=overall_risk_level,
                confidence_score=confidence_score,
                investigation_level=investigation_level,
                detailed_analysis=detailed_analysis,
                recommendations=recommendations,
                summary=summary,
                processing_time=processing_time,
                apis_used=apis_used,
                timestamp=start_time
            )
            
        except Exception as e:
            logger.error(f"Email investigation failed: {e}")
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return InvestigationResult(
                request_id=f"email_{int(start_time.timestamp())}",
                target_type='email',
                target_value=email,
                overall_risk_score=100,
                overall_risk_level='HIGH',
                confidence_score=0,
                investigation_level=investigation_level,
                detailed_analysis={'error': str(e)},
                recommendations=['Investigation failed - manual review required'],
                summary=f"Email investigation failed: {str(e)}",
                processing_time=processing_time,
                apis_used=apis_used,
                timestamp=start_time
            )
    
    async def investigate_phone(self, phone: str, investigation_level: str = 'standard') -> InvestigationResult:
        """Comprehensive phone number investigation"""
        start_time = datetime.utcnow()
        apis_used = []
        
        try:
            # Phone validation and analysis
            phone_result = await self.phone_apis.comprehensive_phone_analysis(phone)
            apis_used.append('phone_validation')
            
            # Risk analysis
            risk_result = await self.phone_apis.analyze_phone_risk(phone)
            apis_used.append('phone_risk')
            
            # Combine results
            detailed_analysis = {
                'phone_analysis': phone_result.data if phone_result.success else None,
                'risk_analysis': risk_result.data if risk_result.success else None
            }
            
            # Calculate overall risk score
            overall_risk = phone_result.data.get('overall_risk_score', 50) if phone_result.success else 50
            overall_risk_level = 'HIGH' if overall_risk > 70 else 'MEDIUM' if overall_risk > 30 else 'LOW'
            
            # Calculate confidence score
            successful_apis = sum(1 for result in [phone_result, risk_result] if result and result.success)
            confidence_score = (successful_apis / 2) * 100
            
            # Generate recommendations
            recommendations = []
            for analysis in detailed_analysis.values():
                if analysis and 'recommendations' in analysis:
                    recommendations.extend(analysis['recommendations'])
                elif analysis and 'recommendation' in analysis:
                    recommendations.append(analysis['recommendation'])
            
            # Generate summary
            summary = f"Phone {phone} analysis: Risk {overall_risk:.1f}/100 ({overall_risk_level})"
            if detailed_analysis['phone_analysis'] and 'summary' in detailed_analysis['phone_analysis']:
                summary += f" | {detailed_analysis['phone_analysis']['summary']}"
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return InvestigationResult(
                request_id=f"phone_{int(start_time.timestamp())}",
                target_type='phone',
                target_value=phone,
                overall_risk_score=overall_risk,
                overall_risk_level=overall_risk_level,
                confidence_score=confidence_score,
                investigation_level=investigation_level,
                detailed_analysis=detailed_analysis,
                recommendations=recommendations,
                summary=summary,
                processing_time=processing_time,
                apis_used=apis_used,
                timestamp=start_time
            )
            
        except Exception as e:
            logger.error(f"Phone investigation failed: {e}")
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return InvestigationResult(
                request_id=f"phone_{int(start_time.timestamp())}",
                target_type='phone',
                target_value=phone,
                overall_risk_score=100,
                overall_risk_level='HIGH',
                confidence_score=0,
                investigation_level=investigation_level,
                detailed_analysis={'error': str(e)},
                recommendations=['Investigation failed - manual review required'],
                summary=f"Phone investigation failed: {str(e)}",
                processing_time=processing_time,
                apis_used=apis_used,
                timestamp=start_time
            )
    
    async def investigate_ip(self, ip_address: str, investigation_level: str = 'standard') -> InvestigationResult:
        """Comprehensive IP address investigation"""
        start_time = datetime.utcnow()
        apis_used = []
        
        try:
            # IP geolocation and reputation
            geo_result = await self.geolocation_apis.comprehensive_ip_analysis(ip_address)
            apis_used.append('ip_geolocation')
            
            # Security reputation check
            security_result = await self.security_apis.check_ip_reputation(ip_address)
            apis_used.append('ip_security')
            
            # Combine results
            detailed_analysis = {
                'geolocation_analysis': geo_result.data if geo_result.success else None,
                'security_analysis': security_result.data if security_result.success else None
            }
            
            # Calculate overall risk score
            risk_scores = []
            if geo_result.success and 'overall_risk_score' in geo_result.data:
                risk_scores.append(geo_result.data['overall_risk_score'])
            if security_result.success and 'overall_risk_score' in security_result.data:
                risk_scores.append(security_result.data['overall_risk_score'])
            
            overall_risk = max(risk_scores) if risk_scores else 50
            overall_risk_level = 'HIGH' if overall_risk > 70 else 'MEDIUM' if overall_risk > 30 else 'LOW'
            
            # Calculate confidence score
            successful_apis = sum(1 for result in [geo_result, security_result] if result and result.success)
            confidence_score = (successful_apis / 2) * 100
            
            # Generate recommendations
            recommendations = []
            for analysis in detailed_analysis.values():
                if analysis and 'recommendations' in analysis:
                    recommendations.extend(analysis['recommendations'])
                elif analysis and 'recommendation' in analysis:
                    recommendations.append(analysis['recommendation'])
            
            # Generate summary
            summary = f"IP {ip_address} analysis: Risk {overall_risk:.1f}/100 ({overall_risk_level})"
            if detailed_analysis['geolocation_analysis'] and 'summary' in detailed_analysis['geolocation_analysis']:
                summary += f" | {detailed_analysis['geolocation_analysis']['summary']}"
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return InvestigationResult(
                request_id=f"ip_{int(start_time.timestamp())}",
                target_type='ip',
                target_value=ip_address,
                overall_risk_score=overall_risk,
                overall_risk_level=overall_risk_level,
                confidence_score=confidence_score,
                investigation_level=investigation_level,
                detailed_analysis=detailed_analysis,
                recommendations=recommendations,
                summary=summary,
                processing_time=processing_time,
                apis_used=apis_used,
                timestamp=start_time
            )
            
        except Exception as e:
            logger.error(f"IP investigation failed: {e}")
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return InvestigationResult(
                request_id=f"ip_{int(start_time.timestamp())}",
                target_type='ip',
                target_value=ip_address,
                overall_risk_score=100,
                overall_risk_level='HIGH',
                confidence_score=0,
                investigation_level=investigation_level,
                detailed_analysis={'error': str(e)},
                recommendations=['Investigation failed - manual review required'],
                summary=f"IP investigation failed: {str(e)}",
                processing_time=processing_time,
                apis_used=apis_used,
                timestamp=start_time
            )
    
    async def investigate_domain(self, domain: str, investigation_level: str = 'standard') -> InvestigationResult:
        """Comprehensive domain investigation"""
        start_time = datetime.utcnow()
        apis_used = []
        
        try:
            # Domain security analysis
            security_result = await self.security_apis.check_domain_reputation(domain)
            apis_used.append('domain_security')
            
            # Anti-malware checks
            malware_result = await self.anti_malware_apis.check_url_reputation(f"https://{domain}")
            apis_used.append('domain_malware')
            
            # Combine results
            detailed_analysis = {
                'security_analysis': security_result.data if security_result.success else None,
                'malware_analysis': malware_result.data if malware_result.success else None
            }
            
            # Calculate overall risk score
            risk_scores = []
            if security_result.success and 'risk_score' in security_result.data:
                risk_scores.append(security_result.data['risk_score'])
            if malware_result.success and 'risk_score' in malware_result.data:
                risk_scores.append(malware_result.data['risk_score'])
            
            overall_risk = max(risk_scores) if risk_scores else 50
            overall_risk_level = 'HIGH' if overall_risk > 70 else 'MEDIUM' if overall_risk > 30 else 'LOW'
            
            # Calculate confidence score
            successful_apis = sum(1 for result in [security_result, malware_result] if result and result.success)
            confidence_score = (successful_apis / 2) * 100
            
            # Generate recommendations
            recommendations = []
            for analysis in detailed_analysis.values():
                if analysis and 'recommendations' in analysis:
                    recommendations.extend(analysis['recommendations'])
                elif analysis and 'recommendation' in analysis:
                    recommendations.append(analysis['recommendation'])
            
            # Generate summary
            summary = f"Domain {domain} analysis: Risk {overall_risk:.1f}/100 ({overall_risk_level})"
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return InvestigationResult(
                request_id=f"domain_{int(start_time.timestamp())}",
                target_type='domain',
                target_value=domain,
                overall_risk_score=overall_risk,
                overall_risk_level=overall_risk_level,
                confidence_score=confidence_score,
                investigation_level=investigation_level,
                detailed_analysis=detailed_analysis,
                recommendations=recommendations,
                summary=summary,
                processing_time=processing_time,
                apis_used=apis_used,
                timestamp=start_time
            )
            
        except Exception as e:
            logger.error(f"Domain investigation failed: {e}")
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return InvestigationResult(
                request_id=f"domain_{int(start_time.timestamp())}",
                target_type='domain',
                target_value=domain,
                overall_risk_score=100,
                overall_risk_level='HIGH',
                confidence_score=0,
                investigation_level=investigation_level,
                detailed_analysis={'error': str(e)},
                recommendations=['Investigation failed - manual review required'],
                summary=f"Domain investigation failed: {str(e)}",
                processing_time=processing_time,
                apis_used=apis_used,
                timestamp=start_time
            )
    
    async def investigate_url(self, url: str, investigation_level: str = 'standard') -> InvestigationResult:
        """Comprehensive URL investigation"""
        start_time = datetime.utcnow()
        apis_used = []
        
        try:
            # URL validation
            validation_result = await self.validation_apis.validate_url(url)
            apis_used.append('url_validation')
            
            # Anti-malware URL reputation
            malware_result = await self.anti_malware_apis.check_url_reputation(url)
            apis_used.append('url_malware')
            
            # Extract domain for additional checks
            try:
                from urllib.parse import urlparse
                parsed_url = urlparse(url)
                domain = parsed_url.netloc
                if domain:
                    domain_result = await self.investigate_domain(domain, investigation_level)
                    apis_used.extend(domain_result.apis_used)
                else:
                    domain_result = None
            except:
                domain_result = None
            
            # Combine results
            detailed_analysis = {
                'validation_analysis': validation_result.data if validation_result.success else None,
                'malware_analysis': malware_result.data if malware_result.success else None,
                'domain_analysis': domain_result.detailed_analysis if domain_result else None
            }
            
            # Calculate overall risk score
            risk_scores = []
            if validation_result.success and 'risk_score' in validation_result.data:
                risk_scores.append(validation_result.data['risk_score'])
            if malware_result.success and 'risk_score' in malware_result.data:
                risk_scores.append(malware_result.data['risk_score'])
            if domain_result:
                risk_scores.append(domain_result.overall_risk_score)
            
            overall_risk = max(risk_scores) if risk_scores else 50
            overall_risk_level = 'HIGH' if overall_risk > 70 else 'MEDIUM' if overall_risk > 30 else 'LOW'
            
            # Calculate confidence score
            successful_checks = sum(1 for result in [validation_result, malware_result] if result and result.success)
            if domain_result:
                successful_checks += 1
            confidence_score = (successful_checks / 3) * 100
            
            # Generate recommendations
            recommendations = []
            for analysis in detailed_analysis.values():
                if analysis and isinstance(analysis, dict):
                    if 'recommendations' in analysis:
                        recommendations.extend(analysis['recommendations'])
                    elif 'recommendation' in analysis:
                        recommendations.append(analysis['recommendation'])
            
            if domain_result and domain_result.recommendations:
                recommendations.extend(domain_result.recommendations)
            
            # Generate summary
            summary = f"URL {url} analysis: Risk {overall_risk:.1f}/100 ({overall_risk_level})"
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return InvestigationResult(
                request_id=f"url_{int(start_time.timestamp())}",
                target_type='url',
                target_value=url,
                overall_risk_score=overall_risk,
                overall_risk_level=overall_risk_level,
                confidence_score=confidence_score,
                investigation_level=investigation_level,
                detailed_analysis=detailed_analysis,
                recommendations=recommendations,
                summary=summary,
                processing_time=processing_time,
                apis_used=apis_used,
                timestamp=start_time
            )
            
        except Exception as e:
            logger.error(f"URL investigation failed: {e}")
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return InvestigationResult(
                request_id=f"url_{int(start_time.timestamp())}",
                target_type='url',
                target_value=url,
                overall_risk_score=100,
                overall_risk_level='HIGH',
                confidence_score=0,
                investigation_level=investigation_level,
                detailed_analysis={'error': str(e)},
                recommendations=['Investigation failed - manual review required'],
                summary=f"URL investigation failed: {str(e)}",
                processing_time=processing_time,
                apis_used=apis_used,
                timestamp=start_time
            )
    
    async def comprehensive_investigation(self, request: InvestigationRequest) -> InvestigationResult:
        """Perform comprehensive investigation based on request type"""
        # Check cache first
        cache_key = self._generate_cache_key(request)
        cached_result = self._get_cached_result(cache_key)
        if cached_result:
            return cached_result
        
        # Update statistics
        self.stats['total_investigations'] += 1
        
        try:
            # Route to appropriate investigation method
            if request.target_type == 'email':
                result = await self.investigate_email(request.target_value, request.investigation_level)
            elif request.target_type == 'phone':
                result = await self.investigate_phone(request.target_value, request.investigation_level)
            elif request.target_type == 'ip':
                result = await self.investigate_ip(request.target_value, request.investigation_level)
            elif request.target_type == 'domain':
                result = await self.investigate_domain(request.target_value, request.investigation_level)
            elif request.target_type == 'url':
                result = await self.investigate_url(request.target_value, request.investigation_level)
            else:
                raise ValueError(f"Unsupported target type: {request.target_type}")
            
            # Update request metadata
            result.request_id = request.request_id or result.request_id
            
            # Cache result
            self._cache_result(cache_key, result)
            
            # Update statistics
            self.stats['successful_investigations'] += 1
            self.stats['apis_called'] += len(result.apis_used)
            
            if result.overall_risk_level == 'HIGH':
                self.stats['high_risk_detections'] += 1
            
            # Update average processing time
            total_time = (self.stats['average_processing_time'] * (self.stats['successful_investigations'] - 1) + 
                         result.processing_time)
            self.stats['average_processing_time'] = total_time / self.stats['successful_investigations']
            
            return result
            
        except Exception as e:
            logger.error(f"Comprehensive investigation failed: {e}")
            self.stats['failed_investigations'] += 1
            
            # Return error result
            return InvestigationResult(
                request_id=request.request_id or f"error_{int(datetime.utcnow().timestamp())}",
                target_type=request.target_type,
                target_value=request.target_value,
                overall_risk_score=100,
                overall_risk_level='HIGH',
                confidence_score=0,
                investigation_level=request.investigation_level,
                detailed_analysis={'error': str(e)},
                recommendations=['Investigation failed - manual review required'],
                summary=f"Investigation failed: {str(e)}",
                processing_time=0.0,
                apis_used=[],
                timestamp=datetime.utcnow()
            )
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive API manager statistics"""
        # Get individual API wrapper statistics
        api_stats = {}
        for service_name, wrapper in self.api_wrappers.items():
            api_stats[service_name] = wrapper.get_stats()
        
        return {
            'investigation_stats': self.stats,
            'api_wrapper_stats': api_stats,
            'cache_size': len(self.investigation_cache),
            'available_apis': list(self.api_wrappers.keys()),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def reset_statistics(self):
        """Reset all statistics"""
        self.stats = {
            'total_investigations': 0,
            'successful_investigations': 0,
            'failed_investigations': 0,
            'high_risk_detections': 0,
            'apis_called': 0,
            'average_processing_time': 0.0,
            'last_reset': datetime.utcnow()
        }
        
        # Reset individual API wrapper statistics
        for wrapper in self.api_wrappers.values():
            wrapper.reset_stats()
    
    def clear_cache(self):
        """Clear investigation cache"""
        self.investigation_cache.clear()
    
    async def batch_investigate(self, requests: List[InvestigationRequest]) -> List[InvestigationResult]:
        """Process multiple investigation requests in parallel"""
        # Limit concurrent investigations to prevent overwhelming APIs
        semaphore = asyncio.Semaphore(5)
        
        async def process_request(request):
            async with semaphore:
                return await self.comprehensive_investigation(request)
        
        tasks = [process_request(request) for request in requests]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                error_result = InvestigationResult(
                    request_id=requests[i].request_id or f"batch_error_{i}",
                    target_type=requests[i].target_type,
                    target_value=requests[i].target_value,
                    overall_risk_score=100,
                    overall_risk_level='HIGH',
                    confidence_score=0,
                    investigation_level=requests[i].investigation_level,
                    detailed_analysis={'error': str(result)},
                    recommendations=['Batch investigation failed - manual review required'],
                    summary=f"Batch investigation failed: {str(result)}",
                    processing_time=0.0,
                    apis_used=[],
                    timestamp=datetime.utcnow()
                )
                final_results.append(error_result)
            else:
                final_results.append(result)
        
        return final_results

