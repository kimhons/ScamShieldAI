#!/usr/bin/env python3
"""
ScamShield AI Client Dashboard API Test Suite
Comprehensive testing for all dashboard API endpoints
"""

import requests
import json
import time
import os
from datetime import datetime

# API Configuration
API_BASE_URL = "http://localhost:5007"
TEST_USER_EMAIL = "test@scamshield.com"
TEST_USER_PASSWORD = "test123"
TEST_USER_NAME = "Test User"

class DashboardAPITester:
    def __init__(self, base_url=API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.user_id = None
        self.investigation_id = None
        
    def log(self, message, status="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {status}: {message}")
    
    def test_health_check(self):
        """Test API health check"""
        self.log("Testing health check endpoint...")
        try:
            response = self.session.get(f"{self.base_url}/api/health")
            if response.status_code == 200:
                data = response.json()
                self.log(f"✅ Health check passed: {data['status']}")
                return True
            else:
                self.log(f"❌ Health check failed: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Health check error: {e}", "ERROR")
            return False
    
    def test_pricing_endpoint(self):
        """Test pricing endpoint"""
        self.log("Testing pricing endpoint...")
        try:
            response = self.session.get(f"{self.base_url}/api/pricing")
            if response.status_code == 200:
                data = response.json()
                pricing = data.get('pricing', {})
                self.log(f"✅ Pricing endpoint working: {len(pricing)} tiers available")
                for tier, info in pricing.items():
                    self.log(f"   {tier.title()}: ${info['price']}")
                return True
            else:
                self.log(f"❌ Pricing endpoint failed: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Pricing endpoint error: {e}", "ERROR")
            return False
    
    def test_demo_login(self):
        """Test demo login functionality"""
        self.log("Testing demo login...")
        try:
            response = self.session.post(f"{self.base_url}/api/auth/demo-login")
            if response.status_code == 200:
                data = response.json()
                user = data.get('user', {})
                self.user_id = user.get('user_id')
                self.log(f"✅ Demo login successful: {user.get('name')} ({user.get('email')})")
                return True
            else:
                self.log(f"❌ Demo login failed: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Demo login error: {e}", "ERROR")
            return False
    
    def test_user_registration(self):
        """Test user registration"""
        self.log("Testing user registration...")
        try:
            # First logout if logged in
            self.session.post(f"{self.base_url}/api/auth/logout")
            
            user_data = {
                "email": TEST_USER_EMAIL,
                "name": TEST_USER_NAME,
                "password": TEST_USER_PASSWORD
            }
            
            response = self.session.post(
                f"{self.base_url}/api/auth/register",
                json=user_data
            )
            
            if response.status_code == 201:
                data = response.json()
                user = data.get('user', {})
                self.user_id = user.get('user_id')
                self.log(f"✅ Registration successful: {user.get('name')}")
                return True
            elif response.status_code == 409:
                self.log("ℹ️ User already exists, testing login instead...")
                return self.test_user_login()
            else:
                self.log(f"❌ Registration failed: {response.status_code} - {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Registration error: {e}", "ERROR")
            return False
    
    def test_user_login(self):
        """Test user login"""
        self.log("Testing user login...")
        try:
            login_data = {
                "email": TEST_USER_EMAIL,
                "password": TEST_USER_PASSWORD
            }
            
            response = self.session.post(
                f"{self.base_url}/api/auth/login",
                json=login_data
            )
            
            if response.status_code == 200:
                data = response.json()
                user = data.get('user', {})
                self.user_id = user.get('user_id')
                self.log(f"✅ Login successful: {user.get('name')}")
                return True
            else:
                self.log(f"❌ Login failed: {response.status_code} - {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Login error: {e}", "ERROR")
            return False
    
    def test_dashboard_stats(self):
        """Test dashboard statistics endpoint"""
        self.log("Testing dashboard statistics...")
        try:
            response = self.session.get(f"{self.base_url}/api/dashboard/stats")
            if response.status_code == 200:
                data = response.json()
                stats = data.get('stats', {})
                self.log(f"✅ Dashboard stats retrieved:")
                self.log(f"   Reports Generated: {stats.get('reports_generated', 0)}")
                self.log(f"   Total Spent: ${stats.get('total_spent', 0)}")
                self.log(f"   Threats Detected: {stats.get('threats_detected', 0)}")
                self.log(f"   Success Rate: {stats.get('success_rate', 0)}%")
                return True
            else:
                self.log(f"❌ Dashboard stats failed: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Dashboard stats error: {e}", "ERROR")
            return False
    
    def test_recent_reports(self):
        """Test recent reports endpoint"""
        self.log("Testing recent reports...")
        try:
            response = self.session.get(f"{self.base_url}/api/dashboard/recent-reports")
            if response.status_code == 200:
                data = response.json()
                reports = data.get('reports', [])
                self.log(f"✅ Recent reports retrieved: {len(reports)} reports")
                for report in reports[:3]:  # Show first 3
                    self.log(f"   {report.get('investigation_id')}: {report.get('target_value')} ({report.get('status')})")
                return True
            else:
                self.log(f"❌ Recent reports failed: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Recent reports error: {e}", "ERROR")
            return False
    
    def test_create_investigation(self):
        """Test creating new investigation"""
        self.log("Testing investigation creation...")
        try:
            investigation_data = {
                "target_type": "email",
                "target_value": "suspicious@example.com",
                "investigation_level": "standard",
                "additional_notes": "Test investigation for API testing",
                "evidence_links": [
                    {
                        "url": "https://suspicious-website.com",
                        "description": "Suspicious website linked to email"
                    }
                ]
            }
            
            response = self.session.post(
                f"{self.base_url}/api/investigations/create",
                json=investigation_data
            )
            
            if response.status_code == 201:
                data = response.json()
                investigation = data.get('investigation', {})
                self.investigation_id = investigation.get('investigation_id')
                self.log(f"✅ Investigation created: {self.investigation_id}")
                self.log(f"   Target: {investigation.get('target_value')}")
                self.log(f"   Level: {investigation.get('investigation_level')}")
                self.log(f"   Price: ${investigation.get('price')}")
                return True
            else:
                self.log(f"❌ Investigation creation failed: {response.status_code} - {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Investigation creation error: {e}", "ERROR")
            return False
    
    def test_investigation_status(self):
        """Test investigation status endpoint"""
        if not self.investigation_id:
            self.log("⚠️ No investigation ID available for status test", "WARNING")
            return False
        
        self.log("Testing investigation status...")
        try:
            response = self.session.get(f"{self.base_url}/api/investigations/{self.investigation_id}/status")
            if response.status_code == 200:
                data = response.json()
                investigation = data.get('investigation', {})
                self.log(f"✅ Investigation status retrieved:")
                self.log(f"   ID: {investigation.get('investigation_id')}")
                self.log(f"   Status: {investigation.get('status')}")
                self.log(f"   Target: {investigation.get('target_value')}")
                self.log(f"   Created: {investigation.get('created_at')}")
                return True
            else:
                self.log(f"❌ Investigation status failed: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Investigation status error: {e}", "ERROR")
            return False
    
    def test_evidence_upload(self):
        """Test evidence file upload"""
        if not self.investigation_id:
            self.log("⚠️ No investigation ID available for evidence upload test", "WARNING")
            return False
        
        self.log("Testing evidence upload...")
        try:
            # Create a test file
            test_file_content = "This is a test evidence file for ScamShield AI testing."
            test_file_path = "/tmp/test_evidence.txt"
            
            with open(test_file_path, 'w') as f:
                f.write(test_file_content)
            
            # Upload the file
            with open(test_file_path, 'rb') as f:
                files = {'files': ('test_evidence.txt', f, 'text/plain')}
                response = self.session.post(
                    f"{self.base_url}/api/investigations/{self.investigation_id}/upload-evidence",
                    files=files
                )
            
            # Clean up test file
            os.remove(test_file_path)
            
            if response.status_code == 200:
                data = response.json()
                uploaded_files = data.get('files', [])
                self.log(f"✅ Evidence upload successful: {len(uploaded_files)} files")
                for file_info in uploaded_files:
                    self.log(f"   {file_info.get('filename')} ({file_info.get('file_size')} bytes)")
                return True
            else:
                self.log(f"❌ Evidence upload failed: {response.status_code} - {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Evidence upload error: {e}", "ERROR")
            return False
    
    def test_payment_processing(self):
        """Test payment processing"""
        if not self.investigation_id:
            self.log("⚠️ No investigation ID available for payment test", "WARNING")
            return False
        
        self.log("Testing payment processing...")
        try:
            payment_data = {
                "investigation_id": self.investigation_id,
                "payment_method": "stripe"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/payment/process",
                json=payment_data
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log(f"✅ Payment processed successfully:")
                self.log(f"   Payment ID: {data.get('payment_id')}")
                self.log(f"   Investigation Status: {data.get('investigation_status')}")
                return True
            else:
                self.log(f"❌ Payment processing failed: {response.status_code} - {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Payment processing error: {e}", "ERROR")
            return False
    
    def test_logout(self):
        """Test user logout"""
        self.log("Testing user logout...")
        try:
            response = self.session.post(f"{self.base_url}/api/auth/logout")
            if response.status_code == 200:
                self.log("✅ Logout successful")
                return True
            else:
                self.log(f"❌ Logout failed: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Logout error: {e}", "ERROR")
            return False
    
    def run_comprehensive_test(self):
        """Run all tests in sequence"""
        self.log("🚀 Starting ScamShield AI Dashboard API Comprehensive Test Suite")
        self.log("=" * 70)
        
        tests = [
            ("Health Check", self.test_health_check),
            ("Pricing Endpoint", self.test_pricing_endpoint),
            ("Demo Login", self.test_demo_login),
            ("Dashboard Stats", self.test_dashboard_stats),
            ("Recent Reports", self.test_recent_reports),
            ("User Registration", self.test_user_registration),
            ("Dashboard Stats (Authenticated)", self.test_dashboard_stats),
            ("Create Investigation", self.test_create_investigation),
            ("Investigation Status", self.test_investigation_status),
            ("Evidence Upload", self.test_evidence_upload),
            ("Payment Processing", self.test_payment_processing),
            ("Investigation Status (After Payment)", self.test_investigation_status),
            ("User Logout", self.test_logout)
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            self.log(f"\n📋 Running: {test_name}")
            self.log("-" * 50)
            
            try:
                if test_func():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                self.log(f"❌ Test '{test_name}' crashed: {e}", "ERROR")
                failed += 1
            
            time.sleep(1)  # Brief pause between tests
        
        # Summary
        self.log("\n" + "=" * 70)
        self.log("🎯 TEST SUITE SUMMARY")
        self.log("=" * 70)
        self.log(f"✅ Passed: {passed}")
        self.log(f"❌ Failed: {failed}")
        self.log(f"📊 Success Rate: {(passed / (passed + failed) * 100):.1f}%")
        
        if failed == 0:
            self.log("🎉 ALL TESTS PASSED! Dashboard API is fully operational.")
        else:
            self.log(f"⚠️ {failed} tests failed. Please check the API implementation.")
        
        return failed == 0

def main():
    """Main test execution"""
    print("ScamShield AI Dashboard API Test Suite")
    print("=====================================")
    
    # Check if API is running
    try:
        response = requests.get(f"{API_BASE_URL}/api/health", timeout=5)
        if response.status_code != 200:
            print(f"❌ API not responding at {API_BASE_URL}")
            print("Please start the dashboard API server first:")
            print("python3 client_dashboard_api.py")
            return False
    except requests.exceptions.RequestException:
        print(f"❌ Cannot connect to API at {API_BASE_URL}")
        print("Please start the dashboard API server first:")
        print("python3 client_dashboard_api.py")
        return False
    
    # Run tests
    tester = DashboardAPITester()
    success = tester.run_comprehensive_test()
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

