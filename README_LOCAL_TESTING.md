# ScamShield AI - Local Testing Guide

## 🚀 GitHub Repository

**Repository URL:** https://github.com/kimhons/ScamShieldAI

## 📋 Prerequisites

Before running ScamShield AI locally, ensure you have the following installed:

- **Python 3.11+**
- **Node.js 18+**
- **Git**
- **Redis** (optional, for advanced caching)

## 🛠️ Quick Setup

### 1. Clone the Repository

```bash
git clone https://github.com/kimhons/ScamShieldAI.git
cd ScamShieldAI
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip3 install -r requirements.txt

# Install additional packages for API integrations
pip3 install aiohttp requests python-json-logger prometheus-client

# Set up environment variables (optional - many APIs work without keys)
cp .env.example .env
# Edit .env file with your API keys (see API Keys section below)
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install Node.js dependencies
npm install

# Build the frontend
npm run build
```

## 🔑 API Keys Configuration (Optional)

Many APIs work without authentication, but for full functionality, you can add API keys to the `.env` file:

```bash
# Free APIs (no keys required)
EMAILREP_API_KEY=  # Leave empty - no auth required
IPAPI_API_KEY=     # Leave empty - no auth required
JSON_TEST_API_KEY= # Leave empty - no auth required

# Paid APIs (optional for enhanced features)
HUNTER_IO_API_KEY=your_hunter_io_key_here
IPGEOLOCATION_API_KEY=your_ipgeolocation_key_here
NUMVERIFY_API_KEY=your_numverify_key_here
CLOUDMERSIVE_API_KEY=your_cloudmersive_key_here
SECURITYTRAILS_API_KEY=your_securitytrails_key_here
ABUSEIPDB_API_KEY=your_abuseipdb_key_here
```

## 🧪 Testing the API Integration Framework

### 1. Run the Comprehensive API Test

```bash
cd backend/tests
python3 simple_api_test.py
```

**Expected Output:**
```
================================================================================
SCAMSHIELD AI - API INTEGRATION TEST
================================================================================
🔍 Testing API Manager Health Check...
Overall API Health: 100.0%
Healthy Services: 6/6

🔍 Testing Individual Investigations...
--- Email Investigation Test ---
Email: test@example.com
Risk Score: 85.0/100 (HIGH)
Confidence: 95.0%
Processing Time: 2.456s
APIs Used: email_validation, email_security, domain_security
Summary: Email test@example.com analysis: Risk 85.0/100 (HIGH)

✅ ALL API INTEGRATION TESTS PASSED!
```

### 2. Run Individual API Wrapper Tests

```bash
# Test specific API categories
cd backend/src

# Test email APIs
python3 -c "
import asyncio
from integrations.email_apis import EmailAPIWrapper

async def test():
    wrapper = EmailAPIWrapper()
    async with wrapper:
        result = await wrapper.validate_email('test@example.com')
        print(f'Email validation result: {result.data}')

asyncio.run(test())
"

# Test IP geolocation APIs
python3 -c "
import asyncio
from integrations.geolocation_apis import GeolocationAPIWrapper

async def test():
    wrapper = GeolocationAPIWrapper()
    async with wrapper:
        result = await wrapper.geolocate_ip('8.8.8.8')
        print(f'IP geolocation result: {result.data}')

asyncio.run(test())
"
```

## 🌐 Running the Complete Platform

### 1. Start the Backend API Server

```bash
cd backend/src/api
python3 live_crewai_api.py
```

**Server will start on:** http://localhost:5004

### 2. Start the Payment API Server

```bash
cd backend/src/api
python3 payment_api.py
```

**Server will start on:** http://localhost:5005

### 3. Start the Integrated API Server

```bash
cd backend/src/api
python3 integrated_api.py
```

**Server will start on:** http://localhost:5006

### 4. Test the API Endpoints

```bash
# Test health check
curl http://localhost:5006/api/health

# Test pricing information
curl http://localhost:5006/api/pricing

# Test email investigation
curl -X POST http://localhost:5006/api/investigate \
  -H "Content-Type: application/json" \
  -d '{
    "target_type": "email",
    "target_value": "test@example.com",
    "investigation_level": "standard"
  }'

# Test phone investigation
curl -X POST http://localhost:5006/api/investigate \
  -H "Content-Type: application/json" \
  -d '{
    "target_type": "phone",
    "target_value": "+1234567890",
    "investigation_level": "standard"
  }'

# Test IP investigation
curl -X POST http://localhost:5006/api/investigate \
  -H "Content-Type: application/json" \
  -d '{
    "target_type": "ip",
    "target_value": "8.8.8.8",
    "investigation_level": "standard"
  }'
```

## 🎨 Frontend Testing

### 1. Serve the Frontend

```bash
cd frontend
npm start
# Or serve the built files
python3 -m http.server 3000 --directory build
```

**Frontend will be available at:** http://localhost:3000

### 2. Test the Demo Pages

Open the following demo pages in your browser:

- **Main Website:** `/home/ubuntu/scamshield-vibrant-animated-website.html`
- **Admin Dashboard:** `/home/ubuntu/scamshield-admin-dashboard.html`
- **Client Dashboard:** `/home/ubuntu/scamshield-client-dashboard.html`
- **Order Tracking:** `/home/ubuntu/scamshield-order-tracking-demo.html`

## 🔧 Advanced Testing

### 1. Load Testing

```bash
# Install Apache Bench for load testing
sudo apt-get install apache2-utils

# Test API performance
ab -n 100 -c 10 http://localhost:5006/api/health

# Test investigation endpoint
ab -n 50 -c 5 -p test_data.json -T application/json http://localhost:5006/api/investigate
```

### 2. Database Testing (if using PostgreSQL)

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb scamshield_ai

# Run database migrations (if implemented)
cd backend
python3 manage.py migrate
```

### 3. Redis Caching Testing (optional)

```bash
# Install Redis
sudo apt-get install redis-server

# Start Redis
sudo systemctl start redis-server

# Test Redis connection
redis-cli ping
```

## 📊 Monitoring and Metrics

### 1. View API Statistics

```bash
# Get comprehensive statistics
curl http://localhost:5006/api/statistics

# Get health status
curl http://localhost:5006/api/health
```

### 2. Check Logs

```bash
# View application logs
tail -f backend/logs/scamshield.log

# View API access logs
tail -f backend/logs/api_access.log
```

## 🐛 Troubleshooting

### Common Issues and Solutions

**1. Import Errors**
```bash
# Ensure you're in the correct directory
cd backend/src
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**2. API Connection Timeouts**
```bash
# Check internet connectivity
ping google.com

# Test specific API endpoints
curl -v https://api.emailrep.io/test@example.com
```

**3. Port Already in Use**
```bash
# Find process using port
sudo lsof -i :5006

# Kill process
sudo kill -9 <PID>
```

**4. Missing Dependencies**
```bash
# Install all required packages
pip3 install aiohttp requests asyncio python-json-logger prometheus-client
```

## 🎯 Performance Benchmarks

**Expected Performance (without API keys):**
- Email Investigation: 2-5 seconds
- Phone Investigation: 1-3 seconds  
- IP Investigation: 1-4 seconds
- Domain Investigation: 1-3 seconds
- URL Investigation: 2-6 seconds

**Expected Performance (with API keys):**
- Email Investigation: 5-15 seconds
- Phone Investigation: 3-8 seconds
- IP Investigation: 2-6 seconds
- Domain Investigation: 2-5 seconds
- URL Investigation: 4-12 seconds

## 🚀 Production Deployment

For production deployment, see:
- `docs/api_integration_guide.md`
- `docs/monitoring_and_logging_guide.md`
- `ScamShield_AI_API_Integration_Final_Report.md`

## 📞 Support

If you encounter any issues:

1. Check the logs in `backend/logs/`
2. Verify API keys in `.env` file
3. Ensure all dependencies are installed
4. Check network connectivity
5. Review the troubleshooting section above

## 🎉 Success Indicators

You'll know the system is working correctly when:

✅ All API health checks return "healthy"
✅ Investigation endpoints return structured results
✅ Response times are within expected ranges
✅ No critical errors in logs
✅ Frontend demos load and function properly

Happy testing! 🚀

