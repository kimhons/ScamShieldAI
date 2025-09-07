# ScamShield AI - API Integrations Package
# Comprehensive API integration framework for fraud detection and investigation

__version__ = "1.0.0"
__author__ = "ScamShield AI Team"

from .api_manager import APIManager
from .security_apis import SecurityAPIWrapper
from .email_apis import EmailAPIWrapper
from .geolocation_apis import GeolocationAPIWrapper
from .phone_apis import PhoneAPIWrapper
from .validation_apis import ValidationAPIWrapper
from .anti_malware_apis import AntiMalwareAPIWrapper

__all__ = [
    'APIManager',
    'SecurityAPIWrapper',
    'EmailAPIWrapper', 
    'GeolocationAPIWrapper',
    'PhoneAPIWrapper',
    'ValidationAPIWrapper',
    'AntiMalwareAPIWrapper'
]

