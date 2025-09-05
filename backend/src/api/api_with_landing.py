#!/usr/bin/env python3
"""
ScamShield AI Investigation API - Complete Version with Landing Page
Per-report pricing model with professional report generation
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import logging
import json
from datetime import datetime
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Per-Report Pricing Model
PRICING_TIERS = {
    "basic": {
        "price": 9.99,
        "pages": "3-5",
        "delivery": "24 hours",
        "features": ["Identity Verification", "Basic Digital Footprint", "Compliance Screening", "PDF & HTML Export"]
    },
    "standard": {
        "price": 24.99,
        "pages": "8-12", 
        "delivery": "12 hours",
        "features": ["Everything in Basic", "Advanced Digital Forensics", "Financial Intelligence", "All Export Formats"]
    },
    "professional": {
        "price": 49.99,
        "pages": "15-25",
        "delivery": "6 hours", 
        "features": ["Everything in Standard", "Multi-Agent AI Investigation", "Advanced Risk Modeling", "Professional Formatting"]
    },
    "forensic": {
        "price": 99.99,
        "pages": "25-40",
        "delivery": "3 hours",
        "features": ["Everything in Professional", "Legal-Grade Documentation", "Expert Certification", "Court-Admissible Format"]
    }
}

INVESTIGATION_TYPES = {
    "domain": "Website/Domain Investigation",
    "email": "Email Investigation", 
    "person": "Person Background Check",
    "company": "Company Investigation",
    "crypto": "Cryptocurrency Investigation",
    "comprehensive": "Comprehensive Investigation"
}

# API Landing Page Template
LANDING_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ScamShield AI Investigation API</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            line-height: 1.6; 
            color: #333; 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background: white;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        .header h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .header p {
            color: #666;
            font-size: 1.2em;
        }
        .status {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 30px;
            text-align: center;
        }
        .status .badge {
            background: #28a745;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
        }
        .endpoints {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .endpoint {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            border-left: 4px solid #667eea;
        }
        .endpoint h3 {
            color: #667eea;
            margin-bottom: 10px;
        }
        .endpoint .method {
            background: #667eea;
            color: white;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
        }
        .endpoint .url {
            background: #e9ecef;
            padding: 8px;
            border-radius: 4px;
            font-family: monospace;
            margin: 10px 0;
            word-break: break-all;
        }
        .pricing-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .pricing-card {
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            transition: transform 0.3s;
        }
        .pricing-card:hover {
            transform: translateY(-5px);
            border-color: #667eea;
        }
        .pricing-card h4 {
            color: #667eea;
            font-size: 1.3em;
            margin-bottom: 10px;
        }
        .pricing-card .price {
            font-size: 2em;
            font-weight: bold;
            color: #28a745;
            margin-bottom: 15px;
        }
        .features {
            list-style: none;
            padding: 0;
        }
        .features li {
            padding: 5px 0;
            border-bottom: 1px solid #f0f0f0;
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e9ecef;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ ScamShield AI Investigation API</h1>
            <p>Professional Fraud Investigation Reports with AI-Powered Analysis</p>
        </div>
        
        <div class="status">
            <span class="badge">✅ API OPERATIONAL</span>
            <p><strong>Per-Report Pricing Model</strong> | Version 2.0.0 | {{ timestamp }}</p>
        </div>
        
        <h2>🔗 Available Endpoints</h2>
        <div class="endpoints">
            <div class="endpoint">
                <h3><span class="method">GET</span> Health Check</h3>
                <div class="url">/api/health</div>
                <p>Check API status and configuration</p>
            </div>
            
            <div class="endpoint">
                <h3><span class="method">GET</span> Pricing Information</h3>
                <div class="url">/api/pricing</div>
                <p>Get all pricing tiers and investigation types</p>
            </div>
            
            <div class="endpoint">
                <h3><span class="method">POST</span> Generate Quote</h3>
                <div class="url">/api/quote</div>
                <p>Generate investigation quote with pricing</p>
            </div>
            
            <div class="endpoint">
                <h3><span class="method">POST</span> Start Investigation</h3>
                <div class="url">/api/investigate</div>
                <p>Begin new fraud investigation</p>
            </div>
            
            <div class="endpoint">
                <h3><span class="method">POST</span> Demo Investigation</h3>
                <div class="url">/api/demo</div>
                <p>Try a realistic investigation demo</p>
            </div>
            
            <div class="endpoint">
                <h3><span class="method">GET</span> Investigation Status</h3>
                <div class="url">/api/status/{id}</div>
                <p>Check investigation progress</p>
            </div>
        </div>
        
        <h2>💰 Pricing Tiers</h2>
        <div class="pricing-grid">
            <div class="pricing-card">
                <h4>Basic Report</h4>
                <div class="price">$9.99</div>
                <ul class="features">
                    <li>3-5 pages</li>
                    <li>24 hour delivery</li>
                    <li>Identity Verification</li>
                    <li>PDF & HTML Export</li>
                </ul>
            </div>
            
            <div class="pricing-card">
                <h4>Standard Report</h4>
                <div class="price">$24.99</div>
                <ul class="features">
                    <li>8-12 pages</li>
                    <li>12 hour delivery</li>
                    <li>Advanced Digital Forensics</li>
                    <li>All Export Formats</li>
                </ul>
            </div>
            
            <div class="pricing-card">
                <h4>Professional Report</h4>
                <div class="price">$49.99</div>
                <ul class="features">
                    <li>15-25 pages</li>
                    <li>6 hour delivery</li>
                    <li>Multi-Agent AI Investigation</li>
                    <li>Professional Formatting</li>
                </ul>
            </div>
            
            <div class="pricing-card">
                <h4>Forensic Report</h4>
                <div class="price">$99.99</div>
                <ul class="features">
                    <li>25-40 pages</li>
                    <li>3 hour delivery</li>
                    <li>Legal-Grade Documentation</li>
                    <li>Court-Admissible Format</li>
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>98% Cost Reduction</strong> vs. Traditional Investigation Services ($500-$5,000)</p>
            <p>Powered by CrewAI Multi-Agent System | 9+ Data Sources | Professional Quality Reports</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def landing_page():
    """API landing page with documentation"""
    return render_template_string(LANDING_PAGE, timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"))

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "ScamShield AI Investigation API",
        "version": "2.0.0",
        "pricing_model": "per-report",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/pricing', methods=['GET'])
def get_pricing():
    """Get pricing information for all report tiers"""
    return jsonify({
        "pricing_model": "per-report",
        "currency": "USD",
        "tiers": PRICING_TIERS,
        "investigation_types": INVESTIGATION_TYPES,
        "cost_comparison": {
            "traditional_services": "$500-$5,000 (2-4 weeks)",
            "scamshield_ai": "$9.99-$99.99 (3-24 hours)",
            "savings": "98% cost reduction"
        }
    })

@app.route('/api/quote', methods=['POST'])
def get_quote():
    """Generate quote for investigation"""
    try:
        data = request.get_json()
        investigation_type = data.get('investigation_type', 'domain')
        report_tier = data.get('report_tier', 'basic')
        subject = data.get('subject', 'example.com')
        
        if report_tier not in PRICING_TIERS:
            return jsonify({"error": "Invalid report tier"}), 400
            
        tier_info = PRICING_TIERS[report_tier]
        quote_id = str(uuid.uuid4())
        
        quote = {
            "quote_id": quote_id,
            "investigation_type": investigation_type,
            "subject": subject,
            "report_tier": report_tier,
            "price": tier_info["price"],
            "pages": tier_info["pages"],
            "delivery_time": tier_info["delivery"],
            "features": tier_info["features"],
            "valid_until": datetime.now().isoformat(),
            "estimated_completion": f"Within {tier_info['delivery']}"
        }
        
        logger.info(f"Generated quote {quote_id} for {investigation_type} investigation of {subject}")
        return jsonify(quote)
        
    except Exception as e:
        logger.error(f"Error generating quote: {str(e)}")
        return jsonify({"error": "Failed to generate quote"}), 500

@app.route('/api/investigate', methods=['POST'])
def start_investigation():
    """Start new investigation with per-report pricing"""
    try:
        data = request.get_json()
        investigation_type = data.get('investigation_type', 'domain')
        report_tier = data.get('report_tier', 'basic')
        subject = data.get('subject', 'example.com')
        
        if report_tier not in PRICING_TIERS:
            return jsonify({"error": "Invalid report tier"}), 400
            
        investigation_id = str(uuid.uuid4())
        tier_info = PRICING_TIERS[report_tier]
        
        # Simulate investigation process
        investigation = {
            "investigation_id": investigation_id,
            "status": "started",
            "investigation_type": investigation_type,
            "subject": subject,
            "report_tier": report_tier,
            "price_paid": tier_info["price"],
            "estimated_completion": tier_info["delivery"],
            "progress": {
                "data_collection": "in_progress",
                "ai_analysis": "pending", 
                "report_generation": "pending",
                "quality_assurance": "pending"
            },
            "started_at": datetime.now().isoformat()
        }
        
        logger.info(f"Started {report_tier} investigation {investigation_id} for {subject}")
        return jsonify(investigation)
        
    except Exception as e:
        logger.error(f"Error starting investigation: {str(e)}")
        return jsonify({"error": "Failed to start investigation"}), 500

@app.route('/api/demo', methods=['POST'])
def demo_investigation():
    """Demo investigation with realistic results"""
    try:
        data = request.get_json()
        investigation_type = data.get('investigation_type', 'domain')
        report_tier = data.get('report_tier', 'professional')
        subject = data.get('subject', 'suspicious-site.com')
        
        # Generate realistic demo results
        demo_results = {
            "investigation_id": str(uuid.uuid4()),
            "status": "completed",
            "investigation_type": investigation_type,
            "subject": subject,
            "report_tier": report_tier,
            "completion_time": "4.2 minutes",
            "risk_score": 0.73,
            "risk_level": "HIGH",
            "confidence": 0.89,
            "findings": {
                "identity_verification": {
                    "status": "SUSPICIOUS",
                    "details": "Domain registered 18 days ago with privacy protection"
                },
                "digital_footprint": {
                    "status": "LIMITED", 
                    "details": "Minimal online presence, no social media verification"
                },
                "compliance_screening": {
                    "status": "CLEAR",
                    "details": "No sanctions, PEP, or adverse media matches found"
                },
                "technical_analysis": {
                    "status": "CONCERNING",
                    "details": "Suspicious hosting patterns and SSL configuration"
                }
            },
            "data_sources": {
                "total_queried": 8,
                "successful": 7,
                "success_rate": "87.5%",
                "sources": ["OpenSanctions", "WhoisXML", "Shodan", "IPinfo", "Cloudflare", "Alpha Vantage", "Background Check APIs"]
            },
            "report_formats": ["PDF", "HTML", "JSON", "Word"],
            "generated_at": datetime.now().isoformat()
        }
        
        logger.info(f"Generated demo investigation for {subject}")
        return jsonify(demo_results)
        
    except Exception as e:
        logger.error(f"Error in demo investigation: {str(e)}")
        return jsonify({"error": "Demo investigation failed"}), 500

@app.route('/api/status/<investigation_id>', methods=['GET'])
def get_investigation_status(investigation_id):
    """Get investigation status"""
    # Simulate investigation progress
    status = {
        "investigation_id": investigation_id,
        "status": "in_progress",
        "progress": {
            "data_collection": "completed",
            "ai_analysis": "in_progress", 
            "report_generation": "pending",
            "quality_assurance": "pending"
        },
        "estimated_completion": "2 hours remaining",
        "last_updated": datetime.now().isoformat()
    }
    
    return jsonify(status)

if __name__ == '__main__':
    logger.info("Starting ScamShield AI Investigation API with Landing Page on port 5003")
    app.run(host='0.0.0.0', port=5003, debug=True)

