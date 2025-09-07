"""
Phone APIs Wrapper for ScamShield AI
Integrates phone validation and carrier lookup APIs
"""

import asyncio
import re
from typing import Dict, Any, Optional, List
from .base_api import BaseAPIWrapper, APIConfig, APIResponse
import logging

logger = logging.getLogger(__name__)

class PhoneAPIWrapper(BaseAPIWrapper):
    """Wrapper for phone validation and carrier lookup APIs"""
    
    def __init__(self, api_keys: Dict[str, str] = None):
        super().__init__(APIConfig(
            name="PhoneAPIs",
            base_url="https://api.phone.com",
            rate_limit=60
        ))
        
        self.api_keys = api_keys or {}
        self.apis = self._initialize_apis()
    
    def _initialize_apis(self) -> Dict[str, APIConfig]:
        """Initialize all phone API configurations"""
        return {
            'numverify': APIConfig(
                name='apilayer numverify',
                base_url='https://apilayer.net/api',
                api_key=self.api_keys.get('numverify'),
                rate_limit=1000,
                cache_ttl=86400,  # 24 hours
                requires_auth=True
            ),
            'veriphone': APIConfig(
                name='Veriphone',
                base_url='https://api.veriphone.io/v2',
                api_key=self.api_keys.get('veriphone'),
                rate_limit=1000,
                cache_ttl=86400,
                requires_auth=True
            ),
            'phone_validation': APIConfig(
                name='Phone Validation',
                base_url='https://api.phone-validator.net/api/v2',
                api_key=self.api_keys.get('phone_validation'),
                rate_limit=1000,
                cache_ttl=86400,
                requires_auth=True
            ),
            'cloudmersive_phone': APIConfig(
                name='Cloudmersive Phone',
                base_url='https://api.cloudmersive.com/validate',
                api_key=self.api_keys.get('cloudmersive'),
                rate_limit=800,
                cache_ttl=86400,
                requires_auth=True
            ),
            'twilio_lookup': APIConfig(
                name='Twilio Lookup',
                base_url='https://lookups.twilio.com/v1',
                api_key=self.api_keys.get('twilio'),
                rate_limit=1000,
                cache_ttl=86400,
                requires_auth=True
            ),
            'phone_number_api': APIConfig(
                name='Phone Number API',
                base_url='https://api.phone-number-api.com/json',
                api_key=None,  # No auth required
                rate_limit=1000,
                cache_ttl=86400,
                requires_auth=False
            ),
            'phoneapi': APIConfig(
                name='PhoneAPI',
                base_url='https://api.phoneapi.com/v1',
                api_key=self.api_keys.get('phoneapi'),
                rate_limit=1000,
                cache_ttl=86400,
                requires_auth=True
            ),
            'carrier_lookup': APIConfig(
                name='Carrier Lookup',
                base_url='https://api.carrier-lookup.com/v1',
                api_key=self.api_keys.get('carrier_lookup'),
                rate_limit=1000,
                cache_ttl=86400,
                requires_auth=True
            )
        }
    
    def get_auth_header_name(self) -> str:
        """Get authentication header name"""
        return 'X-API-Key'
    
    async def health_check(self) -> APIResponse:
        """Check health of all phone APIs"""
        results = {}
        
        # Test Phone Number API (no auth required)
        try:
            response = await self.validate_phone_number('+1234567890')
            results['phone_number_api'] = response.success
        except:
            results['phone_number_api'] = False
        
        return APIResponse(
            success=True,
            data={'health_status': results},
            api_name='PhoneAPIs'
        )
    
    def _normalize_phone_number(self, phone: str) -> str:
        """Normalize phone number format"""
        # Remove all non-digit characters except +
        normalized = re.sub(r'[^\d+]', '', phone)
        
        # Add + if not present and number looks international
        if not normalized.startswith('+') and len(normalized) > 10:
            normalized = '+' + normalized
        
        return normalized
    
    def _is_valid_phone_format(self, phone: str) -> bool:
        """Basic phone number format validation"""
        normalized = self._normalize_phone_number(phone)
        
        # Check if it's a valid international format
        pattern = r'^\+?[1-9]\d{6,14}$'
        return re.match(pattern, normalized) is not None
    
    async def validate_phone_number(self, phone_number: str) -> APIResponse:
        """Validate phone number across multiple services"""
        normalized_phone = self._normalize_phone_number(phone_number)
        
        if not self._is_valid_phone_format(normalized_phone):
            return APIResponse(
                success=True,
                data={
                    'phone_number': phone_number,
                    'normalized_phone': normalized_phone,
                    'valid_format': False,
                    'risk_score': 100,
                    'risk_level': 'HIGH',
                    'recommendation': 'Invalid phone number format'
                },
                api_name='PhoneAPIs'
            )
        
        results = {}
        
        # Phone Number API (free, no auth)
        try:
            self.config = self.apis['phone_number_api']
            # Remove + for this API
            clean_phone = normalized_phone.lstrip('+')
            response = await self.make_request(f'{clean_phone}')
            if response.success:
                data = response.data
                results['phone_number_api'] = {
                    'valid': data.get('valid', False),
                    'country': data.get('country'),
                    'country_code': data.get('country_code'),
                    'carrier': data.get('carrier'),
                    'line_type': data.get('line_type'),
                    'is_mobile': data.get('is_mobile', False),
                    'is_landline': data.get('is_landline', False)
                }
        except Exception as e:
            logger.error(f"Phone Number API error: {e}")
            results['phone_number_api'] = {'error': str(e)}
        
        # Numverify (paid)
        if 'numverify' in self.api_keys:
            try:
                self.config = self.apis['numverify']
                response = await self.make_request(
                    'validate',
                    params={
                        'access_key': self.api_keys.get('numverify'),
                        'number': normalized_phone,
                        'country_code': '',
                        'format': 1
                    }
                )
                if response.success:
                    data = response.data
                    results['numverify'] = {
                        'valid': data.get('valid', False),
                        'number': data.get('number'),
                        'local_format': data.get('local_format'),
                        'international_format': data.get('international_format'),
                        'country_prefix': data.get('country_prefix'),
                        'country_code': data.get('country_code'),
                        'country_name': data.get('country_name'),
                        'location': data.get('location'),
                        'carrier': data.get('carrier'),
                        'line_type': data.get('line_type')
                    }
            except Exception as e:
                logger.error(f"Numverify error: {e}")
                results['numverify'] = {'error': str(e)}
        
        # Veriphone (paid)
        if 'veriphone' in self.api_keys:
            try:
                self.config = self.apis['veriphone']
                response = await self.make_request(
                    'verify',
                    params={
                        'phone': normalized_phone,
                        'key': self.api_keys.get('veriphone')
                    }
                )
                if response.success:
                    data = response.data
                    results['veriphone'] = {
                        'status': data.get('status'),
                        'phone': data.get('phone'),
                        'phone_valid': data.get('phone_valid', False),
                        'phone_type': data.get('phone_type'),
                        'phone_region': data.get('phone_region'),
                        'country': data.get('country'),
                        'country_code': data.get('country_code'),
                        'country_prefix': data.get('country_prefix'),
                        'international_number': data.get('international_number'),
                        'local_number': data.get('local_number'),
                        'e164': data.get('e164'),
                        'carrier': data.get('carrier')
                    }
            except Exception as e:
                logger.error(f"Veriphone error: {e}")
                results['veriphone'] = {'error': str(e)}
        
        # Phone Validation API (paid)
        if 'phone_validation' in self.api_keys:
            try:
                self.config = self.apis['phone_validation']
                response = await self.make_request(
                    'validate',
                    params={
                        'PhoneNumber': normalized_phone,
                        'APIKey': self.api_keys.get('phone_validation')
                    }
                )
                if response.success:
                    data = response.data
                    results['phone_validation'] = {
                        'status': data.get('status'),
                        'result': data.get('result'),
                        'reason': data.get('reason'),
                        'valid': data.get('valid', False),
                        'country': data.get('country'),
                        'country_code': data.get('country_code'),
                        'carrier': data.get('carrier'),
                        'line_type': data.get('line_type'),
                        'is_mobile': data.get('is_mobile', False),
                        'is_landline': data.get('is_landline', False)
                    }
            except Exception as e:
                logger.error(f"Phone Validation API error: {e}")
                results['phone_validation'] = {'error': str(e)}
        
        # Cloudmersive Phone (paid)
        if 'cloudmersive' in self.api_keys:
            try:
                self.config = self.apis['cloudmersive_phone']
                response = await self.make_request(
                    'phonenumber/lookup',
                    method='POST',
                    data={'PhoneNumber': normalized_phone}
                )
                if response.success:
                    data = response.data
                    results['cloudmersive_phone'] = {
                        'is_valid': data.get('IsValid', False),
                        'display_number': data.get('DisplayNumber'),
                        'e164_number': data.get('E164Number'),
                        'country_code': data.get('CountryCode'),
                        'country_name': data.get('CountryName'),
                        'phone_type': data.get('PhoneType'),
                        'carrier': data.get('Carrier'),
                        'is_valid_number': data.get('IsValidNumber', False)
                    }
            except Exception as e:
                logger.error(f"Cloudmersive Phone error: {e}")
                results['cloudmersive_phone'] = {'error': str(e)}
        
        # Calculate phone validation score
        validation_score = 0
        valid_checks = 0
        risk_factors = []
        
        for api_name, api_result in results.items():
            if 'error' not in api_result:
                valid_checks += 1
                
                # Check validation results
                is_valid = (
                    api_result.get('valid', False) or
                    api_result.get('phone_valid', False) or
                    api_result.get('is_valid', False) or
                    api_result.get('is_valid_number', False)
                )
                
                if is_valid:
                    validation_score += 25
                
                # Check for risk factors
                line_type = api_result.get('line_type', '').lower()
                phone_type = api_result.get('phone_type', '').lower()
                
                if 'voip' in line_type or 'voip' in phone_type:
                    risk_factors.append('VoIP number detected')
                
                if 'prepaid' in line_type or 'prepaid' in phone_type:
                    risk_factors.append('Prepaid number')
        
        # Normalize validation score
        if valid_checks > 0:
            validation_score = min(100, validation_score / valid_checks * 100)
        
        # Calculate risk score (inverse of validation score)
        risk_score = 100 - validation_score
        
        # Adjust for risk factors
        risk_score += len(risk_factors) * 15
        risk_score = min(100, risk_score)
        
        return APIResponse(
            success=True,
            data={
                'phone_number': phone_number,
                'normalized_phone': normalized_phone,
                'valid_format': True,
                'validation_score': validation_score,
                'risk_score': risk_score,
                'risk_level': 'HIGH' if risk_score > 70 else 'MEDIUM' if risk_score > 30 else 'LOW',
                'risk_factors': risk_factors,
                'detailed_results': results,
                'recommendation': self._get_phone_recommendation(risk_score, risk_factors, results)
            },
            api_name='PhoneAPIs'
        )
    
    async def lookup_carrier_info(self, phone_number: str) -> APIResponse:
        """Lookup carrier information for phone number"""
        normalized_phone = self._normalize_phone_number(phone_number)
        results = {}
        
        # Carrier Lookup API (if available)
        if 'carrier_lookup' in self.api_keys:
            try:
                self.config = self.apis['carrier_lookup']
                response = await self.make_request(
                    'lookup',
                    params={
                        'phone': normalized_phone,
                        'api_key': self.api_keys.get('carrier_lookup')
                    }
                )
                if response.success:
                    data = response.data
                    results['carrier_lookup'] = {
                        'carrier_name': data.get('carrier_name'),
                        'carrier_type': data.get('carrier_type'),
                        'mobile_country_code': data.get('mobile_country_code'),
                        'mobile_network_code': data.get('mobile_network_code'),
                        'is_ported': data.get('is_ported', False),
                        'original_carrier': data.get('original_carrier'),
                        'roaming': data.get('roaming', False)
                    }
            except Exception as e:
                logger.error(f"Carrier Lookup API error: {e}")
                results['carrier_lookup'] = {'error': str(e)}
        
        # Twilio Lookup (if available)
        if 'twilio' in self.api_keys:
            try:
                self.config = self.apis['twilio_lookup']
                # Twilio uses Basic Auth with Account SID and Auth Token
                response = await self.make_request(
                    f'PhoneNumbers/{normalized_phone}',
                    params={'Type': 'carrier'}
                )
                if response.success:
                    data = response.data
                    carrier_info = data.get('carrier', {})
                    results['twilio_lookup'] = {
                        'carrier_name': carrier_info.get('name'),
                        'carrier_type': carrier_info.get('type'),
                        'mobile_country_code': carrier_info.get('mobile_country_code'),
                        'mobile_network_code': carrier_info.get('mobile_network_code'),
                        'error_code': carrier_info.get('error_code')
                    }
            except Exception as e:
                logger.error(f"Twilio Lookup error: {e}")
                results['twilio_lookup'] = {'error': str(e)}
        
        # Consolidate carrier information
        carrier_data = self._consolidate_carrier_data(results)
        
        return APIResponse(
            success=True,
            data={
                'phone_number': phone_number,
                'normalized_phone': normalized_phone,
                'carrier_info': carrier_data,
                'detailed_results': results,
                'recommendation': self._get_carrier_recommendation(carrier_data)
            },
            api_name='PhoneAPIs'
        )
    
    def _consolidate_carrier_data(self, results: Dict) -> Dict[str, Any]:
        """Consolidate carrier data from multiple sources"""
        consolidated = {
            'carrier_name': None,
            'carrier_type': None,
            'mobile_country_code': None,
            'mobile_network_code': None,
            'is_ported': False,
            'is_roaming': False,
            'confidence_sources': 0
        }
        
        for api_name, api_result in results.items():
            if 'error' not in api_result:
                consolidated['confidence_sources'] += 1
                
                if api_result.get('carrier_name') and not consolidated['carrier_name']:
                    consolidated['carrier_name'] = api_result['carrier_name']
                
                if api_result.get('carrier_type') and not consolidated['carrier_type']:
                    consolidated['carrier_type'] = api_result['carrier_type']
                
                if api_result.get('mobile_country_code') and not consolidated['mobile_country_code']:
                    consolidated['mobile_country_code'] = api_result['mobile_country_code']
                
                if api_result.get('mobile_network_code') and not consolidated['mobile_network_code']:
                    consolidated['mobile_network_code'] = api_result['mobile_network_code']
                
                if api_result.get('is_ported'):
                    consolidated['is_ported'] = True
                
                if api_result.get('roaming'):
                    consolidated['is_roaming'] = True
        
        return consolidated
    
    async def analyze_phone_risk(self, phone_number: str) -> APIResponse:
        """Analyze phone number for fraud risk indicators"""
        # Get validation data
        validation_result = await self.validate_phone_number(phone_number)
        
        # Get carrier information
        carrier_result = await self.lookup_carrier_info(phone_number)
        
        if not validation_result.success:
            return validation_result
        
        validation_data = validation_result.data
        carrier_data = carrier_result.data if carrier_result.success else {}
        
        # Calculate comprehensive risk score
        risk_factors = []
        risk_score = validation_data.get('risk_score', 0)
        
        # Carrier-based risk factors
        carrier_info = carrier_data.get('carrier_info', {})
        carrier_type = carrier_info.get('carrier_type', '').lower()
        
        if 'voip' in carrier_type:
            risk_factors.append('VoIP carrier')
            risk_score += 20
        
        if carrier_info.get('is_ported'):
            risk_factors.append('Ported number')
            risk_score += 10
        
        if carrier_info.get('is_roaming'):
            risk_factors.append('Roaming number')
            risk_score += 15
        
        # Check for suspicious patterns
        normalized_phone = validation_data.get('normalized_phone', '')
        if self._has_suspicious_pattern(normalized_phone):
            risk_factors.append('Suspicious number pattern')
            risk_score += 25
        
        risk_score = min(100, risk_score)
        
        return APIResponse(
            success=True,
            data={
                'phone_number': phone_number,
                'risk_score': risk_score,
                'risk_level': 'HIGH' if risk_score > 70 else 'MEDIUM' if risk_score > 30 else 'LOW',
                'risk_factors': risk_factors,
                'validation_analysis': validation_data,
                'carrier_analysis': carrier_data,
                'recommendation': self._get_risk_recommendation(risk_score, risk_factors)
            },
            api_name='PhoneAPIs'
        )
    
    def _has_suspicious_pattern(self, phone: str) -> bool:
        """Check for suspicious phone number patterns"""
        # Remove country code for pattern analysis
        digits = re.sub(r'[^\d]', '', phone)
        
        # Check for repeated digits (e.g., 1111111111)
        if len(set(digits[-10:])) <= 2:
            return True
        
        # Check for sequential patterns (e.g., 1234567890)
        last_10 = digits[-10:]
        if len(last_10) == 10:
            is_sequential = all(
                int(last_10[i]) == (int(last_10[i-1]) + 1) % 10
                for i in range(1, len(last_10))
            )
            if is_sequential:
                return True
        
        return False
    
    async def batch_validate_phones(self, phone_numbers: List[str]) -> APIResponse:
        """Validate multiple phone numbers in batch"""
        results = {}
        
        # Process phones in parallel (with rate limiting consideration)
        semaphore = asyncio.Semaphore(3)  # Limit concurrent requests
        
        async def process_phone(phone):
            async with semaphore:
                return await self.validate_phone_number(phone)
        
        tasks = [process_phone(phone) for phone in phone_numbers]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        for phone, response in zip(phone_numbers, responses):
            if isinstance(response, Exception):
                results[phone] = {'error': str(response)}
            else:
                results[phone] = response.data if response.success else {'error': 'Failed to validate'}
        
        # Calculate batch statistics
        successful_validations = sum(1 for r in results.values() if 'error' not in r)
        valid_phones = sum(1 for r in results.values() if r.get('validation_score', 0) > 70)
        high_risk_phones = sum(1 for r in results.values() if r.get('risk_level') == 'HIGH')
        
        return APIResponse(
            success=True,
            data={
                'total_phones': len(phone_numbers),
                'successful_validations': successful_validations,
                'valid_phones': valid_phones,
                'high_risk_phones': high_risk_phones,
                'results': results,
                'summary': f"Processed {len(phone_numbers)} phones: {valid_phones} valid, {high_risk_phones} high-risk"
            },
            api_name='PhoneAPIs'
        )
    
    def _get_phone_recommendation(self, risk_score: float, risk_factors: List[str], results: Dict) -> str:
        """Generate recommendation based on phone validation"""
        if risk_score > 70:
            factors_str = ', '.join(risk_factors) if risk_factors else 'multiple validation failures'
            return f"HIGH RISK: Phone number shows {factors_str}. Consider blocking or requiring alternative verification."
        elif risk_score > 30:
            return f"MEDIUM RISK: Phone number has some concerns. Additional verification recommended."
        else:
            return "LOW RISK: Phone number appears valid and legitimate."
    
    def _get_carrier_recommendation(self, carrier_data: Dict) -> str:
        """Generate recommendation based on carrier analysis"""
        carrier_type = carrier_data.get('carrier_type', '').lower()
        
        if 'voip' in carrier_type:
            return "MEDIUM RISK: VoIP number detected. Consider additional verification steps."
        elif carrier_data.get('is_ported'):
            return "LOW-MEDIUM RISK: Number has been ported. Monitor for unusual activity."
        else:
            return "LOW RISK: Standard carrier information detected."
    
    def _get_risk_recommendation(self, risk_score: float, risk_factors: List[str]) -> str:
        """Generate recommendation based on comprehensive risk analysis"""
        if risk_score > 70:
            return f"HIGH RISK: Multiple risk factors detected: {', '.join(risk_factors)}. Implement strict verification."
        elif risk_score > 30:
            return f"MEDIUM RISK: Some risk factors present. Enhanced monitoring recommended."
        else:
            return "LOW RISK: Phone number passes validation and risk assessment checks."
    
    async def comprehensive_phone_analysis(self, phone_number: str) -> APIResponse:
        """Perform comprehensive phone analysis including validation, carrier lookup, and risk assessment"""
        # Get all analysis types
        validation_result = await self.validate_phone_number(phone_number)
        carrier_result = await self.lookup_carrier_info(phone_number)
        risk_result = await self.analyze_phone_risk(phone_number)
        
        if not validation_result.success:
            return validation_result
        
        # Combine all results
        combined_data = {
            'phone_number': phone_number,
            'validation_analysis': validation_result.data,
            'carrier_analysis': carrier_result.data if carrier_result.success else None,
            'risk_analysis': risk_result.data if risk_result.success else None
        }
        
        # Get overall risk score
        overall_risk = max(
            validation_result.data.get('risk_score', 0),
            risk_result.data.get('risk_score', 0) if risk_result.success else 0
        )
        
        return APIResponse(
            success=True,
            data={
                **combined_data,
                'overall_risk_score': overall_risk,
                'overall_risk_level': 'HIGH' if overall_risk > 70 else 'MEDIUM' if overall_risk > 30 else 'LOW',
                'summary': self._generate_phone_summary(combined_data),
                'recommendations': self._generate_phone_recommendations(combined_data)
            },
            api_name='PhoneAPIs'
        )
    
    def _generate_phone_summary(self, data: Dict) -> str:
        """Generate comprehensive phone analysis summary"""
        phone = data['phone_number']
        validation_data = data.get('validation_analysis', {})
        carrier_data = data.get('carrier_analysis', {})
        
        summary_parts = [f"Phone: {phone}"]
        
        validation_score = validation_data.get('validation_score', 0)
        summary_parts.append(f"Validation: {validation_score:.1f}%")
        
        if carrier_data and carrier_data.get('carrier_info'):
            carrier_info = carrier_data['carrier_info']
            if carrier_info.get('carrier_name'):
                summary_parts.append(f"Carrier: {carrier_info['carrier_name']}")
        
        risk_score = validation_data.get('risk_score', 0)
        summary_parts.append(f"Risk: {risk_score:.1f}/100")
        
        return " | ".join(summary_parts)
    
    def _generate_phone_recommendations(self, data: Dict) -> List[str]:
        """Generate list of phone-specific recommendations"""
        recommendations = []
        
        validation_data = data.get('validation_analysis', {})
        carrier_data = data.get('carrier_analysis', {})
        risk_data = data.get('risk_analysis', {})
        
        if validation_data.get('recommendation'):
            recommendations.append(f"Validation: {validation_data['recommendation']}")
        
        if carrier_data and carrier_data.get('recommendation'):
            recommendations.append(f"Carrier: {carrier_data['recommendation']}")
        
        if risk_data and risk_data.get('recommendation'):
            recommendations.append(f"Risk Assessment: {risk_data['recommendation']}")
        
        return recommendations

