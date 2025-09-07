"""
Geolocation APIs Wrapper for ScamShield AI
Integrates IP geolocation and location verification APIs
"""

import asyncio
from typing import Dict, Any, Optional, List
from .base_api import BaseAPIWrapper, APIConfig, APIResponse
import logging
import ipaddress

logger = logging.getLogger(__name__)

class GeolocationAPIWrapper(BaseAPIWrapper):
    """Wrapper for geolocation and IP intelligence APIs"""
    
    def __init__(self, api_keys: Dict[str, str] = None):
        super().__init__(APIConfig(
            name="GeolocationAPIs",
            base_url="https://api.geolocation.com",
            rate_limit=60
        ))
        
        self.api_keys = api_keys or {}
        self.apis = self._initialize_apis()
    
    def _initialize_apis(self) -> Dict[str, APIConfig]:
        """Initialize all geolocation API configurations"""
        return {
            'ip_geolocation': APIConfig(
                name='IP Geolocation',
                base_url='https://api.ipgeolocation.io',
                api_key=self.api_keys.get('ip_geolocation'),
                rate_limit=1000,
                cache_ttl=3600,
                requires_auth=True
            ),
            'ipstack': APIConfig(
                name='apilayer ipstack',
                base_url='https://api.ipstack.com',
                api_key=self.api_keys.get('ipstack'),
                rate_limit=1000,
                cache_ttl=3600,
                requires_auth=True
            ),
            'bigdatacloud': APIConfig(
                name='BigDataCloud',
                base_url='https://api.bigdatacloud.net/data',
                api_key=self.api_keys.get('bigdatacloud'),
                rate_limit=10000,
                cache_ttl=3600,
                requires_auth=True
            ),
            'apiip': APIConfig(
                name='Apiip',
                base_url='https://apiip.net/api',
                api_key=self.api_keys.get('apiip'),
                rate_limit=1000,
                cache_ttl=3600,
                requires_auth=True
            ),
            'airtel_ip': APIConfig(
                name='Airtel IP',
                base_url='https://api.airtel.in/ip',
                api_key=None,  # No auth required
                rate_limit=1000,
                cache_ttl=3600,
                requires_auth=False
            ),
            'ip_api': APIConfig(
                name='ip-api',
                base_url='http://ip-api.com/json',
                api_key=None,  # No auth required
                rate_limit=45,  # 45 requests per minute
                cache_ttl=3600,
                requires_auth=False
            ),
            'ipapi_co': APIConfig(
                name='ipapi.co',
                base_url='https://ipapi.co',
                api_key=None,  # No auth required
                rate_limit=1000,
                cache_ttl=3600,
                requires_auth=False
            ),
            'geojs': APIConfig(
                name='GeoJS',
                base_url='https://get.geojs.io/v1/ip',
                api_key=None,  # No auth required
                rate_limit=1000,
                cache_ttl=3600,
                requires_auth=False
            ),
            'ipinfo': APIConfig(
                name='IPInfo',
                base_url='https://ipinfo.io',
                api_key=self.api_keys.get('ipinfo'),
                rate_limit=50000,  # 50k per month
                cache_ttl=3600,
                requires_auth=True
            ),
            'ip2location': APIConfig(
                name='IP2Location',
                base_url='https://api.ip2location.com/v2',
                api_key=self.api_keys.get('ip2location'),
                rate_limit=500,
                cache_ttl=3600,
                requires_auth=True
            )
        }
    
    def get_auth_header_name(self) -> str:
        """Get authentication header name"""
        return 'X-API-Key'
    
    async def health_check(self) -> APIResponse:
        """Check health of all geolocation APIs"""
        results = {}
        
        # Test ip-api (no auth required)
        try:
            response = await self.geolocate_ip('8.8.8.8')
            results['ip_api'] = response.success
        except:
            results['ip_api'] = False
        
        return APIResponse(
            success=True,
            data={'health_status': results},
            api_name='GeolocationAPIs'
        )
    
    def _is_valid_ip(self, ip: str) -> bool:
        """Validate IP address format"""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    def _is_private_ip(self, ip: str) -> bool:
        """Check if IP is private/internal"""
        try:
            ip_obj = ipaddress.ip_address(ip)
            return ip_obj.is_private
        except ValueError:
            return False
    
    async def geolocate_ip(self, ip_address: str) -> APIResponse:
        """Geolocate IP address across multiple services"""
        if not self._is_valid_ip(ip_address):
            return APIResponse(
                success=True,
                data={
                    'ip_address': ip_address,
                    'valid_ip': False,
                    'error': 'Invalid IP address format'
                },
                api_name='GeolocationAPIs'
            )
        
        if self._is_private_ip(ip_address):
            return APIResponse(
                success=True,
                data={
                    'ip_address': ip_address,
                    'valid_ip': True,
                    'is_private': True,
                    'location': 'Private/Internal Network',
                    'risk_score': 0,
                    'risk_level': 'LOW'
                },
                api_name='GeolocationAPIs'
            )
        
        results = {}
        
        # ip-api (free, no auth)
        try:
            self.config = self.apis['ip_api']
            response = await self.make_request(f'{ip_address}')
            if response.success:
                data = response.data
                if data.get('status') == 'success':
                    results['ip_api'] = {
                        'country': data.get('country'),
                        'country_code': data.get('countryCode'),
                        'region': data.get('regionName'),
                        'city': data.get('city'),
                        'zip': data.get('zip'),
                        'lat': data.get('lat'),
                        'lon': data.get('lon'),
                        'timezone': data.get('timezone'),
                        'isp': data.get('isp'),
                        'org': data.get('org'),
                        'as': data.get('as'),
                        'mobile': data.get('mobile', False),
                        'proxy': data.get('proxy', False),
                        'hosting': data.get('hosting', False)
                    }
        except Exception as e:
            logger.error(f"ip-api error: {e}")
            results['ip_api'] = {'error': str(e)}
        
        # ipapi.co (free, no auth)
        try:
            self.config = self.apis['ipapi_co']
            response = await self.make_request(f'{ip_address}/json/')
            if response.success:
                data = response.data
                results['ipapi_co'] = {
                    'country': data.get('country_name'),
                    'country_code': data.get('country_code'),
                    'region': data.get('region'),
                    'city': data.get('city'),
                    'postal': data.get('postal'),
                    'latitude': data.get('latitude'),
                    'longitude': data.get('longitude'),
                    'timezone': data.get('timezone'),
                    'asn': data.get('asn'),
                    'org': data.get('org'),
                    'currency': data.get('currency'),
                    'languages': data.get('languages')
                }
        except Exception as e:
            logger.error(f"ipapi.co error: {e}")
            results['ipapi_co'] = {'error': str(e)}
        
        # GeoJS (free, no auth)
        try:
            self.config = self.apis['geojs']
            response = await self.make_request(f'{ip_address}.json')
            if response.success:
                data = response.data
                results['geojs'] = {
                    'country': data.get('country'),
                    'country_code': data.get('country_code'),
                    'region': data.get('region'),
                    'city': data.get('city'),
                    'latitude': data.get('latitude'),
                    'longitude': data.get('longitude'),
                    'timezone': data.get('timezone'),
                    'asn': data.get('asn'),
                    'organization': data.get('organization')
                }
        except Exception as e:
            logger.error(f"GeoJS error: {e}")
            results['geojs'] = {'error': str(e)}
        
        # IP Geolocation (paid)
        if 'ip_geolocation' in self.api_keys:
            try:
                self.config = self.apis['ip_geolocation']
                response = await self.make_request(
                    'ipgeo',
                    params={
                        'apiKey': self.api_keys.get('ip_geolocation'),
                        'ip': ip_address,
                        'fields': 'geo,time_zone,isp,threat'
                    }
                )
                if response.success:
                    data = response.data
                    results['ip_geolocation'] = {
                        'country': data.get('country_name'),
                        'country_code': data.get('country_code2'),
                        'state': data.get('state_prov'),
                        'city': data.get('city'),
                        'zipcode': data.get('zipcode'),
                        'latitude': data.get('latitude'),
                        'longitude': data.get('longitude'),
                        'timezone': data.get('time_zone', {}).get('name'),
                        'isp': data.get('isp'),
                        'connection_type': data.get('connection_type'),
                        'threat': data.get('threat', {}),
                        'is_proxy': data.get('threat', {}).get('is_proxy', False),
                        'is_anonymous': data.get('threat', {}).get('is_anonymous', False),
                        'is_threat': data.get('threat', {}).get('is_known_attacker', False)
                    }
            except Exception as e:
                logger.error(f"IP Geolocation error: {e}")
                results['ip_geolocation'] = {'error': str(e)}
        
        # IPStack (paid)
        if 'ipstack' in self.api_keys:
            try:
                self.config = self.apis['ipstack']
                response = await self.make_request(
                    f'{ip_address}',
                    params={
                        'access_key': self.api_keys.get('ipstack'),
                        'security': 1,
                        'hostname': 1
                    }
                )
                if response.success:
                    data = response.data
                    results['ipstack'] = {
                        'country': data.get('country_name'),
                        'country_code': data.get('country_code'),
                        'region': data.get('region_name'),
                        'city': data.get('city'),
                        'zip': data.get('zip'),
                        'latitude': data.get('latitude'),
                        'longitude': data.get('longitude'),
                        'connection': data.get('connection', {}),
                        'security': data.get('security', {}),
                        'hostname': data.get('hostname'),
                        'is_proxy': data.get('security', {}).get('is_proxy', False),
                        'is_crawler': data.get('security', {}).get('is_crawler', False),
                        'is_tor': data.get('security', {}).get('is_tor', False),
                        'threat_level': data.get('security', {}).get('threat_level', 'low')
                    }
            except Exception as e:
                logger.error(f"IPStack error: {e}")
                results['ipstack'] = {'error': str(e)}
        
        # BigDataCloud (paid)
        if 'bigdatacloud' in self.api_keys:
            try:
                self.config = self.apis['bigdatacloud']
                response = await self.make_request(
                    f'ip-geolocation-full',
                    params={
                        'ip': ip_address,
                        'key': self.api_keys.get('bigdatacloud')
                    }
                )
                if response.success:
                    data = response.data
                    results['bigdatacloud'] = {
                        'country': data.get('country', {}).get('name'),
                        'country_code': data.get('country', {}).get('isoAlpha2'),
                        'city': data.get('city'),
                        'postcode': data.get('postcode'),
                        'latitude': data.get('location', {}).get('latitude'),
                        'longitude': data.get('location', {}).get('longitude'),
                        'timezone': data.get('location', {}).get('timeZone', {}).get('ianaTimeId'),
                        'isp': data.get('network', {}).get('organisation'),
                        'is_proxy': data.get('hazardReport', {}).get('isKnownAsTorServer', False),
                        'is_malicious': data.get('hazardReport', {}).get('isKnownAsVpn', False),
                        'confidence_area': data.get('confidenceArea', [])
                    }
            except Exception as e:
                logger.error(f"BigDataCloud error: {e}")
                results['bigdatacloud'] = {'error': str(e)}
        
        # Consolidate location data
        location_data = self._consolidate_location_data(results)
        
        # Calculate risk score based on various factors
        risk_score = self._calculate_location_risk(results, location_data)
        
        return APIResponse(
            success=True,
            data={
                'ip_address': ip_address,
                'valid_ip': True,
                'is_private': False,
                'consolidated_location': location_data,
                'risk_score': risk_score,
                'risk_level': 'HIGH' if risk_score > 70 else 'MEDIUM' if risk_score > 30 else 'LOW',
                'detailed_results': results,
                'recommendation': self._get_location_recommendation(risk_score, location_data, results)
            },
            api_name='GeolocationAPIs'
        )
    
    def _consolidate_location_data(self, results: Dict) -> Dict[str, Any]:
        """Consolidate location data from multiple sources"""
        consolidated = {
            'country': None,
            'country_code': None,
            'region': None,
            'city': None,
            'latitude': None,
            'longitude': None,
            'timezone': None,
            'isp': None,
            'organization': None,
            'is_proxy': False,
            'is_vpn': False,
            'is_tor': False,
            'is_hosting': False,
            'is_mobile': False,
            'confidence_sources': 0
        }
        
        # Collect data from all sources
        for api_name, api_result in results.items():
            if 'error' not in api_result:
                consolidated['confidence_sources'] += 1
                
                # Country information
                if api_result.get('country') and not consolidated['country']:
                    consolidated['country'] = api_result['country']
                if api_result.get('country_code') and not consolidated['country_code']:
                    consolidated['country_code'] = api_result['country_code']
                
                # Location details
                if api_result.get('city') and not consolidated['city']:
                    consolidated['city'] = api_result['city']
                if api_result.get('region') and not consolidated['region']:
                    consolidated['region'] = api_result['region']
                
                # Coordinates
                if api_result.get('latitude') and not consolidated['latitude']:
                    consolidated['latitude'] = api_result['latitude']
                if api_result.get('longitude') and not consolidated['longitude']:
                    consolidated['longitude'] = api_result['longitude']
                
                # Network information
                if api_result.get('isp') and not consolidated['isp']:
                    consolidated['isp'] = api_result['isp']
                if api_result.get('org') and not consolidated['organization']:
                    consolidated['organization'] = api_result['org']
                
                # Security flags
                if api_result.get('is_proxy') or api_result.get('proxy'):
                    consolidated['is_proxy'] = True
                if api_result.get('is_tor'):
                    consolidated['is_tor'] = True
                if api_result.get('hosting'):
                    consolidated['is_hosting'] = True
                if api_result.get('mobile'):
                    consolidated['is_mobile'] = True
                if api_result.get('is_malicious') or api_result.get('is_anonymous'):
                    consolidated['is_vpn'] = True
        
        return consolidated
    
    def _calculate_location_risk(self, results: Dict, location_data: Dict) -> float:
        """Calculate risk score based on location and network characteristics"""
        risk_score = 0
        
        # High-risk countries (example list)
        high_risk_countries = ['CN', 'RU', 'KP', 'IR', 'SY']
        medium_risk_countries = ['PK', 'BD', 'NG', 'ID', 'VN']
        
        country_code = location_data.get('country_code', '').upper()
        
        if country_code in high_risk_countries:
            risk_score += 40
        elif country_code in medium_risk_countries:
            risk_score += 20
        
        # Network-based risk factors
        if location_data.get('is_proxy'):
            risk_score += 30
        if location_data.get('is_tor'):
            risk_score += 50
        if location_data.get('is_vpn'):
            risk_score += 25
        if location_data.get('is_hosting'):
            risk_score += 15
        
        # Check for threat indicators from premium services
        for api_result in results.values():
            if 'threat' in api_result:
                threat_data = api_result['threat']
                if threat_data.get('is_known_attacker'):
                    risk_score += 60
                if threat_data.get('is_malicious'):
                    risk_score += 40
            
            if api_result.get('threat_level') == 'high':
                risk_score += 50
            elif api_result.get('threat_level') == 'medium':
                risk_score += 25
        
        # Confidence adjustment
        confidence_sources = location_data.get('confidence_sources', 1)
        if confidence_sources < 2:
            risk_score += 10  # Less confidence in data
        
        return min(100, risk_score)
    
    async def analyze_ip_reputation(self, ip_address: str) -> APIResponse:
        """Analyze IP reputation and threat indicators"""
        if not self._is_valid_ip(ip_address):
            return APIResponse(
                success=False,
                data={'error': 'Invalid IP address format'},
                api_name='GeolocationAPIs'
            )
        
        # Get geolocation data first
        geo_result = await self.geolocate_ip(ip_address)
        
        if not geo_result.success:
            return geo_result
        
        geo_data = geo_result.data
        results = {
            'geolocation': geo_data,
            'reputation_analysis': {}
        }
        
        # Additional reputation checks using geolocation APIs with security features
        reputation_indicators = {
            'is_proxy': geo_data.get('consolidated_location', {}).get('is_proxy', False),
            'is_vpn': geo_data.get('consolidated_location', {}).get('is_vpn', False),
            'is_tor': geo_data.get('consolidated_location', {}).get('is_tor', False),
            'is_hosting': geo_data.get('consolidated_location', {}).get('is_hosting', False),
            'high_risk_country': geo_data.get('risk_score', 0) > 50
        }
        
        # Calculate reputation score
        reputation_score = 100  # Start with good reputation
        
        for indicator, is_present in reputation_indicators.items():
            if is_present:
                if indicator == 'is_tor':
                    reputation_score -= 50
                elif indicator == 'is_proxy':
                    reputation_score -= 30
                elif indicator == 'is_vpn':
                    reputation_score -= 25
                elif indicator == 'is_hosting':
                    reputation_score -= 15
                elif indicator == 'high_risk_country':
                    reputation_score -= 20
        
        reputation_score = max(0, reputation_score)
        
        results['reputation_analysis'] = {
            'reputation_score': reputation_score,
            'reputation_level': 'HIGH' if reputation_score > 70 else 'MEDIUM' if reputation_score > 30 else 'LOW',
            'indicators': reputation_indicators,
            'risk_factors': [k for k, v in reputation_indicators.items() if v]
        }
        
        return APIResponse(
            success=True,
            data={
                'ip_address': ip_address,
                'reputation_score': reputation_score,
                'reputation_level': results['reputation_analysis']['reputation_level'],
                'detailed_analysis': results,
                'recommendation': self._get_reputation_recommendation(reputation_score, reputation_indicators)
            },
            api_name='GeolocationAPIs'
        )
    
    async def batch_geolocate_ips(self, ip_addresses: List[str]) -> APIResponse:
        """Geolocate multiple IP addresses in batch"""
        results = {}
        
        # Process IPs in parallel (with rate limiting consideration)
        semaphore = asyncio.Semaphore(5)  # Limit concurrent requests
        
        async def process_ip(ip):
            async with semaphore:
                return await self.geolocate_ip(ip)
        
        tasks = [process_ip(ip) for ip in ip_addresses]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        for ip, response in zip(ip_addresses, responses):
            if isinstance(response, Exception):
                results[ip] = {'error': str(response)}
            else:
                results[ip] = response.data if response.success else {'error': 'Failed to geolocate'}
        
        # Calculate batch statistics
        successful_lookups = sum(1 for r in results.values() if 'error' not in r)
        high_risk_ips = sum(1 for r in results.values() if r.get('risk_level') == 'HIGH')
        
        return APIResponse(
            success=True,
            data={
                'total_ips': len(ip_addresses),
                'successful_lookups': successful_lookups,
                'high_risk_ips': high_risk_ips,
                'results': results,
                'summary': f"Processed {len(ip_addresses)} IPs: {successful_lookups} successful, {high_risk_ips} high-risk"
            },
            api_name='GeolocationAPIs'
        )
    
    def _get_location_recommendation(self, risk_score: float, location_data: Dict, results: Dict) -> str:
        """Generate recommendation based on location analysis"""
        if risk_score > 70:
            risk_factors = []
            if location_data.get('is_tor'):
                risk_factors.append('Tor network')
            if location_data.get('is_proxy'):
                risk_factors.append('proxy server')
            if location_data.get('is_vpn'):
                risk_factors.append('VPN service')
            
            factors_str = ', '.join(risk_factors) if risk_factors else 'multiple risk indicators'
            return f"HIGH RISK: IP shows {factors_str}. Consider blocking or requiring additional verification."
        elif risk_score > 30:
            return "MEDIUM RISK: IP has some concerning characteristics. Monitor activity closely."
        else:
            return "LOW RISK: IP appears to be from a legitimate location and network."
    
    def _get_reputation_recommendation(self, reputation_score: float, indicators: Dict) -> str:
        """Generate recommendation based on IP reputation analysis"""
        if reputation_score < 30:
            active_indicators = [k.replace('is_', '') for k, v in indicators.items() if v]
            return f"HIGH RISK: IP reputation compromised by: {', '.join(active_indicators)}. Block immediately."
        elif reputation_score < 70:
            return "MEDIUM RISK: IP shows some suspicious characteristics. Implement additional monitoring."
        else:
            return "LOW RISK: IP has good reputation across geolocation intelligence sources."
    
    async def comprehensive_ip_analysis(self, ip_address: str) -> APIResponse:
        """Perform comprehensive IP analysis including geolocation and reputation"""
        # Get geolocation data
        geo_result = await self.geolocate_ip(ip_address)
        
        # Get reputation analysis
        reputation_result = await self.analyze_ip_reputation(ip_address)
        
        if not geo_result.success:
            return geo_result
        
        # Combine results
        combined_data = {
            'ip_address': ip_address,
            'geolocation_analysis': geo_result.data,
            'reputation_analysis': reputation_result.data if reputation_result.success else None,
            'overall_risk_score': max(
                geo_result.data.get('risk_score', 0),
                reputation_result.data.get('reputation_score', 100) if reputation_result.success else 0
            )
        }
        
        overall_risk = combined_data['overall_risk_score']
        
        return APIResponse(
            success=True,
            data={
                **combined_data,
                'overall_risk_level': 'HIGH' if overall_risk > 70 else 'MEDIUM' if overall_risk > 30 else 'LOW',
                'summary': self._generate_ip_summary(combined_data),
                'recommendations': self._generate_ip_recommendations(combined_data)
            },
            api_name='GeolocationAPIs'
        )
    
    def _generate_ip_summary(self, data: Dict) -> str:
        """Generate comprehensive IP analysis summary"""
        ip = data['ip_address']
        geo_data = data.get('geolocation_analysis', {})
        location = geo_data.get('consolidated_location', {})
        
        summary_parts = [f"IP: {ip}"]
        
        if location.get('country'):
            summary_parts.append(f"Location: {location['city']}, {location['country']}")
        
        if location.get('isp'):
            summary_parts.append(f"ISP: {location['isp']}")
        
        risk_score = data.get('overall_risk_score', 0)
        summary_parts.append(f"Risk: {risk_score:.1f}/100")
        
        # Add risk indicators
        risk_indicators = []
        if location.get('is_proxy'):
            risk_indicators.append('Proxy')
        if location.get('is_tor'):
            risk_indicators.append('Tor')
        if location.get('is_vpn'):
            risk_indicators.append('VPN')
        
        if risk_indicators:
            summary_parts.append(f"Flags: {', '.join(risk_indicators)}")
        
        return " | ".join(summary_parts)
    
    def _generate_ip_recommendations(self, data: Dict) -> List[str]:
        """Generate list of IP-specific recommendations"""
        recommendations = []
        
        geo_data = data.get('geolocation_analysis', {})
        rep_data = data.get('reputation_analysis', {})
        
        if geo_data.get('recommendation'):
            recommendations.append(f"Geolocation: {geo_data['recommendation']}")
        
        if rep_data and rep_data.get('recommendation'):
            recommendations.append(f"Reputation: {rep_data['recommendation']}")
        
        return recommendations

