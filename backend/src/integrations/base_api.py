"""
Base API Wrapper Class for ScamShield AI Integrations
Provides common functionality for all API integrations including rate limiting, caching, and error handling
"""

import asyncio
import aiohttp
import json
import time
import hashlib
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from abc import ABC, abstractmethod
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class APIResponse:
    """Standardized API response format"""
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None
    api_name: str = ""
    response_time: float = 0.0
    cached: bool = False
    rate_limited: bool = False

@dataclass
class APIConfig:
    """API configuration settings"""
    name: str
    base_url: str
    api_key: Optional[str] = None
    rate_limit: int = 100  # requests per minute
    timeout: int = 30
    retry_attempts: int = 3
    cache_ttl: int = 3600  # seconds
    requires_auth: bool = True

class RateLimiter:
    """Rate limiting implementation"""
    
    def __init__(self, max_requests: int, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    def can_make_request(self) -> bool:
        """Check if request can be made within rate limits"""
        now = time.time()
        # Remove old requests outside time window
        self.requests = [req_time for req_time in self.requests if now - req_time < self.time_window]
        
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False
    
    def time_until_next_request(self) -> float:
        """Get time until next request can be made"""
        if not self.requests:
            return 0.0
        
        oldest_request = min(self.requests)
        return max(0, self.time_window - (time.time() - oldest_request))

class APICache:
    """Simple in-memory cache for API responses"""
    
    def __init__(self):
        self.cache = {}
        self.timestamps = {}
    
    def get_cache_key(self, api_name: str, endpoint: str, params: Dict) -> str:
        """Generate cache key from API call parameters"""
        key_data = f"{api_name}:{endpoint}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, cache_key: str, ttl: int) -> Optional[Dict]:
        """Get cached response if still valid"""
        if cache_key in self.cache:
            timestamp = self.timestamps.get(cache_key, 0)
            if time.time() - timestamp < ttl:
                return self.cache[cache_key]
            else:
                # Remove expired cache entry
                del self.cache[cache_key]
                del self.timestamps[cache_key]
        return None
    
    def set(self, cache_key: str, data: Dict):
        """Store response in cache"""
        self.cache[cache_key] = data
        self.timestamps[cache_key] = time.time()
    
    def clear_expired(self, ttl: int):
        """Clear expired cache entries"""
        current_time = time.time()
        expired_keys = [
            key for key, timestamp in self.timestamps.items()
            if current_time - timestamp > ttl
        ]
        for key in expired_keys:
            del self.cache[key]
            del self.timestamps[key]

class BaseAPIWrapper(ABC):
    """Base class for all API wrappers"""
    
    def __init__(self, config: APIConfig):
        self.config = config
        self.rate_limiter = RateLimiter(config.rate_limit)
        self.cache = APICache()
        self.session = None
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'cached_requests': 0,
            'rate_limited_requests': 0
        }
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.config.timeout)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    def get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        headers = {
            'User-Agent': 'ScamShield-AI/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        if self.config.api_key and self.config.requires_auth:
            # Different APIs use different auth header formats
            if 'X-API-Key' in self.get_auth_header_name():
                headers['X-API-Key'] = self.config.api_key
            elif 'Authorization' in self.get_auth_header_name():
                headers['Authorization'] = f'Bearer {self.config.api_key}'
            else:
                headers[self.get_auth_header_name()] = self.config.api_key
        
        return headers
    
    @abstractmethod
    def get_auth_header_name(self) -> str:
        """Get the authentication header name for this API"""
        pass
    
    async def make_request(
        self,
        endpoint: str,
        method: str = 'GET',
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        use_cache: bool = True
    ) -> APIResponse:
        """Make HTTP request with rate limiting, caching, and error handling"""
        
        start_time = time.time()
        params = params or {}
        
        # Generate cache key
        cache_key = self.cache.get_cache_key(self.config.name, endpoint, params)
        
        # Check cache first
        if use_cache:
            cached_response = self.cache.get(cache_key, self.config.cache_ttl)
            if cached_response:
                self.stats['cached_requests'] += 1
                return APIResponse(
                    success=True,
                    data=cached_response,
                    api_name=self.config.name,
                    response_time=time.time() - start_time,
                    cached=True
                )
        
        # Check rate limits
        if not self.rate_limiter.can_make_request():
            self.stats['rate_limited_requests'] += 1
            wait_time = self.rate_limiter.time_until_next_request()
            return APIResponse(
                success=False,
                data={},
                error=f"Rate limited. Try again in {wait_time:.1f} seconds",
                api_name=self.config.name,
                response_time=time.time() - start_time,
                rate_limited=True
            )
        
        # Make request with retries
        for attempt in range(self.config.retry_attempts):
            try:
                self.stats['total_requests'] += 1
                
                url = f"{self.config.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
                headers = self.get_headers()
                
                if not self.session:
                    self.session = aiohttp.ClientSession(
                        timeout=aiohttp.ClientTimeout(total=self.config.timeout)
                    )
                
                async with self.session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=data
                ) as response:
                    
                    response_data = await response.json()
                    
                    if response.status == 200:
                        self.stats['successful_requests'] += 1
                        
                        # Cache successful response
                        if use_cache:
                            self.cache.set(cache_key, response_data)
                        
                        return APIResponse(
                            success=True,
                            data=response_data,
                            api_name=self.config.name,
                            response_time=time.time() - start_time
                        )
                    else:
                        error_msg = f"HTTP {response.status}: {response_data.get('error', 'Unknown error')}"
                        if attempt == self.config.retry_attempts - 1:
                            self.stats['failed_requests'] += 1
                            return APIResponse(
                                success=False,
                                data={},
                                error=error_msg,
                                api_name=self.config.name,
                                response_time=time.time() - start_time
                            )
                        
                        # Wait before retry
                        await asyncio.sleep(2 ** attempt)
            
            except asyncio.TimeoutError:
                error_msg = f"Request timeout after {self.config.timeout} seconds"
                if attempt == self.config.retry_attempts - 1:
                    self.stats['failed_requests'] += 1
                    return APIResponse(
                        success=False,
                        data={},
                        error=error_msg,
                        api_name=self.config.name,
                        response_time=time.time() - start_time
                    )
                await asyncio.sleep(2 ** attempt)
            
            except Exception as e:
                error_msg = f"Request failed: {str(e)}"
                if attempt == self.config.retry_attempts - 1:
                    self.stats['failed_requests'] += 1
                    return APIResponse(
                        success=False,
                        data={},
                        error=error_msg,
                        api_name=self.config.name,
                        response_time=time.time() - start_time
                    )
                await asyncio.sleep(2 ** attempt)
        
        # Should never reach here
        self.stats['failed_requests'] += 1
        return APIResponse(
            success=False,
            data={},
            error="All retry attempts failed",
            api_name=self.config.name,
            response_time=time.time() - start_time
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """Get API usage statistics"""
        total = self.stats['total_requests']
        return {
            'api_name': self.config.name,
            'total_requests': total,
            'successful_requests': self.stats['successful_requests'],
            'failed_requests': self.stats['failed_requests'],
            'cached_requests': self.stats['cached_requests'],
            'rate_limited_requests': self.stats['rate_limited_requests'],
            'success_rate': (self.stats['successful_requests'] / total * 100) if total > 0 else 0,
            'cache_hit_rate': (self.stats['cached_requests'] / total * 100) if total > 0 else 0
        }
    
    @abstractmethod
    async def health_check(self) -> APIResponse:
        """Check if the API is healthy and accessible"""
        pass
    
    def clear_cache(self):
        """Clear all cached responses"""
        self.cache.cache.clear()
        self.cache.timestamps.clear()
    
    def reset_stats(self):
        """Reset usage statistics"""
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'cached_requests': 0,
            'rate_limited_requests': 0
        }

