"""
Email APIs Wrapper for ScamShield AI
Integrates email validation and verification APIs
"""

import asyncio
import re
from typing import Dict, Any, Optional, List
from .base_api import BaseAPIWrapper, APIConfig, APIResponse
import logging

logger = logging.getLogger(__name__)

class EmailAPIWrapper(BaseAPIWrapper):
    """Wrapper for email validation and verification APIs"""
    
    def __init__(self, api_keys: Dict[str, str] = None):
        super().__init__(APIConfig(
            name="EmailAPIs",
            base_url="https://api.email.com",
            rate_limit=60
        ))
        
        self.api_keys = api_keys or {}
        self.apis = self._initialize_apis()
    
    def _initialize_apis(self) -> Dict[str, APIConfig]:
        """Initialize all email API configurations"""
        return {
            'email_validation': APIConfig(
                name='Email Validation',
                base_url='https://api.email-validator.net/api/verify',
                api_key=self.api_keys.get('email_validation'),
                rate_limit=1000,
                cache_ttl=86400,  # 24 hours
                requires_auth=True
            ),
            'cloudmersive': APIConfig(
                name='Cloudmersive Validate',
                base_url='https://api.cloudmersive.com/validate',
                api_key=self.api_keys.get('cloudmersive'),
                rate_limit=800,
                cache_ttl=86400,
                requires_auth=True
            ),
            'mailboxvalidator': APIConfig(
                name='MailboxValidator',
                base_url='https://api.mailboxvalidator.com/v1',
                api_key=self.api_keys.get('mailboxvalidator'),
                rate_limit=1000,
                cache_ttl=86400,
                requires_auth=True
            ),
            'mailboxlayer': APIConfig(
                name='apilayer mailboxlayer',
                base_url='https://apilayer.net/api',
                api_key=self.api_keys.get('mailboxlayer'),
                rate_limit=1000,
                cache_ttl=86400,
                requires_auth=True
            ),
            'verifier': APIConfig(
                name='Verifier',
                base_url='https://verifier.meetchopra.com/verify',
                api_key=self.api_keys.get('verifier'),
                rate_limit=100,
                cache_ttl=86400,
                requires_auth=True
            ),
            'kickbox': APIConfig(
                name='Kickbox',
                base_url='https://api.kickbox.com/v2',
                api_key=None,  # Free tier available
                rate_limit=100,
                cache_ttl=86400,
                requires_auth=False
            ),
            'mailcheck_ai': APIConfig(
                name='MailCheck.ai',
                base_url='https://api.mailcheck.ai/email',
                api_key=None,  # No auth required
                rate_limit=1000,
                cache_ttl=86400,
                requires_auth=False
            ),
            'disify': APIConfig(
                name='Disify',
                base_url='https://www.disify.com/api',
                api_key=None,  # No auth required
                rate_limit=1000,
                cache_ttl=86400,
                requires_auth=False
            ),
            'eva': APIConfig(
                name='EVA',
                base_url='https://api.eva.pingutil.com',
                api_key=None,  # No auth required
                rate_limit=100,
                cache_ttl=86400,
                requires_auth=False
            ),
            'guerrilla_mail': APIConfig(
                name='Guerrilla Mail',
                base_url='https://api.guerrillamail.com/ajax.php',
                api_key=None,  # No auth required
                rate_limit=100,
                cache_ttl=3600,
                requires_auth=False
            )
        }
    
    def get_auth_header_name(self) -> str:
        """Get authentication header name"""
        return 'X-API-Key'
    
    async def health_check(self) -> APIResponse:
        """Check health of all email APIs"""
        results = {}
        
        # Test Disify (no auth required)
        try:
            response = await self.check_disposable_email('test@example.com')
            results['disify'] = response.success
        except:
            results['disify'] = False
        
        return APIResponse(
            success=True,
            data={'health_status': results},
            api_name='EmailAPIs'
        )
    
    def _is_valid_email_format(self, email: str) -> bool:
        """Basic email format validation"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    async def validate_email_deliverability(self, email: str) -> APIResponse:
        """Validate email deliverability across multiple services"""
        if not self._is_valid_email_format(email):
            return APIResponse(
                success=True,
                data={
                    'email': email,
                    'valid_format': False,
                    'deliverable': False,
                    'risk_score': 100,
                    'risk_level': 'HIGH',
                    'recommendation': 'Invalid email format'
                },
                api_name='EmailAPIs'
            )
        
        results = {}
        
        # Email Validation API
        if 'email_validation' in self.api_keys:
            try:
                self.config = self.apis['email_validation']
                response = await self.make_request(
                    '',
                    params={
                        'EmailAddress': email,
                        'APIKey': self.api_keys.get('email_validation')
                    }
                )
                if response.success:
                    data = response.data
                    results['email_validation'] = {
                        'status': data.get('status'),
                        'result': data.get('result'),
                        'reason': data.get('reason'),
                        'disposable': data.get('disposable', False),
                        'role_account': data.get('role_account', False),
                        'free_email': data.get('free_email', False),
                        'syntax_error': data.get('syntax_error', False)
                    }
            except Exception as e:
                logger.error(f"Email Validation API error: {e}")
                results['email_validation'] = {'error': str(e)}
        
        # Cloudmersive
        if 'cloudmersive' in self.api_keys:
            try:
                self.config = self.apis['cloudmersive']
                response = await self.make_request(
                    'email/address/syntaxOnly',
                    method='POST',
                    data={'EmailAddress': email}
                )
                if response.success:
                    syntax_data = response.data
                    
                    # Full validation
                    full_response = await self.make_request(
                        'email/address/full',
                        method='POST',
                        data={'EmailAddress': email}
                    )
                    
                    if full_response.success:
                        full_data = full_response.data
                        results['cloudmersive'] = {
                            'valid_syntax': syntax_data.get('ValidAddress', False),
                            'valid_domain': full_data.get('ValidDomain', False),
                            'valid_smtp': full_data.get('ValidSMTP', False),
                            'catchall': full_data.get('IsCatchall', False),
                            'role': full_data.get('IsRole', False),
                            'disposable': full_data.get('IsDisposable', False),
                            'free_email': full_data.get('IsFreeEmail', False),
                            'domain_type': full_data.get('DomainType')
                        }
            except Exception as e:
                logger.error(f"Cloudmersive error: {e}")
                results['cloudmersive'] = {'error': str(e)}
        
        # MailboxValidator
        if 'mailboxvalidator' in self.api_keys:
            try:
                self.config = self.apis['mailboxvalidator']
                response = await self.make_request(
                    'validation/single',
                    params={
                        'key': self.api_keys.get('mailboxvalidator'),
                        'email': email,
                        'format': 'json'
                    }
                )
                if response.success:
                    data = response.data
                    results['mailboxvalidator'] = {
                        'status': data.get('status'),
                        'result': data.get('result'),
                        'reason': data.get('reason'),
                        'disposable': data.get('is_disposable', False),
                        'role': data.get('is_role', False),
                        'free_email': data.get('is_free', False),
                        'syntax_error': data.get('is_syntax', True),
                        'domain_age': data.get('domain_age'),
                        'mailbox_full': data.get('is_mailbox_full', False)
                    }
            except Exception as e:
                logger.error(f"MailboxValidator error: {e}")
                results['mailboxvalidator'] = {'error': str(e)}
        
        # Mailboxlayer
        if 'mailboxlayer' in self.api_keys:
            try:
                self.config = self.apis['mailboxlayer']
                response = await self.make_request(
                    'check',
                    params={
                        'access_key': self.api_keys.get('mailboxlayer'),
                        'email': email,
                        'smtp': 1,
                        'format': 1
                    }
                )
                if response.success:
                    data = response.data
                    results['mailboxlayer'] = {
                        'valid': data.get('format_valid', False),
                        'smtp_check': data.get('smtp_check', False),
                        'disposable': data.get('disposable', False),
                        'role': data.get('role', False),
                        'free_email': data.get('free', False),
                        'score': data.get('score', 0),
                        'domain': data.get('domain'),
                        'mx_found': data.get('mx_found', False)
                    }
            except Exception as e:
                logger.error(f"Mailboxlayer error: {e}")
                results['mailboxlayer'] = {'error': str(e)}
        
        # Verifier
        if 'verifier' in self.api_keys:
            try:
                self.config = self.apis['verifier']
                response = await self.make_request(
                    f'{email}',
                    params={'token': self.api_keys.get('verifier')}
                )
                if response.success:
                    data = response.data
                    results['verifier'] = {
                        'status': data.get('status'),
                        'result': data.get('result'),
                        'reason': data.get('reason'),
                        'disposable': data.get('disposable', False),
                        'accept_all': data.get('accept_all', False),
                        'role': data.get('role', False)
                    }
            except Exception as e:
                logger.error(f"Verifier error: {e}")
                results['verifier'] = {'error': str(e)}
        
        # Calculate email deliverability score
        deliverability_score = 0
        valid_checks = 0
        risk_factors = []
        
        for api_name, api_result in results.items():
            if 'error' not in api_result:
                valid_checks += 1
                
                # Check various validation results
                if api_result.get('valid_syntax', True) and api_result.get('valid', True):
                    deliverability_score += 20
                
                if api_result.get('valid_smtp', False) or api_result.get('smtp_check', False):
                    deliverability_score += 25
                
                if api_result.get('valid_domain', False) or api_result.get('mx_found', False):
                    deliverability_score += 15
                
                # Risk factors
                if api_result.get('disposable', False):
                    risk_factors.append('Disposable email detected')
                    deliverability_score -= 30
                
                if api_result.get('role', False):
                    risk_factors.append('Role-based email account')
                    deliverability_score -= 10
                
                if api_result.get('syntax_error', False):
                    risk_factors.append('Syntax error detected')
                    deliverability_score -= 40
                
                if api_result.get('mailbox_full', False):
                    risk_factors.append('Mailbox appears full')
                    deliverability_score -= 20
        
        # Normalize score
        if valid_checks > 0:
            deliverability_score = max(0, min(100, deliverability_score / valid_checks * 100))
        
        # Invert to risk score (higher deliverability = lower risk)
        risk_score = 100 - deliverability_score
        
        return APIResponse(
            success=True,
            data={
                'email': email,
                'valid_format': True,
                'deliverability_score': deliverability_score,
                'risk_score': risk_score,
                'risk_level': 'HIGH' if risk_score > 70 else 'MEDIUM' if risk_score > 30 else 'LOW',
                'risk_factors': risk_factors,
                'detailed_results': results,
                'recommendation': self._get_deliverability_recommendation(risk_score, risk_factors)
            },
            api_name='EmailAPIs'
        )
    
    async def check_disposable_email(self, email: str) -> APIResponse:
        """Check if email is from a disposable email service"""
        results = {}
        
        # Disify (free, no auth)
        try:
            self.config = self.apis['disify']
            domain = email.split('@')[1] if '@' in email else email
            response = await self.make_request(
                'email',
                params={'domain': domain}
            )
            if response.success:
                data = response.data
                results['disify'] = {
                    'disposable': data.get('disposable', False),
                    'domain': data.get('domain'),
                    'dns_valid': data.get('dns_valid', True)
                }
        except Exception as e:
            logger.error(f"Disify error: {e}")
            results['disify'] = {'error': str(e)}
        
        # MailCheck.ai (free, no auth)
        try:
            self.config = self.apis['mailcheck_ai']
            response = await self.make_request(f'{email}')
            if response.success:
                data = response.data
                results['mailcheck_ai'] = {
                    'disposable': data.get('disposable', False),
                    'valid': data.get('valid', True),
                    'block': data.get('block', False),
                    'domain': data.get('domain')
                }
        except Exception as e:
            logger.error(f"MailCheck.ai error: {e}")
            results['mailcheck_ai'] = {'error': str(e)}
        
        # EVA (free, no auth)
        try:
            self.config = self.apis['eva']
            response = await self.make_request(f'email/{email}')
            if response.success:
                data = response.data
                results['eva'] = {
                    'deliverable': data.get('deliverable', True),
                    'full_inbox': data.get('full_inbox', False),
                    'host_exists': data.get('host_exists', True),
                    'catch_all': data.get('catch_all', False)
                }
        except Exception as e:
            logger.error(f"EVA error: {e}")
            results['eva'] = {'error': str(e)}
        
        # Determine if email is disposable
        disposable_count = 0
        total_checks = 0
        
        for api_name, api_result in results.items():
            if 'error' not in api_result:
                total_checks += 1
                if api_result.get('disposable', False) or api_result.get('block', False):
                    disposable_count += 1
        
        is_disposable = disposable_count > 0
        confidence = (disposable_count / total_checks * 100) if total_checks > 0 else 0
        
        return APIResponse(
            success=True,
            data={
                'email': email,
                'is_disposable': is_disposable,
                'confidence': confidence,
                'disposable_detections': disposable_count,
                'total_checks': total_checks,
                'detailed_results': results,
                'recommendation': self._get_disposable_recommendation(is_disposable, confidence)
            },
            api_name='EmailAPIs'
        )
    
    async def check_email_breach_status(self, email: str) -> APIResponse:
        """Check if email has been involved in data breaches"""
        # Note: This would typically integrate with HaveIBeenPwned API
        # For now, we'll provide a placeholder structure
        
        results = {
            'haveibeenpwned': {
                'note': 'HaveIBeenPwned integration requires separate implementation',
                'breaches_found': 0,
                'paste_count': 0,
                'breach_names': []
            }
        }
        
        return APIResponse(
            success=True,
            data={
                'email': email,
                'breach_status': 'unknown',
                'detailed_results': results,
                'recommendation': 'Implement HaveIBeenPwned API integration for breach checking'
            },
            api_name='EmailAPIs'
        )
    
    async def analyze_email_domain(self, domain: str) -> APIResponse:
        """Analyze email domain characteristics"""
        results = {}
        
        # Check if domain is a free email provider
        free_email_domains = {
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com',
            'icloud.com', 'protonmail.com', 'yandex.com', 'mail.com', 'zoho.com'
        }
        
        is_free_email = domain.lower() in free_email_domains
        
        # Basic domain analysis
        results['domain_analysis'] = {
            'domain': domain,
            'is_free_email': is_free_email,
            'tld': domain.split('.')[-1] if '.' in domain else '',
            'subdomain_count': len(domain.split('.')) - 2
        }
        
        # Check disposable status
        disposable_result = await self.check_disposable_email(f'test@{domain}')
        if disposable_result.success:
            results['disposable_check'] = disposable_result.data
        
        # Calculate domain risk score
        domain_risk = 0
        
        if is_free_email:
            domain_risk += 10  # Slight risk increase for free emails
        
        if disposable_result.success and disposable_result.data.get('is_disposable'):
            domain_risk += 80  # High risk for disposable domains
        
        # Check TLD risk
        high_risk_tlds = ['tk', 'ml', 'ga', 'cf', 'click', 'download']
        if results['domain_analysis']['tld'].lower() in high_risk_tlds:
            domain_risk += 40
        
        domain_risk = min(100, domain_risk)
        
        return APIResponse(
            success=True,
            data={
                'domain': domain,
                'risk_score': domain_risk,
                'risk_level': 'HIGH' if domain_risk > 70 else 'MEDIUM' if domain_risk > 30 else 'LOW',
                'detailed_results': results,
                'recommendation': self._get_domain_recommendation(domain_risk, results)
            },
            api_name='EmailAPIs'
        )
    
    def _get_deliverability_recommendation(self, risk_score: float, risk_factors: List[str]) -> str:
        """Generate recommendation based on email deliverability analysis"""
        if risk_score > 70:
            return f"HIGH RISK: Email likely undeliverable. Issues: {', '.join(risk_factors)}"
        elif risk_score > 30:
            return f"MEDIUM RISK: Email may have delivery issues. Consider verification: {', '.join(risk_factors)}"
        else:
            return "LOW RISK: Email appears deliverable and legitimate."
    
    def _get_disposable_recommendation(self, is_disposable: bool, confidence: float) -> str:
        """Generate recommendation based on disposable email check"""
        if is_disposable and confidence > 50:
            return f"HIGH RISK: Disposable email detected with {confidence:.1f}% confidence. Consider blocking."
        elif is_disposable:
            return f"MEDIUM RISK: Possible disposable email ({confidence:.1f}% confidence). Verify through other means."
        else:
            return "LOW RISK: Email does not appear to be from a disposable service."
    
    def _get_domain_recommendation(self, risk_score: float, results: Dict) -> str:
        """Generate recommendation based on domain analysis"""
        if risk_score > 70:
            return "HIGH RISK: Domain shows multiple risk factors. Consider blocking or requiring additional verification."
        elif risk_score > 30:
            return "MEDIUM RISK: Domain has some concerning characteristics. Monitor closely."
        else:
            return "LOW RISK: Domain appears legitimate for email communication."
    
    async def comprehensive_email_analysis(self, email: str) -> APIResponse:
        """Perform comprehensive email analysis across all available checks"""
        results = {}
        
        # Basic format validation
        if not self._is_valid_email_format(email):
            return APIResponse(
                success=True,
                data={
                    'email': email,
                    'valid_format': False,
                    'overall_risk_score': 100,
                    'overall_risk_level': 'HIGH',
                    'recommendation': 'Invalid email format - reject immediately'
                },
                api_name='EmailAPIs'
            )
        
        # Deliverability check
        deliverability_result = await self.validate_email_deliverability(email)
        if deliverability_result.success:
            results['deliverability_analysis'] = deliverability_result.data
        
        # Disposable email check
        disposable_result = await self.check_disposable_email(email)
        if disposable_result.success:
            results['disposable_analysis'] = disposable_result.data
        
        # Domain analysis
        domain = email.split('@')[1] if '@' in email else ''
        if domain:
            domain_result = await self.analyze_email_domain(domain)
            if domain_result.success:
                results['domain_analysis'] = domain_result.data
        
        # Breach status check
        breach_result = await self.check_email_breach_status(email)
        if breach_result.success:
            results['breach_analysis'] = breach_result.data
        
        # Calculate overall email risk score
        risk_scores = []
        for analysis in results.values():
            if 'risk_score' in analysis:
                risk_scores.append(analysis['risk_score'])
        
        overall_risk = max(risk_scores) if risk_scores else 0  # Use highest risk score
        
        # Additional risk factors
        risk_factors = []
        for analysis in results.values():
            if 'risk_factors' in analysis:
                risk_factors.extend(analysis['risk_factors'])
        
        return APIResponse(
            success=True,
            data={
                'email': email,
                'valid_format': True,
                'overall_risk_score': overall_risk,
                'overall_risk_level': 'HIGH' if overall_risk > 70 else 'MEDIUM' if overall_risk > 30 else 'LOW',
                'risk_factors': risk_factors,
                'detailed_analysis': results,
                'summary': self._generate_email_summary(overall_risk, results),
                'recommendations': self._generate_email_recommendations(results)
            },
            api_name='EmailAPIs'
        )
    
    def _generate_email_summary(self, overall_risk: float, results: Dict) -> str:
        """Generate comprehensive email analysis summary"""
        summary_parts = [f"Overall Email Risk: {overall_risk:.1f}/100"]
        
        if 'deliverability_analysis' in results:
            deliverability = results['deliverability_analysis']['deliverability_score']
            summary_parts.append(f"Deliverability: {deliverability:.1f}%")
        
        if 'disposable_analysis' in results and results['disposable_analysis']['is_disposable']:
            confidence = results['disposable_analysis']['confidence']
            summary_parts.append(f"Disposable Email Detected ({confidence:.1f}% confidence)")
        
        if 'domain_analysis' in results:
            domain_risk = results['domain_analysis']['risk_score']
            summary_parts.append(f"Domain Risk: {domain_risk:.1f}/100")
        
        return " | ".join(summary_parts)
    
    def _generate_email_recommendations(self, results: Dict) -> List[str]:
        """Generate list of email-specific recommendations"""
        recommendations = []
        
        for analysis_type, analysis_data in results.items():
            if 'recommendation' in analysis_data and analysis_data.get('risk_level') in ['HIGH', 'MEDIUM']:
                recommendations.append(f"{analysis_type.replace('_analysis', '').title()}: {analysis_data['recommendation']}")
        
        return recommendations

