
# 🧪 Testing Guide - Phishing Shield

Comprehensive testing procedures for all components.

## Unit Tests - Backend

### Test 1: Model Feature Extraction

```python
# test_model.py
from model import PhishingDetector

detector = PhishingDetector()

# Test feature extraction
test_urls = [
    "https://www.google.com",
    "http://192.168.1.1/attack",
    "http://secure-verify-login.tk"
]

for url in test_urls:
    features = detector.extract_features(url)
    assert len(features) == 15, f"Expected 15 features, got {len(features)}"
    assert all(0 <= f <= 1 for f in features), "Features must be between 0-1"
    print(f"✅ {url}: {len(features)} features extracted")
```

### Test 2: Prediction Accuracy

```python
from model import PhishingDetector

detector = PhishingDetector()

# Known safe URLs
safe_urls = [
    "https://www.google.com",
    "https://github.com",
    "https://www.stackoverflow.com",
    "https://www.python.org"
]

# Known phishing patterns
phishing_urls = [
    "http://verify-account-login.tk",
    "http://secure-paypal-update.xyz",
    "http://192.168.1.1/admin",
    "http://bank-login-confirmation.ru"
]

safe_correct = 0
for url in safe_urls:
    result = detector.predict(url)
    if not result['is_phishing']:
        safe_correct += 1
        print(f"✅ PASS: {url} correctly identified as SAFE")
    else:
        print(f"❌ FAIL: {url} incorrectly flagged as phishing")

phishing_correct = 0
for url in phishing_urls:
    result = detector.predict(url)
    if result['is_phishing']:
        phishing_correct += 1
        print(f"✅ PASS: {url} correctly identified as PHISHING")
    else:
        print(f"❌ FAIL: {url} not detected as phishing")

print(f"\nAccuracy: {(safe_correct + phishing_correct) / (len(safe_urls) + len(phishing_urls)) * 100:.1f}%")
```

---

## Integration Tests - API

### Test API Endpoints

```bash
#!/bin/bash
# test_api.sh

API="http://localhost:5001"

echo "🧪 Testing Phishing Shield API..."
echo ""

# Test 1: Health Check
echo "Test 1: Health Check"
curl -s $API/health | jq .
echo ""

# Test 2: Check Safe URL
echo "Test 2: Check Safe URL"
curl -s -X POST $API/check \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.google.com"}' | jq .
echo ""

# Test 3: Check Phishing URL
echo "Test 3: Check Phishing URL"
curl -s -X POST $API/check \
  -H "Content-Type: application/json" \
  -d '{"url":"http://verify-login.tk"}' | jq .
echo ""

# Test 4: Batch Check
echo "Test 4: Batch Check (3 URLs)"
curl -s -X POST $API/batch \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [
      "https://www.google.com",
      "http://suspect-login.tk",
      "https://github.com"
    ]
  }' | jq .
echo ""

# Test 5: Stats
echo "Test 5: Statistics"
curl -s $API/stats | jq .
echo ""

echo "✅ All API tests completed!"
```

### Expected Response Format

```json
{
  "url": "https://www.google.com",
  "is_phishing": false,
  "confidence": 0.95,
  "phishing_probability": 0.05,
  "legitimate_probability": 0.95,
  "risk_level": "LOW",
  "features": {
    "url_length": 23,
    "has_https": true,
    "has_suspicious_words": false,
    "has_ip_address": false
  },
  "reasons": ["No obvious phishing indicators"],
  "timestamp": "2026-03-31T10:30:00.000000",
  "api_version": "1.0.0",
  "status": "success"
}
```

---

## UI Tests - Extension

### Test 1: Extension Popup

1. **Load Extension**:
   - Open `chrome://extensions`
   - Enable Developer Mode
   - Click "Load unpacked"
   - Select `extension/` folder
   - Verify icon appears in toolbar

2. **Open Popup**:
   - Click extension icon
   - Should see "API Checking..."
   - Should show "API Online" ✅

3. **Display Current URL**:
   - Popup should show current page URL
   - URL should be truncated if >50 chars

4. **Analyze Button**:
   - Click "🔍 Analyze Site"
   - Should show loading spinner
   - After 2-5 seconds, should show results

### Test 2: Result Display

**Safe Site** (https://www.google.com):
- ✅ Shows green "SAFE" badge
- ✅ Risk level: "LOW"
- ✅ HTTPS: ✓ Yes
- ✅ Confidence bar green, <20%

**Phishing Site** (http://suspicious-login.tk):
- 🚨 Shows red "PHISHING" badge
- ✅ Risk level: "HIGH" or "CRITICAL"
- ✅ HTTPS: ✗ No
- ✅ Confidence bar red, >80%

### Test 3: Feature Display

All four security features should populate:
- HTTPS status (✓ or ✗)
- URL length (number of chars)
- Suspicious words (Found or None)
- IP address (Yes or No)

### Test 4: Settings Page

1. Right-click extension icon → Options
2. Should see:
   - Statistics (Sites Checked, Threats Detected, Accuracy)
   - Auto-check toggle (checked by default)
   - Show notifications toggle (checked)
   - Save Settings button
   - Clear Cache button

3. Test functionality:
   - Toggle checkboxes
   - Click "Save Settings"
   - Should show confirmation
   - Verify settings persist on reload

---

## Manual Testing Scenarios

### Scenario 1: Safe Website Check

```
1. Navigate to: https://www.google.com
2. Click extension icon
3. Verify:
   - URL displays correctly
   - API shows "Online" (green)
   - "Analyze Site" button appears
4. Click "Analyze Site"
5. Verify results:
   - ✅ SAFE badge appears (green)
   - Risk Level: LOW
   - HTTPS: ✓ Yes
   - Confidence: >90%
6. Click "Analyze Again" to test re-analysis
```

### Scenario 2: Phishing Pattern Detection

```
1. Navigate to: http://secure-login-verify-account.tk
2. Click extension icon
3. Click "Analyze Site"
4. Verify results:
   - 🚨 PHISHING badge (red)
   - Risk Level: High or Critical
   - Reason shown: "Suspicious keywords detected" or "No HTTPS"
   - Confidence: >70%
```

### Scenario 3: Batch Checking

```
1. Open terminal
2. Run:
   curl -X POST http://localhost:5001/batch \
     -H "Content-Type: application/json" \
     -d '{
       "urls": [
         "https://www.google.com",
         "https://github.com",
         "http://phishing-site.tk",
         "https://wikipedia.org"
       ]
     }'
3. Verify:
   - 4 results returned
   - Safe sites: 3
   - Phishing: 1
   - Summary stats correct
```

### Scenario 4: API Offline Handling

```
1. Stop Flask server: Ctrl+C
2. Click extension icon
3. Verify:
   - Status shows "API Offline" (red)
   - Click "Analyze Site"
   - Error message appears: "API Offline"
   - Friendly error with instructions shown
4. Restart server:
   python app.py
5. Refresh popup
6. Status changes to "API Online"
```

---

## Performance Testing

### Test 1: Response Time

Expected response times:
- Single URL check: <500ms
- Batch 10 URLs: <3 seconds
- Stats endpoint: <100ms

```bash
# Measure response time
time curl -X POST http://localhost:5001/check \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'

# Should see real time < 1 second
```

### Test 2: Load Testing

```bash
# Test 100 concurrent requests
ab -n 100 -c 10 http://localhost:5001/health

# Verify:
# - All requests succeed
# - No timeouts
# - Average response < 100ms
```

---

## Browser Compatibility Testing

| Browser | Extension | Version | Status |
|---------|-----------|---------|--------|
| Chrome  | MV3       | Latest  | ✅ Tested |
| Edge    | MV3       | Latest  | ✅ Should work |
| Brave   | MV3       | Latest  | ✅ Should work |
| Firefox | N/A       | N/A     | ❌ Different manifest |

---

## Edge Cases to Test

1. **Empty URL**: `""`
   - Should return error: "Invalid URL length"

2. **Very Long URL**: 2000+ characters
   - Should return error: "Invalid URL length"

3. **Invalid URL**: `"not a url!!!"`
   - Should still process and not crash
   - Should add `http://` scheme

4. **URLs without scheme**:
   - Input: `"google.com"`
   - Should convert to: `"http://google.com"`

5. **Special characters**:
   - URLs with emoji, unicode
   - Should handle without crashing

6. **Batch with invalid data**:
   - Input: `{"urls": "not an array"}`
   - Should return error

7. **Network delay** (simulate):
   - Use browser DevTools throttling
   - Extension should still function

---

## Automated Test Script

```python
# run_all_tests.py
import requests
import json
import time

API_URL = 'http://localhost:5001'

def test_api():
    """Run all API tests"""
    print("🧪 Running API Tests...")
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Health
    try:
        r = requests.get(f'{API_URL}/health', timeout=5)
        assert r.status_code == 200
        print("✅ Health check passed")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        tests_failed += 1
    
    # Test 2: Safe URL
    try:
        r = requests.post(f'{API_URL}/check',
            json={'url': 'https://www.google.com'},
            timeout=5)
        assert r.status_code == 200
        data = r.json()
        assert not data['is_phishing']
        print("✅ Safe URL detection passed")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Safe URL test failed: {e}")
        tests_failed += 1
    
    # Test 3: Phishing URL
    try:
        r = requests.post(f'{API_URL}/check',
            json={'url': 'http://verify-login.tk'},
            timeout=5)
        assert r.status_code == 200
        data = r.json()
        assert data['is_phishing']
        print("✅ Phishing URL detection passed")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Phishing URL test failed: {e}")
        tests_failed += 1
    
    # Test 4: Stats
    try:
        r = requests.get(f'{API_URL}/stats')
        assert r.status_code == 200
        data = r.json()
        assert 'total_requests' in data
        print("✅ Stats endpoint passed")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Stats test failed: {e}")
        tests_failed += 1
    
    print(f"\n📊 Results: {tests_passed} passed, {tests_failed} failed")
    return tests_failed == 0

if __name__ == '__main__':
    success = test_api()
    exit(0 if success else 1)
```

---

## ✅ Final Checklist

- [ ] All backend unit tests pass
- [ ] All API endpoints respond correctly
- [ ] Extension loads without errors
- [ ] Extension popup displays properly
- [ ] Safe URLs identified correctly
- [ ] Phishing URLs identified correctly
- [ ] Settings persist after save
- [ ] Notifications trigger for high-risk sites
- [ ] Performance meets <500ms requirement
- [ ] No console errors in DevTools
- [ ] Landing page demo works
- [ ] Batch endpoints handle edge cases
- [ ] API gracefully handles network errors

---

**Testing Complete!** ✅ All systems ready for deployment.
