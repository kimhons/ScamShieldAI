"""
Security APIs Wrapper for ScamShield AI
Integrates critical security and threat intelligence APIs
"""

import asyncio
from typing import Dict, Any, Optional, List
from .base_api import BaseAPIWrapper, APIConfig, APIResponse
import logging

logger = logging.getLogger(__name__)

class SecurityAPIWrapper(BaseAPIWrapper):
    """Wrapper for security and threat intelligence APIs"""
    
    def __init__(self, api_keys: Dict[str, str] = None):
        # Initialize with default config - will be overridden per API
        super().__init__(APIConfig(
            name="SecurityAPIs",
            base_url="https://api.security.com",
            rate_limit=60
        ))
        
        self.api_keys = api_keys or {}
        self.apis = self._initialize_apis()
    
    def _initialize_apis(self) -> Dict[str, APIConfig]:
        """Initialize all security API configurations"""
        return {
            'abuseipdb': APIConfig(
                name='AbuseIPDB',
                base_url='https://api.abuseipdb.com/api/v2',
                api_key=self.api_keys.get('abuseipdb'),
                rate_limit=1000,  # 1000 requests per day
                cache_ttl=3600,
                requires_auth=True
            ),
            'emailrep': APIConfig(
                name='EmailRep',
                base_url='https://emailrep.io',
                api_key=None,  # No auth required
                rate_limit=100,
                cache_ttl=86400,  # 24 hours
                requires_auth=False
            ),
            'fingerprintjs': APIConfig(
                name='FingerprintJS Pro',
                base_url='https://api.fpjs.io',
                api_key=self.api_keys.get('fingerprintjs'),
                rate_limit=100000,  # 100k per month
                cache_ttl=1800,  # 30 minutes
                requires_auth=True
            ),
            'securitytrails': APIConfig(
                name='SecurityTrails',
                base_url='https://api.securitytrails.com/v1',
                api_key=self.api_keys.get('securitytrails'),
                rate_limit=50,  # 50 per month free
                cache_ttl=604800,  # 1 week
                requires_auth=True
            ),
            'greynoise': APIConfig(
                name='GreyNoise',
                base_url='https://api.greynoise.io/v3',
                api_key=self.api_keys.get('greynoise'),
                rate_limit=1000,
                cache_ttl=3600,
                requires_auth=True
            ),
            'fraudlabs': APIConfig(
                name='FraudLabs Pro',
                base_url='https://api.fraudlabspro.com/v1',
                api_key=self.api_keys.get('fraudlabs'),
                rate_limit=500,
                cache_ttl=1800,
                requires_auth=True
            ),
            'pulsedive': APIConfig(
                name='Pulsedive',
                base_url='https://pulsedive.com/api',
                api_key=self.api_keys.get('pulsedive'),
                rate_limit=30,  # 30 per minute
                cache_ttl=3600,
                requires_auth=True
            ),
            'threatjammer': APIConfig(
                name='Threat Jammer',
                base_url='https://dublin.api.threatjammer.com/v1',
                api_key=self.api_keys.get('threatjammer'),
                rate_limit=1000,
                cache_ttl=3600,
                requires_auth=True
            )
        }
    
    def get_auth_header_name(self) -> str:
        """Get authentication header name"""
        return 'X-API-Key'
    
    async def health_check(self) -> APIResponse:
        """Check health of all security APIs"""
        results = {}
        
        # Test EmailRep (no auth required)
        try:
            response = await self.check_email_reputation('test@example.com')
            results['emailrep'] = response.success
        except:
            results['emailrep'] = False
        
        return APIResponse(
            success=True,
            data={'health_status': results},
            api_name='SecurityAPIs'
        )
    
    async def check_ip_reputation(self, ip_address: str) -> APIResponse:
        """Check IP reputation across multiple security APIs"""
        results = {}
        
        # AbuseIPDB
        if 'abuseipdb' in self.api_keys:
            try:
                self.config = self.apis['abuseipdb']
                response = await self.make_request(
                    'check',
                    params={
                        'ipAddress': ip_address,
                        'maxAgeInDays': 90,
                        'verbose': ''
                    }
                )
                if response.success:
                    data = response.data
                    results['abuseipdb'] = {
                        'abuse_confidence': data.get('abuseConfidencePercentage', 0),
                        'is_public': data.get('isPublic', True),
                        'country_code': data.get('countryCode'),
                        'usage_type': data.get('usageType'),
                        'isp': data.get('isp'),
                        'total_reports': data.get('totalReports', 0),
                        'last_reported': data.get('lastReportedAt')
                    }
            except Exception as e:
                logger.error(f"AbuseIPDB error: {e}")
                results['abuseipdb'] = {'error': str(e)}
        
        # GreyNoise
        if 'greynoise' in self.api_keys:
            try:
                self.config = self.apis['greynoise']
                response = await self.make_request(f'community/{ip_address}')
                if response.success:
                    data = response.data
                    results['greynoise'] = {
                        'noise': data.get('noise', False),
                        'riot': data.get('riot', False),
                        'classification': data.get('classification'),
                        'name': data.get('name'),
                        'link': data.get('link'),
                        'last_seen': data.get('last_seen')
                    }
            except Exception as e:
                logger.error(f"GreyNoise error: {e}")
                results['greynoise'] = {'error': str(e)}
        
        # Threat Jammer
        if 'threatjammer' in self.api_keys:
            try:
                self.config = self.apis['threatjammer']
                response = await self.make_request(
                    'risk',
                    params={'ip': ip_address}
                )
                if response.success:
                    data = response.data
                    results['threatjammer'] = {
                        'risk_score': data.get('risk_score', 0),
                        'risk_level': data.get('risk_level'),
                        'categories': data.get('categories', []),
                        'last_seen': data.get('last_seen')
                    }
            except Exception as e:
                logger.error(f"Threat Jammer error: {e}")
                results['threatjammer'] = {'error': str(e)}
        
        # Calculate overall risk score
        risk_scores = []
        if 'abuseipdb' in results and 'abuse_confidence' in results['abuseipdb']:
            risk_scores.append(results['abuseipdb']['abuse_confidence'])
        if 'threatjammer' in results and 'risk_score' in results['threatjammer']:
            risk_scores.append(results['threatjammer']['risk_score'])
        
        overall_risk = sum(risk_scores) / len(risk_scores) if risk_scores else 0
        
        return APIResponse(
            success=True,
            data={
                'ip_address': ip_address,
                'overall_risk_score': overall_risk,
                'risk_level': 'HIGH' if overall_risk > 75 else 'MEDIUM' if overall_risk > 25 else 'LOW',
                'detailed_results': results,
                'recommendation': self._get_ip_recommendation(overall_risk, results)
            },
            api_name='SecurityAPIs'
        )
    
    async def check_email_reputation(self, email: str) -> APIResponse:
        """Check email reputation and threat level"""
        results = {}
        
        # EmailRep (free, no auth)
        try:
            self.config = self.apis['emailrep']
            response = await self.make_request(f'{email}')
            if response.success:
                data = response.data
                results['emailrep'] = {
                    'reputation': data.get('reputation'),
                    'suspicious': data.get('suspicious', False),
                    'references': data.get('references', 0),
                    'details': data.get('details', {}),
                    'blacklisted': data.get('blacklisted', False),
                    'malicious_activity': data.get('malicious_activity', False),
                    'credentials_leaked': data.get('credentials_leaked', False),
                    'data_breach': data.get('data_breach', False),
                    'spam': data.get('spam', False)
                }
        except Exception as e:
            logger.error(f"EmailRep error: {e}")
            results['emailrep'] = {'error': str(e)}
        
        # Calculate email risk score
        email_risk = 0
        if 'emailrep' in results and 'reputation' in results['emailrep']:
            rep_data = results['emailrep']
            if rep_data.get('suspicious'):
                email_risk += 30
            if rep_data.get('blacklisted'):
                email_risk += 40
            if rep_data.get('malicious_activity'):
                email_risk += 50
            if rep_data.get('credentials_leaked'):
                email_risk += 25
            if rep_data.get('spam'):
                email_risk += 20
            
            # Reputation score (higher is better)
            reputation = rep_data.get('reputation', 'neutral')
            if reputation == 'high':
                email_risk = max(0, email_risk - 30)
            elif reputation == 'low':
                email_risk += 40
        
        email_risk = min(100, email_risk)
        
        return APIResponse(
            success=True,
            data={
                'email': email,
                'risk_score': email_risk,
                'risk_level': 'HIGH' if email_risk > 70 else 'MEDIUM' if email_risk > 30 else 'LOW',
                'detailed_results': results,
                'recommendation': self._get_email_recommendation(email_risk, results)
            },
            api_name='SecurityAPIs'
        )
    
    async def check_domain_reputation(self, domain: str) -> APIResponse:
        """Check domain reputation and WHOIS information"""
        results = {}
        
        # SecurityTrails
        if 'securitytrails' in self.api_keys:
            try:
                self.config = self.apis['securitytrails']
                
                # Get domain details
                response = await self.make_request(f'domain/{domain}')
                if response.success:
                    data = response.data
                    results['securitytrails'] = {
                        'alexa_rank': data.get('alexa_rank'),
                        'apex_domain': data.get('apex_domain'),
                        'hostname': data.get('hostname'),
                        'subdomain_count': data.get('subdomain_count', 0),
                        'whois': data.get('whois', {}),
                        'current_dns': data.get('current_dns', {})
                    }
                
                # Get historical WHOIS
                whois_response = await self.make_request(f'history/{domain}/whois')
                if whois_response.success:
                    results['securitytrails']['whois_history'] = whois_response.data.get('result', {})
                
            except Exception as e:
                logger.error(f"SecurityTrails error: {e}")
                results['securitytrails'] = {'error': str(e)}
        
        # Pulsedive
        if 'pulsedive' in self.api_keys:
            try:
                self.config = self.apis['pulsedive']
                response = await self.make_request(
                    'info.php',
                    params={
                        'indicator': domain,
                        'pretty': 1
                    }
                )
                if response.success:
                    data = response.data
                    results['pulsedive'] = {
                        'risk': data.get('risk'),
                        'risk_factors': data.get('riskfactors', []),
                        'attributes': data.get('attributes', []),
                        'threats': data.get('threats', []),
                        'feeds': data.get('feeds', [])
                    }
            except Exception as e:
                logger.error(f"Pulsedive error: {e}")
                results['pulsedive'] = {'error': str(e)}
        
        # Calculate domain risk score
        domain_risk = 0
        
        if 'pulsedive' in results and 'risk' in results['pulsedive']:
            risk_level = results['pulsedive']['risk']
            if risk_level == 'high':
                domain_risk = 80
            elif risk_level == 'medium':
                domain_risk = 50
            elif risk_level == 'low':
                domain_risk = 20
        
        # Check domain age from WHOIS
        if 'securitytrails' in results and 'whois' in results['securitytrails']:
            whois_data = results['securitytrails']['whois']
            created_date = whois_data.get('createdDate')
            if created_date:
                # Young domains are riskier
                import datetime
                try:
                    created = datetime.datetime.fromisoformat(created_date.replace('Z', '+00:00'))
                    age_days = (datetime.datetime.now(datetime.timezone.utc) - created).days
                    if age_days < 30:
                        domain_risk += 30
                    elif age_days < 90:
                        domain_risk += 15
                except:
                    pass
        
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
            api_name='SecurityAPIs'
        )
    
    async def check_fraud_indicators(self, transaction_data: Dict[str, Any]) -> APIResponse:
        """Check transaction for fraud indicators"""
        results = {}
        
        # FraudLabs Pro
        if 'fraudlabs' in self.api_keys:
            try:
                self.config = self.apis['fraudlabs']
                response = await self.make_request(
                    'order/screen',
                    method='POST',
                    data=transaction_data
                )
                if response.success:
                    data = response.data
                    results['fraudlabs'] = {
                        'fraud_score': data.get('fraudlabspro_score', 0),
                        'status': data.get('fraudlabspro_status'),
                        'distribution': data.get('fraudlabspro_distribution'),
                        'id': data.get('fraudlabspro_id'),
                        'credits': data.get('fraudlabspro_credits'),
                        'error_code': data.get('fraudlabspro_error_code'),
                        'message': data.get('fraudlabspro_message')
                    }
            except Exception as e:
                logger.error(f"FraudLabs Pro error: {e}")
                results['fraudlabs'] = {'error': str(e)}
        
        # Calculate overall fraud score
        fraud_score = 0
        if 'fraudlabs' in results and 'fraud_score' in results['fraudlabs']:
            fraud_score = results['fraudlabs']['fraud_score']
        
        return APIResponse(
            success=True,
            data={
                'fraud_score': fraud_score,
                'risk_level': 'HIGH' if fraud_score > 70 else 'MEDIUM' if fraud_score > 30 else 'LOW',
                'detailed_results': results,
                'recommendation': self._get_fraud_recommendation(fraud_score, results)
            },
            api_name='SecurityAPIs'
        )
    
    def _get_ip_recommendation(self, risk_score: float, results: Dict) -> str:
        """Generate recommendation based on IP analysis"""
        if risk_score > 75:
            return "HIGH RISK: Block this IP address immediately. Multiple threat intelligence sources indicate malicious activity."
        elif risk_score > 25:
            return "MEDIUM RISK: Monitor this IP address closely. Consider additional verification steps."
        else:
            return "LOW RISK: IP address appears clean across threat intelligence sources."
    
    def _get_email_recommendation(self, risk_score: float, results: Dict) -> str:
        """Generate recommendation based on email analysis"""
        if risk_score > 70:
            return "HIGH RISK: This email address shows multiple red flags. Avoid engagement and consider blocking."
        elif risk_score > 30:
            return "MEDIUM RISK: Exercise caution with this email address. Verify through additional channels."
        else:
            return "LOW RISK: Email address appears legitimate based on available intelligence."
    
    def _get_domain_recommendation(self, risk_score: float, results: Dict) -> str:
        """Generate recommendation based on domain analysis"""
        if risk_score > 70:
            return "HIGH RISK: Domain shows suspicious characteristics. Avoid interaction and consider blocking."
        elif risk_score > 30:
            return "MEDIUM RISK: Domain requires additional verification. Proceed with caution."
        else:
            return "LOW RISK: Domain appears legitimate based on historical and reputation data."
    
    def _get_fraud_recommendation(self, fraud_score: float, results: Dict) -> str:
        """Generate recommendation based on fraud analysis"""
        if fraud_score > 70:
            return "HIGH RISK: Transaction shows strong fraud indicators. Reject or require manual review."
        elif fraud_score > 30:
            return "MEDIUM RISK: Transaction requires additional verification steps before approval."
        else:
            return "LOW RISK: Transaction appears legitimate based on fraud detection algorithms."
    
    async def comprehensive_security_check(self, target_data: Dict[str, Any]) -> APIResponse:
        """Perform comprehensive security check across all available data"""
        results = {}
        
        # Check IP if provided
        if 'ip_address' in target_data:
            ip_result = await self.check_ip_reputation(target_data['ip_address'])
            results['ip_analysis'] = ip_result.data
        
        # Check email if provided
        if 'email' in target_data:
            email_result = await self.check_email_reputation(target_data['email'])
            results['email_analysis'] = email_result.data
        
        # Check domain if provided
        if 'domain' in target_data:
            domain_result = await self.check_domain_reputation(target_data['domain'])
            results['domain_analysis'] = domain_result.data
        
        # Check for fraud indicators if transaction data provided
        if 'transaction' in target_data:
            fraud_result = await self.check_fraud_indicators(target_data['transaction'])
            results['fraud_analysis'] = fraud_result.data
        
        # Calculate overall security score
        risk_scores = []
        for analysis in results.values():
            if 'risk_score' in analysis:
                risk_scores.append(analysis['risk_score'])
        
        overall_risk = sum(risk_scores) / len(risk_scores) if risk_scores else 0
        
        return APIResponse(
            success=True,
            data={
                'overall_risk_score': overall_risk,
                'overall_risk_level': 'HIGH' if overall_risk > 70 else 'MEDIUM' if overall_risk > 30 else 'LOW',
                'detailed_analysis': results,
                'summary': self._generate_security_summary(overall_risk, results),
                'recommendations': self._generate_security_recommendations(results)
            },
            api_name='SecurityAPIs'
        )
    
    def _generate_security_summary(self, overall_risk: float, results: Dict) -> str:
        """Generate comprehensive security summary"""
        high_risk_items = []
        medium_risk_items = []
        
        for analysis_type, analysis_data in results.items():
            risk_level = analysis_data.get('risk_level', 'LOW')
            if risk_level == 'HIGH':
                high_risk_items.append(analysis_type.replace('_analysis', ''))
            elif risk_level == 'MEDIUM':
                medium_risk_items.append(analysis_type.replace('_analysis', ''))
        
        summary = f"Overall Security Risk: {overall_risk:.1f}/100 "
        
        if high_risk_items:
            summary += f"| HIGH RISK detected in: {', '.join(high_risk_items)} "
        if medium_risk_items:
            summary += f"| MEDIUM RISK detected in: {', '.join(medium_risk_items)} "
        
        if not high_risk_items and not medium_risk_items:
            summary += "| All indicators show LOW RISK"
        
        return summary
    
    def _generate_security_recommendations(self, results: Dict) -> List[str]:
        """Generate list of security recommendations"""
        recommendations = []
        
        for analysis_type, analysis_data in results.items():
            if 'recommendation' in analysis_data:
                recommendations.append(f"{analysis_type.replace('_analysis', '').title()}: {analysis_data['recommendation']}")
        
        return recommendations

