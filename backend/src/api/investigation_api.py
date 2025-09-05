from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
import json
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our report generation components
from reports.simplified_report_engine import ScamShieldReportEngine
from reports.multi_format_exporter import MultiFormatExporter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize report engine and exporter
report_engine = ScamShieldReportEngine()
exporter = MultiFormatExporter()

# Report pricing configuration
REPORT_PRICING = {
    'basic': {
        'price': 9.99,
        'name': 'Basic Report',
        'pages': '3-5 pages',
        'description': 'Essential fraud investigation for quick risk assessment',
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

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'ScamShield AI Investigation API',
        'version': '1.0.0'
    })

@app.route('/api/pricing', methods=['GET'])
def get_pricing():
    """Get all report pricing tiers"""
    try:
        return jsonify({
            'success': True,
            'pricing': REPORT_PRICING,
            'currency': 'USD',
            'payment_methods': ['credit_card', 'paypal', 'stripe'],
            'features': {
                'multi_format_export': True,
                'ai_powered_analysis': True,
                'professional_reports': True,
                'instant_delivery': True
            }
        })
    except Exception as e:
        logger.error(f"Error getting pricing: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/investigation/start', methods=['POST'])
def start_investigation():
    """Start a new investigation with specified report tier"""
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
        
        # Validate report tier
        if report_tier not in REPORT_PRICING:
            return jsonify({
                'success': False,
                'error': f'Invalid report tier: {report_tier}'
            }), 400
        
        # Generate investigation ID
        investigation_id = str(uuid.uuid4())
        
        # Get pricing info
        pricing_info = REPORT_PRICING[report_tier]
        
        # Create investigation record
        investigation = {
            'id': investigation_id,
            'subject': subject,
            'investigation_type': investigation_type,
            'report_tier': report_tier,
            'price': pricing_info['price'],
            'status': 'pending_payment',
            'created_at': datetime.utcnow().isoformat(),
            'estimated_delivery': get_estimated_delivery(report_tier),
            'payment_required': True
        }
        
        return jsonify({
            'success': True,
            'investigation': investigation,
            'pricing': pricing_info,
            'payment_url': f'/api/payment/{investigation_id}',
            'message': f'Investigation created. Payment of ${pricing_info["price"]} required to proceed.'
        })
        
    except Exception as e:
        logger.error(f"Error starting investigation: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/investigation/execute', methods=['POST'])
def execute_investigation():
    """Execute investigation after payment confirmation (demo mode)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'investigation_id' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing investigation_id'
            }), 400
        
        investigation_id = data['investigation_id']
        subject = data.get('subject', 'demo-subject.com')
        report_tier = data.get('report_tier', 'professional')
        
        logger.info(f"Executing investigation {investigation_id} for {subject}")
        
        # Generate investigation report
        report_data = report_engine.generate_investigation_report(
            subject=subject,
            investigation_type='comprehensive',
            report_tier=report_tier
        )
        
        # Export to multiple formats
        export_result = exporter.export_all_formats(
            report_data=report_data,
            base_filename=f"ScamShield_Report_{subject.replace('.', '_')}_{investigation_id[:8]}"
        )
        
        # Update investigation status
        investigation_result = {
            'id': investigation_id,
            'subject': subject,
            'report_tier': report_tier,
            'status': 'completed',
            'completed_at': datetime.utcnow().isoformat(),
            'report_data': report_data,
            'export_files': export_result['files'],
            'quality_score': report_data.get('quality_score', 0.95),
            'risk_score': report_data.get('risk_assessment', {}).get('overall_risk_score', 0.5),
            'confidence_level': report_data.get('confidence_level', 0.87)
        }
        
        return jsonify({
            'success': True,
            'investigation': investigation_result,
            'message': 'Investigation completed successfully',
            'download_links': {
                'pdf': f'/api/download/{investigation_id}/pdf',
                'html': f'/api/download/{investigation_id}/html',
                'json': f'/api/download/{investigation_id}/json',
                'word': f'/api/download/{investigation_id}/word'
            }
        })
        
    except Exception as e:
        logger.error(f"Error executing investigation: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/investigation/demo', methods=['POST'])
def demo_investigation():
    """Demo investigation without payment (limited features)"""
    try:
        data = request.get_json()
        subject = data.get('subject', 'demo-suspicious-site.com')
        
        logger.info(f"Running demo investigation for {subject}")
        
        # Generate basic demo report
        report_data = report_engine.generate_investigation_report(
            subject=subject,
            investigation_type='basic',
            report_tier='basic'
        )
        
        # Add demo limitations
        report_data['demo_mode'] = True
        report_data['limitations'] = [
            'Limited to basic analysis only',
            'Reduced data source access',
            'Watermarked output',
            'No export capabilities'
        ]
        
        return jsonify({
            'success': True,
            'demo': True,
            'report_data': report_data,
            'message': 'Demo investigation completed. Upgrade for full features.',
            'upgrade_url': '/pricing'
        })
        
    except Exception as e:
        logger.error(f"Error running demo investigation: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/download/<investigation_id>/<format>', methods=['GET'])
def download_report(investigation_id, format):
    """Download investigation report in specified format"""
    try:
        # Validate format
        valid_formats = ['pdf', 'html', 'json', 'word']
        if format not in valid_formats:
            return jsonify({
                'success': False,
                'error': f'Invalid format. Must be one of: {valid_formats}'
            }), 400
        
        # In production, this would retrieve from database/storage
        # For demo, we'll generate a sample file
        output_dir = '/tmp/scamshield_reports'
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate sample report for download
        sample_report = {
            'investigation_id': investigation_id,
            'subject': 'sample-investigation.com',
            'report_tier': 'professional',
            'findings': 'Sample investigation findings...',
            'risk_score': 0.65,
            'generated_at': datetime.utcnow().isoformat()
        }
        
        # Export sample report
        export_result = exporter.export_all_formats(
            report_data=sample_report,
            base_filename=f"ScamShield_Report_{investigation_id}",
            output_dir=output_dir
        )
        
        # Get the requested file
        file_path = export_result['files'].get(format)
        if not file_path or not os.path.exists(file_path):
            return jsonify({
                'success': False,
                'error': f'Report file not found for format: {format}'
            }), 404
        
        # Determine MIME type
        mime_types = {
            'pdf': 'application/pdf',
            'html': 'text/html',
            'json': 'application/json',
            'word': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        }
        
        return send_file(
            file_path,
            mimetype=mime_types[format],
            as_attachment=True,
            download_name=os.path.basename(file_path)
        )
        
    except Exception as e:
        logger.error(f"Error downloading report: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/investigation/status/<investigation_id>', methods=['GET'])
def get_investigation_status(investigation_id):
    """Get investigation status and progress"""
    try:
        # In production, this would query the database
        # For demo, return sample status
        status_data = {
            'id': investigation_id,
            'status': 'in_progress',
            'progress': 75,
            'current_step': 'Analyzing threat intelligence',
            'steps_completed': [
                'Domain analysis completed',
                'SSL certificate verification completed',
                'Reputation checking completed',
                'Threat intelligence analysis in progress'
            ],
            'estimated_completion': '2 minutes',
            'agents_deployed': 6,
            'data_sources_queried': 8
        }
        
        return jsonify({
            'success': True,
            'investigation': status_data
        })
        
    except Exception as e:
        logger.error(f"Error getting investigation status: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

def get_estimated_delivery(report_tier):
    """Get estimated delivery time based on report tier"""
    delivery_times = {
        'basic': '24 hours',
        'standard': '12 hours', 
        'professional': '6 hours',
        'forensic': '3 hours'
    }
    return delivery_times.get(report_tier, '24 hours')

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('/tmp/scamshield_reports', exist_ok=True)
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)

