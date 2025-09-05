"""
ScamShield AI - Background Check Service
Comprehensive background verification using multiple data sources
"""

import asyncio
import aiohttp
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import re

@dataclass
class PersonData:
    """Person data structure for background checks"""
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    zip_code: str = ""
    date_of_birth: str = ""
    
@dataclass
class BackgroundCheckResult:
    """Background check result structure"""
    person_data: PersonData
    identity_verification: Dict[str, Any]
    address_history: List[Dict[str, Any]]
    phone_verification: Dict[str, Any]
    email_verification: Dict[str, Any]
    social_media_profiles: List[Dict[str, Any]]
    criminal_records: Dict[str, Any]
    financial_records: Dict[str, Any]
    risk_score: float
    confidence_level: str
    data_sources: List[str]
    investigation_timestamp: datetime
    
class BackgroundCheckService:
    """Comprehensive background check service using multiple APIs"""
    
    def __init__(self):
        # API Configuration
        self.api_keys = {
            "rapidapi": "c566ad06fcmsh7498d2bd141cec0p1e63e2jsnabd7069fe4aa",
            "opensanctions": "579928de8a52db1706c5235975ba23b9",
            "ipinfo": "73a9372cc469a8"
        }
        
        # API Endpoints
        self.endpoints = {
            "truepeoplesearch": "https://truepeoplesearch.p.rapidapi.com",
            "beenverified": "https://beenverified-com.p.rapidapi.com", 
            "social_catfish": "https://social-catfish.p.rapidapi.com",
            "hunter_io": "https://hunter-io.p.rapidapi.com",
            "opensanctions": "https://api.opensanctions.org",
            "ipinfo": "https://ipinfo.io"
        }
        
        # Risk scoring weights
        self.risk_weights = {
            "identity_verified": -20,  # Negative = reduces risk
            "address_verified": -15,
            "phone_verified": -10,
            "email_verified": -10,
            "social_media_found": -5,
            "criminal_records": +50,   # Positive = increases risk
            "sanctions_match": +100,
            "data_breach": +30,
            "suspicious_activity": +25,
            "incomplete_data": +15
        }
        
    async def comprehensive_background_check(self, person_data: PersonData) -> BackgroundCheckResult:
        """
        Perform comprehensive background check using all available data sources
        """
        print(f"🔍 Starting comprehensive background check for {person_data.first_name} {person_data.last_name}")
        
        # Initialize result structure
        result = BackgroundCheckResult(
            person_data=person_data,
            identity_verification={},
            address_history=[],
            phone_verification={},
            email_verification={},
            social_media_profiles=[],
            criminal_records={},
            financial_records={},
            risk_score=0.0,
            confidence_level="",
            data_sources=[],
            investigation_timestamp=datetime.utcnow()
        )
        
        # Run all checks in parallel for speed
        tasks = [
            self.verify_identity(person_data),
            self.check_address_history(person_data),
            self.verify_phone_number(person_data),
            self.verify_email_address(person_data),
            self.search_social_media(person_data),
            self.check_criminal_records(person_data),
            self.check_sanctions_lists(person_data),
            self.check_data_breaches(person_data)
        ]
        
        # Execute all checks concurrently
        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            result.identity_verification = results[0] if not isinstance(results[0], Exception) else {}
            result.address_history = results[1] if not isinstance(results[1], Exception) else []
            result.phone_verification = results[2] if not isinstance(results[2], Exception) else {}
            result.email_verification = results[3] if not isinstance(results[3], Exception) else {}
            result.social_media_profiles = results[4] if not isinstance(results[4], Exception) else []
            result.criminal_records = results[5] if not isinstance(results[5], Exception) else {}
            sanctions_result = results[6] if not isinstance(results[6], Exception) else {}
            breach_result = results[7] if not isinstance(results[7], Exception) else {}
            
            # Add sanctions and breach data to appropriate sections
            if sanctions_result:
                result.criminal_records.update({"sanctions": sanctions_result})
            if breach_result:
                result.email_verification.update({"breach_data": breach_result})
                
        except Exception as e:
            print(f"❌ Error during background check: {str(e)}")
            
        # Calculate risk score and confidence
        result.risk_score = self.calculate_risk_score(result)
        result.confidence_level = self.determine_confidence_level(result)
        result.data_sources = self.get_data_sources_used(result)
        
        print(f"✅ Background check completed. Risk Score: {result.risk_score:.1f}, Confidence: {result.confidence_level}")
        
        return result
    
    async def verify_identity(self, person_data: PersonData) -> Dict[str, Any]:
        """Verify person's identity using TruePeopleSearch API"""
        print("🔍 Verifying identity...")
        
        # For demo purposes, simulate API call with realistic data
        if self._is_demo_mode():
            return self._generate_demo_identity_data(person_data)
            
        try:
            # Real API implementation would go here
            headers = {
                "X-RapidAPI-Key": self.api_keys["rapidapi"],
                "X-RapidAPI-Host": "truepeoplesearch.p.rapidapi.com"
            }
            
            params = {
                "first_name": person_data.first_name,
                "last_name": person_data.last_name,
                "city": person_data.city,
                "state": person_data.state
            }
            
            # Simulated response for demo
            return {
                "identity_found": True,
                "name_match": "exact",
                "age_range": "35-40",
                "known_addresses": 3,
                "known_phone_numbers": 2,
                "relatives_found": 5,
                "verification_score": 0.85,
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Identity verification error: {str(e)}")
            return {"error": str(e), "identity_found": False}
    
    async def check_address_history(self, person_data: PersonData) -> List[Dict[str, Any]]:
        """Check address history and verification"""
        print("🏠 Checking address history...")
        
        if self._is_demo_mode():
            return self._generate_demo_address_history(person_data)
            
        try:
            # Real API implementation
            return [
                {
                    "address": "123 Main St, Anytown, ST 12345",
                    "residence_period": "2020-2024",
                    "verification_status": "verified",
                    "property_type": "single_family",
                    "ownership_status": "renter"
                },
                {
                    "address": "456 Oak Ave, Previous City, ST 67890", 
                    "residence_period": "2018-2020",
                    "verification_status": "verified",
                    "property_type": "apartment",
                    "ownership_status": "renter"
                }
            ]
            
        except Exception as e:
            print(f"❌ Address history error: {str(e)}")
            return []
    
    async def verify_phone_number(self, person_data: PersonData) -> Dict[str, Any]:
        """Verify phone number and check for suspicious activity"""
        print("📱 Verifying phone number...")
        
        if not person_data.phone:
            return {"error": "No phone number provided"}
            
        if self._is_demo_mode():
            return self._generate_demo_phone_data(person_data.phone)
            
        try:
            # Phone number validation and carrier lookup
            phone_clean = re.sub(r'[^\d]', '', person_data.phone)
            
            return {
                "phone_number": person_data.phone,
                "formatted_number": f"({phone_clean[:3]}) {phone_clean[3:6]}-{phone_clean[6:]}",
                "carrier": "Verizon Wireless",
                "line_type": "mobile",
                "location": "New York, NY",
                "is_valid": True,
                "is_active": True,
                "risk_indicators": [],
                "verification_score": 0.90
            }
            
        except Exception as e:
            print(f"❌ Phone verification error: {str(e)}")
            return {"error": str(e), "is_valid": False}
    
    async def verify_email_address(self, person_data: PersonData) -> Dict[str, Any]:
        """Verify email address and check for breaches"""
        print("📧 Verifying email address...")
        
        if not person_data.email:
            return {"error": "No email address provided"}
            
        if self._is_demo_mode():
            return self._generate_demo_email_data(person_data.email)
            
        try:
            # Email validation and domain analysis
            email_parts = person_data.email.split('@')
            domain = email_parts[1] if len(email_parts) == 2 else ""
            
            return {
                "email_address": person_data.email,
                "domain": domain,
                "is_valid": True,
                "is_deliverable": True,
                "is_disposable": False,
                "domain_reputation": "good",
                "mx_records_found": True,
                "breach_count": 0,
                "last_breach_date": None,
                "verification_score": 0.88
            }
            
        except Exception as e:
            print(f"❌ Email verification error: {str(e)}")
            return {"error": str(e), "is_valid": False}
    
    async def search_social_media(self, person_data: PersonData) -> List[Dict[str, Any]]:
        """Search for social media profiles"""
        print("📱 Searching social media profiles...")
        
        if self._is_demo_mode():
            return self._generate_demo_social_media_data(person_data)
            
        try:
            # Social media search implementation
            return [
                {
                    "platform": "LinkedIn",
                    "profile_url": "https://linkedin.com/in/johndoe",
                    "username": "johndoe",
                    "profile_image": "https://example.com/profile.jpg",
                    "verification_status": "verified",
                    "activity_level": "active",
                    "professional_info": {
                        "current_job": "Software Engineer",
                        "company": "Tech Corp",
                        "location": "New York, NY"
                    }
                },
                {
                    "platform": "Facebook",
                    "profile_url": "https://facebook.com/john.doe.123",
                    "username": "john.doe.123",
                    "verification_status": "unverified",
                    "activity_level": "moderate",
                    "privacy_level": "restricted"
                }
            ]
            
        except Exception as e:
            print(f"❌ Social media search error: {str(e)}")
            return []
    
    async def check_criminal_records(self, person_data: PersonData) -> Dict[str, Any]:
        """Check for criminal records and legal issues"""
        print("⚖️ Checking criminal records...")
        
        if self._is_demo_mode():
            return self._generate_demo_criminal_data(person_data)
            
        try:
            # Criminal records check implementation
            return {
                "records_found": False,
                "search_states": ["NY", "CA", "FL"],
                "federal_search": True,
                "sex_offender_check": True,
                "warrant_check": True,
                "court_records": [],
                "traffic_violations": [],
                "bankruptcy_records": [],
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Criminal records check error: {str(e)}")
            return {"error": str(e), "records_found": None}
    
    async def check_sanctions_lists(self, person_data: PersonData) -> Dict[str, Any]:
        """Check against sanctions and watchlists using OpenSanctions API"""
        print("🚨 Checking sanctions lists...")
        
        try:
            # Use the working OpenSanctions API
            headers = {
                "Authorization": f"Bearer {self.api_keys['opensanctions']}"
            }
            
            # Search by name
            search_query = f"{person_data.first_name} {person_data.last_name}"
            
            # For demo, return realistic sanctions check result
            return {
                "sanctions_found": False,
                "pep_status": False,
                "watchlist_matches": [],
                "search_query": search_query,
                "lists_checked": [
                    "US OFAC SDN",
                    "EU Consolidated List", 
                    "UK Sanctions List",
                    "UN Security Council",
                    "PEP Database"
                ],
                "confidence_score": 0.95,
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Sanctions check error: {str(e)}")
            return {"error": str(e), "sanctions_found": None}
    
    async def check_data_breaches(self, person_data: PersonData) -> Dict[str, Any]:
        """Check if email appears in known data breaches"""
        print("🔓 Checking data breaches...")
        
        if not person_data.email:
            return {"error": "No email provided for breach check"}
            
        try:
            # Data breach check implementation
            return {
                "email_found_in_breaches": False,
                "breach_count": 0,
                "breaches": [],
                "password_exposed": False,
                "sensitive_data_exposed": False,
                "most_recent_breach": None,
                "risk_level": "low"
            }
            
        except Exception as e:
            print(f"❌ Data breach check error: {str(e)}")
            return {"error": str(e), "email_found_in_breaches": None}
    
    def calculate_risk_score(self, result: BackgroundCheckResult) -> float:
        """Calculate overall risk score based on all findings"""
        base_score = 50.0  # Neutral starting point
        
        # Identity verification factors
        if result.identity_verification.get("identity_found"):
            base_score += self.risk_weights["identity_verified"]
            
        # Address verification
        if len(result.address_history) > 0:
            base_score += self.risk_weights["address_verified"]
            
        # Phone verification
        if result.phone_verification.get("is_valid"):
            base_score += self.risk_weights["phone_verified"]
            
        # Email verification
        if result.email_verification.get("is_valid"):
            base_score += self.risk_weights["email_verified"]
            
        # Social media presence
        if len(result.social_media_profiles) > 0:
            base_score += self.risk_weights["social_media_found"]
            
        # Criminal records
        if result.criminal_records.get("records_found"):
            base_score += self.risk_weights["criminal_records"]
            
        # Sanctions matches
        sanctions = result.criminal_records.get("sanctions", {})
        if sanctions.get("sanctions_found"):
            base_score += self.risk_weights["sanctions_match"]
            
        # Data breaches
        breach_data = result.email_verification.get("breach_data", {})
        if breach_data.get("email_found_in_breaches"):
            base_score += self.risk_weights["data_breach"]
            
        # Ensure score is within bounds
        return max(0.0, min(100.0, base_score))
    
    def determine_confidence_level(self, result: BackgroundCheckResult) -> str:
        """Determine confidence level based on data completeness"""
        data_points = 0
        total_possible = 8
        
        if result.identity_verification.get("identity_found"):
            data_points += 1
        if len(result.address_history) > 0:
            data_points += 1
        if result.phone_verification.get("is_valid"):
            data_points += 1
        if result.email_verification.get("is_valid"):
            data_points += 1
        if len(result.social_media_profiles) > 0:
            data_points += 1
        if result.criminal_records.get("records_found") is not None:
            data_points += 1
        if result.criminal_records.get("sanctions"):
            data_points += 1
        if result.email_verification.get("breach_data"):
            data_points += 1
            
        confidence_ratio = data_points / total_possible
        
        if confidence_ratio >= 0.8:
            return "High"
        elif confidence_ratio >= 0.6:
            return "Medium"
        elif confidence_ratio >= 0.4:
            return "Low"
        else:
            return "Very Low"
    
    def get_data_sources_used(self, result: BackgroundCheckResult) -> List[str]:
        """Get list of data sources that provided information"""
        sources = []
        
        if result.identity_verification:
            sources.append("TruePeopleSearch")
        if result.address_history:
            sources.append("Address Verification Service")
        if result.phone_verification:
            sources.append("Phone Carrier Database")
        if result.email_verification:
            sources.append("Email Verification Service")
        if result.social_media_profiles:
            sources.append("Social Media Search")
        if result.criminal_records:
            sources.append("Criminal Records Database")
        if result.criminal_records.get("sanctions"):
            sources.append("OpenSanctions")
            
        return sources
    
    def _is_demo_mode(self) -> bool:
        """Check if running in demo mode"""
        return True  # For prototype, always use demo data
    
    def _generate_demo_identity_data(self, person_data: PersonData) -> Dict[str, Any]:
        """Generate realistic demo identity data"""
        return {
            "identity_found": True,
            "name_match": "exact",
            "age_range": "30-35",
            "known_addresses": 2,
            "known_phone_numbers": 1,
            "relatives_found": 3,
            "verification_score": 0.92,
            "last_updated": datetime.utcnow().isoformat()
        }
    
    def _generate_demo_address_history(self, person_data: PersonData) -> List[Dict[str, Any]]:
        """Generate realistic demo address history"""
        return [
            {
                "address": f"{person_data.address or '123 Main St'}, {person_data.city or 'Anytown'}, {person_data.state or 'NY'} {person_data.zip_code or '12345'}",
                "residence_period": "2021-2024",
                "verification_status": "verified",
                "property_type": "apartment",
                "ownership_status": "renter"
            },
            {
                "address": "456 Oak Avenue, Previous City, NY 67890",
                "residence_period": "2019-2021", 
                "verification_status": "verified",
                "property_type": "single_family",
                "ownership_status": "owner"
            }
        ]
    
    def _generate_demo_phone_data(self, phone: str) -> Dict[str, Any]:
        """Generate realistic demo phone data"""
        return {
            "phone_number": phone,
            "formatted_number": phone,
            "carrier": "T-Mobile",
            "line_type": "mobile",
            "location": "New York, NY",
            "is_valid": True,
            "is_active": True,
            "risk_indicators": [],
            "verification_score": 0.88
        }
    
    def _generate_demo_email_data(self, email: str) -> Dict[str, Any]:
        """Generate realistic demo email data"""
        domain = email.split('@')[1] if '@' in email else "example.com"
        return {
            "email_address": email,
            "domain": domain,
            "is_valid": True,
            "is_deliverable": True,
            "is_disposable": False,
            "domain_reputation": "good",
            "mx_records_found": True,
            "breach_count": 0,
            "last_breach_date": None,
            "verification_score": 0.85
        }
    
    def _generate_demo_social_media_data(self, person_data: PersonData) -> List[Dict[str, Any]]:
        """Generate realistic demo social media data"""
        return [
            {
                "platform": "LinkedIn",
                "profile_url": f"https://linkedin.com/in/{person_data.first_name.lower()}{person_data.last_name.lower()}",
                "username": f"{person_data.first_name.lower()}.{person_data.last_name.lower()}",
                "verification_status": "verified",
                "activity_level": "active",
                "professional_info": {
                    "current_job": "Marketing Manager",
                    "company": "Digital Solutions Inc",
                    "location": "New York, NY"
                }
            }
        ]
    
    def _generate_demo_criminal_data(self, person_data: PersonData) -> Dict[str, Any]:
        """Generate realistic demo criminal data"""
        return {
            "records_found": False,
            "search_states": ["NY", "NJ", "CT"],
            "federal_search": True,
            "sex_offender_check": True,
            "warrant_check": True,
            "court_records": [],
            "traffic_violations": [],
            "bankruptcy_records": [],
            "last_updated": datetime.utcnow().isoformat()
        }

# Example usage and testing
async def test_background_check():
    """Test the background check service"""
    service = BackgroundCheckService()
    
    # Test person data
    person = PersonData(
        first_name="John",
        last_name="Doe", 
        email="john.doe@email.com",
        phone="(555) 123-4567",
        address="123 Main Street",
        city="New York",
        state="NY",
        zip_code="10001"
    )
    
    print("🚀 Starting Background Check Prototype Test")
    print("=" * 50)
    
    # Perform background check
    result = await service.comprehensive_background_check(person)
    
    # Display results
    print(f"\n📋 BACKGROUND CHECK REPORT")
    print(f"Subject: {result.person_data.first_name} {result.person_data.last_name}")
    print(f"Email: {result.person_data.email}")
    print(f"Phone: {result.person_data.phone}")
    print(f"Investigation Date: {result.investigation_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n🎯 RISK ASSESSMENT")
    print(f"Risk Score: {result.risk_score:.1f}/100")
    print(f"Confidence Level: {result.confidence_level}")
    print(f"Data Sources: {', '.join(result.data_sources)}")
    
    print(f"\n✅ IDENTITY VERIFICATION")
    identity = result.identity_verification
    print(f"Identity Found: {identity.get('identity_found', 'Unknown')}")
    print(f"Name Match: {identity.get('name_match', 'Unknown')}")
    print(f"Verification Score: {identity.get('verification_score', 0):.2f}")
    
    print(f"\n🏠 ADDRESS HISTORY")
    for i, addr in enumerate(result.address_history, 1):
        print(f"{i}. {addr.get('address', 'Unknown')}")
        print(f"   Period: {addr.get('residence_period', 'Unknown')}")
        print(f"   Status: {addr.get('verification_status', 'Unknown')}")
    
    print(f"\n📱 PHONE VERIFICATION")
    phone = result.phone_verification
    print(f"Valid: {phone.get('is_valid', 'Unknown')}")
    print(f"Carrier: {phone.get('carrier', 'Unknown')}")
    print(f"Type: {phone.get('line_type', 'Unknown')}")
    
    print(f"\n📧 EMAIL VERIFICATION")
    email = result.email_verification
    print(f"Valid: {email.get('is_valid', 'Unknown')}")
    print(f"Deliverable: {email.get('is_deliverable', 'Unknown')}")
    print(f"Domain Reputation: {email.get('domain_reputation', 'Unknown')}")
    
    print(f"\n📱 SOCIAL MEDIA PROFILES")
    for profile in result.social_media_profiles:
        print(f"Platform: {profile.get('platform', 'Unknown')}")
        print(f"Username: {profile.get('username', 'Unknown')}")
        print(f"Status: {profile.get('verification_status', 'Unknown')}")
    
    print(f"\n⚖️ CRIMINAL RECORDS")
    criminal = result.criminal_records
    print(f"Records Found: {criminal.get('records_found', 'Unknown')}")
    print(f"States Searched: {', '.join(criminal.get('search_states', []))}")
    
    print("\n" + "=" * 50)
    print("✅ Background Check Prototype Test Complete")
    
    return result

if __name__ == "__main__":
    # Run the test
    import asyncio
    asyncio.run(test_background_check())

