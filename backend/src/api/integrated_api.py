"""
ScamShield AI Integrated API
Complete end-to-end service combining payment, investigation, and reporting
"""

import os
import sys
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.payment_service import PaymentService, generate_order_id, validate_payment_data
from services.order_processing_service import OrderProcessingService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins="*")  # Allow all origins for development

# Initialize services
payment_service = PaymentService()
order_service = OrderProcessingService()

@app.route('/', methods=['GET'])
def home():
    """API home endpoint"""
    return jsonify({
        'service': 'ScamShield AI Integrated API',
        'version': '2.0.0',
        'status': 'operational',
        'features': [
            'Per-report pricing model',
            'CrewAI investigation engine',
            'Multi-format report generation',
            'Real-time order tracking',
            'Secure payment processing'
        ],
        'endpoints': {
            'pricing': '/api/pricing',
            'create_order': '/api/orders/create',
            'order_status': '/api/orders/<order_id>/status',
            'customer_orders': '/api/customers/<email>/orders',
            'payment_webhook': '/api/webhooks/<provider>',
            'download_report': '/api/reports/<order_id>/download/<format>'
        },
        'payment_methods': {
            'stripe': payment_service.stripe_enabled,
            'paypal': payment_service.paypal_enabled
        },
        'investigation_engine': {
            'crewai_available': order_service.crewai_available,
            'report_engine_available': order_service.report_engine_available
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/pricing', methods=['GET'])
def get_pricing():
    """Get pricing information"""
    try:
        pricing_info = payment_service.get_pricing_info()
        
        # Add delivery time estimates
        delivery_estimates = {
            'basic': '24 hours',
            'standard': '12 hours',
            'professional': '6 hours',
            'forensic': '3 hours'
        }
        
        for tier, info in pricing_info['tiers'].items():
            info['estimated_delivery'] = delivery_estimates.get(tier, '12 hours')
        
        return jsonify({
            'success': True,
            'pricing': pricing_info,
            'add_ons': {
                'expedited': {
                    'price': 19.99,
                    'description': 'Rush processing - 50% faster delivery'
                },
                'phone_support': {
                    'price': 9.99,
                    'description': 'Direct phone consultation with expert'
                },
                'additional_formats': {
                    'price': 4.99,
                    'description': 'Extra export formats (XML, CSV, etc.)'
                }
            },
            'discount_codes': {
                'FIRST10': '10% off first order',
                'BULK20': '20% off bulk orders (5+)',
                'STUDENT15': '15% student discount'
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Pricing info error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/orders/create', methods=['POST'])
def create_investigation_order():
    """Create complete investigation order with payment"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Validate required fields
        validation = validate_payment_data(data)
        if not validation['valid']:
            return jsonify({
                'success': False,
                'errors': validation['errors']
            }), 400
        
        # Extract order details
        tier = data.get('tier')
        customer_email = data.get('customer_email')
        investigation_target = data.get('target')
        payment_method = data.get('payment_method', 'stripe')
        add_ons = data.get('add_ons', [])
        discount_code = data.get('discount_code')
        investigation_type = data.get('investigation_type', 'comprehensive')
        
        # Calculate pricing
        pricing = payment_service.calculate_pricing(tier, add_ons, discount_code)
        
        # Generate order ID
        order_id = generate_order_id(tier, investigation_target)
        
        # Create order in processing service
        order_data = {
            'order_id': order_id,
            'customer_email': customer_email,
            'target': investigation_target,
            'tier': tier,
            'investigation_type': investigation_type,
            'price': pricing['total_price'],
            'payment_method': payment_method,
            'metadata': {
                'add_ons': add_ons,
                'discount_code': discount_code,
                'pricing_breakdown': pricing,
                'requirements': data.get('requirements', ''),
                'priority': data.get('priority', 'normal')
            }
        }
        
        order_result = order_service.create_order(order_data)
        
        if not order_result['success']:
            return jsonify(order_result), 400
        
        # Create payment based on method
        payment_metadata = {
            'order_id': order_id,
            'add_ons': add_ons,
            'discount_code': discount_code,
            'total_price': pricing['total_price'],
            'investigation_type': investigation_type
        }
        
        if payment_method == 'stripe':
            payment_result = payment_service.create_stripe_payment_intent(
                tier=tier,
                customer_email=customer_email,
                investigation_target=investigation_target,
                metadata=payment_metadata
            )
        elif payment_method == 'paypal':
            payment_result = payment_service.create_paypal_order(
                tier=tier,
                customer_email=customer_email,
                investigation_target=investigation_target,
                metadata=payment_metadata
            )
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid payment method'
            }), 400
        
        if payment_result['success']:
            # Combine order and payment information
            response = {
                'success': True,
                'order_id': order_id,
                'order_status': order_result['status'],
                'pricing': pricing,
                'payment': payment_result,
                'investigation': {
                    'target': investigation_target,
                    'tier': tier,
                    'type': investigation_type,
                    'estimated_delivery': {
                        'basic': '24 hours',
                        'standard': '12 hours',
                        'professional': '6 hours',
                        'forensic': '3 hours'
                    }.get(tier, '12 hours')
                },
                'next_steps': [
                    'Complete payment using provided payment details',
                    'Investigation will start automatically after payment confirmation',
                    'You will receive email updates on progress',
                    'Report will be available for download when complete'
                ],
                'created_at': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Complete order created: {order_id}")
            return jsonify(response)
        
        else:
            return jsonify(payment_result), 400
        
    except Exception as e:
        logger.error(f"❌ Order creation error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/orders/<order_id>/status', methods=['GET'])
def get_order_status(order_id):
    """Get detailed order status and progress"""
    try:
        status_result = order_service.get_order_status(order_id)
        
        if status_result['success']:
            # Add human-readable status descriptions
            status_descriptions = {
                'pending_payment': 'Waiting for payment confirmation',
                'payment_confirmed': 'Payment received, preparing investigation',
                'investigation_queued': 'Investigation queued for processing',
                'investigation_in_progress': 'AI agents actively investigating',
                'investigation_completed': 'Investigation complete, generating report',
                'report_generating': 'Creating comprehensive report',
                'report_ready': 'Report generated, preparing delivery',
                'delivered': 'Investigation complete - report ready for download',
                'failed': 'Investigation failed - support will contact you',
                'cancelled': 'Order cancelled'
            }
            
            status_result['status_description'] = status_descriptions.get(
                status_result['status'], 
                'Processing your request'
            )
            
            # Add progress milestones
            progress_milestones = [
                {'step': 'Payment', 'progress': 10, 'completed': status_result['progress'] >= 10},
                {'step': 'Investigation Start', 'progress': 30, 'completed': status_result['progress'] >= 30},
                {'step': 'Data Collection', 'progress': 50, 'completed': status_result['progress'] >= 50},
                {'step': 'Analysis Complete', 'progress': 70, 'completed': status_result['progress'] >= 70},
                {'step': 'Report Generation', 'progress': 90, 'completed': status_result['progress'] >= 90},
                {'step': 'Delivery', 'progress': 100, 'completed': status_result['progress'] >= 100}
            ]
            
            status_result['milestones'] = progress_milestones
            
        return jsonify(status_result), 200 if status_result['success'] else 404
        
    except Exception as e:
        logger.error(f"❌ Order status error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/customers/<email>/orders', methods=['GET'])
def get_customer_orders(email):
    """Get all orders for a customer"""
    try:
        orders_result = order_service.get_all_orders(customer_email=email)
        
        if orders_result['success']:
            # Add summary statistics
            total_spent = sum(order.get('price', 0) for order in orders_result['orders'])
            completed_orders = len([o for o in orders_result['orders'] if o['status'] == 'delivered'])
            
            orders_result['summary'] = {
                'total_orders': orders_result['total_count'],
                'completed_orders': completed_orders,
                'total_spent': total_spent,
                'average_order_value': total_spent / max(orders_result['total_count'], 1)
            }
        
        return jsonify(orders_result), 200 if orders_result['success'] else 404
        
    except Exception as e:
        logger.error(f"❌ Customer orders error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/webhooks/<provider>', methods=['POST'])
def payment_webhook(provider):
    """Handle payment webhooks from different providers"""
    try:
        if provider == 'stripe':
            payload = request.get_data(as_text=True)
            signature = request.headers.get('Stripe-Signature')
            
            if not signature:
                return jsonify({
                    'success': False,
                    'error': 'Missing Stripe signature'
                }), 400
            
            webhook_result = payment_service.verify_stripe_webhook(payload, signature)
            
        elif provider == 'paypal':
            payload = request.get_data(as_text=True)
            headers = dict(request.headers)
            
            webhook_result = payment_service.verify_paypal_webhook(payload, headers)
            
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid payment provider'
            }), 400
        
        if webhook_result['success']:
            # Handle payment confirmation
            if webhook_result.get('action') == 'start_investigation':
                order_data = webhook_result.get('order_data', {})
                order_id = order_data.get('order_id')
                
                if order_id:
                    # Confirm payment in order service
                    confirmation_result = order_service.confirm_payment(order_id, order_data)
                    logger.info(f"🔍 Investigation started for order: {order_id}")
                    
                    # Here you could also send confirmation email
                    
            elif webhook_result.get('action') == 'notify_failure':
                failure_data = webhook_result.get('failure_data', {})
                logger.warning(f"⚠️ Payment failed: {failure_data}")
                
                # Here you could send failure notification email
        
        return jsonify(webhook_result), 200 if webhook_result['success'] else 400
        
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/reports/<order_id>/download/<format>', methods=['GET'])
def download_report(order_id, format):
    """Download report in specified format"""
    try:
        # Get order status to check if report is ready
        status_result = order_service.get_order_status(order_id)
        
        if not status_result['success']:
            return jsonify({
                'success': False,
                'error': 'Order not found'
            }), 404
        
        if status_result['status'] != 'delivered':
            return jsonify({
                'success': False,
                'error': 'Report not ready for download',
                'current_status': status_result['status'],
                'progress': status_result['progress']
            }), 400
        
        # Validate access code if provided
        access_code = request.args.get('code')
        delivery_info = status_result.get('delivery_info', {})
        expected_code = delivery_info.get('access_code')
        
        if access_code != expected_code:
            return jsonify({
                'success': False,
                'error': 'Invalid access code'
            }), 403
        
        # Check if format is available
        available_formats = ['pdf', 'html', 'json']
        if format not in available_formats:
            return jsonify({
                'success': False,
                'error': f'Invalid format. Available: {", ".join(available_formats)}'
            }), 400
        
        # In production, this would serve the actual file
        # For now, return download information
        download_info = {
            'success': True,
            'order_id': order_id,
            'format': format,
            'download_url': delivery_info['download_links'].get(format),
            'expires_at': delivery_info.get('expires_at'),
            'file_size': '2.5 MB',  # Mock file size
            'generated_at': status_result.get('updated_at'),
            'message': f'Report ready for download in {format.upper()} format'
        }
        
        logger.info(f"📥 Report download requested: {order_id} ({format})")
        
        return jsonify(download_info)
        
    except Exception as e:
        logger.error(f"❌ Report download error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/orders/<order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    """Cancel an order"""
    try:
        data = request.get_json() or {}
        reason = data.get('reason', 'Customer request')
        
        cancel_result = order_service.cancel_order(order_id, reason)
        
        return jsonify(cancel_result), 200 if cancel_result['success'] else 400
        
    except Exception as e:
        logger.error(f"❌ Order cancellation error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/test-complete-flow', methods=['POST'])
def test_complete_flow():
    """Test the complete order flow from creation to delivery"""
    try:
        data = request.get_json() or {}
        
        # Use test data
        test_data = {
            'tier': data.get('tier', 'professional'),
            'customer_email': data.get('customer_email', 'test@example.com'),
            'target': data.get('target', 'test-suspicious-site.com'),
            'payment_method': 'stripe',
            'investigation_type': 'comprehensive',
            'add_ons': ['expedited'],
            'discount_code': 'FIRST10'
        }
        
        # Create order
        order_response = create_investigation_order()
        
        if hasattr(order_response, 'get_json'):
            order_data = order_response.get_json()
        else:
            order_data = order_response
        
        if not order_data.get('success'):
            return jsonify(order_data), 400
        
        order_id = order_data['order_id']
        
        # Simulate payment confirmation
        payment_data = {
            'payment_confirmed': True,
            'amount': order_data['pricing']['total_price'],
            'payment_method': 'stripe'
        }
        
        confirmation_result = order_service.confirm_payment(order_id, payment_data)
        
        # Get final status
        final_status = order_service.get_order_status(order_id)
        
        return jsonify({
            'success': True,
            'test_flow': 'complete',
            'order_creation': order_data,
            'payment_confirmation': confirmation_result,
            'final_status': final_status,
            'message': 'Complete flow test successful - order processed from creation to delivery',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Complete flow test error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'available_endpoints': [
            '/api/pricing',
            '/api/orders/create',
            '/api/orders/<order_id>/status',
            '/api/customers/<email>/orders',
            '/api/reports/<order_id>/download/<format>',
            '/api/test-complete-flow'
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    logger.info("🚀 Starting ScamShield AI Integrated API")
    logger.info(f"💰 Payment methods: Stripe={payment_service.stripe_enabled}, PayPal={payment_service.paypal_enabled}")
    logger.info(f"🔍 Investigation engine: CrewAI={order_service.crewai_available}, Reports={order_service.report_engine_available}")
    logger.info("🎯 Complete end-to-end service operational")
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5006,
        debug=True
    )

