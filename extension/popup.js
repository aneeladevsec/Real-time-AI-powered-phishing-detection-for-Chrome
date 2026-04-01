// API Configuration
const API_URL = 'http://localhost:5001';  // For local testing
// Change to: const API_URL = 'https://phishing-detector-api.onrender.com'; for production

// State
let currentUrl = '';
let checkCount = 0;

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
  // Get current tab
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  currentUrl = tab.url;
  
  // Display URL (truncated)
  const displayUrl = currentUrl.length > 50 
    ? currentUrl.substring(0, 50) + '...' 
    : currentUrl;
  document.getElementById('current-url').textContent = displayUrl;
  
  // Check API status
  checkApiStatus();
  
  // Load check count
  const stored = await chrome.storage.local.get(['checkCount']);
  checkCount = stored.checkCount || 0;
  document.getElementById('request-count').textContent = checkCount;
  
  // Event listeners
  document.getElementById('check-btn').addEventListener('click', analyzeSite);
  document.getElementById('report-btn').addEventListener('click', reportPhishing);
});

// Check API status
async function checkApiStatus() {
  const statusEl = document.getElementById('api-status');
  
  try {
    const response = await fetch(`${API_URL}/health`, { 
      method: 'GET'
    });
    
    if (response.ok) {
      statusEl.textContent = 'API Online';
      statusEl.className = 'status online';
    } else {
      throw new Error('API Error');
    }
  } catch (err) {
    statusEl.textContent = 'API Offline';
    statusEl.className = 'status offline';
  }
}

// Analyze current site
async function analyzeSite() {
  const btn = document.getElementById('check-btn');
  const resultSection = document.getElementById('result-section');
  
  btn.disabled = true;
  btn.innerHTML = '<span class="loading"></span> Analyzing...';
  
  try {
    const response = await fetch(`${API_URL}/check`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: currentUrl })
    });
    
    if (!response.ok) {
      throw new Error('API request failed');
    }
    
    const data = await response.json();
    
    // Update UI
    updateUI(data);
    
    // Update count
    checkCount++;
    await chrome.storage.local.set({ checkCount });
    document.getElementById('request-count').textContent = checkCount;
    
    // Notify if phishing
    if (data.is_phishing && data.confidence > 0.7) {
      chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icons/shield128.png',
        title: '⚠️ Phishing Detected!',
        message: `High risk site: ${new URL(currentUrl).hostname}`,
        priority: 2
      });
    }
    
  } catch (err) {
    resultSection.innerHTML = `
      <p style="color: #ff6b6b;">Error: ${err.message}</p>
      <p style="font-size: 0.8rem; color: #888;">Make sure the API server is running on port 5001</p>
    `;
  } finally {
    btn.disabled = false;
    btn.textContent = '🔍 Analyze Again';
  }
}

// Update UI with results
function updateUI(data) {
  const riskBadge = document.getElementById('risk-badge');
  const confidenceFill = document.getElementById('confidence-fill');
  const confidenceText = document.getElementById('confidence-text');
  
  // Risk badge
  const riskClass = `risk-${data.risk_level.toLowerCase()}`;
  riskBadge.className = `risk-badge ${riskClass}`;
  riskBadge.textContent = data.risk_level;
  
  // Features
  const features = data.features;
  document.getElementById('feat-https').innerHTML = features.has_https 
    ? '<span class="feature-safe">✓ Yes</span>' 
    : '<span class="feature-danger">✗ No</span>';
  
  const lengthStatus = features.url_length > 75 ? 'feature-warning' : 'feature-safe';
  document.getElementById('feat-length').innerHTML = 
    `<span class="${lengthStatus}">${features.url_length} chars</span>`;
  
  document.getElementById('feat-suspicious').innerHTML = features.has_suspicious_words
    ? '<span class="feature-danger">⚠️ Found</span>'
    : '<span class="feature-safe">✓ None</span>';
  
  document.getElementById('feat-ip').innerHTML = features.has_ip_address
    ? '<span class="feature-danger">⚠️ Yes</span>'
    : '<span class="feature-safe">✓ No</span>';
  
  // Confidence bar
  const phishingPercent = data.phishing_probability * 100;
  confidenceFill.style.width = `${phishingPercent}%`;
  
  // Confidence text
  const status = data.is_phishing ? 'PHISHING' : 'SAFE';
  const icon = data.is_phishing ? '⚠️' : '✅';
  confidenceText.innerHTML = `
    <strong style="font-size: 1.2rem; color: ${data.is_phishing ? '#ff6b6b' : '#2ed573'}">
      ${icon} ${status}
    </strong><br>
    <span style="font-size: 0.85rem; color: #888;">
      Confidence: ${(data.confidence * 100).toFixed(1)}%<br>
      ${data.reasons[0]}
    </span>
  `;
}

// Report phishing (placeholder)
function reportPhishing() {
  alert('Thank you for reporting! This helps improve our detection.\n\nIn production, this would submit to Google Safe Browsing and PhishTank.');
}
