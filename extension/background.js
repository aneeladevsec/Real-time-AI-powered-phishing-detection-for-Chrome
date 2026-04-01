// Background service worker for Phishing Shield
// Handles real-time detection and caching

const API_URL = 'http://localhost:5001';
const CACHE_DURATION = 300000; // 5 minutes

// Site cache to avoid repeated checks
const checkedSites = new Map();

// Initialize on install
chrome.runtime.onInstalled.addListener(() => {
  console.log('🛡️ Phishing Shield installed');
  
  chrome.storage.local.set({
    checkCount: 0,
    blockedCount: 0,
    settings: {
      autoCheck: true,
      showNotifications: true,
      blockHighRisk: false
    }
  });
});

// Listen for tab updates
chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    // Skip chrome pages
    if (tab.url.startsWith('chrome://') || tab.url.startsWith('chrome-extension://')) {
      return;
    }
    
    // Check if auto-check enabled
    const { settings } = await chrome.storage.local.get(['settings']);
    
    if (settings?.autoCheck) {
      await checkSite(tabId, tab.url);
    }
  }
});

// Check site and update badge
async function checkSite(tabId, url) {
  // Check cache (5 minutes)
  const cached = checkedSites.get(url);
  if (cached && Date.now() - cached.time < CACHE_DURATION) {
    updateBadge(tabId, cached.result);
    return;
  }
  
  try {
    const response = await fetch(`${API_URL}/check`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });
    
    if (!response.ok) throw new Error('API Error');
    
    const data = await response.json();
    
    // Cache result
    checkedSites.set(url, {
      result: data,
      time: Date.now()
    });
    
    // Update badge
    updateBadge(tabId, data);
    
    // Notify if high risk
    if (data.is_phishing && data.risk_level === 'CRITICAL') {
      chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icons/shield128.png',
        title: '🚨 Critical Phishing Site!',
        message: `${new URL(url).hostname} is a known phishing site. Leave immediately!`,
        priority: 2,
        requireInteraction: true
      });
    }
    
  } catch (err) {
    console.error('Check failed:', err);
    chrome.action.setBadgeText({ text: '?', tabId });
  }
}

// Update extension badge
function updateBadge(tabId, data) {
  const isSafe = !data.is_phishing;
  const text = isSafe ? '✓' : '!';
  const color = isSafe ? '#2ed573' : '#e94560';
  
  chrome.action.setBadgeText({ text, tabId });
  chrome.action.setBadgeBackgroundColor({ color, tabId });
  
  // Set title
  const title = isSafe 
    ? `✅ Safe: ${(data.confidence * 100).toFixed(0)}% confident`
    : `🚨 ${data.risk_level} RISK: ${(data.phishing_probability * 100).toFixed(0)}% phishing`;
  
  chrome.action.setTitle({ title, tabId });
}

// Handle messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getCache') {
    const cached = checkedSites.get(request.url);
    sendResponse(cached ? cached.result : null);
  }
  return true;
});
