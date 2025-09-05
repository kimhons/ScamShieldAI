from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import uuid
import logging
from datetime import datetime, timedelta
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Report pricing configuration
REPORT_PRICING = {
    'basic': {
        'price': 9.99,
        'name': 'Basic Report',
        'pages': '3-5 pages',
        'description': 'Essential fraud investigation for quick risk assessment',
        'delivery_time': '24 hours',
        'features': [
            'Identity Verification',
            'Basic Digital Footprint Analysis', 
            'Compliance Screening (Sanctions/PEP)',
            'Risk Assessment Summary',
            'PDF & HTML Export',
            '24-hour delivery',
            'Email support'
        ]
    },
    'standard': {
        'price': 24.99,
        'name': 'Standard Report',
        'pages': '8-12 pages',
        'description': 'Comprehensive analysis with detailed findings and strategic recommendations',
        'delivery_time': '12 hours',
        'features': [
            'Everything in Basic',
            'Advanced Digital Forensics',
            'Financial Intelligence Analysis',
            'Threat Assessment Matrix',
            'Strategic Recommendations',
            'All Export Formats (PDF, HTML, JSON, Word)',
            '12-hour delivery',
            'Priority email support',
            'Investigation methodology disclosure'
        ]
    },
    'professional': {
        'price': 49.99,
        'name': 'Professional Report',
        'pages': '15-25 pages',
        'description': 'Expert-level analysis with advanced risk modeling and detailed methodology',
        'delivery_time': '6 hours',
        'features': [
            'Everything in Standard',
            'Multi-Agent AI Investigation (8 specialized agents)',
            'Advanced Risk Modeling & Confidence Scoring',
            'Cross-Source Data Validation',
            'Detailed Evidence Chain Documentation',
            'Professional Formatting for Business Use',
            'API Integration Results (9+ data sources)',
            '6-hour delivery',
            'Phone & email support',
            'Custom investigation parameters'
        ]
    },
    'forensic': {
        'price': 99.99,
        'name': 'Forensic Report',
        'pages': '25-40 pages',
        'description': 'Legal-grade documentation with complete evidence chain for court proceedings',
        'delivery_time': '3 hours',
        'features': [
            'Everything in Professional',
            'Legal-Grade Documentation Standards',
            'Complete Chain of Custody',
            'Expert Certification & Digital Signatures',
            'Regulatory Compliance (GDPR, CCPA)',
            'Court-Admissible Evidence Format',
            'Detailed Methodology & Source Attribution',
            'Quality Assurance Validation',
            '3-hour delivery',
            'Dedicated support specialist',
            'Expert witness consultation available'
        ]
    }
}

# Investigation types
INVESTIGATION_TYPES = {
    'domain': {
        'name': 'Domain/Website Investigation',
        'description': 'Comprehensive analysis of suspicious websites and domains',
        'icon': '🌐'
    },
    'email': {
        'name': 'Email Investigation',
        'description': 'Advanced email header and content analysis for fraud detection',
        'icon': '📧'
    },
    'person': {
        'name': 'Background Check',
        'description': 'Professional background verification and identity analysis',
        'icon': '👤'
    },
    'company': {
        'name': 'Business Investigation',
        'description': 'Corporate due diligence and business verification',
        'icon': '🏢'
    },
    'crypto': {
        'name': 'Cryptocurrency Investigation',
        'description': 'Blockchain analysis and cryptocurrency compliance screening',
        'icon': '₿'
    },
    'comprehensive': {
        'name': 'Comprehensive Investigation',
        'description': 'Full multi-source investigation using all available methods',
        'icon': '🔍'
    }
}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'ScamShield AI Investigation API',
        'version': '2.0.0',
        'pricing_model': 'per_report'
    })

@app.route('/api/pricing', methods=['GET'])
def get_pricing():
    """Get all report pricing tiers"""
    try:
        return jsonify({
            'success': True,
            'pricing_model': 'per_report',
            'currency': 'USD',
            'tiers': REPORT_PRICING,
            'investigation_types': INVESTIGATION_TYPES,
            'payment_methods': ['stripe', 'paypal', 'credit_card'],
            'features': {
                'multi_format_export': True,
                'ai_powered_analysis': True,
                'professional_reports': True,
                'instant_delivery': True,
                'money_back_guarantee': True
            },
            'comparison': {
                'traditional_services': {
                    'price_range': '$500 - $5,000',
                    'delivery_time': '2-4 weeks',
                    'data_sources': '2-3',
                    'format_options': 'PDF only'
                },
                'scamshield_ai': {
                    'price_range': '$9.99 - $99.99',
                    'delivery_time': '3-24 hours',
                    'data_sources': '9+',
                    'format_options': 'PDF, HTML, JSON, Word'
                },
                'savings': '98% cost reduction'
            }
        })
    except Exception as e:
        logger.error(f"Error getting pricing: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/investigation/quote', methods=['POST'])
def get_investigation_quote():
    """Get a quote for an investigation"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['subject', 'report_tier', 'investigation_type']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        subject = data['subject']
        report_tier = data['report_tier']
        investigation_type = data['investigation_type']
        
        # Validate inputs
        if report_tier not in REPORT_PRICING:
            return jsonify({
                'success': False,
                'error': f'Invalid report tier: {report_tier}. Valid options: {list(REPORT_PRICING.keys())}'
            }), 400
            
        if investigation_type not in INVESTIGATION_TYPES:
            return jsonify({
                'success': False,
                'error': f'Invalid investigation type: {investigation_type}. Valid options: {list(INVESTIGATION_TYPES.keys())}'
            }), 400
        
        # Generate quote
        pricing_info = REPORT_PRICING[report_tier]
        investigation_info = INVESTIGATION_TYPES[investigation_type]
        
        quote = {
            'quote_id': str(uuid.uuid4()),
            'subject': subject,
            'investigation_type': investigation_info,
            'report_tier': pricing_info,
            'total_price': pricing_info['price'],
            'estimated_delivery': pricing_info['delivery_time'],
            'valid_until': (datetime.utcnow() + timedelta(hours=24)).isoformat(),
            'includes': pricing_info['features'],
            'next_steps': [
                'Review quote details',
                'Proceed to secure payment',
                'Investigation begins immediately after payment',
                f'Receive professional report within {pricing_info["delivery_time"]}'
            ]
        }
        
        return jsonify({
            'success': True,
            'quote': quote,
            'message': f'Quote generated for {investigation_info["name"]} - {pricing_info["name"]}'
        })
        
    except Exception as e:
        logger.error(f"Error generating quote: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/investigation/start', methods=['POST'])
def start_investigation():
    """Start a new investigation (requires payment in production)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['subject', 'report_tier', 'investigation_type', 'customer_email']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        subject = data['subject']
        report_tier = data['report_tier']
        investigation_type = data['investigation_type']
        customer_email = data['customer_email']
        
        # Validate inputs
        if report_tier not in REPORT_PRICING:
            return jsonify({
                'success': False,
                'error': f'Invalid report tier: {report_tier}'
            }), 400
            
        if investigation_type not in INVESTIGATION_TYPES:
            return jsonify({
                'success': False,
                'error': f'Invalid investigation type: {investigation_type}'
            }), 400
        
        # Generate investigation ID
        investigation_id = str(uuid.uuid4())
        
        # Get pricing and investigation info
        pricing_info = REPORT_PRICING[report_tier]
        investigation_info = INVESTIGATION_TYPES[investigation_type]
        
        # Create investigation record
        investigation = {
            'id': investigation_id,
            'subject': subject,
            'investigation_type': investigation_info,
            'report_tier': pricing_info,
            'customer_email': customer_email,
            'price': pricing_info['price'],
            'status': 'payment_required',
            'created_at': datetime.utcnow().isoformat(),
            'estimated_completion': (datetime.utcnow() + timedelta(hours=get_delivery_hours(report_tier))).isoformat(),
            'payment_url': f'https://payment.scamshield.ai/pay/{investigation_id}',
            'tracking_url': f'/api/investigation/status/{investigation_id}'
        }
        
        return jsonify({
            'success': True,
            'investigation': investigation,
            'message': f'Investigation created. Payment of ${pricing_info["price"]} required to proceed.',
            'next_steps': [
                'Complete secure payment',
                'Investigation begins immediately',
                'Track progress in real-time',
                f'Receive report within {pricing_info["delivery_time"]}'
            ]
        })
        
    except Exception as e:
        logger.error(f"Error starting investigation: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/investigation/demo', methods=['POST'])
def demo_investigation():
    """Run a demo investigation (free, limited features)"""
    try:
        data = request.get_json()
        subject = data.get('subject', 'demo-suspicious-site.com')
        
        logger.info(f"Running demo investigation for {subject}")
        
        # Generate demo investigation ID
        demo_id = str(uuid.uuid4())
        
        # Simulate investigation process
        demo_result = {
            'id': demo_id,
            'subject': subject,
            'status': 'completed',
            'demo_mode': True,
            'completed_at': datetime.utcnow().isoformat(),
            'findings': {
                'risk_level': 'MEDIUM',
                'risk_score': 0.65,
                'confidence': 0.78,
                'summary': f'Demo analysis of {subject} reveals moderate risk indicators.',
                'key_findings': [
                    'Domain age: 45 days (relatively new)',
                    'SSL certificate: Valid but recently issued',
                    'No sanctions matches found',
                    'Limited online presence detected'
                ],
                'recommendations': [
                    'Proceed with caution',
                    'Verify business credentials independently',
                    'Consider professional investigation for full analysis'
                ]
            },
            'limitations': [
                'Demo limited to basic analysis only',
                'Reduced data source access (2/9 sources)',
                'No export capabilities',
                'Watermarked results',
                'No detailed methodology provided'
            ],
            'upgrade_benefits': [
                'Access to all 9+ premium data sources',
                'Professional report formatting',
                'Multiple export formats (PDF, HTML, JSON, Word)',
                'Legal-grade documentation',
                'Complete investigation methodology',
                'No watermarks or limitations'
            ]
        }
        
        return jsonify({
            'success': True,
            'demo': demo_result,
            'message': 'Demo investigation completed. Upgrade for comprehensive analysis.',
            'upgrade_url': '/pricing',
            'full_investigation_price': {
                'basic': '$9.99',
                'standard': '$24.99', 
                'professional': '$49.99',
                'forensic': '$99.99'
            }
        })
        
    except Exception as e:
        logger.error(f"Error running demo investigation: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/investigation/status/<investigation_id>', methods=['GET'])
def get_investigation_status(investigation_id):
    """Get investigation status and progress"""
    try:
        # In production, this would query the database
        # For demo, return realistic status progression
        
        import random
        
        # Simulate different status stages
        statuses = ['payment_required', 'in_progress', 'completed']
        current_status = random.choice(['in_progress', 'completed'])
        
        if current_status == 'in_progress':
            status_data = {
                'id': investigation_id,
                'status': 'in_progress',
                'progress': random.randint(25, 90),
                'current_step': random.choice([
                    'Deploying AI agents',
                    'Analyzing domain intelligence',
                    'Checking sanctions databases',
                    'Performing threat assessment',
                    'Generating professional report'
                ]),
                'steps_completed': [
                    '✅ Investigation initiated',
                    '✅ Multi-agent deployment',
                    '✅ Data source integration',
                    '🔄 Analysis in progress'
                ],
                'estimated_completion': f'{random.randint(5, 45)} minutes',
                'agents_deployed': random.randint(6, 8),
                'data_sources_queried': random.randint(7, 9),
                'findings_discovered': random.randint(12, 28)
            }
        else:
            status_data = {
                'id': investigation_id,
                'status': 'completed',
                'progress': 100,
                'current_step': 'Investigation completed',
                'completed_at': datetime.utcnow().isoformat(),
                'final_results': {
                    'risk_level': 'HIGH',
                    'risk_score': 0.78,
                    'confidence': 0.92,
                    'agents_deployed': 8,
                    'data_sources_queried': 9,
                    'findings_discovered': 24,
                    'report_pages': random.randint(15, 25)
                },
                'download_links': {
                    'pdf': f'/api/download/{investigation_id}/pdf',
                    'html': f'/api/download/{investigation_id}/html',
                    'json': f'/api/download/{investigation_id}/json',
                    'word': f'/api/download/{investigation_id}/word'
                }
            }
        
        return jsonify({
            'success': True,
            'investigation': status_data
        })
        
    except Exception as e:
        logger.error(f"Error getting investigation status: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_platform_stats():
    """Get platform statistics"""
    try:
        stats = {
            'investigations_completed': 12847,
            'customer_satisfaction': 99.2,
            'average_delivery_time': '4.2 hours',
            'data_sources_integrated': 9,
            'ai_agents_available': 8,
            'cost_savings_vs_traditional': '98%',
            'uptime': '99.9%',
            'countries_served': 45,
            'languages_supported': 12,
            'report_formats': 4
        }
        
        return jsonify({
            'success': True,
            'stats': stats,
            'last_updated': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting platform stats: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

def get_delivery_hours(report_tier):
    """Get delivery time in hours based on report tier"""
    delivery_hours = {
        'basic': 24,
        'standard': 12,
        'professional': 6,
        'forensic': 3
    }
    return delivery_hours.get(report_tier, 24)

if __name__ == '__main__':
    logger.info("Starting ScamShield AI Investigation API with per-report pricing model")
    app.run(debug=True, host='0.0.0.0', port=5000)

