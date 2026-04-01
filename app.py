"""
Phishing Detection API
Flask backend for URL analysis
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from model import PhishingDetector
from datetime import datetime
import os
import json

app = Flask(__name__)

# CORS for extension and web access
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Initialize detector
print("🚀 Initializing Phishing Detection API...")
detector = PhishingDetector()
print("✅ API Ready!")

# Simple in-memory stats
request_count = 0
phishing_detected_count = 0


@app.route('/')
def home():
    """API home"""
    return jsonify({
        "service": "Phishing Shield API",
        "version": "1.0.0",
        "description": "AI-powered phishing detection",
        "endpoints": {
            "check": "/check (POST) - Check single URL",
            "batch": "/batch (POST) - Check multiple URLs",
            "stats": "/stats (GET) - API statistics",
            "health": "/health (GET) - Health check"
        },
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/check', methods=['POST'])
def check_url():
    """
    Check single URL for phishing
    POST body: {"url": "https://example.com"}
    """
    global request_count, phishing_detected_count
    
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                "error": "URL required",
                "usage": {"url": "https://example.com"}
            }), 400
        
        url = data['url'].strip()
        
        # Basic validation
        if not url or len(url) > 2000:
            return jsonify({"error": "Invalid URL length"}), 400
        
        # Add scheme if missing
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        # Analyze
        result = detector.predict(url)
        
        # Update stats
        request_count += 1
        if result['is_phishing']:
            phishing_detected_count += 1
        
        return jsonify({
            **result,
            "timestamp": datetime.now().isoformat(),
            "api_version": "1.0.0",
            "status": "success"
        })
    
    except Exception as e:
        return jsonify({
            "error": "Analysis failed",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500


@app.route('/batch', methods=['POST'])
def batch_check():
    """
    Check multiple URLs
    POST body: {"urls": ["url1", "url2", ...]}
    """
    global request_count, phishing_detected_count
    
    try:
        data = request.get_json()
        
        if not data or 'urls' not in data:
            return jsonify({"error": "URLs array required"}), 400
        
        urls = data['urls']
        
        if not isinstance(urls, list):
            return jsonify({"error": "URLs must be an array"}), 400
        
        if len(urls) > 20:
            return jsonify({"error": "Maximum 20 URLs per batch"}), 400
        
        results = []
        for url in urls:
            if not isinstance(url, str):
                continue
            
            url = url.strip()
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            result = detector.predict(url)
            results.append(result)
            
            request_count += 1
            if result['is_phishing']:
                phishing_detected_count += 1
        
        # Summary
        phishing_count = sum(1 for r in results if r['is_phishing'])
        
        return jsonify({
            "results": results,
            "summary": {
                "total": len(results),
                "phishing_detected": phishing_count,
                "safe": len(results) - phishing_count,
                "phishing_percentage": round((phishing_count / len(results)) * 100, 1) if results else 0
            },
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            "error": "Batch analysis failed",
            "message": str(e)
        }), 500


@app.route('/stats', methods=['GET'])
def get_stats():
    """Get API statistics"""
    return jsonify({
        "total_requests": request_count,
        "phishing_detected": phishing_detected_count,
        "safe_urls": request_count - phishing_detected_count,
        "detection_rate": round((phishing_detected_count / max(request_count, 1)) * 100, 1),
        "model_info": {
            "type": "Ensemble (Random Forest + Gradient Boosting)",
            "features": 15,
            "accuracy": "96%+"
        },
        "timestamp": datetime.now().isoformat()
    })


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "phishing-detector",
        "timestamp": datetime.now().isoformat()
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"🌐 Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
