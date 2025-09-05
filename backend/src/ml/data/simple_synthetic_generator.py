"""
ScamShield AI - Simplified Synthetic Data Generator
Generates realistic fraud and legitimate investigation data without external dependencies.
"""

import random
import string
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple

class SimpleSyntheticDataGenerator:
    """
    Generate synthetic training data using built-in Python libraries only.
    Designed to work without external dependencies like Faker.
    """
    
    def __init__(self, seed: int = 42):
        random.seed(seed)
        self._load_patterns()
    
    def _load_patterns(self):
        """Load fraud and legitimate patterns"""
        self.fraud_patterns = {
            'domains': {
                'typosquatting': [
                    'payp4l', 'g00gle', 'micr0soft', 'amaz0n', 'appl3',
                    'fac3book', 'tw1tter', 'inst4gram', 'link3din'
                ],
                'suspicious_tlds': ['.tk', '.ml', '.ga', '.cf', '.top', '.click'],
                'suspicious_keywords': [
                    'verify', 'secure', 'update', 'suspended', 'urgent',
                    'bank', 'paypal', 'amazon', 'microsoft', 'apple'
                ]
            },
            'emails': {
                'phishing_subjects': [
                    'URGENT: Verify Your Account',
                    'Your Account Has Been Suspended',
                    'Immediate Action Required',
                    'Security Alert: Unusual Activity'
                ],
                'suspicious_content': [
                    'click here immediately',
                    'verify your account now',
                    'suspended due to suspicious activity'
                ]
            },
            'financial': {
                'suspicious_amounts': [9999, 9500, 9800, 4999, 2999],
                'high_risk_countries': ['AF', 'IR', 'KP', 'SY', 'MM'],
                'suspicious_merchants': [
                    'QUICK CASH LLC', 'TEMP SERVICES', 'CRYPTO EXCHANGE'
                ]
            }
        }
        
        self.legitimate_patterns = {
            'domains': {
                'reputable_tlds': ['.com', '.net', '.org', '.edu'],
                'legitimate_registrars': [
                    'GoDaddy', 'Namecheap', 'Cloudflare', 'Google Domains'
                ],
                'business_keywords': [
                    'corp', 'inc', 'llc', 'company', 'services', 'tech'
                ]
            },
            'emails': {
                'normal_subjects': [
                    'Monthly Newsletter', 'Order Confirmation',
                    'Welcome to Our Service', 'Meeting Reminder'
                ],
                'normal_content': [
                    'thank you for your business',
                    'your order has been processed',
                    'welcome to our community'
                ]
            },
            'financial': {
                'normal_amounts': [25.99, 49.99, 99.99, 199.99, 299.99],
                'low_risk_countries': ['US', 'CA', 'GB', 'DE', 'FR', 'AU'],
                'legitimate_merchants': [
                    'AMAZON.COM', 'WALMART', 'TARGET', 'STARBUCKS'
                ]
            }
        }
        
        # Simple fake data generators
        self.companies = [
            'TechCorp', 'DataSystems', 'CloudServices', 'WebSolutions',
            'InfoTech', 'DigitalWorks', 'SmartSystems', 'NetServices'
        ]
        
        self.names = [
            'john', 'jane', 'bob', 'alice', 'mike', 'sarah', 'david', 'lisa'
        ]
        
        self.cities = [
            'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
            'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose'
        ]
    
    def _fake_company(self) -> str:
        """Generate fake company name"""
        return random.choice(self.companies)
    
    def _fake_email(self) -> str:
        """Generate fake email address"""
        domains = ['example.com', 'test.org', 'sample.net', 'demo.com']
        return f'{random.choice(self.names)}@{random.choice(domains)}'
    
    def _fake_ipv4(self) -> str:
        """Generate fake IPv4 address"""
        return f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}'
    
    def _fake_domain(self) -> str:
        """Generate fake domain name"""
        names = ['example', 'test', 'sample', 'demo', 'site', 'web']
        tlds = ['.com', '.net', '.org', '.info']
        return f'{random.choice(names)}{random.choice(tlds)}'
    
    def _fake_date_between(self, start_days_ago: int, end_days_ago: int = 0) -> str:
        """Generate fake date between two points"""
        start_date = datetime.now() - timedelta(days=start_days_ago)
        end_date = datetime.now() - timedelta(days=end_days_ago)
        
        time_between = end_date - start_date
        days_between = time_between.days
        
        if days_between <= 0:
            return start_date.isoformat()
        
        random_days = random.randint(0, days_between)
        random_date = start_date + timedelta(days=random_days)
        return random_date.isoformat()
    
    def _fake_uuid(self) -> str:
        """Generate fake UUID-like string"""
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(32))
    
    def generate_domain_fraud_data(self, num_samples: int = 100) -> Tuple[List[Dict], List[int]]:
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
        company = self._fake_company().lower().replace(' ', '')
        business_word = random.choice(self.legitimate_patterns['domains']['business_keywords'])
        tld = random.choice(self.legitimate_patterns['domains']['reputable_tlds'])
        domain = f"{company}-{business_word}{tld}"
        
        creation_date = self._fake_date_between(1825, 365)  # 1-5 years ago
        
        whois_data = {
            'domain': domain,
            'creation_date': creation_date,
            'updated_date': self._fake_date_between(365, 30),
            'expiry_date': self._fake_date_between(-365, -30),  # Future date
            'registrar': random.choice(self.legitimate_patterns['domains']['legitimate_registrars']),
            'registrant': self._fake_company(),
            'privacy_protected': random.choice([True, False])
        }
        
        ssl_analysis = {
            'valid': True,
            'issuer': random.choice(['Let\'s Encrypt', 'DigiCert', 'Cloudflare']),
            'expiry_date': self._fake_date_between(-365, -30),
            'certificate_age_days': random.randint(30, 365)
        }
        
        dns_analysis = {
            'records': [
                {'type': 'A', 'value': self._fake_ipv4()},
                {'type': 'MX', 'value': f"mail.{domain}"},
                {'type': 'NS', 'value': f"ns1.{domain}"}
            ],
            'mx_count': 1,
            'ns_count': 1,
            'total_records': 3
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
        fraud_type = random.choice(['typosquatting', 'suspicious_tld', 'keyword_stuffing'])
        
        if fraud_type == 'typosquatting':
            domain_base = random.choice(self.fraud_patterns['domains']['typosquatting'])
            tld = random.choice(self.fraud_patterns['domains']['suspicious_tlds'])
            domain = f"{domain_base}{tld}"
        elif fraud_type == 'suspicious_tld':
            legitimate_name = self._fake_company().lower().replace(' ', '')[:8]
            tld = random.choice(self.fraud_patterns['domains']['suspicious_tlds'])
            domain = f"{legitimate_name}{tld}"
        else:  # keyword_stuffing
            keywords = random.sample(self.fraud_patterns['domains']['suspicious_keywords'], 2)
            domain = f"{keywords[0]}-{keywords[1]}.com"
        
        creation_date = self._fake_date_between(30, 0)  # Very recent
        
        whois_data = {
            'domain': domain,
            'creation_date': creation_date,
            'updated_date': creation_date,  # Same as creation (suspicious)
            'expiry_date': self._fake_date_between(-365, -30),
            'registrar': 'Freenom' if domain.endswith(('.tk', '.ml', '.ga', '.cf')) else 'Unknown Registrar',
            'registrant': 'REDACTED FOR PRIVACY',
            'privacy_protected': True
        }
        
        ssl_analysis = {
            'valid': random.choice([False, False, True]),  # 66% chance invalid
            'issuer': 'Self-signed' if random.random() > 0.7 else 'Let\'s Encrypt',
            'expiry_date': None if random.random() > 0.7 else self._fake_date_between(-90, -1),
            'certificate_age_days': random.randint(1, 30)
        }
        
        dns_analysis = {
            'records': [{'type': 'A', 'value': self._fake_ipv4()}],
            'mx_count': 0,  # No email setup
            'ns_count': random.randint(0, 1),
            'total_records': 1
        }
        
        return {
            'domain': domain,
            'whois_data': whois_data,
            'ssl_analysis': ssl_analysis,
            'dns_analysis': dns_analysis,
            'reputation_data': {
                'alexa_rank': random.randint(5000000, 10000000),
                'google_safe_browsing': random.choice(['unsafe', 'malware', 'phishing']),
                'virustotal_detections': random.randint(1, 15)
            }
        }
    
    def generate_email_fraud_data(self, num_samples: int = 100) -> Tuple[List[Dict], List[int]]:
        """Generate synthetic email fraud training data"""
        data = []
        labels = []
        
        # Generate legitimate emails (50%)
        for _ in range(num_samples // 2):
            email_data = self._generate_legitimate_email_data()
            data.append(email_data)
            labels.append(0)
        
        # Generate fraudulent emails (50%)
        for _ in range(num_samples // 2):
            email_data = self._generate_fraudulent_email_data()
            data.append(email_data)
            labels.append(1)
        
        return data, labels
    
    def _generate_legitimate_email_data(self) -> Dict[str, Any]:
        """Generate realistic legitimate email data"""
        sender_domain = f"{self._fake_company().lower().replace(' ', '')}.com"
        sender = f"noreply@{sender_domain}"
        
        headers = {
            'from': sender,
            'to': self._fake_email(),
            'subject': random.choice(self.legitimate_patterns['emails']['normal_subjects']),
            'date': self._fake_date_between(30, 0),
            'message-id': f"<{self._fake_uuid()}@{sender_domain}>",
            'received-spf': 'pass',
            'dkim-signature': f"v=1; a=rsa-sha256; d={sender_domain}; s=default",
            'return-path': sender,
            'reply-to': sender
        }
        
        content = {
            'text': f"Dear Customer,\\n\\n{random.choice(self.legitimate_patterns['emails']['normal_content'])}.\\n\\nBest regards,\\nThe Team",
            'html': f"<html><body><p>Dear Customer,</p><p>{random.choice(self.legitimate_patterns['emails']['normal_content'])}.</p></body></html>"
        }
        
        return {
            'headers': headers,
            'content': content,
            'attachments': []
        }
    
    def _generate_fraudulent_email_data(self) -> Dict[str, Any]:
        """Generate realistic fraudulent email data"""
        fraud_type = random.choice(['phishing', 'spoofing', 'spam'])
        
        if fraud_type == 'phishing':
            legitimate_service = random.choice(['PayPal', 'Amazon', 'Microsoft'])
            fake_domain = f"{legitimate_service.lower()}-security.tk"
            sender = f"security@{fake_domain}"
            subject = random.choice(self.fraud_patterns['emails']['phishing_subjects'])
            content_text = f"URGENT: {random.choice(self.fraud_patterns['emails']['suspicious_content'])}."
        elif fraud_type == 'spoofing':
            real_domain = "paypal.com"
            fake_domain = "payp4l-security.ml"
            sender = f"service@{real_domain}"
            reply_to = f"noreply@{fake_domain}"
            subject = "Account Verification Required"
            content_text = "Please verify your account by clicking the link below."
        else:  # spam
            sender = f"winner@lottery.tk"
            subject = "CONGRATULATIONS! You've Won $1,000,000!"
            content_text = "You have won our international lottery!"
        
        headers = {
            'from': sender,
            'to': self._fake_email(),
            'subject': subject,
            'date': self._fake_date_between(7, 0),
            'message-id': f"<{random.randint(100000, 999999)}@{self._fake_domain()}>",
            'received-spf': random.choice(['fail', 'softfail', 'neutral']),
            'dkim-signature': '',
            'return-path': reply_to if fraud_type == 'spoofing' else sender,
            'reply-to': reply_to if fraud_type == 'spoofing' else sender
        }
        
        content = {
            'text': content_text,
            'html': f"<html><body><p>{content_text}</p></body></html>"
        }
        
        return {
            'headers': headers,
            'content': content,
            'attachments': []
        }
    
    def generate_financial_fraud_data(self, num_samples: int = 100) -> Tuple[List[Dict], List[int]]:
        """Generate synthetic financial fraud training data"""
        data = []
        labels = []
        
        # Generate legitimate transactions (50%)
        for _ in range(num_samples // 2):
            financial_data = self._generate_legitimate_financial_data()
            data.append(financial_data)
            labels.append(0)
        
        # Generate fraudulent transactions (50%)
        for _ in range(num_samples // 2):
            financial_data = self._generate_fraudulent_financial_data()
            data.append(financial_data)
            labels.append(1)
        
        return data, labels
    
    def _generate_legitimate_financial_data(self) -> Dict[str, Any]:
        """Generate realistic legitimate financial transaction data"""
        transaction = {
            'amount': random.choice(self.legitimate_patterns['financial']['normal_amounts']),
            'currency': 'USD',
            'timestamp': self._fake_date_between(30, 0),
            'merchant': {
                'name': random.choice(self.legitimate_patterns['financial']['legitimate_merchants']),
                'category': random.choice(['retail', 'restaurant', 'gas_station'])
            },
            'location': {
                'country': random.choice(self.legitimate_patterns['financial']['low_risk_countries']),
                'city': random.choice(self.cities)
            },
            'payment_method': random.choice(['credit_card', 'debit_card']),
            'payee': random.choice(self.legitimate_patterns['financial']['legitimate_merchants'])
        }
        
        account = {
            'balance': random.uniform(1000, 50000),
            'credit_score': random.randint(650, 850),
            'created_date': self._fake_date_between(1825, 365),
            'country': transaction['location']['country']
        }
        
        transaction_history = []
        for _ in range(random.randint(10, 30)):
            hist_transaction = {
                'amount': random.choice(self.legitimate_patterns['financial']['normal_amounts']),
                'timestamp': self._fake_date_between(90, 1),
                'merchant': random.choice(self.legitimate_patterns['financial']['legitimate_merchants'])
            }
            transaction_history.append(hist_transaction)
        
        return {
            'transaction': transaction,
            'account': account,
            'transaction_history': transaction_history,
            'sanctions_screening': {
                'risk_score': random.uniform(0.0, 0.2),
                'pep_score': random.uniform(0.0, 0.1),
                'aml_score': random.uniform(0.0, 0.2)
            }
        }
    
    def _generate_fraudulent_financial_data(self) -> Dict[str, Any]:
        """Generate realistic fraudulent financial transaction data"""
        fraud_type = random.choice(['structuring', 'high_risk_location', 'suspicious_amount'])
        
        if fraud_type == 'structuring':
            amount = random.choice(self.fraud_patterns['financial']['suspicious_amounts'])
        elif fraud_type == 'high_risk_location':
            amount = random.uniform(1000, 10000)
        else:  # suspicious_amount
            amount = random.choice([10000, 5000, 25000])
        
        transaction = {
            'amount': amount,
            'currency': 'USD',
            'timestamp': self._fake_date_between(7, 0),
            'merchant': {
                'name': random.choice(self.fraud_patterns['financial']['suspicious_merchants']),
                'category': random.choice(['money_transfer', 'cryptocurrency'])
            },
            'location': {
                'country': random.choice(self.fraud_patterns['financial']['high_risk_countries']) if fraud_type == 'high_risk_location' else 'US',
                'city': random.choice(self.cities)
            },
            'payment_method': random.choice(['wire_transfer', 'cryptocurrency']),
            'payee': f'NEW_PAYEE_{random.randint(1000, 9999)}'
        }
        
        account = {
            'balance': random.uniform(100, 5000),
            'credit_score': random.randint(300, 650),
            'created_date': self._fake_date_between(730, 180),
            'country': 'US'
        }
        
        transaction_history = []
        if fraud_type == 'structuring':
            # Multiple suspicious transactions
            for _ in range(random.randint(5, 15)):
                hist_transaction = {
                    'amount': random.choice(self.fraud_patterns['financial']['suspicious_amounts']),
                    'timestamp': self._fake_date_between(30, 1),
                    'merchant': random.choice(self.fraud_patterns['financial']['suspicious_merchants'])
                }
                transaction_history.append(hist_transaction)
        else:
            # Normal history but current transaction suspicious
            for _ in range(random.randint(5, 20)):
                hist_transaction = {
                    'amount': random.uniform(50, 500),
                    'timestamp': self._fake_date_between(90, 7),
                    'merchant': random.choice(self.legitimate_patterns['financial']['legitimate_merchants'])
                }
                transaction_history.append(hist_transaction)
        
        return {
            'transaction': transaction,
            'account': account,
            'transaction_history': transaction_history,
            'sanctions_screening': {
                'risk_score': random.uniform(0.3, 0.9),
                'pep_score': random.uniform(0.0, 0.5),
                'aml_score': random.uniform(0.2, 0.8)
            }
        }
    
    def generate_all_fraud_types(self, samples_per_type: int = 100) -> Tuple[Dict[str, List[Dict]], Dict[str, List[int]]]:
        """Generate synthetic data for all fraud types"""
        all_data = {}
        all_labels = {}
        
        print(f"Generating {samples_per_type} samples per fraud type...")
        
        # Generate domain fraud data
        print("Generating domain fraud data...")
        domain_data, domain_labels = self.generate_domain_fraud_data(samples_per_type)
        all_data['domain'] = domain_data
        all_labels['domain'] = domain_labels
        
        # Generate email fraud data
        print("Generating email fraud data...")
        email_data, email_labels = self.generate_email_fraud_data(samples_per_type)
        all_data['email'] = email_data
        all_labels['email'] = email_labels
        
        # Generate financial fraud data
        print("Generating financial fraud data...")
        financial_data, financial_labels = self.generate_financial_fraud_data(samples_per_type)
        all_data['financial'] = financial_data
        all_labels['financial'] = financial_labels
        
        return all_data, all_labels
    
    def save_synthetic_data(self, output_dir: str = "synthetic_data", samples_per_type: int = 100):
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
        
        print(f"\\nSynthetic data generation complete!")
        print(f"Files saved to: {output_dir}/")
        print(f"Total samples generated: {samples_per_type * 3}")
        
        return output_dir

if __name__ == "__main__":
    # Generate synthetic data for testing
    print("ScamShield AI - Synthetic Data Generator")
    print("=" * 50)
    
    generator = SimpleSyntheticDataGenerator()
    output_dir = generator.save_synthetic_data(samples_per_type=200)
    
    print(f"\\nSynthetic training data ready for ML model training!")
    print(f"Location: {output_dir}")

