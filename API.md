# 📚 API Documentation - Phishing Shield

## Base URL

### Development
```
http://localhost:5001
```

### Production
```
https://phishing-detector-api.onrender.com
```

---

## Endpoints

### 1. Health Check

Check if API is running and healthy.

**Request:**
```http
GET /health
```

**Response:** `200 Ok`
```json
{
  "status": "healthy",
  "service": "phishing-detector",
  "timestamp": "2026-03-31T10:30:00.000000"
}
```

---

### 2. Check Single URL

Analyze a single URL for phishing.

**Request:**
```http
POST /check
Content-Type: application/json

{
  "url": "https://www.example.com"
}
```

**Parameters:**
- `url` (string, required): URL to check (with or without scheme)

**Response:** `200 OK`
```json
{
  "url": "https://www.example.com",
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

**Error Response:** `400 Bad Request`
```json
{
  "error": "URL required",
  "usage": {
    "url": "https://example.com"
  }
}
```

---

### 3. Check Batch URLs

Analyze multiple URLs at once (max 20).

**Request:**
```http
POST /batch
Content-Type: application/json

{
  "urls": [
    "https://www.google.com",
    "http://suspicious-site.tk",
    "https://github.com"
  ]
}
```

**Parameters:**
- `urls` (array, required): Array of URLs to check
  - Maximum 20 URLs per request
  - Each URL can be with or without scheme

**Response:** `200 OK`
```json
{
  "results": [
    {
      "url": "https://www.google.com",
      "is_phishing": false,
      "confidence": 0.95,
      "phishing_probability": 0.05,
      "risk_level": "LOW",
      "reasons": ["No obvious phishing indicators"]
    },
    {
      "url": "http://suspicious-site.tk",
      "is_phishing": true,
      "confidence": 0.92,
      "phishing_probability": 0.92,
      "risk_level": "CRITICAL",
      "reasons": [
        "Suspicious keywords detected",
        "No HTTPS encryption",
        "Unusual domain"
      ]
    }
  ],
  "summary": {
    "total": 2,
    "phishing_detected": 1,
    "safe": 1,
    "phishing_percentage": 50.0
  },
  "timestamp": "2026-03-31T10:30:00.000000"
}
```

**Error Response:** `400 Bad Request`
```json
{
  "error": "URLs array required"
}
```

---

### 4. Get Statistics

Get API usage statistics.

**Request:**
```http
GET /stats
```

**Response:** `200 OK`
```json
{
  "total_requests": 150,
  "phishing_detected": 23,
  "safe_urls": 127,
  "detection_rate": 15.3,
  "model_info": {
    "type": "Ensemble (Random Forest + Gradient Boosting)",
    "features": 15,
    "accuracy": "96%+"
  },
  "timestamp": "2026-03-31T10:30:00.000000"
}
```

---

### 5. API Home

Get API information and available endpoints.

**Request:**
```http
GET /
```

**Response:** `200 OK`
```json
{
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
  "timestamp": "2026-03-31T10:30:00.000000"
}
```

---

## Response Fields Explained

### is_phishing (boolean)
- `true`: URL is identified as phishing
- `false`: URL appears legitimate

### confidence (float, 0-1)
- Overall prediction confidence (0.5-1.0 range)
- Represents the model's certainty

### phishing_probability (float, 0-1)
- Probability the URL is phishing (0-1 range)
- Higher = more likely to be phishing

### legitimate_probability (float, 0-1)
- Probability the URL is legitimate (0-1 range)
- Sum of phishing_prob + legitimate_prob = 1.0

### risk_level (string)
- `LOW`: Confidence < 0.4 (phishing_prob < 0.4)
- `MEDIUM`: Confidence 0.4-0.6
- `HIGH`: Confidence 0.6-0.8
- `CRITICAL`: Confidence > 0.8

### reasons (array)
List of detected risk factors:
- "Contains IP address instead of domain"
- "Suspicious keywords detected"
- "Unusually long URL"
- "Excessive subdomains"
- "No HTTPS encryption"
- "No obvious phishing indicators"

### features (object)
Breaking down individual security features:
- `url_length`: Normalized URL length (0-100+)
- `has_https`: Boolean (true/false)
- `has_suspicious_words`: Boolean (true/false)
- `has_ip_address`: Boolean (true/false)

---

## Usage Examples

### Using cURL

```bash
# Single check
curl -X POST http://localhost:5001/check \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.google.com"}'

# Batch check
curl -X POST http://localhost:5001/batch \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [
      "https://www.google.com",
      "http://phishing.tk"
    ]
  }'

# Search statistics
curl http://localhost:5001/stats
```

### Using JavaScript/Fetch

```javascript
// Single URL
async function checkURL(url) {
  const response = await fetch('http://localhost:5001/check', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ url })
  });
  const data = await response.json();
  console.log(data);
  return data;
}

// Batch URLs
async function checkBatch(urls) {
  const response = await fetch('http://localhost:5001/batch', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ urls })
  });
  const data = await response.json();
  return data;
}
```

### Using Python/Requests

```python
import requests

# Single check
response = requests.post(
    'http://localhost:5001/check',
    json={'url': 'https://www.google.com'}
)
result = response.json()
print(result)

# Batch check
response = requests.post(
    'http://localhost:5001/batch',
    json={'urls': ['https://google.com', 'http://phishing.tk']}
)
result = response.json()
print(result)

# Get stats
response = requests.get('http://localhost:5001/stats')
stats = response.json()
print(stats)
```

---

## Error Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Missing or invalid parameters |
| 500 | Internal Server Error | Server-side error |

---

## Rate Limiting

Currently **no rate limiting** (can be added in production).

**Recommended for production:**
- 100 requests/minute per IP
- 1000 requests/hour per IP

---

## Authentication

Currently **no authentication required** (can be added later).

For production, consider adding:
```javascript
// API key in header
Authorization: Bearer YOUR_API_KEY
```

---

## CORS Headers

The API supports Cross-Origin Requests (CORS):

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

---

## Performance

### Expected Response Times
- Single URL check: 100-500ms
- Batch 10 URLs: 500-2000ms
- Statistics: 50-100ms
- Health check: 10-50ms

### Timeout Recommendations
- Individual requests: 5 seconds
- Batch requests: 10 seconds

---

## Versioning

Current API Version: **1.0.0**

Version string included in all responses:
```json
{
  "api_version": "1.0.0"
}
```

---

## Data Privacy

✅ **No data collection**
- URLs are NOT stored in database
- No analytics or tracking
- No personal data collected
- Results computed in-memory only

---

## Example Workflow

```javascript
async function analyzeWebsite() {
  // 1. Get current tab
  const [tab] = await chrome.tabs.query({ active: true });
  
  // 2. Call API
  const response = await fetch('http://API_URL/check', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url: tab.url })
  });
  
  const result = await response.json();
  
  // 3. Handle result
  if (result.is_phishing && result.risk_level === 'CRITICAL') {
    // Show alert
    chrome.notifications.create({
      type: 'basic',
      title: '⚠️ Phishing Alert',
      message: result.reasons[0]
    });
  }
  
  // 4. Display UI
  updateUI(result);
}
```

---

## Troubleshooting

### Issue: Connection Refused
```
Error: connect ECONNREFUSED 127.0.0.1:5001

Solution:
1. Ensure Flask API is running: python app.py
2. Check if port 5001 is in use: netstat -ano | findstr :5001
3. Try different port: PORT=5002 python app.py
```

### Issue: Timeout
```
Error: Request timed out

Solution:
1. Increase timeout in client code
2. Check system resources
3. Verify network connectivity
4. Try simpler URL first
```

### Issue: Invalid Response
```
Error: JSON parse error

Solution:
1. Verify API is running
2. Check request format
3. Validate JSON in body
4. Check Content-Type header
```

---

## Support

For issues or questions:
1. Check this documentation
2. Review error messages carefully
3. Check server logs: `stdout` in terminal
4. Test with cURL first
5. Open issue on GitHub

---

**Last Updated**: March 2026
**Status**: Production Ready ✅
