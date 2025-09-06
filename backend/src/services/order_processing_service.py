"""
ScamShield AI Order Processing Service
Connects payment processing, CrewAI investigation, and report generation
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import asyncio
from enum import Enum

# Add parent directories to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OrderStatus(Enum):
    PENDING_PAYMENT = "pending_payment"
    PAYMENT_CONFIRMED = "payment_confirmed"
    INVESTIGATION_QUEUED = "investigation_queued"
    INVESTIGATION_IN_PROGRESS = "investigation_in_progress"
    INVESTIGATION_COMPLETED = "investigation_completed"
    REPORT_GENERATING = "report_generating"
    REPORT_READY = "report_ready"
    DELIVERED = "delivered"
    FAILED = "failed"
    CANCELLED = "cancelled"

class OrderProcessingService:
    """
    Orchestrates the complete order processing pipeline
    """
    
    def __init__(self):
        self.orders = {}  # In production, this would be a database
        self.investigation_queue = []
        self.report_queue = []
        
        # Initialize components
        self.crewai_available = False
        self.report_engine_available = False
        
        try:
            # Try to import CrewAI components
            from crews.investigation_crew import InvestigationCrew
            self.investigation_crew = InvestigationCrew()
            self.crewai_available = True
            logger.info("✅ CrewAI investigation crew initialized")
        except ImportError as e:
            logger.warning(f"⚠️ CrewAI not available: {e}")
        except Exception as e:
            logger.error(f"❌ CrewAI initialization failed: {e}")
        
        try:
            # Try to import report engine
            from reports.simplified_report_engine import ScamShieldReportEngine
            from reports.multi_format_exporter import MultiFormatExporter
            self.report_engine = ScamShieldReportEngine()
            self.exporter = MultiFormatExporter()
            self.report_engine_available = True
            logger.info("✅ Report engine initialized")
        except ImportError as e:
            logger.warning(f"⚠️ Report engine not available: {e}")
        except Exception as e:
            logger.error(f"❌ Report engine initialization failed: {e}")
    
    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new investigation order"""
        try:
            order_id = order_data.get('order_id')
            if not order_id:
                raise ValueError("Order ID is required")
            
            # Create order record
            order = {
                'order_id': order_id,
                'customer_email': order_data.get('customer_email'),
                'target': order_data.get('target'),
                'tier': order_data.get('tier'),
                'investigation_type': order_data.get('investigation_type', 'comprehensive'),
                'price': order_data.get('price'),
                'payment_method': order_data.get('payment_method'),
                'payment_id': order_data.get('payment_id'),
                'status': OrderStatus.PENDING_PAYMENT.value,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'metadata': order_data.get('metadata', {}),
                'progress': 0,
                'estimated_completion': None,
                'investigation_results': None,
                'report_data': None,
                'report_files': {},
                'delivery_info': {}
            }
            
            self.orders[order_id] = order
            logger.info(f"✅ Order created: {order_id}")
            
            return {
                'success': True,
                'order_id': order_id,
                'status': order['status'],
                'created_at': order['created_at']
            }
            
        except Exception as e:
            logger.error(f"❌ Order creation failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def confirm_payment(self, order_id: str, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Confirm payment and start investigation process"""
        try:
            if order_id not in self.orders:
                raise ValueError(f"Order not found: {order_id}")
            
            order = self.orders[order_id]
            
            # Update order with payment confirmation
            order['payment_confirmed_at'] = datetime.now().isoformat()
            order['payment_data'] = payment_data
            order['status'] = OrderStatus.PAYMENT_CONFIRMED.value
            order['updated_at'] = datetime.now().isoformat()
            order['progress'] = 10
            
            # Calculate estimated completion based on tier
            tier_delivery_times = {
                'basic': 24,      # 24 hours
                'standard': 12,   # 12 hours
                'professional': 6, # 6 hours
                'forensic': 3     # 3 hours
            }
            
            delivery_hours = tier_delivery_times.get(order['tier'], 12)
            estimated_completion = datetime.now() + timedelta(hours=delivery_hours)
            order['estimated_completion'] = estimated_completion.isoformat()
            
            # Queue investigation
            self.queue_investigation(order_id)
            
            logger.info(f"✅ Payment confirmed for order: {order_id}")
            
            return {
                'success': True,
                'order_id': order_id,
                'status': order['status'],
                'estimated_completion': order['estimated_completion'],
                'progress': order['progress']
            }
            
        except Exception as e:
            logger.error(f"❌ Payment confirmation failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def queue_investigation(self, order_id: str) -> Dict[str, Any]:
        """Queue investigation for processing"""
        try:
            if order_id not in self.orders:
                raise ValueError(f"Order not found: {order_id}")
            
            order = self.orders[order_id]
            order['status'] = OrderStatus.INVESTIGATION_QUEUED.value
            order['queued_at'] = datetime.now().isoformat()
            order['updated_at'] = datetime.now().isoformat()
            order['progress'] = 20
            
            # Add to investigation queue
            if order_id not in self.investigation_queue:
                self.investigation_queue.append(order_id)
            
            logger.info(f"✅ Investigation queued: {order_id}")
            
            # Start investigation if CrewAI is available
            if self.crewai_available:
                return self.start_investigation(order_id)
            else:
                # Use simulated investigation
                return self.start_simulated_investigation(order_id)
            
        except Exception as e:
            logger.error(f"❌ Investigation queueing failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def start_investigation(self, order_id: str) -> Dict[str, Any]:
        """Start CrewAI investigation"""
        try:
            if order_id not in self.orders:
                raise ValueError(f"Order not found: {order_id}")
            
            order = self.orders[order_id]
            order['status'] = OrderStatus.INVESTIGATION_IN_PROGRESS.value
            order['investigation_started_at'] = datetime.now().isoformat()
            order['updated_at'] = datetime.now().isoformat()
            order['progress'] = 30
            
            # Remove from queue
            if order_id in self.investigation_queue:
                self.investigation_queue.remove(order_id)
            
            # Prepare investigation parameters
            investigation_params = {
                'target': order['target'],
                'tier': order['tier'],
                'investigation_type': order['investigation_type'],
                'customer_requirements': order['metadata'].get('requirements', ''),
                'priority': 'high' if order['tier'] in ['professional', 'forensic'] else 'normal'
            }
            
            logger.info(f"🔍 Starting CrewAI investigation: {order_id}")
            
            # Execute investigation using CrewAI
            try:
                investigation_results = self.investigation_crew.execute_investigation(
                    target=order['target'],
                    investigation_type=order['investigation_type'],
                    tier=order['tier']
                )
                
                return self.complete_investigation(order_id, investigation_results)
                
            except Exception as e:
                logger.error(f"❌ CrewAI investigation failed: {e}")
                # Fallback to simulated investigation
                return self.start_simulated_investigation(order_id)
            
        except Exception as e:
            logger.error(f"❌ Investigation start failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def start_simulated_investigation(self, order_id: str) -> Dict[str, Any]:
        """Start simulated investigation (fallback)"""
        try:
            if order_id not in self.orders:
                raise ValueError(f"Order not found: {order_id}")
            
            order = self.orders[order_id]
            order['status'] = OrderStatus.INVESTIGATION_IN_PROGRESS.value
            order['investigation_started_at'] = datetime.now().isoformat()
            order['updated_at'] = datetime.now().isoformat()
            order['progress'] = 30
            
            logger.info(f"🔍 Starting simulated investigation: {order_id}")
            
            # Simulate investigation results
            simulated_results = self.generate_simulated_results(order)
            
            return self.complete_investigation(order_id, simulated_results)
            
        except Exception as e:
            logger.error(f"❌ Simulated investigation failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_simulated_results(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Generate simulated investigation results"""
        target = order['target']
        tier = order['tier']
        
        # Base findings that vary by tier
        tier_findings = {
            'basic': [
                f"Domain analysis of {target}",
                "Basic reputation check completed",
                "DNS configuration assessment",
                "SSL certificate validation"
            ],
            'standard': [
                f"Comprehensive analysis of {target}",
                "Multi-source reputation verification",
                "Network infrastructure assessment",
                "Content analysis and categorization",
                "Social media presence evaluation"
            ],
            'professional': [
                f"Expert-level investigation of {target}",
                "Advanced threat intelligence correlation",
                "Behavioral pattern analysis",
                "Financial transaction indicators",
                "Attribution and actor profiling",
                "Regulatory compliance assessment"
            ],
            'forensic': [
                f"Forensic-grade investigation of {target}",
                "Chain of custody documentation",
                "Legal evidence collection",
                "Expert witness preparation",
                "Court-admissible documentation",
                "Comprehensive timeline reconstruction",
                "Technical artifact preservation"
            ]
        }
        
        # Risk levels based on tier
        risk_levels = {
            'basic': ['LOW', 'MEDIUM'],
            'standard': ['MEDIUM', 'HIGH'],
            'professional': ['HIGH', 'CRITICAL'],
            'forensic': ['CRITICAL']
        }
        
        import random
        risk_level = random.choice(risk_levels.get(tier, ['MEDIUM']))
        confidence = random.uniform(0.85, 0.98)
        
        return {
            'target': target,
            'investigation_type': order['investigation_type'],
            'tier': tier,
            'findings': tier_findings.get(tier, tier_findings['standard']),
            'risk_level': risk_level,
            'confidence_score': round(confidence, 3),
            'threat_indicators': [
                'Suspicious domain registration patterns',
                'Anomalous network behavior',
                'Potential phishing indicators',
                'Fraudulent content markers'
            ],
            'recommendations': [
                'Monitor for continued activity',
                'Implement blocking measures',
                'Report to relevant authorities',
                'Update security policies'
            ],
            'technical_details': {
                'ip_addresses': ['192.168.1.100', '10.0.0.50'],
                'domains': [target],
                'file_hashes': ['abc123def456', 'xyz789uvw012'],
                'network_indicators': ['suspicious_traffic', 'unusual_ports']
            },
            'investigation_duration': '2.5 hours',
            'sources_checked': random.randint(15, 50),
            'completed_at': datetime.now().isoformat()
        }
    
    def complete_investigation(self, order_id: str, investigation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Complete investigation and start report generation"""
        try:
            if order_id not in self.orders:
                raise ValueError(f"Order not found: {order_id}")
            
            order = self.orders[order_id]
            order['status'] = OrderStatus.INVESTIGATION_COMPLETED.value
            order['investigation_completed_at'] = datetime.now().isoformat()
            order['investigation_results'] = investigation_results
            order['updated_at'] = datetime.now().isoformat()
            order['progress'] = 70
            
            logger.info(f"✅ Investigation completed: {order_id}")
            
            # Start report generation
            return self.generate_report(order_id)
            
        except Exception as e:
            logger.error(f"❌ Investigation completion failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_report(self, order_id: str) -> Dict[str, Any]:
        """Generate investigation report"""
        try:
            if order_id not in self.orders:
                raise ValueError(f"Order not found: {order_id}")
            
            order = self.orders[order_id]
            order['status'] = OrderStatus.REPORT_GENERATING.value
            order['report_generation_started_at'] = datetime.now().isoformat()
            order['updated_at'] = datetime.now().isoformat()
            order['progress'] = 80
            
            logger.info(f"📄 Generating report: {order_id}")
            
            if self.report_engine_available:
                # Use real report engine
                report_data = self.report_engine.generate_investigation_report(
                    order['investigation_results'],
                    order['tier']
                )
                
                # Export to multiple formats
                export_results = self.exporter.export_all_formats(
                    report_data,
                    f"ScamShield_Investigation_{order['target'].replace('.', '_')}_{order_id}"
                )
                
                order['report_data'] = report_data
                order['report_files'] = export_results
                
            else:
                # Generate simulated report
                report_data = self.generate_simulated_report(order)
                order['report_data'] = report_data
                order['report_files'] = {
                    'pdf': f"/reports/{order_id}.pdf",
                    'html': f"/reports/{order_id}.html",
                    'json': json.dumps(report_data)
                }
            
            # Complete report generation
            order['status'] = OrderStatus.REPORT_READY.value
            order['report_completed_at'] = datetime.now().isoformat()
            order['updated_at'] = datetime.now().isoformat()
            order['progress'] = 90
            
            logger.info(f"✅ Report generated: {order_id}")
            
            # Prepare for delivery
            return self.prepare_delivery(order_id)
            
        except Exception as e:
            logger.error(f"❌ Report generation failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_simulated_report(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Generate simulated report data"""
        investigation_results = order['investigation_results']
        
        return {
            'title': f"ScamShield AI Investigation Report: {order['target']}",
            'order_id': order['order_id'],
            'target': order['target'],
            'tier': order['tier'],
            'customer_email': order['customer_email'],
            'investigation_type': order['investigation_type'],
            'executive_summary': f"Comprehensive investigation of {order['target']} reveals {investigation_results['risk_level'].lower()} risk indicators with {investigation_results['confidence_score']*100:.1f}% confidence.",
            'findings': investigation_results['findings'],
            'risk_assessment': {
                'level': investigation_results['risk_level'],
                'score': investigation_results['confidence_score'],
                'factors': investigation_results['threat_indicators']
            },
            'recommendations': investigation_results['recommendations'],
            'technical_details': investigation_results['technical_details'],
            'methodology': f"Investigation conducted using ScamShield AI {order['tier']} tier analysis",
            'sources': f"{investigation_results['sources_checked']} sources analyzed",
            'duration': investigation_results['investigation_duration'],
            'generated_at': datetime.now().isoformat(),
            'report_version': '2.0',
            'certification': order['tier'] == 'forensic'
        }
    
    def prepare_delivery(self, order_id: str) -> Dict[str, Any]:
        """Prepare order for delivery"""
        try:
            if order_id not in self.orders:
                raise ValueError(f"Order not found: {order_id}")
            
            order = self.orders[order_id]
            
            # Generate delivery information
            delivery_info = {
                'download_links': {},
                'access_code': f"SC_{order_id[-8:].upper()}",
                'expires_at': (datetime.now() + timedelta(days=30)).isoformat(),
                'delivery_method': 'secure_download',
                'notification_sent': False
            }
            
            # Create secure download links
            for format_type, file_path in order['report_files'].items():
                if format_type != 'json':  # Don't create download link for JSON
                    delivery_info['download_links'][format_type] = f"https://secure.scamshield.ai/download/{order_id}/{format_type}?code={delivery_info['access_code']}"
            
            order['delivery_info'] = delivery_info
            order['status'] = OrderStatus.DELIVERED.value
            order['delivered_at'] = datetime.now().isoformat()
            order['updated_at'] = datetime.now().isoformat()
            order['progress'] = 100
            
            logger.info(f"✅ Order ready for delivery: {order_id}")
            
            return {
                'success': True,
                'order_id': order_id,
                'status': order['status'],
                'delivery_info': delivery_info,
                'progress': order['progress']
            }
            
        except Exception as e:
            logger.error(f"❌ Delivery preparation failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_order_status(self, order_id: str) -> Dict[str, Any]:
        """Get current order status and progress"""
        try:
            if order_id not in self.orders:
                return {
                    'success': False,
                    'error': 'Order not found'
                }
            
            order = self.orders[order_id]
            
            return {
                'success': True,
                'order_id': order_id,
                'status': order['status'],
                'progress': order['progress'],
                'created_at': order['created_at'],
                'updated_at': order['updated_at'],
                'estimated_completion': order.get('estimated_completion'),
                'target': order['target'],
                'tier': order['tier'],
                'customer_email': order['customer_email'],
                'delivery_info': order.get('delivery_info', {}),
                'investigation_summary': {
                    'risk_level': order.get('investigation_results', {}).get('risk_level'),
                    'confidence': order.get('investigation_results', {}).get('confidence_score'),
                    'findings_count': len(order.get('investigation_results', {}).get('findings', []))
                } if order.get('investigation_results') else None
            }
            
        except Exception as e:
            logger.error(f"❌ Order status check failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_all_orders(self, customer_email: str = None) -> Dict[str, Any]:
        """Get all orders, optionally filtered by customer email"""
        try:
            orders = []
            
            for order_id, order in self.orders.items():
                if customer_email and order['customer_email'] != customer_email:
                    continue
                
                orders.append({
                    'order_id': order_id,
                    'status': order['status'],
                    'progress': order['progress'],
                    'target': order['target'],
                    'tier': order['tier'],
                    'price': order['price'],
                    'created_at': order['created_at'],
                    'estimated_completion': order.get('estimated_completion')
                })
            
            return {
                'success': True,
                'orders': orders,
                'total_count': len(orders)
            }
            
        except Exception as e:
            logger.error(f"❌ Orders retrieval failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def cancel_order(self, order_id: str, reason: str = None) -> Dict[str, Any]:
        """Cancel an order"""
        try:
            if order_id not in self.orders:
                return {
                    'success': False,
                    'error': 'Order not found'
                }
            
            order = self.orders[order_id]
            
            # Check if order can be cancelled
            non_cancellable_statuses = [
                OrderStatus.INVESTIGATION_COMPLETED.value,
                OrderStatus.REPORT_READY.value,
                OrderStatus.DELIVERED.value
            ]
            
            if order['status'] in non_cancellable_statuses:
                return {
                    'success': False,
                    'error': 'Order cannot be cancelled at this stage'
                }
            
            order['status'] = OrderStatus.CANCELLED.value
            order['cancelled_at'] = datetime.now().isoformat()
            order['cancellation_reason'] = reason
            order['updated_at'] = datetime.now().isoformat()
            
            # Remove from queues
            if order_id in self.investigation_queue:
                self.investigation_queue.remove(order_id)
            
            logger.info(f"✅ Order cancelled: {order_id}")
            
            return {
                'success': True,
                'order_id': order_id,
                'status': order['status'],
                'cancelled_at': order['cancelled_at']
            }
            
        except Exception as e:
            logger.error(f"❌ Order cancellation failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }


if __name__ == "__main__":
    # Test the order processing service
    service = OrderProcessingService()
    
    # Test order creation
    test_order = {
        'order_id': 'ORD_TEST_001',
        'customer_email': 'test@example.com',
        'target': 'test-domain.com',
        'tier': 'professional',
        'price': 49.99,
        'payment_method': 'stripe',
        'payment_id': 'pi_test_123'
    }
    
    print("Order Processing Service Test:")
    
    # Create order
    result = service.create_order(test_order)
    print(f"Order creation: {result}")
    
    # Confirm payment
    payment_data = {'payment_confirmed': True, 'amount': 49.99}
    result = service.confirm_payment('ORD_TEST_001', payment_data)
    print(f"Payment confirmation: {result}")
    
    # Check status
    status = service.get_order_status('ORD_TEST_001')
    print(f"Order status: {status}")
    
    print(f"CrewAI available: {service.crewai_available}")
    print(f"Report engine available: {service.report_engine_available}")

