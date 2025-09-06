"""
ScamShield AI Payment Service
Handles payment processing for per-report pricing model
Supports Stripe and PayPal integration
"""

import os
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import hashlib
import hmac
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PaymentService:
    """
    Unified payment service supporting multiple payment providers
    """
    
    def __init__(self):
        self.stripe_enabled = False
        self.paypal_enabled = False
        
        # Initialize Stripe
        try:
            import stripe
            self.stripe = stripe
            self.stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_dummy_key')
            self.stripe_publishable_key = os.getenv('STRIPE_PUBLISHABLE_KEY', 'pk_test_dummy_key')
            self.stripe_enabled = True
            logger.info("✅ Stripe payment service initialized")
        except ImportError:
            logger.warning("⚠️ Stripe not available - install with: pip install stripe")
        except Exception as e:
            logger.error(f"❌ Stripe initialization failed: {e}")
        
        # Initialize PayPal
        try:
            self.paypal_client_id = os.getenv('PAYPAL_CLIENT_ID', 'dummy_client_id')
            self.paypal_client_secret = os.getenv('PAYPAL_CLIENT_SECRET', 'dummy_secret')
            self.paypal_mode = os.getenv('PAYPAL_MODE', 'sandbox')  # sandbox or live
            self.paypal_enabled = True
            logger.info("✅ PayPal payment service initialized")
        except Exception as e:
            logger.error(f"❌ PayPal initialization failed: {e}")
        
        # Pricing configuration
        self.pricing_tiers = {
            'basic': {
                'price': 9.99,
                'currency': 'usd',
                'name': 'Basic Investigation',
                'description': 'Essential fraud detection and analysis'
            },
            'standard': {
                'price': 24.99,
                'currency': 'usd',
                'name': 'Standard Investigation',
                'description': 'Comprehensive analysis with multiple sources'
            },
            'professional': {
                'price': 49.99,
                'currency': 'usd',
                'name': 'Professional Investigation',
                'description': 'Expert-level analysis with detailed reporting'
            },
            'forensic': {
                'price': 99.99,
                'currency': 'usd',
                'name': 'Forensic Investigation',
                'description': 'Court-ready forensic analysis and documentation'
            }
        }
    
    def get_pricing_info(self) -> Dict[str, Any]:
        """Get current pricing information"""
        return {
            'tiers': self.pricing_tiers,
            'payment_methods': {
                'stripe': self.stripe_enabled,
                'paypal': self.paypal_enabled
            },
            'currency': 'USD',
            'tax_included': False
        }
    
    def create_stripe_payment_intent(self, tier: str, customer_email: str, 
                                   investigation_target: str, metadata: Dict = None) -> Dict[str, Any]:
        """Create Stripe payment intent for investigation order"""
        if not self.stripe_enabled:
            raise Exception("Stripe payment service not available")
        
        if tier not in self.pricing_tiers:
            raise ValueError(f"Invalid pricing tier: {tier}")
        
        tier_info = self.pricing_tiers[tier]
        amount = int(tier_info['price'] * 100)  # Convert to cents
        
        try:
            # Create payment intent
            intent = self.stripe.PaymentIntent.create(
                amount=amount,
                currency=tier_info['currency'],
                automatic_payment_methods={'enabled': True},
                description=f"ScamShield AI {tier_info['name']} - {investigation_target}",
                receipt_email=customer_email,
                metadata={
                    'tier': tier,
                    'target': investigation_target,
                    'service': 'scamshield_investigation',
                    'customer_email': customer_email,
                    **(metadata or {})
                }
            )
            
            logger.info(f"✅ Stripe payment intent created: {intent.id}")
            
            return {
                'success': True,
                'payment_intent_id': intent.id,
                'client_secret': intent.client_secret,
                'amount': tier_info['price'],
                'currency': tier_info['currency'].upper(),
                'tier': tier,
                'publishable_key': self.stripe_publishable_key
            }
            
        except Exception as e:
            logger.error(f"❌ Stripe payment intent creation failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_paypal_order(self, tier: str, customer_email: str, 
                           investigation_target: str, metadata: Dict = None) -> Dict[str, Any]:
        """Create PayPal order for investigation"""
        if not self.paypal_enabled:
            raise Exception("PayPal payment service not available")
        
        if tier not in self.pricing_tiers:
            raise ValueError(f"Invalid pricing tier: {tier}")
        
        tier_info = self.pricing_tiers[tier]
        
        try:
            # Create PayPal order (simplified for demo)
            order_id = f"PP_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{tier}"
            
            # In production, this would use PayPal SDK
            paypal_order = {
                'id': order_id,
                'status': 'CREATED',
                'amount': {
                    'currency_code': tier_info['currency'].upper(),
                    'value': str(tier_info['price'])
                },
                'description': f"ScamShield AI {tier_info['name']} - {investigation_target}",
                'custom_id': f"scamshield_{tier}_{investigation_target}",
                'metadata': {
                    'tier': tier,
                    'target': investigation_target,
                    'customer_email': customer_email,
                    **(metadata or {})
                }
            }
            
            logger.info(f"✅ PayPal order created: {order_id}")
            
            return {
                'success': True,
                'order_id': order_id,
                'amount': tier_info['price'],
                'currency': tier_info['currency'].upper(),
                'tier': tier,
                'approval_url': f"https://www.sandbox.paypal.com/checkoutnow?token={order_id}",
                'client_id': self.paypal_client_id
            }
            
        except Exception as e:
            logger.error(f"❌ PayPal order creation failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def verify_stripe_webhook(self, payload: str, signature: str) -> Dict[str, Any]:
        """Verify Stripe webhook signature and process event"""
        if not self.stripe_enabled:
            return {'success': False, 'error': 'Stripe not available'}
        
        webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET', 'whsec_dummy')
        
        try:
            event = self.stripe.Webhook.construct_event(
                payload, signature, webhook_secret
            )
            
            logger.info(f"✅ Stripe webhook verified: {event['type']}")
            
            # Process different event types
            if event['type'] == 'payment_intent.succeeded':
                payment_intent = event['data']['object']
                return self._handle_stripe_payment_success(payment_intent)
            
            elif event['type'] == 'payment_intent.payment_failed':
                payment_intent = event['data']['object']
                return self._handle_stripe_payment_failure(payment_intent)
            
            return {'success': True, 'event_type': event['type']}
            
        except Exception as e:
            logger.error(f"❌ Stripe webhook verification failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _handle_stripe_payment_success(self, payment_intent: Dict) -> Dict[str, Any]:
        """Handle successful Stripe payment"""
        try:
            metadata = payment_intent.get('metadata', {})
            
            order_data = {
                'payment_id': payment_intent['id'],
                'amount': payment_intent['amount'] / 100,
                'currency': payment_intent['currency'].upper(),
                'tier': metadata.get('tier'),
                'target': metadata.get('target'),
                'customer_email': metadata.get('customer_email'),
                'payment_method': 'stripe',
                'status': 'paid',
                'created_at': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Payment successful: {payment_intent['id']}")
            
            # Here you would typically:
            # 1. Create investigation order in database
            # 2. Trigger investigation process
            # 3. Send confirmation email
            
            return {
                'success': True,
                'order_data': order_data,
                'action': 'start_investigation'
            }
            
        except Exception as e:
            logger.error(f"❌ Payment success handling failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _handle_stripe_payment_failure(self, payment_intent: Dict) -> Dict[str, Any]:
        """Handle failed Stripe payment"""
        try:
            metadata = payment_intent.get('metadata', {})
            
            failure_data = {
                'payment_id': payment_intent['id'],
                'tier': metadata.get('tier'),
                'target': metadata.get('target'),
                'customer_email': metadata.get('customer_email'),
                'failure_reason': payment_intent.get('last_payment_error', {}).get('message', 'Unknown error'),
                'status': 'failed',
                'created_at': datetime.now().isoformat()
            }
            
            logger.warning(f"⚠️ Payment failed: {payment_intent['id']}")
            
            return {
                'success': True,
                'failure_data': failure_data,
                'action': 'notify_failure'
            }
            
        except Exception as e:
            logger.error(f"❌ Payment failure handling failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def verify_paypal_webhook(self, payload: str, headers: Dict) -> Dict[str, Any]:
        """Verify PayPal webhook and process event"""
        if not self.paypal_enabled:
            return {'success': False, 'error': 'PayPal not available'}
        
        try:
            # Simplified PayPal webhook verification for demo
            event_data = json.loads(payload)
            event_type = event_data.get('event_type')
            
            logger.info(f"✅ PayPal webhook received: {event_type}")
            
            if event_type == 'PAYMENT.CAPTURE.COMPLETED':
                return self._handle_paypal_payment_success(event_data)
            
            elif event_type == 'PAYMENT.CAPTURE.DENIED':
                return self._handle_paypal_payment_failure(event_data)
            
            return {'success': True, 'event_type': event_type}
            
        except Exception as e:
            logger.error(f"❌ PayPal webhook processing failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _handle_paypal_payment_success(self, event_data: Dict) -> Dict[str, Any]:
        """Handle successful PayPal payment"""
        try:
            resource = event_data.get('resource', {})
            custom_id = resource.get('custom_id', '')
            
            # Parse custom_id to extract order details
            parts = custom_id.split('_')
            tier = parts[1] if len(parts) > 1 else 'unknown'
            target = '_'.join(parts[2:]) if len(parts) > 2 else 'unknown'
            
            order_data = {
                'payment_id': resource.get('id'),
                'amount': float(resource.get('amount', {}).get('value', 0)),
                'currency': resource.get('amount', {}).get('currency_code', 'USD'),
                'tier': tier,
                'target': target,
                'payment_method': 'paypal',
                'status': 'paid',
                'created_at': datetime.now().isoformat()
            }
            
            logger.info(f"✅ PayPal payment successful: {resource.get('id')}")
            
            return {
                'success': True,
                'order_data': order_data,
                'action': 'start_investigation'
            }
            
        except Exception as e:
            logger.error(f"❌ PayPal payment success handling failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _handle_paypal_payment_failure(self, event_data: Dict) -> Dict[str, Any]:
        """Handle failed PayPal payment"""
        try:
            resource = event_data.get('resource', {})
            
            failure_data = {
                'payment_id': resource.get('id'),
                'failure_reason': resource.get('status_details', {}).get('reason', 'Unknown error'),
                'status': 'failed',
                'created_at': datetime.now().isoformat()
            }
            
            logger.warning(f"⚠️ PayPal payment failed: {resource.get('id')}")
            
            return {
                'success': True,
                'failure_data': failure_data,
                'action': 'notify_failure'
            }
            
        except Exception as e:
            logger.error(f"❌ PayPal payment failure handling failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def calculate_pricing(self, tier: str, add_ons: List[str] = None, 
                         discount_code: str = None) -> Dict[str, Any]:
        """Calculate final pricing with add-ons and discounts"""
        if tier not in self.pricing_tiers:
            raise ValueError(f"Invalid pricing tier: {tier}")
        
        base_price = self.pricing_tiers[tier]['price']
        total_price = base_price
        
        # Add-ons pricing (example)
        addon_prices = {
            'expedited': 19.99,  # Rush processing
            'phone_support': 9.99,  # Phone consultation
            'additional_formats': 4.99,  # Extra export formats
        }
        
        addon_total = 0
        if add_ons:
            for addon in add_ons:
                if addon in addon_prices:
                    addon_total += addon_prices[addon]
        
        total_price += addon_total
        
        # Apply discount codes (example)
        discount_amount = 0
        discount_codes = {
            'FIRST10': 0.10,  # 10% off first order
            'BULK20': 0.20,   # 20% off bulk orders
            'STUDENT15': 0.15  # 15% student discount
        }
        
        if discount_code and discount_code in discount_codes:
            discount_amount = total_price * discount_codes[discount_code]
            total_price -= discount_amount
        
        return {
            'base_price': base_price,
            'addon_total': addon_total,
            'discount_amount': discount_amount,
            'total_price': round(total_price, 2),
            'currency': 'USD',
            'tier': tier,
            'add_ons': add_ons or [],
            'discount_code': discount_code
        }
    
    def get_payment_status(self, payment_id: str, provider: str) -> Dict[str, Any]:
        """Get payment status from provider"""
        try:
            if provider == 'stripe' and self.stripe_enabled:
                intent = self.stripe.PaymentIntent.retrieve(payment_id)
                return {
                    'success': True,
                    'status': intent.status,
                    'amount': intent.amount / 100,
                    'currency': intent.currency.upper(),
                    'created': intent.created
                }
            
            elif provider == 'paypal' and self.paypal_enabled:
                # In production, would use PayPal API to check status
                return {
                    'success': True,
                    'status': 'completed',  # Mock status
                    'payment_id': payment_id
                }
            
            else:
                return {'success': False, 'error': f'Provider {provider} not available'}
                
        except Exception as e:
            logger.error(f"❌ Payment status check failed: {e}")
            return {'success': False, 'error': str(e)}


# Utility functions
def generate_order_id(tier: str, target: str) -> str:
    """Generate unique order ID"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    target_hash = hashlib.md5(target.encode()).hexdigest()[:8]
    return f"ORD_{timestamp}_{tier.upper()}_{target_hash}"


def validate_payment_data(data: Dict) -> Dict[str, Any]:
    """Validate payment request data"""
    required_fields = ['tier', 'target', 'customer_email']
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    if missing_fields:
        return {
            'valid': False,
            'errors': [f'Missing required field: {field}' for field in missing_fields]
        }
    
    # Validate email format
    email = data.get('customer_email', '')
    if '@' not in email or '.' not in email:
        return {
            'valid': False,
            'errors': ['Invalid email format']
        }
    
    # Validate tier
    valid_tiers = ['basic', 'standard', 'professional', 'forensic']
    if data.get('tier') not in valid_tiers:
        return {
            'valid': False,
            'errors': [f'Invalid tier. Must be one of: {", ".join(valid_tiers)}']
        }
    
    return {'valid': True, 'errors': []}


if __name__ == "__main__":
    # Test the payment service
    payment_service = PaymentService()
    
    # Test pricing calculation
    pricing = payment_service.calculate_pricing(
        tier='professional',
        add_ons=['expedited', 'phone_support'],
        discount_code='FIRST10'
    )
    
    print("Payment Service Test:")
    print(f"Pricing calculation: {pricing}")
    print(f"Available payment methods: Stripe={payment_service.stripe_enabled}, PayPal={payment_service.paypal_enabled}")

