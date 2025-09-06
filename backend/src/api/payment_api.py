"""
ScamShield AI Payment API
RESTful endpoints for payment processing
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins="*")  # Allow all origins for development

# Initialize payment service
payment_service = PaymentService()

@app.route('/', methods=['GET'])
def home():
    """API home endpoint"""
    return jsonify({
        'service': 'ScamShield AI Payment API',
        'version': '1.0.0',
        'status': 'operational',
        'endpoints': {
            'pricing': '/api/pricing',
            'create_stripe_payment': '/api/payments/stripe/create',
            'create_paypal_payment': '/api/payments/paypal/create',
            'stripe_webhook': '/api/webhooks/stripe',
            'paypal_webhook': '/api/webhooks/paypal',
            'payment_status': '/api/payments/status/<payment_id>/<provider>'
        },
        'payment_methods': {
            'stripe': payment_service.stripe_enabled,
            'paypal': payment_service.paypal_enabled
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/pricing', methods=['GET'])
def get_pricing():
    """Get pricing information for all tiers"""
    try:
        pricing_info = payment_service.get_pricing_info()
        
        return jsonify({
            'success': True,
            'pricing': pricing_info,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Pricing info error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/pricing/calculate', methods=['POST'])
def calculate_pricing():
    """Calculate pricing with add-ons and discounts"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        tier = data.get('tier')
        add_ons = data.get('add_ons', [])
        discount_code = data.get('discount_code')
        
        if not tier:
            return jsonify({
                'success': False,
                'error': 'Tier is required'
            }), 400
        
        pricing = payment_service.calculate_pricing(tier, add_ons, discount_code)
        
        return jsonify({
            'success': True,
            'pricing': pricing,
            'timestamp': datetime.now().isoformat()
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        logger.error(f"❌ Pricing calculation error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/payments/stripe/create', methods=['POST'])
def create_stripe_payment():
    """Create Stripe payment intent"""
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
        
        tier = data.get('tier')
        customer_email = data.get('customer_email')
        investigation_target = data.get('target')
        metadata = data.get('metadata', {})
        
        # Generate order ID
        order_id = generate_order_id(tier, investigation_target)
        metadata['order_id'] = order_id
        
        # Create payment intent
        result = payment_service.create_stripe_payment_intent(
            tier=tier,
            customer_email=customer_email,
            investigation_target=investigation_target,
            metadata=metadata
        )
        
        if result['success']:
            logger.info(f"✅ Stripe payment intent created for order: {order_id}")
            result['order_id'] = order_id
            
        return jsonify(result), 200 if result['success'] else 400
        
    except Exception as e:
        logger.error(f"❌ Stripe payment creation error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/payments/paypal/create', methods=['POST'])
def create_paypal_payment():
    """Create PayPal payment order"""
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
        
        tier = data.get('tier')
        customer_email = data.get('customer_email')
        investigation_target = data.get('target')
        metadata = data.get('metadata', {})
        
        # Generate order ID
        order_id = generate_order_id(tier, investigation_target)
        metadata['order_id'] = order_id
        
        # Create PayPal order
        result = payment_service.create_paypal_order(
            tier=tier,
            customer_email=customer_email,
            investigation_target=investigation_target,
            metadata=metadata
        )
        
        if result['success']:
            logger.info(f"✅ PayPal order created for order: {order_id}")
            result['order_id'] = order_id
            
        return jsonify(result), 200 if result['success'] else 400
        
    except Exception as e:
        logger.error(f"❌ PayPal payment creation error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/webhooks/stripe', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events"""
    try:
        payload = request.get_data(as_text=True)
        signature = request.headers.get('Stripe-Signature')
        
        if not signature:
            return jsonify({
                'success': False,
                'error': 'Missing Stripe signature'
            }), 400
        
        result = payment_service.verify_stripe_webhook(payload, signature)
        
        if result['success']:
            logger.info(f"✅ Stripe webhook processed successfully")
            
            # Handle specific actions
            if result.get('action') == 'start_investigation':
                # Here you would trigger the investigation process
                logger.info(f"🔍 Starting investigation for order: {result.get('order_data', {}).get('payment_id')}")
            
            elif result.get('action') == 'notify_failure':
                # Here you would send failure notification
                logger.warning(f"⚠️ Payment failed notification: {result.get('failure_data', {}).get('payment_id')}")
        
        return jsonify(result), 200 if result['success'] else 400
        
    except Exception as e:
        logger.error(f"❌ Stripe webhook error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/webhooks/paypal', methods=['POST'])
def paypal_webhook():
    """Handle PayPal webhook events"""
    try:
        payload = request.get_data(as_text=True)
        headers = dict(request.headers)
        
        result = payment_service.verify_paypal_webhook(payload, headers)
        
        if result['success']:
            logger.info(f"✅ PayPal webhook processed successfully")
            
            # Handle specific actions
            if result.get('action') == 'start_investigation':
                # Here you would trigger the investigation process
                logger.info(f"🔍 Starting investigation for PayPal order: {result.get('order_data', {}).get('payment_id')}")
            
            elif result.get('action') == 'notify_failure':
                # Here you would send failure notification
                logger.warning(f"⚠️ PayPal payment failed notification: {result.get('failure_data', {}).get('payment_id')}")
        
        return jsonify(result), 200 if result['success'] else 400
        
    except Exception as e:
        logger.error(f"❌ PayPal webhook error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/payments/status/<payment_id>/<provider>', methods=['GET'])
def get_payment_status(payment_id, provider):
    """Get payment status from provider"""
    try:
        if provider not in ['stripe', 'paypal']:
            return jsonify({
                'success': False,
                'error': 'Invalid payment provider'
            }), 400
        
        result = payment_service.get_payment_status(payment_id, provider)
        
        return jsonify(result), 200 if result['success'] else 400
        
    except Exception as e:
        logger.error(f"❌ Payment status check error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/orders/create', methods=['POST'])
def create_investigation_order():
    """Create investigation order with payment"""
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
        
        tier = data.get('tier')
        customer_email = data.get('customer_email')
        investigation_target = data.get('target')
        payment_method = data.get('payment_method', 'stripe')
        add_ons = data.get('add_ons', [])
        discount_code = data.get('discount_code')
        
        # Calculate pricing
        pricing = payment_service.calculate_pricing(tier, add_ons, discount_code)
        
        # Generate order ID
        order_id = generate_order_id(tier, investigation_target)
        
        # Create order metadata
        metadata = {
            'order_id': order_id,
            'add_ons': add_ons,
            'discount_code': discount_code,
            'total_price': pricing['total_price']
        }
        
        # Create payment based on method
        if payment_method == 'stripe':
            payment_result = payment_service.create_stripe_payment_intent(
                tier=tier,
                customer_email=customer_email,
                investigation_target=investigation_target,
                metadata=metadata
            )
        elif payment_method == 'paypal':
            payment_result = payment_service.create_paypal_order(
                tier=tier,
                customer_email=customer_email,
                investigation_target=investigation_target,
                metadata=metadata
            )
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid payment method'
            }), 400
        
        if payment_result['success']:
            # Combine order and payment information
            order_response = {
                'success': True,
                'order_id': order_id,
                'pricing': pricing,
                'payment': payment_result,
                'investigation': {
                    'target': investigation_target,
                    'tier': tier,
                    'estimated_delivery': '24 hours'  # Based on tier
                },
                'created_at': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Investigation order created: {order_id}")
            return jsonify(order_response)
        
        else:
            return jsonify(payment_result), 400
        
    except Exception as e:
        logger.error(f"❌ Order creation error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/test-payment', methods=['POST'])
def test_payment():
    """Test payment functionality"""
    try:
        data = request.get_json() or {}
        
        # Default test data
        test_data = {
            'tier': data.get('tier', 'professional'),
            'customer_email': data.get('customer_email', 'test@example.com'),
            'target': data.get('target', 'test-domain.com'),
            'payment_method': data.get('payment_method', 'stripe')
        }
        
        # Calculate pricing
        pricing = payment_service.calculate_pricing(
            tier=test_data['tier'],
            add_ons=['expedited'],
            discount_code='FIRST10'
        )
        
        # Generate test order ID
        order_id = generate_order_id(test_data['tier'], test_data['target'])
        
        return jsonify({
            'success': True,
            'test_mode': True,
            'order_id': order_id,
            'pricing': pricing,
            'payment_methods_available': {
                'stripe': payment_service.stripe_enabled,
                'paypal': payment_service.paypal_enabled
            },
            'test_data': test_data,
            'message': 'Payment system is operational and ready for testing',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Payment test error: {e}")
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
            '/api/payments/stripe/create',
            '/api/payments/paypal/create',
            '/api/orders/create',
            '/api/test-payment'
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    logger.info("🚀 Starting ScamShield AI Payment API")
    logger.info(f"✅ Payment methods available: Stripe={payment_service.stripe_enabled}, PayPal={payment_service.paypal_enabled}")
    logger.info("💰 Per-report pricing model active")
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5005,
        debug=True
    )

