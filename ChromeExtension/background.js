// Service worker - handles API calls
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'ANALYZE_DOMAIN') {
      analyzeSafety(request.domain)
        .then(result => chrome.storage.local.set({[request.domain]: result}));
    }
  });
  
  async function analyzeSafety(domain) {
    const API_KEY = await chrome.storage.local.get('cohereKey');
    
    const response = await fetch('https://api.cohere.ai/v1/analyze', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        "domain": domain,
        "features": ["safety_check", "similar_sites"]
      })
    });
  
    return response.json();
  }
  