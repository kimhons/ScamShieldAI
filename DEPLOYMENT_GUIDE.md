# 🚀 ScamShield AI - Local Deployment Guide

This guide will help you set up and run the complete ScamShield AI platform locally.

## 📋 **Prerequisites**

- **Python 3.11+** (with pip)
- **Node.js 18+** (with npm)
- **Git** for version control
- **Web Browser** (Chrome, Firefox, Safari, Edge)

## 🔧 **Quick Setup (5 Minutes)**

### **1. Clone Repository**
```bash
git clone https://github.com/kimhons/ScamShieldAI.git
cd ScamShieldAI
```

### **2. Install Dependencies**
```bash
# Backend dependencies
cd backend
pip3 install -r requirements.txt
pip3 install -r requirements_dashboard.txt

# Additional packages for full functionality
pip3 install aiohttp requests python-json-logger flask-cors
```

### **3. Start Backend Services**

**Terminal 1 - Main Investigation API:**
```bash
cd backend/src/api
python3 integrated_api.py
# Runs on http://localhost:5006
```

**Terminal 2 - Client Dashboard API:**
```bash
cd backend/src/api
python3 client_dashboard_api.py
# Runs on http://localhost:5007
```

**Terminal 3 - CrewAI Investigation API:**
```bash
cd backend/src/api
python3 live_crewai_api.py
# Runs on http://localhost:5004
```

### **4. Open Dashboards**

**Main Marketing Website:**
```bash
# Open in browser
open demos/scamshield-vibrant-animated-website.html
# OR navigate to: file:///path/to/ScamShieldAI/demos/scamshield-vibrant-animated-website.html
```

**Client Dashboard (Connected to Backend):**
```bash
# Open in browser
open frontend/src/components/ClientDashboardConnected.html
# OR navigate to: file:///path/to/ScamShieldAI/frontend/src/components/ClientDashboardConnected.html
```

**Admin Dashboard:**
```bash
# Open in browser
open demos/scamshield-admin-dashboard.html
# OR navigate to: file:///path/to/ScamShieldAI/demos/scamshield-admin-dashboard.html
```

## 🧪 **Testing the Platform**

### **1. Test Backend APIs**
```bash
# Test main API health
curl http://localhost:5006/api/health

# Test dashboard API
curl http://localhost:5007/api/health

# Test CrewAI API
curl http://localhost:5004/api/status
```

### **2. Test Client Dashboard**
1. Open `frontend/src/components/ClientDashboardConnected.html`
2. Click **"Try Demo Account"** button
3. You should see: "Demo login successful!" notification
4. Dashboard loads with Sarah Johnson's profile and sample data

### **3. Test Investigation Workflow**
1. In the Client Dashboard, click **"+ Start Investigation"**
2. Enter test data: `suspicious@scammer.com`
3. Select **"Standard Investigation ($24.99)"**
4. Click **"💳 Proceed to Payment"**
5. System creates investigation order and shows confirmation

### **4. Test Evidence Upload**
1. In the investigation modal, try the drag & drop area
2. Add links in the "Add Relevant Links" section
3. Add notes in the "Additional Notes" textarea
4. All data is captured and sent to backend

## 📁 **File Structure Guide**

### **Main Entry Points:**
- **Marketing Website**: `demos/scamshield-vibrant-animated-website.html`
- **Client Dashboard**: `frontend/src/components/ClientDashboardConnected.html`
- **Admin Dashboard**: `demos/scamshield-admin-dashboard.html`

### **Backend APIs:**
- **Port 5006**: Main investigation and order processing
- **Port 5007**: Client dashboard with authentication
- **Port 5004**: CrewAI multi-agent investigation system

### **Demo Files:**
```
demos/
├── scamshield-vibrant-animated-website.html    # Main marketing site
├── scamshield-admin-dashboard.html             # Admin interface
├── scamshield-client-dashboard.html            # Client dashboard demo
└── scamshield-order-tracking-demo.html         # Order tracking demo
```

## 🔧 **Configuration (Optional)**

### **API Keys (For Enhanced Features)**
Create `backend/.env` file:
```env
# AI Providers (Optional - has fallbacks)
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
ANTHROPIC_API_KEY=your_anthropic_key
DEEPSEEK_API_KEY=your_deepseek_key

# External APIs (Optional - has mock data)
WHOISXML_API_KEY=your_whoisxml_key
SHODAN_API_KEY=your_shodan_key
IPINFO_API_KEY=your_ipinfo_key

# Payment Processing (Optional - has simulation)
STRIPE_SECRET_KEY=your_stripe_key
PAYPAL_CLIENT_ID=your_paypal_id
```

**Note**: The platform works without API keys using simulation mode and mock data.

## 🚨 **Troubleshooting**

### **Common Issues:**

**1. Port Already in Use:**
```bash
# Kill existing processes
pkill -f "python3.*api"
# Or use different ports by editing the Python files
```

**2. Module Not Found:**
```bash
# Install missing packages
pip3 install flask flask-cors requests aiohttp python-json-logger
```

**3. Dashboard Not Loading:**
- Ensure backend APIs are running (check terminal output)
- Check browser console for errors (F12)
- Verify file paths are correct for your system

**4. CORS Errors:**
- Backend APIs include CORS headers
- Try opening HTML files via `file://` protocol
- Or serve via simple HTTP server: `python3 -m http.server 8000`

### **Verification Commands:**
```bash
# Check if APIs are running
curl http://localhost:5006/api/health
curl http://localhost:5007/api/health
curl http://localhost:5004/api/status

# Check processes
ps aux | grep python3

# Check ports
netstat -tulpn | grep :500
```

## 🎯 **Demo Scenarios**

### **Scenario 1: Basic Investigation**
1. Open Client Dashboard
2. Use demo login
3. Start investigation with email: `test@suspicious.com`
4. Select Basic Investigation ($9.99)
5. Complete workflow

### **Scenario 2: Evidence Upload**
1. Start new investigation
2. Upload sample files (any image/document)
3. Add suspicious links
4. Add investigation notes
5. Select Professional Investigation ($49.99)

### **Scenario 3: Admin Management**
1. Open Admin Dashboard
2. View user analytics and revenue metrics
3. Check recent investigations
4. Monitor system performance

## 📊 **Expected Results**

### **Client Dashboard:**
- ✅ Demo login works instantly
- ✅ User stats show: 7 reports, $347 spent, 3 threats detected
- ✅ Recent reports display with realistic data
- ✅ Investigation modal opens with full functionality
- ✅ Evidence upload accepts files and links
- ✅ Payment processing creates orders

### **Backend APIs:**
- ✅ Health checks return 200 OK
- ✅ Demo authentication creates session
- ✅ Investigation creation returns order IDs
- ✅ File uploads process successfully
- ✅ Status updates work in real-time

### **Performance:**
- ✅ Dashboard loads in <2 seconds
- ✅ API responses in <500ms
- ✅ Investigation creation in <3 seconds
- ✅ File uploads process immediately

## 🚀 **Next Steps**

### **For Development:**
1. Set up API keys for enhanced functionality
2. Configure database for persistent storage
3. Set up payment processing for real transactions
4. Deploy to cloud infrastructure

### **For Production:**
1. Configure environment variables
2. Set up SSL certificates
3. Configure load balancing
4. Set up monitoring and logging

## 📞 **Support**

If you encounter issues:
1. Check this guide first
2. Review terminal output for errors
3. Check browser console (F12) for frontend issues
4. Create GitHub issue with error details

---

**ScamShield AI** - Complete fraud investigation platform ready to run locally in 5 minutes!

*Built with ❤️ for easy deployment and testing*

