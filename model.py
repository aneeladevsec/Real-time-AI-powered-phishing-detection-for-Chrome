"""
Phishing Detection ML Model
Extracts 15 features from URL and predicts phishing probability
"""

import joblib
import numpy as np
import re
import os
import warnings
from urllib.parse import urlparse
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
warnings.filterwarnings('ignore')

class PhishingDetector:
    def __init__(self):
        self.model = None
        self.feature_names = [
            'url_length', 'hostname_length', 'path_length', 'dot_count',
            'hyphen_count', 'at_count', 'question_count', 'and_count',
            'equal_count', 'underscore_count', 'slash_count', 'digit_count',
            'has_ip', 'has_https', 'has_suspicious_words'
        ]
        self.load_or_create()
    
    def extract_features(self, url):
        """
        Extract 15 features from URL for phishing detection
        Returns: list of 15 numerical features (normalized 0-1)
        """
        # Ensure URL has scheme
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        try:
            parsed = urlparse(url)
            hostname = parsed.netloc
            path = parsed.path
        except:
            hostname = url
            path = ''
        
        features = {}
        
        # 1. URL Length (normalized: 0-1, >100 = 1.0)
        features['url_length'] = min(len(url) / 100, 1.0)
        
        # 2. Hostname Length
        features['hostname_length'] = min(len(hostname) / 50, 1.0)
        
        # 3. Path Length
        features['path_length'] = min(len(path) / 50, 1.0)
        
        # 4. Dot count in hostname (subdomains)
        features['dot_count'] = min(hostname.count('.') / 5, 1.0)
        
        # 5. Hyphen count (common in phishing)
        features['hyphen_count'] = min(url.count('-') / 5, 1.0)
        
        # 6. @ symbol (credential stuffing)
        features['at_count'] = 1.0 if '@' in url else 0.0
        
        # 7. Query parameters
        features['question_count'] = min(url.count('?') / 2, 1.0)
        
        # 8. & count (parameters)
        features['and_count'] = min(url.count('&') / 5, 1.0)
        
        # 9. = count (key-value pairs)
        features['equal_count'] = min(url.count('=') / 5, 1.0)
        
        # 10. Underscore count
        features['underscore_count'] = min(url.count('_') / 5, 1.0)
        
        # 11. Slash count (directory depth)
        features['slash_count'] = min(path.count('/') / 5, 1.0)
        
        # 12. Digit ratio in hostname
        digits = sum(c.isdigit() for c in hostname)
        features['digit_count'] = digits / max(len(hostname), 1)
        
        # 13. Has IP address (highly suspicious)
        ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        features['has_ip'] = 1.0 if re.search(ip_pattern, hostname) else 0.0
        
        # 14. Has HTTPS (legitimate sites usually have)
        features['has_https'] = 1.0 if url.startswith('https://') else 0.0
        
        # 15. Suspicious keywords
        suspicious = ['secure', 'account', 'update', 'login', 'verify', 
                     'banking', 'confirm', 'security', 'authenticate',
                     'wallet', 'crypto', 'password', 'credential']
        url_lower = url.lower()
        features['has_suspicious_words'] = 1.0 if any(word in url_lower for word in suspicious) else 0.0
        
        # Return as list in consistent order
        return [features[name] for name in self.feature_names]
    
    def generate_training_data(self, n_samples=10000):
        """
        Generate synthetic training data
        In production, replace with real phishing dataset from Kaggle/PhishTank
        """
        np.random.seed(42)
        
        # Legitimate URL patterns
        legit_samples = n_samples // 2
        legit_features = []
        
        for _ in range(legit_samples):
            # Short URLs, HTTPS, no suspicious words
            features = [
                np.random.uniform(0, 0.3),  # url_length
                np.random.uniform(0, 0.4),  # hostname_length
                np.random.uniform(0, 0.5),  # path_length
                np.random.uniform(0, 0.3),  # dot_count
                np.random.uniform(0, 0.1),  # hyphen_count
                0.0,  # at_count
                np.random.uniform(0, 0.2),  # question_count
                np.random.uniform(0, 0.2),  # and_count
                np.random.uniform(0, 0.2),  # equal_count
                np.random.uniform(0, 0.1),  # underscore_count
                np.random.uniform(0, 0.4),  # slash_count
                np.random.uniform(0, 0.2),  # digit_count
                0.0,  # has_ip
                np.random.choice([0.0, 1.0], p=[0.3, 0.7]),  # has_https (mostly HTTPS)
                0.0   # has_suspicious_words
            ]
            legit_features.append(features)
        
        # Phishing URL patterns
        phishing_samples = n_samples // 2
        phishing_features = []
        
        for _ in range(phishing_samples):
            # Long URLs, HTTP, suspicious words, IP addresses
            features = [
                np.random.uniform(0.4, 1.0),  # url_length (long)
                np.random.uniform(0.4, 1.0),  # hostname_length (long)
                np.random.uniform(0.3, 0.9),  # path_length
                np.random.uniform(0.2, 0.8),  # dot_count (many subdomains)
                np.random.uniform(0, 0.6),    # hyphen_count
                np.random.choice([0.0, 1.0], p=[0.9, 0.1]),  # at_count (sometimes)
                np.random.uniform(0, 0.5),    # question_count
                np.random.uniform(0, 0.6),    # and_count
                np.random.uniform(0, 0.6),    # equal_count
                np.random.uniform(0, 0.3),    # underscore_count
                np.random.uniform(0.2, 0.8),  # slash_count
                np.random.uniform(0.1, 0.5),  # digit_count (more digits)
                np.random.choice([0.0, 1.0], p=[0.7, 0.3]),  # has_ip (sometimes)
                np.random.choice([0.0, 1.0], p=[0.7, 0.3]),  # has_https (less HTTPS)
                np.random.choice([0.0, 1.0], p=[0.2, 0.8])   # has_suspicious_words (usually)
            ]
            phishing_features.append(features)
        
        X = np.vstack([legit_features, phishing_features])
        y = np.hstack([np.zeros(legit_samples), np.ones(phishing_samples)])
        
        return X, y
    
    def train_model(self):
        """Train ensemble model"""
        print("🔄 Training phishing detection model...")
        
        X, y = self.generate_training_data()
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Create ensemble
        rf = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )
        
        gb = GradientBoostingClassifier(
            n_estimators=150,
            learning_rate=0.1,
            max_depth=6,
            random_state=42
        )
        
        self.model = VotingClassifier(
            estimators=[('rf', rf), ('gb', gb)],
            voting='soft'
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"✅ Model trained!")
        print(f"   Accuracy: {accuracy:.1%}")
        print(f"   Samples: {len(y)}")
        
        # Save
        joblib.dump(self.model, 'phishing_model.pkl')
        print("💾 Model saved to phishing_model.pkl")
        
        return accuracy
    
    def load_or_create(self):
        """Load existing model or train new one"""
        if os.path.exists('phishing_model.pkl'):
            self.model = joblib.load('phishing_model.pkl')
            print("✅ Phishing model loaded from file")
        else:
            self.train_model()
    
    def predict(self, url):
        """
        Predict if URL is phishing
        Returns: dict with prediction details
        """
        features = self.extract_features(url)
        features_array = np.array(features).reshape(1, -1)
        
        prediction = self.model.predict(features_array)[0]
        probabilities = self.model.predict_proba(features_array)[0]
        
        confidence = float(max(probabilities))
        phishing_prob = float(probabilities[1])
        
        # Determine risk level
        if phishing_prob > 0.8:
            risk_level = 'CRITICAL'
        elif phishing_prob > 0.6:
            risk_level = 'HIGH'
        elif phishing_prob > 0.4:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'
        
        # Generate reasons
        reasons = []
        if features[12] > 0.5:  # has_ip
            reasons.append("Contains IP address instead of domain")
        if features[14] > 0.5:  # suspicious words
            reasons.append("Suspicious keywords detected")
        if features[0] > 0.7:  # long URL
            reasons.append("Unusually long URL")
        if features[3] > 0.6:  # many dots
            reasons.append("Excessive subdomains")
        if features[13] < 0.5:  # no HTTPS
            reasons.append("No HTTPS encryption")
        
        return {
            'url': url,
            'is_phishing': bool(prediction),
            'confidence': confidence,
            'phishing_probability': phishing_prob,
            'legitimate_probability': float(probabilities[0]),
            'risk_level': risk_level,
            'features': {
                'url_length': int(features[0] * 100),
                'has_https': bool(features[13]),
                'has_suspicious_words': bool(features[14]),
                'has_ip_address': bool(features[12])
            },
            'reasons': reasons if reasons else ['No obvious phishing indicators']
        }

# Test if run directly
if __name__ == "__main__":
    detector = PhishingDetector()
    
    test_urls = [
        "https://www.google.com",
        "https://github.com/login",
        "http://192.168.1.1/secure-login",
        "http://verify-account-update.tk/login.php",
        "https://www.bankofamerica.com",
        "http://crypto-wallet-verify.secure-login.tk/update"
    ]
    
    print("\n" + "="*60)
    print("PHISHING DETECTION TEST RESULTS")
    print("="*60)
    
    for url in test_urls:
        result = detector.predict(url)
        status = "🚨 PHISHING" if result['is_phishing'] else "✅ SAFE"
        print(f"\n{status} | {url}")
        print(f"   Confidence: {result['confidence']:.1%}")
        print(f"   Risk Level: {result['risk_level']}")
        print(f"   Reasons: {', '.join(result['reasons'][:2])}")

        print(f"  Risk: {result['risk_level']}")