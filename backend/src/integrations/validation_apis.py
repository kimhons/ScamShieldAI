"""
Validation APIs Wrapper for ScamShield AI
Integrates data validation and verification APIs
"""

import asyncio
import re
from typing import Dict, Any, Optional, List
from .base_api import BaseAPIWrapper, APIConfig, APIResponse
import logging

logger = logging.getLogger(__name__)

class ValidationAPIWrapper(BaseAPIWrapper):
    """Wrapper for data validation and verification APIs"""
    
    def __init__(self, api_keys: Dict[str, str] = None):
        super().__init__(APIConfig(
            name="ValidationAPIs",
            base_url="https://api.validation.com",
            rate_limit=60
        ))
        
        self.api_keys = api_keys or {}
        self.apis = self._initialize_apis()
    
    def _initialize_apis(self) -> Dict[str, APIConfig]:
        """Initialize all validation API configurations"""
        return {
            'cloudmersive_validate': APIConfig(
                name='Cloudmersive Validate',
                base_url='https://api.cloudmersive.com/validate',
                api_key=self.api_keys.get('cloudmersive'),
                rate_limit=800,
                cache_ttl=3600,
                requires_auth=True
            ),
            'postman_echo': APIConfig(
                name='Postman Echo',
                base_url='https://postman-echo.com',
                api_key=None,  # No auth required
                rate_limit=1000,
                cache_ttl=300,  # 5 minutes
                requires_auth=False
            ),
            'json_test': APIConfig(
                name='JSON Test',
                base_url='https://validate.jsontest.com',
                api_key=None,  # No auth required
                rate_limit=1000,
                cache_ttl=300,
                requires_auth=False
            ),
            'vat_layer': APIConfig(
                name='apilayer vatlayer',
                base_url='https://apilayer.net/api',
                api_key=self.api_keys.get('vat_layer'),
                rate_limit=1000,
                cache_ttl=86400,  # 24 hours
                requires_auth=True
            ),
            'bank_validation': APIConfig(
                name='Bank Validation',
                base_url='https://api.bank-validation.com/v1',
                api_key=self.api_keys.get('bank_validation'),
                rate_limit=1000,
                cache_ttl=86400,
                requires_auth=True
            ),
            'iban_validation': APIConfig(
                name='IBAN Validation',
                base_url='https://api.iban-validation.com/v1',
                api_key=self.api_keys.get('iban_validation'),
                rate_limit=1000,
                cache_ttl=86400,
                requires_auth=True
            ),
            'credit_card_validation': APIConfig(
                name='Credit Card Validation',
                base_url='https://api.credit-card-validation.com/v1',
                api_key=self.api_keys.get('credit_card_validation'),
                rate_limit=1000,
                cache_ttl=300,  # Short cache for security
                requires_auth=True
            ),
            'regex_validation': APIConfig(
                name='Regex Validation',
                base_url='https://api.regex-validation.com/v1',
                api_key=self.api_keys.get('regex_validation'),
                rate_limit=1000,
                cache_ttl=3600,
                requires_auth=True
            )
        }
    
    def get_auth_header_name(self) -> str:
        """Get authentication header name"""
        return 'X-API-Key'
    
    async def health_check(self) -> APIResponse:
        """Check health of all validation APIs"""
        results = {}
        
        # Test JSON Test (no auth required)
        try:
            response = await self.validate_json('{"test": "data"}')
            results['json_test'] = response.success
        except:
            results['json_test'] = False
        
        return APIResponse(
            success=True,
            data={'health_status': results},
            api_name='ValidationAPIs'
        )
    
    async def validate_json(self, json_string: str) -> APIResponse:
        """Validate JSON format and structure"""
        results = {}
        
        # JSON Test (free, no auth)
        try:
            self.config = self.apis['json_test']
            response = await self.make_request(
                '',
                params={'json': json_string}
            )
            if response.success:
                data = response.data
                results['json_test'] = {
                    'valid': data.get('validate', False),
                    'size': data.get('size'),
                    'parse_time_nanoseconds': data.get('parse_time_nanoseconds'),
                    'empty': data.get('empty', False),
                    'error': data.get('error')
                }
        except Exception as e:
            logger.error(f"JSON Test error: {e}")
            results['json_test'] = {'error': str(e)}
        
        # Cloudmersive JSON validation
        if 'cloudmersive' in self.api_keys:
            try:
                self.config = self.apis['cloudmersive_validate']
                response = await self.make_request(
                    'text-input/validate/json',
                    method='POST',
                    data={'InputText': json_string}
                )
                if response.success:
                    data = response.data
                    results['cloudmersive'] = {
                        'valid': data.get('ValidJSON', False),
                        'error_position': data.get('ErrorPosition'),
                        'error_line': data.get('ErrorLine'),
                        'error_details': data.get('ErrorDetails')
                    }
            except Exception as e:
                logger.error(f"Cloudmersive JSON validation error: {e}")
                results['cloudmersive'] = {'error': str(e)}
        
        # Determine overall validity
        is_valid = any(result.get('valid', False) for result in results.values() if 'error' not in result)
        
        return APIResponse(
            success=True,
            data={
                'json_string': json_string[:100] + '...' if len(json_string) > 100 else json_string,
                'is_valid': is_valid,
                'detailed_results': results,
                'recommendation': 'Valid JSON format' if is_valid else 'Invalid JSON - check syntax and structure'
            },
            api_name='ValidationAPIs'
        )
    
    async def validate_credit_card(self, card_number: str) -> APIResponse:
        """Validate credit card number format and type"""
        # Remove spaces and non-digits
        clean_number = re.sub(r'[^\d]', '', card_number)
        
        results = {}
        
        # Basic Luhn algorithm check (local validation)
        luhn_valid = self._luhn_check(clean_number)
        card_type = self._detect_card_type(clean_number)
        
        results['local_validation'] = {
            'luhn_valid': luhn_valid,
            'card_type': card_type,
            'length_valid': len(clean_number) in [13, 14, 15, 16, 17, 18, 19],
            'clean_number_length': len(clean_number)
        }
        
        # Cloudmersive credit card validation
        if 'cloudmersive' in self.api_keys:
            try:
                self.config = self.apis['cloudmersive_validate']
                response = await self.make_request(
                    'payment/cards/validate',
                    method='POST',
                    data={'CardNumber': clean_number}
                )
                if response.success:
                    data = response.data
                    results['cloudmersive'] = {
                        'is_valid': data.get('IsValid', False),
                        'card_type': data.get('CardType'),
                        'card_type_code': data.get('CardTypeCode'),
                        'is_luhn_valid': data.get('IsLuhnValid', False),
                        'cvv_length': data.get('CvvLength')
                    }
            except Exception as e:
                logger.error(f"Cloudmersive credit card validation error: {e}")
                results['cloudmersive'] = {'error': str(e)}
        
        # Credit Card Validation API (if available)
        if 'credit_card_validation' in self.api_keys:
            try:
                self.config = self.apis['credit_card_validation']
                response = await self.make_request(
                    'validate',
                    params={
                        'card_number': clean_number,
                        'api_key': self.api_keys.get('credit_card_validation')
                    }
                )
                if response.success:
                    data = response.data
                    results['credit_card_validation'] = {
                        'valid': data.get('valid', False),
                        'card_type': data.get('card_type'),
                        'issuer': data.get('issuer'),
                        'country': data.get('country'),
                        'luhn_valid': data.get('luhn_valid', False)
                    }
            except Exception as e:
                logger.error(f"Credit Card Validation API error: {e}")
                results['credit_card_validation'] = {'error': str(e)}
        
        # Determine overall validity
        is_valid = luhn_valid and len(clean_number) >= 13
        
        # Calculate risk score
        risk_score = 0
        if not luhn_valid:
            risk_score += 50
        if not card_type or card_type == 'Unknown':
            risk_score += 30
        if len(clean_number) < 13 or len(clean_number) > 19:
            risk_score += 40
        
        risk_score = min(100, risk_score)
        
        return APIResponse(
            success=True,
            data={
                'card_number': '*' * (len(clean_number) - 4) + clean_number[-4:] if len(clean_number) >= 4 else '****',
                'is_valid': is_valid,
                'card_type': card_type,
                'risk_score': risk_score,
                'risk_level': 'HIGH' if risk_score > 70 else 'MEDIUM' if risk_score > 30 else 'LOW',
                'detailed_results': results,
                'recommendation': self._get_card_recommendation(is_valid, risk_score, card_type)
            },
            api_name='ValidationAPIs'
        )
    
    def _luhn_check(self, card_number: str) -> bool:
        """Perform Luhn algorithm check on credit card number"""
        if not card_number.isdigit():
            return False
        
        digits = [int(d) for d in card_number]
        checksum = 0
        
        # Process digits from right to left
        for i in range(len(digits) - 2, -1, -1):
            if (len(digits) - i) % 2 == 0:  # Every second digit from right
                doubled = digits[i] * 2
                checksum += doubled if doubled < 10 else doubled - 9
            else:
                checksum += digits[i]
        
        return (checksum + digits[-1]) % 10 == 0
    
    def _detect_card_type(self, card_number: str) -> str:
        """Detect credit card type based on number pattern"""
        if not card_number.isdigit():
            return 'Unknown'
        
        # Visa
        if card_number.startswith('4') and len(card_number) in [13, 16, 19]:
            return 'Visa'
        
        # Mastercard
        if (card_number.startswith(('51', '52', '53', '54', '55')) or
            (card_number.startswith('2') and 2221 <= int(card_number[:4]) <= 2720)) and len(card_number) == 16:
            return 'Mastercard'
        
        # American Express
        if card_number.startswith(('34', '37')) and len(card_number) == 15:
            return 'American Express'
        
        # Discover
        if (card_number.startswith('6011') or card_number.startswith('65') or
            (card_number.startswith('644') and len(card_number) == 16) or
            (card_number.startswith('622') and 622126 <= int(card_number[:6]) <= 622925)) and len(card_number) == 16:
            return 'Discover'
        
        # Diners Club
        if (card_number.startswith(('300', '301', '302', '303', '304', '305', '36', '38')) and
            len(card_number) == 14):
            return 'Diners Club'
        
        # JCB
        if card_number.startswith(('2131', '1800')) and len(card_number) == 15:
            return 'JCB'
        if card_number.startswith('35') and len(card_number) == 16:
            return 'JCB'
        
        return 'Unknown'
    
    async def validate_iban(self, iban: str) -> APIResponse:
        """Validate International Bank Account Number (IBAN)"""
        # Clean IBAN (remove spaces and convert to uppercase)
        clean_iban = re.sub(r'[^\w]', '', iban.upper())
        
        results = {}
        
        # Basic IBAN validation (local)
        local_valid = self._validate_iban_local(clean_iban)
        
        results['local_validation'] = {
            'format_valid': local_valid,
            'length': len(clean_iban),
            'country_code': clean_iban[:2] if len(clean_iban) >= 2 else '',
            'check_digits': clean_iban[2:4] if len(clean_iban) >= 4 else ''
        }
        
        # IBAN Validation API (if available)
        if 'iban_validation' in self.api_keys:
            try:
                self.config = self.apis['iban_validation']
                response = await self.make_request(
                    'validate',
                    params={
                        'iban': clean_iban,
                        'api_key': self.api_keys.get('iban_validation')
                    }
                )
                if response.success:
                    data = response.data
                    results['iban_validation'] = {
                        'valid': data.get('valid', False),
                        'country': data.get('country'),
                        'country_code': data.get('country_code'),
                        'bank_code': data.get('bank_code'),
                        'account_number': data.get('account_number'),
                        'checksum_valid': data.get('checksum_valid', False)
                    }
            except Exception as e:
                logger.error(f"IBAN Validation API error: {e}")
                results['iban_validation'] = {'error': str(e)}
        
        # Cloudmersive IBAN validation
        if 'cloudmersive' in self.api_keys:
            try:
                self.config = self.apis['cloudmersive_validate']
                response = await self.make_request(
                    'bank-account/iban/validate',
                    method='POST',
                    data={'IBAN': clean_iban}
                )
                if response.success:
                    data = response.data
                    results['cloudmersive'] = {
                        'is_valid': data.get('IsValid', False),
                        'country_code': data.get('CountryCode'),
                        'country_name': data.get('CountryName'),
                        'bank_code': data.get('BankCode'),
                        'account_number': data.get('AccountNumber')
                    }
            except Exception as e:
                logger.error(f"Cloudmersive IBAN validation error: {e}")
                results['cloudmersive'] = {'error': str(e)}
        
        # Determine overall validity
        is_valid = local_valid or any(
            result.get('valid', False) or result.get('is_valid', False)
            for result in results.values() if 'error' not in result
        )
        
        return APIResponse(
            success=True,
            data={
                'iban': clean_iban,
                'is_valid': is_valid,
                'country_code': clean_iban[:2] if len(clean_iban) >= 2 else '',
                'detailed_results': results,
                'recommendation': 'Valid IBAN format' if is_valid else 'Invalid IBAN - check format and checksum'
            },
            api_name='ValidationAPIs'
        )
    
    def _validate_iban_local(self, iban: str) -> bool:
        """Local IBAN validation using mod-97 algorithm"""
        if len(iban) < 4:
            return False
        
        # Check if country code is alphabetic
        if not iban[:2].isalpha():
            return False
        
        # Check if check digits are numeric
        if not iban[2:4].isdigit():
            return False
        
        # Rearrange: move first 4 characters to end
        rearranged = iban[4:] + iban[:4]
        
        # Replace letters with numbers (A=10, B=11, ..., Z=35)
        numeric_string = ''
        for char in rearranged:
            if char.isalpha():
                numeric_string += str(ord(char) - ord('A') + 10)
            else:
                numeric_string += char
        
        # Check if all characters are now numeric
        if not numeric_string.isdigit():
            return False
        
        # Perform mod-97 check
        return int(numeric_string) % 97 == 1
    
    async def validate_vat_number(self, vat_number: str, country_code: str = None) -> APIResponse:
        """Validate VAT (Value Added Tax) number"""
        results = {}
        
        # VAT Layer (paid)
        if 'vat_layer' in self.api_keys:
            try:
                self.config = self.apis['vat_layer']
                params = {
                    'access_key': self.api_keys.get('vat_layer'),
                    'vat_number': vat_number
                }
                if country_code:
                    params['country_code'] = country_code
                
                response = await self.make_request('validate', params=params)
                if response.success:
                    data = response.data
                    results['vat_layer'] = {
                        'valid': data.get('valid', False),
                        'database': data.get('database'),
                        'format_valid': data.get('format_valid', False),
                        'country_code': data.get('country_code'),
                        'vat_number': data.get('vat_number'),
                        'company_name': data.get('company_name'),
                        'company_address': data.get('company_address'),
                        'query': data.get('query')
                    }
            except Exception as e:
                logger.error(f"VAT Layer error: {e}")
                results['vat_layer'] = {'error': str(e)}
        
        # Basic format validation (local)
        format_valid = self._validate_vat_format(vat_number, country_code)
        results['local_validation'] = {
            'format_valid': format_valid,
            'detected_country': self._detect_vat_country(vat_number),
            'clean_number': re.sub(r'[^\w]', '', vat_number.upper())
        }
        
        # Determine overall validity
        is_valid = format_valid or any(
            result.get('valid', False) for result in results.values() if 'error' not in result
        )
        
        return APIResponse(
            success=True,
            data={
                'vat_number': vat_number,
                'country_code': country_code,
                'is_valid': is_valid,
                'detailed_results': results,
                'recommendation': 'Valid VAT number' if is_valid else 'Invalid VAT number - verify format and registration'
            },
            api_name='ValidationAPIs'
        )
    
    def _validate_vat_format(self, vat_number: str, country_code: str = None) -> bool:
        """Basic VAT number format validation"""
        clean_vat = re.sub(r'[^\w]', '', vat_number.upper())
        
        # If no country code provided, try to detect from VAT number
        if not country_code:
            country_code = self._detect_vat_country(clean_vat)
        
        if not country_code:
            return False
        
        # Basic patterns for common countries
        patterns = {
            'GB': r'^GB\d{9}$|^GB\d{12}$|^GBGD\d{3}$|^GBHA\d{3}$',
            'DE': r'^DE\d{9}$',
            'FR': r'^FR[A-Z0-9]{2}\d{9}$',
            'IT': r'^IT\d{11}$',
            'ES': r'^ES[A-Z0-9]\d{7}[A-Z0-9]$',
            'NL': r'^NL\d{9}B\d{2}$',
            'BE': r'^BE0\d{9}$',
            'AT': r'^ATU\d{8}$',
            'DK': r'^DK\d{8}$',
            'SE': r'^SE\d{12}$',
            'FI': r'^FI\d{8}$',
            'IE': r'^IE\d[A-Z0-9]\d{5}[A-Z]$|^IE\d{7}[A-Z]{2}$',
            'PT': r'^PT\d{9}$',
            'LU': r'^LU\d{8}$',
            'PL': r'^PL\d{10}$',
            'CZ': r'^CZ\d{8,10}$',
            'SK': r'^SK\d{10}$',
            'HU': r'^HU\d{8}$',
            'SI': r'^SI\d{8}$',
            'MT': r'^MT\d{8}$',
            'CY': r'^CY\d{8}[A-Z]$',
            'LV': r'^LV\d{11}$',
            'LT': r'^LT\d{9}$|^LT\d{12}$',
            'EE': r'^EE\d{9}$',
            'HR': r'^HR\d{11}$',
            'BG': r'^BG\d{9,10}$',
            'RO': r'^RO\d{2,10}$',
            'GR': r'^EL\d{9}$'
        }
        
        pattern = patterns.get(country_code.upper())
        if pattern:
            return bool(re.match(pattern, clean_vat))
        
        return False
    
    def _detect_vat_country(self, vat_number: str) -> Optional[str]:
        """Detect country code from VAT number prefix"""
        clean_vat = re.sub(r'[^\w]', '', vat_number.upper())
        
        if len(clean_vat) < 2:
            return None
        
        # Check for country prefixes
        country_prefixes = {
            'AT': 'ATU', 'BE': 'BE', 'BG': 'BG', 'CY': 'CY', 'CZ': 'CZ',
            'DE': 'DE', 'DK': 'DK', 'EE': 'EE', 'EL': 'EL', 'ES': 'ES',
            'FI': 'FI', 'FR': 'FR', 'GB': 'GB', 'HR': 'HR', 'HU': 'HU',
            'IE': 'IE', 'IT': 'IT', 'LT': 'LT', 'LU': 'LU', 'LV': 'LV',
            'MT': 'MT', 'NL': 'NL', 'PL': 'PL', 'PT': 'PT', 'RO': 'RO',
            'SE': 'SE', 'SI': 'SI', 'SK': 'SK'
        }
        
        for country, prefix in country_prefixes.items():
            if clean_vat.startswith(prefix):
                return country
        
        return None
    
    async def validate_url(self, url: str) -> APIResponse:
        """Validate URL format and accessibility"""
        results = {}
        
        # Basic URL format validation (local)
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        format_valid = bool(url_pattern.match(url))
        
        results['local_validation'] = {
            'format_valid': format_valid,
            'protocol': url.split('://')[0] if '://' in url else None,
            'has_domain': '.' in url.split('://')[1].split('/')[0] if '://' in url else False,
            'length': len(url)
        }
        
        # Postman Echo URL validation (free)
        try:
            self.config = self.apis['postman_echo']
            response = await self.make_request(
                'get',
                params={'url': url}
            )
            if response.success:
                results['postman_echo'] = {
                    'accessible': True,
                    'response_received': True,
                    'args': response.data.get('args', {}),
                    'headers': response.data.get('headers', {}),
                    'url': response.data.get('url')
                }
        except Exception as e:
            logger.error(f"Postman Echo error: {e}")
            results['postman_echo'] = {'error': str(e), 'accessible': False}
        
        # Cloudmersive URL validation
        if 'cloudmersive' in self.api_keys:
            try:
                self.config = self.apis['cloudmersive_validate']
                response = await self.make_request(
                    'net/is-url-valid',
                    method='POST',
                    data={'URL': url}
                )
                if response.success:
                    data = response.data
                    results['cloudmersive'] = {
                        'is_valid': data.get('IsValid', False),
                        'is_accessible': data.get('IsAccessible', False),
                        'response_code': data.get('ResponseCode'),
                        'response_time': data.get('ResponseTime'),
                        'is_ssl': data.get('IsSSL', False)
                    }
            except Exception as e:
                logger.error(f"Cloudmersive URL validation error: {e}")
                results['cloudmersive'] = {'error': str(e)}
        
        # Determine overall validity and accessibility
        is_valid = format_valid
        is_accessible = any(
            result.get('accessible', False) or result.get('is_accessible', False)
            for result in results.values() if 'error' not in result
        )
        
        # Calculate risk score
        risk_score = 0
        if not format_valid:
            risk_score += 50
        if not is_accessible:
            risk_score += 30
        if not url.startswith('https://'):
            risk_score += 20
        
        risk_score = min(100, risk_score)
        
        return APIResponse(
            success=True,
            data={
                'url': url,
                'is_valid': is_valid,
                'is_accessible': is_accessible,
                'risk_score': risk_score,
                'risk_level': 'HIGH' if risk_score > 70 else 'MEDIUM' if risk_score > 30 else 'LOW',
                'detailed_results': results,
                'recommendation': self._get_url_recommendation(is_valid, is_accessible, risk_score)
            },
            api_name='ValidationAPIs'
        )
    
    def _get_card_recommendation(self, is_valid: bool, risk_score: float, card_type: str) -> str:
        """Generate recommendation for credit card validation"""
        if not is_valid or risk_score > 70:
            return "HIGH RISK: Invalid credit card format. Reject transaction."
        elif risk_score > 30:
            return f"MEDIUM RISK: {card_type} card format valid but requires additional verification."
        else:
            return f"LOW RISK: Valid {card_type} card format detected."
    
    def _get_url_recommendation(self, is_valid: bool, is_accessible: bool, risk_score: float) -> str:
        """Generate recommendation for URL validation"""
        if not is_valid:
            return "HIGH RISK: Invalid URL format. Block access."
        elif not is_accessible:
            return "MEDIUM RISK: URL format valid but not accessible. Verify before use."
        elif risk_score > 30:
            return "MEDIUM RISK: URL accessible but has security concerns (non-HTTPS)."
        else:
            return "LOW RISK: Valid and accessible URL."
    
    async def comprehensive_validation_suite(self, data: Dict[str, Any]) -> APIResponse:
        """Run comprehensive validation across multiple data types"""
        results = {}
        
        # Validate different data types based on what's provided
        if 'json' in data:
            json_result = await self.validate_json(data['json'])
            results['json_validation'] = json_result.data
        
        if 'credit_card' in data:
            card_result = await self.validate_credit_card(data['credit_card'])
            results['credit_card_validation'] = card_result.data
        
        if 'iban' in data:
            iban_result = await self.validate_iban(data['iban'])
            results['iban_validation'] = iban_result.data
        
        if 'vat_number' in data:
            vat_result = await self.validate_vat_number(
                data['vat_number'],
                data.get('country_code')
            )
            results['vat_validation'] = vat_result.data
        
        if 'url' in data:
            url_result = await self.validate_url(data['url'])
            results['url_validation'] = url_result.data
        
        # Calculate overall validation score
        validation_scores = []
        for validation_type, validation_data in results.items():
            if validation_data.get('is_valid'):
                validation_scores.append(100)
            else:
                validation_scores.append(0)
        
        overall_score = sum(validation_scores) / len(validation_scores) if validation_scores else 0
        
        return APIResponse(
            success=True,
            data={
                'overall_validation_score': overall_score,
                'overall_status': 'PASS' if overall_score > 70 else 'PARTIAL' if overall_score > 30 else 'FAIL',
                'validations_performed': len(results),
                'detailed_results': results,
                'summary': self._generate_validation_summary(overall_score, results),
                'recommendations': self._generate_validation_recommendations(results)
            },
            api_name='ValidationAPIs'
        )
    
    def _generate_validation_summary(self, overall_score: float, results: Dict) -> str:
        """Generate comprehensive validation summary"""
        summary_parts = [f"Overall Validation: {overall_score:.1f}%"]
        
        passed_validations = sum(1 for r in results.values() if r.get('is_valid'))
        total_validations = len(results)
        
        summary_parts.append(f"Passed: {passed_validations}/{total_validations}")
        
        # Add specific validation results
        for validation_type, validation_data in results.items():
            status = "✓" if validation_data.get('is_valid') else "✗"
            validation_name = validation_type.replace('_validation', '').upper()
            summary_parts.append(f"{validation_name}: {status}")
        
        return " | ".join(summary_parts)
    
    def _generate_validation_recommendations(self, results: Dict) -> List[str]:
        """Generate list of validation-specific recommendations"""
        recommendations = []
        
        for validation_type, validation_data in results.items():
            if 'recommendation' in validation_data:
                validation_name = validation_type.replace('_validation', '').title()
                recommendations.append(f"{validation_name}: {validation_data['recommendation']}")
        
        return recommendations

