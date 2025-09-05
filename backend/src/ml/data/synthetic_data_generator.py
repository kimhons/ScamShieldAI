"""
ScamShield AI - Synthetic Data Generation System
Generates realistic fraud and legitimate investigation data for ML training.
"""

import random
import string
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import numpy as np
from faker import Faker
import tldextract

class SyntheticFraudDataGenerator:
    """
    Generate synthetic training data using rule-based patterns
    and domain expertise until real labeled data is available.
    """
    
    def __init__(self, seed: int = 42):
        random.seed(seed)
        np.random.seed(seed)
        self.fake = Faker()
        Faker.seed(seed)
        
        # Load fraud patterns and legitimate patterns
        self._load_fraud_patterns()
        self._load_legitimate_patterns()
    
    def _load_fraud_patterns(self):
        """Load known fraud patterns for synthetic generation"""
        self.fraud_patterns = {
            'domains': {
                'typosquatting': [
                    'payp4l', 'g00gle', 'micr0soft', 'amaz0n', 'appl3',
                    'fac3book', 'tw1tter', 'inst4gram', 'link3din'
                ],
                'suspicious_tlds': ['.tk', '.ml', '.ga', '.cf', '.top', '.click', '.download'],
                'suspicious_keywords': [
                    'verify', 'secure', 'update', 'suspended', 'urgent',
                    'bank', 'paypal', 'amazon', 'microsoft', 'apple'
                ],
                'dga_patterns': [
                    'qwerty123', 'random456', 'temp789', 'test123',
                    'abcdef', 'xyz789', 'temp-site', 'quick-fix'
                ]
            },
            'emails': {
                'suspicious_senders': [
                    'noreply@suspicious-domain.tk',
                    'security@fake-bank.ml',
                    'support@phishing-site.ga'
                ],
                'phishing_subjects': [
                    'URGENT: Verify Your Account',
                    'Your Account Has Been Suspended',
                    'Immediate Action Required',
                    'Security Alert: Unusual Activity',
                    'Congratulations! You\'ve Won!'
                ],
                'suspicious_content': [
                    'click here immediately',
                    'verify your account now',
                    'suspended due to suspicious activity',
                    'update your information',
                    'limited time offer'
                ]
            },
            'financial': {
                'suspicious_amounts': [9999, 9500, 9800, 4999, 2999],  # Just under thresholds
                'high_risk_countries': ['AF', 'IR', 'KP', 'SY', 'MM'],
                'suspicious_merchants': [
                    'QUICK CASH LLC', 'TEMP SERVICES', 'CRYPTO EXCHANGE',
                    'MONEY TRANSFER', 'GIFT CARD STORE'
                ],
                'suspicious_patterns': [
                    'multiple_small_transactions',
                    'round_amounts',
                    'unusual_times',
                    'new_payees'
                ]
            }
        }
    
    def _load_legitimate_patterns(self):
        """Load legitimate patterns for synthetic generation"""
        self.legitimate_patterns = {
            'domains': {
                'reputable_tlds': ['.com', '.net', '.org', '.edu', '.gov'],
                'legitimate_registrars': [
                    'GoDaddy', 'Namecheap', 'Cloudflare', 'Google Domains',
                    'Amazon Registrar', 'Microsoft'
                ],
                'business_keywords': [
                    'corp', 'inc', 'llc', 'company', 'services',
                    'solutions', 'consulting', 'tech', 'digital'
                ]
            },
            'emails': {
                'legitimate_senders': [
                    'noreply@company.com',
                    'support@business.net',
                    'info@organization.org'
                ],
                'normal_subjects': [
                    'Monthly Newsletter',
                    'Order Confirmation',
                    'Welcome to Our Service',
                    'Meeting Reminder',
                    'Invoice #12345'
                ],
                'normal_content': [
                    'thank you for your business',
                    'your order has been processed',
                    'welcome to our community',
                    'please find attached',
                    'best regards'
                ]
            },
            'financial': {
                'normal_amounts': [25.99, 49.99, 99.99, 199.99, 299.99],
                'low_risk_countries': ['US', 'CA', 'GB', 'DE', 'FR', 'AU'],
                'legitimate_merchants': [
                    'AMAZON.COM', 'WALMART', 'TARGET', 'STARBUCKS',
                    'MCDONALDS', 'SHELL', 'EXXON'
                ]
            }
        }
    
    def generate_domain_fraud_data(self, num_samples: int = 1000) -> Tuple[List[Dict], List[int]]:
        """Generate synthetic domain fraud training data"""
        data = []
        labels = []
        
        # Generate legitimate domains (50%)
        for _ in range(num_samples // 2):
            domain_data = self._generate_legitimate_domain_data()
            data.append(domain_data)
            labels.append(0)  # Legitimate
        
        # Generate fraudulent domains (50%)
        for _ in range(num_samples // 2):
            domain_data = self._generate_fraudulent_domain_data()
            data.append(domain_data)
            labels.append(1)  # Fraudulent
        
        return data, labels
    
    def _generate_legitimate_domain_data(self) -> Dict[str, Any]:
        """Generate realistic legitimate domain data"""
        # Generate legitimate domain name
        business_word = random.choice(self.legitimate_patterns['domains']['business_keywords'])
        company_name = self.fake.company().lower().replace(' ', '').replace(',', '').replace('.', '')[:10]
        tld = random.choice(self.legitimate_patterns['domains']['reputable_tlds'])
        domain = f"{company_name}-{business_word}{tld}"
        
        # Generate legitimate WHOIS data
        creation_date = self.fake.date_between(start_date='-5y', end_date='-1y')
        whois_data = {
            'domain': domain,
            'creation_date': creation_date.isoformat(),
            'updated_date': self.fake.date_between(start_date=creation_date, end_date='today').isoformat(),
            'expiry_date': self.fake.date_between(start_date='today', end_date='+2y').isoformat(),
            'registrar': random.choice(self.legitimate_patterns['domains']['legitimate_registrars']),
            'registrant': self.fake.company(),
            'privacy_protected': random.choice([True, False])
        }
        
        # Generate legitimate SSL data
        ssl_analysis = {
            'valid': True,
            'issuer': random.choice(['Let\'s Encrypt', 'DigiCert', 'Cloudflare']),
            'expiry_date': self.fake.date_between(start_date='today', end_date='+1y').isoformat(),
            'certificate_age_days': random.randint(30, 365)
        }
        
        # Generate legitimate DNS data
        dns_analysis = {
            'records': [
                {'type': 'A', 'value': self.fake.ipv4()},
                {'type': 'MX', 'value': f"mail.{domain}"},
                {'type': 'NS', 'value': f"ns1.{domain}"},
                {'type': 'NS', 'value': f"ns2.{domain}"}
            ],
            'mx_count': 1,
            'ns_count': 2,
            'total_records': 4
        }
        
        return {
            'domain': domain,
            'whois_data': whois_data,
            'ssl_analysis': ssl_analysis,
            'dns_analysis': dns_analysis,
            'reputation_data': {
                'alexa_rank': random.randint(10000, 1000000),
                'google_safe_browsing': 'safe',
                'virustotal_detections': 0
            }
        }
    
    def _generate_fraudulent_domain_data(self) -> Dict[str, Any]:
        """Generate realistic fraudulent domain data"""
        fraud_type = random.choice(['typosquatting', 'suspicious_tld', 'dga', 'keyword_stuffing'])
        
        if fraud_type == 'typosquatting':
            domain_base = random.choice(self.fraud_patterns['domains']['typosquatting'])
            tld = random.choice(self.fraud_patterns['domains']['suspicious_tlds'])
            domain = f"{domain_base}{tld}"
        elif fraud_type == 'suspicious_tld':
            legitimate_name = self.fake.company().lower().replace(' ', '')[:8]
            tld = random.choice(self.fraud_patterns['domains']['suspicious_tlds'])
            domain = f"{legitimate_name}{tld}"
        elif fraud_type == 'dga':
            domain_base = random.choice(self.fraud_patterns['domains']['dga_patterns'])
            domain = f"{domain_base}-{random.randint(100, 999)}.com"
        else:  # keyword_stuffing
            keywords = random.sample(self.fraud_patterns['domains']['suspicious_keywords'], 2)
            domain = f"{keywords[0]}-{keywords[1]}.com"
        
        # Generate suspicious WHOIS data
        creation_date = self.fake.date_between(start_date='-30d', end_date='today')  # Very recent
        whois_data = {
            'domain': domain,
            'creation_date': creation_date.isoformat(),
            'updated_date': creation_date.isoformat(),  # Same as creation (suspicious)
            'expiry_date': self.fake.date_between(start_date='today', end_date='+1y').isoformat(),
            'registrar': 'Freenom' if domain.endswith(('.tk', '.ml', '.ga', '.cf')) else 'Unknown Registrar',
            'registrant': 'REDACTED FOR PRIVACY' if random.random() > 0.3 else self.fake.name(),
            'privacy_protected': True
        }
        
        # Generate suspicious SSL data
        ssl_analysis = {
            'valid': random.choice([False, False, True]),  # 66% chance of invalid SSL
            'issuer': 'Self-signed' if random.random() > 0.7 else 'Let\'s Encrypt',
            'expiry_date': None if random.random() > 0.7 else self.fake.date_between(start_date='today', end_date='+90d').isoformat(),
            'certificate_age_days': random.randint(1, 30) if random.random() > 0.3 else 0
        }
        
        # Generate suspicious DNS data
        dns_analysis = {
            'records': [
                {'type': 'A', 'value': self.fake.ipv4()}
            ],
            'mx_count': 0,  # No email setup (suspicious)
            'ns_count': random.randint(0, 1),  # Minimal DNS setup
            'total_records': random.randint(1, 2)
        }
        
        return {
            'domain': domain,
            'whois_data': whois_data,
            'ssl_analysis': ssl_analysis,
            'dns_analysis': dns_analysis,
            'reputation_data': {
                'alexa_rank': random.randint(5000000, 10000000),  # Very low ranking
                'google_safe_browsing': random.choice(['unsafe', 'malware', 'phishing']) if random.random() > 0.5 else 'safe',
                'virustotal_detections': random.randint(0, 15) if random.random() > 0.6 else 0
            }
        }
    
    def generate_email_fraud_data(self, num_samples: int = 1000) -> Tuple[List[Dict], List[int]]:
        """Generate synthetic email fraud training data"""
        data = []
        labels = []
        
        # Generate legitimate emails (50%)
        for _ in range(num_samples // 2):
            email_data = self._generate_legitimate_email_data()
            data.append(email_data)
            labels.append(0)  # Legitimate
        
        # Generate fraudulent emails (50%)
        for _ in range(num_samples // 2):
            email_data = self._generate_fraudulent_email_data()
            data.append(email_data)
            labels.append(1)  # Fraudulent
        
        return data, labels
    
    def _generate_legitimate_email_data(self) -> Dict[str, Any]:
        """Generate realistic legitimate email data"""
        sender_domain = f"{self.fake.company().lower().replace(' ', '').replace(',', '')[:10]}.com"
        sender = f"noreply@{sender_domain}"
        
        headers = {
            'from': sender,
            'to': self.fake.email(),
            'subject': random.choice(self.legitimate_patterns['emails']['normal_subjects']),
            'date': self.fake.date_time_between(start_date='-30d', end_date='now').isoformat(),
            'message-id': f"<{self.fake.uuid4()}@{sender_domain}>",
            'received-spf': 'pass',
            'dkim-signature': f"v=1; a=rsa-sha256; d={sender_domain}; s=default",
            'return-path': sender,
            'reply-to': sender
        }
        
        content = {
            'text': f"Dear Customer,\n\n{random.choice(self.legitimate_patterns['emails']['normal_content'])}.\n\nBest regards,\nThe Team",
            'html': f"<html><body><p>Dear Customer,</p><p>{random.choice(self.legitimate_patterns['emails']['normal_content'])}.</p><p>Best regards,<br>The Team</p></body></html>"
        }
        
        return {
            'headers': headers,
            'content': content,
            'attachments': []
        }
    
    def _generate_fraudulent_email_data(self) -> Dict[str, Any]:
        """Generate realistic fraudulent email data"""
        fraud_type = random.choice(['phishing', 'spoofing', 'spam', 'malware'])
        
        if fraud_type == 'phishing':
            # Phishing email mimicking legitimate service
            legitimate_service = random.choice(['PayPal', 'Amazon', 'Microsoft', 'Apple'])
            fake_domain = f"{legitimate_service.lower()}-security.tk"
            sender = f"security@{fake_domain}"
            subject = random.choice(self.fraud_patterns['emails']['phishing_subjects'])
            content_text = f"URGENT: {random.choice(self.fraud_patterns['emails']['suspicious_content'])}. Click here: http://{fake_domain}/verify"
        
        elif fraud_type == 'spoofing':
            # Email with mismatched sender/reply-to
            real_domain = "paypal.com"
            fake_domain = "payp4l-security.ml"
            sender = f"service@{real_domain}"
            reply_to = f"noreply@{fake_domain}"
            subject = "Account Verification Required"
            content_text = "Please verify your account by clicking the link below."
        
        elif fraud_type == 'spam':
            # Spam email with suspicious content
            sender = f"winner@{random.choice(['lottery.tk', 'prize.ml', 'winner.ga'])}"
            subject = "CONGRATULATIONS! You've Won $1,000,000!"
            content_text = "You have won our international lottery! Click here to claim your prize!"
        
        else:  # malware
            # Email with suspicious attachment
            sender = f"document@{self.fake.domain_name()}"
            subject = "Important Document - Please Review"
            content_text = "Please find the attached document for your review."
        
        headers = {
            'from': sender,
            'to': self.fake.email(),
            'subject': subject,
            'date': self.fake.date_time_between(start_date='-7d', end_date='now').isoformat(),
            'message-id': f"<{random.randint(100000, 999999)}@{self.fake.domain_name()}>",
            'received-spf': random.choice(['fail', 'softfail', 'neutral']),
            'dkim-signature': '' if random.random() > 0.3 else f"v=1; a=rsa-sha256; d={sender.split('@')[1]}",
            'return-path': reply_to if fraud_type == 'spoofing' else sender,
            'reply-to': reply_to if fraud_type == 'spoofing' else sender
        }
        
        content = {
            'text': content_text,
            'html': f"<html><body><p>{content_text}</p></body></html>"
        }
        
        attachments = []
        if fraud_type == 'malware':
            attachments = [
                {
                    'filename': 'document.exe',
                    'size': random.randint(1000, 10000),
                    'content_type': 'application/octet-stream'
                }
            ]
        
        return {
            'headers': headers,
            'content': content,
            'attachments': attachments
        }
    
    def generate_financial_fraud_data(self, num_samples: int = 1000) -> Tuple[List[Dict], List[int]]:
        """Generate synthetic financial fraud training data"""
        data = []
        labels = []
        
        # Generate legitimate transactions (50%)
        for _ in range(num_samples // 2):
            financial_data = self._generate_legitimate_financial_data()
            data.append(financial_data)
            labels.append(0)  # Legitimate
        
        # Generate fraudulent transactions (50%)
        for _ in range(num_samples // 2):
            financial_data = self._generate_fraudulent_financial_data()
            data.append(financial_data)
            labels.append(1)  # Fraudulent
        
        return data, labels
    
    def _generate_legitimate_financial_data(self) -> Dict[str, Any]:
        """Generate realistic legitimate financial transaction data"""
        transaction = {
            'amount': random.choice(self.legitimate_patterns['financial']['normal_amounts']),
            'currency': 'USD',
            'timestamp': self.fake.date_time_between(start_date='-30d', end_date='now').isoformat(),
            'merchant': {
                'name': random.choice(self.legitimate_patterns['financial']['legitimate_merchants']),
                'category': random.choice(['retail', 'restaurant', 'gas_station', 'grocery'])
            },
            'location': {
                'country': random.choice(self.legitimate_patterns['financial']['low_risk_countries']),
                'city': self.fake.city(),
                'coordinates': [self.fake.longitude(), self.fake.latitude()]
            },
            'payment_method': random.choice(['credit_card', 'debit_card', 'bank_transfer']),
            'payee': random.choice(self.legitimate_patterns['financial']['legitimate_merchants'])
        }
        
        account = {
            'balance': random.uniform(1000, 50000),
            'credit_score': random.randint(650, 850),
            'created_date': self.fake.date_between(start_date='-5y', end_date='-1y').isoformat(),
            'country': transaction['location']['country']
        }
        
        # Generate normal transaction history
        transaction_history = []
        for _ in range(random.randint(10, 50)):
            hist_transaction = {
                'amount': random.choice(self.legitimate_patterns['financial']['normal_amounts']),
                'timestamp': self.fake.date_time_between(start_date='-90d', end_date='-1d').isoformat(),
                'merchant': random.choice(self.legitimate_patterns['financial']['legitimate_merchants']),
                'payee': random.choice(self.legitimate_patterns['financial']['legitimate_merchants'])
            }
            transaction_history.append(hist_transaction)
        
        device = {
            'ip_address': self.fake.ipv4(),
            'user_agent': self.fake.user_agent(),
            'is_new_device': False,
            'vpn_detected': False,
            'fingerprint_anomaly': False
        }
        
        return {
            'transaction': transaction,
            'account': account,
            'transaction_history': transaction_history,
            'device': device,
            'sanctions_screening': {
                'risk_score': random.uniform(0.0, 0.2),  # Low risk
                'pep_score': random.uniform(0.0, 0.1),
                'aml_score': random.uniform(0.0, 0.2)
            }
        }
    
    def _generate_fraudulent_financial_data(self) -> Dict[str, Any]:
        """Generate realistic fraudulent financial transaction data"""
        fraud_type = random.choice(['structuring', 'high_risk_location', 'suspicious_amount', 'velocity_fraud'])
        
        if fraud_type == 'structuring':
            # Multiple transactions just under reporting threshold
            amount = random.choice(self.fraud_patterns['financial']['suspicious_amounts'])
        elif fraud_type == 'high_risk_location':
            # Transaction from high-risk country
            amount = random.uniform(1000, 10000)
        elif fraud_type == 'suspicious_amount':
            # Round amount or unusual pattern
            amount = random.choice([10000, 5000, 25000, 50000])
        else:  # velocity_fraud
            # Rapid succession of transactions
            amount = random.uniform(500, 2000)
        
        transaction = {
            'amount': amount,
            'currency': 'USD',
            'timestamp': self.fake.date_time_between(start_date='-7d', end_date='now').isoformat(),
            'merchant': {
                'name': random.choice(self.fraud_patterns['financial']['suspicious_merchants']),
                'category': random.choice(['money_transfer', 'cryptocurrency', 'cash_advance'])
            },
            'location': {
                'country': random.choice(self.fraud_patterns['financial']['high_risk_countries']) if fraud_type == 'high_risk_location' else 'US',
                'city': self.fake.city(),
                'coordinates': [self.fake.longitude(), self.fake.latitude()]
            },
            'payment_method': random.choice(['wire_transfer', 'cryptocurrency', 'prepaid_card']),
            'payee': 'NEW_PAYEE_' + str(random.randint(1000, 9999))
        }
        
        account = {
            'balance': random.uniform(100, 5000),  # Lower balance
            'credit_score': random.randint(300, 650),  # Lower credit score
            'created_date': self.fake.date_between(start_date='-2y', end_date='-6m').isoformat(),
            'country': 'US'
        }
        
        # Generate suspicious transaction history
        transaction_history = []
        if fraud_type == 'velocity_fraud':
            # Many recent transactions
            for _ in range(random.randint(20, 50)):
                hist_transaction = {
                    'amount': random.uniform(100, 1000),
                    'timestamp': self.fake.date_time_between(start_date='-24h', end_date='-1h').isoformat(),
                    'merchant': random.choice(self.fraud_patterns['financial']['suspicious_merchants']),
                    'payee': 'PAYEE_' + str(random.randint(100, 999))
                }
                transaction_history.append(hist_transaction)
        elif fraud_type == 'structuring':
            # Multiple transactions just under threshold
            for _ in range(random.randint(5, 15)):
                hist_transaction = {
                    'amount': random.choice(self.fraud_patterns['financial']['suspicious_amounts']),
                    'timestamp': self.fake.date_time_between(start_date='-30d', end_date='-1d').isoformat(),
                    'merchant': random.choice(self.fraud_patterns['financial']['suspicious_merchants']),
                    'payee': 'PAYEE_' + str(random.randint(100, 999))
                }
                transaction_history.append(hist_transaction)
        else:
            # Normal history but current transaction is suspicious
            for _ in range(random.randint(5, 20)):
                hist_transaction = {
                    'amount': random.uniform(50, 500),
                    'timestamp': self.fake.date_time_between(start_date='-90d', end_date='-7d').isoformat(),
                    'merchant': random.choice(self.legitimate_patterns['financial']['legitimate_merchants']),
                    'payee': random.choice(self.legitimate_patterns['financial']['legitimate_merchants'])
                }
                transaction_history.append(hist_transaction)
        
        device = {
            'ip_address': self.fake.ipv4(),
            'user_agent': self.fake.user_agent(),
            'is_new_device': random.choice([True, False]),
            'vpn_detected': random.choice([True, False]),
            'fingerprint_anomaly': random.choice([True, False])
        }
        
        return {
            'transaction': transaction,
            'account': account,
            'transaction_history': transaction_history,
            'device': device,
            'sanctions_screening': {
                'risk_score': random.uniform(0.3, 0.9),  # Higher risk
                'pep_score': random.uniform(0.0, 0.5),
                'aml_score': random.uniform(0.2, 0.8)
            }
        }
    
    def generate_all_fraud_types(self, samples_per_type: int = 1000) -> Tuple[Dict[str, List[Dict]], Dict[str, List[int]]]:
        """Generate synthetic data for all fraud types"""
        all_data = {}
        all_labels = {}
        
        # Generate domain fraud data
        domain_data, domain_labels = self.generate_domain_fraud_data(samples_per_type)
        all_data['domain'] = domain_data
        all_labels['domain'] = domain_labels
        
        # Generate email fraud data
        email_data, email_labels = self.generate_email_fraud_data(samples_per_type)
        all_data['email'] = email_data
        all_labels['email'] = email_labels
        
        # Generate financial fraud data
        financial_data, financial_labels = self.generate_financial_fraud_data(samples_per_type)
        all_data['financial'] = financial_data
        all_labels['financial'] = financial_labels
        
        return all_data, all_labels
    
    def save_synthetic_data(self, output_dir: str = "synthetic_data", samples_per_type: int = 1000):
        """Generate and save synthetic data to files"""
        import os
        
        os.makedirs(output_dir, exist_ok=True)
        
        all_data, all_labels = self.generate_all_fraud_types(samples_per_type)
        
        for data_type in ['domain', 'email', 'financial']:
            # Save data
            data_file = os.path.join(output_dir, f"{data_type}_fraud_data.json")
            with open(data_file, 'w') as f:
                json.dump(all_data[data_type], f, indent=2)
            
            # Save labels
            labels_file = os.path.join(output_dir, f"{data_type}_fraud_labels.json")
            with open(labels_file, 'w') as f:
                json.dump(all_labels[data_type], f, indent=2)
            
            print(f"Generated {len(all_data[data_type])} {data_type} fraud samples")
        
        # Save metadata
        metadata = {
            'generated_at': datetime.now().isoformat(),
            'samples_per_type': samples_per_type,
            'total_samples': samples_per_type * 3,
            'fraud_types': ['domain', 'email', 'financial'],
            'label_distribution': {
                data_type: {
                    'legitimate': all_labels[data_type].count(0),
                    'fraudulent': all_labels[data_type].count(1)
                }
                for data_type in ['domain', 'email', 'financial']
            }
        }
        
        metadata_file = os.path.join(output_dir, "metadata.json")
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Synthetic data generation complete. Files saved to {output_dir}/")
        return output_dir

if __name__ == "__main__":
    # Generate synthetic data for testing
    generator = SyntheticFraudDataGenerator()
    output_dir = generator.save_synthetic_data(samples_per_type=500)
    print(f"Synthetic training data generated in: {output_dir}")

