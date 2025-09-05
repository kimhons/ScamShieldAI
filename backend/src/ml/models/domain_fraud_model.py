"""
ScamShield AI - Domain Fraud Detection Model
Simple, practical Random Forest model for domain fraud detection.
"""

import json
import os
import pickle
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional
import re

# Try to import sklearn, fallback to simple implementation if not available
try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report
    import numpy as np
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("Warning: scikit-learn not available. Using simple rule-based model.")

class SimpleDomainFraudModel:
    """
    Simple, practical domain fraud detection model.
    Uses Random Forest if available, otherwise falls back to rule-based detection.
    """
    
    def __init__(self):
        self.model = None
        self.feature_names = []
        self.model_metadata = {}
        self.is_trained = False
        self.use_sklearn = SKLEARN_AVAILABLE
        
        # Rule-based thresholds for fallback
        self.rule_thresholds = {
            'domain_age_days_suspicious': 30,
            'ssl_invalid_penalty': 0.3,
            'dns_minimal_penalty': 0.2,
            'reputation_low_threshold': 1000000,
            'virustotal_detection_threshold': 1
        }
        
        # Fraud patterns for rule-based detection
        self.fraud_indicators = {
            'suspicious_tlds': ['.tk', '.ml', '.ga', '.cf', '.top', '.click', '.download'],
            'typosquatting_targets': ['paypal', 'google', 'microsoft', 'amazon', 'apple', 'facebook'],
            'suspicious_keywords': ['verify', 'secure', 'update', 'suspended', 'urgent', 'bank'],
            'suspicious_registrars': ['freenom', 'unknown registrar', 'privacy protected']
        }
    
    def extract_features(self, domain_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract comprehensive features from domain data.
        Returns a dictionary of numerical features suitable for ML training.
        """
        features = {}
        
        try:
            # Basic domain features
            domain = domain_data.get('domain', '').lower()
            features.update(self._extract_basic_domain_features(domain))
            
            # WHOIS features
            whois_data = domain_data.get('whois_data', {})
            features.update(self._extract_whois_features(whois_data))
            
            # SSL features
            ssl_data = domain_data.get('ssl_analysis', {})
            features.update(self._extract_ssl_features(ssl_data))
            
            # DNS features
            dns_data = domain_data.get('dns_analysis', {})
            features.update(self._extract_dns_features(dns_data))
            
            # Reputation features
            reputation_data = domain_data.get('reputation_data', {})
            features.update(self._extract_reputation_features(reputation_data))
            
        except Exception as e:
            print(f"Feature extraction error: {str(e)}")
            features = self._get_default_features()
        
        # Ensure all features are numerical and valid
        features = self._validate_features(features)
        
        return features
    
    def _extract_basic_domain_features(self, domain: str) -> Dict[str, float]:
        """Extract basic domain-level features"""
        features = {}
        
        if not domain:
            return {'domain_length': 0, 'subdomain_count': 0, 'has_suspicious_tld': 0}
        
        # Domain length
        features['domain_length'] = len(domain)
        
        # Subdomain count
        parts = domain.split('.')
        features['subdomain_count'] = max(0, len(parts) - 2)  # Subtract domain and TLD
        
        # Suspicious TLD detection
        features['has_suspicious_tld'] = float(any(domain.endswith(tld) for tld in self.fraud_indicators['suspicious_tlds']))
        
        # Typosquatting detection
        domain_base = parts[0] if parts else domain
        typosquatting_score = 0
        for target in self.fraud_indicators['typosquatting_targets']:
            if target in domain_base and domain_base != target:
                # Calculate similarity (simple approach)
                similarity = len(set(domain_base) & set(target)) / len(set(target))
                if similarity > 0.7:  # High similarity but not exact match
                    typosquatting_score = max(typosquatting_score, similarity)
        features['typosquatting_score'] = typosquatting_score
        
        # Suspicious keyword detection
        keyword_count = sum(1 for keyword in self.fraud_indicators['suspicious_keywords'] if keyword in domain)
        features['suspicious_keyword_count'] = keyword_count
        
        # Character analysis
        features['digit_ratio'] = sum(1 for c in domain if c.isdigit()) / len(domain) if domain else 0
        features['hyphen_count'] = domain.count('-')
        
        return features
    
    def _extract_whois_features(self, whois_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract WHOIS-based features"""
        features = {}
        
        # Domain age calculation
        creation_date_str = whois_data.get('creation_date', '')
        if creation_date_str:
            try:
                # Handle different date formats
                if 'T' in creation_date_str:
                    creation_date = datetime.fromisoformat(creation_date_str.replace('Z', '+00:00'))
                else:
                    creation_date = datetime.fromisoformat(creation_date_str)
                
                age_days = (datetime.now() - creation_date.replace(tzinfo=None)).days
                features['domain_age_days'] = max(0, age_days)
            except:
                features['domain_age_days'] = 0
                features['domain_age_unknown'] = 1
        else:
            features['domain_age_days'] = 0
            features['domain_age_unknown'] = 1
        
        # Registrar reputation
        registrar = whois_data.get('registrar', '').lower()
        features['registrar_reputation_score'] = self._calculate_registrar_reputation(registrar)
        
        # Privacy protection
        registrant = str(whois_data.get('registrant', '')).lower()
        features['whois_privacy_protected'] = float('privacy' in registrant or 'redacted' in registrant)
        
        # Update frequency (creation vs update date)
        creation_date_str = whois_data.get('creation_date', '')
        updated_date_str = whois_data.get('updated_date', '')
        if creation_date_str and updated_date_str:
            features['creation_update_same'] = float(creation_date_str == updated_date_str)
        else:
            features['creation_update_same'] = 0
        
        return features
    
    def _calculate_registrar_reputation(self, registrar: str) -> float:
        """Calculate registrar reputation score"""
        if not registrar:
            return 0.3
        
        # High reputation registrars
        high_rep = ['godaddy', 'namecheap', 'cloudflare', 'google domains', 'amazon registrar']
        if any(rep in registrar for rep in high_rep):
            return 0.9
        
        # Medium reputation registrars
        medium_rep = ['network solutions', 'hover', 'name.com', 'gandi']
        if any(rep in registrar for rep in medium_rep):
            return 0.7
        
        # Low reputation registrars
        low_rep = ['freenom', 'unknown registrar']
        if any(rep in registrar for rep in low_rep):
            return 0.1
        
        return 0.5  # Unknown registrar
    
    def _extract_ssl_features(self, ssl_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract SSL certificate features"""
        features = {}
        
        # SSL validity
        features['ssl_valid'] = float(ssl_data.get('valid', False))
        
        # Certificate age
        cert_age = ssl_data.get('certificate_age_days', 0)
        features['ssl_certificate_age_days'] = cert_age
        features['ssl_very_new'] = float(cert_age < 7)  # Very new certificate
        
        # Issuer reputation
        issuer = ssl_data.get('issuer', '').lower()
        if 'self-signed' in issuer:
            features['ssl_issuer_reputation'] = 0.1
        elif any(trusted in issuer for trusted in ['let\'s encrypt', 'digicert', 'cloudflare']):
            features['ssl_issuer_reputation'] = 0.9
        else:
            features['ssl_issuer_reputation'] = 0.5
        
        return features
    
    def _extract_dns_features(self, dns_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract DNS configuration features"""
        features = {}
        
        # DNS record counts
        features['dns_mx_count'] = dns_data.get('mx_count', 0)
        features['dns_ns_count'] = dns_data.get('ns_count', 0)
        features['dns_total_records'] = dns_data.get('total_records', 0)
        
        # Minimal DNS setup (suspicious)
        features['dns_minimal_setup'] = float(features['dns_total_records'] <= 2)
        features['dns_no_email'] = float(features['dns_mx_count'] == 0)
        
        return features
    
    def _extract_reputation_features(self, reputation_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract reputation and security features"""
        features = {}
        
        # Alexa rank (lower is better)
        alexa_rank = reputation_data.get('alexa_rank', 10000000)
        features['alexa_rank_log'] = min(10, max(0, 10 - (alexa_rank / 1000000)))  # Normalize to 0-10
        
        # Google Safe Browsing
        safe_browsing = reputation_data.get('google_safe_browsing', 'safe').lower()
        features['google_safe_browsing_safe'] = float(safe_browsing == 'safe')
        
        # VirusTotal detections
        vt_detections = reputation_data.get('virustotal_detections', 0)
        features['virustotal_detections'] = min(20, vt_detections)  # Cap at 20
        features['virustotal_clean'] = float(vt_detections == 0)
        
        return features
    
    def _validate_features(self, features: Dict[str, float]) -> Dict[str, float]:
        """Validate and clean features"""
        validated = {}
        
        for name, value in features.items():
            try:
                # Convert to float
                float_val = float(value)
                
                # Check for invalid values
                if str(float_val).lower() in ['nan', 'inf', '-inf']:
                    float_val = 0.0
                
                # Apply reasonable bounds
                if name.endswith('_ratio') or name.endswith('_score'):
                    float_val = max(0.0, min(1.0, float_val))
                elif name.endswith('_days') or name.endswith('_count'):
                    float_val = max(0.0, float_val)
                
                validated[name] = float_val
                
            except (ValueError, TypeError):
                validated[name] = 0.0
        
        return validated
    
    def _get_default_features(self) -> Dict[str, float]:
        """Get default feature set for error cases"""
        return {
            'domain_length': 0, 'subdomain_count': 0, 'has_suspicious_tld': 0,
            'typosquatting_score': 0, 'suspicious_keyword_count': 0,
            'digit_ratio': 0, 'hyphen_count': 0, 'domain_age_days': 0,
            'domain_age_unknown': 1, 'registrar_reputation_score': 0.3,
            'whois_privacy_protected': 0, 'creation_update_same': 0,
            'ssl_valid': 0, 'ssl_certificate_age_days': 0, 'ssl_very_new': 0,
            'ssl_issuer_reputation': 0.5, 'dns_mx_count': 0, 'dns_ns_count': 0,
            'dns_total_records': 0, 'dns_minimal_setup': 1, 'dns_no_email': 1,
            'alexa_rank_log': 0, 'google_safe_browsing_safe': 0,
            'virustotal_detections': 0, 'virustotal_clean': 0
        }
    
    def train(self, training_data: List[Dict[str, Any]], labels: List[int]) -> Dict[str, Any]:
        """
        Train the domain fraud detection model.
        Returns training metrics.
        """
        print(f"Training domain fraud model with {len(training_data)} samples...")
        
        # Extract features from training data
        X = []
        for data in training_data:
            features = self.extract_features(data)
            X.append(list(features.values()))
        
        # Store feature names for later use
        if training_data:
            sample_features = self.extract_features(training_data[0])
            self.feature_names = list(sample_features.keys())
        
        if self.use_sklearn and len(X) > 10:
            return self._train_sklearn_model(X, labels)
        else:
            return self._train_rule_based_model(training_data, labels)
    
    def _train_sklearn_model(self, X: List[List[float]], labels: List[int]) -> Dict[str, Any]:
        """Train using scikit-learn Random Forest"""
        X = np.array(X)
        y = np.array(labels)
        
        # Split data for validation
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train Random Forest
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'  # Handle imbalanced data
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        
        # Cross-validation
        cv_scores = cross_val_score(self.model, X_train, y_train, cv=5)
        
        # Feature importance
        feature_importance = dict(zip(self.feature_names, self.model.feature_importances_))
        top_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:10]
        
        self.is_trained = True
        self.model_metadata = {
            'model_type': 'RandomForest',
            'training_samples': len(X),
            'features_count': len(self.feature_names),
            'trained_at': datetime.now().isoformat()
        }
        
        metrics = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'top_features': top_features[:5],
            'model_type': 'sklearn_random_forest'
        }
        
        print(f"Model trained successfully: Accuracy={accuracy:.3f}, Precision={precision:.3f}, Recall={recall:.3f}")
        return metrics
    
    def _train_rule_based_model(self, training_data: List[Dict[str, Any]], labels: List[int]) -> Dict[str, Any]:
        """Train using rule-based approach (fallback)"""
        print("Training rule-based model (sklearn not available)...")
        
        # Analyze training data to optimize thresholds
        fraud_samples = [data for data, label in zip(training_data, labels) if label == 1]
        legit_samples = [data for data, label in zip(training_data, labels) if label == 0]
        
        # Calculate optimal thresholds based on training data
        if fraud_samples:
            fraud_ages = []
            for sample in fraud_samples:
                features = self.extract_features(sample)
                fraud_ages.append(features.get('domain_age_days', 0))
            
            if fraud_ages:
                # Set threshold at 75th percentile of fraud domain ages
                fraud_ages.sort()
                threshold_idx = int(len(fraud_ages) * 0.75)
                self.rule_thresholds['domain_age_days_suspicious'] = fraud_ages[threshold_idx]
        
        # Test rule-based model on training data
        correct_predictions = 0
        total_predictions = len(training_data)
        
        for data, true_label in zip(training_data, labels):
            predicted_prob, _, _ = self.predict(data)
            predicted_label = 1 if predicted_prob > 0.5 else 0
            if predicted_label == true_label:
                correct_predictions += 1
        
        accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
        
        self.is_trained = True
        self.model_metadata = {
            'model_type': 'rule_based',
            'training_samples': len(training_data),
            'trained_at': datetime.now().isoformat(),
            'thresholds': self.rule_thresholds
        }
        
        metrics = {
            'accuracy': accuracy,
            'precision': accuracy,  # Approximation for rule-based
            'recall': accuracy,     # Approximation for rule-based
            'f1_score': accuracy,   # Approximation for rule-based
            'model_type': 'rule_based'
        }
        
        print(f"Rule-based model trained: Accuracy={accuracy:.3f}")
        return metrics
    
    def predict(self, domain_data: Dict[str, Any]) -> Tuple[float, float, Dict[str, Any]]:
        """
        Predict fraud probability for a domain.
        Returns: (fraud_probability, confidence, explanation)
        """
        if not self.is_trained:
            return 0.5, 0.0, {'error': 'Model not trained'}
        
        try:
            features = self.extract_features(domain_data)
            
            if self.use_sklearn and self.model is not None:
                return self._predict_sklearn(features)
            else:
                return self._predict_rule_based(features, domain_data)
                
        except Exception as e:
            return 0.5, 0.0, {'error': f'Prediction error: {str(e)}'}
    
    def _predict_sklearn(self, features: Dict[str, float]) -> Tuple[float, float, Dict[str, Any]]:
        """Make prediction using sklearn model"""
        # Convert features to array in correct order
        feature_array = np.array([[features.get(name, 0) for name in self.feature_names]])
        
        # Get prediction probability
        fraud_prob = self.model.predict_proba(feature_array)[0][1]
        
        # Calculate confidence based on how far from decision boundary
        confidence = abs(fraud_prob - 0.5) * 2
        
        # Get feature importance for explanation
        feature_importance = dict(zip(self.feature_names, self.model.feature_importances_))
        top_factors = sorted(
            [(name, features[name], importance) for name, importance in feature_importance.items()],
            key=lambda x: x[2], reverse=True
        )[:5]
        
        explanation = {
            'model_type': 'sklearn_random_forest',
            'top_risk_factors': [
                {'feature': name, 'value': value, 'importance': importance}
                for name, value, importance in top_factors
            ]
        }
        
        return fraud_prob, confidence, explanation
    
    def _predict_rule_based(self, features: Dict[str, float], domain_data: Dict[str, Any]) -> Tuple[float, float, Dict[str, Any]]:
        """Make prediction using rule-based approach"""
        risk_score = 0.0
        risk_factors = []
        
        # Domain age risk
        domain_age = features.get('domain_age_days', 0)
        if domain_age < self.rule_thresholds['domain_age_days_suspicious']:
            age_risk = 0.3 * (1 - domain_age / self.rule_thresholds['domain_age_days_suspicious'])
            risk_score += age_risk
            risk_factors.append(f'Very new domain ({domain_age} days old)')
        
        # Suspicious TLD
        if features.get('has_suspicious_tld', 0) > 0:
            risk_score += 0.4
            risk_factors.append('Suspicious top-level domain')
        
        # Typosquatting
        typo_score = features.get('typosquatting_score', 0)
        if typo_score > 0.5:
            risk_score += 0.5 * typo_score
            risk_factors.append(f'Possible typosquatting (similarity: {typo_score:.2f})')
        
        # SSL issues
        if features.get('ssl_valid', 1) == 0:
            risk_score += self.rule_thresholds['ssl_invalid_penalty']
            risk_factors.append('Invalid SSL certificate')
        
        # Minimal DNS setup
        if features.get('dns_minimal_setup', 0) > 0:
            risk_score += self.rule_thresholds['dns_minimal_penalty']
            risk_factors.append('Minimal DNS configuration')
        
        # Low reputation
        alexa_rank = domain_data.get('reputation_data', {}).get('alexa_rank', 0)
        if alexa_rank > self.rule_thresholds['reputation_low_threshold']:
            risk_score += 0.2
            risk_factors.append('Low domain reputation')
        
        # VirusTotal detections
        vt_detections = features.get('virustotal_detections', 0)
        if vt_detections >= self.rule_thresholds['virustotal_detection_threshold']:
            risk_score += min(0.5, vt_detections * 0.1)
            risk_factors.append(f'Security detections ({vt_detections} engines)')
        
        # Suspicious keywords
        keyword_count = features.get('suspicious_keyword_count', 0)
        if keyword_count > 0:
            risk_score += min(0.3, keyword_count * 0.1)
            risk_factors.append(f'Suspicious keywords ({keyword_count} found)')
        
        # Normalize risk score to probability
        fraud_prob = min(1.0, risk_score)
        confidence = min(1.0, len(risk_factors) * 0.2)  # More factors = higher confidence
        
        explanation = {
            'model_type': 'rule_based',
            'risk_factors': risk_factors,
            'risk_score': risk_score,
            'total_factors': len(risk_factors)
        }
        
        return fraud_prob, confidence, explanation
    
    def save_model(self, filepath: str):
        """Save the trained model to file"""
        model_data = {
            'model': self.model,
            'feature_names': self.feature_names,
            'model_metadata': self.model_metadata,
            'is_trained': self.is_trained,
            'use_sklearn': self.use_sklearn,
            'rule_thresholds': self.rule_thresholds,
            'fraud_indicators': self.fraud_indicators
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"Model saved to: {filepath}")
    
    def load_model(self, filepath: str):
        """Load a trained model from file"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data['model']
        self.feature_names = model_data['feature_names']
        self.model_metadata = model_data['model_metadata']
        self.is_trained = model_data['is_trained']
        self.use_sklearn = model_data.get('use_sklearn', SKLEARN_AVAILABLE)
        self.rule_thresholds = model_data.get('rule_thresholds', self.rule_thresholds)
        self.fraud_indicators = model_data.get('fraud_indicators', self.fraud_indicators)
        
        print(f"Model loaded from: {filepath}")

if __name__ == "__main__":
    # Test the domain fraud model
    print("ScamShield AI - Domain Fraud Model Test")
    print("=" * 50)
    
    # Load synthetic training data
    data_dir = "../data/synthetic_data"
    
    try:
        with open(os.path.join(data_dir, "domain_fraud_data.json"), 'r') as f:
            training_data = json.load(f)
        
        with open(os.path.join(data_dir, "domain_fraud_labels.json"), 'r') as f:
            labels = json.load(f)
        
        print(f"Loaded {len(training_data)} training samples")
        
        # Create and train model
        model = SimpleDomainFraudModel()
        metrics = model.train(training_data, labels)
        
        print("\nTraining Results:")
        for metric, value in metrics.items():
            if isinstance(value, float):
                print(f"  {metric}: {value:.3f}")
            else:
                print(f"  {metric}: {value}")
        
        # Test prediction on a sample
        if training_data:
            test_sample = training_data[0]
            fraud_prob, confidence, explanation = model.predict(test_sample)
            
            print(f"\nTest Prediction:")
            print(f"  Domain: {test_sample.get('domain', 'Unknown')}")
            print(f"  Fraud Probability: {fraud_prob:.3f}")
            print(f"  Confidence: {confidence:.3f}")
            print(f"  Explanation: {explanation}")
        
        # Save model
        model.save_model("domain_fraud_model.pkl")
        print("\nModel training and testing complete!")
        
    except FileNotFoundError:
        print("Error: Synthetic training data not found. Please run the data generator first.")
    except Exception as e:
        print(f"Error: {str(e)}")

